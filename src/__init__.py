# Importing necessary libraries
import click
from tabulate import tabulate
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Importing from src package
from src.config import get_ec2_client
from src import ec2_service as svc
