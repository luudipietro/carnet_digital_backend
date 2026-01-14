import pandas as pd

def procesar_archivos(file_socios, file_deudas):
    # 1. Leer archivos (detecta si es CSV o Excel)
    df_socios = pd.read_excel(file_socios) if file_socios.filename.endswith('.xlsx') else pd.read_csv(file_socios)
    df_deudas = pd.read_excel(file_deudas) if file_deudas.filename.endswith('.xlsx') else pd.read_csv(file_deudas)

    # 2. Limpieza básica
    # Aseguramos que el CUIT sea tratado como string para evitar pérdida de ceros a la izquierda
    df_socios['cuit'] = df_socios['cuit'].astype(str)
    
    # 3. Cruce de datos (Merge)
    # Como el archivo de deudas no tiene CUIT, unimos por 'Nombre y Apellido'
    # NOTA: Esto requiere que los nombres escritos sean idénticos en ambos archivos
    df_final = pd.merge(df_socios, df_deudas, on='nombre_apellido', how='left')
    
    # Rellenamos con 0 a los que no tienen deuda
    df_final['monto_deuda'] = df_final['monto_deuda'].fillna(0)
    
    return df_final


# --- CLASE PARA SIMULAR EL OBJETO FILE DE FLASK ---
class MockFile:
    def __init__(self, path):
        self.path = path
        self.filename = path  # Aquí le damos la propiedad .filename que pide tu función

    def __getattr__(self, name):
        # Esto permite que pandas use read_excel/csv directamente sobre el path
        return self.path

# --- EJECUCIÓN DEL TEST ---
if __name__ == "__main__":
    # 1. Nombres de tus archivos reales
    archivo_clientes = "socios_reales.xlsx"  # <--- Cambia por tu nombre real
    archivo_deudas = "deudas_reales.csv"     # <--- Cambia por tu nombre real

    print(f"📂 Cargando {archivo_clientes} y {archivo_deudas}...")

    try:
        # Creamos los objetos simulados
        socio_mock = MockFile(archivo_clientes)
        deuda_mock = MockFile(archivo_deudas)

        # 2. LLAMADA A TU FUNCIÓN
        resultado = procesar_archivos(socio_mock, deuda_mock)

        # 3. MOSTRAR RESULTADOS
        print("\n✅ Procesamiento completado con éxito.")
        print("-" * 50)
        print(f"Total de registros resultantes: {len(resultado)}")
        
        # Ver cuántos socios tienen deuda mayor a 0
        con_deuda = resultado[resultado['monto_deuda'] > 0]
        print(f"Socios con deuda encontrada: {len(con_deuda)}")
        
        print("\n👀 Primeras 10 filas del resultado:")
        print(resultado[['cuit', 'nombre_apellido', 'monto_deuda']].head(10))

        # Opcional: Guardar el resultado en un Excel para revisar manualmente
        # resultado.to_excel("resultado_test.xlsx", index=False)

    except FileNotFoundError:
        print("❌ Error: No se encontraron los archivos. Verifica los nombres.")
    except Exception as e:
        print(f"❌ Error durante el test: {e}")