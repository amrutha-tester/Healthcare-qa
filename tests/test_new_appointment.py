import pytest
from playwright.sync_api import Page, expect
from src.pages.appointment_page import AppointmentPage
from src.utils.data_generator import AppointmentDataFactory


@pytest.mark.regression
def test_open_appointment_for_registered_patient(receptionist_page: Page, registered_patient: dict):
    """
    Test Scenario:
    1. Utilize a registered patient from the registered_patient fixture.
    2. Receptionist navigates to Calendar view and clicks 'New Appointment'.
    3. Searches for and associates the registered patient.
    4. Selects a provider, sets appointment time (hour/minute), and defines duration.
    5. Verifies all configured fields and saves the appointment.
    """
    appointment_page = AppointmentPage(receptionist_page)
    appointment_data = AppointmentDataFactory.generate_appointment(patient=registered_patient["last_name"])

    # 1. Open New Appointment modal/form from Calendar
    appointment_page.open_new_appointment()

    # 2. Verify appointment form elements are displayed
    expect(appointment_page.form_category_dropdown).to_be_visible()
    appointment_page.fill_appointment_details(appointment_data)

    # 5. Confirm appointment form save action is available and save
    expect(appointment_page.form_save_button).to_be_visible()
    appointment_page.save_appointment()
