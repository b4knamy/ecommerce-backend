
from rest_framework import serializers
from .models import Brand, Category, Glasses, Model, Color, Image, Shape


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"


class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = "__all__"


class GlassesModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Model
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = "__all__"


class GlassesSerializer(serializers.ModelSerializer):
    color = ColorSerializer(required=True, many=True)

    class Meta:

        model = Glasses
        fields = "__all__"


class FiltersDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    count = serializers.IntegerField()
    slug = serializers.CharField(max_length=150)


class AmountMaxMinSerializer(serializers.Serializer):
    min = serializers.DecimalField(max_digits=10, decimal_places=2)
    max = serializers.DecimalField(max_digits=10, decimal_places=2)


class GlassesCardSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    final_amount = serializers.SerializerMethodField()

    class Meta:

        model = Glasses
        fields = ("id", "name", "is_promo", "slug", "amount", "installments_amount",
                  "installments_count", "images", "final_amount", "discount")

    def get_images(self, obj: Glasses):
        if img := obj.images.first():
            return ImageSerializer(img).data
        return None

    def get_final_amount(self, obj: Glasses):
        return obj.final_amount


class GlassesProfileSerializer(serializers.ModelSerializer):
    color = ColorSerializer(required=True, many=True)
    category = CategorySerializer(required=True, many=True)
    shape = ShapeSerializer(required=True, many=True)
    brand = BrandSerializer(required=True, many=True)
    model = GlassesModelSerializer(required=True, many=True)
    images = ImageSerializer(required=True, many=True)
    final_amount = serializers.SerializerMethodField()

    def get_final_amount(self, obj: Glasses):
        return obj.final_amount

    class Meta:

        model = Glasses
        fields = "__all__"


class GlassesDynamicSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:

        model = Glasses
        fields = ("id", "name", "quantitaty", "amount", "slug", "images")

    def get_images(self, obj):
        if img := obj.images.first():
            return ImageSerializer(img).data
        return None
