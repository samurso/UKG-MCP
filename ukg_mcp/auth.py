import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    token_url = os.getenv("UKG_TOKEN_URL")
    client_id = os.getenv("UKG_CLIENT_ID")
    client_secret = os.getenv("UKG_CLIENT_SECRET")

    payload = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        token_url,
        data=payload,
        auth=(client_id, client_secret)
    )

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")
