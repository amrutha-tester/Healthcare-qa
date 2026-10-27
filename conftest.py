
import os
import subprocess
import pytest

def _reset_openemr_db():
    """Resets OpenEMR test data using docker/seed_demo_users.sql when running locally."""
    sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker", "seed_demo_users.sql")
    if os.path.exists(sql_path):
        try:
            with open(sql_path, "rb") as f:
                subprocess.run(
                    [
                        "docker", "exec", "-i", "healthcare-qa-openemr-1",
                        "mariadb", "--skip-ssl", "-u", "openemr",
                        "--password=openemr", "-h", "mysql", "openemr",
                    ],
                    stdin=f,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=15,
                )
        except Exception:
            pass

@pytest.fixture(scope="session", autouse=True)
def clean_openemr_test_data():
    """Automatically clears OpenEMR test data before and after every local pytest run."""
    _reset_openemr_db()
    yield
    _reset_openemr_db()
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from src.pages.base_page import BasePage
from src.pages.patient_registration_page import PatientRegistrationPage
from src.pages.appointment_page import AppointmentPage
from src.pages.clinician_page import ClinicianPage
from src.pages.physician_page import PhysicianPage
from src.pages.login_page import LoginPage
from src.config.roles import ROLES
from src.config.settings import settings
from src.utils.data_generator import PatientDataFactory, AppointmentDataFactory, VitalsDataFactory, SoapNoteDataFactory

