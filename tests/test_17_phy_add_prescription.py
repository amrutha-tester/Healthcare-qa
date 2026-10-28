import pytest
from playwright.sync_api import Page, expect
from src.pages.physician_page import PhysicianPage
from src.pages.dashboard_page import DashboardPage

@pytest.mark.regression
def test_add_prescription(physician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    """
    Add prescription for patient with vitals recorded.
    """
    physician = PhysicianPage(physician_page)
    dashboard = DashboardPage(physician_page)
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    physician.select_patient_from_flowboard(patient_last_name)
    physician.page.wait_for_timeout(1500)
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(1500)
    dashboard.add_prescription()
    dashboard.page.wait_for_timeout(1500)
    dashboard.navigate_to_dashboard_tab()
    dashboard.page.wait_for_timeout(1500)
    expect(dashboard.dashboard_frame.get_by_text("amoxicillin")).to_be_visible(timeout=dashboard.timeout)
    expect(dashboard.dashboard_frame.get_by_text("500mg 2 in tablet Daily")).to_be_visible(timeout=dashboard.timeout)
   