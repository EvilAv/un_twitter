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

    path('tweet/<int:pk>/details', views.detail_tweet, name='tweet-detail'),
    path('tweet/<int:pk>/add-comment', views.add_comment, name='add-comment'),
    path('tweet/<int:pk>/delete-comment/<int:comId>', views.delete_comment, name='delete-comment'),

    path('tweet/<int:pk>/rate-handler', views.add_rate, name='rate-handler'),
]