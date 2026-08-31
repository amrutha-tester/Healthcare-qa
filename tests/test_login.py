import re
import pytest
from playwright.sync_api import Page, expect
from src.config.settings import settings
from src.pages.login_page import LoginPage
from src.config.roles import ROLES

@pytest.mark.smoke
def test_admin_login(page: Page):
    """Test login with admin credentials."""
    login_page = LoginPage(page)
    login_page.navigation().login(ROLES["admin"]["username"], ROLES["admin"]["password"])
    expect(page).to_have_title(re.compile(r"OpenEMR"))

# Test login with physician credentials
@pytest.mark.smoke
def test_physician_login(page: Page):
    """Test login with physician credentials."""
    login_page = LoginPage(page)
    login_page.navigation().login(ROLES["physician"]["username"], ROLES["physician"]["password"])
    expect(page).to_have_title(re.compile(r"OpenEMR"))

# Test login with clinician credentials
@pytest.mark.smoke
def test_clinician_login(page: Page):
    """Test login with clinician credentials."""
    login_page = LoginPage(page)
    login_page.navigation().login(ROLES["clinician"]["username"], ROLES["clinician"]["password"])
    expect(page).to_have_title(re.compile(r"OpenEMR"))

# Test login with receptionist credentials
@pytest.mark.smoke
def test_receptionist_login(page: Page):
    """Test login with receptionist credentials."""
    login_page = LoginPage(page)
    login_page.navigation().login(ROLES["receptionist"]["username"], ROLES["receptionist"]["password"])
    expect(page).to_have_title(re.compile(r"OpenEMR"))

def test_login_invalid_credentials(page: Page):
    """Test login with invalid credentials."""
    login_page = LoginPage(page)
    login_page.navigation().login("invalid", "invalid")
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(re.compile(r"(Invalid|inválido)", re.IGNORECASE))
