import pytest

from appflask import appf

@pytest.fixture
def app():
    app = appf
    return app