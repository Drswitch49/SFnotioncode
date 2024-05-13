import argparse
import yaml
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load the YAML configuration file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file) or {}
    return config

def calculate_age(birthdate: str) -> int:
    """
    Calculate age given the birthdate.
    """
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def generate_medical_prompt(patient_data: Dict[str, Any], diagnosis: str, config: Dict[str, Any]) -> str:
    """
    Generate a medical prompt for the medical report based on patient data and diagnosis details using a template from the configuration.
    Uses REASONDESCRIPTION as the source for the patient's conditions.
    """
    prompt_template = config.get('prompt_template', "Default template if not specified in config.")
    age = calculate_age(patient_data['BIRTHDATE'])  # Calculating age using the BIRTHDATE field
    conditions = patient_data.get('REASONDESCRIPTION', 'No reason description provided')  # Default message if not specified
    prompt = prompt_template.format(
        diagnosis=diagnosis,
        age=age,
        gender=patient_data['GENDER'],
        conditions=conditions,  # Correct field used
        observations=patient_data.get('observation', 'No observations recorded'),  # Use correct field for observations
        care_plans=patient_data.get('DESCRIPTION_careplan', 'No care plans recorded'),
        modality=patient_data.get('modality', "Not specified"),
        body_area=patient_data.get('body_area', "Not specified")
    )
    return prompt

def load_patient_data(csv_path: str) -> pd.DataFrame:
    """
    Load patient data from a CSV file.
    """
    return pd.read_csv(csv_path)

def select_random_patient_data(patient_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Select random patient data from the entire dataset, independent of the diagnosis.
    """
    return patient_data.sample(n=1).iloc[0].to_dict()

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Medical Report Generator')
    parser.add_argument('--config_path', type=str, default='/Users/ayodejioyesanya/Documents/SFdev/Prompt_engineer/config.yaml', help='Path to the YAML configuration file.')
    parser.add_argument('--csv_path', type=str, default='/Users/ayodejioyesanya/Desktop/Tdata/cleaned_medical_data.csv', help='Path to the CSV file containing patient data.')
    parser.add_argument('--diagnosis', type=str, required=True, help='Diagnosis determined by the image classifier.')
    return parser.parse_args()

def main() -> None:
    """
    Main function to orchestrate the workflow.
    """
    args = parse_arguments()
    config = load_config(args.config_path)
    patient_data = load_patient_data(args.csv_path)
    diagnosis = args.diagnosis  # Diagnosis passed from the command line
    random_patient_data = select_random_patient_data(patient_data)

    if random_patient_data:
        medical_prompt = generate_medical_prompt(random_patient_data, diagnosis, config)
        print(medical_prompt)
    else:
        print("No patient data available.")

if __name__ == '__main__':
    main()
