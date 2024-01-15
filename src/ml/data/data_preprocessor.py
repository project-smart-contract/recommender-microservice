from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def preprocess_data(raw_data):
    """
    Preprocess raw data for recommendation system.

    Parameters:
    - raw_data (pd.DataFrame): Raw data DataFrame.

    Returns:
    - tuple: Tuple containing preprocessed data (X_train, X_test).
    """
    try:
        # Extract features and target variable
        features = raw_data.drop(columns=['target_variable'])
        target = raw_data['target_variable']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Optionally, perform additional preprocessing steps, such as scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        return X_train_scaled, X_test_scaled

    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return None, None
