import requests
from typing import Any, Dict, Optional

from src.config.settings import settings
from src.api.auth import auth_manager

class KingdeeClient:
    def __init__(self):
        self.session = requests.Session()
        # Header configuration
        self.session.headers.update({
            "Content-Type": "application/json",
            # X-GW-Router-Addr is required. 
            # We assume it's configured in settings or we might need to fetch it.
            # For now, let's allow passing it or set from env.
            # "X-GW-Router-Addr": settings.JDY_ROUTER_ADDR # If we add this to settings
        })
    
    def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        Wrapper for requests. 
        Automatically injects access_token, dbId, sId into params.
        """
        # 1. Get Token
        token = auth_manager.get_access_token()
        
        # 2. Prepare URL
        # Path should be relative, e.g., '/jdyaccouting/voucherlist'
        url = f"{settings.JDY_API_BASE_URL}{path}"
        
        # 3. Inject Common Params
        params = kwargs.get("params", {})
        params.update({
            "access_token": token,
            "dbId": settings.JDY_ENTERPRISE_ID,
            "sId": settings.JDY_SERVICE_ID
        })
        kwargs["params"] = params
        
        # 4. Check Router Address
        # The doc says `X-GW-Router-Addr` header is required.
        if settings.JDY_IDC_DOMAIN:
            kwargs.setdefault("headers", {})
            kwargs["headers"]["X-GW-Router-Addr"] = settings.JDY_IDC_DOMAIN
        
        # 5. Execute
        response = self.session.request(method, url, **kwargs)
        
        # 6. Error Handling
        if response.status_code >= 400:
            # Handle standard HTTP errors
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
            
        data = response.json()
        
        # Check Business Errors (code != 0)
        # Some APIs use 'code', some 'errcode'. Accounting seems to use 'code'.
        if "code" in data and str(data["code"]) != "0":
            # 尝试从 list 中提取详细错误信息（批量操作时金蝶返回 list[0].msg）
            detail_msg = data.get('msg') or data.get('description')
            if isinstance(data.get('list'), list) and data['list']:
                item = data['list'][0]
                if item.get('msg'):
                    detail_msg = item['msg']
            raise Exception(f"API Error {data['code']}: {detail_msg}")
             
        return data

    def post(self, path: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        return self.request("POST", path, json=data, **kwargs)

    def get(self, path: str, **kwargs) -> Dict[str, Any]:
        return self.request("GET", path, **kwargs)

    def delete(self, path: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        return self.request("DELETE", path, json=data, **kwargs)

client = KingdeeClient()
