from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from application.utils.constants import DB_NAME, MONGO_SERVER_URI

app = Flask(__name__)
MONGO_CLIENT = MongoClient(MONGO_SERVER_URI)
MONGO_DB = MONGO_CLIENT[DB_NAME]

try:
    MONGO_CLIENT.admin.command('ping')
    print("Server available")
except ConnectionFailure:
    print("Server not available")

from application import router
