from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Blog, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = post
        comment.comment = request.POST.get('comment')
        comment.save()
        return redirect(request.path)
    comments = Comment.objects.filter(blog=post)
    context = {
        'post': post,
        'comments': comments,
        "comment_count": len(comments)
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