import boto3
from botocore.exceptions import ClientError

# Inicializa o cliente EC2
ec2 = boto3.client('ec2')

def criar_instancia(nome):
    try:
        instancia = ec2.run_instances(
            ImageId='ami-0c94855ba95c71c99', # Substitua pelo seu AMI
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': nome}]
            }]
        )
        print(f"Instância criada: {instancia['Instances'][0]['InstanceId']}")
    except ClientError as e:
        print(f"Erro ao criar instância: {e}")

