from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CategoryForm, BlogForm, UserForm, AddUserForm
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

def get_user_role(user):
    if user.groups.filter(name="Manager").exists():
        return "Manager"
    elif user.groups.filter(name="Editor").exists():
        return "Editor"
    elif user.groups.filter(name="Author").exists():
        return "Author"
    else:
        return None

# Create your views here.
@login_required
def dashboard(request):
    category_count = Category.objects.all().count()
    role = get_user_role(request.user)

    if role == 'Author':
        post_count = Blog.objects.filter(author=request.user).count()
    else:
        post_count = Blog.objects.count()

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
@permission_required('blogs.add_category', login_url='dashboard')
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
@permission_required('blogs.change_category', login_url='dashboard')
def edit_category(request, id):
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
@permission_required('blogs.delete_category', login_url='dashboard')
def delete_category(request, id):
    if request.method != 'POST':
        raise PermissionDenied
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect('dashboard_categories')

# -----------------------------Blog Posts---------------------------------
@login_required
@permission_required('blogs.view_blog', login_url='dashboard')
def posts(request):
    '''Authors can access thier posts only and Editors/Managers can access all Posts'''
    role = get_user_role(request.user)
    if role == "Author":
        blogs = Blog.objects.filter(author=request.user).order_by('-updated_at')
    elif role in ('Editor', 'Manager'):
        blogs = Blog.objects.all().order_by('-updated_at')
    else:
        raise PermissionDenied
    context = {
        'posts': blogs
    }
    return render(request, 'dashboard/blogs.html', context)

@login_required
@permission_required('blogs.add_blog', login_url='dashboard')
def add_posts(request):
    '''Logged in user becomes the owner of the post'''
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
@permission_required('blogs.change_blog', login_url='dashboard')
def edit_post(request, id):
    role = get_user_role(request.user)
    if role == "Author":
        post = get_object_or_404(Blog, pk=id, author=request.user)
    elif role in ("Editor", "Manager"):
        post = get_object_or_404(Blog, pk=id)
    else:
        raise PermissionDenied
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
@permission_required('blogs.delete_blog', login_url='dashboard')
def delete_post(request, id):
    '''Author can delete their posts only and Manager/Editor can delete any post'''
    if request.method != 'POST':
        raise PermissionDenied
    role = get_user_role(request.user)
    if role == "Author":
        post = get_object_or_404(Blog, pk=id, author=request.user)
    elif role in ("Editor", "Manager"):
        post = get_object_or_404(Blog, pk=id)
    else:
        raise PermissionDenied
    post.delete()
    return redirect('dashboard_posts')

# ----------------------------- Users ---------------------------------
@login_required
@permission_required('auth.view_user', login_url='dashboard')
def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'dashboard/users.html', context)

@login_required
@permission_required('auth.add_user', login_url="dashboard")
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_users')
    else:
        form = AddUserForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/add_user.html', context)

@login_required
@permission_required('auth.change_user', login_url="dashboard")
def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard_users")
    else:
        form = UserForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'dashboard/edit_user.html', context)

@login_required
@permission_required('auth.delete_user', login_url="dashboard")
def delete_user(request, id):
    if request.method != "POST":
        raise PermissionDenied
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('dashboard_users')