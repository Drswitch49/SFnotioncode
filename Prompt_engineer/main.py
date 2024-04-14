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

def generate_medical_prompt(patient_data: Dict[str, Any], diagnosis: str, modality: Optional[str], body_area: Optional[str]) -> str:
    """
    Generate a medical prompt for the medical report based on patient data and diagnosis details.
    """
    prompt_template = (
        "Diagnosis: {diagnosis}. Patient's age: {age}. Gender: {gender}. "
        "Conditions: {conditions}. Observations: {observations}. Care plans: {care_plans}. "
        "Imaging modality: {modality}. Body area: {body_area}. "
        "Please provide a comprehensive report based on the patient's data and imaging results."
    )

    prompt = prompt_template.format(
        diagnosis=diagnosis,
        age=patient_data['age'],
        gender=patient_data['gender'],
        conditions=', '.join(patient_data['conditions']),
        observations=', '.join(patient_data['observations']),
        care_plans=', '.join(patient_data['care_plans']),
        modality=modality or "Not specified",
        body_area=body_area or "Not specified"
    )
    return prompt

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Medical Report Generator')
    # Update this path to where your config.yaml actually resides
    default_config_path = '/Users/ayodejioyesanya/Documents/SFdev/Prompt_engineer/config.yaml'
    parser.add_argument('--config_path', type=str, default=default_config_path, help='Path to the YAML configuration file.')
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
        medical_prompt = generate_medical_prompt(patient_data, diagnosis, modality, body_area)
        print(medical_prompt)
    else:
        print("No patient data found for the given diagnosis.")

if __name__ == '__main__':
    main()
