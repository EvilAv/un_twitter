from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.exceptions import ValidationError
from tweets.models import Tweet


# Create your models here.

# for test user password -> 0SCh^Ok37Rm%
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=255, null=True, blank=True)
    # username we will use like login
    main_name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=120)

    # add some date of birth or smth

    def serialize(self):
        return {
            'username': self.__str__(),
            'nickname': self.nickname,
            'bio': self.bio,
            'tweet_count': Tweet.objects.filter(author=self).count(),
            'followers': Followers.objects.filter(follow_target=self).count(),
        }

    def __str__(self):
        return '@' + str(self.main_name)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.pk)])

# maybe add some superuser model or smth like this


class Followers(models.Model):
    the_one_who_follow = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='the_one_who_follow')
    follow_target = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follow_target')

    def clean(self):
        if self.the_one_who_follow == self.follow_target:
            raise ValidationError('You cant follow yourself')
        if Followers.objects.filter(the_one_who_follow=self.the_one_who_follow,follow_target=self.follow_target):
            raise ValidationError('You cant follow on one person many times')

    def __str__(self):
        return str(self.the_one_who_follow) + ' -> ' + str(self.follow_target)

    def get_absolute_url(self):
        pass