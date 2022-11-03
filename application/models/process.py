from application import MONGO_DB

class Process:

    @staticmethod
    def insert(user_id: str, proof_doc:str, comp_hours: int, status: str):
        """
        This function add a process in the database
        -------------------------------------------
        user_id:    Id of the process owner
        proof_doc:  Is the document to comproove the time spend
        comp_hours: Amount of hours that will be computed
        status:     Process status (Created, Validated, Rejected)
        """

        try:
            process = {
                user_id: user_id, 
                proof_doc: proof_doc, 
                comp_hours: comp_hours, 
                status: status
            }
            
            MONGO_DB.process.insert_one(process)
        except ValueError as e:
            raise(e)

    @staticmethod
    def find(user_id: str):
        user = MONGO_DB.user.find_one(user_id)
        return user

# get opened
# get all
# get by user
# update 
# delete
