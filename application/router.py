import base64

from application import app
from flask import request, jsonify, send_file

from application.utils.validation import *
from application.utils.constants import VOUCHERS_GENERAL_DIR

from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller
from application.controllers.process import Process_Controller

# ====== User

@app.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    role = data['role']

    try:
        User_Controller.create(name, email, role)
        status_code = 200
        message = "User successfully created"
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/user/email/<email>", methods=["GET"])
def find_user_by_email(email):
    try:
        user = User_Controller.find_by_email(email)
        status_code = 200
        res = {
            "user": user,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/user/role/<role>", methods=["GET"])
def find_by_role(role):
    try:
        users = User_Controller.find_by_role(role)
        status_code = 200
        res = {
            "users": users,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

# ====== Activity

@app.route("/activity/register", methods=["POST"])
def register_activity():
    files = request.files
    voucher = files['voucher']

    data = request.form
    owner_email = http_data_field(data, 'owner_email')
    workload = http_data_field(data, 'workload')
    kind = http_data_field(data, 'kind')
    description = http_data_field(data, 'description')
    start_date = http_data_field(data, 'start_date')
    end_date = http_data_field(data, 'end_date')

    try:
        Activity_Controller.register(owner_email, voucher, workload, kind, description, start_date, end_date)
        status_code = 200
        message = "Activity successfully created"
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/activities/find_all", methods=["POST"])
def find_all_subm_activities():
    page = request.args.get('page')
    size = request.args.get('size')
    sort = request.args.get('sort')
    order = request.args.get('order')

    try:
        activity = Activity_Controller.find_all_subm_activities(page, size, sort, order)
        status_code = 200
        res = {
            "activities": activity,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = 400
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code


# @app.route("/activity/validate/<activity_id>", methods=["PUT"])
# def validate_activity(activity_id):
#     data = request.get_json()

#     try:
#         Activity_Controller.validate(activity_id, data)
#         status_code = 200
#         message = "Atividade atualizada com sucesso"
#     except AssertionError as e:
#         message = e.args[0]
#         status_code = e.args[1]

#     res = {
#         "message": message,
#         "status_code": status_code,
#     }

    return jsonify(res), status_code

@app.route("/activities/find_by_state", methods=["POST"])
def find_by_owner_or_state():
    data = request.get_json()
    states = http_data_field(data, 'states')
    owner_email = http_data_field(data, 'owner_email')

    page = int(request.args.get('page'))
    size = int(request.args.get('size'))
    sort = str(request.args.get('sort'))
    order = str(request.args.get('order'))

    try:
        activity = Activity_Controller.find_by_owner_or_state(owner_email, states, page, size, sort, order)
        status_code = 200
        res = {
            "activities": activity,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = 400
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activity/assign/<activity_id>", methods=["PUT"])
def assign_activity(activity_id):
    data = request.get_json()
    reviewer_email = data['reviewer_email']

    try:
        Activity_Controller.assign(activity_id, reviewer_email)
        status_code = 200
        message = "Atividade atualizada com sucesso"
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/activity/validate/<activity_id>", methods=["PUT"])
def validate_activity(activity_id):
    data = request.get_json()

    reviewer_email = http_data_field(data, 'reviewer_email')
    computed_credits = http_data_field(data, 'computed_credits')
    justify = http_data_field(data, 'justify')
    state = http_data_field(data, 'state')

    try:
        Activity_Controller.validate(activity_id, reviewer_email, state, computed_credits, justify)
        status_code = 200
        message = "Atividade atualizada com sucesso"
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/activities/count_by_state", methods=["POST"])
def count_activities_by_state():
    data = request.get_json()
    states = http_data_field(data, 'states')
    owner_email = http_data_field(data, 'owner_email')

    try:
        activities_count = Activity_Controller.count_by_owner_or_state(owner_email, states)
        status_code = 200
        res = {
            "activities_count": activities_count,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = 400
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activities/computeCredits/<owner_email>", methods=["GET"])
def compute_activities_credits(owner_email):
    try:
        credits_info = Activity_Controller.compute_credits(owner_email)
        status_code = 200
        res = {
            "credits_info": credits_info,
            "status_code": status_code,
        }
    except AssertionError as e:
        message = e.args[0]
        status_code = 400
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code
@app.route("/activity/voucher/download", methods=["GET"])
def download_activity_voucher():
    path = request.args.get('path')
    return send_file(f'../{VOUCHERS_GENERAL_DIR}/{path}', as_attachment=True)


# ====== Process ======

@app.route("/process/generate", methods=["POST"])
def generateProcess():
    data = request.get_json()

    owner_email = data['owner_email']
    owner_name = data['owner_name']
    owner_enroll = data['owner_enroll']

    try:
        final_process_path = Process_Controller.generate_process(owner_email, owner_name, owner_enroll)

        with open(final_process_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode()

        return jsonify(file=pdf_base64)
    except FileNotFoundError as e:
        raise (e)


@app.route("/process/check", methods=["POST"])
def checkProcess():
    files = request.files
    voucher = files['voucher']
    user_email = request.form['user_email']

    try:
        is_valid = Process_Controller.check_process(voucher, user_email)

        status_code = 200
        res = {
            "isValid": is_valid,
            "status_code": status_code,
        }

        return jsonify(res), status_code
    except FileNotFoundError as e:
        raise (e)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,PATCH')
    return response
