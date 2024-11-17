import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.exceptions import NotFittedError
import numpy as np



def preprocess_data(df):
    if 'value' in df.columns:
        df.drop(columns=['value'], inplace=True)
    # Step 1: Define numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    # Ensure 'CPI' is included in numerical columns if present in DataFrame
    if 'CPI' in df.columns and 'CPI' not in numerical_cols:
        numerical_cols.append('CPI')
    
    # Define categorical columns and explicitly remove 'CPI' if present
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if 'CPI' in categorical_cols:
        categorical_cols.remove('CPI')

    # Step 2: Define transformations
    # Transformation pipeline for numerical columns
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Transformation pipeline for categorical columns, only if categorical columns exist
    if categorical_cols:
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
    else:
        categorical_transformer = 'passthrough'

    # Combine transformations into a preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols) if categorical_cols else ('cat', 'drop', [])
        ]
    )

    # Step 3: Fit and transform the data
    df_transformed = preprocessor.fit_transform(df)
    print(f"Transformed data shape: {df_transformed.shape}")

    # Step 4: Retrieve feature names after transformations if there are categorical features
    try:
        categorical_feature_names = (preprocessor.named_transformers_['cat']['onehot']
                                     .get_feature_names_out(categorical_cols).tolist()
                                     if categorical_cols else [])
    except NotFittedError:
        categorical_feature_names = []

    # Construct column names list
    transformed_column_names = numerical_cols + categorical_feature_names

    # Check the length of transformed columns and DataFrame columns
    print(f"Expected number of columns: {len(transformed_column_names)}")
    print(f"Transformed data shape: {df_transformed.shape}")

    # Ensure column count matches transformed data shape
    if df_transformed.shape[1] != len(transformed_column_names):
        raise ValueError(f"Column mismatch: transformed data has {df_transformed.shape[1]} columns, but {len(transformed_column_names)} column names provided.")
    
    # Step 5: Create a DataFrame with transformed data
    df_preprocessed = pd.DataFrame(df_transformed, columns=transformed_column_names)
    
    # Step 6: Handle 'Close' column
    # If 'Close' is in the original DataFrame, add it back to the transformed data
    if 'Close' in df.columns:
        df_preprocessed['Close'] = df['Close'].values  # Add the unscaled 'Close' column

    # Step 7: Check shape and column alignment for debugging
    print("Final shape of preprocessed data:", df_preprocessed.shape)
  
    # Step 8: Return preprocessed DataFrame and scaler for future use
    return df_preprocessed, preprocessor.named_transformers_['num'].named_steps['scaler']

def add_gaussian_noise(df, columns_to_augment, noise_fraction=0.02):
    """
    Adds Gaussian noise to specified numerical columns in the DataFrame.

    Parameters:
    - df: The input DataFrame.
    - columns_to_augment: List of column names to which noise will be added.
    - noise_fraction: Fraction of the mean to determine the standard deviation of the noise.

    Returns:
    - DataFrame with added Gaussian noise in specified columns.
    """
    df_augmented = df.copy()  # Create a copy to avoid modifying the original DataFrame
    print("debugging 1")
    count=0
    for column in columns_to_augment:
        if column in df_augmented.columns:
            mean = df_augmented[column].mean()
            print(f"debugging 2 mean: {mean}")
            std_dev = noise_fraction * mean  # Calculate standard deviation as a fraction of the mean
            print(f"debugging 3 std_dev: {std_dev}")
            noise = np.random.normal(0, std_dev, size=df_augmented[column].shape)  # Generate Gaussian noise
            print(f"debugging 4 noise: {noise}")
            df_augmented[column] += noise  # Add noise to the column
            print(type(df_augmented[column]))
            count+=1
            print(f"debugging 5 count: {count} column: {column}")

    return df_augmented




def data_augmentation(data):
    # Example usage
    print("Data augmentation")
    columns_to_augment = [
        'Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume',
        'Taker buy base asset volume', 'Taker buy quote asset volume',
        'RSI', 'Inflation Rate', 'avg_block_size',
        'num_transactions', 'miners_revenue'
    ]
    print("Data before augmentation")
    # Assuming 'data' is your original DataFrame
    data.head()
    print("Data after augmentation")
    data_augmented = add_gaussian_noise(data, columns_to_augment)
    data_augmented.head()
    return data_augmented
