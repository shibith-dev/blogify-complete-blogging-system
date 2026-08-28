from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Categories
    path('categories/', views.categories, name='dashboard_categories'),
    path('categories/add/', views.add_category, name='dashboard_add_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='dashboard_edit_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='dashboard_delete_category'),
    # Blog Posts
    path('posts/', views.posts, name="dashboard_posts"),
    path('posts/add/', views.add_posts, name="dashboard_add_post"),
    path('posts/edit/<int:id>/', views.edit_post, name="dashboard_edit_post"),
    path('posts/delete/<int:id>/', views.delete_post, name="dashboard_delete_post"),
    # Users
    path('users/', views.users, name='dashboard_users'),
    path('users/add/', views.add_user, name="dashboard_add_user"),
    path('users/edit/<int:id>/', views.edit_user, name="dashboard_edit_user"),
    path('users/delete/<int:id>', views.delete_user, name="dashboard_delete_user")
]