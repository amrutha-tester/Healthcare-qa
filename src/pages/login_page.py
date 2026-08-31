# src/pages/auth/login_page.py
import re
from playwright.sync_api import Page, expect, Locator
from src.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for login page
        self.username: Locator = page.locator("#authUser")
        self.password: Locator = page.locator("#clearPass")
        self.language_select: Locator = page.locator("select[name='languageChoice']")
        self.login_button: Locator = page.locator("button[type='submit']")
        self.error_message: Locator = page.get_by_text(re.compile(r"(Invalid|inválido)", re.IGNORECASE))

    # def navigate(self):
    #     """Navigate to the login page."""
    #     self.navigate_to("/")
    #     return self

    def navigation(self):
       """Navigate to the login page."""
       self.navigate_to("/")
       return self

    def login(self, username: str, password: str):
        """Fills login fields, submits, and waits for post-login dashboard."""
        self.username.fill(username)
        self.password.fill(password)
        lang_dropdown = self.language_select
        if lang_dropdown.is_visible():
            lang_dropdown.select_option(value="1")
        self.login_button.click()
        return self

    def get_error_message(self):
        """Returns the error message."""
        expect(self.error_message).to_be_visible()
        return self.error_message.text_content()