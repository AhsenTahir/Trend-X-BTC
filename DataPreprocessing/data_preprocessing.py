import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def preprocess_data(df):
     # Define numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    # Ensure 'CPI' is included in numerical columns it was making it a categorical column
    if 'CPI' not in numerical_cols:
        numerical_cols.append('CPI')
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    # Define preprocessing for numerical columns
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Define preprocessing for categorical columns
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # Step 3: Fit and transform the data
    df_preprocessed = preprocessor.fit_transform(df)

    # Step 4: Print the shape of the preprocessed data
    print("Shape of preprocessed data:", df_preprocessed.shape)

    # Convert the result back to a DataFrame

    categorical_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols).tolist()


    # Step 5: Print the number of columns expected in the final DataFrame
    print("Expected number of columns:", len(numerical_cols) + len(categorical_feature_names))

    # Create the DataFrame
    df_preprocessed = pd.DataFrame(df_preprocessed, columns=numerical_cols + categorical_feature_names)
    
    # Extract the scaler from the preprocessing pipeline
    scaler = preprocessor.named_transformers_['num'].named_steps['scaler']
    
    # Remove 'Close' from numerical columns
    close_column = 'Close'
    numerical_cols.remove(close_column)
    
    # Add the unscaled 'Close' column back to the preprocessed data
    df_preprocessed[close_column] = df[close_column]
    
    return df_preprocessed, scaler
