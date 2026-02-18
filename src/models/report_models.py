from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field

# --- Common Reporting Models ---

class ReportItemBase(BaseModel):
    """Base model for report items with row, col, and name."""
    row: int = Field(..., description="Row number")
    col: Optional[int] = Field(None, description="Column number") # Some reports might not have col
    name: str = Field(..., description="Item name")

# --- Profit Statement Models (Report type 2) & Cash Flow (Report type 3) ---
# They share the same structure: value (current period), ytdValue (year to date)

class ProfitAndCashFlowItem(ReportItemBase):
    """Item for Profit Statement and Cash Flow Statement."""
    value: Union[float, str] = Field(..., description="Current period amount")
    ytdValue: Union[float, str] = Field(..., description="Year to date amount")

class ReportValue(BaseModel):
    """Container for a specific period's report data."""
    date: int = Field(..., description="Period, e.g., 201901")
    items: List[ProfitAndCashFlowItem]

class ReportResponseData(BaseModel):
    """Generic data structure for report responses (Profit, Balance, Cash Flow)."""
    reportValues: List[ReportValue]
    fdbid: Optional[str] = Field(None, description="Financial DB ID")

# --- Balance Sheet Models (Report type 1) ---

class BalanceSheetItem(ReportItemBase):
    """Item for Balance Sheet."""
    yearOpeningBalance: Union[float, str] = Field(..., description="Year opening balance")
    balance: Union[float, str] = Field(..., description="Closing balance")

class BalanceSheetReportValue(BaseModel):
    date: int
    items: List[BalanceSheetItem]

class BalanceSheetResponseData(BaseModel):
    reportValues: List[BalanceSheetReportValue]
    fdbid: Optional[str]

# --- Expense Detail Models ---

class ExpenseDetailItem(BaseModel):
    """Item for Expense Detail Report."""
    period_expense: Dict[str, Union[float, str]] = Field(..., description="Expense by period, e.g. {'201904': 0}")
    number: Union[str, int] = Field(..., description="Account number") # API doc says number, example 5301
    accountId: int = Field(..., description="Account ID")
    level: int = Field(..., description="Account level")
    name: str = Field(..., description="Account name")
    id: Optional[int] = None
    isLeaf: bool = Field(..., description="Is leaf node")
    parentId: int
    dc: Optional[int] = None # Direction?
    yearTotal: Union[float, str] = Field(..., description="Year total")

class ExpenseDetailResponseData(BaseModel):
    totalsize: int = Field(alias="total") # API doc says 'total', example 'totalsize'? Let's support alias if needed or check example.
    # The example shows "totalsize": 5, doc says "total". We should allow both or check. 
    # Let's trust the example "totalsize" but `total` in doc.
    # Pydantic alias can handle this.
    items: List[ExpenseDetailItem]

# --- Tax Payable Detail Models ---

class TaxPayableItem(BaseModel):
    """Item for Tax Payable Report."""
    item: str = Field(..., description="Tax item name")
    row: Union[int, str] = Field(..., description="Row number/id")
    value: Optional[Union[float, str]] = Field(None, description="Current period value")
    yearTotal: Optional[Union[float, str]] = Field(None, description="Year total value")

class TaxPayableResponseData(BaseModel):
    totalsize: int = Field(alias="total") 
    items: List[TaxPayableItem]
