from application import MONGO_DB
import pymongo, datetime

class Activity:

    @staticmethod
    def register(owner_email:str, owner_enroll: str, proof_doc: str, credits: str, period: str, type: str, description: str, status: str):
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
                'owner_email': owner_email,
                'owner_enroll': owner_enroll,
                'proof_doc': proof_doc,
                'credits': credits,
                'period': period,
                'type': type,
                'description': description,
                'status': status,
                'reviewer': None,
                'createdTime': datetime.datetime.utcnow(),
                'updatedTime': datetime.datetime.utcnow(),
            }
            
            MONGO_DB.activity.insert_one(activity)
        except ValueError as e:
            raise(e)

    @staticmethod
    def find(query: dict, page: int, size: int, sort:str, order:str):
        projection =  {'_id': 0, 'proof_doc': 0}
        direction = pymongo.ASCENDING if order == 'asc' else pymongo.DESCENDING
        activity = MONGO_DB.activity.find(query, projection).sort(sort, direction).limit(size).skip(page * page)
        return activity

    @staticmethod
    def find_one(query: dict):
        projection =  {'_id': 0}
        activity = MONGO_DB.activity.find_one(query, projection)
        return activity

    @staticmethod
    def update(owner_enroll: str, description: str, update_fields:str):
        query = { "owner_enroll": owner_enroll, "description": description, 'updatedTime': datetime.datetime.utcnow() }
        update_doc = { "$set": update_fields }
        activity = MONGO_DB.activity.find_one_and_update(query, update_doc, return_document=pymongo.ReturnDocument.AFTER)
        return activity

    @staticmethod
    def remove(owner_enroll: str, description: str):
        query = { "owner_enroll": owner_enroll, "description": description }
        MONGO_DB.activity.delete_one(query)

