from django_filters import rest_framework as filter
from .models import Glasses


class CharInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class GlassesFilter(filter.FilterSet):
    categoria = CharInFilter(field_name="category__slug", lookup_expr="in")
    marca = CharInFilter(field_name="brand__slug", lookup_expr="in")
    formato = CharInFilter(field_name="shape__slug", lookup_expr="in")
    modelo = CharInFilter(field_name="model__slug", lookup_expr="in")
    cor = CharInFilter(field_name="color__slug", lookup_expr="in")
    max = filter.NumberFilter(field_name="amount", lookup_expr="lte")
    min = filter.NumberFilter(field_name="amount", lookup_expr="gte")
    ordem = filter.OrderingFilter(
        fields=(
            ("amount", "ASC"),
            ("-amount", "DESC")
        )
    )

    class Meta:
        model = Glasses

        fields = ["category", "shape", "brand", "amount", "model", "color"]
