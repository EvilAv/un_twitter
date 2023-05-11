import datetime
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from .models import Tweet, Comment, Rate
from .forms import TweetForm, CommentForm
from custom_users.models import CustomUser, Followers
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import time
from .recomend import train_system, get_top_predictions


# Create your views here.
@login_required
def home_page(request):
    return render(request, 'tweets/index.html')


@login_required
def followers_tweets_page(request):
    subs = Followers.objects.filter(the_one_who_follow=request.user).values_list('follow_target')
    if not subs:
        return redirect('list-of-follows')
    return render(request, 'tweets/followers-tweets.html')


@login_required
def recommend_page(request):
    return render(request, 'tweets/recommendations.html')


@login_required
def tweet_list(request, pk):
    viewed_user = CustomUser.objects.get(pk=pk)
    return render(request, 'tweets/tweets.html', {'viewed_user': viewed_user})


@login_required
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
    json_list = [i.serialize(request.user) for i in tweets_list]
    data = {
        'data': json_list,
    }
    return JsonResponse(data)


@login_required
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
                return JsonResponse(raw_tweet.serialize(request.user), status=201)
        if form.errors:
            if is_ajax:
                return JsonResponse(form.errors, status=400)


@login_required
def detail_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    comments = Comment.objects.filter(parent=tweet)
    is_liked = tweet.is_liked_by_user(request.user)
    return render(request, 'tweets/tweet-detail.html', {'tweet': tweet, 'comments': comments, 'is_liked': is_liked})


@login_required
def add_comment(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            raw_comment = form.save(commit=False)
            raw_comment.author = request.user
            raw_comment.date = timezone.localtime(timezone.now())
            raw_comment.parent = tweet
            raw_comment.save()
    return redirect(reverse('tweet-detail', args=[str(pk)]))


@login_required
def delete_comment(request, pk, comId):
    comment = get_object_or_404(Comment, pk=comId)
    if request.user == comment.author:
        comment.delete()
    return redirect(reverse('tweet-detail', args=[str(pk)]))


@login_required
def handle_rate(request, pk):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    tweet = get_object_or_404(Tweet, pk=pk)
    if is_ajax:
        if request.method == 'POST':
            new_rate = Rate(parent=tweet, author=request.user, rate_type='l')
            new_rate.clean()
            new_rate.save()
            likes = tweet.get_like_count()
            return JsonResponse({'result': 'add', 'likes': likes}, status=200)
        elif request.method == 'DELETE':
            rate = get_object_or_404(Rate, parent=tweet, author=request.user)
            rate.delete()
            tweet = get_object_or_404(Tweet, pk=pk)
            # maube it should be id of rate in json response, so it will be easier and faster to delete rate
            likes = tweet.get_like_count()
            return JsonResponse({'result': 'delete', 'likes': likes}, status=200)


@login_required
def delete_tweet(request, pk):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    tweet = get_object_or_404(Tweet, pk=pk)
    user = request.user
    if tweet.author == user:
        tweet.delete()
    if is_ajax:
        if request.method == 'DELETE':
            return JsonResponse({}, status=200)
    if request.method == 'POST':
        return redirect(reverse('tweet-list', args=[str(user.pk)]))


def get_top_tweets(request, start):
    tweets = Tweet.objects.all().order_by('-like_count', '-date')
    if start >= len(tweets):
        return JsonResponse({})
    elif start + 10 >= len(tweets):
        end = len(tweets)
    else:
        end = start + 10
    tweets_list = tweets[start:end]
    json_list = [i.serialize(request.user) for i in tweets_list]
    data = {
        'data': json_list,
    }
    return JsonResponse(data)


@login_required
def get_followers_tweets(request, start):
    subs = Followers.objects.filter(the_one_who_follow=request.user).values_list('follow_target')
    tweets = Tweet.objects.filter(author__in=subs).order_by('-date')
    if start >= len(tweets):
        return JsonResponse({})
    elif start + 10 >= len(tweets):
        end = len(tweets)
    else:
        end = start + 10
    tweets_list = tweets[start:end]
    json_list = [i.serialize(request.user) for i in tweets_list]
    data = {
        'data': json_list,
    }
    return JsonResponse(data)


@login_required
def get_recommended_tweets(request):
    list_of_id = get_recommends_list(request.user, get_unviewed_list(request.user))
    tweets_list = Tweet.objects.filter(pk__in=list_of_id)
    json_list = [i.serialize(request.user) for i in tweets_list]
    if not json_list:
        data = {
            'msg': 'no_rec'
        }
    else:
        data = {
            'data': json_list,
        }
    return JsonResponse(data)


def make_dataset():
    ts = time.time()
    dataset = {'item': [], 'user': [], 'is_liked': []}
    for item in Tweet.objects.all():
        for user in CustomUser.objects.all():
            # superuser filter
            if user.is_superuser:
                continue
            is_rated = Rate.objects.filter(author=user, parent=item)
            dataset['item'].append(item.pk)
            dataset['user'].append(user.pk)
            if is_rated:
                dataset['is_liked'].append(1)
            else:
                dataset['is_liked'].append(0)
    end = time.time()
    print(end - ts)
    return dataset


def get_unviewed_list(user):
    res = []
    for item in Tweet.objects.all():
        is_rated = Rate.objects.filter(author=user, parent=item)
        if not is_rated and not item.author == user:
            res.append(item.pk)
    return res


def get_recommends_list(user, un_list):
    ts = time.time()
    train_system(make_dataset())
    recommends = get_top_predictions(user, un_list)
    if not recommends:
        print('>_<')
    end = time.time()
    print(end - ts)
    return recommends
