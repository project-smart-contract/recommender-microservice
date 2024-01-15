import pandas as pd


def load_raw_data(file_path):
    """
    Load raw data from a CSV file.

    Parameters:
    - file_path (str): Path to the raw data file.

    Returns:
    - pd.DataFrame: DataFrame containing the raw data.
    """
    try:
        # Load data from CSV file
        raw_data = pd.read_csv(file_path)

        # Optionally, perform any initial data cleaning or preprocessing here

        return raw_data

    except Exception as e:
        print(f"Error loading raw data: {e}")
        return None
