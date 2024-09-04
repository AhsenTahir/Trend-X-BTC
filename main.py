import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from data.DataGenerator import Data_Generator

data=Data_Generator()
print(data.describe())
