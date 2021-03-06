import pytest

from mock import MagicMock
from pipeliner.context import Context


@pytest.fixture
def context():
    return Context(current_pipeline=None)


@pytest.fixture
def requests_get(monkeypatch):
    def func(expected_result):
        result_mock = MagicMock()
        result_mock.configure_mock(**expected_result)

        mock = MagicMock(return_value=result_mock)
        monkeypatch.setattr("requests.get", mock)

        return mock
    return func
