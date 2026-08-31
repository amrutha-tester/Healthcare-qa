from playwright.sync_api import Page, Locator
from src.config.settings import settings

class BasePage:
    """Base class providing shared element actions and page-level helpers."""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.DEFAULT_TIMEOUT

    def navigate_to(self, url_path: str = ""):
        """Constructs the full URL using settings.BASE_URL and navigates."""
        base = settings.BASE_URL.rstrip('/')
        path = url_path.lstrip('/')
        
        # If url_path is empty or '/', go directly to base URL
        full_url = f"{base}/{path}" if path else base
        
        # Explicitly pass url as a keyword argument
        self.page.goto(url=full_url, wait_until="domcontentloaded")

    def click(self, locator: Locator):
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.click()

    def fill(self, locator: Locator, text: str):
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.fill(text)

    def select_option_by_value(self, locator: Locator, value: str):
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.select_option(value=value)

    def select_option_by_label(self, locator: Locator, label: str):
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.select_option(label=label)

    def get_text(self, locator: Locator) -> str:
        locator.wait_for(state="visible", timeout=self.timeout)
        return locator.inner_text().strip()