from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def _send_mail(subject: str, template: str, context: dict, to: str):
    """Helper that actually sends the email, usable synchronously too."""
    try:
        html_content = render_to_string(template, context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=subject,  # plain-text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.error(f"Email send failed to {to}: {e}")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_id: str):
    from apps.accounts.models import User
    try:
        user = User.objects.get(id=user_id)
        _send_mail(
            subject="Welcome to SOIE — Your Luxury Begins Here",
            template="emails/welcome.html",
            context={"user": user, "frontend_url": settings.FRONTEND_URL, "brand_name": "SOIE"},
            to=user.email,
        )
    except Exception as exc:
        logger.error(f"send_welcome_email error: {exc}")
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            pass


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation_email(self, order_id: str):
    from apps.orders.models import Order
    try:
        order = Order.objects.select_related("user").prefetch_related("items__product").get(id=order_id)
        _send_mail(
            subject=f"Order Confirmed — SOIE #{order.order_number}",
            template="emails/order_confirmation.html",
            context={"order": order, "user": order.user, "frontend_url": settings.FRONTEND_URL, "brand_name": "SOIE"},
            to=order.user.email,
        )
    except Exception as exc:
        logger.error(f"send_order_confirmation_email error: {exc}")
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            pass


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_shipping_update_email(self, order_id: str):
    from apps.orders.models import Order
    try:
        order = Order.objects.select_related("user").get(id=order_id)
        _send_mail(
            subject=f"Your SOIE Order is On Its Way — #{order.order_number}",
            template="emails/shipping_update.html",
            context={"order": order, "user": order.user, "frontend_url": settings.FRONTEND_URL, "brand_name": "SOIE"},
            to=order.user.email,
        )
    except Exception as exc:
        logger.error(f"send_shipping_update_email error: {exc}")
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            pass