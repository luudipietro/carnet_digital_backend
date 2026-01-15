from enum import unique

from sqlalchemy.orm import backref

from extensions import db
from sqlalchemy import Numeric

class Socio(db.Model):
    __tablename__ = "socio"

    cuit = db.Column(db.String(14), primary_key=True, nullable=False, unique=True)
    nombre =db.Column(db.String(100), nullable = False)
    telefono = db.Column(db.String(45))
    monto_adeudado = db.Column(db.Numeric(10,2), nullable=False)
    

    def __repr__(self) -> str:
        return f'<Socio {self.cuit} - {self.nombre}'