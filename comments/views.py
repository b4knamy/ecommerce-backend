from random import randint
from time import sleep
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from core.settings import MAX_COMMENT_PER_PAGE
from .serializers import SaveCommentsSerializer, CommentsSerializer
from .models import Comments
from django.core.paginator import Paginator
import logging

logger = logging.getLogger("debugger")


class GlassesCommentsView(APIView):
    def get(self, request, slug, page):
        if slug is not None and page is not None:
            sleep(2)
            order_received = request.GET.get("order")
            order = self.get_related_and_valid_orders(order_received)
            try:
                data, max_comments_page, count = self.get_paginated_serializer_data(
                    slug, order, page)
            except Comments.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            except Exception as error:
                logger.error(error)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            answer = {
                "new_comments": data,
                "limit": max_comments_page,
                "max": count,
            }
            return Response(answer, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def post(self, request, slug):
        comments_serializer = SaveCommentsSerializer(
            data=request.data)
        if comments_serializer.is_valid(raise_exception=False):
            comments_serializer.save()
            comment_ID = comments_serializer.data.get("id", None)
            return Response({"comment_ID": comment_ID}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request, slug, id):
        comment = Comments.objects.filter(pk=id)
        if comment.exists():
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_related_and_valid_orders(self, value: str) -> str:
        """
          check value and return a valid order.
        """
        if value == "higher":
            return "-rating"

        elif value == "lower":
            return "rating"

        elif value == "older":
            return "created_at"

        elif value == "image":
            return "-has_images"

        else:
            return "-created_at"

    def get_paginated_serializer_data(self, slug: str, order: str, page: str):
        comments = Comments.objects.filter(
            glasses__slug=slug).order_by(order, "id")
        paginator = Paginator(comments, MAX_COMMENT_PER_PAGE)
        max_comments_page = paginator.num_pages

        page = self.page_checker_resolver(page=page, limit=max_comments_page)

        paginated_comments = paginator.page(page)
        comments_serializer = CommentsSerializer(
            paginated_comments, many=True)

        return comments_serializer.data, max_comments_page, paginator.count

    def page_checker_resolver(self, page, limit):
        if isinstance(page, int):
            return page if page <= limit else limit
        elif isinstance(page, str) and page.isnumeric():
            page = int(page)
            return page if page <= limit else limit
        return 1
