import numpy as np
from src.ml.data.data_loader import load_raw_data
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


def preprocess_data(raw_data_path, processed_data_path):
    """
       Preprocess raw data for recommendation system.

       Parameters:
       - raw_data_path (string): Raw data path , processed_data_path (string): processed data path

       Returns:
       - tuple: Tuple containing preprocessed data (X_train, X_test).
       """

    raw_data = load_raw_data(raw_data_path)
    processed_data = raw_data

    processed_data["vehicle_year"].fillna(value=0, inplace=True)
    processed_data["number_insured_vehicles"].fillna(value=0, inplace=True)
    processed_data.fillna(value='unknown', inplace=True)

    # dropping these cols because we do not need it at this stage of code
    processed_data = processed_data.drop(['timestamp', 'fullname'], axis=1)

    economic_cars = ['dacia', 'renault', 'fiat', 'peugeot', 'ford', 'honda', 'hyundai', 'kia', 'nissan', 'subaru',
                     'toyota', 'volkswagen', 'cappuccino']
    midrange_cars = ['audi', 'bmw', 'mazda', 'mercedes', 'volvo', 'Nissan']
    luxury_cars = ['aston martin', 'bentley', 'ferrari', 'lamborghini', 'porsche', 'rolls-royce', 'tesla']

    # category
    hybrid_cars = ['Prius', 'Insight', 'Fusion Hybrid', 'Volt', 'RX Hybrid', 'Camry Hybrid', 'Ioniq Hybrid', 'Niro',
                   'i3', '3', 'chr']
    electric_cars = ['s', 'X', 'Y', 'Spark EV', 'i4', 'Kona Electric', 'Soul EV', 'e-tron']
    diesel_cars = ['500', 'logan', 'rs q4', 'Spark EV', 'i4', 'Kona Electric', 'Soul EV', 'e-tron', '50cc', 'lodge']

    # state
    vehicle_state = ['vetuste', 'recent']

    processed_data.loc[processed_data['vehicle_make'].isin(economic_cars), 'vehicle_range'] = 'Economic'
    processed_data.loc[processed_data['vehicle_make'].isin(midrange_cars), 'vehicle_range'] = 'Midrange'
    processed_data.loc[processed_data['vehicle_make'].isin(luxury_cars), 'vehicle_range'] = 'Luxury'
    processed_data.loc[processed_data['vehicle_make'].isin(['unknown']), 'vehicle_range'] = 'unknown'

    processed_data.loc[processed_data['vehicle_model'].isin(hybrid_cars), 'vehicle_category'] = 'Hybrid'
    processed_data.loc[processed_data['vehicle_model'].isin(electric_cars), 'vehicle_category'] = 'Electric'
    processed_data.loc[processed_data['vehicle_model'].isin(diesel_cars), 'vehicle_category'] = 'Diesel'
    processed_data.loc[processed_data['vehicle_model'].isin(['unknown']), 'vehicle_category'] = 'unknown'

    processed_data['vehicle_state'] = pd.cut(
        processed_data['vehicle_year'],
        bins=[1886, 2019, float('inf')],
        labels=['Vetuste', 'Recent']
    )
    processed_data = processed_data.drop(['vehicle_make', 'vehicle_model', 'vehicle_year'], axis=1)

    label_encoder = preprocessing.LabelEncoder()

    processed_data['occupation'] = label_encoder.fit_transform(processed_data['occupation'])
    processed_data['occupation'].unique()
    processed_data['parent'] = processed_data['parent'].map({True: 1, False: 0, 'unknown': 2})

    processed_data['www'] = processed_data['www'].map({True: 1, False: 0, 'unknown': 2})
    processed_data['vehicle_type'] = processed_data['vehicle_type'].map(
        {'motorcycle': 1, 'car': 2, 'truck': 3, 'bus': 4, 'boat': 5, 'unknown': 0})
    processed_data['vehicle_range'] = processed_data['vehicle_range'].map(
        {'Economic': 1, 'Midrange': 2, 'Luxury': 3, 'unknown': 0})
    processed_data['vehicle_category'] = processed_data['vehicle_category'].map(
        {'Diesel': 1, 'Electric': 2, 'Hybrid': 3, 'unknown': 0})
    processed_data['vehicle_state'] = processed_data['vehicle_state'].map({'Vetuste': 1, 'Recent': 2, np.NAN: 0})

    processed_data['business_field'] = label_encoder.fit_transform(processed_data['business_field'])
    processed_data['business_field'].unique()

    # Extract numeric data
    selected_columns = processed_data.iloc[:, 1:13]

    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(selected_columns)

    processed_data.iloc[:, 1:13] = scaled_data
    print(processed_data)

    # ///////////////////////
    numeric_columns = ['parent', 'age', 'occupation', 'www', 'vehicle_type', 'number_seats',
                       'business_field', 'number_insured_vehicles', 'vehicle_range', 'vehicle_category',
                       'vehicle_state']

    # Assuming processed_data is your DataFrame
    selected_columns = processed_data[numeric_columns]

    # Instantiate PCA with 3 components
    pca = PCA(n_components=3)

    # Fit and transform the selected columns
    pca_data = pca.fit_transform(selected_columns)

    # Create new DataFrame with PCA components
    pca_df = pd.DataFrame(data=pca_data, columns=['PCA1', 'PCA2', 'PCA3'])

    # Concatenate the original DataFrame excluding numeric_columns with the PCA DataFrame
    processed_data = pd.concat([processed_data.drop(columns=numeric_columns), pca_df], axis=1)

    return processed_data
