from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('test<int:start>', views.test_view),
    path('test-list', views.test_list_view, name='test-list'),
    path('test-create', views.create_test),
    path('<int:pk>/tweets', views.tweet_list, name='tweet-list'),
    path('<int:pk>/get/tweets/<int:start>', views.get_tweets, name='get-tweets'),
    path('tweets/create', views.create_tweet, name='tweet-create'),
]