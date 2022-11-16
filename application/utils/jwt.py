import jwt, datetime
from dotenv import load_dotenv
from application.utils.constants import JWT_SECRET, JWT_TIMEOUT, JWT_EMAIL_TIMEOUT

def create_email_confirmation_jwt(email):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EMAIL_TIMEOUT),
        "iat": datetime.datetime.utcnow(),
        "sub": email
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm="HS256"
    )

def encode_auth_token(user_id:str) -> str:
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_TIMEOUT),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm="HS256"
    )

def decode_auth_token(auth_token):
    payload = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
    expire_datetime = datetime.datetime.fromtimestamp(payload['exp'])
    current_datetime = datetime.datetime.now()

    return expire_datetime > current_datetime
