from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog, Comment
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CategoryForm, BlogForm, UserForm, AddUserForm
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.paginator import Paginator


ALL_ROLES = {"Manager", "Editor", "Author"}
MANAGEMENT_ROLES = {"Manager", "Editor"}

# ------------------------------ Helper Functions ----------------------------------
def get_user_role(user):
    """returns the highest role of the requesting user"""

    if user.is_superuser:
        return "Superuser"

    roles = set(user.groups.values_list("name", flat=True))

    for role in ("Manager", "Editor", "Author"):
        if role in roles:
            return role

    return None


def is_content_manager(user):
    """Return True if the user can manage all post content."""
    return user.is_superuser or user.groups.filter(name__in=MANAGEMENT_ROLES).exists()


def get_accessible_queryset(user):
    """Return the posts the user is allowed to access."""

    posts = Blog.objects.select_related("author", "category")

    if user.is_superuser or is_content_manager(user):
        return posts.order_by("-updated_at")

    if user.groups.filter(name="Author").exists():
        return posts.filter(author=user).order_by("-updated_at")

    raise PermissionDenied("You don't have permission ot view these records.")


def paginate_queryset(request, queryset, per_page=3):
    """Paginate a queryset by the page number from the request"""

    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))


# Create your views here.
#------------------------------------- Dashboard -----------------------------------------
@login_required
def dashboard(request):
    """Display dashboard statistics and recent posts."""

    role = get_user_role(request.user)

    if role == "Author":
        post_count = Blog.objects.filter(author=request.user).count()
        comments_count = Comment.objects.filter(user=request.user).count()
        recent_posts = Blog.objects.filter(author=request.user).order_by("-created_at")[:5]
        users_count = None
    elif request.user.is_superuser or role in MANAGEMENT_ROLES:
        post_count = Blog.objects.count()
        comments_count = Comment.objects.count()
        users_count = User.objects.count()
        recent_posts = Blog.objects.all().order_by("-created_at")[:5]
    else:
        raise PermissionDenied

    category_count = Category.objects.count()

    context = {
        "category_count": category_count,
        "post_count": post_count,
        "comments_count": comments_count,
        "users_count": users_count,
        "recent_posts": recent_posts,
    }
    return render(request, "dashboard/dashboard.html", context)


# -----------------------------Categories ------------------------------------


@login_required
def categories(request):

    search = request.GET.get("search", "").strip()
    categories = Category.objects.all().order_by("-created_at")

    # apply search
    if search:
        categories = categories.filter(category_name__contains=search)

    context = {
        "categories": paginate_queryset(request, categories), 
        "search": search
    }
    return render(request, "dashboard/categories.html", context)


@login_required
@permission_required("blogs.add_category", login_url="dashboard")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
    else:
        form = CategoryForm()
    context = {"form": form}
    return render(request, "dashboard/add_category.html", context)


@login_required
@permission_required("blogs.change_category", login_url="dashboard")
def edit_category(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("dashboard_categories")
    else:
        form = CategoryForm(instance=category)
    context = {"form": form, "category": category}
    return render(request, "dashboard/edit_category.html", context)


@login_required
@permission_required("blogs.delete_category", login_url="dashboard")
def delete_category(request, id):
    if request.method != "POST":
        raise PermissionDenied
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect("dashboard_categories")


# -----------------------------Blog Posts---------------------------------


@login_required
@permission_required("blogs.view_blog", login_url="dashboard")
def posts(request):
    """Authors can access thier posts only and Editors/Managers can access all Posts"""

    featured = request.GET.get("featured", "").strip()
    search = request.GET.get("search", "").strip()

    posts = get_accessible_queryset(request.user)

    # Apply Search
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(short_description__icontains=search)
            | Q(blog_body__icontains=search)
            | Q(category__category_name__icontains=search)
            | Q(status__icontains=search)
            | Q(author__username__icontains=search)
        )

    # Apply filter
    if featured == "true":
        posts = posts.filter(is_featured=True)
    elif featured == "false":
        posts = posts.filter(is_featured=False)

    context = {
        "posts": paginate_queryset(request, posts), 
        "featured": featured, 
        "search": search
    }
    return render(request, "dashboard/blogs.html", context)


