
from src.pages import patient_registration_page
from src.pages import base_page
from src.pages.patient_registration_page import PatientRegistrationPage
from src.pages.appointment_page import AppointmentPage
from src.pages.clinician_page import ClinicianPage
from src.utils.data_generator import AppointmentDataFactory
import pytest
import os
from playwright.sync_api import Browser, BrowserContext, Page
from src.pages.login_page import LoginPage
from src.config.roles import ROLES
from src.config.settings import settings
from src.utils.data_generator import PatientDataFactory

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