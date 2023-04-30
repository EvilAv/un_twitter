from django.urls import path
from . import views

urlpatterns = [
    path('dialogue-list/<int:pk>', views.dialogue_list, name='dialogue-list'),
    path('dialogue/<int:pk>', views.chat_detail, name='chat'),
    path('create-chat/<int:pk>', views.chat_create, name='chat-create'),
]