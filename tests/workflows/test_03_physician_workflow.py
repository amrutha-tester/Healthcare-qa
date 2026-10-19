import pytest
from playwright.sync_api import Page, expect
from src.pages.physician_page import PhysicianPage
from src.utils.data_generator import SoapNoteDataFactory

@pytest.mark.workflow
def test_physician_workflow(physician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    """Test physician workflow: enter SOAP note and advance status"""
    physician = PhysicianPage(physician_page)
    soap_note_data = SoapNoteDataFactory.generate_soap_note()
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    #Select patient from flowboard
    physician.select_patient_from_flowboard(patient_last_name)
    expect(physician.encounter_tab).to_be_visible(timeout=physician.timeout)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(5000)
    #Create SOAP note
    physician.open_soap_form()
    physician.page.wait_for_timeout(5000)
    #Fill SOAP note
    physician.fill_soap_form(soap_note_data)
    physician.save_soap_form()
    physician.page.wait_for_timeout(5000)
    #Sign SOAP note
    physician.sign_soap_form("physician")
    physician.page.wait_for_timeout(5000)
    #Verify SOAP note is signed
    physician.verify_soap_signed()
    #Advance patient status
    physician.locate_patient_in_flowboard(patient_last_name)
    physician.page.wait_for_timeout(5000)
    physician.advance_patient_status()
    physician.page.wait_for_timeout(5000)
    #Verify patient status is updated
    physician.verify_updated_status(patient_last_name)
   