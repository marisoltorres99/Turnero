from .db import db
from .estados_turno import EstadoTurno

class Turno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=EstadoTurno.PENDIENTE)
    observaciones = db.Column(db.Text, nullable=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicio.id"), nullable=False)