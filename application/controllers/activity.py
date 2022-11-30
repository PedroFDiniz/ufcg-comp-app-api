from application.models.activity import Activity
from application.utils.validation import *
from application.utils.constants import ACTIVITY_STATUS_CREATED, ACTIVITY_STATUS_VALIDATED, ACTIVITY_STATUS_FINISHED

class Activity_Controller:
    def register(owner_email: str, owner_enroll: str, proof_doc: str, credits: str, period:str, type:str, description:str):

        myAssert(owner_email, Exception("Owner email can't be empty.", 400))
        myAssert(owner_enroll, Exception("Owner enroll can't be empty.", 400))
        myAssert(proof_doc, Exception("Document can't be empty.", 400))
        myAssert(period, Exception("Period can't be empty.", 400))
        myAssert(type, Exception("Type can't be empty.", 400))
        myAssert(description, Exception("Description can't be empty.", 400))
        myAssert(credits, Exception("Hours can't be empty.", 400))

        activity = Activity.register(owner_email, owner_enroll, proof_doc, credits, period, type, description, ACTIVITY_STATUS_CREATED)

        return activity

    def find(query: dict, page: str, size: str, sort: str, order:str):
        activity = list(Activity.find(query, page, size, sort, order))
        return activity

    def update(owner_enroll: str, description: str, update_fields: str):
        myAssert(owner_enroll, Exception("Owner enroll can't be empty.", 400))        
        myAssert(description, Exception("Owner enroll can't be empty.", 400))        

        activity = Activity.find_one({ "owner_enroll": owner_enroll, "description": description})
        myAssert(activity, Exception(f"Activity not found.", 404))

        for field in update_fields:
          myAssert(field, Exception(f"${field} can't be empty.", 400))        

        Activity.update(owner_enroll, description, update_fields)

    def remove(owner_enroll: str, description: str):
        myAssert(owner_enroll, Exception("Owner enroll can't be empty.", 400))        
        myAssert(description, Exception("Owner enroll can't be empty.", 400))       

        activity = Activity.find_one({ "owner_enroll": owner_enroll, "description": description})
        myAssert(activity, Exception(f"Activity not found.", 404))

        Activity.remove(owner_enroll, description)
