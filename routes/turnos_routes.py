from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.turno import Turno
from models.cliente import Cliente
from models.servicio import Servicio
from models.estados_turno import EstadoTurno
from models.db import db

turnos_bp = Blueprint("turno", __name__, url_prefix="/turnos")

@turnos_bp.route("/")
def listar():
    turnos = Turno.query.all()
    return render_template("turnos/listado.html", turnos=turnos)

@turnos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        fecha_hora = datetime.strptime(request.form["fecha_hora"], "%Y-%m-%dT%H:%M")
        observaciones = request.form["observaciones"]
        cliente_id = request.form["cliente_id"]
        servicio_id = request.form["servicio_id"]

        nuevo = Turno(
            fecha_hora=fecha_hora,
            observaciones=observaciones,
            cliente_id=cliente_id,
            servicio_id=servicio_id,
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("turno.listar"))

    clientes = Cliente.query.filter_by(activo=True).all()
    servicios = Servicio.query.filter_by(activo=True).all()

    return render_template("turnos/form.html", clientes=clientes, servicios=servicios)

@turnos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    turno = db.session.get(Turno, id)

    if not turno:
        return "Turno no encontrado"

    if request.method == "POST":
        turno.fecha_hora = datetime.strptime(request.form["fecha_hora"], "%Y-%m-%dT%H:%M")
        turno.estado = request.form["estado"]
        turno.observaciones = request.form["observaciones"]
        turno.cliente_id = request.form["cliente_id"]
        turno.servicio_id = request.form["servicio_id"]

        db.session.commit()

        return redirect(url_for("turno.listar"))

    clientes = Cliente.query.filter_by(activo=True).all()
    servicios = Servicio.query.filter_by(activo=True).all()

    return render_template("turnos/form.html", turno=turno, clientes=clientes, servicios=servicios)

@turnos_bp.route("/cancelar/<int:id>", methods=["POST"])
def cancelar(id):
    turno = db.session.get(Turno, id)

    if not turno:
        abort(404)

    turno.estado = EstadoTurno.CANCELADO

    db.session.commit()

    return redirect(url_for("turno.listar"))

