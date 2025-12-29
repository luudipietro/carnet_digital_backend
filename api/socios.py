from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.deuda_socio_service import ServicioDeuda

from . import api

class SociosResource(Resource):

    def get(self, id):
        data, error = ServicioDeuda.obtener_estado_deuda(id)

        if error:
            return {'message': error}, 404
        return data, 200

api.add_resource(SociosResource, '/socios/<string:id>', endpoint='socios_id')



