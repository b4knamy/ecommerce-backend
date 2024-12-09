from django.db import models
from authentication.models import User
from data.models import Color, Glasses
from django.utils.translation import gettext_lazy as _
from data.models import AbstractTimeStamp
from datetime import datetime
from random import randint


class PaymentOrder(AbstractTimeStamp):
    edited_at = None
    order_status_choices = (
        ("PEN", _("Pendente")),
        ("CAN", _("Cancelado")),
        ("ENT", _("Entregue"))
    )

    checkout_id = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_("Usuário"), related_name="payment_orders")
    payment_method = models.CharField(
        max_length=50, verbose_name=_("Método de pagamento"))
    is_installment = models.BooleanField(
        default=False, blank=True, verbose_name=_("Está parcelado?"))
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Preço"))

    order_number = models.CharField(_("Numero do Pedido"), max_length=20, default="")
    order_status = models.CharField(
        max_length=3, choices=order_status_choices, default="PEN")

    def __str__(self):
        return f"Pedido do usuário: {self.user.first_name}"

    def get_all_order_items_related(self):
        return OrderItem.objects.filter(order_id=self.pk)

    @property
    def amount_in_real(self):
        return round(self.amount / 100, 2)

    def generate_order_number(self):
        date_str = datetime.now().strftime("%d%m%Y")
        payment_count = PaymentOrder.objects.filter(
            created_at__date=datetime.now().date()
        ).count() + 1
        return f"{date_str}{payment_count:04d}{randint(1000, 9999)}"

    def save(self, *args, **kwargs):
        if not self.order_number or self.order_number == "":
            # TODO: fix that sometime
            self.order_number = self.generate_order_number()
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(PaymentOrder, related_name="order", verbose_name=_("Pedido"),
                              on_delete=models.CASCADE)
    product = models.ForeignKey(
        Glasses, verbose_name=_("Produto"), on_delete=models.CASCADE)
    color = models.ForeignKey(Color, verbose_name=_("Cor"), on_delete=models.CASCADE)
    quantitaty = models.IntegerField(_("Quantidade"))
