from application.models.activity import Activity
from application.utils.validation import *
from application.utils.constants import ACTIVITY_STATUS_CREATED, ACTIVITY_STATUS_ASSIGNED, ACTIVITY_STATUS_VALIDATED
from bson.objectid import ObjectId


class Activity_Controller:
    def register(owner_email: str, doc_path: str, period: str, type: str, description: str):

        myAssert(owner_email, Exception("Owner email can't be empty.", 400))
        myAssert(doc_path, Exception("Document can't be empty.", 400))
        myAssert(period, Exception("Period can't be empty.", 400))
        myAssert(type, Exception("Type can't be empty.", 400))
        myAssert(description, Exception("Description can't be empty.", 400))

        activity = Activity.register(
            owner_email, doc_path, period, type, description, ACTIVITY_STATUS_CREATED)

        return activity

    def find(query: dict, page: str, size: str, sort: str, order: str):
        activities = list(Activity.find(query, page, size, sort, order))
        return activities

    def update(activity_id: str, update_fields: str):
        myAssert(activity_id, Exception("Activity id can't be empty.", 400))

        activity = Activity.find_one_by_id(activity_id)
        myAssert(activity, Exception(f"Activity not found.", 404))

        for field in update_fields:
            myAssert(field, Exception(f"${field} can't be empty.", 400))

        Activity.update(activity_id, update_fields)

    def assign(activity_id: str, reviewer: str):
        myAssert(activity_id, Exception("Activity id can't be empty.", 400))
        myAssert(reviewer, Exception("Reviewer id can't be empty.", 400))

        update_fields = {'reviewer': reviewer,
                         'status': ACTIVITY_STATUS_ASSIGNED}
        Activity.update(activity_id, update_fields)

    def count(query: dict):
        count = Activity.count(query)
        return count

    def compute_credits(owner_email: str):
        activities = list(Activity.find({
            "owner_email": owner_email,
            "status": ACTIVITY_STATUS_VALIDATED
        }, None, None, None, None))

        computed_credits = 0
        missing_credits = 22
        for activity in activities:
            computed_credits += int(activity['credits'])
            missing_credits -= int(activity['credits'])

        return {
            'computed_credits': computed_credits,
            'missing_credits': missing_credits
        }
