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
    reg_page.select_provider()
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


@pytest.mark.regression
@pytest.mark.parametrize("missing_field", ["last_name", "first_name"])
def test_registration_fails_when_mandatory_field_missing(receptionist_page: Page, missing_field: str):
    """
    Test Scenario:
    1. Generate synthetic patient demographics and omit a mandatory field (last_name / first_name).
    2. Receptionist navigates to Patient Registration.
    3. Fills the form with missing mandatory field and attempts to click create.
    4. Verifies validation prevents patient creation:
       - Duplicate/confirm creation modal does not appear.
       - Create button remains visible on the registration form.
    """
    # 1. Generate test data and clear mandatory field
    patient_data = PatientDataFactory.generate_patient()
    patient_data[missing_field] = ""

    # 2. Initialize Page Object and navigate
    reg_page = PatientRegistrationPage(receptionist_page)
    reg_page.navigate()

    # 3. Handle any JavaScript validation dialogs if triggered
    dialog_messages = []
    receptionist_page.on("dialog", lambda dialog: (dialog_messages.append(dialog.message), dialog.accept()))

    # 4. Fill demographics with missing mandatory field and attempt submission
    reg_page.fill_demographics(patient_data)
    reg_page.create_patient_button.click()

    # 5. Verify creation is blocked and user remains on registration form
    expect(reg_page.confirm_create_button).not_to_be_visible()
    expect(reg_page.create_patient_button).to_be_visible()

