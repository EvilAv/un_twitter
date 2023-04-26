from django.contrib import admin
from .models import Test, Tweet, Comment

# Register your models here.
admin.site.register(Test)
admin.site.register(Tweet)
admin.site.register(Comment)