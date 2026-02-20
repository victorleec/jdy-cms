"""
出纳路由
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from src.api.dependencies import verify_api_key
from src.models.cashier_models import CashierJournalItem, CashierAccountItem
from src.services.cashier_service import cashier_service

router = APIRouter(prefix="/cashier", tags=["出纳"], dependencies=[Depends(verify_api_key)])

# ========== 日记账 ==========


@router.get("/journal/list", summary="日记账查询")
def get_journal_list(
    period: str = Query(..., description="会计期间，如 202301"),
    cashier_account_number: str = Query(..., alias="cashierAccountNumber", description="出纳账户编码"),
    include_vch: Optional[str] = Query(None, alias="includeVch", description="0:未生成凭证 1:仅生成凭证 空:全部"),
):
    """查询日记账列表。"""
    return cashier_service.get_journal_list(period, cashier_account_number, include_vch)


@router.post("/journal/add", summary="日记账新增")
def save_journal(items: List[CashierJournalItem]):
    """批量新增日记账条目。"""
    return cashier_service.save_journal(items)


@router.post("/journal/update", summary="日记账修改")
def update_journal(items: List[CashierJournalItem]):
    """批量修改日记账条目（需包含 id 字段）。"""
    return cashier_service.update_journal(items)


@router.post("/journal/delete", summary="日记账删除")
def delete_journal(ids: List[int]):
    """批量删除日记账条目。"""
    return cashier_service.delete_journal(ids)


# ========== 账户 ==========


@router.get("/account/list", summary="账户查询")
def get_account_list(
    type: int = Query(..., description="账户类型（1:现金账户 2:银行账户）"),
    is_forbid: Optional[int] = Query(None, alias="isForbid", description="0:启用 1:禁用"),
):
    """查询出纳账户列表。"""
    return cashier_service.get_account_list(type, is_forbid)


@router.post("/account/add", summary="账户新增")
def save_account(items: List[CashierAccountItem]):
    """批量新增出纳账户。"""
    return cashier_service.save_account(items)


@router.post("/account/update", summary="账户修改")
def update_account(items: List[CashierAccountItem]):
    """批量修改出纳账户（需包含 id 字段）。"""
    return cashier_service.update_account(items)


@router.post("/account/delete", summary="账户删除")
def delete_account(numbers: List[str]):
    """批量删除出纳账户（按编码）。"""
    return cashier_service.delete_account(numbers)
