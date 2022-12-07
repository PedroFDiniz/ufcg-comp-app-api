from application.models.activity import Activity
from application.utils.validation import *
from application.utils.constants import ACTIVITY_STATUS_CREATED, ACTIVITY_STATUS_ASSIGNED
from bson.objectid import ObjectId

class Activity_Controller:
    def register(owner_email: str, owner_enroll: str, doc_path: str, period:str, type:str, description:str):

        myAssert(owner_email, Exception("Owner email can't be empty.", 400))
        myAssert(owner_enroll, Exception("Owner enroll can't be empty.", 400))
        myAssert(doc_path, Exception("Document can't be empty.", 400))
        myAssert(period, Exception("Period can't be empty.", 400))
        myAssert(type, Exception("Type can't be empty.", 400))
        myAssert(description, Exception("Description can't be empty.", 400))

        activity = Activity.register(owner_email, owner_enroll, doc_path, period, type, description, ACTIVITY_STATUS_CREATED)

        return activity

    def find(query: dict, page: str, size: str, sort: str, order:str):
        activity = list(Activity.find(query, page, size, sort, order))
        return activity

    def update(activity_id: str, update_fields: str):
        myAssert(activity_id, Exception("Activity id can't be empty.", 400))        

        activity = Activity.find_one_by_id(activity_id)
        myAssert(activity, Exception(f"Activity not found.", 404))

        for field in update_fields:
           myAssert(field, Exception(f"${field} can't be empty.", 400))        

        Activity.update(activity_id, update_fields)

    def assign (activity_id: str, reviewer: str):
        myAssert(activity_id, Exception("Activity id can't be empty.", 400))        
        myAssert(reviewer, Exception("Reviewer id can't be empty.", 400))        

        update_fields = {'reviewer': reviewer, 'status': ACTIVITY_STATUS_ASSIGNED}
        Activity.update(activity_id, update_fields)

    def remove(activity_id: str, description: str):
        myAssert(activity_id, Exception("Activity id can't be empty.", 400))        

        activity = Activity.find_one_by_id(activity_id)
        myAssert(activity, Exception(f"Activity not found.", 404))
        myAssert(activity, Exception(f"Activity not found.", 404))

        Activity.remove(activity_id)

    def count():
        count = Activity.count()
        return count

