import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_access_token():
    token_url = os.getenv("UKG_TOKEN_URL")
    client_id = os.getenv("UKG_CLIENT_ID")
    client_secret = os.getenv("UKG_CLIENT_SECRET")

    required_values = {
        "UKG_TOKEN_URL": token_url,
        "UKG_CLIENT_ID": client_id,
        "UKG_CLIENT_SECRET": client_secret,
    }

    missing_values = [name for name, value in required_values.items() if not value]
    if missing_values:
        raise Exception(f"Missing required environment variables: {', '.join(missing_values)}")

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = requests.post(
        token_url,
        data=payload,
        headers=headers,
        timeout=30,
    )

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        if not access_token:
            raise Exception("Authentication succeeded but no access_token was returned.")
        return access_token

    raise Exception(f"Authentication failed: {response.status_code} - {response.text}")
