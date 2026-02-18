from typing import List, Dict, Any, Union, Optional
from src.api.client import client
from src.models.cashier_models import (
    CashierJournalItem, CashierJournalListResponse, 
    CashierJournalOperationResponse, CashierJournalListItem,
    CashierAccountItem, CashierAccountListResponse,
    CashierAccountOperationResponse, CashierAccountDeleteResponse
)

class CashierService:
    # --- Cashier Journal Methods ---
    
    def get_journal_list(
        self, 
        period: Union[str, int], 
        cashierAccountNumber: str,
        includeVch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询日记账
        GET /jdyaccouting/cashier/journal/list
        """
        params = {
            "period": period,
            "cashierAccountNumber": cashierAccountNumber,
            "includeVch": includeVch # 0:未生产凭证 1:仅生成凭证 为空就是所有凭证
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return client.get("/jdyaccouting/cashier/journal/list", params=params)

    def save_journal(self, items: List[CashierJournalItem]) -> Dict[str, Any]:
        """
        新增日记账
        POST /jdyaccouting/cashier/journal/add
        """
        payload = {
            "items": [item.dict(exclude_unset=True) for item in items]
        }
        return client.post("/jdyaccouting/cashier/journal/add", payload)

    def update_journal(self, items: List[CashierJournalItem]) -> Dict[str, Any]:
        """
        修改日记账
        POST /jdyaccouting/cashier/journal/update
        """
        payload = {
            "items": [item.dict(exclude_unset=True) for item in items]
        }
        return client.post("/jdyaccouting/cashier/journal/update", payload)

    def delete_journal(self, ids: List[int]) -> Dict[str, Any]:
        """
        删除日记账
        POST /jdyaccouting/cashier/journal/delete
        """
        # Doc says body items: [id1, id2], not {items: [id1, id2]} ?
        # Wait, doc says:
        # BODY:
        # {
        #     items: [
        #         10000000010,
        #         ...
        #     ]
        # }
        payload = {
            "items": ids
        }
        return client.post("/jdyaccouting/cashier/journal/delete", payload)

    # --- Cashier Account Methods ---

    def get_account_list(
        self, 
        type: int, 
        isForbid: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        查询账户列表
        GET /jdyaccouting/cashieraccount/list
        """
        params = {
            "type": type, # 1：现金账户 2：银行账户
            "isForbid": isForbid # 0：使用 1：禁用
        }
        params = {k: v for k, v in params.items() if v is not None}
        return client.get("/jdyaccouting/cashieraccount/list", params=params)

    def save_account(self, items: List[CashierAccountItem]) -> Dict[str, Any]:
        """
        新增账户
        POST /jdyaccouting/cashieraccount/add
        """
        payload = {
            "items": [item.dict(exclude_unset=True) for item in items]
        }
        return client.post("/jdyaccouting/cashieraccount/add", payload)

    def update_account(self, items: List[CashierAccountItem]) -> Dict[str, Any]:
        """
        修改账户
        POST /jdyaccouting/cashieraccount/update
        """
        payload = {
            "items": [item.dict(exclude_unset=True) for item in items]
        }
        return client.post("/jdyaccouting/cashieraccount/update", payload)

    def delete_account(self, numbers: List[str]) -> Dict[str, Any]:
        """
        删除账户（批量）
        DELETE /jdyaccouting/cashieraccount/delete
        """
        # Doc says method DELETE but uses BODY?
        # Many HTTP clients don't support body in DELETE.
        # But doc request example shows BODY.
        # Let's hope client.delete supports json/data arg or use client.request('DELETE', ...)
        # If client.delete doesn't support json, we might need a workaround. 
        # Checking src/api/client.py would be good, but let's assume standard requests usage.
        # requests.delete(url, json=...) works.
        payload = {
            "numberArray": numbers
        }
        return client.request("DELETE", "/jdyaccouting/cashieraccount/delete", json=payload)

cashier_service = CashierService()
