import joblib
import pandas as pd
from sklearn.cluster import KMeans

from src.ml.data.data_loader import load_raw_data
from src.ml.data.data_preprocessor import preprocess_datapoint


def kmeans_clustering():
    processed_data_path = '/Users/aya/Desktop/ML/insurance-recommender/data/processed/processed_user_data.csv'
    processed_user_data = load_raw_data(processed_data_path)
    features_for_clustering = processed_user_data[['PCA1', 'PCA2', 'PCA3']]
    kmeans = KMeans(n_clusters=9)
    processed_user_data['cluster'] = kmeans.fit_predict(features_for_clustering)
    # saving cluster assignments
    processed_user_data.to_csv('/Users/aya/Desktop/ML/insurance-recommender/data/processed/users_clusters.csv',
                               index=False)

    model_save_path = '/Users/aya/Desktop/ML/insurance-recommender/src/ml/models/kmeans_model.joblib'

    # Save the model using joblib
    joblib.dump(kmeans, model_save_path)


def load_kmeans_model(model_path):
    # Load the K-Means model from the specified path
    kmeans_model = joblib.load(model_path)
    return kmeans_model


def perform_clustering(user_data):
    # converting it to csv
    user_df = pd.DataFrame([user_data])
    # print(user_df)
    user_preprocessed_data = preprocess_datapoint(user_df)
    print(user_preprocessed_data)
    # Loading  pre-trained K-Means model
    kmeans_model_path = '/Users/aya/Desktop/ML/insurance-recommender/src/ml/models/kmeans_model.joblib'
    kmeans_model = load_kmeans_model(kmeans_model_path)

    # Perform clustering on the user's features
    cluster_assignment = kmeans_model.predict(user_preprocessed_data)
    return int(cluster_assignment[0])  # Returning as an integer for simplicity
