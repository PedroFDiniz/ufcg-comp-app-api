from application import app
from flask import request, jsonify
from application.controllers.user import User_Controller


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
