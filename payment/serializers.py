
from data.models import Glasses
from data.serializers import ColorSerializer, ImageSerializer
from rest_framework import serializers
from payment.models import OrderItem, PaymentOrder


class ShoppingGlassesSerializer(serializers.ModelSerializer):
    color = ColorSerializer(required=True, many=True)
    images = serializers.SerializerMethodField()
    currentQTD = serializers.IntegerField(default=1, read_only=True)

    class Meta:
        model = Glasses
        fields = ("id", "color", "name", "quantitaty", "amount", "installments_amount", "installments_count",
                  "warranty", "images", "currentQTD", "slug"
                  )

    def get_images(self, obj):
        if img := obj.images.first():
            return ImageSerializer(img).data
        return None


class PaymentProductSerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()

    class Meta:
        model = Glasses
        fields = ("id", "name", "amount",
                  "warranty", "images", "slug"
                  )

    def get_images(self, obj):
        if img := obj.images.first():
            return ImageSerializer(img).data
        return None


class OrderItemsSerializer(serializers.ModelSerializer):
    product = PaymentProductSerializer(required=True)
    color = ColorSerializer(required=True)

    class Meta:

        model = OrderItem
        fields = ("product", "color", "quantitaty")


class PaymentOrderSerializer(serializers.ModelSerializer):
    order = OrderItemsSerializer(many=True, required=True)
    created_at = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = PaymentOrder
        fields = (
            "payment_method",
            "is_installment",
            "created_at",
            "order",
            "order_number",
            "order_status",
            "amount"
        )
