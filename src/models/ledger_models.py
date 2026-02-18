
from typing import List, Optional, Any, Union
from pydantic import BaseModel, Field

# --- Common Request Models ---

class BaseLedgerRequest(BaseModel):
    """
    账簿查询通用请求参数
    Common request parameters for ledger queries.
    """
    fromPeriod: str = Field(..., description="开始期间 (e.g., 202301)")
    toPeriod: str = Field(..., description="结束期间 (e.g., 202301)")
    currency: Optional[str] = Field(None, description="币别 (e.g., RMB)")

# --- 1. Subject Balance (科目余额表) ---

class SubjectBalanceRequest(BaseLedgerRequest):
    """
    科目余额表请求参数
    /jdyaccouting/account/balance
    """
    fromAccountId: Optional[int] = Field(None, description="起始科目ID")
    toAccountId: Optional[int] = Field(None, description="结束科目ID")
    happen: Optional[int] = Field(None, description="包括无发生额且余额为0数据 (0:不显示, 1:显示)")
    fromLevel: Optional[int] = Field(None, description="科目最小级数")
    toLevel: Optional[int] = Field(None, description="科目最大级数")

# --- Helper for Loose Types ---
from typing import Union

Num = Union[float, str, int, None]
Bool = Union[bool, str, int, None]
Int = Union[int, str, None]

class SubjectBalanceItem(BaseModel):
    id: Int = Field(..., description="唯一标识ID")
    number: str = Field(..., description="科目编码")
    name: Optional[str] = Field(None, description="科目名称", alias="accountname") 
    # accountname: Optional[str] = None # Removed due to alias conflict
    level: Int = None
    isLeaf: Bool = None
    parentId: Int = None
    
    # Amounts
    beginDebit: Num = 0.0
    beginCredit: Num = 0.0
    debit: Num = 0.0
    credit: Num = 0.0
    ytdDebit: Num = 0.0
    ytdCredit: Num = 0.0
    endDebit: Num = 0.0
    endCredit: Num = 0.0
    
    # Foreign Currency (Optional)
    beginDebitFor: Num = 0.0
    beginCreditFor: Num = 0.0
    debitFor: Num = 0.0
    creditFor: Num = 0.0
    ytdDebitFor: Num = 0.0
    ytdCreditFor: Num = 0.0
    endDebitFor: Num = 0.0
    endCreditFor: Num = 0.0

class SubjectBalanceResponse(BaseModel):
    totalsize: Int = 0
    items: List[SubjectBalanceItem] = []

# --- 2. Detail Ledger (明细账) ---

class DetailLedgerRequest(BaseLedgerRequest):
    """
    明细账请求参数
    /jdyaccouting/querydetail
    """
    accountNum: str = Field(..., description="科目编号")

class DetailLedgerItem(BaseModel):
    ymd: Union[str, int] = Field(..., description="日期")
    yearPeriod: Int = Field(..., description="会计期间")
    voucherNo: Optional[str] = None
    remark: Optional[str] = None
    
    debit: Num = 0.0
    credit: Num = 0.0
    balance: Num = 0.0
    dcType: Optional[str] = None
    dc: Int = None
    
    # Currency
    currency: Optional[str] = None
    rate: Num = None
    debitFor: Num = 0.0
    creditFor: Num = 0.0
    balanceFor: Num = 0.0
    
    # Check for unexpected fields in Validation if strictly required? No, Pydantic ignores extra by default.

class DetailLedgerResponse(BaseModel):
    totalsize: Int = 0
    items: List[DetailLedgerItem] = []

# --- 3. Qty Amount Detail (数量金额明细账) ---

class QtyAmountDetailRequest(BaseLedgerRequest):
    """
    数量金额明细账请求参数
    /jdyaccouting/report/qtyamountdetail
    """
    accountNum: Optional[str] = None
    amountPlaces: Optional[int] = None
    pricePlaces: Optional[int] = None
    balance: Optional[int] = None
    happen: Optional[int] = None
    fromLevel: Optional[int] = None
    toLevel: Optional[int] = None

class QtyAmountDetailItem(BaseModel):
    data: Optional[str] = None
    explanation: Optional[str] = None
    voucherNo: Optional[str] = None
    
    creditAmount: Num = 0.0
    creditPrice: Num = 0.0
    creditQty: Num = 0.0
    
    debitAmount: Num = 0.0
    debitPrice: Num = 0.0
    debitQty: Num = 0.0
    
    balance: Num = 0.0
    price: Num = 0.0
    qty: Num = 0.0
    ddc: Optional[str] = None

class QtyAmountDetailResponse(BaseModel):
    total: Int = 0
    items: List[QtyAmountDetailItem] = []

# --- 4. Qty Amount Total (数量金额总账) ---

class QtyAmountTotalRequest(BaseLedgerRequest):
    """
    数量金额总账请求参数
    /jdyaccouting/report/qtyamounttotal
    """
    accountNum: Optional[str] = None
    fromLevel: Optional[int] = None
    toLevel: Optional[int] = None
    includeItem: Optional[int] = None
    amountPlaces: Optional[int] = None
    pricePlaces: Optional[int] = None
    balance: Optional[int] = None
    happen: Optional[int] = None

