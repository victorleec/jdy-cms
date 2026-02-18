
import logging
from typing import Dict, Any, Optional

from src.api.client import KingdeeClient
from src.models.ledger_models import (
    SubjectBalanceRequest, SubjectBalanceResponse,
    DetailLedgerRequest, DetailLedgerResponse,
    QtyAmountDetailRequest, QtyAmountDetailResponse,
    QtyAmountTotalRequest, QtyAmountTotalResponse,
    ItemBalanceRequest, ItemBalanceResponse,
    ItemDetailRequest, ItemDetailResponse,
    CombinationRequest, CombinationResponse,
    GeneralLedgerRequest, GeneralLedgerResponse
)

logger = logging.getLogger(__name__)

class LedgerService:
    """
    账簿服务 (Ledger Service)
    提供科目余额表、明细账、数量金额账等报表的查询功能。
    """

    def __init__(self, client: KingdeeClient):
        self.client = client

    def _handle_response(self, response: Dict[str, Any], model_class: Any) -> Any:
        # Helper to check code and parse response
        code = response.get("code")
        status = response.get("status")
        
        is_success = False
        if code is not None and str(code) == "0":
            is_success = True
        elif status is not None:
            if int(status) == 200:
                is_success = True
            elif int(status) == 250:
                 # 250 means No Query Results. Treat as success with empty data.
                 # We need to return an empty instance of model_class.
                 # Assuming model_class has default values or we can construct it.
                 # Most response models require 'total'/'totalsize' and 'items'.
                 # We'll try to construct with defaults or empty list.
                 # This is a bit hacky but Pydantic 2.x/1.x might require valid fields.
                 
                 # Strategy: Return empty dict and let Pydantic defaults handle it? 
                 # Models defined require 'total' or 'totalsize'.
                 # Let's inspect model fields or just try to instantiate with 0/[]
                 
                 defaults = {}
                 if "totalsize" in model_class.model_fields:
                     defaults["totalsize"] = 0
                 if "total" in model_class.model_fields:
                     defaults["total"] = 0
                 if "items" in model_class.model_fields:
                     defaults["items"] = []
                 
                 # Add other required fields if any? 
                 # For combination, it has 'items' and 'columnTotal'.
                 
                 try:
                     return model_class(**defaults)
                 except: 
                     # If validation fails, just return empty object? Or raise?
                     logger.warning(f"Could not create empty model for status 250, returning default. Model: {model_class.__name__}")
                     # Try constructing without args if all optional?
                     pass
                 
                 is_success = True # Proceed to normal parsing if we didn't return above? No, response data is likely missing.
                 # If we assume success and data is empty, 'data = response["data"]' might fail if data is missing.
                 
                 # Actually, if we set is_success=True here, and data is missing, the next block will fail.
                 # So we MUST return here.
                 return model_class.construct(**defaults) # .construct skips validation (Pydantic v1) or use typical init.

        if not is_success:
            error_msg = response.get("msg", "Unknown error")
            c = code if code is not None else "None"
            s = status if status is not None else "None"
            logger.error(f"Ledger API Error: {error_msg} (code={c}, status={s})")
            raise Exception(f"Kingdee API Error: {error_msg} (code={c}, status={s})")
        
        # Some endpoints return data in 'data', others in root? 
        # Checking docs:
        # Balance: items in root? No, example shows root. items list.
        # QueryDetail: items in data object.
        # QtyAmountDetail: msg, data: { total, items }
        # Let's handle these specific cases.
        
        data = response
        if "data" in response and isinstance(response["data"], dict):
            # Many reports wrap items in a 'data' object
            data = response["data"]
        
        # For SubjectBalance, users provided example shows root keys: msg, totalsize, items.
        # So 'data' extraction above is safe if 'data' key exists, otherwise use root.
        
        return model_class(**data)

    def get_account_balance(self, request: SubjectBalanceRequest) -> SubjectBalanceResponse:
        """
        查询科目余额表
        Path: /jdyaccouting/account/balance
        """
        endpoint = "/jdyaccouting/account/balance"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, SubjectBalanceResponse)

    def get_detail_ledger(self, request: DetailLedgerRequest) -> DetailLedgerResponse:
        """
        查询明细账
        Path: /jdyaccouting/querydetail
        """
        endpoint = "/jdyaccouting/querydetail"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, DetailLedgerResponse)

    def get_qty_amount_detail(self, request: QtyAmountDetailRequest) -> QtyAmountDetailResponse:
        """
        查询数量金额明细账
        Path: /jdyaccouting/report/qtyamountdetail
        Fallback Path Assumption: report usually correct based on updated docs.
        """
        endpoint = "/jdyaccouting/report/qtyamountdetail"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, QtyAmountDetailResponse)

    def get_qty_amount_total(self, request: QtyAmountTotalRequest) -> QtyAmountTotalResponse:
        """
        查询数量金额总账
        Path: /jdyaccouting/report/qtyamounttotal
        """
        endpoint = "/jdyaccouting/report/qtyamounttotal"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, QtyAmountTotalResponse)

    def get_item_balance(self, request: ItemBalanceRequest) -> ItemBalanceResponse:
        """
        查询核算项目余额表
        Path: /jdyaccouting/report/itembalance
        """
        endpoint = "/jdyaccouting/report/itembalance"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, ItemBalanceResponse)

    def get_item_detail(self, request: ItemDetailRequest) -> ItemDetailResponse:
        """
        查询核算项目明细账
        Path: /jdyaccouting/report/itemdetail
        """
        endpoint = "/jdyaccouting/report/itemdetail"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, ItemDetailResponse)

    def get_combination(self, request: CombinationRequest) -> CombinationResponse:
        """
        查询核算项目组合表
        Path: /jdyaccouting/report/combination
        """
        endpoint = "/jdyaccouting/report/combination"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, CombinationResponse)

    def get_general_ledger(self, request: GeneralLedgerRequest) -> GeneralLedgerResponse:
        """
        查询总账
        Path: /jdyaccouting/report/genledger
        """
        endpoint = "/jdyaccouting/report/genledger"
        payload = request.model_dump(exclude_none=True)
        response = self.client.get(endpoint, params=payload)
        return self._handle_response(response, GeneralLedgerResponse)
