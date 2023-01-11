from application.models.user import User
from application.utils.validation import *

class User_Controller:
  
    def create(name: str, email: str, role: str):
        myAssert(name, AssertionError("Name can't be empty", 400))
        myAssert(email, AssertionError("Email can't be empty", 400))
        myAssert(role, AssertionError("Role can't be empty", 400))
        myAssert(User.find_one({'email' : email}) is None, AssertionError("User already registered", 400))

        return User.create(name, email, role)

    def find(query: dict):
        users = list(User.find(query))
        myAssert(users, AssertionError(f"Users not found.", 404))
        return users

    def find_by_email(email: str):
        user = User.find_one({'email': email})
        myAssert(user, AssertionError(f"User not found.", 404))
        return user
