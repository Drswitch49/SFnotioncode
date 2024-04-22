# main.py
import argparse
import yaml
import pandas as pd
from typing import Dict, Any, Optional

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load the YAML configuration file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file) or {}
    return config

def generate_medical_prompt(patient_data: Dict[str, Any], diagnosis: str, config: Dict[str, Any]) -> str:
    """
    Generate a medical prompt for the medical report based on patient data and diagnosis details using a template from the configuration.
    """
    prompt_template = config.get('prompt_template', "Default template if not specified in config.")
    prompt = prompt_template.format(
        diagnosis=diagnosis,
        age=patient_data['BIRTHDATE'],
        gender=patient_data['GENDER'],
        conditions=patient_data['DESCRIPTION_cond'],
        observations=', '.join(patient_data.get('observations', [])),  # Assuming this needs a similar change
        care_plans=patient_data['DESCRIPTION_careplan'],
        modality=patient_data.get('modality', "Not specified"),  # Assuming a similar field needs to be added or changed
        body_area=patient_data.get('body_area', "Not specified")
    )
    return prompt

def load_patient_data(csv_path: str) -> pd.DataFrame:
    """
    Load patient data from a CSV file.
    """
    return pd.read_csv(csv_path)

def select_random_patient_data(patient_data: pd.DataFrame, diagnosis: str) -> Optional[Dict[str, Any]]:
    """
    Select random patient data with a specific diagnosis.
    """
    matching_patients = patient_data[patient_data['REASONDESCRIPTION'] == diagnosis]
    if not matching_patients.empty:
        return matching_patients.sample(n=1).iloc[0].to_dict()
    return None

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Medical Report Generator')
    parser.add_argument('--config_path', type=str, default='/Users/ayodejioyesanya/Documents/SFdev/Prompt_engineer/config.yaml', help='Path to the YAML configuration file.')
    return parser.parse_args()

def main() -> None:
    """
    Main function to orchestrate the workflow.
    """
    args = parse_arguments()
    config = load_config(args.config_path)
    patient_data = load_patient_data(config['cleaned_data_csv_path'])
    diagnosis = "Lung Cancer"  # Example diagnosis
    random_patient_data = select_random_patient_data(patient_data, diagnosis)

    if random_patient_data:
        medical_prompt = generate_medical_prompt(random_patient_data, diagnosis, config)
        print(medical_prompt)
    else:
        print("No patient data found for the given diagnosis.")

if __name__ == '__main__':
    main()
