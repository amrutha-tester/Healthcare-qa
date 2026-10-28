# 🔗 Requirements Traceability Matrix (RTM)

| Document ID | System Under Test | Total Requirements | Total Automated Test Executions | Latest CI Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| `RTM-OEMR-2026-01` | OpenEMR v8.4.1 | `22 Clinical & System Requirements` | `46 (15 Cross-Browser Smoke + 31 Regression/E2E)` | **100% (46 / 46 Passed)** |

---

## Traceability Overview

In accordance with **IEC 62304** (Medical Device Software Lifecycle) and **ISO 13485** (Quality Management Systems), this matrix provides bidirectional traceability between **System / Clinical Requirements**, **Risk & Regulatory Classifications**, **Automated Pytest Verification Scripts**, and **CI Execution Results**.

### Safety & Regulatory Legend
- **IEC 62304 Class C:** High Risk — Failure could result in serious patient injury (e.g., missed drug allergy, wrong prescription, unflagged critical vitals, duplicate patient record mix-up).
- **IEC 62304 Class B:** Moderate Risk — Failure could result in delayed care, unauthorized access, or unsigned clinical documentation.
- **IEC 62304 Class A:** Low Risk — Administrative, scheduling, or billing functionality with no direct patient safety impact.
- **HIPAA § 164.312:** Access control, unique user identification, and role-based authorization.
- **FDA 21 CFR Part 11:** Electronic records and password-authenticated electronic signatures (`Locked` encounter state).

---

## 1. System & Functional Requirements Traceability (`REQ-001` – `REQ-018`)

| Req ID | Requirement Description | Regulatory / Safety Class | Automated Test File & Test Case(s) | Browser Coverage | Latest CI Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-001** | The EHR web server shall be reachable over HTTP and render the authentication interface across supported browsers. | `IEC 62304 Class A` | `tests/test_01_smoke.py`<br>• `test_environment_connection` | Chromium, Firefox, WebKit | ✅ **PASS** |
| **REQ-002** | The system shall enforce Role-Based Access Control (RBAC), allowing valid logins for Admin, Physician, Clinician, and Receptionist roles while rejecting invalid credentials. | `IEC 62304 Class B`<br>`HIPAA § 164.312(a)(1)` | `tests/test_02_role_based_login.py`<br>• `test_admin_login`<br>• `test_physician_login`<br>• `test_clinician_login`<br>• `test_receptionist_login`<br>• `test_login_invalid_credentials` | Chromium, Firefox, WebKit | ✅ **PASS** |
| **REQ-003** | A Receptionist shall be able to register a new patient with complete demographics, and the system shall block registration when mandatory fields (`first_name`, `last_name`) are missing. | `IEC 62304 Class B` | `tests/test_03_rec_register_patient.py`<br>• `test_receptionist_can_register_new_patient`<br>• `test_registration_fails_when_mandatory_field_missing[last_name]`<br>• `test_registration_fails_when_mandatory_field_missing[first_name]` | Chromium | ✅ **PASS** |
| **REQ-004** | The system shall detect and warn the user via a duplicate-check modal when attempting to register a patient with identical demographics to an existing patient. | `IEC 62304 Class C`<br>`ISO 14971 Patient ID` | `tests/test_04_rec_duplicate_patient.py`<br>• `test_duplicate_patient_warning` | Chromium | ✅ **PASS** |
| **REQ-005** | A Receptionist shall be able to search for and retrieve an existing patient record using their unique public Patient ID (`PID`). | `IEC 62304 Class B` | `tests/test_05_rec_search_patient.py`<br>• `test_search_patient` | Chromium | ✅ **PASS** |
| **REQ-006** | A Receptionist shall be able to schedule a new calendar appointment for a registered patient with a designated clinical provider. | `IEC 62304 Class A` | `tests/test_06_rec_new_appointment.py`<br>• `test_open_appointment_for_registered_patient` | Chromium | ✅ **PASS** |
| **REQ-007** | The calendar module shall detect provider double-booking conflicts when scheduling overlapping appointments for the same provider and time slot. | `IEC 62304 Class A` | `tests/test_07_rec_double_booking.py`<br>• `test_provider_double_booking_conflict` | Chromium | ✅ **PASS** |
| **REQ-008** | A Receptionist shall be able to reschedule an existing appointment to a new time slot and cancel/delete an appointment from the calendar grid. | `IEC 62304 Class A` | `tests/test_08_rec_reschedule_cancel_apt.py`<br>• `test_reschedule_appointment`<br>• `test_cancel_appointment` | Chromium | ✅ **PASS** |
| **REQ-009** | A Receptionist shall be able to check in a patient (`Arrived @` status), assign an exam room, and propagate the patient to the clinical Flow Board. | `IEC 62304 Class B` | `tests/test_09_rec_check_in_patient.py`<br>• `test_check_in_patient` | Chromium | ✅ **PASS** |
| **REQ-010** | A Clinician shall be able to filter the Flow Board by provider and patient name and open the checked-in patient's clinical chart and encounter. | `IEC 62304 Class B` | `tests/test_10_clin_select_checkedin_patient.py`<br>• `test_select_checkedin_patient` | Chromium | ✅ **PASS** |
| **REQ-011** | A Clinician shall be able to record patient vitals (Weight, Height, BP, Pulse, SpO2) with automatic BMI calculation, while the system rejects non-numeric vitals and flags critical/abnormal values. | `IEC 62304 Class C`<br>`ISO 14971 Clinical Risk` | `tests/test_11_clin_record_vitals.py`<br>• `test_recording_vitals`<br>• `test_invalid_vitals`<br>• `test_abnormal_vitals` | Chromium | ✅ **PASS** |
| **REQ-012** | A Clinician shall be able to record a patient drug allergy (`penicillin`) and reaction severity (`Mild`), and the allergy shall be visibly displayed on the Patient Dashboard. | `IEC 62304 Class C`<br>`ISO 14971 Medication Safety` | `tests/test_12_clin_add_allergy.py`<br>• `test_add_allergy` | Chromium | ✅ **PASS** |
| **REQ-013** | A Clinician shall be able to update and advance the patient's triage status on the clinical Flow Board. | `IEC 62304 Class B` | `tests/test_13_clin_status_advance.py`<br>• `test_status_advance` | Chromium | ✅ **PASS** |
| **REQ-014** | A Physician shall be able to document a full SOAP note (Subjective, Objective, Assessment, Plan) and electronically sign it, locking the record (`Locked` badge). | `IEC 62304 Class B`<br>`FDA 21 CFR Part 11` | `tests/test_14_phy_enter_soapnote.py`<br>• `test_enter_soap_note` | Chromium | ✅ **PASS** |
| **REQ-015** | A Physician shall be able to save and electronically sign a partial SOAP note, transitioning the clinical form to an immutable `Locked` state. | `IEC 62304 Class B`<br>`FDA 21 CFR Part 11` | `tests/test_15_phy_partial_soapnote.py`<br>• `test_partial_soap_note` | Chromium | ✅ **PASS** |
| **REQ-016** | The e-Signature module shall reject electronic signature attempts when an invalid physician password is supplied and keep the SOAP note unlocked. | `IEC 62304 Class B`<br>`FDA 21 CFR Part 11`<br>`HIPAA § 164.312(d)` | `tests/test_16_phy_esign_validation.py`<br>• `test_esign_invalid_password` | Chromium | ✅ **PASS** |
| **REQ-017** | A Physician shall be able to prescribe medication (`amoxicillin 500mg`) with dosage and route instructions, and the prescription shall appear on the Patient Dashboard. | `IEC 62304 Class C`<br>`ISO 14971 Medication Safety` | `tests/test_17_phy_add_prescription.py`<br>• `test_add_prescription` | Chromium | ✅ **PASS** |
| **REQ-018** | A Physician shall be able to assign standardized CPT4 procedure codes (`99201`) to the patient encounter via the Fee Sheet. | `IEC 62304 Class A` | `tests/test_18_phy_add_fee_sheet_code.py`<br>• `test_add_fee_sheet_codes` | Chromium | ✅ **PASS** |

