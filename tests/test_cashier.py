import sys
import os
import random
import time
from pprint import pprint

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.services.cashier_service import cashier_service
from src.models.cashier_models import CashierJournalItem, CashierAccountItem

def check_success(res):
    if "code" in res:
        if res["code"] == 0 or str(res["code"]) == "0":
            return True
    if "status" in res:
        if res["status"] == 200 or str(res["status"]) == "200":
            return True
    return False

def test_cashier_account():
    print("\n--- Testing Cashier Accounts ---")
    
    # Generate unique test data
    suffix = str(random.randint(1000, 9999))
    account_number = f"TEST-{suffix}"
    account_name = f"Test Account {suffix}"
    
    # 1. Add Account
    print(f"1. Adding Account: {account_number}")
    new_account = CashierAccountItem(
        number=account_number,
        name=account_name,
        type=1, # Cash
        isForbid=0
    )
    try:
        res = cashier_service.save_account([new_account])
        if check_success(res) and res.get("data", {}).get("succeedList"):
            print("   Success")
            account_data = res["data"]["succeedList"][0]
            # Handle potential dict or object if pydantic parsed it, but here it's raw dict from API
            # Wait, service returns dict from client.post which returns dict.
            account_id = account_data.get("id")
            print(f"   Created Account ID: {account_id}")
        else:
            print(f"   Failed: {res}")
            return None
    except Exception as e:
        print(f"   Exception adding account: {e}")
        return None

    # 2. List Accounts
    print("2. Listing Accounts")
    try:
        res = cashier_service.get_account_list(type=1)
        if check_success(res):
            count = res.get("count", 0)
            print(f"   Found {count} accounts")
            # Verify our account is there
            found = False
            for acct in res.get("list", []):
                if acct.get("number") == account_number:
                    found = True
                    # Update ID if needed (though we got it from create)
                    if not account_id:
                        account_id = acct.get("id")
                    break
            if found:
                print(f"   Verified account {account_number} exists in list")
            else:
                print(f"   Account {account_number} NOT found in list")
        else:
            print(f"   Failed to list accounts: {res}")
    except Exception as e:
        print(f"   Exception listing accounts: {e}")

    if not account_id:
        print("Cannot proceed with Update/Delete without Account ID")
        return None

    # 3. Update Account
    print("3. Updating Account")
    try:
        new_name = f"{account_name} Updated"
        update_account = CashierAccountItem(
            id=account_id,
            number=account_number,
            name=new_name,
            type=1,
            isForbid=0
        )
        res = cashier_service.update_account([update_account])
        if check_success(res) and res.get("data", {}).get("succeedList"):
             print("   Success")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception updating account: {e}")

    # 4. Delete Account
    print("4. Deleting Account")
    try:
        res = cashier_service.delete_account([account_number])
        if check_success(res):
            data = res.get("data", {})
            if account_number in data.get("succeed", []) or account_number in str(data.get("succeed", [])):
                print("   Success")
            else:
                 print(f"   Account not in succeed list: {data}")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception deleting account: {e}")

    return account_number

def test_cashier_journal():
    print("\n--- Testing Cashier Journal ---")
    
    # We need a valid Cashier Account Number.
    # Since we deleted the test one, let's find an existing one or create a temp one.
    # For now, let's try to list and use the first one available.
    
    target_account_num = None
    try:
        res = cashier_service.get_account_list(type=1)
        if check_success(res) and res.get("list"):
            first_acct = res["list"][0]
            target_account_num = first_acct.get("number")
            print(f"Using existing account: {target_account_num} ({first_acct.get('name')})")
        else:
            print("No existing cash accounts found. Creating a temp one.")
            # Create temp account
            suffix = str(random.randint(1000, 9999))
            temp_acct = CashierAccountItem(number=f"JTEST-{suffix}", name=f"Journal Test {suffix}", type=1)
            res_add = cashier_service.save_account([temp_acct])
            if check_success(res_add) and res_add.get("data", {}).get("succeedList"):
                target_account_num = f"JTEST-{suffix}"
                print(f"Created temp account: {target_account_num}")
            else:
                print("Failed to create temp account for journal test. Aborting.")
                return
    except Exception as e:
        print(f"Exception getting/creating account: {e}")
        return

    # 1. Add Journal
    print("1. Adding Journal Entry")
    # Use current date to avoid period issues
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    period = datetime.now().strftime("%Y%m")
    print(f"   Using date: {current_date}, period: {period}")

    journal_item = CashierJournalItem(
        cashierAccountNumber=target_account_num,
        date=current_date,
        explanation="Test Journal Entry",
        credit=0,
        debit=100,
        remark="Test Remark"
    )
    
    journal_id = None
    try:
        res = cashier_service.save_journal([journal_item])
        # Check result
        if check_success(res):
            data = res.get("data", {})
            if data.get("succeedList"):
                success_item = data["succeedList"][0]
                journal_id = success_item.get("id")
                print(f"   Success. Journal ID: {journal_id}")
            elif data.get("failedList"):
                print(f"   Failed List: {data['failedList']}")
            else:
                print(f"   Unknown response structure: {data}")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception adding journal: {e}")
        return

    if not journal_id:
        print("Cannot proceed with Update/Delete without Journal ID")
        return

    # 2. List Journal
    print("2. Listing Journal Entries")
    try:
        # Period format usually yyyyMM or yyyy-MM-dd? Doc says 'period' string in example 201904.
        # But our date is 2024-01-15. So period is 202401.
        # period variable is already set above
        res = cashier_service.get_journal_list(period=period, cashierAccountNumber=target_account_num)
        if check_success(res):
            items = res.get("data", {}).get("items", [])
            print(f"   Found {len(items)} items")
            found = False
            for item in items:
                # Need to check how ID is returned (str/int)
                if str(item.get("id")) == str(journal_id):
                    found = True
                    break
            if found:
                print("   Verified journal entry exists in list")
            else:
                print(f"   Journal {journal_id} NOT found in list")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception listing journals: {e}")

    # 3. Update Journal
    print("3. Updating Journal Entry")
    try:
        update_item = CashierJournalItem(
            id=journal_id,
            cashierAccountNumber=target_account_num,
            date=current_date,
            explanation="Test Journal Entry Updated",
            credit=0,
            debit=150, # Changed amount
            remark="Updated Remark"
        )
        res = cashier_service.update_journal([update_item])
        if check_success(res):
             # Check succeedList
             data = res.get("data", {})
             if data.get("succeedList"):
                 print("   Success")
             else:
                 print(f"   Failed/Empty success list: {data}")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception updating journal: {e}")

    # 4. Delete Journal
    print("4. Deleting Journal Entry")
    try:
        res = cashier_service.delete_journal([journal_id])
        if check_success(res):
            data = res.get("data", {})
            # Check succeedList (it might be list of IDs)
            succeed_list = data.get("succeedList", [])
            if journal_id in succeed_list or str(journal_id) in [str(x) for x in succeed_list]:
                 print("   Success")
            else:
                 print(f"   Journal ID not in succeed list: {succeed_list}")
                 if data.get("failedList"):
                     print(f"   Failed List: {data['failedList']}")
        else:
             print(f"   Failed: {res}")
    except Exception as e:
        print(f"   Exception deleting journal: {e}")


if __name__ == "__main__":
    test_cashier_account()
    test_cashier_journal()
