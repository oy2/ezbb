# Generated by Django 4.1.1 on 2022-10-06 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privatemessage',
            old_name='pm_read',
            new_name='pm_read_receiver',
        ),
        migrations.RemoveField(
            model_name='privatemessagereplies',
            name='pmr_read',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='pm_read_sender',
            field=models.BooleanField(default=True),
        ),
    ]