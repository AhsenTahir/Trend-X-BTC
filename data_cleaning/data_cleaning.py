import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def data_cleaning(data):
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    return data