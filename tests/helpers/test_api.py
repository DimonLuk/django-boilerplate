import pytest
from django.urls import reverse


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_healthcheck(drf_client):
    url = reverse("healthcheck")
    response = drf_client.get(url).json()
    assert response["detail"] == "Everything works"


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_healthcheck_error(drf_client, mock_connection_error):
    url = reverse("healthcheck")
    response = drf_client.get(url)
    assert response.status_code == 500
