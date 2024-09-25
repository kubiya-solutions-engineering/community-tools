#!/usr/bin/env python3

import requests
import os

host = "http://localhost:8080"
username = "admin"
password = "QkTjXrVjP28EQ5M2TdfNNo"

if not all([host, username, password]):
    raise ValueError("Missing required environment variables")

try:
    response = requests.get(
        f"{host}/api/json?tree=jobs[name,url]",
        auth=(username, password),
        headers={"Accept": "application/json"}
    )
    response.raise_for_status()
    data = response.json()
    print(data)
except Exception as e:
    print(f"Failed to retrieve users from Jenkins: {str(e)}")