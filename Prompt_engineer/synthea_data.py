from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

# Example static data, simulating a patient database
PATIENT_DATA = [
    {
        'BIRTHDATE': '1990-01-01',
        'GENDER': 'Male',
        'REASONDESCRIPTION': 'lung cancer',
        'observation': 'increased cough',
        'DESCRIPTION_careplan': 'regular monitoring',
        'modality': 'X-Ray',
        'body_area': 'Chest'
    },
    {
        'BIRTHDATE': '1985-05-15',
        'GENDER': 'Female',
        'REASONDESCRIPTION': '',  # This patient has no diagnosis specified.
        'observation': 'shortness of breath',
        'DESCRIPTION_careplan': 'oxygen therapy',
        'modality': 'CT Scan',
        'body_area': 'Chest'
    },
    # Additional records can be added here.
]

class SyntheaData:
    """
    Simulates data retrieval from a static dataset.
    """
    def get_patient_data_by_diagnosis(self, diagnosis: str) -> Tuple[Dict[str, Any], Optional[str], Optional[str]]:
        """
        Retrieves a random patient's data who has been diagnosed with a specified condition using the REASONDESCRIPTION.
        If no diagnosis is provided in REASONDESCRIPTION, it defaults to "Nil significant past medical history."
        """
        # Filtering patients based on diagnosis, considering those with empty or null diagnosis as having no significant history.
        matching_patients = [patient for patient in PATIENT_DATA if patient['REASONDESCRIPTION'].strip().lower() == diagnosis.lower()] if diagnosis.strip() else [patient for patient in PATIENT_DATA if not patient['REASONDESCRIPTION'].strip()]

        if matching_patients:
            selected_patient = random.choice(matching_patients)
            age = relativedelta(datetime.now(), datetime.strptime(selected_patient['BIRTHDATE'], '%Y-%m-%d')).years
            patient_data = {
                'age': age,
                'gender': selected_patient['GENDER'],
                'conditions': selected_patient['REASONDESCRIPTION'] if selected_patient['REASONDESCRIPTION'].strip() else "Nil significant past medical history",
                'observations': selected_patient['observation'],
                'care_plans': selected_patient['DESCRIPTION_careplan'],
                'modality': selected_patient.get('modality', "Not specified"),
                'body_area': selected_patient.get('body_area', "Not specified")
            }
            modality = selected_patient.get('modality')
            body_area = selected_patient.get('body_area')
            return patient_data, modality, body_area
        else:
            # Default case when no patients match the criteria, including empty diagnosis search
            return ({
                'age': None,
                'gender': None,
                'conditions': "Nil significant past medical history",
                'observations': None,
                'care_plans': None,
                'modality': None,
                'body_area': None
            }, None, None)
