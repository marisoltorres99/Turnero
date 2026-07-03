from flask import Flask, render_template
from flask_migrate import Migrate
from models.cliente import Cliente
from models.servicio import Servicio
from models.turno import Turno
from routes.clientes_routes import cliente_bp
from routes.servicios_routes import servicio_bp
from routes.turnos_routes import turnos_bp

from models.db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///turnero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route("/")
def inicio():
    return render_template("dashboard/index.html")

app.register_blueprint(cliente_bp)
app.register_blueprint(servicio_bp)
app.register_blueprint(turnos_bp)