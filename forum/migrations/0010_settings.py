# Generated by Django 4.1.1 on 2022-10-16 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_post_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='ezbb', max_length=200)),
                ('site_description', models.CharField(default='An ezbb site', max_length=200)),
                ('footer_social_links', models.BooleanField(default=True)),
                ('footer_social_links_facebook', models.CharField(default='https://www.facebook.com/', max_length=200)),
                ('footer_social_links_twitter', models.CharField(default='https://twitter.com/', max_length=200)),
                ('footer_social_links_instagram', models.CharField(default='https://www.instagram.com/', max_length=200)),
                ('footer_privacy_policy', models.CharField(default='https://www.google.com/', max_length=200)),
                ('footer_terms_of_service', models.CharField(default='https://www.google.com/', max_length=200)),
                ('accounts_signup_enabled', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]