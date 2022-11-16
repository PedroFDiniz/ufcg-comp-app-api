from application.models.user import User
from application.utils.validation import *
from application.utils.jwt import *

class User_Controller:

    def create(enroll: str, name: str, email: str, role: str, password: str):
        myAssert(enroll, Exception("Enroll can't be empty", 400))
        myAssert(name, Exception("Name can't be empty", 400))
        myAssert(email, Exception("Email can't be empty", 400))
        myAssert(role, Exception("Role can't be empty", 400))
        myAssert(password, Exception("Password can't be empty", 400))
        myAssert(User.find_by_enroll(enroll) is None, Exception("User already registered", 400))

        return User.create(enroll, name, email, role, password)

    def confirm_email(enroll, email_confirmation_jwt):
        user  = User.find_by_enroll(enroll)
        myAssert(user is not None, Exception("User not found", 404))
        myAssert(user.get('email_confirmation_jwt') == email_confirmation_jwt, Exception("Invalid email jwt", 400))

        return User.update(enroll, {"email_confirmed": True, "_email_confirmation_jwt": None})

    def auth(enroll: str, password: str):
        myAssert(enroll, Exception("Enroll can't be empty", 400))
        myAssert(password, Exception("Password can't be empty", 400))

        user = User.find_by_enroll(enroll, True)
        myAssert(user is not None, Exception("User not found", 404))
        myAssert(password == user.get('password'), Exception("Wrong Password", 401))

        return encode_auth_token(user.get('enroll'))
        
    def check_auth(auth: str):
        myAssert(auth, jwt.InvalidTokenError)
        myAssert(len(auth.split(" ")) == 2 and "Bearer" in auth, jwt.InvalidTokenError)

        token = auth.split().pop()
        return decode_auth_token(token)

