# 🏥 OpenEMR Role-Based Clinical Encounter Automation Framework

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-v1.40%2B-2EAD33.svg?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/pytest-v8.0%2B-0A9EDC.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Page%20Object%20Model%20(POM)-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Active%20Development-success.svg)]()

A modern, robust end-to-end UI automation framework for **OpenEMR** built with **Python**, **Playwright**, and **pytest**. 

This framework simulates realistic clinical workflows and validates role-based access control (RBAC) across multiple healthcare personas—from front-desk patient registration to clinical triage, provider documentation, and billing.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Tech Stack](#-architecture--tech-stack)
- [Project Structure](#-project-structure)
- [User Roles & Permissions](#-user-roles--permissions)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
- [Running Tests](#-running-tests)
  - [Test Execution by Markers](#test-execution-by-markers)
  - [Running Specific Test Suites](#running-specific-test-suites)
  - [Cross-Browser & Execution Modes](#cross-browser--execution-modes)
  - [Generating Test Reports](#generating-test-reports)
- [Debugging & Traces](#-debugging--traces)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🔍 Overview

OpenEMR is an open-source electronic health record (EHR) and medical practice management solution. Testing healthcare applications requires strict data isolation, role-specific UI access, and intricate multi-step workflows.

This framework leverages **Playwright's modern browser automation engine** combined with **pytest fixtures** and the **Page Object Model (POM)** pattern to deliver fast, deterministic, and maintainable automated tests.

---

## 🚀 Key Features

- **🎭 Page Object Model (POM)**: Modular, encapsulated page and component classes for clean separation of UI locators and test logic.
- **🔐 Role-Based Access Control (RBAC)**: Pre-configured fixtures and session handlers for Receptionists, Clinicians, Physicians, Accountants, and Admins.
- **⚡ Session & State Management**: Playwright `storage_state` caching for rapid authentication without redundant login overhead.
- **🎲 Synthetic Test Data Generation**: Built-in `PatientDataFactory` powered by `Faker` to generate realistic, compliant demographic data on the fly.
- **🛡️ Flake-Resistant Automation**: Intelligent auto-waiting, resilient locators, and dynamic frame handling (targeting OpenEMR iframe architectures).
- **📊 Rich Diagnostics & Artifacts**: Automatic capture of screenshots, videos, and Playwright execution traces on test failures.
- **📈 Comprehensive Reporting**: Integration with `pytest-html` and structured execution logging.

---

## 🛠️ Architecture & Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **Automation Engine** | Playwright for Python | Cross-browser web automation & fast execution |
| **Test Runner** | pytest | Test discovery, execution, markers & fixtures |
| **Data Generation** | Faker | Dynamic synthetic patient demographic generator |
| **Configuration** | Pydantic Settings / python-dotenv | Type-safe environment management |
| **Reporting** | pytest-html | Visual HTML test execution reports |

---

## 📁 Project Structure

```text
Healthcare-qa/
├── src/
│   ├── config/               # Global settings and role definitions
│   │   ├── roles.py          # User role credentials and permission metadata
│   │   └── settings.py       # Pydantic environment configuration
│   ├── pages/                # Page Object Model classes
│   │   ├── base_page.py      # Core page abstraction & common navigation methods
│   │   ├── login_page.py     # Authentication page object
│   │   ├── patient_registration_page.py  # Patient demographics & search
│   │   └── components/       # Reusable UI component wrappers
│   │       └── base_components.py
│   └── utils/                # Utility helpers & generators
│       └── data_generator.py # Faker-based PatientDataFactory
├── tests/                    # Test suites organized by domain
│   ├── test_login.py         # Login & RBAC validation tests
│   ├── test_patient_registration.py # Patient creation & demographic verification
│   ├── test_search_patient.py # Patient search functionality
│   └── test_smoke.py         # Fast smoke / sanity checks
├── conftest.py               # Session fixtures, role fixtures, browser contexts
├── pytest.ini                # Pytest CLI configuration, markers & default flags
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 👥 User Roles & Permissions

The framework maps standard healthcare personas to validate role-specific UI capabilities and restrictions:

| Role | Default User | Capabilities / Workflow Area |
| :--- | :--- | :--- |
| **Receptionist** | `receptionist` | Patient Registration, Search, Demographic Management, Calendar Scheduling |
| **Clinician** | `clinician` | Nursing Intake, Vitals Capture, Triage, Flowboard Updates |
| **Physician** | `physician` | Clinical Encounter, SOAP Notes, Orders, Prescriptions, Fee Sheet Review |
| **Accountant** | `accountant` | Checkout, Copays, Billing, Fee Sheet Auditing |
| **Administrator**| `admin` | Full system administration, ACL management, global facility settings |

---

## 🏁 Getting Started

### Prerequisites

- **Python 3.10+** installed on your system.
- **Git** installed.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/amrutha-tester/Healthcare-qa.git
   cd Healthcare-qa
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browser binaries**:
   ```bash
   playwright install chromium
   # Or install all browsers:
   # playwright install
   ```

### Local OpenEMR (Docker Setup)

If running OpenEMR locally with Docker:

1. **Start containers**:
   ```bash
   docker compose up -d
   ```
2. **Wait for initial configuration (~2 minutes)**:
   On first launch, OpenEMR configures MySQL, SSL certificates, and starts Apache. You can follow container progress with:
   ```bash
   docker compose logs -f openemr
   ```
   Wait until you see `Starting Apache!` and `resuming normal operations`.

3. **Seed demo users & roles**:
   Seed the required roles (`receptionist`, `clinician`, `physician`, `accountant`) into MariaDB:
   - **Windows (PowerShell)**:
     ```powershell
     Get-Content docker/seed_demo_users.sql | docker compose exec -T mysql mariadb -u root -proot openemr
     ```
   - **Linux / macOS**:
     ```bash
     cat docker/seed_demo_users.sql | docker compose exec -T mysql mariadb -u root -proot openemr
     ```

### Environment Configuration

Create a `.env` file in the project root (or rely on default settings in [src/config/settings.py](file:///c:/Users/user/Desktop/Github/Healthcare-qa/src/config/settings.py)):

```ini
BASE_URL="http://localhost:8080"
DEFAULT_TIMEOUT=20000.0
HEADLESS=false
SLOW_MO=0.5
```

---

## 🧪 Running Tests

### Test Execution by Markers

Execute specific test subsets using `pytest` markers:

```bash
# Run smoke tests
pytest -m smoke

# Run regression test suite
pytest -m regression

# Run role-based access control tests
pytest -m rbac

# Run end-to-end clinical workflow
pytest -m e2e
```

### Running Specific Test Suites

```bash
# Run patient registration tests
pytest tests/test_patient_registration.py

# Run login tests
pytest tests/test_login.py

# Run with verbose output and live logs
pytest -v -s
```

### Cross-Browser & Execution Modes

```bash
# Run in Headless mode (overriding pytest.ini)
pytest --headless

# Run on Firefox
pytest --browser firefox

# Run on WebKit (Safari engine)
pytest --browser webkit

# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto
```

### Generating Test Reports

Generate a standalone HTML test execution report:

```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 🔍 Debugging & Traces

Playwright captures execution traces and artifacts on test failures as configured in `pytest.ini`:

- **Screenshots**: Automatically saved on failure (`--screenshot=only-on-failure`).
- **Videos**: Retained on failure (`--video=retain-on-failure`).
- **Trace Viewer**: Inspect failed test execution step-by-step with DOM snapshots and network logs:
  ```bash
  playwright show-trace test-results/<trace-directory>/trace.zip
  ```

---

## 🗺️ Roadmap

- [x] Base Page Object Model architecture & component abstraction
- [x] Role-based test fixtures (`receptionist_page`, `clinician_page`, `physician_page`)
- [x] Synthetic patient demographic generation (`PatientDataFactory`)
- [x] Patient Registration & Search test suites
- [ ] Appointment Scheduling & Calendar management tests
- [ ] Flowboard status progression (Arrived ➡️ In Room ➡️ With Provider ➡️ Done)
- [ ] Clinical vitals intake & validation
- [ ] Physician SOAP encounter documentation & coding
- [ ] CI/CD integration with GitHub Actions

---

## 🤝 Contributing

1. Fork the repository.
2. Create a descriptive feature branch: `git checkout -b feature/new-page-object`.
3. Commit your changes following standard commit conventions: `git commit -m "feat: add appointment scheduling page object"`.
4. Push to the branch: `git push origin feature/new-page-object`.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) (or as designated in the repository).
