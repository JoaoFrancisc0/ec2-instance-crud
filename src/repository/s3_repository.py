import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3", region_name="us-east-1")

def create_bucket(bucket_name): 
    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "us-east-1"}
        )
        return response
    except ClientError as e:
        print(f"Erro ao criar bucket {bucket_name}: {e}")
        return None

def list_buckets():
    try:
        response = s3.list_buckets()
        return response.get("Buckets", [])
    except ClientError as e:
        print(f"Erro ao listar buckets: {e}")
        return []

def upload_file(bucket_name, file_path, object_name=None):
    try:
        if object_name is None:
            object_name = file_path
        s3.upload_file(file_path, bucket_name, object_name)
        return True
    except ClientError as e:
        print(f"Erro ao fazer upload para {bucket_name}: {e}")
        return False

def download_file(bucket_name, object_name, file_path):
    try:
        s3.download_file(bucket_name, object_name, file_path)
        return True
    except ClientError as e:
        print(f"Erro ao baixar {object_name} de {bucket_name}: {e}")
        return False

def list_objects(bucket_name, prefix=None):
    try:
        params = {"Bucket": bucket_name}
        if prefix:
            params["Prefix"] = prefix
        response = s3.list_objects_v2(**params)
        return response.get("Contents", [])
    except ClientError as e:
        print(f"Erro ao listar objetos em {bucket_name}: {e}")
        return []

def delete_object(bucket_name, object_name):
    try:
        return s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        print(f"Erro ao deletar {object_name} de {bucket_name}: {e}")
        return None

def delete_bucket(bucket_name):
    try:
        return s3.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        print(f"Erro ao deletar bucket {bucket_name}: {e}")
        return None
