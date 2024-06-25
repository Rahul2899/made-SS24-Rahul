import os
import sqlite3
import pandas as pd
import kaggle
import tempfile
import pytest

# Set up Kaggle API credentials from environment variables
def setup_kaggle():
    os.environ['KAGGLE_USERNAME'] = os.getenv('KAGGLE_USERNAME')
    os.environ['KAGGLE_KEY'] = os.getenv('KAGGLE_KEY')
    kaggle.api.authenticate()

setup_kaggle()

# Define expected output files and tables
expected_files = [
    "./data/Combined_Crop_Data.csv"
]

expected_tables = {
    "Combined_Crop_Data.csv": ["Nitrogen", "Temperature", "Rainfall", "Crop", "Year", "Value"]
}

# Process Crop Recommendation data
def process_crop_recommendation_data(temp_dir):
    try:
        csv_filename = os.path.join(temp_dir, 'Crop_recommendation.csv')
        df = pd.read_csv(csv_filename)

        # Keep only the specified columns
        df = df[['N', 'temperature', 'rainfall']]
        df.columns = ['Nitrogen', 'Temperature', 'Rainfall']

        # Remove rows with null values in any column
        df.dropna(inplace=True)

        # Sample 500 rows
        df_sampled = df.sample(n=500, random_state=1)
        print(f"Crop Recommendation Dataset - Sampled Rows: {len(df_sampled)}")
        return df_sampled
    except Exception as e:
        print(f"Error processing crop recommendation data: {e}")
        return None

# Process Crop Production data
def process_crop_production_data(temp_dir):
    try:
        csv_filename = os.path.join(temp_dir, 'crop_production.csv')
        df = pd.read_csv(csv_filename)

        # Keep only the specified columns and rename them
        df = df[['State_Name', 'Crop', 'Crop_Year', 'Production']]
        df.rename(columns={'Crop_Year': 'Year', 'Production': 'Value'}, inplace=True)

        # Remove rows with null values in any column
        df.dropna(inplace=True)

        # Sample 500 rows
        df_sampled = df.sample(n=500, random_state=1)
        print(f"Crop Production Dataset - Sampled Rows: {len(df_sampled)}")
        return df_sampled
    except Exception as e:
        print(f"Error processing crop production data: {e}")
        return None

# Merge two datasets on the 'Year' column
def merge_datasets(df1, df2):
    try:
        # Assign random years from df2 to df1 for merging
        df1['Year'] = np.random.choice(df2['Year'], size=len(df1))
        merged_df = pd.merge(df1, df2, on='Year')

        # Remove rows with null values in any column in the merged dataset
        merged_df.dropna(inplace=True)

        print(f"Merged Dataset - Rows: {len(merged_df)}")
        return merged_df
    except Exception as e:
        print(f"Error merging datasets: {e}")
        return None

# Main function to download, process, merge, and save the datasets
def main():
    setup_kaggle()  

    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    dataset1_id = 'atharvaingle/crop-recommendation-dataset'
    dataset2_id = 'ankurzing/crop-production'

    with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
        if not download_and_extract_dataset(dataset1_id, temp_dir1):
            print(f"Failed to download dataset {dataset1_id}")
            return
        if not download_and_extract_dataset(dataset2_id, temp_dir2):
            print(f"Failed to download dataset {dataset2_id}")
            return

        df_crop_recommendation = process_crop_recommendation_data(temp_dir1)
        df_crop_production = process_crop_production_data(temp_dir2)

        if df_crop_recommendation is not None and df_crop_production is not None:
            merged_df = merge_datasets(df_crop_recommendation, df_crop_production)
            if merged_df is not None:
                # Save the combined dataset to CSV
                combined_path = os.path.join(data_dir, 'Combined_Crop_Data.csv')
                merged_df.to_csv(combined_path, index=False)
                print(f"Combined data saved to {combined_path}")
            else:
                print("Error: Failed to merge datasets")
        else:
            print("Error: Failed to process one or more datasets")

# Download and extract a Kaggle dataset into a specified temporary folder
def download_and_extract_dataset(dataset_id, temp_dir):
    try:
        kaggle.api.dataset_download_files(dataset_id, path=temp_dir, unzip=True)
        print(f'Dataset downloaded and extracted to {temp_dir}')
    except Exception as e:
        print(f"Error downloading and extracting dataset {dataset_id}: {e}")
        return False
    return True

# Test to check Kaggle credentials are set
def test_kaggle_credentials():
    setup_kaggle()
    username = os.getenv('KAGGLE_USERNAME')
    key = os.getenv('KAGGLE_KEY')
    assert username is not None, "Kaggle username not set"
    assert key is not None, "Kaggle key not set"

# Test to check Kaggle dataset URLs
@pytest.mark.parametrize("dataset_id", [
    "varshitanalluri/crop-recommendation-dataset",
    "thedevastator/crop-production"
])
def test_kaggle_dataset_exists(dataset_id):
    try:
        kaggle.api.dataset_download_files(dataset_id, path=tempfile.mkdtemp(), unzip=False)
    except Exception as e:
        pytest.fail(f"Dataset {dataset_id} could not be accessed. Error: {e}")

# Test to check the existence of the output files (actual check)
@pytest.mark.parametrize("filepath", expected_files)
def test_file_existence(filepath):
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

# Test to check the integrity of data in the CSV file
@pytest.mark.parametrize("csv_name,columns", expected_tables.items())
def test_data_integrity(csv_name, columns):
    df = pd.read_csv(f"./data/{csv_name}")
    for column in columns:
        assert column in df.columns, f"Column {column} not found in {csv_name}"

if __name__ == "__main__":
    main()
    pytest.main()
