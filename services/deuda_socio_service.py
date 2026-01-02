from domain.deudas import Deudas
from schemas.resumen_deuda import resumen_schema

class ServicioDeuda:

    @staticmethod
    def obtener_estado_deuda(deuda_id):
        if len(deuda_id) <= 8:
            deuda = Deudas.query.filter(Deudas.socio_cuit.like(f'%-{deuda_id}-%')).first()
        else:
            deuda = Deudas.query.filter_by(socio_cuit=deuda_id).first() #usamos el cuit

        if not deuda:
            return None, 'Socio no encontrado'

        socio = deuda.socio

        data = {
            'cuit':socio.cuit,
            'nombre':socio.nombre,
            'monto_adeudado':deuda.monto_adeudado,
            'estado' : 'Inactivo' if deuda.monto_adeudado > 0 else 'Activo'

        }

        return resumen_schema.dump(data), None