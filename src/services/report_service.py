from typing import List, Dict, Any, Union, Optional
from src.api.client import client
from src.models.report_models import (
    ReportResponseData, 
    BalanceSheetResponseData,
    ExpenseDetailResponseData, 
    TaxPayableResponseData
)

class ReportService:
    def get_profit_statement(self, start_period: int, end_period: int) -> Dict[str, Any]:
        """
        查询利润表
        GET /jdyaccouting/report
        reportType=2
        """
        params = {
            "reportType": 2,
            "startPeriod": start_period,
            "endPeriod": end_period
        }
        return client.get("/jdyaccouting/report", params=params)

    def get_balance_sheet(self, start_period: int, end_period: int) -> Dict[str, Any]:
        """
        查询资产负债表
        GET /jdyaccouting/report
        reportType=1
        """
        params = {
            "reportType": 1,
            "startPeriod": start_period,
            "endPeriod": end_period
        }
        return client.get("/jdyaccouting/report", params=params)

    def get_cash_flow_statement(self, start_period: int, end_period: int) -> Dict[str, Any]:
        """
        查询现金流量表
        GET /jdyaccouting/report
        reportType=3
        """
        params = {
            "reportType": 3,
            "startPeriod": start_period,
            "endPeriod": end_period
        }
        return client.get("/jdyaccouting/report", params=params)

    def get_expense_detail(
        self, 
        from_period: int,
        to_period: int, 
        account_num: int, 
        show_type: int = 1, 
        show_item: int = 0
    ) -> Dict[str, Any]:
        """
        查询费用明细表
        GET /jdyaccouting/report/expenseDetail
        (Doc says POST but example uses GET params, trying GET first)
        """
        params = {
            "fromPeriod": from_period,
            "toPeriod": to_period,
            "accountNum": account_num,
            "showType": show_type,
            "showItem": show_item
        }
        return client.get("/jdyaccouting/report/expenseDetail", params=params)

    def get_tax_payable_detail(self, period: int) -> Dict[str, Any]:
        """
        查询主要应交税金明细表
        GET /jdyaccouting/report/taxPayableDetail
        """
        params = {
            "period": period
        }
        return client.get("/jdyaccouting/report/taxPayableDetail", params=params)

report_service = ReportService()
