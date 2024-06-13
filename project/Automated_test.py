import os
import pandas as pd

# Define the Ingestion class
class Ingestion:
    def __init__(self, file_path):
        self.file_path = file_path

    def ingest_from_file(self):
        return pd.read_csv(self.file_path)

# Define the DataPrep class
class DataPrep:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        # Mocked data cleaning logic
        return {
            'cleaned_data.csv': self.df[['Area', 'Year', 'Crop', 'Production']]
        }

# Define the SaveData class
class SaveData:
    def __init__(self, cleaned_data):
        self.cleaned_data = cleaned_data

    def save_to_directory(self):
        # Save logic
        data_dir = "/content/data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        for filename, df in self.cleaned_data.items():
            df.to_csv(os.path.join(data_dir, filename), index=False)

# Function to run the pipeline
def run_pipeline(file_path):
    print("Initializing test data ingestion...")
    ingestion = Ingestion(file_path)
    print("Testing ingestion from file...")
    df = ingestion.ingest_from_file()
    print("Completed ingestion successfully...")

    # Perform data cleaning
    prep = DataPrep(df)
    cleaned_data = prep.clean_data()

    # Save cleaned data
    save_data = SaveData(cleaned_data)
    save_data.save_to_directory()

    # Verify saved files
    data_dir = "/content/data"
    expected_files = ['cleaned_data.csv']
    for file in expected_files:
        assert os.path.exists(os.path.join(data_dir, file)), f"{file} should be saved in the data directory"

    print("Full pipeline test passed.")

# File path to CSV
file_path = "/content/crop_production.csv"

# Run the pipeline
run_pipeline(file_path)
