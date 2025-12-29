from domain.deudas import Deudas
from extensions import ma, db
from marshmallow import fields, validate

from schemas.socio_schema import SocioSchema


class DeudasSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Deudas
        load_instance = True
        sqla_session = db.session

    idpagos_cuota = ma.auto_field(dump_only=True)
    monto = ma.Float(required=True, validate=validate.Range(min=0))
    cuit = ma.Nested(SocioSchema)


deuda_schema = DeudasSchema()
deudas_schema = DeudasSchema(many=True)