import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage
from src.pages.dashboard_page import DashboardPage


@pytest.mark.regression
def test_add_allergy(clinician_page: Page, checked_in_patient: dict) -> None:
    """
    Test case for recording patient vitals.
    """
    clinician = ClinicianPage(clinician_page)
    dashboard = DashboardPage(clinician_page)
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    clinician.page.wait_for_timeout(5000)
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(5000)
    dashboard.add_allergy()
    dashboard.page.wait_for_timeout(5000)
    dashboard.dashboard.click()
    dashboard.page.wait_for_timeout(5000)
    expect(dashboard.dashboard_frame.get_by_text("penicillin (Mild)")).to_be_visible()