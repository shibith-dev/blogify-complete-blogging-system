from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Blog


# Create your views here.

def posts_by_category(request, id):
    posts = Blog.objects.filter(status='Published', category=id)
    category = get_object_or_404(Category, id=id)
    context = {
        'posts': posts,
        'current_category': category.category_name,
    }
    return render(request, 'posts_by_category.html', context)