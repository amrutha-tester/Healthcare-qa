import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage

@pytest.mark.smoke
def test_select_checkedin_patient(clinician_page: Page, checked_in_patient: dict):
    clinician = ClinicianPage(clinician_page)
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    
    
