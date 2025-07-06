import requests
import boto3
import json
from pathlib import Path
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("AWS_REGION", "eu-central-1")

if not KEY or not SECRET:
    raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in .env file")

IP_FILE = Path("/home/alice/security_group_updater/.last_ip.txt")
LAMBDA_NAME = "UpdateMyIPSecurityGroup"
# Boto3 session with custom credentials
session = boto3.Session(
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    region_name=REGION
)
lambda_client = session.client("lambda")

def get_current_ip():
    return requests.get("https://checkip.amazonaws.com").text.strip()

def read_last_ip():
    return IP_FILE.read_text().strip() if IP_FILE.exists() else None

def save_current_ip(ip):
    print(f"Saving IP: {ip} → {IP_FILE}")
    try:
        IP_FILE.write_text(ip)
        print("✔ IP saved successfully")
    except Exception as e:
        print(f"❌ Failed to save IP: {e}")

def trigger_lambda(ip):
    payload = {"ip": ip}
    response = lambda_client.invoke(
        FunctionName=LAMBDA_NAME,
        InvocationType="Event",  # async
        Payload=json.dumps(payload)
    )
    print("Triggered Lambda:", response["StatusCode"])

def main():
    current_ip = get_current_ip()
    last_ip = read_last_ip()

    if current_ip != last_ip:
        print(f"IP changed: {last_ip} -> {current_ip}")
        trigger_lambda(current_ip)
        save_current_ip(current_ip)
    else:
        print("IP unchanged.")

if __name__ == "__main__":
    main()
