from django import forms
from django.core.exceptions import ValidationError

from .models import Test, Tweet, Comment


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['text']

    def clean_data(self):
        text = self.clean_data['text']
        if len(text) > 255:
            raise ValidationError('Test tweet is too long')
        return text


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text']

    def clean_data(self):
        text = self.clean_data['text']
        if len(text) > 255:
            raise ValidationError('Tweet is too long')
        return text


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean_data(self):
        text = self.clean_data['text']
        if len(text) > 255:
            raise ValidationError('Tweet is too long')
        return text
