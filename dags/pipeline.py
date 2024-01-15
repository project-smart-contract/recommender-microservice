from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.providers.mongo.hooks.mongo import MongoHook
import json
import csv
import os
from bson import json_util
from bson import ObjectId

default_args = {
    'owner': 'admin',
    'start_date': datetime(2023, 12, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    dag_id='recommendation_system_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2023, 12, 28),
    catchup=False
)
def recommendation_system_pipeline():
    @task()
    def fetch_new_data_from_mongo():
        try:
            hook = MongoHook(mongo_conn_id='mongo_default')
            client = hook.get_conn()
            user_data = client.Assurance.user_data
            print(f"Connected to MongoDB - {client.server_info()}")
            two_days_ago = datetime.utcnow() - timedelta(days=1)
            two_days_ago = two_days_ago.replace(microsecond=0)  # Remove microseconds for comparison
            two_days_ago_str = two_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            print(two_days_ago_str)
            new_data = user_data.find({"timestamp": {"$gte": two_days_ago_str}})
            print(new_data)
            # # Convert ObjectId to serializable format
            # new_data_list = json.loads(json_util.dumps(list(new_data)))

            # Convert ObjectId to serializable format
            new_data_list = []
            for document in new_data:
                # Convert ObjectId to str for the '_id' field
                document['_id'] = str(document['_id'])
                new_data_list.append(document)

            print(f"found {len(new_data_list)}")
            print(new_data_list)
            return new_data_list
        except Exception as e:
            print(f"Error connecting to MongoDB -- {e}")
            return None

    @task()
    def append_to_csv(data_list):
        try:
            csv_file_path = '/Users/aya/Desktop/ML/insurance-recommender/data/raw/user_data.csv'

            # If the data_list is not empty, write to the CSV file
            if data_list:
                with open(csv_file_path, 'a', newline='') as csvfile:  # option 'a' to append data to the end of csv
                    fieldnames = data_list[0].keys() if data_list else []
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    # Write the header -> to write the field names
                    # writer.writeheader()

                    # Write the data
                    writer.writerows(data_list)

                print("Data written to CSV file successfully.")
            else:
                print("No data to write to CSV file.")

        except Exception as e:
            print(f"Error writing data to CSV -- {e}")

    mongo_collection = fetch_new_data_from_mongo()

    # new_data_to_append = [
    #     {
    #         '_id': 'test_id_1',
    #         'fullname': 'Test User 1',
    #         'age': 30,
    #         'parent': True,
    #         'occupation': 'Engineer',
    #         'vehicle_year': 2022,
    #         'vehicle_age': 1,
    #         'car_make': 'Test Make',
    #         'car_model': 'Test Model',
    #         'car_type': 'Test Type',
    #         'number_insured_cars': 2,
    #         'business_size': 'Test Size',
    #         'business_field': 'Test Field',
    #         'timestamp': '2024-01-15T14:30:00.000Z'
    #     },
    # ]

    data = append_to_csv(mongo_collection)


summary = recommendation_system_pipeline()