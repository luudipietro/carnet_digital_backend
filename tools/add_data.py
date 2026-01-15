import pandas as pd

def procesar_archivos(file_socios, file_deudas):
    # 1. Lectura flexible de formato
    df_socios = pd.read_excel(file_socios) if file_socios.filename.endswith('.xlsx') else pd.read_csv(file_socios)
    df_deudas = pd.read_excel(file_deudas) if file_deudas.filename.endswith('.xlsx') else pd.read_csv(file_deudas)

    # 2. FUNCIÓN DE RENOMBRADO FLEXIBLE
    # Buscamos nombres parecidos y los estandarizamos
    def estandarizar_columnas(df, tipo):
        # Pasamos todos los nombres de columnas a minúsculas para comparar fácil
        cols = {c.lower().strip(): c for c in df.columns}
        nuevos_nombres = {}

        if tipo == 'socios':
            # Buscamos la columna del CUIT
            for c in cols:
                if 'cuit' in c or 'cuil' in c or 'documento' in c:
                    nuevos_nombres[cols[c]] = 'cuit'
                if 'nombre' in c or 'socio' in c or 'apellido' in c:
                    nuevos_nombres[cols[c]] = 'nombre_apellido'
                if 'tel' in c or 'celular' in c:
                    nuevos_nombres[cols[c]] = 'telefono'
        
        elif tipo == 'deudas':
            for c in cols:
                if 'nombre' in c or 'socio' in c or 'apellido' in c:
                    nuevos_nombres[cols[c]] = 'nombre_apellido'
                if 'deuda' in c or 'monto' in c or 'saldo' in c or 'importe' in c:
                    nuevos_nombres[cols[c]] = 'monto_deuda'
        
        return df.rename(columns=nuevos_nombres)

    # Aplicamos la flexibilidad
    df_socios = estandarizar_columnas(df_socios, 'socios')
    df_deudas = estandarizar_columnas(df_deudas, 'deudas')

    # 3. Limpieza de Datos (Normalización de Texto)
    # Convertimos a string, quitamos espacios y pasamos a MAYÚSCULAS
    df_socios['nombre_apellido'] = df_socios['nombre_apellido'].astype(str).str.strip().str.upper()
    df_deudas['nombre_apellido'] = df_deudas['nombre_apellido'].astype(str).str.strip().str.upper()
    
    # Limpiamos CUIT de posibles puntos o formatos científicos
    df_socios['cuit'] = df_socios['cuit'].astype(str).str.replace('.0', '', regex=False).str.replace('-', '', regex=False)

    # 4. Consolidación (Agrupar múltiples deudas del mismo socio)
    # Si 'JUAN PEREZ' tiene 3 deudas, las sumamos en una sola
    df_d_agrupado = df_deudas.groupby('nombre_apellido')['monto_deuda'].sum().reset_index()

    # 5. Cruce Final (Merge)
    # Unimos la tabla de socios con la tabla de deudas consolidada
    df_final = pd.merge(df_socios, df_d_agrupado, on='nombre_apellido', how='left')

    # Si un socio no tiene deuda, ponemos 0 en lugar de vacío (NaN)
    df_final['monto_deuda'] = df_final['monto_deuda'].fillna(0)

    # Retornamos solo las columnas que necesita nuestra base de datos
    return df_final[['cuit', 'nombre_apellido', 'telefono', 'monto_deuda']]