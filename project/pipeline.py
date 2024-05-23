import requests
import pandas as pd
import sqlite3
import os


data_urls = [
    'https://data.bs.ch/api/v2/catalog/datasets/100009/exports/csv',
    'https://data.bs.ch/api/v2/catalog/datasets/100082/exports/csv'
]


if not os.path.exists('data'):
    os.makedirs('data')


def download_and_clean_data(url):
    response = requests.get(url)
    file_name = url.split('/')[-1]
    file_path = os.path.join('data', file_name)

    
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    
    df = pd.read_csv(file_path)
    
    
    df.dropna(inplace=True)
    
    return df

cleaned_data_frames = []


for url in data_urls:
    df = download_and_clean_data(url)
    cleaned_data_frames.append(df)


combined_df = pd.concat(cleaned_data_frames)


conn = sqlite3.connect('data/cleaned_data.db')
combined_df.to_sql('cleaned_data', conn, if_exists='replace', index=False)
conn.close()

print("Data pipeline executed successfully and data is stored in /data/cleaned_data.db")
