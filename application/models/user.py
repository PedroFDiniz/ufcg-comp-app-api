import threading
from typing import Union

from application import MONGO_DB
from pymongo import ReturnDocument

from application.utils.email import *

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
    def get_all():
        results = MONGO_DB.user.find({})
        users_list = list(results)
        return users_list

    @staticmethod
    def find(enroll: str) -> Union[dict, None]:
        user = MONGO_DB.user.find_one({'enroll': enroll})
        return user

    @staticmethod
    def update(enroll, update_fields):
        query = { "enroll": enroll }
        update_doc = { "$set": update_fields }
        user = MONGO_DB.user.find_one_and_update(query,  update_doc, return_document=ReturnDocument.AFTER)
        return user

        # @staticmethod
        # def delete_user(username:str):
        #     query = {"username": username}
        #     projection = {"password" : 0}
        #     user = DB.user.find_one(query, projection)
        #     DB.user.delete_one({"username": username})
        #     return user

        # @staticmethod
        # def update_user(username:str, update_fields:dict):
        #     query = { "username": username }
        #     update_doc = { "$set": update_fields }
        #     return DB.user.find_one_and_update(query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
