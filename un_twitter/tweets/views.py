import datetime
from django.shortcuts import render
from django.http import JsonResponse
from .models import Test, Tweet
from .forms import TestForm, TweetForm
from custom_users.models import CustomUser
from django.utils import timezone


# Create your views here.
def home_page(request):
    return render(request, 'tweets/index.html')


def test_view(request, start):
    # maybe it should be prohibited to enter json part but i am not sure
    if start >= len(Test.objects.all()):
        return JsonResponse({})
    elif start + 40 >= len(Test.objects.all()):
        end = len(Test.objects.all())
    else:
        end = start + 40
    test_list = Test.objects.all()[start:end]
    json_list = [i.serialize() for i in test_list]
    data = {
        'name': 'aaaa',
        'data': json_list,
    }
    return JsonResponse(data)


def test_list_view(request):
    # data_format_test = Date_Test.objects.all()[0].test_date.strftime('%d %b %Y')
    test_tweet = Tweet.objects.all()[0].serialize()
    return render(request, 'tweets/test.html', {'test': test_tweet})


def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if form.is_valid():
            test_tweet = form.save()
            # test_tweet.text = 'хуй тебе'
            test_tweet.sub_text = 'aaaaa'
            test_tweet.save()
            if is_ajax:
                return JsonResponse(test_tweet.serialize(), status=201)
        if form.errors:
            if is_ajax:
                return JsonResponse(form.errors, status=400)

    else:
        form = TestForm()

    return render(request, 'tweets/tweet-create.html', {'form': form})


def tweet_list(request, pk):
    viewed_user = CustomUser.objects.get(pk=pk)
    return render(request, 'tweets/tweets.html', {'viewed_user': viewed_user})


def get_tweets(request, start, pk):
    # maybe it should be prohibited to enter json part but i am not sure
    viewed_user = CustomUser.objects.get(pk=pk)
    tweets = Tweet.objects.filter(author=viewed_user)
    if start >= len(tweets):
        return JsonResponse({})
    elif start + 10 >= len(tweets):
        end = len(tweets)
    else:
        end = start + 10
    tweets_list = tweets[start:end]
    json_list = [i.serialize() for i in tweets_list]
    data = {
        'data': json_list,
    }
    print(data)
    return JsonResponse(data)


def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if form.is_valid():
            raw_tweet = form.save(commit=False)
            raw_tweet.author = request.user
            raw_tweet.date = timezone.localtime(timezone.now())
            raw_tweet.like_count = 0
            raw_tweet.comment_count = 0
            raw_tweet.save()
            if is_ajax:
                print(raw_tweet.serialize())
                return JsonResponse(raw_tweet.serialize(), status=201)
        if form.errors:
            if is_ajax:
                return JsonResponse(form.errors, status=400)

    else:
        form = TestForm()