class QtyAmountTotalItem(BaseModel):
    accountnumber: str
    accountname: str
    unit: Optional[str] = None
    
    debitqty: Num = 0.0
    debit: Num = 0.0
    creditqty: Num = 0.0
    credit: Num = 0.0
    ytddebitqty: Num = 0.0
    ytddebit: Num = 0.0
    ytdcreditqty: Num = 0.0
    ytdcredit: Num = 0.0
    endqty: Num = 0.0
    endnprice: Num = 0.0
    endbalance: Num = 0.0
    ddc: Optional[str] = None
    beginqty: Num = 0.0
    beginprice: Num = 0.0
    beginbalance: Num = 0.0
    dc: Optional[str] = None

class QtyAmountTotalResponse(BaseModel):
    total: Int = 0
    items: List[QtyAmountTotalItem] = []

# --- 5. Item Balance (核算项目余额表) ---

class ItemBalanceRequest(BaseLedgerRequest):
    """
    核算项目余额表请求参数
    /jdyaccouting/report/itembalance
    """
    auxiliaryType: str
    auxiliaryNum: Optional[str] = None
    accountNum: Optional[str] = None
    includeItem: Optional[int] = None
    amountPlaces: Optional[int] = None
    pricePlaces: Optional[int] = None
    balance: Optional[int] = None
    happen: Optional[int] = None

class ItemBalanceItem(BaseModel):
    itemNumber: Optional[str] = None
    name: Optional[str] = None
    beginDebit: Num = 0.0
    beginCredit: Num = 0.0
    debit: Num = 0.0
    credit: Num = 0.0
    ytdDebit: Num = 0.0
    ytdCredit: Num = 0.0
    endDebit: Num = 0.0
    endCredit: Num = 0.0

class ItemBalanceResponse(BaseModel):
    total: Int = 0
    items: List[ItemBalanceItem] = []

# --- 6. Item Detail (核算项目明细账) ---

class ItemDetailRequest(BaseLedgerRequest):
    """
    核算项目明细账请求参数
    /jdyaccouting/report/itemdetail
    """
    auxiliaryType: str
    auxiliaryNum: str
    accountNum: Optional[str] = None
    includeItem: Optional[int] = None
    amountPlaces: Optional[int] = None
    pricePlaces: Optional[int] = None
    balance: Optional[int] = None
    happen: Optional[int] = None

class ItemDetailItem(BaseModel):
    ymd: Union[str, int]
    voucherNo: Optional[str] = None
    remark: Optional[str] = None
    dc: Optional[str] = Field(None, alias="dcType")
    
    debit: Num = 0.0
    credit: Num = 0.0
    balance: Num = 0.0
    
    vchEntryAcctNum: Optional[str] = None

class ItemDetailResponse(BaseModel):
    total: Int = 0
    items: List[ItemDetailItem] = []

# --- 7. Item Combination (核算项目组合表) ---

class CombinationRequest(BaseLedgerRequest):
    """
    核算项目组合表请求参数
    /jdyaccouting/report/combination
    """
    type: str = Field(..., description="组合方式(1:科目-辅助 2:双辅助)")
    accountNum: Optional[str] = None # Only for type=2
    totalDc: int = Field(..., description="合计方向(1:借 2:贷)")
    fromLevel: Optional[int] = None
    toLevel: Optional[int] = None
    
    row: Optional[str] = None # type=1 only
    column: Optional[str] = None # type=1 only
    rowData: Optional[str] = None
    columnData: Optional[str] = None
    
    showOnlyNotZero: Optional[int] = 1
    onlyDetailAcctName: Optional[int] = 1

class CombinationItem(BaseModel):
    # Dynamic structure mostly, but has basic fields
    id: Int = None
    number: Optional[str] = None
    name: Optional[str] = None
    isSummaryRow: Bool = None

class CombinationResponse(BaseModel):
    logData: Optional[str] = None
    items: List[Any] = [] # Structure is highly dynamic based on row/col
    columnTotal: Optional[Any] = None

# --- 8. General Ledger ---

class GeneralLedgerRequest(BaseLedgerRequest):
    """
    总账请求参数
    /jdyaccouting/report/genledger
    """
    fromAccountNum: Optional[str] = None
    toAccountNum: Optional[str] = None
    includeItem: Optional[int] = 0
    balance: Optional[int] = 1
    happen: Optional[int] = 1
    fromLevel: Optional[int] = None
    toLevel: Optional[int] = None

class GeneralLedgerRow(BaseModel):
    """
    总账行数据。API返回的是List[List[Row]]结构。
    """
    id: Optional[str] = None
    number: Optional[str] = None
    name: Optional[str] = None
    yearPeriod: Union[str, int, None] = None
    exp: Optional[str] = None
    
    gdebit: Num = 0.0
    gcredit: Num = 0.0
    gbalance: Num = 0.0
    
    gdebitFor: Num = None
    gcreditFor: Num = None
    gbalanceFor: Num = None
    
    dcType: Optional[str] = None
    gdc: Union[int, str, None] = None
    curRate: Optional[str] = None

class GeneralLedgerResponse(BaseModel):
    total: Int = Field(0, alias="totalsize")
    items: List[List[GeneralLedgerRow]] = []
