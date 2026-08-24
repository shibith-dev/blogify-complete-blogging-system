from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Blog
from django.db.models import Q


# Create your views here.

def posts_by_category(request, cat_name):
    category = get_object_or_404(Category, category_name=cat_name)
    posts = Blog.objects.filter(status='Published', category=category)
    context = {
        'posts': posts,
        'current_category': category.category_name,
    }
    return render(request, 'posts_by_category.html', context)

def post_by_slug(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'blog.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
    context = {
        'posts': blogs,
        'keyword': keyword
    }
    return render(request, 'search.html', context)