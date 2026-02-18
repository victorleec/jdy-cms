
import os
import sys
import json
import logging
from datetime import datetime

# Add root to sys.path
sys.path.insert(0, os.getcwd())

from src.config.settings import settings
from src.api.client import client
from src.services.ledger_service import LedgerService
from src.models.ledger_models import (
    SubjectBalanceRequest,
    DetailLedgerRequest,
    QtyAmountDetailRequest,
    QtyAmountTotalRequest,
    ItemBalanceRequest,
    ItemDetailRequest,
    CombinationRequest,
    GeneralLedgerRequest
)

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("=== Kingdee Ledger Module Demo ===")
    
    # 1. Initialize Service
    ledger_service = LedgerService(client)
    
    # Configuration
    PERIOD = "202601" # Default test period
    CURRENCY = "RMB"
    
    print(f"Target Period: {PERIOD}")
    
    # 2. Test Subject Balance (科目余额表)
    print("\n[1] Testing Subject Balance (科目余额表)...")
    try:
        req = SubjectBalanceRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD,
            currency=CURRENCY,
            fromLevel=1,
            toLevel=1
        )
        res = ledger_service.get_account_balance(req)
        print(f"Success! Total Items: {res.totalsize}")
        if res.items:
            print(f"First Item: {res.items[0].number} - {res.items[0].name}, End Debit: {res.items[0].endDebit}")
    except Exception as e:
        print(f"Failed: {e}")

    # 3. Test Detail Ledger (明细账)
    print("\n[2] Testing Detail Ledger (明细账)...")
    try:
        # Need a valid account number. Let's try '1001' (Cash) or '1002' (Bank) usually safer, 
        # or grab from the balance list if available.
        # For demo, I'll try '1001'. If it fails, users can change it.
        target_account = "1001" 
        print(f"Querying Account: {target_account}")
        
        req = DetailLedgerRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD,
            accountNum=target_account
        )
        res = ledger_service.get_detail_ledger(req)
        print(f"Success! Total Items: {res.totalsize}")
        if res.items:
            print(f"First Item: {res.items[0].ymd} - {res.items[0].voucherNo}, Balance: {res.items[0].balance}")
    except Exception as e:
        print(f"Failed: {e}")

    # 4. Test General Ledger (总账)
    print("\n[3] Testing General Ledger (总账)...")
    try:
        req = GeneralLedgerRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD,
            includeItem=0
        )
        res = ledger_service.get_general_ledger(req)
        print(f"Success! Total Items: {res.total}")
        if res.items:
            # API returns List[List[Row]]
            first_row = res.items[0][0]
            print(f"First Item: {first_row.number} - {first_row.name}")
    except Exception as e:
        print(f"Failed: {e}")

    # 5. Test Qty Amount Detail (数量金额明细账)
    print("\n[4] Testing Qty Amount Detail (数量金额明细账)...")
    # This might require specific accounts that have Quantity enabled. 
    # Validating generic call.
    try:
        req = QtyAmountDetailRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD,
            accountNum="1001" # Try a valid account
        )
        res = ledger_service.get_qty_amount_detail(req)
        print(f"Success! Total Items: {res.total}")
    except Exception as e:
        print(f"Failed: {e}")

    # 6. Test Qty Amount Total (数量金额总账)
    print("\n[5] Testing Qty Amount Total (数量金额总账)...")
    try:
        req = QtyAmountTotalRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD
        )
        res = ledger_service.get_qty_amount_total(req)
        print(f"Success! Total Items: {res.total}")
    except Exception as e:
        print(f"Failed: {e}")

    # 7. Test Item Balance (核算项目余额表)
    print("\n[6] Testing Item Balance (核算项目余额表)...")
    try:
        # Req requires auxiliaryType. 
        # We need to know a valid auxiliaryType ID. 
        # Without one, this will likely fail. I'll hardcode '1' (Customer usually) as a guess or skip if unknown.
        # Let's try '1'.
        aux_type = "1"
        print(f"Using Auxiliary Type: {aux_type}")
        req = ItemBalanceRequest(
            fromPeriod=PERIOD,
            toPeriod=PERIOD,
            auxiliaryType=aux_type
        )
        res = ledger_service.get_item_balance(req)
        print(f"Success! Total Items: {res.total}")
    except Exception as e:
        print(f"Failed: {e}")

    print("\n=== Demo Completed ===")

if __name__ == "__main__":
    main()
