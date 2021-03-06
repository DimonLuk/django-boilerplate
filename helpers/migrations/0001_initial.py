# Generated by Django 3.0.2 on 2020-01-17 21:22

from django.db import migrations
from django.contrib.auth.models import User


def create_admin_user(app, schema_editor):
    user = User.objects.create_superuser("admin")
    user.set_password("admin")
    user.save()


def delete_admin_user(app, schema_editor):
    user = User.objects.get(username="admin")
    user.delete()


class Migration(migrations.Migration):

    dependencies = []

    operations = [migrations.RunPython(create_admin_user, delete_admin_user)]
