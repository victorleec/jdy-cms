from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field

# --- Helper for Loose Types ---
Num = Union[float, str, int, None]
Int = Union[int, str, None]
Bool = Union[bool, str, int, None]

# --- 1. System Profile (系统参数) ---

class SystemProfileResponse(BaseModel):
    value: Optional[str] = None

# --- 2. Account Subjects (科目) ---

class AccountSubject(BaseModel):
    id: Int = None
    number: Optional[str] = None
    name: Optional[str] = None
    fullName: Optional[str] = Field(None, alias="fullname") # Example uses "fullname" (lowercase n)
    level: Int = None
    parentId: Int = None
    rootId: Int = None
    groupId: Int = None
    groupName: Optional[str] = None
    isDetail: Bool = None
    dc: Int = None # 1 or -1
    helperCode: Optional[str] = None
    itemClsId: Int = None 
    currency: Union[List[str], str, None] = None # Example: ["RMB"]
    
    useCustomer: Bool = None
    useSupplier: Bool = None
    useDept: Bool = None
    useEmp: Bool = None
    useInventory: Bool = None
    useProject: Bool = None
    useQtyAux: Bool = None
    isRateAdj: Bool = None
    isCash: Bool = None
    qtyUnit: Optional[str] = None
    useItem: Bool = None
    plAcctId: Int = None
    isDeleted: Bool = None

class AccountSubjectListResponse(BaseModel):
    count: Int = 0
    list: List[AccountSubject] = []

class AccountSubjectSaveRequest(BaseModel):
    number: Union[str, int]
    name: str
    dc: int
    groupName: str
    itemClsName: Optional[str] = None
    itemClsName1: Optional[str] = None
    currency: Optional[str] = None
    useCustomer: Optional[Union[bool, str, int]] = None
    useSupplier: Optional[Union[bool, str, int]] = None
    useDept: Optional[Union[bool, str, int]] = None
    useEmp: Optional[Union[bool, str, int]] = None
    useInventory: Optional[Union[bool, str, int]] = None
    useProject: Optional[Union[bool, str, int]] = None
    useQtyAux: Optional[Union[bool, str, int]] = None
    qtyUnit: Optional[str] = None

# --- 3. Voucher Words (凭证字) ---

class VoucherWord(BaseModel):
    defaultCode: Bool = None
    name: str

class VoucherWordListResponse(BaseModel):
    totalsize: Int = 0
    items: List[VoucherWord] = []

# --- 4. Auxiliary Item Classes (辅助核算类别) ---

class AuxiliaryItemClass(BaseModel):
    id: Int = None
    name: str

class AuxiliaryItemClassListResponse(BaseModel):
    count: Int = 0
    list: List[AuxiliaryItemClass] = []

# --- 5. Auxiliary Items (辅助核算项目) ---

class AuxiliaryItem(BaseModel):
    id: Int = None
    number: Optional[str] = None
    fullNumber: Optional[str] = None
    name: Optional[str] = None
    level: Int = None
    parentId: Int = None
    isDetail: Bool = None
    isDeleted: Bool = None
    itemClsId: Int = Field(None, alias="itemClsID") # Example uses itemClsID
    itemClsName: Optional[str] = None
    unit: Optional[str] = None
    spec: Optional[str] = None
    remark: Optional[str] = None

class AuxiliaryItemListResponse(BaseModel):
    count: Int = 0
    list: List[AuxiliaryItem] = []

class AuxiliaryItemSaveRequest(BaseModel):
    itemClsName: str
    number: str
    name: str
    unit: Optional[str] = None
    spec: Optional[str] = None
    isDeleted: Optional[bool] = False
