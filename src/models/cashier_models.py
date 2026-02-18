from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field, validator

# --- Cashier Journal Models (出纳日记账) ---

class CashierJournalItem(BaseModel):
    """
    Model for Cashier Journal Item (used in Add/Update).
    """
    cashierAccountNumber: str = Field(..., description="出纳账户编码")
    date: str = Field(..., description="日期")
    explanation: str = Field(..., description="摘要")
    credit: Union[float, str] = Field(..., description="支出金额")
    debit: Union[float, str] = Field(..., description="收入金额")
    serialNum: Optional[str] = Field(None, description="流水号")
    accountName: Optional[str] = Field(None, description="对方账户名称")
    accountNo: Optional[str] = Field(None, description="对方账号")
    accountNumber: Optional[str] = Field(None, description="对方科目编号")
    accountItem: Optional[str] = Field(None, description="对方科目辅助核算列")
    bankField: Optional[str] = Field(None, description="对方银行")
    remark: Optional[str] = Field(None, description="备注")
    id: Optional[int] = Field(None, description="ID (required for update)")

    @validator('credit', 'debit', pre=True, allow_reuse=True)
    def convert_to_string(cls, v):
        return str(v)

class CashierJournalListItem(BaseModel):
    """
    Model for Cashier Journal Item in List Response.
    """
    id: int
    date: str
    serialNum: Optional[str] = None
    explanation: Optional[str] = None
    remark: Optional[str] = None
    bankField: Optional[str] = None
    accountNo: Optional[str] = None
    accountName: Optional[str] = None
    balance: Optional[float] = None
    credit: Optional[float] = None
    debit: Optional[float] = None
    voucherNo: Optional[str] = None
    dcType: Optional[str] = None # e.g. "借", "贷", "平"
    # Additional fields from example
    ymd: Optional[str] = None
    currency: Optional[str] = None

class CashierJournalListResponse(BaseModel):
    """
    Response model for Get Journal List.
    """
    total: int
    items: List[CashierJournalListItem]

class JournalOperationSuccessItem(BaseModel):
    id: Optional[int] = None
    date: Optional[str] = None
    cashierAccountNumber: Optional[str] = None
    explanation: Optional[str] = None
    credit: Optional[float] = None
    debit: Optional[float] = None
    # Add other fields as needed from success list

class JournalOperationFailItem(BaseModel):
    id: Optional[int] = None
    msg: Optional[str] = None
    # Add other fields as needed

class CashierJournalOperationResponse(BaseModel):
    """
    Response model for Add/Update/Delete Journal.
    """
    failedList: Optional[List[JournalOperationFailItem]] = []
    succeedList: Optional[List[Union[JournalOperationSuccessItem, int]]] = [] # Delete returns list of IDs (int) sometimes?
    # Doc for delete says succeedList: [10000000004, ...], so it can be list of ints.
    # But Add/Update returns objects.

# --- Cashier Account Models (出纳账户) ---

class CashierAccountItem(BaseModel):
    """
    Model for Cashier Account Item (used in Add/Update).
    """
    number: str = Field(..., description="账户编码")
    name: str = Field(..., description="账户名称")
    type: Union[str, int] = Field(..., description="账户类型（1：现金账户 2：银行账户）")
    bankNo: Optional[str] = Field(None, description="银行账号（只对作用于银行账户）")
    isForbid: Optional[Union[str, int]] = Field(0, description="是否禁用 （0：启用；1：禁用）")
    id: Optional[int] = Field(None, description="账户id (required for update)")

class CashierAccountListItem(CashierAccountItem):
    """
    Model for Cashier Account in List Response.
    """
    accountId: Optional[int] = None
    cur: Optional[str] = None
    # Override id to be int if coming from API
    id: Optional[int] = None

class CashierAccountListResponse(BaseModel):
    """
    Response model for Get Account List.
    """
    count: int
    list: List[CashierAccountListItem]

class AccountOperationSuccessItem(CashierAccountItem):
    accountId: Optional[int] = None
    cur: Optional[str] = None
    curName: Optional[str] = None
    curId: Optional[int] = None
    isItem: Optional[int] = None

class AccountOperationFailItem(BaseModel):
    number: Optional[str] = None
    name: Optional[str] = None
    code: Optional[int] = None
    msg: Optional[str] = None

class CashierAccountOperationResponse(BaseModel):
    """
    Response model for Add/Update Account.
    """
    failedList: Optional[List[AccountOperationFailItem]] = []
    succeedList: Optional[List[AccountOperationSuccessItem]] = []

class CashierAccountDeleteResponse(BaseModel):
    """
    Response model for Delete Account.
    """
    failed: Optional[List[Dict[str, Any]]] = []
    succeed: Optional[List[str]] = [] # List of account numbers
