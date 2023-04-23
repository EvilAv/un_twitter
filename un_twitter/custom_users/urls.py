from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='custom_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/edit', views.UserUpdateView.as_view(), name='profile-edit'),
    path('user/<int:pk>/profile', views.profile_view, name='profile'),
    path('user/<int:pk>/follow', views.add_follow, name='add-follow'),
    path('user/<int:pk>/unfollow', views.delete_follow, name='delete-follow'),
    path('user/follows', views.show_follows, name='list-of-follows'),
]