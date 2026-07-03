from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.turno import Turno
from models.db import db

turnos_bp = Blueprint("turno", __name__, url_prefix="/turnos")

@turnos_bp.route("/")
def listar():
    turnos = Turno.query.all()
    return render_template("turnos/listado.html", turnos=turnos)

@turnos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        fecha_hora = request.form["fecha_hora"]
        observaciones = request.form["observaciones"]

        nuevo = Turno(fecha_hora=fecha_hora, observaciones=observaciones)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("turno.listar"))
    
    return render_template("turnos/form.html")

@turnos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    turno = db.session.get(Turno, id)

    if not turno:
        return "Turno no encontrado"

    if request.method == "POST":
        turno.fecha_hora = request.form["fecha_hora"]
        turno.estado = request.form["estado"]
        turno.observaciones = request.form["observaciones"]

        db.session.commit()

        return redirect(url_for("turno.listar"))

    return render_template("turnos/form.html", turno=turno)

