import pandas as pd
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, Any, Tuple, Optional
import yaml
import argparse

class SyntheaData:
    """
    Handles operations related to processing and retrieving patient data from a consolidated dataset.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    def get_patient_data_by_diagnosis(self, diagnosis: str) -> Tuple[Dict[str, Any], Optional[str], Optional[str]]:
        conn = sqlite3.connect(self.config['database_path'])
        query = """
        SELECT * FROM cleaned_medical_data
        WHERE DESCRIPTION_cond LIKE ? OR REASONDESCRIPTION LIKE ?
        """
        df = pd.read_sql_query(query, conn, params=(f'%{diagnosis}%', f'%{diagnosis}%'))
        conn.close()

        if not df.empty:
            selected_row = df.sample(n=1).iloc[0]
            patient_data = {
                'age': relativedelta(datetime.now(), datetime.strptime(selected_row['BIRTHDATE'], '%Y-%m-%d')).years,
                'gender': selected_row['GENDER'],
                'conditions': [selected_row['DESCRIPTION_cond']],
                'observations': [selected_row.get('observation', '')],
                'care_plans': [selected_row.get('DESCRIPTION_careplan', '')],
            }
            modality = selected_row.get('modality', None)
            body_area = selected_row.get('body_area', None)
            return patient_data, modality, body_area
        else:
            return {}, None, None

    def import_cleaned_data_to_sqlite(self) -> None:
        conn = sqlite3.connect(self.config['database_path'])
        df = pd.read_csv(self.config['cleaned_data_csv_path'])
        df.to_sql('cleaned_medical_data', conn, if_exists='replace', index=False)
        conn.close()

def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Medical Report Generator')
    parser.add_argument('--config_path', type=str, default='/Users/ayodejioyesanya/Documents/SFdev/Prompt_engineer/config.yaml', help='Path to the YAML configuration file.')
    return parser.parse_args()

def generate_report(patient_data: Dict[str, Any]) -> str:
    """
    Generates a textual report based on the patient data.
    """
    report_lines = [
        f"Patient Age: {patient_data['age']}",
        f"Gender: {patient_data['gender']}",
        f"Conditions: {', '.join(patient_data['conditions'])}",
        f"Observations: {', '.join(patient_data['observations'])}",
        f"Care Plans: {', '.join(patient_data['care_plans'])}",
    ]
    report = "\n".join(report_lines)
    return report

def main():
    args = parse_arguments()
    config = load_config(args.config_path)

    data_processor = SyntheaData(config)
    # Call import_cleaned_data_to_sqlite to ensure the database is populated before making queries
    data_processor.import_cleaned_data_to_sqlite()  # Make sure this line is uncommented and called here

    # Use "Prediabetes" as the example diagnosis to query
    diagnosis = "Prediabetes"
    patient_data, modality, body_area = data_processor.get_patient_data_by_diagnosis(diagnosis)
    print(patient_data, modality, body_area)

    if patient_data:  # Ensure there is data to generate a report from
        report = generate_report(patient_data)
        print("Generated Report:", report)
    else:
        print("No patient data found for the given diagnosis.")

if __name__ == '__main__':
    main()
