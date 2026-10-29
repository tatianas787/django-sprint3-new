from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post
from .constants import POSTS_ON_MAIN_PAGE


def index(request):
    current_time = timezone.now()
    posts = Post.published.filter(
        pub_date__lte=current_time,
        category__is_published=True
    )[:POSTS_ON_MAIN_PAGE]

    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.published,
        id=post_id,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )

    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )
