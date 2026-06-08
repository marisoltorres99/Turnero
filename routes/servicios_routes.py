from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.servicio import Servicio
from models.db import db

servicio_bp = Blueprint("servicio", __name__, url_prefix="/servicios")

@servicio_bp.route("/")
def listar():
    servicios = Servicio.query.all()
    return render_template("servicios/listado.html", servicios=servicios)

@servicio_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        duracion_minutos = request.form["duracion_minutos"]
        precio = request.form["precio"]

        nuevo = Servicio(nombre=nombre, duracion_minutos=duracion_minutos, precio=precio)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("servicio.listar"))
    
    return render_template("servicios/form.html")

@servicio_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    servicio = db.session.get(Servicio, id)

    if not servicio:
        return "Cliente no encontrado"

    if request.method == "POST":
        servicio.nombre = request.form["nombre"]
        servicio.duracion_minutos = request.form["duracion_minutos"]
        servicio.precio = request.form["precio"]

        db.session.commit()

        return redirect(url_for("servicio.listar"))

    return render_template("servicios/form.html", servicio=servicio)

@servicio_bp.route("/desactivar/<int:id>", methods=["POST"])
def desactivar(id):
    servicio = db.session.get(Servicio, id)

    if not servicio:
        abort(404)

    servicio.activo = False

    db.session.commit()

    return redirect(url_for("servicio.listar"))

@servicio_bp.route("/activar/<int:id>", methods=["POST"])
def activar(id):
    servicio = db.session.get(Servicio, id)

    if not servicio:
        abort(404)

    servicio.activo = True

    db.session.commit()

    return redirect(url_for("servicio.listar"))

