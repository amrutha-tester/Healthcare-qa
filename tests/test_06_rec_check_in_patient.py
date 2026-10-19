import pytest
from playwright.sync_api import Page, expect
from src.pages.appointment_page import AppointmentPage
from src.utils.data_generator import AppointmentDataFactory

@pytest.mark.regression
def test_check_in_patient(receptionist_page: Page, registered_patient: dict):
    """
    Test Scenario:
    1. Utilize a registered patient from the registered_patient fixture.
    2. Receptionist navigates to Calendar view and clicks 'New Appointment'.
    3. Searches for and associates the registered patient.
    4. Selects a provider, sets appointment time (hour/minute), and defines duration.
    5. Verifies all configured fields and saves the appointment.
    """
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)

    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(5000)
    appointment_page.open_existing_appointment(patient_last_name)
    appointment_page.page.wait_for_timeout(5000)
    appointment_page.check_in_patient()
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(5000)
    # verify arrived status in flowboard
    appointment_page.navigate_to_flowboard()
    checked_in_patient = appointment_page.flowboard_frame.locator(f'tr:has-text("{patient_last_name}")')
    expect(checked_in_patient).to_be_visible()
    
    