from tools.add_data import procesar_archivos # Tu función de Pandas corregida
from services.db_service import guardar_datos_masivos

class SocioService:
    @staticmethod
    def procesar_carga_masiva(file_socios, file_deudas):
        try:
            # 1. Procesamiento (Pandas)
            # Esto devuelve el DataFrame con las columnas: cuit, nombre_apellido, telefono, monto_deuda
            df_limpio = procesar_archivos(file_socios, file_deudas)
            
            # Validación básica por si el Excel estaba vacío
            if df_limpio.empty:
                return {"status": "error", "message": "Los archivos procesados no generaron datos válidos."}

            # 2. Persistencia (MySQL Upsert)
            total_filas = guardar_datos_masivos(df_limpio)
            
            return {
                "status": "success", 
                "message": f"Proceso completado. Se procesaron {total_filas} registros.",
                "detalles": {
                    "total": total_filas,
                    "filas_con_deuda": len(df_limpio[df_limpio['monto_adeudado'] > 0])
                }
            }, None
            
        except ValueError as ve:
            # Errores de validación (columnas faltantes, etc.)
            return {"status": "error", "message": str(ve)}
        except Exception as e:
            # Errores inesperados de base de datos o código
            return {"status": "error", "message": f"Error interno: {str(e)}"}