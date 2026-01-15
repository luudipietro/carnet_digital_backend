import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURACIÓN ---
# Si quieres ver el resultado en la BD, pon tus credenciales aquí. 
# Si solo quieres probar la lógica, deja comentada la parte de SQL.
# engine = create_engine('mysql+mysqlconnector://usuario:pass@localhost/tu_bd')

# Cambia estos nombres por los nombres exactos de tus archivos reales
FILE_SOCIOS = "mis_clientes.xlsx" 
FILE_DEUDAS = "mis_deudas.csv"

def probar_con_archivos_reales():
    print("🚀 Iniciando prueba con archivos reales...")

    try:
        # 1. Cargar archivos
        df_s = pd.read_excel(FILE_SOCIOS) if FILE_SOCIOS.endswith('.xlsx') else pd.read_csv(FILE_SOCIOS)
        df_d = pd.read_excel(FILE_DEUDAS) if FILE_DEUDAS.endswith('.xlsx') else pd.read_csv(FILE_DEUDAS)

        print(f"📊 Socios cargados: {len(df_s)} filas")
        print(f"📊 Deudas cargadas: {len(df_d)} filas")

        # 2. Limpieza de nombres (Crucial para archivos reales)
        # Pasamos a mayúsculas y quitamos espacios para asegurar que "JUAN PEREZ" coincida con "juan perez "
        df_s['nombre_apellido'] = df_s['nombre_apellido'].astype(str).str.strip().str.upper()
        df_d['nombre_apellido'] = df_d['nombre_apellido'].astype(str).str.strip().str.upper()

        # 3. El Cruce (Merge)
        # Intentamos unir las deudas con los socios usando el nombre
        df_final = pd.merge(df_s, df_d, on='nombre_apellido', how='left')
        df_final['monto_deuda'] = df_final['monto_deuda'].fillna(0)

        # 4. Verificaciones de calidad
        socios_con_deuda = df_final[df_final['monto_deuda'] > 0]
        
        print("\n--- ANÁLISIS DE RESULTADOS ---")
        print(f"✅ Total de socios procesados: {len(df_final)}")
        print(f"💰 Socios con deuda detectada: {len(socios_con_deuda)}")
        
        # 5. Detectar posibles errores (Nombres que están en deudas pero no en socios)
        errores = df_d[~df_d['nombre_apellido'].isin(df_s['nombre_apellido'])]
        if not errores.empty:
            print("\n⚠️ ALERTA: Hay nombres en el archivo de DEUDAS que no existen en el de SOCIOS:")
            print(errores['nombre_apellido'].unique()[:10]) # Muestra los primeros 10
            print(f"Total de nombres no encontrados: {len(errores)}")

        # 6. Mostrar previsualización
        print("\n--- VISTA PREVIA DE LOS DATOS A CARGAR ---")
        print(df_final[['cuit', 'nombre_apellido', 'monto_deuda']].head(10))

    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    probar_con_archivos_reales()    
    print("cambioTonto")