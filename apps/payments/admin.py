from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = (
        'paystack_reference', 'order_link', 'amount_display',
        'status_badge', 'channel', 'paid_at', 'created_at',
    )
    list_filter   = ('status', 'channel', 'currency')
    search_fields = ('paystack_reference', 'paystack_transaction_id', 'order__order_number')
    readonly_fields = (
        'paystack_reference', 'paystack_transaction_id',
        'amount', 'currency', 'channel', 'paid_at',
        'metadata', 'created_at',
    )
    ordering = ('-created_at',)

    def order_link(self, obj):
        if obj.order:
            return format_html(
                '<a href="/admin/orders/order/{}/change/">{}</a>',
                obj.order.id,
                obj.order.order_number,
            )
        return '—'
    order_link.short_description = 'Order'

    def amount_display(self, obj):
        return f'${obj.amount:.2f} {obj.currency}'
    amount_display.short_description = 'Amount'

    def status_badge(self, obj):
        colours = {
            'success':   ('background:#e8f5e9;color:#2e7d32', 'Success'),
            'pending':   ('background:#fff8e1;color:#f57f17', 'Pending'),
            'failed':    ('background:#ffebee;color:#c62828', 'Failed'),
            'abandoned': ('background:#f5f5f5;color:#757575', 'Abandoned'),
        }
        style, label = colours.get(obj.status, ('background:#f5f5f5;color:#333', obj.status))
        return format_html(
            '<span style="{}; padding:3px 10px; border-radius:3px; '
            'font-size:11px; text-transform:uppercase; letter-spacing:0.5px">{}</span>',
            style, label,
        )
    status_badge.short_description = 'Status'