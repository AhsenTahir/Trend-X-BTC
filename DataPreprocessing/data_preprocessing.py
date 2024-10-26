import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.exceptions import NotFittedError

def preprocess_data(df):
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
