import functions_framework
from google.cloud import storage
import pandas as pd
import io

@functions_framework.cloud_event
def ingestadata(cloudevent):
    event_data = cloudevent.data
    bucket_name = event_data['bucket']
    file_name = event_data['name']

    if file_name != "orderdetails.csv":
        print(f"Archivo {file_name} no es el objetivo, omitiendo.")
        return

    client_storage = storage.Client()
    source_bucket = client_storage.bucket(bucket_name)
    source_blob = source_bucket.blob(file_name)
    
    csv_bytes = source_blob.download_as_bytes()
    
    df = pd.read_csv(
        io.BytesIO(csv_bytes),
        sep=';'
    )
    
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='raise')
        except (ValueError, TypeError):
            pass

    dest_bucket_name = "dl-csantoyo-raw"
    dest_file_name = f"orderdetails/{file_name}"
    dest_bucket = client_storage.bucket(dest_bucket_name)
    
    csv_processed_bytes = io.BytesIO()
    df.to_csv(csv_processed_bytes, index=False, header=True, sep=';')
    csv_processed_bytes.seek(0)

    dest_blob = dest_bucket.blob(dest_file_name)
    dest_blob.upload_from_file(csv_processed_bytes, content_type='text/csv')
    
    print(f"Archivo {file_name} procesado y guardado en gs://{dest_bucket_name}/{dest_file_name}")