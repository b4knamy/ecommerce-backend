from django.contrib import admin
from .models import PaymentOrder, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ("order", "product", "color", "quantitaty")


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):

    readonly_fields = ("user", "payment_method", "is_installment", "created_at")
    exclude = ("checkout_id",)
