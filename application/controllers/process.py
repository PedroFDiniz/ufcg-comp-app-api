from application.models.process import Process

class Process_Controller:
    def create(user_enroll: str, proof_doc: str, credits: str, period:str, type:str, description:str, status: str):
        assert user_enroll, "User enroll can't be empty."
        assert proof_doc, "Document can't be empty."
        assert period, "period can't be empty."
        assert type, "type can't be empty."
        assert description, "descriptio can't be empty."
        assert credits, "Hours can't be empty."
        assert status, "status can't be empty."

        process = Process.insert(user_enroll, proof_doc, credits, period, type, description, status)

        return vars(process)
