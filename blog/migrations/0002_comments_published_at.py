# Generated by Django 4.1.5 on 2023-01-29 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='published_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]