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
        self.select_choices = self.frame.locator("#header_3 button")
        self.provider_dropdown = self.frame.locator("#form_providerID")

        
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

    def select_provider(self):
        self.select_choices.click()
        select_provider = self.provider_dropdown
        if select_provider.is_visible():
            select_provider.select_option(value="6")
        return self

    def submit_and_confirm(self) -> str:
        """Submits registration form, handles duplicate check modal, and returns PID."""
        self.create_patient_button.click()

        # Handle duplicate check modal if it appears
        try:
            self.confirm_create_button.wait_for(state="visible", timeout=10000)
            # Allow Bootstrap modal fade-in animation to complete so modal('hide') is not dropped
            self.page.wait_for_timeout(800)
            self.confirm_create_button.click()

            # If the modal remains visible (e.g. Bootstrap dropped hide during transition), retry
            self.page.wait_for_timeout(700)
            if self.confirm_create_button.is_visible():
                self.confirm_create_button.click(force=True)

            # If still visible, trigger form submission directly inside the 'pat' iframe
            self.page.wait_for_timeout(700)
            if self.confirm_create_button.is_visible():
                try:
                    self.frame.locator("body").evaluate(
                        "() => { if (typeof srcConfirmSave === 'function') srcConfirmSave(); else if (document.forms[0]) document.forms[0].submit(); }"
                    )
                except Exception:
                    pass
        except Exception:
            # Duplicate check modal did not appear; submission proceeded directly
            pass

        # Clean up any lingering duplicate-check modal wrapper so it cannot block subsequent actions
        try:
            self.page.evaluate(
                """() => {
                    if (window.top && window.top.document) {
                        const doc = window.top.document;
                        doc.querySelectorAll('.dialogModal, .modal.show, .modal-backdrop').forEach(el => el.remove());
                        if (doc.body) {
                            doc.body.classList.remove('modal-open');
                            doc.body.style.removeProperty('overflow');
                            doc.body.style.removeProperty('padding-right');
                        }
                    }
                }"""
            )
        except Exception:
            pass

        # Wait for the patient header banner to populate
        self.patient_title_banner.wait_for(state="visible", timeout=self.timeout)
        self.page.wait_for_timeout(500)
        # Dismiss any post-registration popups (such as #bdayreminder if DOB matches today)
        try:
            self.page.evaluate(
                """() => {
                    if (window.top && window.top.document) {
                        const doc = window.top.document;
                        doc.querySelectorAll('#bdayreminder, .dialogModal, .modal.show, .modal-backdrop').forEach(el => el.remove());
                        if (doc.body) {
                            doc.body.classList.remove('modal-open');
                            doc.body.style.removeProperty('overflow');
                            doc.body.style.removeProperty('padding-right');
                        }
                    }
                }"""
            )
        except Exception:
            pass
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
