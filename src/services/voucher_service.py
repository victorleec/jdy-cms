from typing import List, Dict, Any, Union
from src.api.client import client
from src.models.voucher import VoucherCreate, VoucherQueryFilter

class VoucherService:
    def get_voucher_list(self, filter_data: VoucherQueryFilter) -> Dict[str, Any]:
        """
        查询凭证列表
        POST /jdyaccouting/voucherlist
        """
        # The API expects parameters in body for this POST request
        return client.post("/jdyaccouting/voucherlist", data=filter_data.model_dump(exclude_none=True))

    def save_vouchers(self, vouchers: List[VoucherCreate]) -> Dict[str, Any]:
        """
        保存/创建凭证 (批量)
        POST /jdyaccouting/voucher
        """
        # API requires a List as the root body
        payload = [v.model_dump(exclude_none=True) for v in vouchers]
        return client.post("/jdyaccouting/voucher", data=payload)

    def delete_vouchers(self, voucher_ids: List[int | str]) -> Dict[str, Any]:
        """
        删除凭证
        DELETE /jdyaccouting/voucher
        Body: { idSet: [...] }
        """
        # requests.delete usually supports json/data
        # Our client.request handles 'json' if passed.
        # But requests.delete signature in wrapper might need check.
        # Base client wraps 'request', so we can pass json.
        return client.request("DELETE", "/jdyaccouting/voucher", json={"idSet": voucher_ids})

    def reverse_vouchers(self, voucher_ids: List[int | str]) -> Dict[str, Any]:
        """
        冲销凭证
        POST /jdyaccouting/voucher
        Params: isReverse=1
        Body: { vchId: "id1,id2" } -> Note: Doc says "Multiple IDs separated by comma" in vchId field.
        """
        # Format IDs: "123,456"
        ids_str = ",".join(str(i) for i in voucher_ids)
        
        # Doc: Body parameter: vchId (String)
        payload = {"vchId": ids_str}
        
        # Param: isReverse=1
        return client.post("/jdyaccouting/voucher", params={"isReverse": 1}, data=payload)

    def get_voucher_summary(self, from_date: str, to_date: str, action: str = "getVchTotalQuery") -> Dict[str, Any]:
        """
        凭证汇总表
        GET /jdyaccouting/voucher
        Params: action=getVchTotalQuery, fromDate, toDate
        """
        params = {
            "action": action,
            "fromDate": from_date,
            "toDate": to_date
        }
        return client.get("/jdyaccouting/voucher", params=params)

voucher_service = VoucherService()
