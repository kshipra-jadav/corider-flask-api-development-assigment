import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

HOST = os.getenv("MONGODB_HOST")
PORT = int(os.getenv("MONGODB_PORT"))
USERNAME = os.getenv("MONGODB_USERNAME")
PASSWORD = os.getenv("MONGODB_PASSWORD")


def get_mongo_client(db=None, collection=None):
    if db is not None and collection is not None:
        client = MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, authSource="admin")
        database = client[db]
        coll = database[collection]
        return coll
    return MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, authSource="admin")
