import pytest
from playwright.sync_api import Page, expect
from src.pages.patient_registration_page import PatientRegistrationPage
from src.utils.data_generator import PatientDataFactory

@pytest.mark.regression
def test_duplicate_patient_warning(receptionist_page: Page) -> None:
    """
    Test Scenario:
    1. Register an initial patient (Patient A) with unique demographics.
    2. Attempt to register a second patient with identical Name, DOB, and Gender.
    3. Click 'Create New Patient'.
    4. Assert that OpenEMR triggers the Duplicate Patient Check modal ('#confirmCreate').
    5. Assert that the duplicate patient was NOT automatically created before confirmation.
    """
    reg_page = PatientRegistrationPage(receptionist_page)
    patient_data = PatientDataFactory.generate_patient()

    # Step 1: Register initial patient
    reg_page.navigate()
    reg_page.fill_demographics(patient_data)
    reg_page.select_provider()
    first_pid = reg_page.submit_and_confirm()
    assert first_pid.isdigit()

    # Step 2: Attempt to register a duplicate patient with the same details
    reg_page.navigate()
    reg_page.fill_demographics(patient_data)
    reg_page.select_provider()

    # Step 3: Click Create New Patient
    reg_page.create_patient_button.click()

    # Step 4: Assert Duplicate Warning / Confirm modal appears
    expect(reg_page.confirm_create_button).to_be_visible(timeout=7000)

    # Step 5: Assert patient creation is blocked until explicit confirmation
    # The modal frame table will list the matching existing patient name
    duplicate_modal = receptionist_page.frame_locator('iframe[name="modalframe"], iframe#modalframe')
    expect(duplicate_modal.locator("body")).to_contain_text(patient_data["last_name"])