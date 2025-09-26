from src.service.ec2_service import *
from src.config import get_ec2_client

def cli_ec2(ec2):
    while True:
        print("Escolha uma das opcoes abaixo:")
        print("1 - Criar instância")
        print("2 - Lista instância")
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
            return


def cli_s3():
    pass

def cli():
    ec2 = get_ec2_client()
    print("Ola, bem vindo ao gerenciador de instancias EC2 e S3!")
    while True:
        print("Escolha uma das opcoes abaixo:")
        print("1 - Utilizar EC2")
        print("2 - Utilizar S3")
        print("0 - Sair")
        escolha = input("Escolha uma opcao: ")
        if escolha == "1":
            cli_ec2(ec2)
        elif escolha == "2":
            cli_s3()
        elif escolha == "0":
            print("Saindo...")
            return
