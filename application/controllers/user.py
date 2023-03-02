from application.models.user import User
from application.utils.validation import *
from application.database.psql_database import DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT


class User_Controller:

    def create(name: str, email: str, role: str, picture: str = None):
        myAssert(name, AssertionError("Nome não pode ser vazio.", 400))
        myAssert(email, AssertionError("Email não pode ser vazio.", 400))
        myAssert(role, AssertionError("Cargo não pode ser vazio.", 400))
        myAssert(User.find_by_email(email) is None, AssertionError("User already registered.", 409))

        if role.upper() in [DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT]:
            user = User.create(name, email, role.lower(), picture)
            return User_Controller.map_user_to_dict(user)
        else:
            raise AssertionError("Cargo inválido.", 400)

    def update_enroll(email: str, enroll: int):
        myAssert(email, AssertionError("Email não pode ser vazio.", 400))
        myAssert(enroll, AssertionError("Matricula não pode ser vazio.", 400))
        myAssert(len(str(enroll)) == 9, AssertionError("Matrícula inválida.", 400))
        myAssert(User.find_by_email(email), AssertionError(f"Usuário não encontrado.", 404))

        user = User.update_enroll(email, enroll)
        return User_Controller.map_user_to_dict(user)

    def find_by_email(email: str):
        myAssert(email, AssertionError("Email não pode ser vazio.", 400))

        user = User.find_by_email(email)
        myAssert(user, AssertionError(f"Usuário não encontrado.", 404))

        return User_Controller.map_user_to_dict(user)

    def find_by_role(role: str):
        myAssert(role, AssertionError("Cargo não pode ser vazio.", 400))

        if role.upper() not in [DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER, DB_ENUM_U_ROLE_STUDENT]:
            raise AssertionError("Cargo inválido.", 400)

        users = User.find_by_role(role.lower())
        myAssert(users, AssertionError(f"Usuário não encontrado.", 404))

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

