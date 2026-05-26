import requests
import os
from .auth import get_access_token

def get_employee_names():
    base_url = os.getenv("UKG_BASE_URL")
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    endpoint = f"{base_url}/employees"

    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch employees: {response.status_code} - {response.text}")

    data = response.json()

    employees = []

    for emp in data.get("employees", []):
        employees.append({
            "employee_id": emp.get("employeeId"),
            "employee_name": f"{emp.get('firstName')} {emp.get('lastName')}"
        })

    return employees
