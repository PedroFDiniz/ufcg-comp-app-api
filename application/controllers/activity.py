from application.utils.validation import *
from application.models.activity import Activity
from application.utils.constants import ACTIVITY_STATUS_CREATED, ACTIVITY_STATUS_ASSIGNED, ACTIVITY_STATUS_VALIDATED
from werkzeug.datastructures import FileStorage


class Activity_Controller:
    def register(owner_email: str, voucher: FileStorage, period: str, kind: str, description: str):
        myAssert(owner_email, AssertionError("Owner email can't be empty.", 400))
        myAssert(voucher, AssertionError("Document can't be empty.", 400))
        myAssert(period, AssertionError("Period can't be empty.", 400))
        myAssert(kind, AssertionError("Type can't be empty.", 400))
        myAssert(description, AssertionError("Description can't be empty.", 400))

        activity = Activity.register(
            owner_email, voucher, period, kind, description, ACTIVITY_STATUS_CREATED)

        return activity

    def find(query: dict, page: str, size: str, sort: str, order: str):
        activities = list(Activity.find(query, page, size, sort, order))
        return activities

    def update(activity_id: str, update_fields: str):
        myAssert(activity_id, AssertionError("Activity id can't be empty.", 400))

        activity = Activity.find_one_by_id(activity_id)
        myAssert(activity, AssertionError(f"Activity not found.", 404))

        for field in update_fields:
            myAssert(field, AssertionError(f"${field} can't be empty.", 400))

        Activity.update(activity_id, update_fields)

    def assign(activity_id: str, reviewer: str):
        myAssert(activity_id, AssertionError("Activity id can't be empty.", 400))
        myAssert(reviewer, AssertionError("Reviewer id can't be empty.", 400))

        update_fields = {'reviewer': reviewer,
                         'status': ACTIVITY_STATUS_ASSIGNED}
        Activity.update(activity_id, update_fields)

    def count(query: dict):
        count = Activity.count(query)
        return count

    def compute_credits(owner_email: str):
        myAssert(owner_email, AssertionError("Owner email can't be empty.", 400))

        activities = list(Activity.find({
            "owner_email": owner_email,
            "status": ACTIVITY_STATUS_VALIDATED
        }, None, None, None, None))

        computed_credits = 0
        missing_credits = 22
        for activity in activities:
            computed_credits += int(activity['credits'])
        
        if computed_credits > missing_credits:
            missing_credits = 0
        else:
            missing_credits -= computed_credits

        return {
            'computed_credits': computed_credits,
            'missing_credits': missing_credits
        }

    def generate_process(owner_email: str, owner_name: str, owner_enroll: str):
        myAssert(owner_email, AssertionError("Owner email can't be empty.", 400))
        myAssert(owner_name, AssertionError("Owner name can't be empty.", 400))
        myAssert(owner_enroll, AssertionError("Owner enroll can't be empty.", 400))

        activities = list(Activity.find({
            "owner_email": owner_email,
            "status": ACTIVITY_STATUS_VALIDATED
        }, None, None, None, None))

        data, voucher_paths, reviewers = Activity.get_process_data(activities)
        Activity.generate_table_of_contents(owner_email, owner_name, owner_enroll, data)

        process_path = Activity.merge_vouchers(owner_email, voucher_paths)
        return Activity.generate_final_process(process_path, reviewers)
