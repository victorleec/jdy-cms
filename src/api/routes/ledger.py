"""
账簿路由
"""
from fastapi import APIRouter, Depends
from src.api.dependencies import verify_api_key
from src.api.client import client
from src.models.ledger_models import (
    SubjectBalanceRequest,
    DetailLedgerRequest,
    QtyAmountDetailRequest,
    QtyAmountTotalRequest,
    ItemBalanceRequest,
    ItemDetailRequest,
    CombinationRequest,
    GeneralLedgerRequest,
)
from src.services.ledger_service import LedgerService

router = APIRouter(prefix="/ledger", tags=["账簿"], dependencies=[Depends(verify_api_key)])

# LedgerService 需要传入 client 实例
_ledger_service = LedgerService(client)


@router.post("/account-balance", summary="科目余额表")
def get_account_balance(request: SubjectBalanceRequest):
    """查询科目余额表，支持按期间、科目范围、级别筛选。"""
    result = _ledger_service.get_account_balance(request)
    return result.model_dump()


@router.post("/detail", summary="明细账")
def get_detail_ledger(request: DetailLedgerRequest):
    """查询明细账，需指定科目编号。"""
    result = _ledger_service.get_detail_ledger(request)
    return result.model_dump()


@router.post("/qty-amount-detail", summary="数量金额明细账")
def get_qty_amount_detail(request: QtyAmountDetailRequest):
    """查询数量金额明细账。"""
    result = _ledger_service.get_qty_amount_detail(request)
    return result.model_dump()


@router.post("/qty-amount-total", summary="数量金额总账")
def get_qty_amount_total(request: QtyAmountTotalRequest):
    """查询数量金额总账。"""
    result = _ledger_service.get_qty_amount_total(request)
    return result.model_dump()


@router.post("/item-balance", summary="核算项目余额表")
def get_item_balance(request: ItemBalanceRequest):
    """查询核算项目余额表，需指定辅助核算类型。"""
    result = _ledger_service.get_item_balance(request)
    return result.model_dump()


@router.post("/item-detail", summary="核算项目明细账")
def get_item_detail(request: ItemDetailRequest):
    """查询核算项目明细账，需指定辅助核算类型和编码。"""
    result = _ledger_service.get_item_detail(request)
    return result.model_dump()


@router.post("/combination", summary="核算项目组合表")
def get_combination(request: CombinationRequest):
    """查询核算项目组合表。"""
    result = _ledger_service.get_combination(request)
    return result.model_dump()


@router.post("/general", summary="总账")
def get_general_ledger(request: GeneralLedgerRequest):
    """查询总账。"""
    result = _ledger_service.get_general_ledger(request)
    return result.model_dump()
