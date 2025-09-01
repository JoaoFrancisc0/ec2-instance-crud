from src import os, load_dotenv, boto3

def get_ec2_client():
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "resources", ".env")
    load_dotenv(dotenv_path=dotenv_path)

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    return ec2
