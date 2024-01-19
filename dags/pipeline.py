import csv
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook

from src.ml.data.data_preprocessor import preprocess_data

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
    def fetch_new_data_from_mongo(collection_name):
        try:
            hook = MongoHook(mongo_conn_id='mongo_default')
            client = hook.get_conn()
            user_data = client.Assurance[collection_name]
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
    def append_to_csv(data_list, path):
        try:
            csv_file_path = path

            # If the data_list is not empty, write to the CSV file
            if data_list:
                with open(csv_file_path, 'a', newline='') as csvfile:  # option 'a' to append data to the end of csv
                    fieldnames = data_list[0].keys() if data_list else []
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    # Write the header -> to write the field names
                    # if csvfile.tell() == 0:
                    # writer.writeheader()

                    # Write the data
                    writer.writerows(data_list)

                print("Data written to CSV file successfully.")
            else:
                print("No data to write to CSV file.")

        except Exception as e:
            print(f"Error writing data to CSV -- {e}")

    # user_data_collection = fetch_new_data_from_mongo("user_data")
    # data = append_to_csv(user_data_collection, '/Users/aya/Desktop/ML/insurance-recommender/data/raw/user_data.csv')

    # insurance_data_collection = fetch_new_data_from_mongo("insurance_policies")
    # data = append_to_csv(insurance_data_collection,
    #                      '/Users/aya/Desktop/ML/insurance-recommender/data/raw/insurance_policies.csv')
    #
    # contract_data_collection = fetch_new_data_from_mongo("contract_record")
    # data = append_to_csv(contract_data_collection,
    #                      '/Users/aya/Desktop/ML/insurance-recommender/data/raw/contract_record.csv')

    @task()
    def process_data():
        preprocess_data('/Users/aya/Desktop/ML/insurance-recommender/data/raw/user_data.csv',
                        '/Users/aya/Desktop/ML/insurance-recommender/data/processed/processed_user_data.csv')

    process_data()


summary = recommendation_system_pipeline()
