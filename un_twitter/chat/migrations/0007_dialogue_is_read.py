# Generated by Django 4.1.2 on 2023-05-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_dialogue_msg_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogue',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]