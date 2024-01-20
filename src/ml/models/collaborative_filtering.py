import numpy as np
import pandas as pd

from src.ml.data.data_loader import load_raw_data


def collaborative_filtering(cluster_assignment):
    print(cluster_assignment)

    processed_user_data = load_raw_data(
        "/Users/aya/Desktop/ML/insurance-recommender/data/processed/users_clusters.csv")
    contract_record = load_raw_data("/Users/aya/Desktop/ML/insurance-recommender/data/raw/contract_record.csv")
    # print(processed_user_data.head())

    # print(processed_user_data.dtypes)
    # print(processed_user_data['cluster'].unique())

    user_cluster_mapping = dict(zip(processed_user_data['_id'], processed_user_data['cluster']))
    # print("hello ==========", user_cluster_mapping)

    # get only similar users _ids
    target_cluster_users = processed_user_data[processed_user_data['cluster'] == cluster_assignment]['_id'].tolist()
    # print("hello ==========", target_cluster_users)

    # pick only the records of similar users
    filtered_contract_record = contract_record[contract_record['user_id'].isin(target_cluster_users)]

    # construct the matrix
    user_item_matrix = pd.pivot_table(filtered_contract_record, values='rating', index='user_id',
                                      columns='insurance_policy_id', fill_value=0)

    # calculating the mean rating of each insurance policy
    average_ratings = np.mean(user_item_matrix, axis=0)
    # picking top 3 ratings
    top3_recommendations = average_ratings.sort_values(ascending=False).head(3).index

    return top3_recommendations.tolist()
