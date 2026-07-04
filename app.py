from datetime import date, datetime, timedelta

from flask import Flask, render_template
from flask_migrate import Migrate
from models.cliente import Cliente
from models.servicio import Servicio
from models.turno import Turno
from models.estados_turno import EstadoTurno
from routes.clientes_routes import cliente_bp
from routes.servicios_routes import servicio_bp
from routes.turnos_routes import turnos_bp

from models.db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///turnero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

ESTADOS_ACTIVOS = (EstadoTurno.PENDIENTE, EstadoTurno.CONFIRMADO)

@app.route("/")
def inicio():
    ahora = datetime.now()
    inicio_dia = datetime.combine(date.today(), datetime.min.time())
    fin_dia = inicio_dia + timedelta(days=1)

    cantidad_clientes = Cliente.query.filter_by(activo=True).count()
    cantidad_servicios = Servicio.query.filter_by(activo=True).count()

    turnos_hoy = Turno.query.filter(
        Turno.fecha_hora >= inicio_dia,
        Turno.fecha_hora < fin_dia,
        Turno.estado.in_(ESTADOS_ACTIVOS),
    ).order_by(Turno.fecha_hora).all()

    proximos_turnos = Turno.query.filter(
        Turno.fecha_hora >= ahora,
        Turno.estado.in_(ESTADOS_ACTIVOS),
    ).order_by(Turno.fecha_hora).limit(5).all()

    return render_template(
        "dashboard/index.html",
        cantidad_clientes=cantidad_clientes,
        cantidad_servicios=cantidad_servicios,
        turnos_hoy=turnos_hoy,
        proximos_turnos=proximos_turnos,
    )

app.register_blueprint(cliente_bp)
app.register_blueprint(servicio_bp)
app.register_blueprint(turnos_bp)