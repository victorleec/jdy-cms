import sys
import os
import json
from pprint import pprint

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.services.report_service import report_service

def check_success(res):
    # Check for "code" == 0 or "0"
    if "code" in res:
        # Check if code is integer 0 or string "0"
        if res["code"] == 0 or str(res["code"]) == "0":
            return True
    # Check for "status" == 200 or "200"
    if "status" in res:
        if res["status"] == 200 or str(res["status"]) == "200":
            return True
    return False

def test_profit_statement():
    print("\n--- Testing Profit Statement ---")
    try:
        res = report_service.get_profit_statement(202401, 202401)
        # print("Response:", res) 
        if check_success(res):
            print("Success")
            data = res.get("data")
            if data and data.get("reportValues"):
                 print(f"Got {len(data['reportValues'])} report values")
                 if len(data['reportValues']) > 0 and len(data['reportValues'][0]['items']) > 0:
                     print("First item:", data['reportValues'][0]['items'][0])
            else:
                 print("No report values found or empty data")
        else:
            print("Error:", res.get("msg"))
    except Exception as e:
        print(f"Exception: {e}")

def test_balance_sheet():
    print("\n--- Testing Balance Sheet ---")
    try:
        res = report_service.get_balance_sheet(202401, 202401)
        # print("Response:", res)
        if check_success(res):
            print("Success")
            data = res.get("data")
            if data and data.get("reportValues"):
                 print(f"Got {len(data['reportValues'])} report values")
            else:
                 print("No report values found")
        else:
             print("Error:", res.get("msg"))
    except Exception as e:
        print(f"Exception: {e}")

def test_cash_flow():
    print("\n--- Testing Cash Flow ---")
    try:
        res = report_service.get_cash_flow_statement(202401, 202401)
        # print("Response:", res)
        if check_success(res):
             print("Success")
        else:
             print("Error:", res.get("msg"))
    except Exception as e:
        print(f"Exception: {e}")

def test_expense_detail():
    print("\n--- Testing Expense Detail ---")
    try:
        # Passing from_period now
        # Account 6602 might be valid, or we try to find one if this fails with no data
        res = report_service.get_expense_detail(202401, 202401, 6602)
        print("Response Code/Starus:", res.get("code"), res.get("status"))
        if check_success(res):
             print("Success")
             if res.get("data"):
                # pprint(res.get("data"))
                print("Got expense detail data")
        else:
             print("Error:", res.get("msg"))
    except Exception as e:
        print(f"Exception: {e}")

def test_tax_payable():
    print("\n--- Testing Tax Payable Detail ---")
    try:
        res = report_service.get_tax_payable_detail(202401)
        print("Response Code/Status:", res.get("code"), res.get("status"))
        if check_success(res):
             print("Success")
             if res.get("data"):
                # pprint(res.get("data"))
                print("Got tax payable data")
        else:
             print("Error:", res.get("msg"))
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_profit_statement()
    test_balance_sheet()
    test_cash_flow()
    test_expense_detail()
    test_tax_payable()
