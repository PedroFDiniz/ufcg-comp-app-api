import base64
from json import dumps
from application import app
from functools import wraps
from flask import Response, request, jsonify, abort
from application.utils.validation import *
from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller

def auth_required(f):
    @wraps(f)
    def token_decoder(*args, **kwargs):
        try:
            auth = request.headers.get('Authorization')
            User_Controller.check_auth(auth)
        except Exception as e:
            status_code = 498            
            message = dumps({'message': "Invalid token."})
            abort(Response(message, status_code))

        return f(*args, **kwargs)
    return token_decoder

# @app.route("/user/auth", methods=["POST"])
# def auth_user():
#     data = request.get_json()
#     enroll = data['enroll']
#     password = data['password']

#     try:
#         token = User_Controller.auth(enroll, password)
#         status_code = 200
#         message = "Usuário autenticado com sucesso"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "token": token,
#         "message": message,
#         "status_code": status_code,
#     }

#     return jsonify(res), status_code

# TODO colocar um campo para adicionar revisores válidos
# @app.route("/user/create", methods=["POST"])
# def create_user():
#     data = request.get_json()
#     enroll = data['enroll']
#     name = data['name']
#     email = data['email']
#     role = data['role']
#     password = data['password']

#     try:
#         User_Controller.create(enroll, name, email, role, password)
#         status_code = 200
#         message = "Usuário criado com sucesso"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "message": message,
#         "status_code": status_code,
#     }

#     return jsonify(res), status_code

# TODO enviar email quando uma atividade for atribuida a alguem
# @app.route("/user/<enroll>/confirm_email/<email_confirmation_jwt>", methods=["GET"])
# def confirm_email(enroll, email_confirmation_jwt):
#     try:
#         User_Controller.confirm_email(enroll, email_confirmation_jwt)
#         status_code = 200
#         email_confirmed = True
#         message = "Confirmacao de email bem sucedida"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]
#         email_confirmed = False

#     res = {
#         "message": message,
#         "status_code": status_code,
#         "email_confirmed": email_confirmed,
#     }

#     return jsonify(res), status_code


# TODO add @admin_required
# @app.route("/user", methods=["GET"])
# @auth_required 
# def find_user():
#     data = request.form

#     query = dict()
#     for e_str in data:
#         e_raw = eval(data[e_str])
#         if len(e_raw) > 1:
#             query[e_str] = {'$all': e_raw}
#         else:
#             query[e_str] = e_raw[0]

#     try:
#         users = User_Controller.find(query)
#         status_code = 200
#         res = {
#             "users": users,
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

# @app.route("/user/<enroll>", methods=["GET"])
# @auth_required 
# def find_user_by_enroll(enroll):
#     try:
#         user = User_Controller.find_by_enroll(enroll)
#         status_code = 200
#         res = {
#             "user": user,
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

# @app.route("/user/<enroll>", methods=["PUT"])
# @auth_required
# def update_user(enroll):
#     data = request.form

#     query = dict()
#     for e_str in data:
#         query[e_str] = data[e_str]

#     try:
#         User_Controller.update(enroll, query)
#         status_code = 200
#         message = "Usuário atualizado com sucesso"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "message": message,
#         "status_code": status_code,
#     }

#     return jsonify(res), status_code

# @app.route("/user/<enroll>", methods=["DELETE"])
# @auth_required
# def remove_user(enroll):
#     try:
#         User_Controller.remove(enroll)
#         status_code = 200
#         message = "Uuário removido com sucesso"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "message": message,
#         "status_code": status_code,
#     }

#     return jsonify(res), status_code

@app.route("/activity/register", methods=["POST"])
def register_activity():
    files = request.files
    proof_doc = files['proof_doc']
    b64_doc = base64.b64encode(proof_doc.read()).decode('UTF-8')

    data = request.form
    owner_email = data['owner_email']
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
        Activity_Controller.register(
            owner_email, owner_enroll, b64_doc, credits, period, type, description)
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

# TODO add @admin_required
@app.route("/activities", methods=["POST"])
def find_activity():
    data = request.get_json()

    query = dict()
    for e_str in data:
        e_raw = data[e_str]
        if type(e_raw) is list:
            query[e_str] = {'$in': e_raw}
        else:
            query[e_str] = e_raw[0]

    try:
        activity = Activity_Controller.find(query)
        status_code = 200
        res = {
            "activities": activity,
            "status_code": status_code,
        }
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activity/update/<owner_enroll>/<description>", methods=["PUT"])
def update_activity(owner_enroll, description):
    data = request.form

    query = dict()
    for e_str in data:
        query[e_str] = data[e_str]

    try:
        Activity_Controller.update(owner_enroll, description, query)
        status_code = 200
        message = "Atividade atualizada com sucesso"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

# @app.route("/activity/remove/<owner_enroll>/<description>", methods=["DELETE"])
# def remove_activity(owner_enroll, description):
#     try:
#         Activity_Controller.remove(owner_enroll, description)
#         status_code = 200
#         message = "Atividade removida com sucesso"
#     except Exception as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "message": message,
#         "status_code": status_code,
#     }

#     return jsonify(res), status_code

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response
