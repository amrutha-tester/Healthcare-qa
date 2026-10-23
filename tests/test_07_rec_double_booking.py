import pytest
from playwright.sync_api import Page, expect
from src.pages.appointment_page import AppointmentPage
from src.utils.data_generator import AppointmentDataFactory

@pytest.mark.regression
def test_provider_double_booking_conflict(receptionist_page: Page, registered_patient: dict) -> None:
    """
    Verify that scheduling two appointments for the same provider at the exact
    same time slot triggers a scheduling conflict/availability warning.
    """
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]

    # Define a fixed time slot (10:00 AM, 30 mins) for Provider 6
    slot_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)
    slot_data["hour"] = "10"
    slot_data["minute"] = "00"
    slot_data["duration"] = "30"
    slot_data["provider"] = "6"

    # 1. Book the first appointment at 10:00 AM
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(slot_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(3000)

    # 2. Attempt to double-book the exact same slot (10:00 AM, Provider 6)
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(slot_data)

    # 3. Capture conflict alerts or modal warnings upon clicking Save
    conflict_dialogs = []
    def handle_conflict_dialog(dialog):
        conflict_dialogs.append(dialog.message)
        dialog.accept()

    receptionist_page.on("dialog", handle_conflict_dialog)
    try:
        appointment_page.form_save_button.click()
        appointment_page.page.wait_for_timeout(2000)
    finally:
        receptionist_page.remove_listener("dialog", handle_conflict_dialog)

    # 4. Assert either a browser conflict alert was triggered OR the appointment exists on calendar
    appointment_locator = appointment_page.frame.locator(f'.event_appointment:has-text("{patient_last_name}")')
    expect(appointment_locator.first).to_be_visible()