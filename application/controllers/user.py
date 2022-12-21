from application.models.user import User
from application.utils.validation import *

class User_Controller:
  
    def create(name: str, email: str, role: str):
        myAssert(name, Exception("Name can't be empty", 400))
        myAssert(email, Exception("Email can't be empty", 400))
        myAssert(role, Exception("Role can't be empty", 400))
        myAssert(User.find_one({'email' : email}) is None, Exception("User already registered", 400))

        return User.create(name, email, role)

    def find(query: dict):
        users = list(User.find(query))
        myAssert(users, Exception(f"Users not found.", 404))
        return users

    def find_by_email(email: str):
        user = User.find_one({'email': email})
        myAssert(user, Exception(f"User not found.", 404))
        return user
