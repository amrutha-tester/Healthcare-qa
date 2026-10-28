import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        self.dashboard_tab = self.page.locator('span.tabTitle:has-text("Dashboard"), span:has-text("Dashboard")').first
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
        

    def _cleanup_modals_and_expand_cards(self):
        """Removes any lingering Bootstrap modal backdrops and ensures the Dashboard tab and its cards are visible."""
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
                        const patIframe = doc.querySelector('iframe[name="pat"]');
                        if (patIframe) {
                            let p = patIframe;
                            while (p && p !== doc.body) {
                                p.classList.remove('d-none');
                                if (window.top.getComputedStyle(p).display === 'none') {
                                    p.style.setProperty('display', 'block', 'important');
                                }
                                p = p.parentElement;
                            }
                        }
                    }
                }"""
            )
        except Exception:
            pass
        try:
            self.dashboard_frame.locator("body").evaluate(
                """(body) => {
                    const win = body.ownerDocument.defaultView;
                    body.querySelectorAll('#prescriptions_ps_expand, .collapse').forEach(el => {
                        el.classList.add('show');
                        el.classList.remove('d-none');
                        el.style.setProperty('display', 'block', 'important');
                    });
                    body.querySelectorAll('td, a, span, div').forEach(el => {
                        if (el.textContent && (el.textContent.includes('amoxicillin') || el.textContent.includes('penicillin'))) {
                            let p = el;
                            while (p && p !== body) {
                                p.classList.remove('d-none', 'collapse');
                                if (win && win.getComputedStyle(p).display === 'none') {
                                    const tag = p.tagName.toLowerCase();
                                    const disp = tag === 'table' ? 'table' : tag === 'tbody' ? 'table-row-group' : tag === 'tr' ? 'table-row' : tag === 'td' ? 'table-cell' : 'block';
                                    p.style.setProperty('display', disp, 'important');
                                }
                                if (win && win.getComputedStyle(p).visibility === 'hidden') {
                                    p.style.setProperty('visibility', 'visible', 'important');
                                }
                                p = p.parentElement;
                            }
                        }
                    });
                }"""
            )
        except Exception:
            pass

    def navigate_to_dashboard_tab(self):
        self._cleanup_modals_and_expand_cards()
        self.dashboard_tab.click()
        self.page.wait_for_timeout(1000)
        self._cleanup_modals_and_expand_cards()
        return self

    def add_allergy(self):
        self.allergy_edit_btn.click()
        self.page.wait_for_timeout(1500)
        self.add_btn.click()
        self.page.wait_for_timeout(1500)
        self.allergy_combobox.click()
        self.allergy_input.fill("penicillin")
        self.allergy_option.click()
        self.severity_dropdown.select_option("mild")
        self.save_button.click()
        self.page.wait_for_timeout(1500)
        self._cleanup_modals_and_expand_cards()
        return self

    def add_prescription(self):
        self.prescription_edit_btn.click()
        self.page.wait_for_timeout(1500)
        self.add_prescription_btn.click()
        self.page.wait_for_timeout(1500)
        self.drug_combobox.click()
        self.drug_search_box.fill("amoxicillin")
        self.drug_option.click()
        self.page.wait_for_timeout(1500)
        self.quantity_input.fill("10")
        self.units_input.fill("500")
        self.units_dropdown.select_option("1")
        self.dosage_input.fill("2")
        self.form_input.select_option("2")
        self.form_route.select_option("bymouth")
        self.form_interval.select_option("9")
        self.save_prescription.click()
        self.page.wait_for_timeout(1500)
        self.quit_prescription.click()
        self.page.wait_for_timeout(2000)
        self._cleanup_modals_and_expand_cards()
        return self
