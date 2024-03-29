from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('<int:pk>/tweets', views.tweet_list, name='tweet-list'),
    path('<int:pk>/get/tweets/<int:start>', views.get_tweets, name='get-tweets'),
    path('tweets/create', views.create_tweet, name='tweet-create'),

    path('tweet/<int:pk>/details', views.detail_tweet, name='tweet-detail'),
    path('tweet/<int:pk>/add-comment', views.add_comment, name='add-comment'),
    path('tweet/<int:pk>/delete-comment/<int:comId>', views.delete_comment, name='delete-comment'),

    path('tweet/<int:pk>/rate-handler', views.handle_rate, name='rate-handler'),

    path('tweet/<int:pk>/delete', views.delete_tweet, name='delete-tweet'),

    path('get/top-tweets/<int:start>', views.get_top_tweets, name='get-top-tweets'),
]