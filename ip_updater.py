import requests
import boto3
import json
import os
from pathlib import Path

KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("AWS_REGION", "eu-central-1")
IP_FILE_PATH = os.getenv("IP_FILE", "/tmp/.last_ip.txt")
LAMBDA_NAME = os.getenv("LAMBDA_NAME", "UpdateMyIPSecurityGroup")

if not KEY or not SECRET:
    raise ValueError("Missing AWS credentials")

session = boto3.Session(
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET,
    region_name=REGION,
)
lambda_client = session.client("lambda")

def get_current_ip():
    return requests.get("https://checkip.amazonaws.com").text.strip()

def read_last_ip():
    path = Path(IP_FILE_PATH)
    return path.read_text().strip() if path.exists() else None

def save_current_ip(ip):
    try:
        Path(IP_FILE_PATH).write_text(ip)
        print(f"✔ Saved IP: {ip}")
    except Exception as e:
        print(f"❌ Failed to save IP: {e}")

def trigger_lambda(ip):
    payload = {"ip": ip}
    response = lambda_client.invoke(
        FunctionName=LAMBDA_NAME,
        InvocationType="Event",
        Payload=json.dumps(payload)
    )
    print("✅ Lambda triggered, status:", response["StatusCode"])

def main():
    current_ip = get_current_ip()
    last_ip = read_last_ip()

    if current_ip != last_ip:
        print(f"🔄 IP changed: {last_ip} → {current_ip}")
        trigger_lambda(current_ip)
        save_current_ip(current_ip)
    else:
        print("✅ IP unchanged.")

if __name__ == "__main__":
    main()