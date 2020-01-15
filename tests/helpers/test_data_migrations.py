import pytest
from django.core.management import call_command
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_admin_user():
    call_command("migrate", "helpers", "0001", interactive=False)
    user = User.objects.get(username="admin")
    assert user


@pytest.mark.django_db
def test_remove_admin_user():
    call_command("migrate", "helpers", "zero")
    assert User.objects.all().count() == 0
