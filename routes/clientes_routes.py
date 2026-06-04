from flask import Blueprint, render_template, request, redirect, url_for
from models.cliente import Cliente
from models.db import db

cliente_bp = Blueprint("cliente", __name__, url_prefix="/clientes")

@cliente_bp.route("/")
def listar():
    clientes = Cliente.query.all()
    return render_template("clientes/listado.html", clientes=clientes)

@cliente_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        nuevo = Cliente(nombre=nombre, apellido=apellido, telefono=telefono, email=email)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("cliente.listar"))
    
    return render_template("clientes/form.html")

@cliente_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    cliente = db.session.get(Cliente, id)

    if not cliente:
        return "Cliente no encontrado"

    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.apellido = request.form["apellido"]
        cliente.telefono = request.form["telefono"]
        cliente.email = request.form["email"]

        db.session.commit()

        return redirect(url_for("cliente.listar"))

    return render_template("clientes/form.html", cliente=cliente)

@cliente_bp.route("/desactivar/<int:id>", methods=["POST"])
def desactivar(id):
    cliente = db.session.get(Cliente, id)

    if not cliente:
        return "Cliente no encontrado"

    cliente.activo = False

    db.session.commit()

    return redirect(url_for("cliente.listar"))

@cliente_bp.route("/activar/<int:id>", methods=["POST"])
def activar(id):
    cliente = db.session.get(Cliente, id)

    if not cliente:
        return "Cliente no encontrado"

    cliente.activo = True

    db.session.commit()

    return redirect(url_for("cliente.listar"))

