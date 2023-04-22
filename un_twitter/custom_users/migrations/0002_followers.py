# Generated by Django 4.1.2 on 2023-04-22 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_target', to=settings.AUTH_USER_MODEL)),
                ('the_one_who_follow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_one_who_follow', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
