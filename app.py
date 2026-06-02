from flask import Flask
from flask_migrate import Migrate
from models.cliente import Cliente
from models.servicio import Servicio
from models.turno import Turno

from models.db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///turnero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)