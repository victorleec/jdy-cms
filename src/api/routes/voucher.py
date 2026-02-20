"""
凭证 & 原始凭证路由
"""
import os
import tempfile
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from src.api.dependencies import verify_api_key
from src.models.voucher import VoucherCreate, VoucherQueryFilter
from src.services.voucher_service import voucher_service
from src.services.evidence_service import evidence_service

router = APIRouter(prefix="/voucher", tags=["凭证"], dependencies=[Depends(verify_api_key)])

# ========== 凭证 ==========


@router.post("/list", summary="凭证查询")
def get_voucher_list(filter_data: VoucherQueryFilter):
    """查询凭证列表，支持按期间、凭证字、状态等条件筛选。"""
    return voucher_service.get_voucher_list(filter_data)


@router.post("/save", summary="凭证保存")
def save_vouchers(vouchers: List[VoucherCreate]):
    """批量创建/保存凭证。"""
    return voucher_service.save_vouchers(vouchers)


@router.post("/reverse", summary="凭证冲销")
def reverse_vouchers(voucher_ids: List[int]):
    """冲销指定凭证（生成红字凭证）。"""
    return voucher_service.reverse_vouchers(voucher_ids)


@router.post("/delete", summary="凭证删除")
def delete_vouchers(voucher_ids: List[int]):
    """批量删除凭证。"""
    return voucher_service.delete_vouchers(voucher_ids)


@router.get("/summary", summary="凭证汇总表")
def get_voucher_summary(
    from_date: str = Query(..., description="起始日期"),
    to_date: str = Query(..., description="结束日期"),
):
    """查询凭证汇总表。"""
    return voucher_service.get_voucher_summary(from_date, to_date)


# ========== 原始凭证 ==========

evidence_router = APIRouter(prefix="/evidence", tags=["原始凭证"], dependencies=[Depends(verify_api_key)])


@evidence_router.post("/upload", summary="原始凭证上传")
async def upload_evidence(
    file: UploadFile = File(..., description="上传的文件"),
    period: int = Form(..., description="会计期间，如 202301"),
    file_name: Optional[str] = Form(None, description="文件名（默认使用上传文件名）"),
):
    """上传原始凭证文件。"""
    actual_name = file_name or file.filename
    # 将上传文件保存到临时目录，调用底层服务
    suffix = os.path.splitext(actual_name)[1] if actual_name else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = evidence_service.upload_evidence(tmp_path, period, actual_name)
    finally:
        os.unlink(tmp_path)

    return result


@evidence_router.post("/attach", summary="原始凭证绑定")
def attach_evidence(voucher_id: int, evidence_ids: List[int]):
    """将原始凭证绑定到指定凭证。"""
    return evidence_service.attach_evidence(voucher_id, evidence_ids)


@evidence_router.post("/unattach", summary="原始凭证解绑")
def unattach_evidence(evidence_id: str, file_id: str):
    """解绑原始凭证。"""
    return evidence_service.unattach_evidence(evidence_id, file_id)


@evidence_router.post("/list", summary="原始凭证查询")
def get_evidence_list(
    begin_period: str = Query(..., description="起始期间，如 202301"),
    end_period: str = Query(..., description="结束期间，如 202312"),
    is_class: Optional[int] = Query(None, description="是否按分类"),
    is_voucher: Optional[int] = Query(None, description="是否关联凭证"),
):
    """查询原始凭证列表。"""
    return evidence_service.get_evidence_list(begin_period, end_period, is_class, is_voucher)


@evidence_router.post("/attachment-list", summary="附件查询")
def get_attachment_list(
    begin_period: str = Query(..., description="起始期间，如 202301"),
    end_period: str = Query(..., description="结束期间，如 202312"),
    is_class: Optional[int] = Query(None, description="是否按分类"),
    is_voucher: Optional[int] = Query(None, description="是否关联凭证"),
):
    """查询附件列表。"""
    return evidence_service.get_attachment_list(begin_period, end_period, is_class, is_voucher)
