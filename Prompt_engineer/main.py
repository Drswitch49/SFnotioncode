import argparse
import yaml
from typing import Dict, Any, Optional
from synthea_data import SyntheaData

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
        age=patient_data['age'],
        gender=patient_data['gender'],
        conditions=', '.join(patient_data['conditions']),
        observations=', '.join(patient_data['observations']),
        care_plans=', '.join(patient_data['care_plans']),
        modality=patient_data.get('modality', "Not specified"),
        body_area=patient_data.get('body_area', "Not specified")
    )
    return prompt

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Medical Report Generator')
    parser.add_argument('--config_path', type=str, default='./config.yaml', help='Path to the YAML configuration file.')
    return parser.parse_args()

def main() -> None:
    """
    Main function to orchestrate the workflow.
    """
    args = parse_arguments()
    config = load_config(args.config_path)

    synthea_data = SyntheaData()
    diagnosis = "lung cancer"  # Example diagnosis
    patient_data, modality, body_area = synthea_data.get_patient_data_by_diagnosis(diagnosis)

    if patient_data:
        medical_prompt = generate_medical_prompt(patient_data, diagnosis, config)
        print(medical_prompt)
    else:
        print("No patient data found for the given diagnosis.")

if __name__ == '__main__':
    main()
