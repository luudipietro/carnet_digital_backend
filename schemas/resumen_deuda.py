from extensions import ma
from marshmallow import fields
class ResumenDeudaSchema(ma.SQLAlchemySchema):
    cuit = fields.String()
    nombre = fields.String()
    # Marshmallow se encarga de transformar el Decimal a Float aquí
    monto_adeudado = fields.Float()
    estado = fields.String()

resumen_schema = ResumenDeudaSchema()
