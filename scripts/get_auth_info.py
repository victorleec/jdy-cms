import time
import uuid
import sys
import os
# Add project root to sys.path to allow importing from src
sys.path.append(os.getcwd())

import requests
import json
from src.config.settings import settings
from src.utils.signature import get_header_signature

def get_auth_info():
    print("=== Kingdee App Authorization Info ===")
    
    # Check Prereqs
    check_vars = [
        ("Base URL", settings.JDY_API_BASE_URL),
        ("Client ID", settings.JDY_CLIENT_ID),
        ("Client Secret", settings.JDY_CLIENT_SECRET),
        ("Outer Instance ID", settings.JDY_OUTER_INSTANCE_ID)
    ]
    
    missing = [name for name, val in check_vars if not val]
    if missing:
        print(f"Error: Missing configuration: {', '.join(missing)}")
        print("Please configure them in .env")
        if "Outer Instance ID" in missing:
            print("Note: JDY_OUTER_INSTANCE_ID is required for this specific API. Check your Kingdee App Details.")
        return

    # API Constants
    method = "POST"
    path = "/jdyconnector/app_management/push_app_authorize"
    url = f"{settings.JDY_API_BASE_URL}{path}"
    
    # Params
    params = {
        "outerInstanceId": settings.JDY_OUTER_INSTANCE_ID
    }
    
    # Header Factors
    timestamp = str(int(time.time() * 1000))
    nonce = str(time.time_ns()) # or random int
    
    # Calculate Signature
    # Signature input: method, path, params, nonce, timestamp
    signature = get_header_signature(
        client_secret=settings.JDY_CLIENT_SECRET,
        method=method,
        path=path,
        params=params,
        nonce=nonce,
        timestamp=timestamp
    )
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-ClientID": settings.JDY_CLIENT_ID,
        "X-Api-Auth-Version": "2.0",
        "X-Api-TimeStamp": timestamp,
        "X-Api-Nonce": nonce,
        "X-Api-SignHeaders": "X-Api-TimeStamp,X-Api-Nonce",
        "X-Api-Signature": signature
    }
    
    print(f"Requesting: {url}")
    print(f"Params: {params}")
    
    try:
        # Note: requests.post with 'params' adds them to URL query string, which is correct for this API
        res = requests.post(url, params=params, headers=headers)
        
        print(f"Status: {res.status_code}")
        try:
            data = res.json()
            print("Response Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get("code") == 200 and data.get("data"):
                auth_data = data["data"][0]
                print("\n--- EXTRACTED INFO ---")
                print(f"Domain (IDC): {auth_data.get('domain')}")
                print(f"Service ID:   {auth_data.get('serviceId')}")
                print(f"Account ID:   {auth_data.get('accountId')}")
                print(f"App Key:      {auth_data.get('appKey')}")
                print(f"App Secret:   {auth_data.get('appSecret')}")
                print("----------------------")
                print("Please update your .env file with these values if they differ.")
                
        except json.JSONDecodeError:
            print("Raw Response:", res.text)
            
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    get_auth_info()
