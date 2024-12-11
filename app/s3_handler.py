import boto3
from botocore.exceptions import ClientError
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME
from fastapi import UploadFile
import io

class S3Handler:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        self.bucket_name = AWS_BUCKET_NAME

    async def upload_file(self, file: UploadFile):
        try:
            contents = await file.read()
            self.s3.put_object(Bucket=self.bucket_name, Key=file.filename, Body=contents)
            print(f"Archivo {file.filename} subido exitosamente a {self.bucket_name}")
            return True
        except ClientError as e:
            print(f"Error al subir el archivo a S3: {e}")
            return False

    async def download_file(self, file_name: str):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
            return response['Body'].read()
        except ClientError as e:
            print(f"Error al descargar el archivo de S3: {e}")
            raise e

# Asegúrate de que esta línea esté al final del archivo
__all__ = ['S3Handler']


