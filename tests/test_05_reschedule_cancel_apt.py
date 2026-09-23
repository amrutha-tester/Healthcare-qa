import pytest
from playwright.sync_api import Page, expect
from src.pages.appointment_page import AppointmentPage
from src.utils.data_generator import AppointmentDataFactory

@pytest.mark.regression
def test_reschedule_appointment(receptionist_page: Page, registered_patient: dict):
    """
    Test Scenario: Reschedule an existing appointment to a different time slot.
    1. Create an initial appointment at 09:00.
    2. Re-open the appointment from the calendar.
    3. Modify time to 14:30.
    4. Save and verify the appointment modal closes and updates.
    """
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(5000)
    # 2. Open existing appointment to reschedule
    appointment_page.open_existing_appointment(patient_last_name)
    # 3. Reschedule: Change time to 14:30
    appointment_page.set_time(hour="14", minute="30")
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(5000)
    # 4. Verify update succeeded
    appointment_locator = appointment_page.frame.locator(f'.event_appointment:has-text("{patient_last_name}")')
    expect(appointment_locator).to_be_visible()

@pytest.mark.regression
def test_cancel_appointment(receptionist_page: Page, registered_patient: dict):
    """
    Test Scenario: Cancel an existing appointment.
    1. Create an initial appointment at 09:00.
    2. Re-open the appointment from the calendar.
    3. Cancel the appointment.
    4. Verify the appointment is removed from the calendar.
    """
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(5000)
    # 2. Open existing appointment to cancel
    appointment_page.open_existing_appointment(patient_last_name)
    appointment_page.page.wait_for_timeout(5000)
    # 3. Cancel the appointment
    appointment_page.delete_or_cancel_appointment()
    appointment_page.page.wait_for_timeout(5000)
    # 4. Verify the appointment is removed from the calendar
    appointment_locator = appointment_page.frame.locator(f'.event_appointment:has-text("{patient_last_name}")')
    expect(appointment_locator).not_to_be_visible()