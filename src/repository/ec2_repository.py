import boto3
from botocore.exceptions import ClientError

def create_instance(ec2, image_id, instance_type, min_count, max_count, name):
    try:
        ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=min_count,
            MaxCount=max_count,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': name}]
                }
            ]
        )
        return True
    except ClientError as e:
        print(f"Erro ao criar instância:\n{e}")
        return None


def get_instance(ec2, instance_id):
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        return response["Reservations"][0]["Instances"][0]
    except ClientError as e:
        print(f"Erro ao buscar instância:\n{e}")
        return None

def list_instances(ec2, filters=None):
    try:
        response = ec2.describe_instances(Filters=filters or [])
        instances = [i for r in response["Reservations"] for i in r["Instances"]]
        return instances
    except ClientError as e:
        print(f"Erro ao listar instâncias:\n{e}")
        return []

def update_instance(ec2, instance_id, action):
    try:
        if action == "start":
            return ec2.start_instances(InstanceIds=[instance_id])
        elif action == "stop":
            return ec2.stop_instances(InstanceIds=[instance_id])
        elif action == "reboot":
            return ec2.reboot_instances(InstanceIds=[instance_id])
        else:
            raise ValueError("Ação inválida. Use 'start', 'stop' ou 'reboot'.")
    except ClientError as e:
        print(f"Erro ao atualizar instância:\n{e}")
        return None

def delete_instance(ec2, instance_id):
    try:
        return ec2.terminate_instances(InstanceIds=[instance_id])
    except ClientError as e:
        print(f"Erro ao deletar instância:\n{e}")
        return None
    