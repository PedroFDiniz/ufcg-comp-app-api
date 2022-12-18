from application import MONGO_DB
import datetime

DEFAULT_PROJECTION_FIELDS = {
    '_id': {"$toString": "$_id"},
    'enroll': 1,
    'name': 1, 
    'email': 1,
    'role': 1,
    'createdTime': 1,
    'updatedTime': 1,
}


class User:
    @staticmethod
    def create(enroll: str, name: str, email: str, role: str):
        user = {
            'enroll': enroll,
            'name': name, 
            'email': email,
            'role': role,
            'createdTime': datetime.datetime.utcnow(),
            'updatedTime': datetime.datetime.utcnow(),
        }

        MONGO_DB.user.insert_one(user)

        return user

    @staticmethod
    def find(query: dict):
        projection = DEFAULT_PROJECTION_FIELDS
        users = MONGO_DB.user.find(query, projection)
        return users

    @staticmethod
    def find_by_enroll(enroll: str):
        projection = DEFAULT_PROJECTION_FIELDS
        user = MONGO_DB.user.find_one({'enroll': enroll}, projection)
        return user
