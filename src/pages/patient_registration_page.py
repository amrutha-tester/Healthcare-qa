import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class PatientRegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        # OpenEMR main workspace frame locator (handles both iframe and tab layout)
        self.frame = page.frame_locator('iframe[name="pat"]')

        #Locators for  New/Search patient modal
        self.new_patient_button = self.sidebar.new_search_menu

        #Form Field Locators (inside frame)
        self.title_select = self.frame.locator("#form_title")
        self.first_name_input = self.frame.locator("#form_fname")
        self.middle_name_input = self.frame.locator("#form_mname")
        self.last_name_input = self.frame.locator("#form_lname")
        self.dob_input = self.frame.locator("#form_DOB")
        self.sex_select = self.frame.locator("#form_sex")
        
        #Submission & Confirmation Buttons
        self.create_patient_button = self.frame.locator("#create")
        # self.confirm_create_button = self.page.locator("#confirmCreate")
        self.confirm_create_button = self.page.frame_locator('iframe[name="modalframe"], iframe#modalframe').locator('#confirmCreate')
        
        #Patient Header Banner (where PID and full name are rendered)
        self.patient_title_banner = self.page.locator("a.ptName")
        #Patient Search locators
        self.search_patient_button = self.sidebar.new_search_menu
        self.search_pid_input = self.frame.locator("#form_pubpid")
        self.search_button = self.frame.locator("#search")
        self.search_results = self.page.frame_locator('iframe[src*="patient_select.php"]').locator("body")
    
    #Page Actions

    def navigate(self):
        """Navigates to the patient registration screen."""
        self.sidebar.navigate_to_patient_registration()
        return self
        
    def fill_demographics(self, patient: dict):
        """Fills all standard demographic fields."""
        if "title" in patient:
            self.title_select.select_option(label=patient["title"])
        self.first_name_input.fill(patient["first_name"])
        if "middle_name" in patient:
            self.middle_name_input.fill(patient["middle_name"])
        self.last_name_input.fill(patient["last_name"])
        self.dob_input.fill(patient["dob"])
        self.sex_select.select_option(label=patient["gender"])
        return self
    def submit_and_confirm(self) -> str:
        """Submits registration form, handles duplicate check modal, and returns PID."""
        self.create_patient_button.click()
        self.confirm_create_button.click()
        # Wait for the patient header banner to populate
        self.patient_title_banner.wait_for(state="visible", timeout=self.timeout)
        banner_text = self.patient_title_banner.inner_text()
        # Extract PID using regex: e.g., "Doe, John [102]" or "PID: 102"
        pid_match = re.search(r"(\d+)", banner_text)
        if not pid_match:
            raise ValueError(f"Could not extract PID from banner: '{banner_text}'")
        
        return pid_match.group(1)

    def search_for_patient(self, pid: str):
        self.navigate()
        self.search_pid_input.fill(pid)
        self.search_button.click()
        self.search_results.wait_for(state="visible", timeout=self.timeout)
        return self