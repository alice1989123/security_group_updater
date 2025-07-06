import boto3
import requests
import json
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("AWS_REGION", "eu-central-1")
LAMBDA_NAME = os.getenv("LAMBDA_NAME", "UpdateMyIPSecurityGroup")

if not KEY or not SECRET:
    raise ValueError("Missing AWS credentials")

session = boto3.Session(
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    region_name=REGION,
)

ssm = session.client("ssm")
lambda_client = session.client("lambda")

def get_current_ip():
    return requests.get("https://checkip.amazonaws.com").text.strip()

def read_last_ip():
    try:
        response = ssm.get_parameter(Name="/infra/ip/last", WithDecryption=False)
        logger.info(f"SSM response: {response}")
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        logger.warning("Parameter not found, returning None")
        return None
    except Exception as e:
        logger.error(f"Error reading IP from SSM: {e}")
        return None

def save_current_ip(ip):
    try:
        ssm.put_parameter(
            Name="/infra/ip/last",
            Value=ip,
            Type="String",
            Overwrite=True
        )
        logger.info(f"✔ Saved IP: {ip}")
    except Exception as e:
        logger.info(f"❌ Failed to save IP to SSM: {e}")

def trigger_lambda(ip):
    payload = {"ip": ip}
    response = lambda_client.invoke(
        FunctionName=LAMBDA_NAME,
        InvocationType="Event",
        Payload=json.dumps(payload)
    )
    logger.info(f"✅ Lambda triggered, status: {response['StatusCode']}")

def main():
    current_ip = get_current_ip()
    last_ip = read_last_ip()

    if current_ip != last_ip:
        logger.info(f"🔄 IP changed: {last_ip} → {current_ip}")
        trigger_lambda(current_ip)
        save_current_ip(current_ip)
    else:
        logger.info("✅ IP unchanged.")

if __name__ == "__main__":
    
    logger.info("Starting security group updater")
    main()
