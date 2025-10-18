import functions_framework
import mysql.connector as connection
from google.cloud import storage
import pandas as pd
import io
import csv

# Nombre del bucket de destino en la capa RAW
BUCKET_DESTINO = "dl-csantoyo-raw"

# Lista de tablas a migrar
TABLAS_A_MIGRAR = ["customers", "employees", "offices", "orders", "payments", "productlines", "products"]

@functions_framework.http
def mysqltobq(request):
    request_args = request.args
    tabla = request_args.get('tbl')

    if not tabla:
        return "El parámetro 'tbl' es necesario para la ingesta.", 400

    if tabla == "all":
        for t in TABLAS_A_MIGRAR:
            print(f"Iniciando ingesta de la tabla {t} a Cloud Storage")
            _ejecutar_ingesta(t)
            print(f"Ingesta de {t} completada.")
        return "ok"
    else:
        print(f"Iniciando ingesta de la tabla {tabla} a Cloud Storage")
        _ejecutar_ingesta(tabla)
        print(f"Ingesta de {tabla} completada.")
        return "ok"


def _ejecutar_ingesta(tabla):
    try:
        mydb = connection.connect(
            host="34.16.150.20",
            user="dataurp",
            passwd="Heissen@09",
            database="csantoyo"
        )
        cursor = mydb.cursor()
        query = f"select * from csantoyo.{tabla}"
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        mydb.close()
        
        result_df = pd.DataFrame(rows, columns=columns)
        
        #Limpiar saltos de línea y puntos y coma de las columnas de texto
        if 'productDescription' in result_df.columns:
            result_df['productDescription'] = result_df['productDescription'].str.replace(r'[\r\n;]+', ' ', regex=True)
        if 'textDescription' in result_df.columns:
            result_df['textDescription'] = result_df['textDescription'].str.replace(r'[\r\n;]+', ' ', regex=True)
            
        #Convertir salesRepEmployeeNumber a tipo entero si existe
        if 'salesRepEmployeeNumber' in result_df.columns:
            result_df['salesRepEmployeeNumber'] = result_df['salesRepEmployeeNumber'].astype(pd.Int64Dtype())

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_DESTINO)
        
        blob = bucket.blob(f"mysql_data/{tabla}.csv")
        
        with io.BytesIO() as buffer:
            result_df.to_csv(buffer, sep=',', index=False, quoting=csv.QUOTE_ALL)
            buffer.seek(0)
            
            blob.upload_from_file(buffer, content_type='text/csv')
            
    except Exception as e:
        print(f"Error en la ingesta para la tabla {tabla}: {e}")
        raise e