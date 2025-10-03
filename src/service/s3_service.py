from src.repository import s3_repository as repo
import os

def create_bucket(s3, bucket_name):
    if not bucket_name or " " in bucket_name:
        raise ValueError("Nome do bucket inválido (não pode ter espaços).")
    sucess = repo.create_bucket(s3, bucket_name)
    if sucess:
        print("Bucket criado com sucesso!")
    else:
        print("Falha ao criar o bucket.")
    return 


def list_buckets(s3):
    buckets = repo.list_buckets(s3)
    if buckets:
        print("\nBuckets existentes:")
        for b in buckets:
            print(f"- {b['Name']}")
    elif not buckets:
        print("Nenhuma bucket encontrado.")


def delete_bucket(s3, bucket_name):
    # Exemplo: regra para impedir deletar bucket "producao"
    if bucket_name == "meu-bucket-producao":
        raise PermissionError("Bucket de produção não pode ser deletado!")
    sucess = repo.delete_bucket(s3, bucket_name)
    if sucess:
        print(f"Bucket deletado com sucesso.")
    else:
        print("Não foi possível deletar o bucket.")


def upload_file(s3, bucket_name, file_path, object_name = None):
    # Se object_name não for informado, usa o nome do arquivo original
    if object_name is None:
        object_name = os.path.basename(file_path)
        
    # Exemplo de regra extra: validar extensão
    if not file_path.endswith((".txt", ".csv", ".json", ".jpg", ".png")):
        print("Extensão de arquivo não permitida.")
        return
    
    # Verificação do arquivo
    if not os.path.isfile(file_path):
        print("Arquivo não encontrado.")
        return
    
    response = repo.list_buckets(s3)
    buckets = [b["Name"] for b in response] 
    if (bucket_name in buckets):
        if repo.upload_file(s3, bucket_name, file_path, object_name):
            print("Arquivo enviado com sucesso.")
    else:
        print("Bucket não encontrado.")


def list_objects(s3, bucket_name, prefix = None):
    return repo.list_objects(s3, bucket_name, prefix)


def download_file(s3, bucket_name, object_name, file_path):
    return repo.download_file(s3, bucket_name, object_name, file_path)


def delete_object(s3, bucket_name, object_name):
    return repo.delete_object(s3, bucket_name, object_name)
