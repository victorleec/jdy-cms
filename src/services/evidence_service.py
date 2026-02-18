import os
from typing import Dict, Any, List, Optional
from src.api.client import client

class EvidenceService:
    def upload_evidence(self, file_path: str, period: int, file_name: str = None) -> Dict[str, Any]:
        """
        上传原始凭证
        POST /jdyaccouting/evidence/upload
        
        Args:
            file_path: absolute path to the file
            period: accounting period, e.g., 202102
            file_name: optional, defaults to basename of file_path
        """
        if not file_name:
            file_name = os.path.basename(file_path)
        
        file_size = os.path.getsize(file_path)
        
        # Based on API docs, these parameters are passed in the query string
        params = {
            "fileName": file_name,
            "fileSize": file_size,
            "period": period
        }
        
        # 'newfile' based on "body参数" description in docs.
        # We need to ensure we don't send JSON content-type.
        with open(file_path, "rb") as f:
            files = {"newfile": (file_name, f)}
            
            # Using client.request to have full control.
            # Pass 'Content-Type': None to headers to allow requests to set boundary.
            return client.request(
                "POST", 
                "/jdyaccouting/evidence/upload", 
                params=params, 
                files=files,
                headers={"Content-Type": None}
            )

    def attach_evidence(self, voucher_id: int, evidence_ids: List[int]) -> Dict[str, Any]:
        """
        绑定原始凭证到凭证
        POST /jdyaccouting/evidence/attach
        """
        # Doc says evidIds: "number", "multiple separated by comma"
        evid_ids_str = ",".join(str(e) for e in evidence_ids)
        params = {
            "voucherId": voucher_id,
            "evidIds": evid_ids_str
        }
        return client.post("/jdyaccouting/evidence/attach", params=params)

    def unattach_evidence(self, evidence_id: str, file_id: str) -> Dict[str, Any]:
        """
        解绑原始凭证
        POST /jdyaccouting/evidence/unattach
        """
        params = {
            "evidId": evidence_id,
            "fileId": file_id
        }
        return client.post("/jdyaccouting/evidence/unattach", params=params)
        
    def get_evidence_list(self, 
                          begin_period: str, 
                          end_period: str, 
                          is_class: Optional[int] = None, 
                          is_voucher: Optional[int] = None) -> Dict[str, Any]:
        """
        查询原始凭证列表
        POST /jdyaccouting/evidence/list
        """
        params = {
            "beginYearPeriod": begin_period,
            "endYearPeriod": end_period
        }
        if is_class is not None:
            params["isClass"] = is_class
        if is_voucher is not None:
            params["isVoucher"] = is_voucher
            
        return client.post("/jdyaccouting/evidence/list", params=params)

    def get_attachment_list(self,
                            begin_period: str,
                            end_period: str,
                            is_class: Optional[int] = None,
                            is_voucher: Optional[int] = None) -> Dict[str, Any]:
        """
        查询附件列表
        POST /jdyaccouting/evidence/attachmentList
        """
        params = {
            "beginYearPeriod": begin_period,
            "endYearPeriod": end_period
        }
        if is_class is not None:
            params["isClass"] = is_class
        if is_voucher is not None:
            params["isVoucher"] = is_voucher
            
        return client.post("/jdyaccouting/evidence/attachmentList", params=params)

evidence_service = EvidenceService()
