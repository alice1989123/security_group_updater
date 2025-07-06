import boto3
import requests
import json
import os

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
        return response["Parameter"]["Value"]
    except ssm.exceptions.ParameterNotFound:
        return None

def save_current_ip(ip):
    try:
        ssm.put_parameter(
            Name="/infra/ip/last",
            Value=ip,
            Type="String",
            Overwrite=True
        )
        print(f"✔ Saved IP: {ip}")
    except Exception as e:
        print(f"❌ Failed to save IP to SSM: {e}")

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
