from .db import db

class Servicio(db.Model):
    __tablename__ = "servicio"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion_minutos = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    turnos = db.relationship("Turno", backref="servicio", lazy=True)