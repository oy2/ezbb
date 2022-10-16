# Generated by Django 4.1.1 on 2022-10-16 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_alter_settings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='comments_per_page',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='settings',
            name='index_welcome_banner_content',
            field=models.TextField(default='Welcome to your new installation of ezbb. This message can be changed from the settings section in the admin site! To get started with your new forum add a topic in the admin site!!', max_length=5000),
        ),
        migrations.AddField(
            model_name='settings',
            name='index_welcome_banner_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='index_welcome_banner_title',
            field=models.TextField(default='Welcome to ezbb!', max_length=5000),
        ),
        migrations.AddField(
            model_name='settings',
            name='posts_per_page',
            field=models.IntegerField(default=10),
        ),
    ]