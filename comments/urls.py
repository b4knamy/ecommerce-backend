from django.urls import path
from .views import GlassesCommentsView

urlpatterns = [
    path("comments/glasses/<str:slug>/page/<int:page>", view=GlassesCommentsView.as_view(),
         name="get_comments_from_glasses"),
    path("comments/glasses/<str:slug>/<int:id>", view=GlassesCommentsView.as_view(),
         name="delete_comments_from_glasses"),
    path("comments/glasses/<str:slug>", view=GlassesCommentsView.as_view(),
         name="create_comments_from_glasses")
]
