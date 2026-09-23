import pytest
from playwright.sync_api import Page
from src.config.settings import settings

@pytest.mark.smoke
def test_environment_connection(page: Page):
    """Verify that OpenEMR demo is accessible and loads the login page."""
    page.goto(settings.BASE_URL)
    assert "OpenEMR" in page.title()
