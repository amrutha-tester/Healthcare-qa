import pytest
from playwright.sync_api import Page,Browser, expect
from src.pages.login_page import LoginPage
from src.config.roles import ROLES
from src.pages.patient_registration_page import PatientRegistrationPage
from src.pages.appointment_page import AppointmentPage
from src.pages.clinician_page import ClinicianPage
from src.pages.physician_page import PhysicianPage
from src.pages.dashboard_page import DashboardPage
from src.utils.data_generator import PatientDataFactory, AppointmentDataFactory, VitalsDataFactory, SoapNoteDataFactory

@pytest.mark.workflow
def test_e2e_workflow(browser: Browser, browser_context_args: dict) -> None:
    """Test end-to-end workflow: full patient journey through the system:Register patient, create appointment, record vitals,add allergies, create SOAP note, add prescription, add fee sheet code and advance patient status"""
    # Generate test data
    patient_data = PatientDataFactory.generate_patient()
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_data["last_name"])
    vitals_data = VitalsDataFactory.generate_vitals()
    soap_note_data = SoapNoteDataFactory.generate_soap_note()
   
    #1.Receptionist (Register, Book Appointment & Check-In)
    rec_context = browser.new_context(**browser_context_args)
    rec_page = rec_context.new_page()
    LoginPage(rec_page).navigation().login(ROLES["receptionist"]["username"], ROLES["receptionist"]["password"])
    registration_page = PatientRegistrationPage(rec_page)
    registration_page.navigate()
    registration_page.fill_demographics(patient_data)
    registration_page.select_provider()
    registration_page.submit_and_confirm()
    expect(registration_page.patient_title_banner).to_contain_text(patient_data["last_name"])
    #Create & Check-in Appointment (Receptionist)
    appointment_page = AppointmentPage(rec_page)
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(1500)

    # Check-in the patient (moves patient to Arrived status in the flowboard)
    appointment_page.open_existing_appointment(patient_data["last_name"])
    appointment_page.page.wait_for_timeout(1500)
    appointment_page.check_in_patient()
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(1500)
    rec_context.close()

    #2.Clinician (Record Vitals & Advance Status)
    clin_context = browser.new_context(**browser_context_args)
    clin_page = clin_context.new_page()
    LoginPage(clin_page).navigation().login(ROLES["clinician"]["username"], ROLES["clinician"]["password"])
    clinician = ClinicianPage(clin_page)
    dashboard = DashboardPage(clin_page)
    #Record Vitals (Clinician)
    clinician.select_checked_in_patient(patient_data["last_name"])
    expect(clinician.encounter_tab).to_be_visible(timeout=clinician.timeout)
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(1500)
    clinician.enter_vitals(vitals_data)
    clinician.page.wait_for_timeout(1500)
    #Verify Vitals
    clinician.open_past_encounter()
    clinician.page.wait_for_timeout(1500)
    expect(clinician.vitals_summary_bmi).to_contain_text('22 kg/m^2')
    #Add allergies
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(1500)
    dashboard.add_allergy()
    dashboard.page.wait_for_timeout(1500)
    #verify allergies
    dashboard.dashboard.click()
    dashboard.page.wait_for_timeout(1500)
    expect(dashboard.dashboard_frame.get_by_text("penicillin (Mild)")).to_be_visible(timeout=dashboard.timeout)

    # Clinician advances status to "in exam room"
    clinician.locate_patient_in_flowboard(patient_data["last_name"])
    clinician.page.wait_for_timeout(1500)
    clinician.advance_patient_status()
    clinician.page.wait_for_timeout(1500)
    clin_context.close()

    #3. Physician (Create SOAP Note,Add Prescription,Add Fee Sheet Code & Advance Status)
    phys_context = browser.new_context(**browser_context_args)
    phys_page = phys_context.new_page()
    LoginPage(phys_page).navigation().login(ROLES["physician"]["username"], ROLES["physician"]["password"])
    physician = PhysicianPage(phys_page)
    dashboard = DashboardPage(phys_page)
    # Create SOAP note (Physician)
    physician.select_patient_from_flowboard(patient_data["last_name"])
    expect(physician.encounter_tab).to_be_visible(timeout=physician.timeout)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(1500)
    physician.open_soap_form()
    physician.page.wait_for_timeout(1500)
    physician.fill_soap_form(soap_note_data)
    physician.save_soap_form()
    physician.page.wait_for_timeout(1500)
    physician.sign_soap_form("physician")
    physician.page.wait_for_timeout(1500)
    physician.verify_soap_signed()
    #Add prescription
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(1500)
    dashboard.add_prescription()
    dashboard.page.wait_for_timeout(1500)
    #verify prescription
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(1500)
    expect(dashboard.dashboard_frame.get_by_text("amoxicillin")).to_be_visible(timeout=dashboard.timeout)
    #add fee sheet code
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(1500)
    physician.open_fee_sheet()
    physician.page.wait_for_timeout(1500)
    physician.add_fee_code_and_save()
    physician.page.wait_for_timeout(1500)
    #verify fee code
    expect(physician.fee_sheet_table).to_contain_text("CPT4")
    expect(physician.fee_sheet_table).to_contain_text("99201")
    # Physician advances status to "completed"
    physician.locate_patient_in_flowboard(patient_data["last_name"])
    physician.page.wait_for_timeout(1500)
    physician.advance_patient_status()
    physician.page.wait_for_timeout(1500)
    #verify updated status
    physician.verify_updated_status(patient_data["last_name"])
    phys_context.close()

    