from domain.socio import Socio
from extensions import ma, db
from marshmallow import fields, validate

class SocioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Socio
        load_instance = True
        sqla_session = db.session

    cuit = ma.auto_field(required=True, validate=validate.Length(min=1, max=14))
    nombre = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    telefono = ma.auto_field(validate=validate.Length(min=1, max=45))
    monto_adeudado = ma.auto_field(required= True, validate=validate.Range(min=0))
    estado = fields.String()



socio_schema = SocioSchema()
socios_schema = SocioSchema(many=True)