# app.py
import json
from flask import Flask, request, jsonify
import yaml
from kafka import KafkaProducer
from src.config.db import create_mongo_client, ping_mongo_deployment
from src.ml.models.clustering import perform_clustering
from src.ml.models.collaborative_filtering import collaborative_filtering
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# def load_kafka_config():
#     with open('/Users/aya/Desktop/ML/insurance-recommender/config/kafka_config.yaml', 'r') as config_file:
#         kafka_configuration = yaml.safe_load(config_file)
#     return kafka_configuration
#
#
# kafka_config = load_kafka_config()
# bootstrap_servers = kafka_config['kafka']['bootstrap_servers']
# topic = kafka_config['kafka']['topic']
#
# producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# connection to db
mongo_client = create_mongo_client()
ping_mongo_deployment(mongo_client)

# Define the user_data collection
users_collection = mongo_client.Assurance.user_data
insurance_policies_collection = mongo_client.Assurance.insurance_policies
contract_record_collection = mongo_client.Assurance.contract_record


# Endpoint for receiving user data, performing clustering, collaborative filtering, and returning recommendations
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    try:
        user_data = request.get_json()
        print(user_data)
        user_id = str(users_collection.insert_one(user_data).inserted_id)

        # Perform clustering
        cluster_assignment = perform_clustering(user_data)
        print("~~~~~~~~~~~~~~~~~~~~~~~",cluster_assignment)
        # Generate user-item matrix and collaborative filtering recommendations
        recommendations = collaborative_filtering(cluster_assignment)
        print("~~~~~~~~~~~~~~~~~~~~~~~",recommendations)
        # producer.send('recommendation_topic', json.dumps(recommendations).encode('utf-8'))

        return jsonify({
            'success': True,
            'cluster assignment': cluster_assignment,
            'recommendations': recommendations,
            'message': f'User added with ID: {user_id}'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/post_user', methods=['POST'])
def post_user():
    try:
        data = request.json

        # Insert the user data into the MongoDB collection
        user_id = users_collection.insert_one(data).inserted_id

        return jsonify({'message': f'User added with ID: {user_id}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/post_insurance_policy', methods=['POST'])
def post_insurance_policy():
    try:
        data = request.json

        # Insert the user data into the MongoDB collection
        insurance_policy_id = insurance_policies_collection.insert_one(data).inserted_id

        return jsonify({'message': f'Insurance policy added with ID: {insurance_policy_id}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/post_contract_record', methods=['POST'])
def post_contract_record():
    try:
        data = request.json

        # Insert the user data into the MongoDB collection
        contract_record_id = contract_record_collection.insert_one(data).inserted_id

        return jsonify({'message': f'Insurance policy added with ID: {contract_record_id}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
