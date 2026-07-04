from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.turno import Turno
from models.cliente import Cliente
from models.servicio import Servicio
from models.estados_turno import EstadoTurno
from models.db import db

turnos_bp = Blueprint("turno", __name__, url_prefix="/turnos")

ESTADOS_ACTIVOS = (EstadoTurno.PENDIENTE, EstadoTurno.CONFIRMADO)

def _verificar_superposicion(fecha_hora, cliente_id, servicio_id, turno_id=None):
    cliente_id = int(cliente_id)
    servicio_id = int(servicio_id)

    query = Turno.query.filter(
        Turno.fecha_hora == fecha_hora,
        Turno.estado.in_(ESTADOS_ACTIVOS),
    )
    if turno_id is not None:
        query = query.filter(Turno.id != turno_id)

    if query.filter(Turno.servicio_id == servicio_id).first():
        return "Ya hay un turno pendiente o confirmado para ese servicio en esa fecha y hora."

    if query.filter(Turno.cliente_id == cliente_id).first():
        return "El cliente ya tiene un turno pendiente o confirmado en esa fecha y hora."

    return None

@turnos_bp.route("/")
def listar():
    turnos = Turno.query.all()
    return render_template("turnos/listado.html", turnos=turnos)

@turnos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    clientes = Cliente.query.filter_by(activo=True).all()
    servicios = Servicio.query.filter_by(activo=True).all()

    if request.method == "POST":
        fecha_hora = datetime.strptime(request.form["fecha_hora"], "%Y-%m-%dT%H:%M")
        observaciones = request.form["observaciones"]
        cliente_id = request.form["cliente_id"]
        servicio_id = request.form["servicio_id"]

        error = _verificar_superposicion(fecha_hora, cliente_id, servicio_id)
        if error:
            return render_template(
                "turnos/form.html", clientes=clientes, servicios=servicios, error=error,
            )

        nuevo = Turno(
            fecha_hora=fecha_hora,
            observaciones=observaciones,
            cliente_id=cliente_id,
            servicio_id=servicio_id,
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("turno.listar"))

    return render_template("turnos/form.html", clientes=clientes, servicios=servicios)

@turnos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    turno = db.session.get(Turno, id)

    if not turno:
        return "Turno no encontrado"

    clientes = Cliente.query.filter_by(activo=True).all()
    servicios = Servicio.query.filter_by(activo=True).all()

    if request.method == "POST":
        fecha_hora = datetime.strptime(request.form["fecha_hora"], "%Y-%m-%dT%H:%M")
        estado = request.form["estado"]
        cliente_id = request.form["cliente_id"]
        servicio_id = request.form["servicio_id"]

        if estado in ESTADOS_ACTIVOS:
            error = _verificar_superposicion(fecha_hora, cliente_id, servicio_id, turno_id=turno.id)
            if error:
                turno.fecha_hora = fecha_hora
                turno.estado = estado
                turno.observaciones = request.form["observaciones"]
                turno.cliente_id = cliente_id
                turno.servicio_id = servicio_id
                return render_template(
                    "turnos/form.html", turno=turno, clientes=clientes, servicios=servicios, error=error,
                )

        turno.fecha_hora = fecha_hora
        turno.estado = estado
        turno.observaciones = request.form["observaciones"]
        turno.cliente_id = cliente_id
        turno.servicio_id = servicio_id

        db.session.commit()

        return redirect(url_for("turno.listar"))

    return render_template("turnos/form.html", turno=turno, clientes=clientes, servicios=servicios)

@turnos_bp.route("/cancelar/<int:id>", methods=["POST"])
def cancelar(id):
    turno = db.session.get(Turno, id)

    if not turno:
        abort(404)

    turno.estado = EstadoTurno.CANCELADO

    db.session.commit()

    return redirect(url_for("turno.listar"))

