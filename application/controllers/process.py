from application.utils.validation import *
from application.models.user import User
from application.models.process import Process
from application.models.activity import Activity
from application.database.psql_database import DB_ENUM_A_STATE_APPROVED
from werkzeug.datastructures import FileStorage


class Process_Controller:
    def generate_process(owner_email: str, owner_name: str, owner_enroll: str):
        myAssert(owner_email, AssertionError("Owner email can't be empty.", 400))
        myAssert(owner_name, AssertionError("Owner name can't be empty.", 400))
        myAssert(owner_enroll, AssertionError("Owner enroll can't be empty.", 400))

        activities = Activity.find_by_owner_or_state(owner_email, [DB_ENUM_A_STATE_APPROVED], None, None, None, None)

        data, voucher_paths, reviewers = Process.get_process_data(activities)
        Process.generate_table_of_contents(owner_email, owner_name, owner_enroll, data)

        process_path = Process.merge_vouchers(owner_email, voucher_paths)
        process_path = Process.generate_final_process(process_path, reviewers)
        Process.save_process(process_path, owner_email)

        return process_path

    def check_process(voucher: FileStorage, user_email: str):
        myAssert(user_email, AssertionError("The student email can't be empty.", 400))
        user = User.find_by_email(user_email)
        myAssert(user, AssertionError("Student not found.", 404))
        myAssert(user[0] == user_email, AssertionError("Invalid User.", 400))         # 0 is the user email index
        
        return Process.check_process(voucher, user_email)

