from __future__ import annotations

import pytest

from computer_use.runtime import ensure_app
from computer_use.settings import load_settings


@pytest.fixture(scope="session")
def app_server():
    settings = load_settings()
    ensure_app(settings)
    yield settings
