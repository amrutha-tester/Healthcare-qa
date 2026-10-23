import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage
from src.pages.dashboard_page import DashboardPage
from src.utils.data_generator import VitalsDataFactory

@pytest.mark.workflow
def test_clinician_workflow(clinician_page: Page, checked_in_patient: dict):
    """Test clinician workflow: create vitals and advance status"""
    clinician = ClinicianPage(clinician_page)
    dashboard = DashboardPage(clinician_page)
    vitals_data = VitalsDataFactory.generate_vitals()
    patient_last_name = checked_in_patient["last_name"]
    #Record vitals for checked-in patient
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(5000)
    clinician.enter_vitals(vitals_data)
    clinician.page.wait_for_timeout(5000)
    #Add allergies to the patient dashboard
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(5000)
    dashboard.add_allergy()
    dashboard.page.wait_for_timeout(5000)
    #Locate patient in flowboard
    clinician.locate_patient_in_flowboard(patient_last_name)
    clinician.page.wait_for_timeout(5000)
    #Advance patient status
    clinician.advance_patient_status()
    clinician.page.wait_for_timeout(5000)
    patient_locator = clinician.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
    expect(patient_locator).to_be_visible(timeout=clinician.timeout)
    #Verify the visit status is updated
    expect(patient_locator.locator('a.btn:has-text("Room 1")')).to_be_visible()
    #Open past encounter
    clinician.open_past_encounter()
    clinician.page.wait_for_timeout(5000)
    #Verify vitals and allergies are recorded
    expect(clinician.vitals_summary_bmi).to_contain_text('22 kg/m^2')
    