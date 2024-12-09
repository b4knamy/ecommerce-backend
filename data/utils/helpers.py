from django.db.models import Count, Max, Min
from data.serializers import AmountMaxMinSerializer, FiltersDataSerializer


def get_filters_serialized_data(model, related_name: str = None, is_amount=False):
    if is_amount:
        amount_data = model.objects.aggregate(
            min=Min("amount"), max=Max("amount"))
        amount_serializer = AmountMaxMinSerializer(amount_data)
        return amount_serializer.data

    filter_data = model.objects.annotate(
        count=Count(related_name)).values("id", "name", "count", "slug")
    filter_data_serializer = FiltersDataSerializer(filter_data, many=True)

    return filter_data_serializer.data


def get_sub_informatios_serialized_data(model, serializer):
    data = model.objects.all().order_by("name")
    serialized_data = serializer(data, many=True)
    return serialized_data.data
