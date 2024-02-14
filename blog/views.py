from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Post


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "blog/category_detail.html"


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
