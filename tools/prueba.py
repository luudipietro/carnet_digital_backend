import os
import traceback
import pandas as pd
from unittest.mock import MagicMock

# --- IMPORTACIÓN DINÁMICA ---
# Importamos la función desde tu archivo real. 
# Cambia 'helpers' por el nombre de tu archivo .py
from add_data import procesar_archivos 

def test_con_archivos_reales():
    # 1. Configura las rutas a tus archivos locales
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Unimos la carpeta con el nombre del archivo
    PATH_SOCIOS = os.path.join(BASE_DIR, "clientes.xlsx")
    PATH_DEUDAS = os.path.join(BASE_DIR, "deudas.xlsx")

    if not os.path.exists(PATH_SOCIOS) or not os.path.exists(PATH_DEUDAS):
        print("❌ Error: Los archivos reales no se encuentran en la carpeta.")
        return

    print(f"🚀 Probando función importada con: {PATH_SOCIOS} y {PATH_DEUDAS}")

    try:
        # 2. Creamos "Mocks" que simulan el objeto de Flask
        # Esto engaña a la función para que crea que recibe un objeto con .filename
        file_s_mock = MagicMock()
        file_s_mock.file_path = PATH_SOCIOS
        
        file_d_mock = MagicMock()
        file_d_mock.file_path = PATH_DEUDAS

        # 3. LLAMADA A LA FUNCIÓN REAL
        # Aquí se ejecuta el código que tienes en tu archivo de proyecto
        resultado = procesar_archivos(file_s_mock, file_d_mock)

        # 4. Reporte de resultados
        print("\n✅ EJECUCIÓN COMPLETADA")
        print("--------------------------------------------------")
        print(f"Filas procesadas: {len(resultado)}")
        print(f"Deudas vinculadas: {len(resultado[resultado['monto_deuda'] > 0])}")
        
        print("\n--- Vista Previa ---")
        print(resultado.head(80))

        # Verificación de columnas resultantes
        columnas_esperadas = ['cuit', 'nombre_apellido', 'telefono', 'monto_deuda']
        if all(col in resultado.columns for col in columnas_esperadas):
            print("\n💎 Estructura de columnas: CORRECTA")
        else:
            print("\n⚠️ Estructura de columnas: INCORRECTA")

    except Exception as e:
        print(f"\n💥 Error al ejecutar la función importada: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_con_archivos_reales()