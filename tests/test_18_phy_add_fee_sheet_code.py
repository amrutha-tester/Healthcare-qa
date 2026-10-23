import pytest
from playwright.sync_api import Page, expect
from src.pages.physician_page import PhysicianPage


@pytest.mark.regression
def test_add_fee_sheet_codes(physician_page: Page, checked_in_patient_with_vitals: dict) -> None:
    """
    Add fee code for patient with vitals recorded.
    """
    physician = PhysicianPage(physician_page)
    patient_last_name = checked_in_patient_with_vitals['last_name']
    physician.select_patient_from_flowboard(patient_last_name)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(5000)
    physician.open_fee_sheet()
    physician.add_fee_code_and_save()
    # Assertion on fee code table after reopen
    #physician.open_fee_sheet()
    physician.page.wait_for_timeout(5000)
    expect(physician.fee_sheet_table).to_contain_text("CPT4")
    expect(physician.fee_sheet_table).to_contain_text("99201")
    
    
    