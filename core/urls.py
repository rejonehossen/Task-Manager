# Created by Rejone Hossen | Premium Task Manager | 2025
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import RegisterView, CustomLoginView, logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('toggle-complete/<int:pk>/', views.task_toggle_complete, name='task_toggle_complete'),
    path('category/create/', views.category_create, name='category_create'),
    path('tag/create/', views.tag_create, name='tag_create'),
    path('shared/create/', views.shared_list_create, name='shared_list_create'),
    path('shared/<int:pk>/', views.shared_list_detail, name='shared_list_detail'),
    path('profile/', views.profile, name='profile'),
    path('update-order/', views.update_task_order, name='update_task_order'),
]
