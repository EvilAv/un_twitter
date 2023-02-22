from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=255, null=True, blank=True)
    # username we will use like login
    main_name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=120)

    # add some date of birth or smth

    def __str__(self):
        return '@' + str(self.main_name)

# maybe add some superuser model or smth like this
