import pandas as pd
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, Any, Tuple, Optional


class SyntheaData:
    """
    Handles operations related to processing and retrieving patient data from a consolidated dataset.
    """
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initializes with configuration settings.
        """
        self.config = config

    def get_patient_data_by_diagnosis(self, diagnosis: str) -> Tuple[Dict[str, Any], Optional[str], Optional[str]]:
        """
        Retrieves a random patient's data who has been diagnosed with a specified condition.
        """
        conn = sqlite3.connect(self.config['database_path'])
        query = """
        SELECT * FROM cleaned_medical_data
        WHERE description_cond LIKE ? OR reasondescription LIKE ?
        """
        df = pd.read_sql_query(query, conn, params=(f'%{diagnosis}%', f'%{diagnosis}%'))
        conn.close()

        if not df.empty:
            selected_row = df.sample(n=1).iloc[0]
            patient_data = {
                'age': relativedelta(datetime.now(), datetime.strptime(selected_row['BIRTHDATE'], '%Y-%m-%d')).years,
                'gender': selected_row['GENDER'],
                'conditions': [selected_row['description_cond']],
                'observations': [selected_row.get('observation', '')],
                'care_plans': [selected_row.get('DESCRIPTION_careplan', '')],
            }
            modality = selected_row.get('modality', None)  # Assuming your database includes this column
            body_area = selected_row.get('body_area', None)  # Assuming your database includes this column
            return patient_data, modality, body_area
        else:
            return {}, None, None

        def import_cleaned_data_to_sqlite(self) -> None:
            """
            Imports cleaned medical data from a CSV file into an SQLite database.
            """
            conn = sqlite3.connect(self.config['database_path'])
            df = pd.read_csv(self.config['cleaned_data_csv_path'])
            # Assuming the table name you want to use is 'cleaned_medical_data'
            df.to_sql('cleaned_medical_data', conn, if_exists='replace', index=False)
            conn.close()

