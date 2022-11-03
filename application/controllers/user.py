from application.models.user import User
from application.utils.validation import *

class User_Controller:

    def create(enroll: str, name: str, email: str, role: str, password: str):
        myAssert(enroll, Exception("Enroll can't be an empty", 400))
        myAssert(name, Exception("Name can't be an empty", 400))
        myAssert(email, Exception("Email can't be an empty", 400))
        myAssert(role, Exception("Role can't be an empty", 400))
        myAssert(password, Exception("Password can't be an empty", 400))
        myAssert(User.find(enroll) is None, Exception("User already registered", 400))

        return User.create(enroll, name, email, role, password)

    def confirm_email(enroll, email_confirmation_jwt):
        user  = User.find(enroll)
        myAssert(user is not None, Exception("User not found", 404))
        myAssert(user.get('email_confirmation_jwt') == email_confirmation_jwt, Exception("Invalid email jwt", 400))

        return User.update(enroll, {"email_confirmed": True, "_email_confirmation_jwt": None})

    def auth(email: str, password: str):
        myAssert(email, Exception("Email can't be an empty", 400))
        myAssert(password, Exception("Password can't be an empty", 400))

        