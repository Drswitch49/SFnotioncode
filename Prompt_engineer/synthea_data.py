from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

# Example static data, simulating a patient database
PATIENT_DATA = [
    {
        'BIRTHDATE': '1990-01-01',
        'GENDER': 'Male',
        'description_cond': 'lung cancer',
        'observation': 'increased cough',
        'DESCRIPTION_careplan': 'regular monitoring',
        'modality': 'X-Ray',
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
        Retrieves a random patient's data who has been diagnosed with a specified condition.
        """
        matching_patients = [patient for patient in PATIENT_DATA if diagnosis in patient['description_cond']]
        if matching_patients:
            selected_patient = random.choice(matching_patients)
            age = relativedelta(datetime.now(), datetime.strptime(selected_patient['BIRTHDATE'], '%Y-%m-%d')).years
            patient_data = {
                'age': age,
                'gender': selected_patient['GENDER'],
                'conditions': selected_patient['description_cond'],
                'observations': selected_patient['observation'],
                'care_plans': selected_patient['DESCRIPTION_careplan'],
                'modality': selected_patient.get('modality', "Not specified"),
                'body_area': selected_patient.get('body_area', "Not specified")
            }
            modality = selected_patient.get('modality')
            body_area = selected_patient.get('body_area')
            return patient_data, modality, body_area
        else:
            return None, None, None
