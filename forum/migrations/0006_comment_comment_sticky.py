# Generated by Django 4.1.1 on 2022-09-27 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_comment_comment_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_sticky',
            field=models.BooleanField(default=False),
        ),
    ]
