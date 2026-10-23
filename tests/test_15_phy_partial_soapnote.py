import pytest
from playwright.sync_api import Page, expect
from src.pages.physician_page import PhysicianPage
from src.utils.data_generator import SoapNoteDataFactory

@pytest.mark.regression
def test_partial_soap_note(physician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    physician = PhysicianPage(physician_page)
    soap_note_data = SoapNoteDataFactory.generate_incomplete_soap_note()
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    physician.select_patient_from_flowboard(patient_last_name)
    expect(physician.encounter_tab).to_be_visible(timeout=physician.timeout)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(5000)
    physician.open_soap_form()
    physician.page.wait_for_timeout(5000)
    physician.fill_soap_form(soap_note_data)
    physician.save_soap_form()
    physician.page.wait_for_timeout(5000)
    physician.sign_soap_form("physician")
    physician.page.wait_for_timeout(5000)
    physician.verify_soap_signed()
    #Verify entered fields are visible in summary
    expect(physician.summary_frame.get_by_text("Subjective:")).to_be_visible()
    expect(physician.summary_frame.get_by_text("Assessment:")).to_be_visible()
    #Verify omitted 'Plan' section is NOT visible
    expect(physician.summary_frame.get_by_text("Plan:")).not_to_be_visible()
    physician.page.wait_for_timeout(5000)
    #Verify SOAP note is locked after e-signature
    expect(physician.soap_locked_badge).to_be_visible()



    
   