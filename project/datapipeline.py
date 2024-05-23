import os
os.environ['KAGGLE_USERNAME'] = 'rahulnitinramraje' 
os.environ['KAGGLE_KEY'] = '95c8b238b744776bca6406ac38aad804' 

import kaggle
import time

dataset_links = ["https://www.kaggle.com/datasets/thedevastator/the-relationship-between-crop-production-and-cli",
                 "https://www.kaggle.com/datasets/swapnilbhange/average-temperature-of-cities",
                 ]

for dataset in dataset_links:
    folder_name = f"../data/{'-'.join(dataset.split('/')[-2:])}"
    dataset = '/'.join(dataset.split('/')[-2:])

    print(f'Creating folder at {folder_name}')
    os.mkdir(folder_name)

    print(f'Downloading the {dataset} dataset')

    kaggle.api.dataset_download_files(dataset, path=folder_name, unzip=True)
    time.sleep(1)

print('Done')
