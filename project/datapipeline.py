import os
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import kaggle
import zipfile
import shutil
import json

# Ensure kaggle.json is in the correct location
def setup_kaggle_api():
    #kaggle_dir = os.path.expanduser("~/.kaggle")
    kaggle_json_path = ("kaggle.json")
    
    #if not os.path.exists(kaggle_dir):
        #os.makedirs(kaggle_dir)
    
    if not os.path.exists(kaggle_json_path):
        raise FileNotFoundError("kaggle.json file not found in ~/.kaggle. Please place the file there.")
    
    os.chmod(kaggle_json_path, 0o600)  # Set appropriate permissions

def kaggle_download(dataset_links, download_path):
    """Download datasets from Kaggle."""
    setup_kaggle_api()  # Ensure API is set up before downloading
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

def descriptive_statistics(df):
    """Generate descriptive statistics for the dataset."""
    print("\nDescriptive Statistics:")
    print(df.describe())

def correlation_analysis(df):
    """Perform correlation analysis."""
    numeric_df = df.select_dtypes(include=[float, int])
    print("\nNumeric Columns for Correlation Matrix:", numeric_df.columns)
    
    print("\nCorrelation Matrix:")
    correlation_matrix = numeric_df.corr()
    print(correlation_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

def data_visualization(df):
    """Visualize data."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['crop'], kde=True)
    plt.title("Distribution of Crop Production")
    plt.xlabel("Crop Production")
    plt.ylabel("Frequency")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='rainfall', y='crop', data=df)
    plt.title("Crop Production vs Rainfall")
    plt.xlabel("Rainfall")
    plt.ylabel("Crop Production")
    plt.show()

def predictive_analysis(df):
    """Perform predictive analysis."""
    X = df[['rainfall']]
    y = df['crop']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nPredictive Analysis:")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    plt.figure(figsize=(10, 6))
    plt.scatter(X_test, y_test, color='blue', label='Actual')
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
    plt.title("Crop Production vs Rainfall - Regression Line")
    plt.xlabel("Rainfall")
    plt.ylabel("Crop Production")
    plt.legend()
    plt.show()

def main_advanced():
    data_dir = './data'
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

    # Load combined data from the SQLite database
    df_combined = load_combined_data(combined_db_path)

    if df_combined is not None:
        descriptive_statistics(df_combined)
        correlation_analysis(df_combined)
        data_visualization(df_combined)
        predictive_analysis(df_combined)
    else:
        print("Error: Failed to load combined dataset")

if __name__ == "__main__":
    main_advanced()
