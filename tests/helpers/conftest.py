import pytest
from tests.classes.mock_classes import MockedConnection


@pytest.fixture
def mock_connection_error(monkeypatch):

    connections = {"default": MockedConnection()}
    monkeypatch.setattr("helpers.views.connections", connections)
