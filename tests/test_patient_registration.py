# tests/test_patient_registration.py
import pytest
from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage
from src.pages.patient_registration_page import PatientRegistrationPage
from src.utils.data_generator import PatientDataFactory

@pytest.mark.regression
def test_receptionist_can_register_new_patient(receptionist_page: Page):
    """
    Test Scenario:
    1. Generate synthetic patient demographics.
    2. Receptionist navigates to Patient Registration.
    3. Fills and submits the form.
    4. Confirms patient creation and verifies PID is assigned.
    """
    # 1. Generate test data
    patient_data = PatientDataFactory.generate_patient()
    
    # 2. Initialize Page Object
    reg_page = PatientRegistrationPage(receptionist_page)
    # login_page = LoginPage(receptionist_page)
    
    # 3. Perform registration
    # login_page.navigation()
    # login_page.login("receptionist", "receptionist")

    reg_page.navigate()
    reg_page.fill_demographics(patient_data)
    pid = reg_page.submit_and_confirm()
    print(f"PID: {pid}")

    # 4. Assertions
    assert pid is not None and pid.isdigit(), f"Expected a numeric PID, got '{pid}'"
    
    # Verify patient banner contains the generated last name
    banner_text = reg_page.patient_title_banner.inner_text()
    assert patient_data["last_name"] in banner_text, (
        f"Expected patient last name '{patient_data['last_name']}' in banner, found: '{banner_text}'"
    )
    reg_page.search_for_patient(pid)
    expect(reg_page.search_results).to_be_visible()
    expect(reg_page.search_results).to_contain_text(patient_data["last_name"])
    print(f"Patient {pid} - {patient_data['last_name']} verified successfully")
