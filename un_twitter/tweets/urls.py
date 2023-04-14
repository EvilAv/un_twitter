from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('test<int:start>', views.test_view),
    path('test-list', views.test_list_view, name='test-list'),
]