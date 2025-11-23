from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

from config import Config
from extensions import db
from api.base import api_base
from api.hospitals import api_hospitals
from api.complaints import api_complaints
from api.users import api_users
from api.charts import api_charts

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://equihealth-1.onrender.com/"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

CORS(app, resources={
    r"/api/*": {
        "origins": "https://equihealth-1.onrender.com/"
    }
})

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from models import Hospital, Category

app.register_blueprint(api_base)
app.register_blueprint(api_hospitals)
app.register_blueprint(api_complaints)
app.register_blueprint(api_users)
app.register_blueprint(api_charts)

port = os.environ.get("PORT", 5000)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(port))