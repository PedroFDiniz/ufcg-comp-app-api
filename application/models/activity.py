from application import MONGO_DB
import pymongo

class Activity:

    @staticmethod
    def register(owner_enroll: str, proof_doc: str, credits: str, period: str, type: str, description: str, status: str):
        """
        This function add a activity in the database
        -------------------------------------------
        owner_enroll: Id of the activity owner
        proof_doc: Is the document to comproove the time spend
        credits: Amount of hours that will be computed
        period: Period that the student participates 
        activity_type: Activity type
        activity_description: Activity description
        status: activity status (Created, Validated, Rejected)
        """

        try:
            activity = {
                'owner_enroll': owner_enroll,
                'proof_doc': proof_doc,
                'credits': credits,
                'period': period,
                'type': type,
                'description': description,
                'status': status,
            }
            
            MONGO_DB.activity.insert_one(activity)
        except ValueError as e:
            raise(e)

    @staticmethod
    def find(query: dict):
        activity = MONGO_DB.activity.find(query, {'_id': 0})
        return activity

    @staticmethod
    def find_one(query: dict):
        activity = MONGO_DB.activity.find_one(query, {'_id': 0})
        return activity

    @staticmethod
    def update(owner_enroll: str, description: str, update_fields:str):
        query = { "owner_enroll": owner_enroll, "description": description }
        update_doc = { "$set": update_fields }
        activity = MONGO_DB.activity.find_one_and_update(query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
        return activity

    @staticmethod
    def remove(owner_enroll: str, description: str):
        query = { "owner_enroll": owner_enroll, "description": description }
        MONGO_DB.activity.delete_one(query)

