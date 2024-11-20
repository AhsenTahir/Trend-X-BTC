from firebase_admin import credentials, initialize_app, storage, db
import pandas as pd
import io
from datetime import datetime
import torch
import tempfile
import os

# Initialize Firebase Admin SDK with correct bucket name
cred = credentials.Certificate('firebase-credentials.json')

# Use the exact bucket name from Firebase Console
firebase_app = initialize_app(cred, {
    'storageBucket': 'trend-x-btc-c7d80.firebasestorage.app',  # Updated bucket name
    'databaseURL': 'https://trend-x-btc-c7d80-default-rtdb.firebaseio.com'
})

# Initialize storage bucket
try:
    bucket = storage.bucket()
    print(f"Successfully connected to Firebase Storage bucket")
except Exception as e:
    print(f"Error with storage bucket: {str(e)}")
    raise

# Initialize database
database = db.reference()

def save_df_to_firebase(df, filename):
    """Save DataFrame to Firebase Storage and Database"""
    try:
        # Save to Storage
        csv_content = df.to_csv(index=False)
        blob = bucket.blob(f"data/{filename}")
        blob.upload_from_string(csv_content, content_type='text/csv')
        print(f"Successfully saved {filename} to Firebase Storage")
        
        # Save metadata to Database
        db_ref = database.child('data').child(filename.replace('.csv', ''))
        db_ref.set({
            'last_updated': datetime.now().isoformat(),
            'rows': len(df),
            'columns': list(df.columns)
        })
        return True
    except Exception as e:
        print(f"Error saving to Firebase: {str(e)}")
        return False

def load_df_from_firebase(filename):
    """Load DataFrame from Firebase Storage"""
    try:
        blob = bucket.blob(f"data/{filename}")
        content = blob.download_as_string()
        return pd.read_csv(io.StringIO(content.decode('utf-8')))
    except Exception as e:
        print(f"Error loading from Firebase: {str(e)}")
        return None

def file_exists_in_firebase(filename):
    """Check if file exists in Firebase Storage"""
    blob = bucket.blob(f"data/{filename}")
    return blob.exists()

def save_model_to_firebase(model, model_name):
    """Save PyTorch model to Firebase"""
    try:
        # Create a temporary directory instead of a file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path for the temporary file
            temp_path = os.path.join(temp_dir, 'temp_model.pt')
            
            # Save the model to the temporary file
            torch.save(model.state_dict(), temp_path)
            
            # Upload to Firebase
            blob = bucket.blob(f"models/{model_name}")
            blob.upload_from_filename(temp_path)
            
            print(f"Successfully saved model {model_name} to Firebase Storage")
            
            # Save metadata to Database
            db_ref = database.child('models').child(model_name.replace('.pt', ''))
            db_ref.set({
                'last_updated': datetime.now().isoformat(),
                'architecture': model.__class__.__name__
            })
            return True
    except Exception as e:
        print(f"Error saving model to Firebase: {str(e)}")
        return False

def load_model_from_firebase(model_architecture, model_name):
    """Load PyTorch model from Firebase"""
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path for the temporary file
            temp_path = os.path.join(temp_dir, 'temp_model.pt')
            
            # Download the model
            blob = bucket.blob(f"models/{model_name}")
            blob.download_to_filename(temp_path)
            
            # Load the model
            model = model_architecture()
            model.load_state_dict(torch.load(temp_path))
            return model
    except Exception as e:
        print(f"Error loading model from Firebase: {str(e)}")
        return None

def model_exists_in_firebase(model_name):
    """Check if model exists in Firebase Storage"""
    blob = bucket.blob(f"models/{model_name}")
    return blob.exists() 