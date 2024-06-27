import os
import pandas as pd
import sqlite3
import kaggle
import zipfile
import shutil
import json

os.environ['KAGGLE_USERNAME'] = 'rahulnitinramraje' 
os.environ['KAGGLE_KEY'] = 'aa1f265dc17c2b5b74f6742e50ce25cb' 
   

def kaggle_download(dataset_links, download_path):
    """Download datasets from Kaggle."""
    
    
    
    for dataset in dataset_links:
        try:
            dataset_id = '/'.join(dataset.split('/')[-2:])
            kaggle.api.dataset_download_files(dataset_id, path=download_path, unzip=True)
            print(f"Downloaded and extracted {dataset_id} to {download_path}")
        except Exception as e:
            print(f"Error downloading {dataset_id}: {e}")

def csv_to_sqlite(csv_directory, sqlite_db_path):
    """Convert CSV files in a directory to a SQLite database."""
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)
            table_name = os.path.splitext(filename)[0]
            df = pd.read_csv(file_path)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Table '{table_name}' created/updated from file '{filename}'")
    
    conn.commit()
    conn.close()
    print(f"All CSV files have been imported into '{sqlite_db_path}'")

def load_combined_data(db_path):
    """Load combined data from SQLite."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql('SELECT * FROM combined_data', conn)
    conn.close()
    return df


def main_advanced():
    data_dir = '../data/'
    combined_db_path = os.path.join(data_dir, 'combined_crop_rainfall.sqlite')

    # Create necessary directories
    os.makedirs(data_dir, exist_ok=True)
    downloads_dir = os.path.join(data_dir, 'downloads')
    os.makedirs(downloads_dir, exist_ok=True)

    # Download datasets from Kaggle
    kaggle_datasets = [
        "https://www.kaggle.com/datasets/thedevastator/the-relationship-between-crop-production-and-cli",
        "https://www.kaggle.com/datasets/aksahaha/rainfall-india"
    ]
    kaggle_download(kaggle_datasets, downloads_dir)

    # Convert CSV files to SQLite database
    csv_to_sqlite(downloads_dir, combined_db_path)

    # Remove downloads directory after processing
    shutil.rmtree(downloads_dir)

if __name__ == "__main__":
    main_advanced()
