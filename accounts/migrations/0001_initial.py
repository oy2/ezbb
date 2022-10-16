# Generated by Django 4.1.1 on 2022-10-06 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm_title', models.CharField(max_length=100)),
                ('pm_content', models.TextField(max_length=5000)),
                ('pm_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pm_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pm_receiver', to=settings.AUTH_USER_MODEL)),
                ('pm_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pm_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PrivateMessageReplies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pmr_content', models.TextField(max_length=5000)),
                ('pmr_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pmr_pm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pmr_pm', to='accounts.privatemessage')),
                ('pmr_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pmr_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
