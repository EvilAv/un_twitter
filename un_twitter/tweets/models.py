from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Test(models.Model):
    text = models.CharField(max_length=100)
    sub_text = models.TextField(max_length=100, null=True)
    # trying to add some fields and add them via view, not form
    # it works
    class Meta:
        ordering = ['-id']

    # def __str__(self):
    #     return self.text

    def serialize(self):
        return {
            'text': self.text
        }


class Tweet(models.Model):
    author = models.ForeignKey('custom_users.CustomUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    # 'date': dateformat.format(self.date, 'd N Y'),
    # 'time': dateformat.format(timezone.localtime(self.date), 'H : i e'),

    def serialize(self):
        return {
            'nickname': self.author.nickname,
            'authorLink': self.author.get_absolute_url(),
            'author': str(self.author),
            'text': self.text,
            'date': timezone.localtime(self.date).strftime('%d %b %Y'),
            'time': timezone.localtime(self.date).strftime('%H:%M'),
            'likeCount': integer_format(self.like_count),
            'commentCount': integer_format(self.comment_count),
            'tweetLink': self.get_absolute_url()
        }

    class Meta:
        ordering = ['-date']

    def get_comment_link(self):
        return reverse('add-comment', args=[str(self.pk)])

    def get_absolute_url(self):
        return reverse('tweet-detail', args=[str(self.pk)])

    def get_date(self):
        return timezone.localtime(self.date).strftime('%d %b %Y')

    def get_time(self):
        return timezone.localtime(self.date).strftime('%H:%M')


class Comment(models.Model):
    parent = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey('custom_users.CustomUser', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return timezone.localtime(self.date).strftime('%d %b %Y')

    def get_time(self):
        return timezone.localtime(self.date).strftime('%H:%M')

    def get_delete_link(self):
        return reverse('delete-comment', args=[str(self.parent.pk), str(self.pk)])
    # or use kwargs

    class Meta:
        ordering = ['-date']


def integer_format(integer):
    if integer == 0:
        return ''
    else:
        return str(integer)