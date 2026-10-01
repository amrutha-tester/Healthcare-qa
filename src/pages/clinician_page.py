import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class ClinicianPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        # Flowboard frame
        self.flowboard_frame = self.page.frame_locator('iframe[name="flb"]')
        # Patient search locators
        self.patient_name_input = self.flowboard_frame.locator("#form_patient_name")
        self.provider_select = self.flowboard_frame.locator("#form_provider")
        self.filter_button = self.flowboard_frame.locator("#filter_submit")
        # Encounter tab locator
        self.encounter_tab = self.page.locator('span.tabTitle:has-text("Encounter")')
        # Encounter frame
        self.encounter_frame = self.page.frame_locator('iframe[name="enc"]')
        # Forms navigation frame inside the encounter
        self.forms_frame = self.encounter_frame.frame_locator('iframe[src*="forms.php"], frame[src*="forms.php"]')
        # Menu items located inside forms_frame
        self.clinical_menu = self.forms_frame.locator('#category_Clinical')
        self.vitals_menu_link = self.forms_frame.locator('a.dropdown-item:has-text("Vitals")')
        #Vitals locators
        self.vitals_frame = self.encounter_frame.frame_locator('iframe[name^="enctabs-"]')
        self.vitals_weight = self.vitals_frame.locator("#weight_input_metric")
        self.vitals_height = self.vitals_frame.locator("#height_input_metric")
        self.bp_systolic = self.vitals_frame.locator("#bps_input")
        self.bp_diastolic = self.vitals_frame.locator("#bpd_input")
        self.pulse = self.vitals_frame.locator("#pulse_input")
        self.oxygen_saturation = self.vitals_frame.locator("#oxygen_saturation_input")
        self.bmi_field = self.vitals_frame.locator("#BMI_input")
        self.save_vitals = self.vitals_frame.locator('button.btn-save:has-text("Save"), button[name="Submit"]')
        self.summary_frame = self.encounter_frame.frame_locator('iframe:has-text("Problem loading."), iframe[src*="forms_review.php"]')
        self.vitals_summary_bmi = self.summary_frame.locator("#divid_2")
        self.select_encounter = self.page.locator("#pastEncounters")
        
        

    #Navigate to flowboard
    def select_checked_in_patient(self, patient_name):
        self.sidebar.navigate_to_flowboard()
        self.page.wait_for_timeout(5000)
        self.provider_select.select_option("6")
        self.patient_name_input.fill(patient_name)
        self.filter_button.click()
        self.page.wait_for_timeout(5000)
        patient_locator = self.flowboard_frame.locator(f'tr:has-text("{patient_name}")')
        expect(patient_locator).to_be_visible(timeout=self.timeout)
        expect(patient_locator.locator('a.btn:has-text("Room 1")')).to_be_visible()
         # Click the patient link to open their encounter/chart
        patient_link = patient_locator.locator(f'a:has-text("{patient_name}")').first
        if patient_link.is_visible():
            patient_link.click()
        else:
            patient_locator.click()
        return self


    #Navigate to encounter tab
    def navigate_to_encounter_tab(self):
        self.encounter_tab.click()
        return self

    def enter_vitals(self, vitals_data: dict):
        # 1. Open Clinical dropdown and wait for the Vitals link to be visible
        self.clinical_menu.click()
        self.vitals_menu_link.wait_for(state="visible", timeout=self.timeout)
        self.vitals_menu_link.click()
        # 2. Wait for the first form field to be visible and fill it
        self.vitals_weight.wait_for(state="visible", timeout=self.timeout)
        # 3. Fill inputs and trigger native calculations
        self.vitals_weight.fill(vitals_data["weight_kg"])
        self.vitals_height.fill(vitals_data["height_cm"])
        self.bp_systolic.fill(vitals_data["systolic"])
        self.bp_diastolic.fill(vitals_data["diastolic"])
        self.pulse.fill(vitals_data["pulse"])
        self.oxygen_saturation.fill(vitals_data["spo2"])
        
        # Ensure OpenEMR's weight_input hidden field is populated so backend saves weight & calculates BMI
        self.vitals_frame.locator("#weight_input").evaluate("""(el) => {
            let metric = document.getElementById('weight_input_metric');
            if (metric && metric.value) {
                let val = parseFloat(metric.value) / 0.45359237;
                el.value = val.toFixed(2);
                let usa = document.getElementById('weight_input_usa');
                if (usa) usa.value = val.toFixed(2);
            }
        }""")
        self.vitals_frame.locator("#height_input").evaluate("""(el) => {
            let metric = document.getElementById('height_input_metric');
            if (metric && metric.value) {
                let val = parseFloat(metric.value) / 2.54;
                el.value = val.toFixed(2);
                let usa = document.getElementById('height_input_usa');
                if (usa) usa.value = val.toFixed(2);
            }
        }""")
        self.vitals_frame.locator("#BMI_input").evaluate("""(el) => {
            let wMetric = document.getElementById('weight_input_metric');
            let hMetric = document.getElementById('height_input_metric');
            if (wMetric && hMetric && wMetric.value && hMetric.value) {
                let w = parseFloat(wMetric.value);
                let h = parseFloat(hMetric.value) / 100;
                el.value = Math.round(w / (h * h)).toString();
            }
        }""")
        self.save_vitals.click()
        self.page.wait_for_timeout(5000)
        return self
    
    def open_past_encounter(self, encounter_category: str = None):
        """Clicks 'Select Encounter' dropdown and selects the encounter."""
        # 1. Click dropdown button
        self.select_encounter.click()
        
        # 2. Select matching encounter or the first one
        if encounter_category:
            self.page.locator(f'a[data-bind*="chooseEncounterEvent"]:has-text("{encounter_category}")').click()
        else:
            self.page.locator('a[data-bind*="chooseEncounterEvent"]').first.click()
        
        return self

    def enter_invalid_vitals(self, invalid_vitals_data: dict):
        # 1. Open Clinical dropdown and wait for the Vitals link to be visible
        self.clinical_menu.click()
        self.vitals_menu_link.wait_for(state="visible", timeout=self.timeout)
        self.vitals_menu_link.click()
        # 2. Wait for the first form field to be visible and fill it
        self.vitals_weight.wait_for(state="visible", timeout=self.timeout)
        # 3. Fill inputs and trigger native calculations
        self.vitals_weight.fill(invalid_vitals_data["weight_kg"])
        self.vitals_height.fill(invalid_vitals_data["height_cm"])
        self.bp_systolic.fill(invalid_vitals_data["systolic"])
        self.bp_diastolic.fill(invalid_vitals_data["diastolic"])
        self.pulse.fill(invalid_vitals_data["pulse"])
        self.oxygen_saturation.fill(invalid_vitals_data["spo2"])
       # 4. Register one-time dialog handler BEFORE clicking save
        alert_messages = []
        def handle_dialog(dialog):
            alert_messages.append(dialog.message)
            dialog.accept()  # Clicks 'OK' to dismiss
        self.page.once("dialog", handle_dialog)
        
        # 5. Click Save (dialog is handled automatically)
        self.save_vitals.click()
        
        return alert_messages[0] if alert_messages else ""
    