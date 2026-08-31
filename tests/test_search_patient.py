import pytest
from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage
from src.pages.patient_registration_page import PatientRegistrationPage
from src.utils.data_generator import PatientDataFactory


@pytest.mark.regression
def test_search_patient(receptionist_page: Page, registered_patient: dict):
    search_page = PatientRegistrationPage(receptionist_page)
    search_page.search_for_patient(registered_patient["pid"])
    expect(search_page.search_results).to_be_visible()
    expect(search_page.search_results).to_contain_text(registered_patient["last_name"])
    print(f"Patient {registered_patient['pid']} - {registered_patient['last_name']} verified successfully")
