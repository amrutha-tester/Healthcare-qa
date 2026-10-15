import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage

@pytest.mark.regression
def test_status_advance(clinician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    """
    Test case for advancing patient status.
    """
    clinician = ClinicianPage(clinician_page)
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    clinician.page.wait_for_timeout(5000)
    clinician.locate_patient_in_flowboard(patient_last_name)
    clinician.page.wait_for_timeout(5000)
    clinician.advance_patient_status()
    clinician.page.wait_for_timeout(5000)
    patient_locator = clinician.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
    expect(patient_locator).to_be_visible(timeout=clinician.timeout)
    expect(patient_locator.locator('a.btn:has-text("Room 2")')).to_be_visible()