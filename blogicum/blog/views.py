from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from .constants import POSTS_ON_MAIN_PAGE


def index(request):
    template = 'blog/index.html'
    current_time = timezone.now()
    post_list = Post.objects.filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    )[:POSTS_ON_MAIN_PAGE]

    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        id=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
