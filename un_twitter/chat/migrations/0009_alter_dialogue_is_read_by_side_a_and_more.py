# Generated by Django 4.1.2 on 2023-05-12 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_remove_dialogue_is_read_dialogue_is_read_by_side_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialogue',
            name='is_read_by_side_a',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dialogue',
            name='is_read_by_side_b',
            field=models.BooleanField(default=True),
        ),
    ]