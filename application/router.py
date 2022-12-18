import threading, os
from application import app
from flask import request, jsonify, send_file

from application.utils.email import *
from application.utils.validation import *

from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller

# ====== User

@app.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    enroll = data['enroll']
    name = data['name']
    email = data['email']
    role = data['role']

    try:
        User_Controller.create(enroll, name, email, role)
        status_code = 200
        message = "User created sussefull"
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1] 

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/user", methods=["GET"])
def find_user():
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
    except Exception as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/user/<enroll>", methods=["GET"])
def find_user_by_enroll(enroll):
    try:
        user = User_Controller.find_by_enroll(enroll)
        status_code = 200
        res = {
            "user": user,
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


# ====== Activity
@app.route("/activity/register", methods=["POST"])
def register_activity():
    files = request.files
    preflight_doc = files['preflight_doc']

    data = request.form
    owner_email = data['owner_email']
    owner_enroll = data['owner_enroll']
    period = data['period']
    type = data['type']
    description = data['description']

    doc_dir = f'./documents'
    doc_path = f'{owner_enroll}/{preflight_doc.filename}'
    main_path = f'{doc_dir}/{doc_path}'

    if not os.path.exists(f'{doc_dir}/{owner_enroll}'):
        os.makedirs(f'{doc_dir}/{owner_enroll}')

    if not os.path.exists(main_path):
      preflight_doc.save(main_path)

    try:
        Activity_Controller.register(owner_email, owner_enroll, doc_path, period, type, description)
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

@app.route("/activity/update/<activity_id>", methods=["PUT"])
def update_activity(activity_id):
    data = request.get_json()

    try:
        Activity_Controller.update(activity_id, data)
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
    except Exception as e:
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
    return send_file(f'../documents/{path}', as_attachment=True)

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
    except Exception as e:
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
    except Exception as e:
        message = e.args[0]
        status_code = 400
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "http://localhost:3000")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response
