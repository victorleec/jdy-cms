"""
报表路由
"""
from fastapi import APIRouter, Depends, Query
from src.api.dependencies import verify_api_key
from src.services.report_service import report_service

router = APIRouter(prefix="/report", tags=["报表"], dependencies=[Depends(verify_api_key)])


@router.get("/profit", summary="利润表")
def get_profit_statement(
    start_period: int = Query(..., description="起始期间，如 202301"),
    end_period: int = Query(..., description="结束期间，如 202312"),
):
    """查询利润表。"""
    return report_service.get_profit_statement(start_period, end_period)


@router.get("/balance-sheet", summary="资产负债表")
def get_balance_sheet(
    start_period: int = Query(..., description="起始期间，如 202301"),
    end_period: int = Query(..., description="结束期间，如 202312"),
):
    """查询资产负债表。"""
    return report_service.get_balance_sheet(start_period, end_period)


@router.get("/cash-flow", summary="现金流量表")
def get_cash_flow_statement(
    start_period: int = Query(..., description="起始期间，如 202301"),
    end_period: int = Query(..., description="结束期间，如 202312"),
):
    """查询现金流量表。"""
    return report_service.get_cash_flow_statement(start_period, end_period)


@router.get("/expense-detail", summary="费用明细表")
def get_expense_detail(
    from_period: int = Query(..., description="起始期间"),
    to_period: int = Query(..., description="结束期间"),
    account_num: int = Query(..., description="科目编码"),
    show_type: int = Query(1, description="显示方式"),
    show_item: int = Query(0, description="是否显示明细"),
):
    """查询费用明细表。"""
    return report_service.get_expense_detail(from_period, to_period, account_num, show_type, show_item)


@router.get("/tax-payable", summary="主要应交税金明细表")
def get_tax_payable_detail(
    period: int = Query(..., description="会计期间，如 202301"),
):
    """查询主要应交税金明细表。"""
    return report_service.get_tax_payable_detail(period)
