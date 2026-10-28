# 📋 Software Verification & Validation (V&V) Test Plan

| Document ID | Version | System Under Test (SUT) | Regulatory Alignment | Status |
| :--- | :--- | :--- | :--- | :--- |
| `TP-OEMR-2026-01` | `1.0` | OpenEMR v8.4.1 (Containerized EHR) | IEC 62304, ISO 13485, FDA 21 CFR Part 11, HIPAA | **Approved / Active** |

---

## 1. Purpose & Scope

This Software Verification Test Plan defines the strategy, risk classification, test levels, environment controls, and acceptance criteria for verifying the **OpenEMR Electronic Health Record (EHR)** system.

The automation suite validates critical clinical and administrative workflows across role-based personas (**Receptionist**, **Clinician**, **Physician**, and **Administrator**), ensuring functional accuracy, patient safety controls, electronic signature integrity, and cross-browser compatibility.

---

## 2. Regulatory & Quality Standards Awareness

In regulated healthcare and medical software environments, verification activities must demonstrate traceability, repeatability, and risk-based coverage. This framework is designed with awareness of the following standards:

| Standard / Regulation | Relevance to This Automation Framework |
| :--- | :--- |
| **IEC 62304** *(Medical Device Software — Software Life Cycle Processes)* | Categorizes tests by software safety class (**Class A, B, C**) based on potential patient harm (e.g., allergy documentation, abnormal vitals, and medication prescribing are treated as Class C safety-critical paths). |
| **ISO 13485** *(Medical Devices — Quality Management Systems)* | Enforces repeatable, deterministic test execution inside isolated Docker containers with automated generation of auditable JUnit XML and timestamped HTML test evidence in Azure DevOps CI/CD. |
| **ISO 14971** *(Application of Risk Management to Medical Devices)* | Drives negative and boundary testing for clinical hazards: duplicate patient identity collisions, provider double-booking, invalid vitals input, abnormal vitals flags, and unauthorized e-Signatures. |
| **FDA 21 CFR Part 11** *(Electronic Records; Electronic Signatures)* | Validates that clinical encounter SOAP notes require password re-authentication to sign, transition to an immutable `Locked` state upon signing, and reject invalid credentials. |
| **HIPAA Security & Privacy Rules** *(45 CFR § 164.312)* | Validates Role-Based Access Control (RBAC) across 5 clinical personas and uses 100% synthetic, non-PHI patient data generated dynamically via `Faker` (`PatientDataFactory`). |

---

## 3. Risk-Based Test Classification (IEC 62304 Alignment)

All test cases in this repository are classified into three safety tiers according to **IEC 62304**:

- 🔴 **Class C (High Clinical Risk — Serious Injury / Patient Harm Possible):**
  - Drug allergy documentation & Dashboard visibility (`test_12_clin_add_allergy.py`)
  - Medication prescription entry & dosage verification (`test_17_phy_add_prescription.py`)
  - Clinical vitals capture, BMI calculation & abnormal vitals detection (`test_11_clin_record_vitals.py`)
  - Duplicate patient identity warning during registration (`test_04_rec_duplicate_patient.py`)
  - Full multi-role clinical handoff (`test_04_e2e_workflow.py`)
- 🟠 **Class B (Moderate Risk — Non-Serious Injury / Clinical Delay or Record Integrity Issue):**
  - Role-Based Access Control & authentication (`test_02_role_based_login.py`)
  - Physician SOAP note documentation & 21 CFR Part 11 e-Signature locking (`test_14`, `test_15`, `test_16`)
  - Patient registration mandatory field validation & PID search (`test_03`, `test_05`)
  - Patient check-in & Flow Board status transitions (`test_09`, `test_10`, `test_13`)
- 🟢 **Class A (Low Risk — No Patient Harm; Administrative / Scheduling / Billing):**
  - System reachability smoke checks (`test_01_smoke.py`)
  - Appointment scheduling, double-booking conflict, reschedule & cancellation (`test_06`, `test_07`, `test_08`)
  - CPT4 Fee Sheet billing code entry (`test_18_phy_add_fee_sheet_code.py`)

---

## 4. Test Levels & Execution Strategy

| Test Level | Pytest Marker | Target Browsers | Execution Trigger | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Level 1: Cross-Browser Smoke Suite** | `-m smoke` | Chromium, Firefox, WebKit | Every Push / PR (Stage 3A) | Verifies server availability, SSL/HTTP response, and RBAC authentication across all 3 major browser engines (`15 test executions`). |
| **Level 2: Functional & Negative Regression** | `-m regression` | Chromium (Headless) | Every Push / PR (Stage 3B) | Verifies individual clinical modules, boundary conditions, negative inputs, and modal validations (`22 test executions`). |
| **Level 3: End-to-End Clinical Workflows** | `-m workflow` | Chromium (Headless) | Every Push / PR (Stage 3B) | Validates stateful, multi-step journeys for Receptionist, Clinician, Physician, and the full 3-role hospital visit lifecycle (`4 E2E workflows`). |

---

## 5. Test Environment & Data Hygiene Controls

To satisfy **ISO 13485** repeatability requirements and prevent test-data contamination across runs:

1. **Containerized Infrastructure (`docker-compose.yml`):**
   - **Database:** `mariadb:11.4` configured with UTF-8 (`utf8mb4`) character sets and automated healthchecks.
   - **Application:** `openemr/openemr:latest` (v8.4.1 on Apache / PHP 8.3).
   - **Test Runner:** `mcr.microsoft.com/playwright/python:v1.48.0-noble` with pre-installed Chromium, Firefox, and WebKit binaries.
2. **Deterministic Database Seeding & Cleanup (`docker/seed_demo_users.sql` & `conftest.py`):**
   - Before and after every test run, automated SQL routines seed standardized GACL user roles (`receptionist`, `clinician`, `physician`, `accountant`, `admin`) and truncate transactional clinical tables (`patient_data`, `form_encounter`, `forms`, `esign_signatures`, `form_soap`, `form_vitals`, `lists`, `prescriptions`, `billing`, `patient_tracker`).
3. **Synthetic Non-PHI Data (`src/utils/data_generator.py`):**
   - No real Protected Health Information (PHI) is stored or used. All patient names, SSNs, addresses, and clinical notes are synthetically generated at runtime with a `Test_` prefix.

---

## 6. Entry & Exit Criteria (Definition of Done)

### Entry Criteria
- `mysql` and `openemr` Docker containers are healthy and returning `HTTP 200` on `/interface/login/login.php?site=default`.
- `docker/seed_demo_users.sql` has executed with exit code `0`.

### Exit Criteria
- **100% Pass Rate** on Cross-Browser Smoke Tests (`15 / 15` across Chromium, Firefox, WebKit).
- **100% Pass Rate** on Regression and E2E Clinical Workflow Tests (`31 / 31` on Chromium).
- Zero unresolved **Class C** or **Class B** defects.
- JUnit XML (`junit-*.xml`) and self-contained HTML reports (`report-*.html`) published to Azure DevOps Pipeline Artifacts for audit traceability.
