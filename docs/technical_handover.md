# 金蝶云星辰 API 集成 - 技术交接文档
**日期**: 2026-02-18
**版本**: v1.0

## 1. 项目概览
本项目是一个 Python SDK 和 CLI 工具，用于集成金蝶云星辰（Kingdee Jingu Cloud）API。
目前的重点是实现凭证（Voucher）模块的查询与操作。

### 目录结构
```
jdy-cms/
├── .env                  # 环境变量配置 (关键)
├── .kingdee_auth_cache.json # 自动生成的认证缓存 (已忽略)
├── scripts/              # 工具脚本
│   ├── demo.py           # 主演示/测试脚本
│   ├── debug_api.py      # API 连接诊断工具
│   └── get_auth_info.py  # 授权信息获取工具 (获取 IDC Domain)
├── src/
│   ├── api/              # API 核心 (Auth, Client)
│   ├── config/           # 配置加载 (Settings)
│   ├── models/           # Pydantic 数据模型
│   ├── services/         # 业务服务层
│   └── utils/            # 工具函数 (签名算法)
└── docs/                 # 文档与输出样例
    ├── technical_handover.md
    └── voucher_demo_output.json
```

## 2. 关键技术实现

### 2.1 动态认证 (Dynamic Auth)
由于 `JDY_APP_SECRET` 每24小时变更，为了保证服务高可用，我们在 `src/api/auth.py` 中实现了 **自动刷新机制**：
1.  **加载缓存**: 优先读取 `.kingdee_auth_cache.json`。
2.  **过期检查**: 如果 App Secret 过期或不存在，自动调用 `push_app_authorize` 接口获取新密钥。
3.  **自动保存**: 获取后更新本地缓存文件 (有效期设为23小时)。

### 2.2 路由与配置 (Routing & Config)
金蝶云 API 是多数据中心架构，**必须** 配置正确的路由地址。
*   **Base URL**: `https://api.kingdee.com` (固定)
*   **Gateway Router (IDC)**: `JDY_IDC_DOMAIN` (动态，例如 `https://vip1-hz.jdy.com`)。
    *   **错误现象**: 如果配置错误，API 会返回 `404 No Route` 或 `519 API Not Found`。
    *   **获取方法**: 运行 `scripts/get_auth_info.py`。
*   **Service ID**: `JDY_SERVICE_ID` (sId)。通常不等于 `dbId`，需通过上述脚本获取。

## 3. 已实现模块

### 3.1 凭证模块 (Voucher)
*   **代码位置**: `src/services/voucher_service.py`
*   **功能**:
    *   `get_voucher_list`: 查询凭证列表 (已验证)
    *   `save_vouchers`: 新增凭证 (待深度验证)
    *   `delete_vouchers`: 删除凭证
    *   `get_voucher_summary`: 凭证汇总

### 3.2 原始凭证模块 (Evidence)
*   **代码位置**: `src/services/evidence_service.py`
*   **功能**:
    *   `upload_evidence`: 上传原始凭证 (已验证，成功)
    *   `get_evidence_list`: 查询原始凭证列表 (存在权限问题 4012，需检查应用权限)
    *   `get_attachment_list`: 查询附件列表 (存在权限问题 4012，需检查应用权限)
    *   `attach_evidence`: 绑定原始凭证 (依赖凭证 ID)
    *   `unattach_evidence`: 解绑原始凭证


### 3.3 账簿模块 (Ledger)
*   **代码位置**: `src/services/ledger_service.py`
*   **功能**:
    *   `get_account_balance`: 科目余额表 (已验证)
    *   `get_detail_ledger`: 明细账 (已验证)
    *   `get_general_ledger`: 总账 (已验证，处理了嵌套列表结构)
    *   `get_qty_amount_total`: 数量金额总账 (已验证)
    *   其他支持接口: `qtyamountdetail`, `itembalance`, `itemdetail`, `combination`

### 3.4 报表模块 (Report)
*   **代码位置**: `src/services/report_service.py`
*   **功能**:
    *   `get_profit_statement`: 利润表 (已验证)
    *   `get_balance_sheet`: 资产负债表 (已验证)
    *   `get_cash_flow_statement`: 现金流量表 (已验证)
    *   `get_expense_detail`: 费用明细表 (已验证，修正了文档参数缺失问题)
    *   `get_tax_payable_detail`: 应交税金明细表 (已验证)
    
### 3.5 出纳模块 (Cashier)
*   **代码位置**: `src/services/cashier_service.py`
*   **功能**:
    *   `get_journal_list`: 日记账查询 (已验证)
    *   `save_journal`: 日记账新增 (已验证，支持数值类型自动转换)
    *   `update_journal`: 日记账修改 (已验证)
    *   `delete_journal`: 日记账删除 (已验证)
    *   `get_account_list`: 账户查询 (已验证)
    *   `save_account`: 账户新增 (已验证)
    *   `update_account`: 账户修改 (已验证)
    *   `delete_account`: 账户删除 (已验证)

## 4. 验证步骤

### 4.1 运行 Demo
```bash
uv run python scripts/demo.py        # 凭证模块
uv run python scripts/demo_ledger.py # 账簿模块
uv run python tests/reproduce_report.py # 报表模块
uv run python tests/test_cashier.py     # 出纳模块
```
*   `demo.py`: 自动认证并查询凭证。
*   `demo_ledger.py`: 验证科目余额表、明细账、总账等核心报表。

### 4.2 诊断问题
如果遇到 404/500 错误：
```bash
uv run python scripts/debug_api.py
```
*   该脚本会打印详细的 Request Headers 和 Params。
*   提供直连 IDC 的测试模式。

## 5. 已知问题与注意事项 (Known Issues)
1.  **API 状态码不统一**: 
    -   部分接口返回 `code: "0"` (标准化)。
    -   部分接口返回 `status: 200` 且无 code (如总账)。
    -   部分接口返回 `status: 250` 表示无数据 (需视为成功)。
    -   **处理**: `LedgerService` 已兼容这三种情况。
2.  **数据结构差异**: 
    -   总账接口文档描述为对象列表，实际返回为嵌套列表 (`List[List]`)。已在模型中适配。
3.  **字段名映射**: 
    -   科目余额表文档称字段为 `name`，实际返回 `accountname`。已通过 alias 解决。
4.  **数据类型宽松**: 
    -   API 返回的数值字段经常混用 `float`/`string`/`null`。Pydantic 模型已配置为宽松模式 (`Union[float, str, int, None]`)。
5.  **权限报错**: 
    -   原始凭证查询接口仍报 `4012` 权限错误，需在云之家/金蝶后台检查应用权限配置。
6.  **报表接口差异**:
    -   利润表/资产负债表/现金流量表返回 `code: 0`。
    -   费用明细表/应交税金明细表返回 `status: 200` 且无 `code` 字段。`ReportService` 已做兼容处理。
7.  **文档参数缺失**:
    -   费用明细表 (`expenseDetail`) 接口文档未标注 `fromPeriod` 为必填，但实际调用必须传递，否则报错。已在代码中修复。
8.  **出纳日记账金额**:
    -   API 文档要求金额字段为字符串 (`string`)，但实际接收数值 (`number`) 会报错或行为不一致。模型层已添加验证器自动转换。

## 6. 待办事项 (Next Steps)
1.  **科目管理**: 实现科目表的获取与维护。
2.  **基础资料**: 客商档案的同步。
3.  **权限排查**: 解决原始凭证查询接口的 4012 权限错误。
