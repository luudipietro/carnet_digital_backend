
# from extensions import db
# from sqlalchemy import Numeric



# class Deudas(db.Model):

#     __tablename__ = 'deudas'

#     idpagos_cuota = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     monto_adeudado = db.Column(db.Numeric(10,2), nullable= False)
#     socio_cuit = db.Column(db.String(14), db.ForeignKey('socio.cuit'))
