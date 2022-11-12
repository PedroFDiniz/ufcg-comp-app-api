from application.models.activty import Activity
from application.utils.validation import *
from application.utils.constants import ACTIVITY_STATUS_CREATED, ACTIVITY_STATUS_VALIDATED, ACTIVITY_STATUS_FINISHED

class Activity_Controller:
    def register(owner_enroll: str, proof_doc: str, credits: str, period:str, type:str, description:str):
        assert owner_enroll, "Owner enroll can't be empty."
        assert proof_doc, "Document can't be empty."
        assert period, "Period can't be empty."
        assert type, "Type can't be empty."
        assert description, "Description can't be empty."
        assert credits, "Hours can't be empty."

        myAssert(owner_enroll, Exception("Owner enroll can't be empty.", 400))
        myAssert(proof_doc, Exception("Document can't be empty.", 400))
        myAssert(period, Exception("Period can't be empty.", 400))
        myAssert(type, Exception("Type can't be empty.", 400))
        myAssert(description, Exception("Description can't be empty.", 400))
        myAssert(credits, Exception("Hours can't be empty.", 400))

        activity = Activity.register(owner_enroll, proof_doc, credits, period, type, description, ACTIVITY_STATUS_CREATED)

        return activity

    def find(query: dict):
        activity = Activity.find(query)
        return activity

