import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        self.dashboard_tab = self.page.locator('span:has-text("Dashboard")')
        self.dashboard_frame = self.page.frame_locator('iframe[name="pat"]')
        self.allergy_edit_btn = self.dashboard_frame.locator('span > a').first
        self.add_btn = self.dashboard_frame.locator('a:has-text("Add"), button:has-text("Add")').first
        self.modal_frame = self.page.frame_locator('iframe[name="modalframe"], iframe[src*="add_edit_issue.php"]')
        #Allergy and Reactions Module locators
        self.allergy_input = self.modal_frame.get_by_role("searchbox",name="Search")
        self.allergy_combobox = self.modal_frame.get_by_role("combobox").first
        self.allergy_option = self.modal_frame.get_by_role("option", name=re.compile("penicillin", re.I))
        self.severity_dropdown = self.modal_frame.locator('#form_severity_id')
        self.save_button = self.modal_frame.locator('button[name="form_save"]')
        self.dashboard = self.dashboard_frame.get_by_role("link", name="Dashboard")
        #Prescription Module locators
        self.prescription_edit_btn = self.dashboard_frame.locator('.iframe').first
        self.prescription_modal_frame = self.page.frame_locator('iframe[name="editScripts"]')
        self.add_prescription_btn = self.prescription_modal_frame.locator('#addButton')
        self.drug_select_box = self.prescription_modal_frame.locator('#select2-drug-container')
        self.drug_combobox = self.prescription_modal_frame.get_by_label("", exact=True)
        self.drug_search_box = self.prescription_modal_frame.get_by_role("searchbox",name="Search")
        self.drug_option = self.prescription_modal_frame.get_by_role("option", name="amoxicillin").first
        self.quantity_input = self.prescription_modal_frame.locator('#quantity')
        self.units_input = self.prescription_modal_frame.locator('#size')
        self.units_dropdown = self.prescription_modal_frame.locator('#unit')
        self.dosage_input = self.prescription_modal_frame.locator('#dosage')
        self.form_input = self.prescription_modal_frame.locator('#form')
        self.form_route = self.prescription_modal_frame.locator('#route')
        self.form_interval = self.prescription_modal_frame.locator('#interval')
        self.save_prescription = self.prescription_modal_frame.locator('#save')
        self.quit_prescription = self.prescription_modal_frame.locator('a:has-text("Quit")')
        



    def navigate_to_dashboard_tab(self):
        self.dashboard_tab.click()
        return self

    def add_allergy(self):
        self.allergy_edit_btn.click()
        self.page.wait_for_timeout(5000)
        self.add_btn.click()
        self.page.wait_for_timeout(5000)
        self.allergy_combobox.click()
        self.allergy_input.fill("penicillin")
        self.allergy_option.click()
        self.severity_dropdown.select_option("mild")
        self.save_button.click()
        self.page.wait_for_timeout(5000)
        return self

    def add_prescription(self):
        self.prescription_edit_btn.click()
        self.page.wait_for_timeout(5000)
        self.add_prescription_btn.click()
        self.page.wait_for_timeout(5000)
        self.drug_combobox.click()
        self.drug_search_box.fill("amoxicillin")
        self.drug_option.click()
        self.page.wait_for_timeout(5000)
        self.quantity_input.fill("10")
        self.units_input.fill("500")
        self.units_dropdown.select_option("1")
        self.dosage_input.fill("2")
        self.form_input.select_option("2")
        self.form_route.select_option("bymouth")
        self.form_interval.select_option("9")
        self.save_prescription.click()
        self.page.wait_for_timeout(5000)
        self.quit_prescription.click()
        return self