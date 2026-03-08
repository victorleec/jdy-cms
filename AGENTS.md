# AGENTS.md

本文件为 Codex (Codex.ai/code) 提供项目上下文和操作指引。

## 项目概述

本项目是 **金蝶精斗云 (JDY) 云会计 API** 的 Python SDK 与 REST API 封装。提供对会计操作（凭证、账簿、财务报表、出纳、系统设置）的编程访问能力，同时通过 FastAPI 暴露 39 个 REST 端点。

## 常用命令

**包管理器：UV（不使用 pip）**

```bash
# 启动 API 服务器（端口 9034）
uv run python main.py

# 运行测试
uv run pytest tests/unit/                  # 仅单元测试（无需凭据）
uv run pytest tests/                       # 全部测试（需要有效的 .env）

# 运行单个测试文件
uv run pytest tests/unit/test_signature.py

# 代码检查
uv run ruff check src/
uv run ruff format src/

# 演示/诊断脚本
uv run python scripts/demo.py              # 凭证查询演示
uv run python scripts/demo_ledger.py       # 账簿/报表演示
uv run python scripts/debug_api.py         # API 连通性诊断
uv run python scripts/get_auth_info.py     # 获取 IDC 路由地址
```

## 架构

**分层架构：** 配置 → API客户端 → 服务层 → 数据模型 → REST路由

```
src/
├── config/settings.py          # pydantic-settings 读取 .env 配置
├── api/
│   ├── auth.py                 # 动态 Token 刷新 + App Secret 轮换（24小时）
│   ├── client.py               # HTTP 客户端，封装所有金蝶 API 调用
│   ├── dependencies.py         # FastAPI 依赖注入（API Key 认证）
│   └── routes/                 # FastAPI 路由层
│       ├── voucher.py          # 凭证 & 原始凭证路由（10个端点）
│       ├── ledger.py           # 账簿路由（8个端点）
│       ├── report.py           # 报表路由（5个端点）
│       ├── cashier.py          # 出纳路由（8个端点）
│       └── settings.py         # 设置路由（8个端点）
├── services/                   # 每个会计模块一个服务
│   ├── voucher_service.py      # 凭证：增删改查、冲销
│   ├── evidence_service.py     # 原始凭证：上传、绑定/解绑、查询
│   ├── ledger_service.py       # 账簿：科目余额、总账/明细账
│   ├── report_service.py       # 报表：利润表、资产负债表、现金流量表
│   ├── cashier_service.py      # 出纳：日记账、账户管理
│   └── settings_service.py     # 设置：系统参数、科目、辅助核算
├── models/                     # Pydantic v2 数据模型（按模块划分）
├── app.py                      # FastAPI 应用实例（路由注册、启动事件）
└── utils/signature.py          # HMAC-SHA256 签名（两种方案）
```

## REST API

- **端口**：9034（通过 `main.py` 启动）
- **API 前缀**：`/api`
- **交互式文档**：`http://localhost:9034/docs`（Swagger UI）或 `/redoc`
- **认证方式**：`X-API-Key` 请求头（在 `.env` 中设置 `API_KEY`）
- **健康检查**：`GET /health`

详细的接口说明请参阅 `docs/api_reference.md`。

## 认证系统

认证系统较为复杂 —— 修改前请仔细阅读 `src/api/auth.py`：

1. **App Secret 轮换**：金蝶 API 每 24 小时轮换 `app_secret`。`auth.py` 在每次请求 Token 前获取新 Secret 并缓存。
2. **两种签名方案**：
   - 请求头方式：`X-Api-Signature`（大多数端点使用）
   - 参数方式：`app_signature` 查询参数（部分端点使用）
3. **认证缓存**：`.kingdee_auth_cache.json` 本地存储 Token 和 Secret（已排除在 git 之外）。
4. **REST API 认证**：`X-API-Key` 请求头保护所有 REST 端点，使用 `secrets.compare_digest` 做时序安全比较。

## 金蝶 API 行为特性

金蝶 API 存在不一致性 —— 务必使用测试中的 `check_success` 模式：
- 成功可能是 `code=0`、`status=200` 或 `status=250`（无数据）
- 错误响应可能仍返回 HTTP 200
- 部分端点对同一概念返回不同的字段名

## 环境配置

复制 `.env.example` 为 `.env` 并填写：
```
JDY_API_BASE_URL=https://api.kingdee.com
JDY_CLIENT_ID=
JDY_CLIENT_SECRET=
JDY_APP_KEY=
JDY_APP_SECRET=
JDY_ENTERPRISE_ID=        # dbId（企业数据库ID）
JDY_SERVICE_ID=           # sId（服务ID）
JDY_IDC_DOMAIN=           # 路由地址（通过 scripts/get_auth_info.py 获取）
API_KEY=                   # REST API 认证密钥（留空则为开发模式，无需认证）
```

`JDY_IDC_DOMAIN` 作为 `X-GW-Router-Addr` 请求头在每次请求中传递。运行 `scripts/get_auth_info.py` 获取你企业的路由地址。

## 代码规范

- 行宽限制：120 字符（ruff）
- 目标版本：Python 3.10+ 语法
- 模型使用 Pydantic v2（`model_validator`、`field_validator`）
- 所有模型字段名遵循金蝶 API 的 camelCase JSON 约定，通过 Pydantic alias 映射
