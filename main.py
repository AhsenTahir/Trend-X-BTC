import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_cleaning.data_cleaning import data_cleaning
from data_generator.DataGenerator import Data_Generator
from config import GENERATE_NEW_DATA 
from DataPreprocessing.data_preprocessing import preprocess_data

# Define the path to your Excel file
excel_file_path = 'Stored_data/cleaned_data.xlsx'

if GENERATE_NEW_DATA:
    # Generate new data
    Raw_Data = Data_Generator()
    print("Raw Data head")
    print(Raw_Data.head())
    print("Raw Data info")
    print(Raw_Data.info())
    print("Raw Data describe")
    print(Raw_Data.describe())

    # Clean the generated data
    data = data_cleaning(Raw_Data)
    print("Data head")
    print(data.head())
    print("Data info")
    print(data.info())
    print("Data describe")
    print(data.describe())

    # Save the cleaned data to an Excel sheet, overwriting the existing file
    data.to_excel(excel_file_path, index=False)
    print(f"Cleaned data saved to {excel_file_path}")

else:
    # Use the existing data from the Excel file
    data = pd.read_excel(excel_file_path)
    print("Loaded data from existing Excel file")
    print("Data head")
    print(data.head())
    print("Data info")
    print(data.info())
    print("Data describe")
    print(data.describe())

##data preprocessing
data = preprocess_data(data)
print("Data head")
print(data.head())
print("Data info")
print(data.info())
print("Data describe")
print(data.describe())

# Save preprocessed data to a new Excel file
preprocessed_excel_file_path = 'Stored_data/preprocessed_data.xlsx'
data.to_excel(preprocessed_excel_file_path, index=False)
print(f"Preprocessed data saved to {preprocessed_excel_file_path}")