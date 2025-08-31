from src import ClientError, get_ec2_client

# Inicializa o cliente EC2
ec2 = get_ec2_client()

def criar_instancia(nome):
    try:
        instancia = ec2.run_instances(
            ImageId='ami-0c94855ba95c71c99',
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': nome}]
            }]
        )
        print(f"Instância criada: {instancia['Instances'][0]['InstanceId']}")
    except ClientError as e:
        print(f"Erro ao criar instância: {e}")


def listar_instancias():
    try:
        response = ec2.describe_instances()
        instancias_info = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                tags = 'N/A'
                if 'Tags' in instance:
                    tags = ', '.join([f"{tag['Key']}={tag['Value']}" for tag in instance['Tags']])

                info = {
                    'ID': instance['InstanceId'],
                    'Status': instance['State']['Name'],
                    'IP Público': instance.get('PublicIpAddress', 'N/A'),
                    'Tags': tags
                }
                instancias_info.append(info)

        if (instancias_info):
            num_instancias = len(instancias_info)
            if (num_instancias > 1):
                print(f'{num_instancias} instâncias encontradas: ')
                print('')
            else:
                print('1 instância encontrada: ')
                print('')
            for instancia in instancias_info:
                print(f'ID: {instancia['ID']}')
                print(f'Status: {instancia['Status']}')
                print(f'IP público: {instancia['IP Público']}')
                print(f'Tags: {instancia['Tags']}')
                print('')
        else:
            print('Nenhuma instância encontrada!')
    except ClientError as e:
        print(tratar_erro_boto3(e, operacao='list'))

# ============================== UPDATE ============================== #

def add_tag(instance_id: str, key: str, value: str):
    try:
        response = ec2.create_tags(
            Resources=[instance_id],
            Tags=[{"Key": key, "Value": value}]
        )
        return response
    except ClientError as e:
        tratar_erro_boto3(e)


def remove_tag(instance_id: str, key: str, value: str = None):
    try:
        # if value == None, remove all tags with the key
        tags = [{"Key": key}]
        if value:
            tags[0]["Value"] = value

        response = ec2.delete_tags(
            Resources=[instance_id],
            Tags=tags
        )
        return response
    except ClientError as e:
        tratar_erro_boto3(e)


def change_instance_type(instance_id: str, instance_type: str):
    try:
        # Necessita que a instância esteja parada
        response = ec2.modify_instance_attribute(
            InstanceId=instance_id,
            InstanceType={"Value": instance_type}
        )
        return response
    except ClientError as e:
        tratar_erro_boto3(e)


# def change_security_group():


def start(instance_id: str):
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        return response
    except ClientError as e:
        tratar_erro_boto3(e, "start")


def stop(instance_id: str, hibernate: bool = False):
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], Hibernate=hibernate)
        return response
    except ClientError as e:
        tratar_erro_boto3(e, "stop")


def reboot(instance_id: str):
    try:
        response = ec2.reboot_instances(InstanceIds=[instance_id])
        return response
    except ClientError as e:
        tratar_erro_boto3(e, "reboot")


def hibernate(instance_id: str):
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], Hibernate=True)
        return response
    except ClientError as e:
        tratar_erro_boto3(e, "hibernate")


def tratar_erro_boto3(e: ClientError, operacao: str = None) -> str:
    error_code = e.response['Error']['Code']

    # Erros de estado da instância
    if error_code in ['IncorrectInstanceState', 'IncorrectState']:
        if operacao in ['reboot', 'stop', 'hibernate']:
            return "Erro: A instância deve estar **rodando** para esta operação."
        elif operacao == 'start':
            return "Erro: A instância deve estar **parada** para esta operação."
        else:
            return "Erro: A instância está em estado incorreto para esta operação."

    # Erro de hibernação não suportada
    elif error_code == 'UnsupportedHibernationConfiguration':
        return "Erro: A instância não foi configurada para hibernação."

    # Erro de ID de instância não encontrado
    elif error_code == "InvalidInstanceID.NotFound":
        return "Erro: ID da instância inválido."

    # Erros de permissão
    elif error_code in ['UnauthorizedOperation', 'AccessDenied']:
        if operacao == 'list':
            return "Erro: Permissão insuficiente para listar as instâncias."
        return "Erro: Permissão insuficiente para realizar a operação."

    # Outros erros
    else:
        return f"Erro inesperado: {e}"
