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
        last_name = f"Test_{fake.last_name()}"  # Prefix helps identify automation test data
        
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

   
