from django.shortcuts import get_object_or_404, render

from .models import Category, Post
from .constants import POSTS_ON_MAIN_PAGE


def index(request):
    posts = Post.published.all()[:POSTS_ON_MAIN_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post.published, id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts(manager='published').all()

    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )
