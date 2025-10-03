from src.service.ec2_service import *
from src.config import get_ec2_client, get_s3_client
from src.service import s3_service

def cli_ec2(ec2):
    while True:
        print("\n=== Gerenciamento de EC2 ===")
        print("1 - Criar instância")
        print("2 - Lista instâncias")
        print("3 - Buscar instância por ID")
        print("4 - Atualizar instância")
        print("5 - Deletar instância")
        print("0 - Sair")
        
        escolha = input("Escolha uma opcao: ")
        if escolha == "1":
            image_id = input("Digite o ID da AMI (pressione Enter para padrão) [padrão: ami-0c94855ba95c71c99]: ").strip() or "ami-0c94855ba95c71c99"
            instance_type = input("Digite o tipo da instância (Ex: t2.micro, t3.micro) [padrão: t3.micro]: ").strip() or "t3.micro"
            min_count = input("Digite a quantidade mínima de instâncias (padrão: 1): ").strip()
            min_count = int(min_count) if min_count.isdigit() and int(min_count) > 0 else 1
            max_count = input("Digite a quantidade máxima de instâncias (padrão: 1): ").strip()
            max_count = int(max_count) if max_count.isdigit() and int(max_count) >= min_count else min_count
            name = input("Digite o nome da instância (padrão: MinhaInstancia): ").strip() or "MinhaInstancia"
            add_ec2_instance(ec2, image_id, instance_type, min_count, max_count, name)

        elif escolha == "2":
            filter_choice = input("Deseja aplicar algum filtro? (y/n): ").strip().lower()
            if filter_choice == 'y':
                print("Filtros disponíveis:")
                print("1 - instâncias em execução")
                print("2 - instâncias paradas")
                print("3 - todas as instâncias")
                filter_option = input("Escolha um filtro (1, 2, 3): ").strip()
                if filter_option == '1':
                    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
                elif filter_option == '2':
                    filters = [{'Name': 'instance-state-name', 'Values': ['stopped']}]
                elif filter_option == '3':
                    filters = None
                else:
                    print("Opção de filtro inválida. Listando todas as instâncias.")
                    filters = None
            else:
                filters = None
            find_all_ec2_instances(ec2, filters)

        elif escolha == "3":
            instance_id = input("Digite o ID da instância: ").strip()
            find_ec2_instance(ec2, instance_id)

        elif escolha == "4":
            instance_id = input("Digite o ID da instância: ").strip()
            action = input("Digite a ação (start, stop, reboot): ").strip().lower()
            if action in ["start", "stop", "reboot"]:
                modify_ec2_instance(ec2, instance_id, action)
            else:
                print("Ação inválida. Use 'start', 'stop' ou 'reboot'.")

        elif escolha == "5":
            instance_id = input("Digite o ID da instância: ").strip()
            confirm = input(f"Tem certeza que deseja deletar a instância {instance_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                terminate_ec2_instance(ec2, instance_id)
            else:
                print("Operação de deleção cancelada.")
        
        elif escolha == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")



def cli_s3(s3):
    while True:
        print("\n=== Gerenciamento de S3 ===")
        print("1 - Criar Bucket")
        print("2 - Listar Buckets")
        print("3 - Fazer Upload de Arquivo")
        print("4 - Fazer Download de Arquivo")
        print("5 - Listar Objetos em um Bucket")
        print("6 - Deletar Objeto")
        print("7 - Deletar Bucket")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            bucket_name = input("Digite o nome do bucket: ").strip()
            if bucket_name:
                s3_service.create_bucket(s3, bucket_name)
            else:
                print("Nome do bucket não pode ser vazio.")

        elif escolha == "2":
            s3_service.list_buckets(s3)

        elif escolha == "3":
            bucket_name = input("Digite o nome do bucket: ").strip()
            file_path = input("Digite o caminho do arquivo local: ").strip()
            object_name = input("Digite o nome do objeto no S3 (ou deixe vazio para usar o nome do arquivo): ").strip() or None
            s3_service.upload_file(s3, bucket_name, file_path, object_name)

        elif escolha == "4":
            bucket_name = input("Digite o nome do bucket: ").strip()
            object_name = input("Digite o nome do objeto no S3: ").strip()
            file_path = input("Digite o caminho de destino local: ").strip()
            s3_service.download_file(s3, bucket_name, object_name, file_path)

        elif escolha == "5":
            bucket_name = input("Digite o nome do bucket: ").strip()
            prefix = input("Digite um prefixo (ou deixe vazio): ").strip() or None
            objects = s3_service.list_objects(s3, bucket_name, prefix)
            if not objects:
                print("Nenhum objeto encontrado.")
            else:
                print("\nObjetos:")
                for obj in objects:
                    print(f"- {obj['Key']} ({obj['Size']} bytes)")

        elif escolha == "6":
            bucket_name = input("Digite o nome do bucket: ").strip()
            object_name = input("Digite o nome do objeto: ").strip()
            confirm = input(f"Tem certeza que deseja deletar '{object_name}' de '{bucket_name}'? (y/n): ").strip().lower()
            if confirm == "y":
                s3_service.delete_object(s3, bucket_name, object_name)

        elif escolha == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")


def cli():
    ec2 = get_ec2_client()
    s3 = get_s3_client()

    print("Ola, bem vindo ao gerenciador de instancias EC2 e S3!")
    while True:
        print("\nEscolha uma das opcoes abaixo:")
        print("1 - Utilizar EC2")
        print("2 - Utilizar S3")
        print("0 - Sair")
        escolha = input("Escolha uma opcao: ")
        if escolha == "1":
            cli_ec2(ec2)
        elif escolha == "2":
            cli_s3(s3)
        elif escolha == "0":
            print("Saindo...")
            break
