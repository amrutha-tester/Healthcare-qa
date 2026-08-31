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