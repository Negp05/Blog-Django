# blog/posts/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
