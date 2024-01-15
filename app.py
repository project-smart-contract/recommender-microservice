# app.py
from flask import Flask, request, jsonify
from src.config.db import create_mongo_client, ping_mongo_deployment

app = Flask(__name__)

# connection to db
mongo_client = create_mongo_client()
ping_mongo_deployment(mongo_client)


# Define the user_data collection
users_collection = mongo_client.Assurance.user_data


@app.route('/post_user', methods=['POST'])
def post_user():
    try:
        data = request.json

        # Insert the user data into the MongoDB collection
        user_id = users_collection.insert_one(data).inserted_id

        return jsonify({'message': f'User added with ID: {user_id}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

"""{
  "type": "personal",
  "user_info": {
    "fullname": "Kamilia Hamza",
    "age": 22,
    "parent": false,
    "occupation": "doctor",
    "vehicle_year":"2017",
    "vehicle_age": 3,
    "car_make": "toyota",
    "car_model": "chr",
    "car_type": null,
    "number_insured_cars": null,
    "business_size":null,
    "business_field": null
  },
  "timestamp": "{{__ISO8601}}"
}"""