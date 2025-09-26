ALL_STATES = ["pending", "running", "stopping", "stopped", "shutting-down", "terminated"]

PREDEFINED_FILTERS = {
    "not-terminated": [
        {
            "Name": "instance-state-name",
            "Values": [state for state in ALL_STATES if state != "terminated"]
        }
    ],
    "running-only": [
        {
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]
}

from botocore.exceptions import ClientError
from src.repository.ec2_repository import (
    create_instance,
    get_instance,
    list_instances,
    update_instance,
    delete_instance
)

def add_ec2_instance(ec2, image_id, instance_type, min_count=1, max_count=1, name="MinhaInstancia"):
    try:
        success = create_instance(
            ec2=ec2,
            image_id=image_id,
            instance_type=instance_type,
            min_count=min_count,
            max_count=max_count,
            name=name
        )

        if success:
            print("Instância criada com sucesso!")

        else:
            print("Falha ao criar a instância.")

    except ClientError as e:
        print(f"Erro inesperado ao criar a instância:\n{e}")


def find_ec2_instance(ec2, instance_id):
    try:
        instance = get_instance(ec2, instance_id)

        if instance is None:
            print("Instância não encontrada.")
        
        else:
            # Pegar o nome da instância via tag 'Name'
            name_tag = "N/A"
            tags = instance.get('Tags', [])
            for tag in tags:
                if tag.get('Key') == 'Name':
                    name_tag = tag.get('Value', "N/A")
                    break
            
            instance_info = {
                "Name": name_tag,
                "InstanceId": instance.get("InstanceId", "N/A"),
                "State": instance.get("State", {}).get("Name", "N/A"),
                "InstanceType": instance.get("InstanceType", "N/A"),
                "AvailabilityZone": instance.get("Placement", {}).get("AvailabilityZone", "N/A"),
                "PublicIPv4": instance.get("PublicIpAddress", "N/A")
            }
            
            # Print dos atributos
            print("Nome da instância:", instance_info["Name"])
            print("ID da instância:", instance_info["InstanceId"])
            print("Estado da instância:", instance_info["State"])
            print("Tipo de instância:", instance_info["InstanceType"])
            print("Zona de disponibilidade:", instance_info["AvailabilityZone"])
            print("IPv4 público:", instance_info["PublicIPv4"])
        
    except ClientError as e:
        print(f"Erro ao buscar a instância:\n{e}")

    
def find_all_ec2_instances(ec2, filter=None):
    try:
        # Verifica se filter é uma chave em PREDEFINED_FILTERS
        if isinstance(filter, str):
            applied_filter = PREDEFINED_FILTERS.get(filter, None)
        else:
            applied_filter = filter

        instances = list_instances(ec2, applied_filter)

        if not instances:
            print("Nenhuma instância encontrada com os filtros fornecidos.")

        for instance in instances:
            # Pegar o nome da instância via tag 'Name'
            name_tag = "N/A"
            tags = instance.get('Tags', [])
            for tag in tags:
                if tag.get('Key') == 'Name':
                    name_tag = tag.get('Value', "N/A")
                    break

            info = {
                "Name": name_tag,
                "InstanceId": instance.get("InstanceId", "N/A"),
                "State": instance.get("State", {}).get("Name", "N/A"),
                "InstanceType": instance.get("InstanceType", "N/A"),
                "AvailabilityZone": instance.get("Placement", {}).get("AvailabilityZone", "N/A"),
                "PublicIPv4": instance.get("PublicIpAddress", "N/A")
            }

            # Print dos atributos
            print("Nome da instância:", info["Name"])
            print("ID da instância:", info["InstanceId"])
            print("Estado da instância:", info["State"])
            print("Tipo de instância:", info["InstanceType"])
            print("Zona de disponibilidade:", info["AvailabilityZone"])
            print("DNS/IPv4 público:", info["PublicIPv4"])
            print("-" * 40)

    except ClientError as e:
        print(f"Erro ao listar instâncias:\n{e}")


def modify_ec2_instance(ec2, instance_id, action):
    try:
        response = update_instance(ec2, instance_id, action)

        if response is None:
            print(f"Falha ao executar ação '{action}' na instância.")

        # Mensagem amigável de acordo com a ação
        action_messages = {
            "start": "Iniciada",
            "stop": "Parada",
            "reboot": "Reiniciada"
        }
        message = action_messages.get(action, "Atualizada")

        print(f"Instância {message} com sucesso!")

    except ValueError as ve:
        print(f"Erro ao executar ação '{action}' na instância:\n{ve}")

    except ClientError as e:
        print(f"Erro ao executar ação '{action}' na instância:\n{e}")

def terminate_ec2_instance(ec2, instance_id):
    if not instance_id:
        print("Nenhum ID de instância fornecido.")

    try:
        result = delete_instance(ec2, instance_id)
        if result:
            print(f"Instância solicitada para término com sucesso.")

    except Exception as e:
        # Aqui você pode logar de forma mais detalhada ou notificar outro sistema
        print(f"Erro ao terminar a instância:\n{e}")
