from sqlalchemy.dialects.mysql import insert
from sqlalchemy import text
from domain.socio import Socio # Importa tu modelo y tu objeto db
from extensions import db

def guardar_datos_masivos(df_final):
    # 1. Convertimos el DataFrame a una lista de diccionarios para SQLAlchemy
    # Orient='records' crea una lista: [{'cuit': '20...', 'nombre': 'Juan', ...}, {...}]
    datos = df_final.to_dict(orient='records')
    
    if not datos:
        return 0 # No hay datos para guardar

    # 2. Preparamos la sentencia INSERT
    tabla = Socio.__table__
    stmt = insert(tabla).values(datos)

    # 3. Configuramos la lógica "ON DUPLICATE KEY UPDATE"
    # Aquí definimos EXACTAMENTE lo que pediste:
    # Si el CUIT choca, SOLO actualizamos el monto_deuda. 
    # El nombre y teléfono originales se preservan.
    update_dict = {
        'monto_adeudado': stmt.inserted.monto_adeudado
        # Si quisieras actualizar también el nombre, agregarías:
        # 'nombre_apellido': stmt.inserted.nombre_apellido 
    }
    
    upsert_stmt = stmt.on_duplicate_key_update(**update_dict)

    # 4. Ejecutamos en una transacción segura
    try:
        with db.engine.begin() as conn:
            conn.execute(upsert_stmt)
            return len(datos)
    except Exception as e:
        raise e