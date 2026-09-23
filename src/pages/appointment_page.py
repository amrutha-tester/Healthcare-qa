import re
from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.components.base_components import SidebarMenuComponent

class AppointmentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sidebar = SidebarMenuComponent(page)
        # Calender frame where the new appointment form is located
        self.frame = page.frame_locator('iframe[name="cal"]')
        # Appointment Modal frame where the form inputs and save button are located
        self.modal_frame = self.page.frame_locator('iframe[src*="add_edit_event.php"]')
        # Flowboard frame
        self.flowboard_frame = self.page.frame_locator('iframe[name="flb"]')
        # Find Patient Popup frame
        self.find_patient_frame = self.page.frame_locator('iframe[name="findPatient"]')
        
        # Locator for calendar menu
        self.calendar_button = self.sidebar.calendar_menu

        # Locator for flowboard menu
        self.flowboard_button = self.sidebar.flow_board_menu
        
        # Appointment Page Locators
        self.add_appointment_button = self.frame.locator('a.btn.btn-primary[title="New Appointment"], a:has-text("+")').first
        self.form_category_dropdown = self.modal_frame.locator('#form_category')
        self.form_patient = self.modal_frame.locator('#form_patient')
        self.form_patient_search = self.find_patient_frame.locator('#searchparm')
        self.form_patient_search_button = self.find_patient_frame.locator('#submitbtn')
        self.form_provider = self.modal_frame.locator('#provd')
        self.form_time_slot_hour = self.modal_frame.locator('input[name="form_hour"], select[name="form_hour"]')
        self.form_time_slot_minute = self.modal_frame.locator('input[name="form_minute"], select[name="form_minute"]')
        self.form_duration = self.modal_frame.locator('input[name="form_duration"], select[name="form_duration"]')
        self.form_comments = self.modal_frame.locator('input[name="form_comments"], textarea[name="form_comments"]')
        self.form_save_button = self.modal_frame.locator('#form_save')
        self.form_delete_button = self.modal_frame.locator('#form_delete')
        self.form_status = self.modal_frame.locator('#form_apptstatus')
        self.form_room = self.modal_frame.locator('#form_room')
        
    def open_new_appointment(self):
        """Navigates to the Calendar view and clicks 'New Appointment'."""
        self.sidebar.navigate_to_calendar()
        self.add_appointment_button.click()
        return self

    def search_patient(self, patient: str):
        """Opens the patient search popup, searches for the patient, and selects them."""
        # 1. Click form_patient to open findPatient iframe popup
        self.form_patient.click()
        # 2. Search for patient by name or PID
        self.form_patient_search.fill(patient)
        self.form_patient_search_button.click()
        # 3. Select the matching patient from search results
        patient_result = self.find_patient_frame.locator(f'td:has-text("{patient}"), a:has-text("{patient}")').first
        patient_result.click()
        return self

    def select_provider(self, provider_value: str = "6", provider_label: str = None):
        """Selects a provider by value (default '6' for demo provider) or label."""
        if provider_label:
            self.form_provider.select_option(label=provider_label)
        else:
            self.form_provider.select_option(value=provider_value)
        return self

    def set_time(self, hour: str = "09", minute: str = "00"):
        """Sets appointment hour and minute."""
        self.form_time_slot_hour.wait_for(state="visible", timeout=self.timeout)
        self.form_time_slot_hour.fill(hour)
        self.form_time_slot_minute.wait_for(state="visible", timeout=self.timeout)
        self.form_time_slot_minute.fill(minute)
        return self

    def set_duration(self, duration: str = "15"):
        """Sets appointment duration in minutes."""
        if self.form_duration.is_visible():
            self.form_duration.fill(duration)
        return self


    def fill_appointment_details(self, appointment: dict):
        """Fills complete appointment details."""
        if "category" in appointment:
            self.form_category_dropdown.select_option(label=appointment["category"])
        if "patient" in appointment:
            self.search_patient(appointment["patient"])
        if "provider" in appointment:
            self.select_provider(provider_value=appointment["provider"])
        if "hour" in appointment:
            self.set_time(hour=appointment["hour"], minute=appointment["minute"])
        if "duration" in appointment:
            self.set_duration(appointment["duration"])
        if "comments" in appointment:
            self.form_comments.fill(appointment["comments"])
        return self

    
    def save_appointment(self):
        """Clicks the Save button to schedule the appointment, accepting any availability/conflict dialogs."""
        dialog_handler = lambda dialog: dialog.accept()
        self.page.on("dialog", dialog_handler)
        try:
            self.form_save_button.click()
            self.page.locator('iframe[src*="add_edit_event.php"]').wait_for(state="hidden", timeout=self.timeout)
            try:
                self.page.evaluate("() => { if (window.top && window.top.jQuery) window.top.jQuery('.modal.show, .dialogModal.show').modal('hide'); }")
            except Exception:
                pass
        finally:
            self.page.remove_listener("dialog", dialog_handler)
        return self

    def open_existing_appointment(self, patient_last_name: str):
        """Finds and clicks an appointment on the calendar grid."""
        event_locator = self.frame.locator(
            f'.event_appointment:has-text("{patient_last_name}") a.event_time'
        ).first
        if not event_locator.is_visible():
            self.sidebar.navigate_to_calendar()
            self.page.wait_for_timeout(2000)
        event_locator.wait_for(state="visible", timeout=self.timeout)
        event_locator.click()
        return self
    
    def delete_or_cancel_appointment(self):
        """Clicks the Delete button inside the modal and accepts the confirmation alert."""
        dialog_handler = lambda dialog: dialog.accept()
        self.page.on("dialog", dialog_handler)
        try:
            self.form_delete_button.click()
            self.page.locator('iframe[src*="add_edit_event.php"]').wait_for(state="hidden", timeout=self.timeout)
            try:
                self.page.evaluate("() => { if (window.top && window.top.jQuery) window.top.jQuery('.modal.show, .dialogModal.show').modal('hide'); }")
            except Exception:
                pass
        finally:
            self.page.remove_listener("dialog", dialog_handler)
        return self

    def check_in_patient(self):
        """Check-in the patient and update the appointment status to Arrived (@)."""
        self.form_status.wait_for(state="visible", timeout=self.timeout)
        self.form_status.select_option(value="@")
        if self.form_room.is_visible():
            try:
                self.form_room.select_option(value="1")
            except Exception:
                self.form_room.select_option(index=1)
        return self

    def navigate_to_flowboard(self):
        """Navigate to flowboard"""
        self.sidebar.navigate_to_flowboard()
        self.page.wait_for_timeout(5000)
        return self