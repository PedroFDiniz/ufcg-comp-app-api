import base64
from application import app
from flask import request, jsonify
from application.utils.validation import *
from application.controllers.activity import Activity_Controller

@app.route("/activity/register", methods=["POST"])
def register_activity():
    files = request.files
    proof_doc = files['proof_doc']
    b64_doc = base64.b64encode(proof_doc.read()).decode('UTF-8')

    data = request.form
    owner_email = data['owner_email']
    owner_enroll = data['owner_enroll']
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
        Activity_Controller.register(owner_email, owner_enroll, b64_doc, period, type, description)
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
            query[e_str] = e_raw[0]

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

@app.route("/activities/count", methods=["GET"])
def count_activities():
    try:
        activities_count = Activity_Controller.count()
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
