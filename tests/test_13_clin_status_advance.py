import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage
from src.utils.data_generator import VitalsDataFactory

@pytest.mark.regression
def test_status_advance(clinician_page: Page, checked_in_patient: dict) -> None:
    """
    Test case for advancing patient status.
    """
    clinician = ClinicianPage(clinician_page)
    vitals_data = VitalsDataFactory.generate_vitals()
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(1500)
    clinician.enter_vitals(vitals_data)
    clinician.page.wait_for_timeout(1500)
    clinician.locate_patient_in_flowboard(patient_last_name)
    clinician.page.wait_for_timeout(1500)
    clinician.advance_patient_status()
    clinician.page.wait_for_timeout(1500)
    patient_locator = clinician.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
    expect(patient_locator).to_be_visible(timeout=clinician.timeout)
    expect(patient_locator.locator('a.btn:has-text("Room 1")')).to_be_visible()