# Generated by Django 4.1.5 on 2023-02-01 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comments_published_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_text',
            field=models.TextField(max_length=10000),
        ),
    ]