@login_required
@permission_required("blogs.add_blog", login_url="dashboard")
def add_post(request):
    """Logged in user becomes the owner of the post"""
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # save to get the post unique id
            post.slug = f"{slugify(post.title)}-{post.id}"
            post.save()
            return redirect("dashboard_posts")
    else:
        form = BlogForm()
    context = {"form": form}
    return render(request, "dashboard/add_post.html", context)


@login_required
@permission_required("blogs.change_blog", login_url="dashboard")
def edit_post(request, id):
    """ Edit the post if the user has access to it."""
    if request.user.is_superuser or is_content_manager(request.user):
        post = get_object_or_404(Blog, pk=id)
    else:
        post = get_object_or_404(Blog, pk=id, author=request.user)

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_data = form.save(commit=False)
            updated_data.slug = f"{slugify(updated_data.title)}-{updated_data.id}"
            updated_data.save()
            return redirect("dashboard_posts")
    else:
        form = BlogForm(instance=post)
    context = {"form": form, "post": post}
    return render(request, "dashboard/edit_post.html", context)


@login_required
@permission_required("blogs.delete_blog", login_url="dashboard")
def delete_post(request, id):
    """Delete the post if the user has access to it."""
    if request.method != "POST":
        raise PermissionDenied

    if request.user.is_superuser or is_content_manager(request.user):
        post = get_object_or_404(Blog, pk=id)
    else:
        post = get_object_or_404(Blog, pk=id, author=request.user)
    
    post.delete()
    return redirect("dashboard_posts")


# ----------------------------- Users ---------------------------------
@login_required
@permission_required("auth.view_user", login_url="dashboard")
def users(request):

    search = request.GET.get("search", "").strip()
    role = request.GET.get("role", "").strip()

    users = User.objects.all()

    # apply search
    if search:
        users = users.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    # Apply filter
    if role == "superuser":
        users = users.filter(is_superuser=True)
    elif role in ["Manager", "Editor", "Author"]:
        users = users.filter(groups__name=role).distinct()

    context = {
        "users": paginate_queryset(request, users), 
        "role": role, 
        "search": search
    }
    return render(request, "dashboard/users.html", context)


@login_required
@permission_required("auth.add_user", login_url="dashboard")
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard_users")
    else:
        form = AddUserForm()
    context = {"form": form}
    return render(request, "dashboard/add_user.html", context)


@login_required
@permission_required("auth.change_user", login_url="dashboard")
def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard_users")
    else:
        form = UserForm(instance=user)
    context = {"form": form}
    return render(request, "dashboard/edit_user.html", context)


@login_required
@permission_required("auth.delete_user", login_url="dashboard")
def delete_user(request, id):
    if request.method != "POST":
        raise PermissionDenied
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect("dashboard_users")


# ---------------------------comments----------------------------------------

@login_required
def comments(request):
    search = request.GET.get("search", "").strip()

    if request.user.is_superuser or is_content_manager(request.user):
        print("manager")
        comments = Comment.objects.all().order_by("-created_at")
    else:
        print("auther")
        comments = Comment.objects.filter(blog__author=request.user).select_related('blog').order_by("-created_at")

    if search:
        comments = comments.filter(
            Q(comment__icontains=search) | Q(blog__title__icontains=search)
        )    

    context = {
        "comments": paginate_queryset(request, comments), 
        "search": search
    }
    return render(request, "dashboard/comments.html", context)

@login_required
def delete_comment(request, id):
    if request.method != "POST":
        raise PermissionDenied
    if request.user.is_superuser or is_content_manager(request.user):
        comment = get_object_or_404(Comment, pk=id)
    else:
        comment = get_object_or_404(Comment, pk=id, blog__author=request.user)
    comment.delete()
    return redirect("dashboard_comments")
