# src/core/base_component.py
from playwright.sync_api import Page, Locator
from src.pages.base_page import BasePage

class SidebarMenuComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locators for sidebar menu
        self.patient_menu = page.get_by_text("Patient", exact=True)
        self.new_search_menu =  page.get_by_text("New/Search", exact=True)
        self.flow_board_menu = page.get_by_text("Flow", exact=True)
        self.calendar_menu = page.get_by_text("Calendar", exact=True)

    # Workflow Navigation Actions
    def navigate_to_patient_registration(self):
        """Opens Patient dropdown and clicks New/Search."""
        self.click(self.patient_menu)
        self.click(self.new_search_menu)

    def navigate_to_flowboard(self):
        """Navigates to the Flowboard view."""
        self.click(self.flow_board_menu)

    
    def navigate_to_calendar(self):
        """Navigates to the Calendar view."""
        self.click(self.calendar_menu)
   