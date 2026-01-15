from flask import request
from flask_restful import Resource
from services.socios_service import SocioService
from . import api

class CargaMasivaResource(Resource):
    
    def post(self):
        # 1. Validación básica de la petición
        if 'socios' not in request.files:
            return {'message': 'Faltan un archivo requeridos (key: socios)'}, 400

        file_socios = request.files['socios']
        if 'deudas' in request.files:
            file_deudas = request.files['deudas']
            data, error = SocioService.procesar_carga_masiva(file_socios, file_deudas)

        # 2. Llamada al Servicio (Siguiendo tu patrón data, error)
        data, error = SocioService.procesar_carga_masiva(file_socios, None)

        # 3. Respuesta
        if error:
            # Si es un error de validación del usuario (400) o interno (500)
            # Aquí simplificamos a 400, pero podrías refinarlo
            return {'message': error}, 400
        
        return data, 201
    
api.add_resource(CargaMasivaResource, '/upload', endpoint='socios_upload')