# BROWSER CONFIGURATION
# This fixture customizes every browser context in all tests

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    scope="session" means this runs ONCE for the whole test session,
    not once per test. This is efficient.
    """
    return {
        **browser_context_args,    # keep existing defaults
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,       # useful for staging environments
        "locale": "en-US",
        "extra_http_headers": {
             "Accept-Language": "en-US,en;q=0.9"    # sets the language for the browser
        }
    }


# AUTHENTICATED PAGE FIXTURE
# Logs in ONCE, saves the session, reuses it across tests
# This is MUCH faster than logging in at the start of every single test

@pytest.fixture(scope="session")
def admin_auth_state(browser: Browser, tmp_path_factory):
    """
    Logs in as admin and saves the session state to a file.
    'scope=session' means this runs only once per test run.
    """
    # Create a temporary context just for login
    context = browser.new_context()
    page = context.new_page()

    # Perform the login
    LoginPage(page).navigation().login("admin", "pass")
    page.wait_for_load_state("networkidle")  # Ensures session cookies are populated

    # Save cookies and localStorage to a JSON file
    # This file acts like a "saved session" — like remembering login in a browser
    auth_file = tmp_path_factory.mktemp("auth") / "admin_state.json"
    context.storage_state(path=str(auth_file))
    context.close()

    # Return the path to the saved state file
    return str(auth_file)

@pytest.fixture
def admin_page(browser: Browser, browser_context_args) -> Page:
    """Provides a fresh browser context logged in as admin."""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    LoginPage(page).navigation().login(ROLES["admin"]["username"], ROLES["admin"]["password"])
    yield page
    context.close()

# ──────────────────────────────────────────────────────────────────────────────
# ROLE-SPECIFIC FIXTURES
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def physician_page(browser: Browser, browser_context_args) -> Page:
    """Provides a fresh browser context logged in as a physician."""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    LoginPage(page).navigation().login(ROLES["physician"]["username"], ROLES["physician"]["password"])
    yield page
    context.close()

@pytest.fixture
def clinician_page(browser: Browser, browser_context_args) -> Page:
    """Provides a fresh browser context logged in as a clinician."""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    LoginPage(page).navigation().login(ROLES["clinician"]["username"], ROLES["clinician"]["password"])
    yield page
    context.close()

@pytest.fixture
def receptionist_page(browser: Browser, browser_context_args) -> Page:
    """Provides a fresh browser context logged in as a receptionist."""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    LoginPage(page).navigation().login(ROLES["receptionist"]["username"], ROLES["receptionist"]["password"])
    yield page
    context.close()
    
@pytest.fixture
def registered_patient(receptionist_page) -> dict:
    """
    Creates a new synthetic patient via the receptionist role
    and provides their PID and demographic data to any test.
    """
    patient_data = PatientDataFactory.generate_patient()
    reg_page = PatientRegistrationPage(receptionist_page)
    
    reg_page.navigate()
    reg_page.fill_demographics(patient_data)
    pid = reg_page.submit_and_confirm()
    
    return {
        "pid": pid,
        "first_name": patient_data["first_name"],
        "last_name": patient_data["last_name"],
        "dob": patient_data["dob"],
        "gender": patient_data["gender"]
    }

@pytest.fixture
def checked_in_patient(receptionist_page, registered_patient: dict) -> dict:
    """
    Creates an appointment for the registered patient and checks them in (Arrived status).
    Provides patient data and appointment info to clinician workflow tests.
    """
    appointment_page = AppointmentPage(receptionist_page)
    patient_last_name = registered_patient["last_name"]
    appointment_data = AppointmentDataFactory.generate_appointment(patient=patient_last_name)
    # 1. Create new appointment
    appointment_page.open_new_appointment()
    appointment_page.fill_appointment_details(appointment_data)
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(3000)
    # 2. Check in the patient
    appointment_page.open_existing_appointment(patient_last_name)
    appointment_page.page.wait_for_timeout(3000)
    appointment_page.check_in_patient()
    appointment_page.save_appointment()
    appointment_page.page.wait_for_timeout(3000)
    receptionist_page.context.close()
    return {
        **registered_patient,
        "appointment": appointment_data
    }

@pytest.fixture
def checked_in_patient_with_vitals(clinician_page: Page, checked_in_patient: dict) -> dict:
    """
    Takes a checked-in patient, navigates via the clinician role to their encounter,
    and records their vitals.
    Provides patient data, appointment info, and recorded vitals data to downstream workflow tests.
    """
    clinician = ClinicianPage(clinician_page)
    vitals_data = VitalsDataFactory.generate_vitals()
    patient_last_name = checked_in_patient["last_name"]
    
    # 1. Select checked-in patient in flowboard and navigate to encounter
    clinician.select_checked_in_patient(patient_last_name)
    clinician.navigate_to_encounter_tab()
    clinician.page.wait_for_timeout(3000)
    
    # 2. Enter and save vitals
    clinician.enter_vitals(vitals_data)
    clinician.page.wait_for_timeout(3000)
    clinician_page.context.close()
    
    return {
        **checked_in_patient,
        "vitals": vitals_data
    }

@pytest.fixture
def patient_with_soap_note(physician_page: Page, checked_in_patient_with_vitals: dict) -> dict:
    """
    Takes a checked-in patient with vitals, navigates via the physician role to their encounter,
    and records a soap note and signs it.
    Provides patient data, appointment info, and recorded soap note data to downstream workflow tests.
    """
    physician = PhysicianPage(physician_page)
    soap_note_data = SoapNoteDataFactory.generate_soap_note()
    patient_last_name = checked_in_patient_with_vitals["last_name"]
    
    # 1. Select checked-in patient in flowboard and navigate to encounter
    physician.select_patient_from_flowboard(patient_last_name)
    physician.navigate_to_encounter_tab()
    physician.page.wait_for_timeout(3000)
    # 2. Fill and save soap note
    physician.open_soap_form()
    physician.page.wait_for_timeout(5000)
    physician.fill_soap_form(soap_note_data)
    physician.save_soap_form()
    physician.page.wait_for_timeout(5000)
    physician.sign_soap_form("physician")
    physician.page.wait_for_timeout(5000)
    physician_page.context.close()
    return {
        **checked_in_patient_with_vitals,
        "soap_note": soap_note_data
    }
