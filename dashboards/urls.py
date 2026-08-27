from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='dashboard_categories'),
    path('categories/add', views.add_category, name='dashboard_add_category'),
    path('categories/edit/<int:id>', views.edit_dategory, name='dashboard_edit_category'),
    path('categories/delete/<int:id>', views.delete_category, name='dashboard_delete_category') 
]