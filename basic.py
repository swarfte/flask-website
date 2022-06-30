import flask as web
import flask_sqlalchemy as sql
import json

with open("./config/location.json") as f:
    location = json.load(f)

app = web.Flask(__name__)

app.config['SECRET_KEY'] = 'edenitchan2016'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = sql.SQLAlchemy(app)


def get_app():
    return app


def get_db():
    return db


def get_location():
    return location
