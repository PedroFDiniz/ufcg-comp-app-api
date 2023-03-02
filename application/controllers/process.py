from application.utils.validation import *
from application.models.user import User
from application.models.process import Process
from application.models.activity import Activity
from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller
from application.database.psql_database import DB_ENUM_A_STATE_APPROVED
from werkzeug.datastructures import FileStorage


class Process_Controller:
    def generate_process(owner_email: str):
        myAssert(owner_email, AssertionError("Owner email can't be empty.", 400))

        user = User.find_by_email(owner_email)
        myAssert(user, AssertionError("Student not found.", 404))

        user = User_Controller.map_user_to_dict(user)
        activities = Activity.find_by_owner_or_state(owner_email, [DB_ENUM_A_STATE_APPROVED], None, None, None, None)
        myAssert(activities, AssertionError("Activities not found.", 404))
        
        activities_list = list()
        for activity in activities:
          activities_dict = Activity_Controller.map_activity_to_dict(activity)
          activities_list.append(activities_dict)

        data, voucher_paths, reviewers = Process.get_process_data(activities_list)
        Process.generate_table_of_contents(owner_email, user['name'], user['enroll'], data)

        process_path = Process.merge_vouchers(owner_email, voucher_paths)
        process_path = Process.generate_final_process(process_path, reviewers)
        Process.save_process(process_path, owner_email)

        return process_path

    def check_process(voucher: FileStorage, user_enroll: int):
        myAssert(user_enroll, AssertionError("The student enroll can't be empty.", 400))
        myAssert(len(str(user_enroll)) == 9, AssertionError("Student enroll must have 9 digits.", 400))

        user = User.find_by_enroll(user_enroll)
        myAssert(user, AssertionError("Student not found.", 404))

        user = User_Controller.map_user_to_dict(user)
        myAssert(user['enroll'] == user_enroll, AssertionError("Invalid User.", 400))
        
        return Process.check_process(voucher, user['email'])

