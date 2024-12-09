
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from core.settings.site import MAX_GLASSES_PER_PAGE, MAX_SEARCH_PRODUCT_PER_PAGE
from data import serializers
from rest_framework.views import APIView
from .models import Glasses, Category, Color, Model, Shape, Brand
from data.filters import GlassesFilter
from django.views.decorators.cache import cache_page, never_cache
from django.core.paginator import Paginator
from comments.models import Comments
from django.db.models import Count

from .utils.helpers import get_filters_serialized_data, get_sub_informatios_serialized_data
from time import sleep
import logging

logger = logging.getLogger("debugger")


@cache_page(60 * 60 * 1)
@api_view(["GET"])
@never_cache
def get_glasses_promotion_view(request, page):
    data = Glasses.objects.filter(is_sample=True)
    paginated_data = Paginator(data, 5, orphans=2)
    next_items = paginated_data.page(page)
    serializer = serializers.GlassesCardSerializer(next_items, many=True)

    answer = {
        "has_next": next_items.has_next(),
        "data": serializer.data
    }
    return Response(answer, status=status.HTTP_200_OK)


@cache_page(60 * 60 * 1)
@api_view(['GET'])
def get_glasses_sub_informations(request):

    if request.method == "GET":
        try:
            answer = [
                {
                    "name": "Categorias", "filter_name": "categoria", "data": get_sub_informatios_serialized_data(
                        Category, serializers.CategorySerializer)
                },
                {
                    "name": "Cores", "filter_name": "cor", "data": get_sub_informatios_serialized_data(
                        Color, serializers.ColorSerializer)
                },
                {
                    "name": "Modelos", "filter_name": "modelo", "data": get_sub_informatios_serialized_data(
                        Model, serializers.GlassesModelSerializer)
                },
                {
                    "name": "Formatos", "filter_name": "formato", "data": get_sub_informatios_serialized_data(
                        Shape, serializers.ShapeSerializer)
                },
                {
                    "name": "Marcas", "filter_name": "marca", "data": get_sub_informatios_serialized_data(
                        Brand, serializers.BrandSerializer)
                }
            ]

        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        finally:
            pass
        return Response(answer, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@cache_page(60 * 60 * 1)
@api_view(["GET"])
def get_search_filter_area_informations(request):

    if request.method == "GET":

        try:
            answer = {
                "filter_1": get_filters_serialized_data(Category, "glasses_category"),
                "filter_2": get_filters_serialized_data(Color, "glasses_color"),
                "filter_3": get_filters_serialized_data(Model, "glasses_model"),
                "filter_4": get_filters_serialized_data(Shape, "glasses_shape"),
                "filter_5": get_filters_serialized_data(Brand, "glasses_brand"),
                "amount": get_filters_serialized_data(Glasses, is_amount=True),
            }

        except Exception as error:
            print("error: ", error)
            return Response(status=status.HTTP_404_NOT_FOUND)
        finally:
            pass

        return Response(answer, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


class GlassesSearchView(APIView):

    def get(self, request):
        sleep(2)
        page = request.GET.get("page", 1)
        try:
            if querys_params := request.query_params:
                queryset = self.search_query_resolver(querys_params)
                if not queryset.is_valid():
                    return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)

                queryset = queryset.qs
            else:
                queryset = Glasses.objects.all()

            answer = self.get_paginated_response(queryset, page)

            return Response(answer, status=status.HTTP_200_OK)
        except EmptyPage:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            logger.error(error)

    def search_query_resolver(self, qs):
        queryset = Glasses.objects.all().distinct()
        return GlassesFilter(qs, queryset)

    def get_paginated_response(self, queryset, page):
        paginator = Paginator(queryset, MAX_GLASSES_PER_PAGE)

        paginated_glasses = paginator.page(page)

        glasses_serializer = serializers.GlassesCardSerializer(
            paginated_glasses, many=True)

        answer = {
            "products": glasses_serializer.data,
            "count": paginator.count,
            "last": paginator.num_pages,
            "page": int(page)
        }

        return answer


@api_view(["GET"])
def glasses_profile_view(request, slug):
    if request.method == "GET" and slug is not None:
        try:
            glasses = Glasses.objects.get(slug=slug)
            glasses_serializer = serializers.GlassesProfileSerializer(
                glasses)
            ratings = Comments.objects.values("rating").annotate(
                count=Count("rating")).filter(rating__in=[1, 2, 3, 4, 5], glasses=glasses.id)
            relateds_glasses = Glasses.objects.filter(
                category__in=glasses.category.all(),
                brand__in=glasses.brand.all(),
            ).exclude(slug=slug).distinct()[:8]
            relateds_serializer = serializers.GlassesCardSerializer(
                relateds_glasses, many=True)
        except Glasses.DoesNotExist:
            message_404 = {"error": f'Nenhum Óculos "{
                slug}" foi encontrado.'}
            return Response(data=message_404, status=status.HTTP_404_NOT_FOUND)

        except Exception as error:
            logger.error(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        answer = {
            "glasses": glasses_serializer.data,
            "relateds_glasses": relateds_serializer.data,
            "ratings": ratings,
        }
        return Response(answer, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def dynamic_search(request):
    query = request.GET.get("query", None)
    if not query:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    page = request.GET.get("page", 1)

    try:

        queryset = Glasses.objects.filter(name__icontains=query)
        paginator = Paginator(queryset, MAX_SEARCH_PRODUCT_PER_PAGE)
        next_products = paginator.page(page)
        queryset_serializer = serializers.GlassesDynamicSerializer(
            next_products, many=True)
        answer = {
            "products": queryset_serializer.data,
            "last": paginator.num_pages,
            "count": paginator.count
        }
    except Exception as e:
        print(e)

    return Response(answer, status=200)
