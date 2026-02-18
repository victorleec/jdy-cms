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

## 4. 验证步骤

### 4.1 运行 Demo
```bash
uv run python scripts/demo.py
```
*   该脚本会自动进行认证（处理动态密钥）。
*   查询 `202601` 期间的凭证列表。
*   结果保存至 `voucher_demo_output.json`（位于根目录）。

### 4.2 诊断问题
如果遇到 404/500 错误：
```bash
uv run python scripts/debug_api.py
```
*   该脚本会打印详细的 Request Headers 和 Params。
*   提供直连 IDC 的测试模式。

## 5. 待办事项 (Next Steps)
1.  **科目管理**: 实现科目表的获取与维护。
2.  **基础资料**: 客商档案的同步。
3.  **权限排查**: 解决原始凭证查询接口的 4012 权限错误。
