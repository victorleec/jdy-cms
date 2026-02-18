
import logging
from typing import Dict, Any, List, Optional
from src.api.client import KingdeeClient
from src.models.settings_models import (
    SystemProfileResponse,
    AccountSubjectListResponse, AccountSubjectSaveRequest,
    VoucherWordListResponse,
    AuxiliaryItemClassListResponse,
    AuxiliaryItemListResponse, AuxiliaryItemSaveRequest
)

logger = logging.getLogger(__name__)

class SettingsService:
    """
    设置服务 (Settings Service)
    提供系统参数、科目、凭证字、辅助核算等基础资料的查询与管理。
    """

    def __init__(self, client: KingdeeClient):
        self.client = client

    def _handle_response(self, response: Dict[str, Any], model_class: Any) -> Any:
        # Standard error handling
        code = response.get("code")
        status = response.get("status") # Some APIs might use status
        
        is_success = False
        if code is not None and (str(code) == "0" or str(code) == "200"):
            is_success = True
        elif status is not None and (str(status) == "200" or str(status) == "250"):
            is_success = True
        
        # Specific check for auxiliary items save response (complex structure)
        # But here we are mostly handling GET responses or simple POSTs.
        
        if not is_success:
            # Check if it is a list response where code might be missing?
            # VoucherWord list response has 'code': 0.
            # Account list response has 'code': 0.
            error_msg = response.get("msg", "Unknown error")
            logger.error(f"Settings API Error: {error_msg} (code={code})")
            raise Exception(f"Kingdee API Error: {error_msg} (code={code})")

        # Data extraction logic
        # Most settings APIs return data directly in root or 'data' field?
        # Profile: root (value)
        # Account: root (list, count)
        # VoucherWord: root (items, totalsize)
        # ItemClass: root (list, count)
        # Item: root (list, count)
        
        return model_class(**response)

    def get_system_profile(self, key: str) -> SystemProfileResponse:
        """
        获取系统参数
        Path: /jdyaccouting/profile
        """
        endpoint = "/jdyaccouting/profile"
        params = {"key": key}
        response = self.client.get(endpoint, params=params)
        return self._handle_response(response, SystemProfileResponse)

    def get_account_subjects(self, 
                             number: Optional[str] = None,
                             name: Optional[str] = None,
                             groupName: Optional[str] = None,
                             classId: Optional[str] = None
                             ) -> AccountSubjectListResponse:
        """
        获取科目列表
        Path: /jdyaccouting/account
        """
        endpoint = "/jdyaccouting/account"
        params = {}
        if number: params["number"] = number
        if name: params["name"] = name
        if groupName: params["groupName"] = groupName
        if classId: params["classId"] = classId
        
        response = self.client.get(endpoint, params=params)
        return self._handle_response(response, AccountSubjectListResponse)

    def save_account_subject(self, subjects: List[AccountSubjectSaveRequest]) -> Dict[str, Any]:
        """
        保存科目
        Path: /jdyaccouting/account
        Note: Document says body is a list.
        """
        endpoint = "/jdyaccouting/account"
        payload = [s.model_dump(exclude_none=True) for s in subjects]
        response = self.client.post(endpoint, data=payload)
        return response # Return raw response or specific model if needed

    def get_voucher_words(self, page: int = 1, page_size: int = 100) -> VoucherWordListResponse:
        """
        查询凭证字
        Path: /jdyaccouting/generateCode/list
        Method: POST
        """
        endpoint = "/jdyaccouting/generateCode/list"
        payload = {"page": page, "pageSize": page_size}
        response = self.client.post(endpoint, data=payload)
        return self._handle_response(response, VoucherWordListResponse)

    def get_auxiliary_item_classes(self) -> AuxiliaryItemClassListResponse:
        """
        获取辅助核算类别列表
        Path: /jdyaccouting/itemclass/query
        """
        endpoint = "/jdyaccouting/itemclass/query"
        response = self.client.get(endpoint)
        return self._handle_response(response, AuxiliaryItemClassListResponse)

    def get_auxiliary_items(self, 
                            itemClsName: Optional[str] = None,
                            number: Optional[str] = None,
                            name: Optional[str] = None,
                            isDeleted: Optional[str] = None,
                            page: Optional[int] = None,
                            pageSize: Optional[int] = None
                            ) -> AuxiliaryItemListResponse:
        """
        查询辅助核算列表
        Path: /jdyaccouting/item
        """
        endpoint = "/jdyaccouting/item"
        params = {}
        if itemClsName: params["itemClsName"] = itemClsName
        if number: params["number"] = number
        if name: params["name"] = name
        if isDeleted: params["isDeleted"] = isDeleted
        if page: params["page"] = str(page)
        if pageSize: params["pageSize"] = str(pageSize)
        
        response = self.client.get(endpoint, params=params)
        return self._handle_response(response, AuxiliaryItemListResponse)

    def save_auxiliary_items(self, items: List[AuxiliaryItemSaveRequest]) -> Dict[str, Any]:
        """
        保存辅助核算
        Path: /jdyaccouting/item
        Method: POST
        """
        endpoint = "/jdyaccouting/item"
        payload = [item.model_dump(exclude_none=True) for item in items]
        response = self.client.post(endpoint, data=payload)
        return response

    def delete_auxiliary_items(self, item_class_name: str, number_array: List[str]) -> Dict[str, Any]:
        """
        删除辅助核算
        Path: /jdyaccouting/item
        Method: DELETE
        Body: { itemClassName: ..., numberArray: [...] }
        """
        endpoint = "/jdyaccouting/item"
        payload = {
            "itemClassName": item_class_name,
            "numberArray": number_array
        }
        # DELETE with body ? python requests supports it.
        response = self.client.delete(endpoint, data=payload)
        return response
