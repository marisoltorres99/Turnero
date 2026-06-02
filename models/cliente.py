from .db import db

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    turnos = db.relationship("Turno", backref="cliente", lazy=True)