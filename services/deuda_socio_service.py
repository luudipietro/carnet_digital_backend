from domain.socio import Socio
from schemas.socio_schema import SocioSchema

class ServicioDeuda:

    @staticmethod
    def obtener_estado_deuda(deuda_id):
        if len(deuda_id) <= 8:
            socio = Socio.query.filter(Socio.cuit.like(f'%{deuda_id}%')).first()
        else:
            socio = Socio.query.filter_by(cuit=deuda_id).first() #usamos el cuit

        if not socio:
            return None, 'Socio no encontrado'

        
        data = {
            'cuit':socio.cuit,
            'nombre':socio.nombre,
            'estado' : 'Inactivo' if socio.monto_adeudado > 8000 else 'Activo'

        }

        return SocioSchema(only=('cuit', 'nombre', 'estado')).dump(data), None