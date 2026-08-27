from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogForm
from django.utils.text import slugify

# Create your views here.
@login_required
def dashboard(request):
    category_count = Category.objects.all().count()
    post_count = Blog.objects.all().count()

    context = {
       'category_count': category_count,
        'post_count': post_count
    }
    return render(request, 'dashboard/dashboard.html', context)

# -----------------------------Categories ------------------------------------

@login_required
def categories(request):
    return render(request, 'dashboard/categories.html')

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_categories')
    else:
        form = CategoryForm()
    context = {
        'form' : form
    }
    return render(request, 'dashboard/add_category.html', context)

@login_required
def edit_dategory(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard_categories')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'dashboard/edit_category.html', context)

@login_required
def delete_category(request, id):
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect('dashboard_categories')

# -----------------------------Blog Posts---------------------------------
@login_required
def posts(request):
    blogs = Blog.objects.all().order_by('-updated_at')
    context = {
        'posts': blogs
    }
    return render(request, 'dashboard/blogs.html', context)

@login_required
def add_posts(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save() # save to get the post unique id 
            post.slug = f"{slugify(post.title)}-{post.id}"
            post.save()
            return redirect('dashboard_posts')
    else:
        form = BlogForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/add_post.html', context)

@login_required
def edit_post(request, id):
    post = get_object_or_404(Blog, pk=id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_data = form.save(commit=False)
            updated_data.slug = f"{slugify(updated_data.title)}-{updated_data.id}"
            updated_data.save()
            return redirect('dashboard_posts')
    else:
        form = BlogForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'dashboard/edit_post.html', context)

@login_required
def delete_post(request, id):
    post = get_object_or_404(Blog, pk=id)
    post.delete()
    return redirect('dashboard_posts')

