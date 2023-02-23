from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm


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