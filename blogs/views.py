from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Blog, Comment
from django.db.models import Q
from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=3):
    """Paginate a queryset by the page number from the request"""

    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))

# Create your views here.

def posts_by_category(request, cat_name):
    category = get_object_or_404(Category, category_name=cat_name)
    posts = Blog.objects.filter(status='Published', category=category).order_by("-created_at")
    featured_posts = Blog.objects.filter(is_featured=True, status="Published").order_by("-created_at")[:3]

    sorting = request.GET.get('sorting', '').strip()
    if sorting == 'oldest':
        posts = Blog.objects.filter(status='Published', category=category).order_by("created_at")

    context = {
        'posts': paginate_queryset(request, posts),
        'current_category': category.category_name,
        'featured_posts': featured_posts,
        "sorting": sorting
    }
    return render(request, 'posts.html', context)

def post_by_slug(request, slug):
    post = get_object_or_404(Blog, slug=slug)

    # posting comments :
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = post
        comment.comment = request.POST.get('comment')
        comment.save()
        return redirect(request.path)
    
    comments = Comment.objects.filter(blog=post)
    related_posts = Blog.objects.filter(category=post.category, status="Published").order_by("-created_at")[:3]

    context = {
        'post': post,
        'comments': comments,
        "comment_count": len(comments),
        "related_posts": related_posts
    }
    return render(request, 'blog.html', context)

def search(request):
    keyword = request.GET.get('base_search')
    featured_posts = Blog.objects.filter(is_featured=True, status="Published").order_by("-created_at")[:3]
    posts = Blog.objects.filter(
                Q(title__icontains=keyword)
                | Q(short_description__icontains=keyword)
                | Q(blog_body__icontains=keyword)
                | Q(category__category_name__icontains=keyword)
                | Q(author__username__icontains=keyword)
            )
    # apply sorting
    sorting = request.GET.get('sorting', '').strip()
    if sorting == 'oldest':
        posts = posts.order_by("created_at")
    else:
        posts = posts.order_by("-created_at")

    context = {
        'posts': paginate_queryset(request, posts),
        'base_search': keyword,
        "featured_posts": featured_posts,
        'sorting': sorting
    }
    return render(request, 'posts.html', context)

def all_posts(request):
    posts = Blog.objects.filter(is_featured=False, status="Published").order_by("-created_at")
    featured_posts = Blog.objects.filter(is_featured=True, status="Published").order_by("-created_at")[:3]

    # apply sorting
    sorting = request.GET.get('sorting', '').strip()
    if sorting == 'oldest':
        posts = Blog.objects.filter(is_featured=False, status="Published").order_by("created_at")

    context = {
        "posts": paginate_queryset(request, posts),
        "featured_posts": featured_posts,
        "sorting": sorting
    }
    return render(request, 'posts.html', context)

def all_featured_posts(request):
    posts = Blog.objects.filter(is_featured=True, status="Published").order_by("-created_at")
    popular_posts = Blog.objects.filter(is_featured=False, status="Published").order_by("-created_at")[:3]

    sorting = request.GET.get('sorting', '').strip()
    if sorting == 'oldest':
        posts = Blog.objects.filter(is_featured=True, status="Published").order_by("created_at")
    
    context = {
        "posts": paginate_queryset(request, posts),
        "featured_posts": popular_posts,
        "sorting": sorting
    }
    return render(request, 'posts.html', context)