---

## 2. End-to-End Multi-Role Workflow Requirements (`REQ-019` – `REQ-022`)

| Req ID | Workflow Requirement Description | Regulatory / Safety Class | Automated Workflow Script | Personas Verified | Latest CI Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-019** | **Front-Office Intake Workflow:** Complete patient registration, appointment creation, check-in (`Arrived @`), and Flow Board propagation in a single continuous receptionist session. | `IEC 62304 Class B` | `tests/workflows/test_01_receptionist_workflow.py`<br>• `test_receptionist_workflow` | Receptionist | ✅ **PASS** |
| **REQ-020** | **Nursing Triage Workflow:** Select checked-in patient from Flow Board, record vitals & verify BMI, document drug allergy, and advance visit status. | `IEC 62304 Class C` | `tests/workflows/test_02_clinician_workflow.py`<br>• `test_clinician_workflow` | Clinician | ✅ **PASS** |
| **REQ-021** | **Physician Encounter Workflow:** Select triaged patient, document & e-Sign SOAP note (`21 CFR Part 11`), prescribe medication (`amoxicillin`), record CPT4 Fee Sheet billing (`99201`), and advance visit to `Completed ($)`. | `IEC 62304 Class C`<br>`FDA 21 CFR Part 11` | `tests/workflows/test_03_physician_workflow.py`<br>• `test_physician_workflow` | Physician | ✅ **PASS** |
| **REQ-022** | **Full Hospital Visit E2E Lifecycle:** Multi-role clinical handoff across separate authenticated browser contexts from Receptionist (Registration & Check-In) ➡️ Clinician (Vitals & Allergy Triage) ➡️ Physician (SOAP Note, e-Sign, Prescription, CPT4 Coding & Checkout). | `IEC 62304 Class C`<br>`FDA 21 CFR Part 11`<br>`HIPAA § 164.312` | `tests/workflows/test_04_e2e_workflow.py`<br>• `test_e2e_workflow` | Receptionist + Clinician + Physician | ✅ **PASS** |

---

## 3. Summary Metrics by Safety Class

| IEC 62304 Safety Class | Requirements Mapped | Automated Tests Passing | Coverage |
| :--- | :--- | :--- | :--- |
| 🔴 **Class C (Patient Safety Critical)** | `6` (`REQ-004`, `011`, `012`, `017`, `020`, `021`, `022`) | `100%` | **100%** |
| 🟠 **Class B (Clinical Integrity & RBAC)** | `10` (`REQ-002`, `003`, `005`, `009`, `010`, `013`, `014`, `015`, `016`, `019`) | `100%` | **100%** |
| 🟢 **Class A (Administrative & Billing)** | `5` (`REQ-001`, `006`, `007`, `008`, `018`) | `100%` | **100%** |
| **Total** | **22 Requirements** | **46 / 46 Test Executions Passed** | **100%** |
