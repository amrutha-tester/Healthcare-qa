from typing import Dict

# Standard OpenEMR demo credentials mapped by role
ROLES: Dict[str, Dict[str, str]] = {
    "admin": {
        "username": "admin",
        "password": "pass",
        "description": "Full administrative and ACL configuration privileges"
    },
    "physician": {
        "username": "physician",
        "password": "physician",
        "description": "Provider access: SOAP notes, orders, fee sheet entry"
    },
    "clinician": {
        "username": "clinician",
        "password": "clinician",
        "description": "Nursing access: vitals recording, patient intake triage"
    },
    "accountant": {
        "username": "accountant",
        "password": "accountant",
        "description": "Billing access: checkout, copays, fee sheet reviews"
    },
    "receptionist": {
        "username": "receptionist",
        "password": "receptionist",
        "description": "Front desk: registration, search, calendar scheduling"
    }
}