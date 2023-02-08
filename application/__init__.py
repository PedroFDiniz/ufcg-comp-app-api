from flask import Flask
from application.database.psql_database import init_database, fill_activities_metrics

app = Flask(__name__)

try:
    init_database()
    fill_activities_metrics()
    print("Server available")
except Exception as e:
    print("Server not available")
    raise e

from application import router