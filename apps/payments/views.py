import hmac
import hashlib
import json
import logging
import uuid as _uuid
from decimal import Decimal

import requests as http_client
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order, OrderItem, Cart, ShippingAddress
from apps.shipping.models import ShippingConfig
from apps.products.models import InchPricing
from .models import Payment

logger = logging.getLogger(__name__)


def _usd_to_paystack_amount(usd_total: Decimal) -> int:
    """
    Convert a USD decimal total to the smallest Paystack currency unit.

    - KES: multiply by rate, then × 100 (kobo/cents)
    - USD: multiply by 100 (cents)

    Paystack always wants the amount in the LOWEST denomination.
    e.g. KES 100 = 10000, USD 1.00 = 100
    """
    currency = getattr(settings, 'PAYSTACK_CURRENCY', 'KES')
    if currency == 'KES':
        rate = getattr(settings, 'USD_TO_KES_RATE', 130)
        kes_total = usd_total * rate
        return int(kes_total * 100)
    elif currency == 'USD':
        return int(usd_total * 100)
    elif currency == 'NGN':
        # Nigerian Naira — convert via rate if stored in USD
        rate = getattr(settings, 'USD_TO_NGN_RATE', 1500)
        return int(usd_total * rate * 100)
    elif currency == 'GHS':
        rate = getattr(settings, 'USD_TO_GHS_RATE', 12)
        return int(usd_total * rate * 100)
    # Default fallback: treat as cents
    return int(usd_total * 100)


class InitializePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shipping_data = request.data.get('shipping_address', {})
        cart_items    = request.data.get('cart_items', [])

        if not cart_items:
            return Response(
                {'status': 400, 'message': 'Your cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── Validate required shipping fields ────────────────────────────────
        required = ['full_name', 'email', 'phone', 'address_line1', 'city', 'country']
        missing  = [f for f in required if not shipping_data.get(f)]
        if missing:
            return Response(
                {'status': 400, 'message': f'Missing shipping fields: {", ".join(missing)}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── Shipping config ──────────────────────────────────────────────────
        shipping_config = ShippingConfig.objects.filter(is_active=True).first()
        shipping_fee    = shipping_config.fee_usd if shipping_config else Decimal('12.00')
        est_delivery    = (
            f"{shipping_config.estimated_days_min}–{shipping_config.estimated_days_max} business days"
            if shipping_config else '8–15 business days'
        )

        # ── Resolve cart items and build order ───────────────────────────────
        subtotal       = Decimal('0.00')
        items_snapshot = []

        for item in cart_items:
            inch_pricing_id = item.get('inch_pricing_id')
            quantity        = max(1, int(item.get('quantity', 1)))

            try:
                pricing = InchPricing.objects.select_related('product').get(
                    id=inch_pricing_id, is_available=True
                )
            except InchPricing.DoesNotExist:
                return Response(
                    {'status': 400, 'message': f'Selected item is no longer available.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            line_total = pricing.price * quantity
            subtotal  += line_total
            items_snapshot.append({
                'pricing': pricing,
                'quantity': quantity,
                'line_total': line_total,
            })

        usd_total = subtotal + shipping_fee

        # ── Create shipping address ──────────────────────────────────────────
        address = ShippingAddress.objects.create(
            user=request.user,
            full_name     = shipping_data.get('full_name', ''),
            email         = shipping_data.get('email', request.user.email),
            phone         = shipping_data.get('phone', ''),
            address_line1 = shipping_data.get('address_line1', ''),
            address_line2 = shipping_data.get('address_line2', ''),
            city          = shipping_data.get('city', ''),
            state         = shipping_data.get('state', ''),
            country       = shipping_data.get('country', 'Kenya'),
            postal_code   = shipping_data.get('postal_code', ''),
        )

        # ── Create pending order ─────────────────────────────────────────────
        order = Order.objects.create(
            user             = request.user,
            shipping_address = address,
            subtotal         = subtotal,
            shipping_fee     = shipping_fee,
            total            = usd_total,
            status           = 'pending',
            estimated_delivery = est_delivery,
        )
        OrderItem.objects.bulk_create([
            OrderItem(
                order        = order,
                product      = snap['pricing'].product,
                product_name = snap['pricing'].product.name,
                inches       = snap['pricing'].inches,
                unit_price   = snap['pricing'].price,
                quantity     = snap['quantity'],
                subtotal     = snap['line_total'],
            )
            for snap in items_snapshot
        ])

        # ── Build unique Paystack reference ──────────────────────────────────
        reference = f"SOIE-{_uuid.uuid4().hex[:14].upper()}"

        # ── Convert amount to Paystack's smallest currency unit ──────────────
        paystack_amount = _usd_to_paystack_amount(usd_total)
        currency        = getattr(settings, 'PAYSTACK_CURRENCY', 'KES')
        frontend_url    = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')

        # ── Call Paystack initialize endpoint ────────────────────────────────
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type':  'application/json',
        }
        payload = {
            'email':        request.user.email,
            'amount':       paystack_amount,
            'currency':     currency,
            'reference':    reference,
            'callback_url': f'{frontend_url}/checkout/verify?reference={reference}',
            'metadata': {
                'order_id':     str(order.id),
                'order_number': order.order_number,
                'user_id':      str(request.user.id),
                'usd_total':    str(usd_total),
                'currency_display': f'${usd_total} USD',
                'cancel_action': f'{frontend_url}/checkout',
            },
            'channels': ['card', 'mobile_money', 'bank_transfer'],
        }

        try:
            resp = http_client.post(
                f'{settings.PAYSTACK_BASE_URL}/transaction/initialize',
                headers=headers,
                json=payload,
                timeout=15,
            )
        except http_client.exceptions.Timeout:
            order.delete()
            return Response(
                {'status': 503, 'message': 'Payment gateway timed out. Please try again.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except http_client.exceptions.RequestException as e:
            logger.error(f'Paystack network error: {e}')
            order.delete()
            return Response(
                {'status': 503, 'message': 'Could not connect to payment gateway. Please try again.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        resp_data = resp.json()

        # ── Log Paystack's full response for debugging ───────────────────────
        logger.info(
            f'Paystack init response [{resp.status_code}]: '
            f'status={resp_data.get("status")} '
            f'message={resp_data.get("message")} '
            f'amount={paystack_amount} currency={currency}'
        )

        if not resp_data.get('status'):
            paystack_msg = resp_data.get('message', 'Unknown error from Paystack.')
            logger.error(f'Paystack init failed for order {order.order_number}: {paystack_msg}')
            # Clean up the pending order since payment didn't start
            order.status = 'cancelled'
            order.save()
            return Response(
                {
                    'status': 400,
                    'message': f'Payment could not be started: {paystack_msg}',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── Save payment record ──────────────────────────────────────────────
        Payment.objects.create(
            order               = order,
            paystack_reference  = reference,
            amount              = usd_total,
            currency            = 'USD',  # store display currency
            status              = 'pending',
        )

        # ── Return access_code (for Popup) + authorization_url (for Redirect)
        return Response({
            'access_code':       resp_data['data']['access_code'],
            'authorization_url': resp_data['data']['authorization_url'],
            'reference':         reference,
            'order_id':          str(order.id),
            'order_number':      order.order_number,
            'amount_display':    f'${usd_total:.2f}',
        })


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reference = request.query_params.get('reference')
        if not reference:
            return Response(
                {'status': 400, 'message': 'Payment reference is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}

        try:
            resp = http_client.get(
                f'{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}',
                headers=headers,
                timeout=15,
            )
        except http_client.exceptions.RequestException as e:
            logger.error(f'Paystack verify network error: {e}')
            return Response(
                {'status': 503, 'message': 'Could not verify payment. Please try again or contact support.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        data = resp.json()
        logger.info(
            f'Paystack verify [{reference}]: '
            f'status={data.get("data", {}).get("status")} '
            f'amount={data.get("data", {}).get("amount")}'
        )

        tx_data = data.get('data', {})
        tx_status = tx_data.get('status')

        if not data.get('status') or tx_status != 'success':
            friendly = {
                'failed':    'Payment failed. Please try a different payment method.',
                'abandoned': 'Payment was cancelled. Your order has not been charged.',
                'timeout':   'Payment timed out. Please try again.',
            }.get(tx_status, f'Payment status: {tx_status}. Please contact support.')
            return Response(
                {'status': 400, 'message': friendly},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ── Verify amount matches ────────────────────────────────────────────
        # (Paystack sends amount in smallest unit; we stored USD total)
        try:
            payment = Payment.objects.select_related('order').get(
                paystack_reference=reference
            )
        except Payment.DoesNotExist:
            return Response(
                {'status': 404, 'message': 'Payment record not found. Contact support.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ── Mark payment and order as successful ─────────────────────────────
        if payment.status != 'success':
            payment.status                  = 'success'
            payment.paystack_transaction_id = str(tx_data.get('id', ''))
            payment.channel                 = tx_data.get('channel', '')
            payment.paid_at                 = timezone.now()
            payment.metadata                = tx_data.get('metadata', {})
            payment.save()

            order = payment.order
            order.status = 'paid'
            order.save()

            # Clear the user's cart
            Cart.objects.filter(user=request.user).delete()

            # Send confirmation email (async via Celery / eager in dev)
            try:
                from apps.accounts.tasks import send_order_confirmation_email
                send_order_confirmation_email.delay(str(order.id))
            except Exception as e:
                logger.warning(f'Could not queue confirmation email: {e}')

        return Response({
            'status':        200,
            'message':       'Payment confirmed successfully.',
            'order_number':  payment.order.order_number,
            'order_id':      str(payment.order.id),
        })


class PaystackWebhookView(APIView):
    """
    Receives Paystack webhook events.
    Register this URL in your Paystack dashboard:
    Settings → API Keys & Webhooks → Webhook URL
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        signature = request.headers.get('x-paystack-signature', '')
        payload   = request.body

        # Verify the webhook signature
        computed = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
            payload,
            hashlib.sha512,
        ).hexdigest()

        if not hmac.compare_digest(computed, signature):
            logger.warning('Paystack webhook: invalid signature')
            return Response(status=400)

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            return Response(status=400)

        logger.info(f'Paystack webhook event: {event.get("event")}')

        if event.get('event') == 'charge.success':
            reference = event['data'].get('reference', '')
            try:
                payment = Payment.objects.select_related('order').get(
                    paystack_reference=reference
                )
                if payment.status != 'success':
                    payment.status  = 'success'
                    payment.paid_at = timezone.now()
                    payment.channel = event['data'].get('channel', '')
                    payment.save()
                    payment.order.status = 'paid'
                    payment.order.save()
                    logger.info(
                        f'Webhook: order {payment.order.order_number} marked as paid'
                    )
            except Payment.DoesNotExist:
                logger.warning(f'Webhook: no payment found for ref {reference}')

        return Response(status=200)