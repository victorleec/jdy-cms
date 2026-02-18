import sys
import os
# Add project root to sys.path to allow importing from src
sys.path.append(os.getcwd())

import json
import requests
from src.services.voucher_service import voucher_service
from src.config.settings import settings
from src.api.client import client
from src.api.auth import auth_manager

def main():
    print("=== Kingdee API Diagnosis ===")
    
    # 1. Auth
    try:
        token = auth_manager.get_access_token()
        print(f"[Auth] Access Token: {token[:10]}...")
    except Exception as e:
        print(f"[Auth] Failed: {e}")
        return

    # 2. Check Settings
    print(f"[Config] Base URL: {settings.JDY_API_BASE_URL}")
    print(f"[Config] Router Addr (IDC): {settings.JDY_IDC_DOMAIN}")
    print(f"[Config] DB ID: {settings.JDY_ENTERPRISE_ID}")
    print(f"[Config] Service ID (sId): {settings.JDY_SERVICE_ID}")

    if not settings.JDY_SERVICE_ID and settings.JDY_ENTERPRISE_ID:
        print("\n[!] Warning: JDY_SERVICE_ID is not set. Assuming sId = dbId for testing.")
        # Temporarily hack the client to inject sId if missing
        # We can pass it in params to override
        fallback_sId = settings.JDY_ENTERPRISE_ID
    else:
        fallback_sId = settings.JDY_SERVICE_ID

    # 3. Try Summary Interface (GET) - often simpler
    print("\n[Test 1] GET Voucher Summary")
    try:
        # GET /jdyaccouting/voucher?action=getVchTotalQuery...
        res = voucher_service.get_voucher_summary(
            from_date="2026-01-01", 
            to_date="2026-01-31"
        )
        print("Summary Response:", res)
    except Exception as e:
        print(f"Summary Failed: {e}")
        
    # 3b. Try Summary WITH explicit sId if it failed or just to be sure
    print(f"\n[Test 1b] GET Voucher Summary (Explicit sId={fallback_sId})")
    try:
        request_params = {
            "action": "getVchTotalQuery",
            "fromDate": "2026-01-01",
            "toDate": "2026-01-31",
            "sId": fallback_sId 
        }
        res = client.get("/jdyaccouting/voucher", params=request_params)
        print("Summary (Explicit sId) Response:", res)
    except Exception as e:
        print(f"Summary (Explicit sId) Failed: {e}")
        
    # 4. Try Voucher List (POST)
    print("\n[Test 2] POST Voucher List (via Gateway)")
    try:
        url = "/jdyaccouting/voucherlist"
        data = {
            "fromPeriod": 202601,
            "toPeriod": 202601,
            "pageSize": 1
        }
        full_url = f"{settings.JDY_API_BASE_URL}{url}"
        
        # Construct Params
        token = auth_manager.get_access_token()
        params = {
            "access_token": token,
            "dbId": settings.JDY_ENTERPRISE_ID,
            "sId": fallback_sId
        }
        
        # Headers
        headers = {
            "Content-Type": "application/json",
            "X-GW-Router-Addr": settings.JDY_IDC_DOMAIN
        }
        
        # Generate Curl
        param_str = "&".join(f"{k}={v}" for k, v in params.items())
        curl_cmd = f"curl -X POST '{full_url}?{param_str}' \\\n"
        for k, v in headers.items():
            curl_cmd += f"  -H '{k}: {v}' \\\n"
        curl_cmd += f"  -d '{json.dumps(data)}'"
        
        print("\n--- Equivalent Curl Command ---")
        print(curl_cmd)
        print("-------------------------------")

        print(f"Requesting: {full_url}")
        # Note: client.post wraps logic, but we want to be sure what we send.
        # Let's use requests directly to be 100% sure we match the curl above.
        res = requests.post(full_url, params=params, json=data, headers=headers)
        print(f"List Response: {res.status_code} {res.text}")
        
    except Exception as e:
        print(f"List Failed: {e}")

if __name__ == "__main__":
    main()