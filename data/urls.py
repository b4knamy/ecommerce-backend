from django.urls import path
from .views import (
    dynamic_search,
    get_glasses_promotion_view,
    get_glasses_sub_informations,
    get_search_filter_area_informations,
    glasses_profile_view,
    GlassesSearchView
)


app_name = "data"

urlpatterns = [
    path("glasses/promotions/<int:page>", view=get_glasses_promotion_view,
         name="get_glasses_promotion_view"),

    path("glasses/nav", view=get_glasses_sub_informations,
         name="get_glasses_sub_informations"),

    path("glasses/filters", view=get_search_filter_area_informations,
         name="get_search_filter_area_informations"),

    path("glasses/search", view=GlassesSearchView.as_view(),
         name="GetGlassesListView"),

    path("glasses/profile/<str:slug>", view=glasses_profile_view,
         name="glasses-profile-view"),

    path("glasses/search/dynamic", view=dynamic_search,
         name="dynamic_search"),
]
