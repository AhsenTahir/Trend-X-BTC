import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_cleaning.data_cleaning import data_cleaning
from data.DataGenerator import Data_Generator

Raw_Data=Data_Generator()
print("Raw Data head")
print(Raw_Data.head())
print("Raw Data info")
print(Raw_Data.info())
print("Raw Data describe")
print(Raw_Data.describe())
data=data_cleaning(Raw_Data)
print("Data head")
print(data.head())
print("Data info")
print(data.info())
print("Data describe")
print(data.describe())
