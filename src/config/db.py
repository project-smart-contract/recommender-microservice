# mongodb_connection.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def create_mongo_client():
    uri = "mongodb+srv://ayahamza:ayaado2003@cluster.vycctwf.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client


def ping_mongo_deployment(client):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!!")
    except Exception as e:
        print(e)
