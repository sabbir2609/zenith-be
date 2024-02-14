from django.urls import path
from .views import CategoryListView, CategoryDetailView, PostListView, PostDetailView

app_name = "blog"

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path(
        "categories/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"
    ),
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
