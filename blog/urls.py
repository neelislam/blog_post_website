from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/update/', views.update_post, name='post-update'),
    path('post/<int:pk>/delete/', views.delete_post, name='post-delete'),
    path('register/', views.register, name='register'),
]