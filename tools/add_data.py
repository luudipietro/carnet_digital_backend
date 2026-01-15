import pandas as pd

def procesar_archivos(file_socios, file_deudas):
    # Verificamos si los archivos vienen con una ruta física (para el test)
    # o si son el objeto directo (para Flask)
    path_s = getattr(file_socios, 'file_path', file_socios)
    
    # 1. Lectura flexible de formato
    df_socios = pd.read_excel(path_s) if file_socios.filename.endswith('.xlsx') else pd.read_csv(path_s)
    

    


    # 2. FUNCIÓN DE RENOMBRADO FLEXIBLE
    # Buscamos nombres parecidos y los estandarizamos
    def estandarizar_columnas(df, tipo):
        # Pasamos todos los nombres de columnas a minúsculas para comparar fácil
        cols = {c.lower().strip(): c for c in df.columns}
        nuevos_nombres = {}

        encontrados = set()

        if tipo == 'socios':
            # Buscamos la columna del CUIT
            for c in cols:
                if 'cuit' not in encontrados and any(x in c for x in ['cuit' ,'cuil' ,'documento' ,'dni']):
                    nuevos_nombres[cols[c]] = 'cuit'
                    encontrados.add('cuit')
                # if 'nombre' == c:
                if 'nombre' not in encontrados and any(x in c for x in ['cliente' ,'nombre' ,'socio' ,'apellido']):
                    nuevos_nombres[cols[c]] = 'nombre'
                    encontrados.add('nombre')
                if 'telefono' not in encontrados and any(x in c for x in ['tel' ,'telefono' ,'cel' ,'celular']):
                    nuevos_nombres[cols[c]] = 'telefono'
                    encontrados.add('telefono')
        
        elif tipo == 'deudas':
            for c in cols:
                if 'nombre' not in encontrados and c =='cliente':
                    nuevos_nombres[cols[c]] = 'nombre'
                    encontrados.add('nombre')
                if 'monto_adeudado' not in encontrados and c == 'importe mon. ppal.':
                    nuevos_nombres[cols[c]] = 'monto_adeudado'
                    encontrados.add('monto_deuda')
        
        return df.rename(columns=nuevos_nombres)

    # Aplicamos la flexibilidad
    df_socios = estandarizar_columnas(df_socios, 'socios')

    df_socios['nombre'] = df_socios['nombre'].astype(str).str.strip().str.upper()

    df_socios['cuit'] = df_socios['cuit'].astype(str).str.replace('.0', '', regex=False)

    if file_deudas:
        path_d = getattr(file_deudas, 'file_path', file_deudas)
        df_deudas = pd.read_excel(path_d) if file_deudas.filename.endswith('.xlsx') else pd.read_csv(path_d)
        df_deudas = estandarizar_columnas(df_deudas, 'deudas')
        
        df_deudas['nombre'] = df_deudas['nombre'].astype(str).str.strip().str.upper()
        
        
        df_d_agrupado = df_deudas.groupby('nombre')['monto_adeudado'].sum().reset_index()

        # 5. Cruce Final (Merge)
        # Unimos la tabla de socios con la tabla de deudas consolidada
        df_final = pd.merge(df_socios, df_d_agrupado, on='nombre', how='left')
        
    
    else:
        df_final = df_socios
        df_final['monto_adeudado'] = None

    # Si un socio no tiene deuda, ponemos 0 en lugar de vacío (NaN)
    df_final['monto_adeudado'] = df_final['monto_adeudado'].fillna(0)

    # Retornamos solo las columnas que necesita nuestra base de datos
    return df_final[['cuit', 'nombre', 'telefono', 'monto_adeudado']]