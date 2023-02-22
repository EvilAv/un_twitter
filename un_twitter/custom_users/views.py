from django.shortcuts import render


# Create your views here.
def signup(request):
    return render(request, 'custom_users/signup.html')


def login(request):
    return render(request, 'custom_users/login.html')