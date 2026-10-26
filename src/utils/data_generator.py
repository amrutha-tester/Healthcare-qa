# src/utils/data_generator.py
from faker import Faker
import random
from typing import Dict, Any

fake = Faker()

class PatientDataFactory:
    """Generates synthetic patient demographics for EMR testing."""

    @staticmethod
    def generate_patient() -> Dict[str, Any]:
        gender = random.choice(["Male", "Female"])
        first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
        last_name = f"Test_{fake.last_name()}_{fake.lexify('???')}"  # Prefix helps identify automation test data
        
        return {
            "title": "Mr." if gender == "Male" else "Ms.",
            "first_name": first_name,
            "middle_name": fake.first_name()[0],
            "last_name": last_name,
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d"),
            "gender": gender,
            "s.s.": fake.ssn(),
            "phone": fake.numerify(text="555-###-####"),
            "email": fake.email(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
        }

class AppointmentDataFactory:
    """Generates synthetic appointment data for EMR testing."""
    @staticmethod
    def generate_appointment(patient: str = None) -> Dict[str, Any]:
        return {
            "category": random.choice(["Office Visit", "Established Patient", "New Patient"]),
            "patient": patient if patient is not None else f"Test_{fake.last_name()}",
            "provider": "6",
            "hour": random.choice(["09", "10", "11", "12", "13", "14", "15", "16"]),
            "minute": random.choice(["00", "15", "30", "45"]),
            "duration": random.choice(["15", "30", "45"]),
            "comments": fake.sentence(),
        }

class VitalsDataFactory:
    """Generates synthetic vitals data for EMR testing."""
    @staticmethod
    def generate_vitals() -> Dict[str, Any]:
        return {
            "systolic": "120",
            "diastolic": "80",
            "pulse": "72",
            "spo2": "98",
            "height_cm": "150",
            "weight_kg": "50",
            "expected_bmi": "22"
        }

    @staticmethod
    def generate_invalid_vitals() -> Dict[str, Any]:
        return {
            "systolic": "180",
            "diastolic": "120",
            "pulse": "xyz",
            "spo2": "98",
            "height_cm": "170",
            "weight_kg": "80",
            "expected_bmi": "28"
        }
    @staticmethod
    def generate_abnormal_vitals() -> Dict[str, Any]:
        return {
        "systolic": "210",
        "diastolic": "130",
        "pulse": "155",
        "spo2": "85",
        "height_cm": "150",
        "weight_kg": "110",
        "expected_bmi": "49"
    }

class SoapNoteDataFactory:
    """Generates synthetic SOAP note data for EMR testing."""
    @staticmethod
    def generate_soap_note()-> Dict[str, Any]:
        return {
    "subjective": (
        "Synthetic patient presents for a routine follow-up visit. "
        "Reports feeling well with no new concerns. "
        "Denies fever, cough, chest discomfort, shortness of breath, "
        "or dizziness. "
        "This note contains fictional data created exclusively "
        "for automation testing."
    ),
    "objective": (
        "Blood pressure: 120/80 mmHg. "
        "Pulse: 72 beats per minute. "
        "Oxygen saturation: 98%. "
        "Height: 59.06 in (150.00 cm). "
        "Weight: 110.23 lb (50.00 kg). "
        "BMI: 22 kg/m², as displayed by the application. "
        "BMI status: Normal, as displayed by the application. "
        "No additional examination findings entered for this synthetic encounter."
    ),
    "assessment": (
        "Routine follow-up encounter for a fictional patient. "
        "Vital-sign documentation completed. "
        "The application displays BMI as 22 kg/m² "
        "and BMI status as Normal. "
        "No real clinical diagnosis is established by this test note."
    ),
    "plan": (
        "Save the SOAP note and verify that all four sections persist "
        "after reopening. "
        "Confirm that the note is associated with the correct patient "
        "and encounter. "
        "Complete the configured e-signature and locking workflow. "
        "Verify that the signed form is read-only. "
        "No actual medication, investigation, or treatment is prescribed."
    ),
}
    @staticmethod
    def generate_incomplete_soap_note() -> Dict[str, Any]:
        return {
    "subjective": (
        "Synthetic patient presents for a routine follow-up visit. "
        "Reports feeling well with no new concerns. "
        "Denies fever, cough, chest discomfort, shortness of breath, "
        "or dizziness. "
        "This note contains fictional data created exclusively "
        "for automation testing."
    ),
    "objective": (
        "Blood pressure: 120/80 mmHg. "
        "Pulse: 72 beats per minute. "
        "Oxygen saturation: 98%. "
        "Height: 59.06 in (150.00 cm). "
        "Weight: 110.23 lb (50.00 kg). "
        "BMI: 22 kg/m², as displayed by the application. "
        "BMI status: Normal, as displayed by the application. "
        "No additional examination findings entered for this synthetic encounter."
    ),
    "assessment": (
        "Routine follow-up encounter for a fictional patient. "
        "Vital-sign documentation completed. "
        "The application displays BMI as 22 kg/m² "
        "and BMI status as Normal. "
        "No real clinical diagnosis is established by this test note."
    ),
}