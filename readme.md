OpenEMR Role-Based Clinical Encounter Automation Framework

Overview
A Python-based healthcare UI automation framework using pytest, Playwright, and Page Object Model. The project validates a receptionist-to-clinician-to-physician patient-visit workflow, including patient registration, appointment scheduling, check-in, vitals capture, Flowboard updates, SOAP documentation, coding, and role-based access control. 

Features
Role-Based Access Control: Tests across three user roles (Receptionist, Clinician, Physician) with dedicated test fixtures and login flows.
POM Architecture: Reusable page objects for each module (login, patient registration, scheduling, vitals, etc.).
AI-Powered Test Data: Faker library generates realistic synthetic patient data (names, emails, addresses).
Browser Isolation: Playwright's parallel browser execution ensures fast, reliable test runs.
Test Management: pytest framework with HTML reports (pytest-html) and Allure reporting.

Project Structure
src/
├── pages/                # Page Object Model classes
│   ├── login_page.py
│   ├── patient_registration_page.py
│   ├── appointment_page.py
│   ├── checkin_page.py
│   ├── vitals_page.py
│   ├── flowboard_page.py
│   └── clinician_soap_page.py
├── conftest.py           # pytest fixtures (browsers, logins)
├── utils/                # Utility modules
│   ├── helpers.py        # Custom locators and actions
│   ├── data_generator.py # Faker test data generation
│   └── logger.py         # Custom logging configuration
├── tests/                # Test modules organized by feature
│   ├── test_registration.py
│   ├── test_appointments.py
│   ├── test_vitals.py
│   ├── test_soap.py
│   ├── test_flowboard.py
│   └── test_role_switching.py
├── reports/              # Test reports will be generated here
└── pytest.ini            # pytest configuration
