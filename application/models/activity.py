from application import MONGO_DB
from bson.objectid import ObjectId
import pymongo
import datetime

DEFAULT_PROJECTION_FIELDS = {
    '_id': {"$toString": "$_id"},
    'owner_email': 1,
    'owner_enroll': 1,
    'credits': 1,
    'period': 1,
    'type': 1,
    'description': 1,
    'status': 1,
    'reviewer': 1,
    'createdTime': 1,
    'updatedTime': 1,
    'proof_doc': 1
}


class Activity:

    @staticmethod
    def register(owner_email: str, owner_enroll: str, proof_doc: str, period: str, type: str, description: str, status: str):
        """
        This function add a activity in the database
        -------------------------------------------
        owner_enroll: Id of the activity owner
        proof_doc: Is the document to comproove the time spend
        credits: Amount of hours that will be computed
        period: Period that the student participates
        activity_type: Activity type
        activity_description: Activity description
        status: activity status (Created, Assigned, Validated, Rejected)
        """

        try:
            activity = {
                'owner_enroll': owner_enroll,
                'owner_email': owner_email,
                'description': description,
                'proof_doc': proof_doc,
                'period': period,
                'status': status,
                'type': type,
                'justify': None,
                'credits': None,
                'reviewer': None,
                'createdTime': datetime.datetime.utcnow(),
                'updatedTime': datetime.datetime.utcnow(),
            }

            MONGO_DB.activity.insert_one(activity)
        except ValueError as e:
            raise (e)

    @staticmethod
    def find(query: dict, page: int, size: int, sort: str, order: str):
        projection = DEFAULT_PROJECTION_FIELDS
        direction = pymongo.ASCENDING if order == 'asc' else pymongo.DESCENDING
        activity = MONGO_DB.activity.find(query, projection).sort(
            sort, direction).limit(size).skip(page * size)
        return activity

    @staticmethod
    def find_one(query: dict):
        projection = DEFAULT_PROJECTION_FIELDS
        activity = MONGO_DB.activity.find_one(query, projection)
        return activity

    @staticmethod
    def find_one_by_id(activity_id: str):
        projection = DEFAULT_PROJECTION_FIELDS
        activity = MONGO_DB.activity.find_one({'_id': ObjectId(activity_id)}, projection)
        return activity

    @staticmethod
    def update(activity_id: str, update_fields: str):
        query = {'_id': ObjectId(activity_id)}
        update_doc = {"$set": update_fields}
        activity = MONGO_DB.activity.find_one_and_update(query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
        return activity

    @staticmethod
    def count(query: dict):
        return MONGO_DB.activity.count_documents(query)
