
from rest_framework import serializers
from .models import CommentsMedia, Comments
from authentication.serializers import SimpleUserSerializer
from data.serializers import ColorSerializer
from core.settings import FILE_UPLOAD_MAX_MEMORY_SIZE, FILE_UPLOAD_MAX_MEMORY_SIZE_MB, MAX_FILE_PER_COMMENT


class CommentsMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsMedia
        fields = ["id", "image"]


class CommentsSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(required=True)
    images_comments = CommentsMediaSerializer(required=True, many=True)
    color = ColorSerializer(required=True)
    created_at = serializers.DateTimeField(format="ás %H:%Mhrs, %d/%m/%Y")

    class Meta:

        model = Comments
        fields = ("id",  "user", "text", "title",
                  "rating", 'images_comments', "created_at", "color")


class SaveCommentsSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(write_only=True, required=False), write_only=True, required=False
    )

    class Meta:
        model = Comments
        fields = ("id", "glasses", "color", "rating", "user",
                  "title", "text", "images", "has_images")

    def create(self, validated_data):
        images = validated_data.pop("images", None)

        comment = Comments.objects.create(**validated_data)

        if images:
            comment.has_images = True
            comment.save()
            for image in images:
                CommentsMedia.objects.create(comment=comment, image=image)

        return comment

    def validate_images(self, value):

        for img in value:
            if img.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise serializers.ValidationError(
                    f"Imagem com tamanho superior a {FILE_UPLOAD_MAX_MEMORY_SIZE_MB}MB.")

        if (len(value) > MAX_FILE_PER_COMMENT):
            raise serializers.ValidationError(
                f"O limite de maximo é de {MAX_FILE_PER_COMMENT} arquivos.")

        return value
