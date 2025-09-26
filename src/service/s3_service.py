from src.repository import s3_repository as repo

def create_bucket(bucket_name: str):
    if not bucket_name or " " in bucket_name:
        raise ValueError("Nome do bucket inválido (não pode ter espaços).")
    return repo.create_bucket(bucket_name)

def upload_file(bucket_name: str, file_path: str, object_name: str = None):
    # Exemplo de regra extra: validar extensão
    if not file_path.endswith((".txt", ".csv", ".json", ".jpg", ".png")):
        raise ValueError("Extensão de arquivo não permitida.")
    return repo.upload_file(bucket_name, file_path, object_name)

def download_file(bucket_name: str, object_name: str, file_path: str):
    return repo.download_file(bucket_name, object_name, file_path)

def list_buckets():
    return repo.list_buckets()

def list_objects(bucket_name: str, prefix: str = None):
    return repo.list_objects(bucket_name, prefix)

def delete_object(bucket_name: str, object_name: str):
    return repo.delete_object(bucket_name, object_name)

def delete_bucket(bucket_name: str):
    # Exemplo: regra para impedir deletar bucket "producao"
    if bucket_name == "meu-bucket-producao":
        raise PermissionError("Bucket de produção não pode ser deletado!")
    return repo.delete_bucket(bucket_name)
