from typing import List, Optional, Any
from pydantic import BaseModel, Field

# --- Common Models ---

class VoucherEntry(BaseModel):
    """
    凭证分录实体 (Voucher Entry)
    Required for Save: acctNo, dc, exp, currency, rate, amount
    """
    entryId: Optional[int] = None # 分录序号 (Response only)
    
    # Core Fields for Save
    acctNo: str = Field(..., description="会计科目编码") # Request uses acctNo
    # Note: Response uses accountNumber. We might need aliases or separate models if huge diff.
    # For now, let's allow both or use aliases? 
    # The doc shows Request: acctNo, Response: accountNumber. 
    # Let's create separate models for Request and Response to be clean, or use aliases.
    # Given the complexity, separate models for Create vs Read is often safer.
    
    dc: int = Field(..., description="借/贷 (1 : 借；-1 : 贷)")
    exp: str = Field(..., description="摘要") # Request: exp, Response: explanation? No, response has explanation in header, but entry?
    # Response Entry: itemClassName... 
    
    currency: str = Field(default="RMB", description="货币编码")
    rate: float = Field(default=1.0, description="货币汇率")
    amount: float = Field(..., description="原币金额")
    
    # Optional Auxiliaries
    itemClsName: Optional[str] = None # 自定义辅助核算类别名称
    itemNo: Optional[str] = None      # 自定义辅助核算项目编码
    
    # Standard Auxiliaries
    custNo: Optional[str] = None      # 客户编码
    suppNo: Optional[str] = None      # 供应商编码
    deptNo: Optional[str] = None      # 部门编码
    empNo: Optional[str] = None       # 职员编码
    inventoryNo: Optional[str] = None # 存货编码
    projectNo: Optional[str] = None   # 项目编码
    
    qty: Optional[float] = 0
    unit: Optional[str] = None
    price: Optional[float] = 0

class VoucherCreate(BaseModel):
    """
    凭证创建模型
    """
    linkId: Optional[str] = None    # 关联的单据标识
    groupName: str = Field(..., description="凭证字 (e.g. 记)")
    vchNumber: Optional[int] = None # 凭证号
    date: str = Field(..., description="凭证日期 yyyy-MM-dd")
    yearPeriod: int = Field(..., description="凭证年期 (e.g. 202301)")
    entries: List[VoucherEntry]

# --- Query Models ---

class VoucherQueryFilter(BaseModel):
    """
    凭证列表查询参数
    """
    fromPeriod: int = Field(..., description="起始期间 (e.g. 202301)")
    toPeriod: int = Field(..., description="结束期间 (e.g. 202302)")
    vchGroup: Optional[str] = None # 凭证字
    vchNum: Optional[str] = None   # 凭证号 (1,2,3 or 1-3)
    vchId: Optional[str] = None
    status: Optional[int] = None   # 0-未审核; 1-已审核
    onlyMech: Optional[int] = 2    # 是否只查询机制凭证 (2 - 全部)
    account: Optional[str] = None  # 科目编码
    page: int = 1
    pageSize: int = 20

# --- Response Models ---
# Simplified for now, or we can use Dict[str, Any] for flexibility until strictly needed.
# Since the user wants a "Data Model Layer", let's define the basics.

class VoucherEntryResponse(BaseModel):
    entryId: int
    accountNumber: str
    accountName: str
    amount: float
    dc: int
    cur: str
    # ... Add more as needed

class VoucherDetailResponse(BaseModel):
    id: str
    date: str
    yearPeriod: int
    voucherNo: str
    groupName: str
    number: int
    entries: List[VoucherEntryResponse]
    debitTotal: float
    creditTotal: float

class VoucherListResponse(BaseModel):
    totalSize: int = Field(..., alias="totalsize")
    items: List[VoucherDetailResponse]
