# Generated by Django 5.1 on 2025-05-29 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlist',
            old_name='better_store',
            new_name='best_store',
        ),
    ]
