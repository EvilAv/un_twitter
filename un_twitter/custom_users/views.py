from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, CustomUserChangeForm
from django.views import generic
from .models import CustomUser


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
    user = CustomUser.objects.get(pk=pk)
    data = user.serialize()
    return render(request, 'custom_users/profile_view.html', {'data': data, 'viewed_user': user})
