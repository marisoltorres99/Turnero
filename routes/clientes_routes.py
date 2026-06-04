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
        activo = True

        nuevo = Cliente(nombre=nombre, apellido=apellido, telefono=telefono, email=email)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("cliente.listar"))
    
    return render_template("clientes/form.html")

