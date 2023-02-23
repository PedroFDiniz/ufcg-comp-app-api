from application.models.user import User
from application.utils.validation import *
from application.database.psql_database import DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT


class User_Controller:

    def create(name: str, email: str, role: str, picture: str = None):
        myAssert(name, AssertionError("Name can't be empty", 400))
        myAssert(email, AssertionError("Email can't be empty", 400))
        myAssert(role, AssertionError("Role can't be empty", 400))
        myAssert(User.find_by_email(email) is None, AssertionError("User already registered", 400))

        if role.upper() in [DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT]:
            user = User.create(name, email, role.lower(), picture)
            return User_Controller.map_user_to_dict(user)
        else:
            raise AssertionError("Invalid role", 400)

    def find_by_email(email: str):
        myAssert(email, AssertionError("Email can't be empty", 400))

        user = User.find_by_email(email)
        myAssert(user, AssertionError(f"User not found.", 404))

        return User_Controller.map_user_to_dict(user)

    def find_by_role(role: str):
        myAssert(role, AssertionError("Role can't be empty", 400))

        if role.upper() not in [DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT]:
            raise AssertionError("Invalid role", 400)

        users = User.find_by_role(role.lower())
        myAssert(users, AssertionError(f"User not found.", 404))

        users_list = list()
        for user in users:
            users_list.append(User_Controller.map_user_to_dict(user))

        return users_list

    def map_user_to_dict(user):
        return {
            'email': user[0],
            'name': user[1],
            'role': user[2],
            'enroll': user[3],
            'picture': user[4],
        }

