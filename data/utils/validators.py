from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def min_and_max_discount_value_validator(value: int) -> None | ValidationError:
    if value > 100 or value < 0:
        raise ValidationError(
            _("O percentual de desconto não pode ser menor que 0 ou maior que 100 "))
