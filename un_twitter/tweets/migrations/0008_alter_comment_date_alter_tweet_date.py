# Generated by Django 4.1.2 on 2023-04-26 08:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0007_alter_tweet_options_alter_tweet_date_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
