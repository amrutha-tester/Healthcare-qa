import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class PhysicianPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        # Flowboard frame
        self.flowboard_frame = self.page.frame_locator('iframe[name="flb"]')
        #status update frame
        self.status_modal_frame = self.page.frame_locator('iframe#modalframe, iframe[src*="patient_tracker_status"]')
        # Encounter tab locator
        self.encounter_tab = self.page.locator('span.tabTitle:has-text("Encounter")')
        # Encounter frame
        self.encounter_frame = self.page.frame_locator('iframe[name="enc"]')
        # Forms navigation frame inside the encounter
        self.forms_frame = self.encounter_frame.frame_locator('iframe[src*="forms.php"], frame[src*="forms.php"]')
        #Encounter summary frame
        self.summary_frame = self.encounter_frame.frame_locator('iframe:has-text("Problem loading."), iframe[src*="forms_review.php"]')
        #SOAP frame
        self.soap_frame = self.encounter_frame.frame_locator('iframe[src*="load_form.php"], frame[src*="soap"]')
        #Patient search locators
        self.patient_name_input = self.flowboard_frame.locator("#form_patient_name")
        self.provider_select = self.flowboard_frame.locator("#form_provider")
        self.filter_button = self.flowboard_frame.locator("#filter_submit")
        self.visit_status = self.flowboard_frame.locator("#form_apptstatus")
        #Patient status advance locators
        self.status_type_dropdown = self.status_modal_frame.locator("#statustype")
        self.room_dropdown = self.status_modal_frame.locator("#roomnum")
        self.status_save_button = self.status_modal_frame.locator('button:has-text("Save"), input[value*="Save"]')
        # Menu items located inside forms_frame
        self.clinical_menu = self.forms_frame.locator('#category_Clinical')
        self.soap_link = self.forms_frame.locator('a.dropdown-item:has-text("SOAP")')
        #SOAP input fields
        self.subjective = self.soap_frame.locator("textarea[name='subjective']")
        self.objective = self.soap_frame.locator("textarea[name='objective']")
        self.assessment = self.soap_frame.locator("textarea[name='assessment']")
        self.plan = self.soap_frame.locator("textarea[name='plan']")
        self.save_soap = self.soap_frame.locator('button.btn-save:has-text("Save"), button[name="Submit"]')
        #eSign locators
        self.esign = self.summary_frame.locator('a.esign-button-form[data-formdir="soap"]')
        #Password field in the eSign modal
        self.esign_password = self.summary_frame.locator('#esign-signature-form #password')
        #Sign / Submit button
        self.esign_submit_button = self.summary_frame.locator('#esign-signature-form').get_by_role("button", name="Sign")
        #Locked badge assertion
        self.soap_locked_badge = self.summary_frame.get_by_role("link", name="Locked").first
        #Fee sheet locators
        self.administrative_tab = self.forms_frame.locator('#category_Administrative')
        self.fee_sheet = self.forms_frame.locator('a.dropdown-item:has-text("Fee Sheet")')
        #Fee sheet frame
        self.fee_sheet_frame = self.encounter_frame.frame_locator('iframe[src*="fee_sheet"], iframe[name^="enctabs-"]').last
        self.new_patient_code = self.fee_sheet_frame.get_by_role("button", name="New Patient")
        self.established_patient_code = self.fee_sheet_frame.get_by_role("button", name="Established Patient")
        self.new_patient_brief_code = self.fee_sheet_frame.locator(".code-choice").first
        self.established_patient_brief_code = self.fee_sheet_frame.locator(".code-choice").first
        self.ok_button = self.fee_sheet_frame.get_by_role("button", name="OK")
        self.fee_sheet_table = self.fee_sheet_frame.locator("#selected_codes")
        self.fee_sheet_save = self.fee_sheet_frame.locator('button[name="bn_save"]')

    def select_patient_from_flowboard(self, patient_name):
        self.sidebar.navigate_to_flowboard()
        self.page.wait_for_timeout(5000)
        self.provider_select.select_option("6")
        self.patient_name_input.fill(patient_name)
        self.filter_button.click()
        self.page.wait_for_timeout(5000)
        patient_locator = self.flowboard_frame.locator(f'tr:has-text("{patient_name}")')
        expect(patient_locator).to_be_visible(timeout=self.timeout)
         # Click the patient link to open their encounter/chart
        patient_link = patient_locator.locator(f'a:has-text("{patient_name}")').first
        if patient_link.is_visible():
            patient_link.click()
        else:
            patient_locator.click()
        return self

    def navigate_to_encounter_tab(self):
        self.encounter_tab.click()
        return self

    def open_soap_form(self):
        self.clinical_menu.click()
        self.soap_link.wait_for(state="visible", timeout=self.timeout)
        self.soap_link.click()
        self.page.wait_for_timeout(5000)
        return self

    def fill_soap_form(self, soap_data: dict):
        """
        Fills the SOAP form with the given data.
        """
        if "subjective" in soap_data:
            self.subjective.fill(soap_data["subjective"])
        if "objective" in soap_data:
            self.objective.fill(soap_data["objective"])
        if "assessment" in soap_data:
            self.assessment.fill(soap_data["assessment"])
        if "plan" in soap_data:
            self.plan.fill(soap_data["plan"])
        return self

    def save_soap_form(self):
        self.save_soap.click()
        self.page.wait_for_timeout(2000)
        return self

    def sign_soap_form(self, password: str):
        self.esign.click()
        self.page.wait_for_timeout(2000)
        self.esign_password.fill(password)
        self.page.wait_for_timeout(2000)
        self.esign_submit_button.click()
        self.page.wait_for_timeout(2000)
        return self

    def verify_soap_signed(self):
        self.page.wait_for_timeout(2000)
        expect(self.soap_locked_badge).to_be_visible(timeout=self.timeout)
        return self

     #Locate patient in flowboard
    def locate_patient_in_flowboard(self, patient_name):
        """Locates the patient in the flowboard."""
        self.sidebar.navigate_to_flowboard()
        self.page.wait_for_timeout(5000)
        self.provider_select.select_option("6")
        self.patient_name_input.fill(patient_name)
        self.filter_button.click()
        self.page.wait_for_timeout(5000)
        patient_locator = self.flowboard_frame.locator(f'tr:has-text("{patient_name}")')
        expect(patient_locator).to_be_visible(timeout=self.timeout)
        self.page.wait_for_timeout(5000)
        appt_status = patient_locator.locator('a.btn:has-text("Room 1")').first
        expect(appt_status).to_be_visible(timeout=self.timeout)
        appt_status.click()
        self.page.wait_for_timeout(5000)
        return self

    def advance_patient_status(self):
        """Advances the patient status, done by physician."""
        #Click Status dropdown and wait for it to be visible
        self.status_type_dropdown.wait_for(state="visible", timeout=self.timeout)
        self.status_type_dropdown.click()
        #Select the desired status
        self.status_type_dropdown.select_option(value="$")
        #Click Save
        self.status_save_button.click()
        return self

    def verify_updated_status(self,patient_last_name):
        self.page.wait_for_timeout(5000)
        self.visit_status.select_option(value="$")
        self.filter_button.click()
        patient_locator = self.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
        expect(patient_locator).to_be_visible(timeout=self.timeout)
        return self        

    def open_fee_sheet(self):
        self.administrative_tab.click()
        self.fee_sheet.wait_for(state="visible", timeout=self.timeout)
        self.fee_sheet.click()
        self.page.wait_for_timeout(5000)
        return self

    def add_fee_code_and_save(self):
        self.new_patient_code.wait_for(state="visible", timeout=self.timeout)
        self.new_patient_code.click()
        self.new_patient_brief_code.wait_for(state="visible", timeout=self.timeout)
        self.new_patient_brief_code.click()
        self.ok_button.wait_for(state="visible", timeout=self.timeout)
        self.ok_button.click()
        expect(self.fee_sheet_table).to_contain_text("CPT4", timeout=self.timeout)
        self.fee_sheet_save.wait_for(state="visible", timeout=self.timeout)
        self.fee_sheet_save.click()
        self.page.wait_for_timeout(5000)
        return self    

    
