import pytest

from mock import MagicMock


@pytest.fixture
def context():
    return {}


@pytest.fixture
def requests_get(monkeypatch):
    def func(expected_result):
        result_mock = MagicMock()
        result_mock.configure_mock(**expected_result)

        mock = MagicMock(return_value=result_mock)
        monkeypatch.setattr("requests.get", mock)

        return mock
    return func
