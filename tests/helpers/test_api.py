import pytest
from django.urls import reverse


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_healthcheck(app):
    url = reverse("healthcheck")
    response = app.get(url).json
    assert response["detail"] == "Everything works"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_healthcheck_error(app, mock_connection_error):
    url = reverse("healthcheck")
    with pytest.raises(Exception):
        app.get(url)
