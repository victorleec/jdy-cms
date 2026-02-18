import os
import sys
from src.api.auth import auth_manager
from src.api.client import client

from src.config.settings import settings

def deep_print(obj, indent=0):
    prefix = "  " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(f"{prefix}{k}:")
            deep_print(v, indent + 1)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            print(f"{prefix}[{i}]:")
            deep_print(item, indent + 1)
    else:
        print(f"{prefix}{obj}")

from datetime import datetime
from src.services.voucher_service import voucher_service
from src.models.voucher import VoucherQueryFilter

def main():
    print("=== Kingdee API Demo ===")
    
    # Check Env
    if not settings.JDY_CLIENT_ID or not settings.JDY_APP_KEY:
        print("Error: Environment variables not set. Please configure .env file.")
        print(f"Current Settings: BaseURL={settings.JDY_API_BASE_URL}, ClientID={'*' * len(settings.JDY_CLIENT_ID) if settings.JDY_CLIENT_ID else 'None'}")
        return

    try:
        # 1. Test Auth
        print("\n[1] Testing Authentication...")
        token = auth_manager.get_access_token()
        print(f"Success! Access Token: {token[:10]}... (expires in {int(auth_manager.token_expires_at - 0)}s)")
        
        # 2. Test Voucher Module
        print("\n[2] Testing Voucher Module...")
        
        if not settings.JDY_ENTERPRISE_ID:
             print("Skipping Voucher test: JDY_ENTERPRISE_ID (dbId) not set in .env")
        else:
            # Query Vouchers
            # User requested 202601
            current_period = 202601
            
            print(f"Querying Vouchers for period: {current_period}")
            query_filter = VoucherQueryFilter(
                fromPeriod=current_period, 
                toPeriod=current_period,
                pageSize=5
            )
            
            try:
                res = voucher_service.get_voucher_list(query_filter)
                print(f"Query Success. Total Records: {res.get('totalsize', 0)}")
                
                # Save to file
                output_file = "voucher_demo_output.json"
                import json
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(res, f, indent=2, ensure_ascii=False)
                print(f"Full response saved to: {output_file}")
                
                if res.get("items"):
                    print(f"First Voucher ID: {res['items'][0].get('id')} (See file for details)")
                else:
                    print("No vouchers found in this period.")
                    
            except Exception as e:
                print(f"Voucher Query Failed: {e}")
            
    except Exception as e:
        print(f"\n[!] Fatal Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure src is in path if running from root
    sys.path.insert(0, os.getcwd())
    main()
