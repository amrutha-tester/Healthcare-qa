import pytest
from playwright.sync_api import Page, expect
from src.pages.appointment_page import AppointmentPage
from src.utils.data_generator import AppointmentDataFactory

@pytest.mark.workflow
def test_receptionist_workflow(receptionist_page: Page, registered_patient: dict):
    """Test receptionist workflow: create patient, create appointment and check in the patient"""
    # Creates registered patient (uses fixture created by create_patient.py)
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)
    # Opens calender and creates new appointment
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(1500)
    # Opens existing appointment and checks in the patient
    appointment_page.open_existing_appointment(patient_last_name)
    appointment_page.page.wait_for_timeout(1500)
    appointment_page.check_in_patient()
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(1500)
    # verify arrived status in flowboard
    appointment_page.navigate_to_flowboard()
    checked_in_patient = appointment_page.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
    expect(checked_in_patient).to_be_visible()