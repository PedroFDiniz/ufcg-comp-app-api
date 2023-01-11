import threading
from application import app
from flask import request, jsonify, send_file

from application.utils.email import *
from application.utils.validation import *
from application.utils.constants import VOUCHERS_GENERAL_DIR

from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller

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


@app.route("/user/<email>", methods=["GET"])
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


@app.route("/users", methods=["POST"])
def find_users():
    data = request.get_json()

    query = dict()
    for e_str in data:
        e_raw = data[e_str]
        if type(e_raw) is list:
            query[e_str] = {'$in': e_raw}
        else:
            query[e_str] = e_raw

    try:
        users = User_Controller.find(query)
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
    owner_email = data['owner_email']
    period = data['period']
    kind = data['type']
    description = data['description']

    try:
        Activity_Controller.register(
            owner_email, voucher, period, kind, description)
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


@app.route("/activity/update/<activity_id>", methods=["PUT"])
def update_activity(activity_id):
    data = request.get_json()

    try:
        Activity_Controller.update(activity_id, data)
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


@app.route("/activity/assign/<activity_id>", methods=["PUT"])
def assign_activity(activity_id):
    data = request.get_json()

    reviewer = data['reviewer']

    try:
        thread = threading.Thread(target=send_noreply_email(reviewer))
        thread.start()

        Activity_Controller.assign(activity_id, reviewer)
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


@app.route("/activity/doc/download", methods=["GET"])
def download_activity_doc():
    path = request.args.get('path')
    return send_file(f'../{VOUCHERS_GENERAL_DIR}/{path}', as_attachment=True)


@app.route("/activities", methods=["POST"])
def find_activities():
    data = request.get_json()

    page = int(request.args.get('page'))
    size = int(request.args.get('size'))
    sort = str(request.args.get('sort'))
    order = str(request.args.get('order'))

    query = dict()
    for e_str in data:
        e_raw = data[e_str]
        if type(e_raw) is list:
            query[e_str] = {'$in': e_raw}
        else:
            query[e_str] = e_raw

    try:
        activity = Activity_Controller.find(query, page, size, sort, order)
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


@app.route("/activities/count", methods=["POST"])
def count_activities():
    data = request.get_json()

    query = dict()
    for e_str in data:
        e_raw = data[e_str]
        if type(e_raw) is list:
            query[e_str] = {'$in': e_raw}
        else:
            query[e_str] = e_raw

    try:
        activities_count = Activity_Controller.count(query)
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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response
