import jwt, os, base64
from application import app
from functools import wraps
from flask import request, jsonify, abort, make_response
from application.utils.validation import *
from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller

def auth_required(f):
    @wraps(f)
    def token_decoder(*args, **kwargs):
        auth = request.headers.get('Authorization')
        try:
            User_Controller.check_auth(auth)
        except jwt.ExpiredSignatureError:
            status_code = 498 
            message = "Signature expired. Please log in again.",
            return jsonify({message, status_code}), status_code            
        except jwt.InvalidTokenError:
            status_code = 498 
            message = "Invalid token. Please log in again.",
            return jsonify({message, status_code}), status_code
        except Exception as e:
            message = e.args[0]
            status_code = e.args[1]
            return jsonify({message, status_code}), status_code

        return f(*args, **kwargs)
    return token_decoder

@app.route("/user/create", methods=["POST"])
def create_user():
    data = request.get_json()
    enroll = data['enroll']
    name = data['name']
    email = data['email']
    role = data['role']
    password = data['password']

    try:
        User_Controller.create(enroll, name, email, role, password)
        status_code = 200
        message = "Usuário criado com sucesso"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/user/<enroll>/confirm_email/<email_confirmation_jwt>", methods=["GET"])
def confirm_email(enroll, email_confirmation_jwt):
    try:
        User_Controller.confirm_email(enroll, email_confirmation_jwt)
        status_code = 200
        email_confirmed = True
        message = "Confirmacao de email bem sucedida"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]
        email_confirmed = False

    res = {
        "message": message,
        "status_code": status_code,
        "email_confirmed": email_confirmed,
    }

    return jsonify(res), status_code

@app.route("/user/auth", methods=["POST"])
def auth_user():
    data = request.get_json()
    enroll = data['enroll']
    password = data['password']

    try:
        token = User_Controller.auth(enroll, password)
        status_code = 200
        message = "Usuário autenticado com sucesso"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "token": token,
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/activity/register", methods=["POST"])
@auth_required
def register_activity():
    files = request.files
    proof_doc = files['proof_doc']
    b64_doc = base64.b64encode(proof_doc.read()).decode('UTF-8')

    data = request.form
    owner_enroll = data['owner_enroll']
    credits = data['credits']
    period = data['period']
    type = data['type']
    description = data['description']

    # userdir = f'./documents/{owner_enroll}'
    # filepath = f'{userdir}/{proof_doc.filename}'

    # if not os.path.exists(userdir):
    #     os.makedirs(userdir)

    # if not os.path.exists(filepath):
    #   proof_doc.save(filepath)

    try:
      Activity_Controller.register(owner_enroll, b64_doc, credits, period, type, description)
      status_code = 200
      message = "Atividade registrada com sucesso"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

# # TODO add @admin_required
# @app.route("/activities", methods=["GET"])
# @auth_required
# def find_activity():
#     data = request.form

#     query = dict()
#     for e in data:
#         query[e] = eval(data[e])

#     try:
#         activity = Activity_Controller.find(query)
#         status_code = 200

#         print(activity)

#         res = {
#             "activity": activity,
#             "status_code": status_code,
#         }

#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]
#         res = {
#             "message": message,
#             "status_code": status_code,
#         }

#     return jsonify(res), status_code