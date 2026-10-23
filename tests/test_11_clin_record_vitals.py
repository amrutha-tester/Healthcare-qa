import pytest
from playwright.sync_api import Page, expect
from src.pages.clinician_page import ClinicianPage
from src.utils.data_generator import VitalsDataFactory


@pytest.mark.regression
def test_recording_vitals(clinician_page: Page, checked_in_patient: dict) -> None:
    """
    Test case for recording patient vitals.
    """
    clinician = ClinicianPage(clinician_page)
    vitals_data = VitalsDataFactory.generate_vitals()
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(5000)
    clinician.enter_vitals(vitals_data)
    clinician.page.wait_for_timeout(5000)
    clinician.open_past_encounter()
    clinician.page.wait_for_timeout(5000)
    # Checks that the BMI row contains the expected bmi value
    # expect(clinician.summary_frame.get_by_role("link", name="Vitals (by Fred Stone)")).to_be_visible()
    expect(clinician.vitals_summary_bmi).to_contain_text('22 kg/m^2')

@pytest.mark.regression
def test_invalid_vitals(clinician_page: Page, checked_in_patient: dict) -> None:
    """
    Test case for recording patient vitals.
    """
    clinician = ClinicianPage(clinician_page)
    invalid_vitals_data = VitalsDataFactory.generate_invalid_vitals()
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(5000)
    alert_message = clinician.enter_invalid_vitals(invalid_vitals_data)
    assert "Please correct the value(s) before proceeding!" in alert_message


@pytest.mark.regression
def test_abnormal_vitals(clinician_page: Page, checked_in_patient: dict) -> None:
    """
    Test case for recording patient vitals.
    """
    clinician = ClinicianPage(clinician_page)
    abnormal_vitals_data = VitalsDataFactory.generate_abnormal_vitals()
    patient_last_name = checked_in_patient["last_name"]
    clinician.select_checked_in_patient(patient_last_name)
    expect(clinician.encounter_tab).to_be_visible()
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(5000)
    clinician.enter_vitals(abnormal_vitals_data)
    clinician.page.wait_for_timeout(5000)
    clinician.open_past_encounter()
    clinician.page.wait_for_timeout(5000)
    expect(clinician.vitals_summary_bmi).to_contain_text('49 kg/m^2')
    expect(clinician.vitals_summary_bmi).to_contain_text('Obesity III')
    