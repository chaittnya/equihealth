from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from config import Config
from extensions import db
from api.base import api_base
from api.hospitals import api_hospitals
from api.complaints import api_complaints
from api.users import api_users
from api.charts import api_charts

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from models import Hospital, Category

app.register_blueprint(api_base)
app.register_blueprint(api_hospitals)
app.register_blueprint(api_complaints)
app.register_blueprint(api_users)
app.register_blueprint(api_charts)

if __name__ == "__main__":
    app.run(debug=True)