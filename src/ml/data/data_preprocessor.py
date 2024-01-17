import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from src.ml.data.data_loader import load_raw_data
from sklearn import preprocessing


def clean_and_transform_data(raw_data):

    processed_data = raw_data.fillna(value='unknown')

    processed_data['timestamp'] = pd.to_datetime(processed_data['timestamp'])

    return processed_data


def save_processed_data(processed_data, processed_data_path):
    # Implement your logic to save processed data to a file
    # This function should take processed data and a file path as input
    # For example, if using pandas to save a DataFrame to CSV:
    processed_data.to_csv(processed_data_path, index=False)


def preprocess_data(raw_data_path, processed_data_path):
    """
    Preprocess raw data for recommendation system.

    Parameters:
    - raw_data (pd.DataFrame): Raw data DataFrame.

    Returns:
    - tuple: Tuple containing preprocessed data (X_train, X_test).
    """
    # load data
    raw_data = load_raw_data(raw_data_path)

    # Clean and transform data
    processed_data = clean_and_transform_data(raw_data)

    # Save processed data
    save_processed_data(processed_data, processed_data_path)

