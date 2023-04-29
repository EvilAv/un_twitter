from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='custom_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('<int:pk>/edit', views.UserUpdateView.as_view(), name='profile-edit'),
    path('<int:pk>/profile', views.profile_view, name='profile'),

    path('<int:pk>/follow', views.add_follow, name='add-follow'),
    path('<int:pk>/unfollow', views.delete_follow, name='delete-follow'),
    path('follows', views.show_follows, name='list-of-follows'),

    path('search-page', views.main_search, name='main-search'),
    path('search/', views.SearchView.as_view(), name='search'),
]