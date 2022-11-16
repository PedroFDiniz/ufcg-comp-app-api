import threading
from typing import Union

from application import MONGO_DB
from pymongo import ReturnDocument

from application.utils.email import *
from application.utils.jwt import *

class User:
    @staticmethod
    def create(enroll: str, name: str, email: str, role: str, password: str):
        API_URL = "http://127.0.0.1:5000"

        email_confirmation_jwt = create_email_confirmation_jwt(email)
        email_confirmation_link = f"{API_URL}/user/{enroll}/confirm_email/{email_confirmation_jwt}"

        thread = threading.Thread(target=send_confirmation_email, args=(email, email_confirmation_link))
        thread.start()

        user = {
            'enroll': enroll,
            'name': name, 
            'email': email,
            'role': role,
            'password': password,
            'email_confirmed': False,
            'email_confirmation_jwt': email_confirmation_jwt
        }

        MONGO_DB.user.insert_one(user)

        return user

    @staticmethod
    def find(query: dict, _project_password=0):
        projection = {"password" : _project_password, '_id': 0}
        users = MONGO_DB.user.find(query, projection)
        return users

    @staticmethod
    def find_by_enroll(enroll: str, _project_password=0) -> Union[dict, None]:
        projection = {"password" : _project_password, '_id': 0}
        user = MONGO_DB.user.find_one({'enroll': enroll}, projection)
        return user

    @staticmethod
    def update(enroll: str, update_fields: str):
        query = { "enroll": enroll }
        update_doc = { "$set": update_fields }
        user = MONGO_DB.user.find_one_and_update(query,  update_doc, return_document=ReturnDocument.AFTER)
        return user

    @staticmethod
    def remove(enroll: str):
        query = { "enroll": enroll }
        MONGO_DB.user.delete_one(query)