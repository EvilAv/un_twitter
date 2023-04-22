from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, CustomUserChangeForm #FollowerForm
from django.views import generic
from .models import CustomUser, Followers
from django.http import JsonResponse
import json


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'custom_users/signup.html', {'form': form})


class UserUpdateView(generic.UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'custom_users/edit.html'

    # This keeps users from accessing the profile of other users.
    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)


def profile_view(request, pk):
    viewed_user = CustomUser.objects.get(pk=pk)

    if Followers.objects.filter(the_one_who_follow=request.user, follow_target=viewed_user):
        is_follower = True
    else:
        is_follower = False

    data = viewed_user.serialize()

    return render(request, 'custom_users/profile_view.html',
                  {'data': data, 'viewed_user': viewed_user, 'is_follower': is_follower})


def add_follow(request, pk):
    if request.method == 'POST':
        follow = Followers(the_one_who_follow=request.user,follow_target=CustomUser.objects.get(pk=pk))
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        follow.clean()
        follow.save()
        if is_ajax:
            # json_data = json.loads(request.body)
            return JsonResponse({}, status=200)

    return render(request, 'tweets/index.html')


def delete_follow(request, pk):
    if request.method == 'POST':
        Followers.objects.filter(the_one_who_follow=request.user,follow_target=CustomUser.objects.get(pk=pk)).delete()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            # json_data = json.loads(request.body)
            return JsonResponse({}, status=200)

    return render(request, 'tweets/index.html')
