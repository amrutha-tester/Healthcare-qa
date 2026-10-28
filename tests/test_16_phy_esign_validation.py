import pytest
from playwright.sync_api import Page, expect
from src.pages.physician_page import PhysicianPage
from src.utils.data_generator import SoapNoteDataFactory

@pytest.mark.regression
def test_esign_invalid_password(physician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    physician = PhysicianPage(physician_page)
    soap_note_data = SoapNoteDataFactory.generate_soap_note()
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    physician.select_patient_from_flowboard(patient_last_name)
    expect(physician.encounter_tab).to_be_visible(timeout=physician.timeout)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(1500)
    physician.open_soap_form()
    physician.page.wait_for_timeout(1500)
    physician.fill_soap_form(soap_note_data)
    physician.save_soap_form()
    physician.page.wait_for_timeout(1500)
    #Click eSign to open modal
    physician.esign.click()
    physician.esign_password.wait_for(state="visible")
    #Enter wrong password & submit
    physician.esign_password.fill("wrongpassword")
    physician.esign_submit_button.click()
    physician.page.wait_for_timeout(1500)
    #Verify error message appears when wrong password is submitted
    expect(physician.summary_frame.get_by_text("The password you entered is invalid")).to_be_visible()
    #Correct the password inside the still-open modal & submit
    physician.esign_password.fill("physician")
    physician.esign_submit_button.click()
    # Verify the note is now successfully signed & locked
    physician.verify_soap_signed()