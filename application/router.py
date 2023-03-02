import re
import base64
import requests

from functools import wraps
from flask import request, jsonify, send_file, render_template

from application import app
from application.utils.validation import *
from application.utils.constants import AUTH_STUDENT_DOMAIN, AUTH_REVIEWER_DOMAIN, AUTH_COORDINATOR_EMAIL
from application.database.psql_database import DB_ENUM_U_ROLE_STUDENT, DB_ENUM_U_ROLE_COORDINATOR, DB_ENUM_U_ROLE_REVIEWER

from application.controllers.user import User_Controller
from application.controllers.activity import Activity_Controller
from application.controllers.process import Process_Controller

from google.auth import jwt

# ====== CHECK AUTH

def check_auth_student(f):
    @wraps(f)
    def token_verifier(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if auth is None:
            return jsonify({"message": "No Authorization header"}), 401

        try:
            url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={0}'.format(auth.split(' ')[1])
            response = requests.get(url)
            data = response.json()

            if int(data['expires_in']) <= 0:
                return jsonify({"message": "Token expired"}), 401

            if not re.match(rf"[^@]+{AUTH_STUDENT_DOMAIN}", data['email']):
                return jsonify({"message": "Invalid email"}), 401

            # TODO ver se o email é igual o match do token na tabela, se não, revoga o token
        except KeyError as e:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return token_verifier


def check_auth_coordinator(f):
    @wraps(f)
    def token_verifier(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if auth is None:
            return jsonify({"message": "No Authorization header"}), 401

        try:
            token = auth.split(' ')[1]
            data = jwt.decode(token, verify=False)

            if int(data['exp']) <= 0:
                return jsonify({"message": "Token expired"}), 401

            if not data['email'] == AUTH_COORDINATOR_EMAIL:
                return jsonify({"message": "Invalid email"}), 401

            # TODO ver se o email é igual o match do token na tabela, se não, revoga o token
        except KeyError as e:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return token_verifier


def check_auth_reviewer(f):
    @wraps(f)
    def token_verifier(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if auth is None:
            return jsonify({"message": "No Authorization header"}), 401

        try:
            token = auth.split(' ')[1]
            data = jwt.decode(token, verify=False)

            if int(data['exp']) <= 0:
                return jsonify({"message": "Token expired"}), 401

            if not re.search(rf"[^@]+{AUTH_REVIEWER_DOMAIN}", data['email']):
                return jsonify({"message": "Invalid email"}), 401

            # TODO ver se o email é igual o match do token na tabela, se não, revoga o token
        except KeyError as e:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return token_verifier

# ====== User

@app.route("/auth/user/student", methods=["POST"])
def auth_student():
    auth = request.headers.get('Authorization')

    response = requests.get('https://openidconnect.googleapis.com/v1/userinfo', 
        headers={
            'Authorization': auth,
            'Content-Type': 'application/json'
        }
    )

    if response.status_code != 200:
        res = {
          "message": "Failed to connect to Google", 
          "status_code": response.status_code
        }
        return jsonify(res), response.status_code

    try:
        response_data = response.json()
        hd = response_data['hd']
        email = response_data['email']
        user = User_Controller.find_by_email(email)

        status_code = 200
        message = "User successfully authenticated"
    except AssertionError as e:
        if e.args[1] == 404 and hd == "ccc.ufcg.edu.br":
            name = response_data['name']
            picture = response_data['picture']
            user = User_Controller.create(name, email, DB_ENUM_U_ROLE_STUDENT, picture)

            status_code = 200
            message = "User successfully authenticated"
        else:
            user = None
            message = e.args[0]
            status_code = e.args[1]

    res = {
        "user": user,
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/auth/user/reviewer_and_coordinator", methods=["POST"])
def auth_reviewer_and_coordinator():
    auth = request.headers.get('Authorization')
    token = auth.split(' ')[1]
    token_data = jwt.decode(token, verify=False)

    try:
        email = token_data['email']
        picture = token_data['picture']
        user = User_Controller.find_by_email(email)

        status_code = 200
        message = "User successfully authenticated"
    except AssertionError as e:
        if e.args[1] == 404 and re.search(rf"[^@]+{AUTH_REVIEWER_DOMAIN}", email):
            name = token_data['name']
            picture = token_data['picture']
            user = User_Controller.create(name, email, DB_ENUM_U_ROLE_REVIEWER, picture)

            status_code = 200
            message = "User successfully authenticated"
        elif e.args[1] == 404 and email == AUTH_COORDINATOR_EMAIL:
            name = token_data['name']
            picture = token_data['picture']
            user = User_Controller.create(name, email, DB_ENUM_U_ROLE_COORDINATOR, picture)

            status_code = 200
            message = "User successfully authenticated"
        else:
            user = None
            message = e.args[0]
            status_code = e.args[1]

    res = {
        "user": user,
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/user/register", methods=["POST"])
@check_auth_coordinator
def register_user():
    data = request.form

    name = http_data_field(data, 'name')
    email = http_data_field(data, 'email')
    role = http_data_field(data, 'role')

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

@app.route("/user/update/enroll", methods=["PUT"])
@check_auth_coordinator
def update_user_enroll():
    data = request.form

    email = http_data_field(data, 'email')
    enroll = int(http_data_field(data, 'enroll'))

    try:
        User_Controller.update_enroll(email, enroll)
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


# ====== Activity

@app.route("/activity/register", methods=["POST"])
@check_auth_student
def register_activity():
    files = request.files
    voucher = files['voucher']

    data = request.form
    owner_email = http_data_field(data, 'owner_email')
    kind = http_data_field(data, 'kind')
    description = http_data_field(data, 'description')
    workload = http_data_field(data, 'workload')
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
    
@app.route("/activities/find_all", methods=["GET"])
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
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activities/find_by_state", methods=["POST"])
def find_by_owner_or_state():
    data = request.form

    owner_email = http_data_field(data, 'owner_email')
    states = http_data_field(data, 'states')
    if states:
        states = states.replace('[', '').replace(']', '').split(',')
        states = [state.strip() for state in states]

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
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activity/assign/<activity_id>", methods=["PUT"])
@check_auth_coordinator
def assign_activity(activity_id):
    data = request.form

    reviewer_email = data['reviewer_email']

    try:
        Activity_Controller.assign(activity_id, reviewer_email)
        status_code = 200
        message = "Atividade atribuida com sucesso"
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]

    res = {
        "message": message,
        "status_code": status_code,
    }

    return jsonify(res), status_code

@app.route("/activity/validate/<activity_id>", methods=["PUT"])
@check_auth_reviewer
def validate_activity(activity_id):
    data = request.form

    reviewer_email = http_data_field(data, 'reviewer_email')
    computed_credits = http_data_field(data, 'computed_credits')
    justify = http_data_field(data, 'justify')
    state = http_data_field(data, 'state')

    try:
        Activity_Controller.validate(int(activity_id), reviewer_email, state, computed_credits, justify)
        status_code = 200
        message = "Atividade validada com sucesso"
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
    data = request.form
   
    owner_email = http_data_field(data, 'owner_email')
    states = http_data_field(data, 'states')
    if states:
        states = states.replace('[', '').replace(']', '').split(',')
        states = [state.strip() for state in states]

    try:
        activities_count = Activity_Controller.count_by_owner_or_state(owner_email, states)
        status_code = 200
        res = {
            "activities_count": activities_count,
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
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

    return jsonify(res), status_code

@app.route("/activity/voucher/download", methods=["GET"])
def download_activity_voucher():
    path = request.args.get('path')
    return send_file(f'../{path}', as_attachment=True)

@app.route("/activities/metrics", methods=["GET"])
def get_activity_metrics():
    try:
        metrics_info = Activity_Controller.get_metrics()
        status_code = 200
        res = {
            "metrics_info": metrics_info,
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


# ====== Process ======

@app.route("/process/generate", methods=["POST"])
@check_auth_student
def generateProcess():
    data = request.form
    owner_email = http_data_field(data, 'owner_email')

    try:
        final_process_path = Process_Controller.generate_process(owner_email)

        with open(final_process_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode()

        return jsonify(file=pdf_base64)
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }

        return jsonify(res), status_code
    except FileNotFoundError as e:
        raise (e)


@app.route("/process/check", methods=["POST"])
@check_auth_coordinator
def checkProcess():
    files = request.files
    voucher = files['voucher']

    data = request.form
    user_enroll = int(http_data_field(data, 'user_enroll'))

    try:
        is_valid = Process_Controller.check_process(voucher, user_enroll)

        status_code = 200
        res = {
            "isValid": is_valid,
            "status_code": status_code,
        }

        return jsonify(res), status_code
    except AssertionError as e:
        message = e.args[0]
        status_code = e.args[1]
        res = {
            "message": message,
            "status_code": status_code,
        }
        return jsonify(res), status_code

    except FileNotFoundError as e:
        raise (e)


# ====== User Guides ======

@app.route("/guide/activities", methods=["GET"])
def get_process_user_guide():
    return render_template('activities_user_guide.html')


# ====== CORS ======

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response
