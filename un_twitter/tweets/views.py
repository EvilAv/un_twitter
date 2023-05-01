import datetime
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from .models import Tweet, Comment, Rate
from .forms import TweetForm, CommentForm
from custom_users.models import CustomUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home_page(request):
    return render(request, 'tweets/index.html')


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

