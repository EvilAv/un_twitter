from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dialogue, TestMsg
from django.db.models import Q
from custom_users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
@login_required
def dialogue_list(request, pk):
    # User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True))
    d_list = Dialogue.objects.filter(Q(side_a=request.user) | Q(side_b=request.user))
    return render(request, 'chat/dialogue-list.html', {'d_list': d_list})


@login_required
def chat_detail(request, pk):
    dialogue = get_object_or_404(Dialogue, pk=pk)
    messages = TestMsg.objects.filter(dialogue=dialogue)
    return render(request, 'chat/chat-detail.html', {'dialogue': dialogue, 'messages': messages})


@login_required
def chat_create(request, pk):
    target = CustomUser.objects.get(pk=pk)
    try:
        chat = Dialogue.objects.get(Q(side_a=request.user, side_b=target) | Q(side_a=target, side_b=request.user))
    except ObjectDoesNotExist:
        chat = None
    if chat:
        return redirect(reverse('chat', args=[str(chat.pk)]))
    else:
        new_chat = Dialogue(side_a=request.user, side_b=target)
        new_chat.save()
        return redirect(reverse('chat', args=[str(new_chat.pk)]))
