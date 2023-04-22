from django.contrib import admin
from . models import CustomUser, Followers

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Followers)