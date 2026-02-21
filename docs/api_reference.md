# 金蝶精斗云会计 API 接口说明书

> 版本: 1.0
> 基础地址: `http://localhost:9034/api`
> 协议: HTTP REST API，数据格式为 JSON

---

## 目录

- [1. 认证与通用说明](#1-认证与通用说明)
  - [1.1 认证方式](#11-认证方式)
  - [1.2 通用错误码](#12-通用错误码)
  - [1.3 通用响应格式](#13-通用响应格式)
- [2. 凭证模块](#2-凭证模块-apivoucher)
  - [2.1 凭证查询](#21-凭证查询)
  - [2.2 凭证保存](#22-凭证保存)
  - [2.3 凭证冲销](#23-凭证冲销)
  - [2.4 凭证删除](#24-凭证删除)
  - [2.5 凭证汇总表](#25-凭证汇总表)
- [3. 原始凭证模块](#3-原始凭证模块-apievidence)
  - [3.1 原始凭证上传](#31-原始凭证上传)
  - [3.2 原始凭证绑定](#32-原始凭证绑定)
  - [3.3 原始凭证解绑](#33-原始凭证解绑)
  - [3.4 原始凭证查询](#34-原始凭证查询)
  - [3.5 附件查询](#35-附件查询)
- [4. 账簿模块](#4-账簿模块-apiledger)
  - [4.1 科目余额表](#41-科目余额表)
  - [4.2 明细账](#42-明细账)
  - [4.3 数量金额明细账](#43-数量金额明细账)
  - [4.4 数量金额总账](#44-数量金额总账)
  - [4.5 核算项目余额表](#45-核算项目余额表)
  - [4.6 核算项目明细账](#46-核算项目明细账)
  - [4.7 核算项目组合表](#47-核算项目组合表)
  - [4.8 总账](#48-总账)
- [5. 报表模块](#5-报表模块-apireport)
  - [5.1 利润表](#51-利润表)
  - [5.2 资产负债表](#52-资产负债表)
  - [5.3 现金流量表](#53-现金流量表)
  - [5.4 费用明细表](#54-费用明细表)
  - [5.5 主要应交税金明细表](#55-主要应交税金明细表)
- [6. 出纳模块](#6-出纳模块-apicashier)
  - [6.1 日记账查询](#61-日记账查询)
  - [6.2 日记账新增](#62-日记账新增)
  - [6.3 日记账修改](#63-日记账修改)
  - [6.4 日记账删除](#64-日记账删除)
  - [6.5 账户查询](#65-账户查询)
  - [6.6 账户新增](#66-账户新增)
  - [6.7 账户修改](#67-账户修改)
  - [6.8 账户删除](#68-账户删除)
- [7. 设置模块](#7-设置模块-apisettings)
  - [7.1 系统参数](#71-系统参数)
  - [7.2 科目查询](#72-科目查询)
  - [7.3 科目保存](#73-科目保存)
  - [7.4 凭证字查询](#74-凭证字查询)
  - [7.5 辅助核算类别查询](#75-辅助核算类别查询)
  - [7.6 辅助核算查询](#76-辅助核算查询)
  - [7.7 辅助核算保存](#77-辅助核算保存)
  - [7.8 辅助核算删除](#78-辅助核算删除)

---

## 1. 认证与通用说明

### 1.1 认证方式

所有接口均需通过 `X-API-Key` 请求头进行认证。API Key 在服务端 `.env` 文件中通过 `API_KEY` 字段配置。

- **生产模式**: 必须在每个请求的 Header 中携带 `X-API-Key`，值为 `.env` 中配置的 `API_KEY`。
- **开发模式**: 若 `.env` 中未配置 `API_KEY`，则服务处于开发模式，所有接口无需认证即可访问。

请求头示例:

```
X-API-Key: your-api-key-here
```

### 1.2 通用错误码

| HTTP 状态码 | 说明 |
|---|---|
| 200 | 请求成功 |
| 400 | 请求参数错误，缺少必填字段或格式不正确 |
| 401 | 认证失败，`X-API-Key` 缺失或不正确 |
| 500 | 服务端内部错误或上游金蝶 API 调用失败 |

### 1.3 通用响应格式

成功响应:

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

失败响应:

```json
{
  "success": false,
  "error": "错误描述信息",
  "detail": "详细错误信息（可选）"
}
```

---

## 2. 凭证模块 (`/api/voucher`)

### 2.1 凭证查询

查询指定期间内的会计凭证列表，支持多种筛选条件。

- **接口路径**: `POST /api/voucher/list`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间，格式如 `202301` |
| toPeriod | int | 是 | 结束期间，格式如 `202312` |
| vchGroup | string | 否 | 凭证字，如 `"记"` |
| vchNum | string | 否 | 凭证号，支持逗号分隔 `"1,2,3"` 或范围 `"1-3"` |
| vchId | string | 否 | 凭证 ID |
| status | int | 否 | 审核状态: `0` - 未审核, `1` - 已审核 |
| onlyMech | int | 否 | 是否只查询机制凭证，默认 `2` |
| account | string | 否 | 科目编码 |
| page | int | 否 | 页码，默认 `1` |
| pageSize | int | 否 | 每页条数，默认 `20` |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/voucher/list \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "status": 1,
    "page": 1,
    "pageSize": 20
  }'
```

**响应说明**:

返回凭证列表数据，包含凭证头信息及分录明细。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "vchId": 12345,
        "vchGroup": "记",
        "vchNumber": 1,
        "date": "2023-01-15",
        "yearPeriod": 202301,
        "status": 1,
        "entries": [...]
      }
    ],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}
```

---

### 2.2 凭证保存

新建一张或多张会计凭证。

- **接口路径**: `POST /api/voucher/save`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，每个元素为一张凭证:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| linkId | string | 否 | 关联单据标识 |
| groupName | string | 是 | 凭证字，如 `"记"` |
| vchNumber | int | 否 | 凭证号，不填则自动编号 |
| date | string | 是 | 日期，格式 `yyyy-MM-dd` |
| yearPeriod | int | 是 | 年期，如 `202301` |
| entries | array | 是 | 分录列表，详见下表 |

**分录 (entries) 字段**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| acctNo | string | 是 | 科目编码 |
| dc | int | 是 | 借贷方向: `1` - 借, `-1` - 贷 |
| exp | string | 是 | 摘要 |
| currency | string | 否 | 货币编码，默认 `"RMB"` |
| rate | float | 否 | 汇率，默认 `1.0` |
| amount | float | 是 | 原币金额 |
| itemClsName | string | 否 | 辅助核算类别名称 |
| itemNo | string | 否 | 辅助核算编码 |
| custNo | string | 否 | 客户编码 |
| suppNo | string | 否 | 供应商编码 |
| deptNo | string | 否 | 部门编码 |
| empNo | string | 否 | 员工编码 |
| inventoryNo | string | 否 | 存货编码 |
| projectNo | string | 否 | 项目编码 |
| qty | float | 否 | 数量 |
| unit | string | 否 | 单位 |
| price | float | 否 | 单价 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/voucher/save \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "groupName": "记",
      "date": "2023-01-15",
      "yearPeriod": 202301,
      "entries": [
        {
          "acctNo": "6001",
          "dc": 1,
          "exp": "销售收入",
          "amount": 10000.00
        },
        {
          "acctNo": "1122",
          "dc": -1,
          "exp": "销售收入",
          "amount": 10000.00
        }
      ]
    }
  ]'
```

**响应说明**:

返回保存结果，包含新建凭证的 ID 信息。

```json
{
  "success": true,
  "data": {
    "vchIds": [12345]
  },
  "message": "凭证保存成功"
}
```

---

### 2.3 凭证冲销

对指定凭证生成红字冲销凭证。

- **接口路径**: `POST /api/voucher/reverse`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，元素为需要冲销的凭证 ID (int)。

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| (数组元素) | int | 是 | 凭证 ID |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/voucher/reverse \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[12345, 12346]'
```

**响应说明**:

返回冲销操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "凭证冲销成功"
}
```

---

### 2.4 凭证删除

删除指定的会计凭证。

- **接口路径**: `POST /api/voucher/delete`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，元素为需要删除的凭证 ID (int)。

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| (数组元素) | int | 是 | 凭证 ID |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/voucher/delete \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[12345, 12346]'
```

**响应说明**:

返回删除操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "凭证删除成功"
}
```

---

### 2.5 凭证汇总表

查询指定日期范围内的凭证汇总统计信息。

- **接口路径**: `GET /api/voucher/summary`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| from_date | string | 是 | 起始日期 |
| to_date | string | 是 | 结束日期 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/voucher/summary?from_date=2023-01-01&to_date=2023-12-31" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回凭证汇总统计数据。

```json
{
  "success": true,
  "data": {
    "summary": [...]
  }
}
```

---

## 3. 原始凭证模块 (`/api/evidence`)

### 3.1 原始凭证上传

上传原始凭证附件文件（图片、PDF 等）。

- **接口路径**: `POST /api/evidence/upload`
- **Content-Type**: `multipart/form-data`

**请求参数 (Form)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| file | File | 是 | 上传的文件 |
| period | int | 是 | 会计期间，如 `202301` |
| file_name | string | 否 | 自定义文件名，不填则使用原始文件名 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/evidence/upload \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/to/invoice.pdf" \
  -F "period=202301" \
  -F "file_name=发票-001.pdf"
```

**响应说明**:

返回上传成功后的原始凭证信息，包含凭证 ID。

```json
{
  "success": true,
  "data": {
    "evidenceId": "abc123",
    "fileName": "发票-001.pdf"
  },
  "message": "上传成功"
}
```

---

### 3.2 原始凭证绑定

将已上传的原始凭证附件绑定到指定会计凭证。

- **接口路径**: `POST /api/evidence/attach`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| voucher_id | int | 是 | 会计凭证 ID |
| evidence_ids | int[] | 是 | 原始凭证 ID 列表 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/evidence/attach \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "voucher_id": 12345,
    "evidence_ids": [100, 101, 102]
  }'
```

**响应说明**:

返回绑定操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "绑定成功"
}
```

---

### 3.3 原始凭证解绑

解除原始凭证与会计凭证的绑定关系。

- **接口路径**: `POST /api/evidence/unattach`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| evidence_id | string | 是 | 原始凭证 ID |
| file_id | string | 是 | 文件 ID |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/evidence/unattach \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "evidence_id": "abc123",
    "file_id": "file456"
  }'
```

**响应说明**:

返回解绑操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "解绑成功"
}
```

---

### 3.4 原始凭证查询

查询原始凭证列表。

- **接口路径**: `POST /api/evidence/list`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| begin_period | int | 是 | 起始期间 |
| end_period | int | 是 | 结束期间 |
| is_class | int | 否 | 分类筛选 |
| is_voucher | int | 否 | 是否已关联凭证 |

**请求示例**:

```bash
curl -X POST "http://localhost:9034/api/evidence/list?begin_period=202301&end_period=202312&is_class=0&is_voucher=0" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回原始凭证列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "evidenceId": "abc123",
        "fileName": "发票-001.pdf",
        "period": 202301,
        "isVoucher": false
      }
    ]
  }
}
```

---

### 3.5 附件查询

查询原始凭证附件列表。

- **接口路径**: `POST /api/evidence/attachment-list`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| begin_period | int | 是 | 起始期间 |
| end_period | int | 是 | 结束期间 |
| is_class | int | 否 | 分类筛选 |
| is_voucher | int | 否 | 是否已关联凭证 |

**请求示例**:

```bash
curl -X POST "http://localhost:9034/api/evidence/attachment-list?begin_period=202301&end_period=202312" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回附件列表信息。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "fileId": "file456",
        "fileName": "发票-001.pdf",
        "fileUrl": "https://...",
        "period": 202301
      }
    ]
  }
}
```

---

## 4. 账簿模块 (`/api/ledger`)

### 4.1 科目余额表

查询指定期间内各科目的期初余额、本期发生额和期末余额。

- **接口路径**: `POST /api/ledger/account-balance`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| currency | string | 否 | 货币编码 |
| fromAccountId | string | 否 | 起始科目 ID |
| toAccountId | string | 否 | 结束科目 ID |
| happen | int | 否 | 是否只显示有发生额的科目 |
| fromLevel | int | 否 | 起始科目级次 |
| toLevel | int | 否 | 结束科目级次 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/account-balance \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312
  }'
```

**响应说明**:

返回科目余额数据列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "accountNum": "1001",
        "accountName": "库存现金",
        "beginBalance": 5000.00,
        "debitAmount": 20000.00,
        "creditAmount": 15000.00,
        "endBalance": 10000.00
      }
    ]
  }
}
```

---

### 4.2 明细账

查询指定科目的明细账记录。

- **接口路径**: `POST /api/ledger/detail`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| accountNum | string | 是 | 科目编码 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/detail \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "accountNum": "1001"
  }'
```

**响应说明**:

返回该科目的逐笔明细记录。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "date": "2023-01-15",
        "vchGroup": "记",
        "vchNumber": 1,
        "explanation": "销售收入",
        "debitAmount": 10000.00,
        "creditAmount": 0,
        "balance": 15000.00,
        "dc": "借"
      }
    ]
  }
}
```

---

### 4.3 数量金额明细账

查询带有数量和金额信息的明细账。

- **接口路径**: `POST /api/ledger/qty-amount-detail`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| accountNum | string | 否 | 科目编码 |
| amountPlaces | int | 否 | 金额小数位数 |
| pricePlaces | int | 否 | 单价小数位数 |
| balance | int | 否 | 余额筛选 |
| happen | int | 否 | 发生额筛选 |
| fromLevel | int | 否 | 起始科目级次 |
| toLevel | int | 否 | 结束科目级次 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/qty-amount-detail \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "accountNum": "1405"
  }'
```

**响应说明**:

返回带数量、单价信息的明细账数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "date": "2023-01-15",
        "explanation": "采购入库",
        "qty": 100,
        "price": 50.00,
        "debitAmount": 5000.00,
        "creditAmount": 0,
        "balanceQty": 100,
        "balanceAmount": 5000.00
      }
    ]
  }
}
```

---

### 4.4 数量金额总账

查询带有数量和金额信息的总账数据。

- **接口路径**: `POST /api/ledger/qty-amount-total`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| accountNum | string | 否 | 科目编码 |
| fromLevel | int | 否 | 起始科目级次 |
| toLevel | int | 否 | 结束科目级次 |
| includeItem | int | 否 | 是否包含核算项目 |
| amountPlaces | int | 否 | 金额小数位数 |
| pricePlaces | int | 否 | 单价小数位数 |
| balance | int | 否 | 余额筛选 |
| happen | int | 否 | 发生额筛选 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/qty-amount-total \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "accountNum": "1405"
  }'
```

**响应说明**:

返回按期间汇总的数量金额总账数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "period": 202301,
        "accountNum": "1405",
        "accountName": "库存商品",
        "debitQty": 100,
        "debitAmount": 5000.00,
        "creditQty": 50,
        "creditAmount": 2500.00,
        "balanceQty": 50,
        "balanceAmount": 2500.00
      }
    ]
  }
}
```

---

### 4.5 核算项目余额表

查询辅助核算项目的余额表数据。

- **接口路径**: `POST /api/ledger/item-balance`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| auxiliaryType | string | 是 | 辅助核算类别 |
| auxiliaryNum | string | 否 | 辅助核算编码 |
| accountNum | string | 否 | 科目编码 |
| includeItem | int | 否 | 是否包含核算项目 |
| amountPlaces | int | 否 | 金额小数位数 |
| pricePlaces | int | 否 | 单价小数位数 |
| balance | int | 否 | 余额筛选 |
| happen | int | 否 | 发生额筛选 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/item-balance \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "auxiliaryType": "客户"
  }'
```

**响应说明**:

返回各核算项目的余额信息。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "auxiliaryNum": "C001",
        "auxiliaryName": "客户A",
        "beginBalance": 0,
        "debitAmount": 50000.00,
        "creditAmount": 30000.00,
        "endBalance": 20000.00
      }
    ]
  }
}
```

---

### 4.6 核算项目明细账

查询指定辅助核算项目的明细账记录。

- **接口路径**: `POST /api/ledger/item-detail`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| auxiliaryType | string | 是 | 辅助核算类别 |
| auxiliaryNum | string | 是 | 辅助核算编码 |
| accountNum | string | 否 | 科目编码 |
| includeItem | int | 否 | 是否包含核算项目 |
| amountPlaces | int | 否 | 金额小数位数 |
| pricePlaces | int | 否 | 单价小数位数 |
| balance | int | 否 | 余额筛选 |
| happen | int | 否 | 发生额筛选 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/item-detail \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "auxiliaryType": "客户",
    "auxiliaryNum": "C001"
  }'
```

**响应说明**:

返回该核算项目的逐笔明细。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "date": "2023-01-20",
        "vchGroup": "记",
        "vchNumber": 5,
        "explanation": "销售款",
        "accountNum": "1122",
        "accountName": "应收账款",
        "debitAmount": 10000.00,
        "creditAmount": 0,
        "balance": 10000.00
      }
    ]
  }
}
```

---

### 4.7 核算项目组合表

查询核算项目的组合分析数据，支持科目-辅助和双辅助两种模式。

- **接口路径**: `POST /api/ledger/combination`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| type | int | 是 | 组合类型: `1` - 科目-辅助, `2` - 双辅助 |
| accountNum | string | 否 | 科目编码 |
| totalDc | int | 是 | 汇总方向: `1` - 借方, `2` - 贷方 |
| fromLevel | int | 否 | 起始科目级次 |
| toLevel | int | 否 | 结束科目级次 |
| row | string | 否 | 行维度 |
| column | string | 否 | 列维度 |
| rowData | string | 否 | 行数据筛选 |
| columnData | string | 否 | 列数据筛选 |
| showOnlyNotZero | int | 否 | 是否只显示非零项 |
| onlyDetailAcctName | int | 否 | 是否只显示明细科目 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/combination \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312,
    "type": 1,
    "totalDc": 1
  }'
```

**响应说明**:

返回核算项目组合分析表数据。

```json
{
  "success": true,
  "data": {
    "list": [...]
  }
}
```

---

### 4.8 总账

查询指定期间内的总账数据。

- **接口路径**: `POST /api/ledger/general`
- **Content-Type**: `application/json`

**请求参数 (Body)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| fromPeriod | int | 是 | 起始期间 |
| toPeriod | int | 是 | 结束期间 |
| fromAccountNum | string | 否 | 起始科目编码 |
| toAccountNum | string | 否 | 结束科目编码 |
| includeItem | int | 否 | 是否包含核算项目 |
| balance | int | 否 | 余额筛选 |
| happen | int | 否 | 发生额筛选 |
| fromLevel | int | 否 | 起始科目级次 |
| toLevel | int | 否 | 结束科目级次 |
| currency | string | 否 | 货币编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/ledger/general \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "fromPeriod": 202301,
    "toPeriod": 202312
  }'
```

**响应说明**:

返回按期间汇总的总账数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "period": 202301,
        "accountNum": "1001",
        "accountName": "库存现金",
        "debitAmount": 20000.00,
        "creditAmount": 15000.00,
        "balance": 10000.00,
        "dc": "借"
      }
    ]
  }
}
```

---

## 5. 报表模块 (`/api/report`)

### 5.1 利润表

查询指定期间的利润表数据。

- **接口路径**: `GET /api/report/profit`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| start_period | int | 是 | 起始期间，如 `202301` |
| end_period | int | 是 | 结束期间，如 `202312` |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/report/profit?start_period=202301&end_period=202312" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回利润表各项目数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "itemName": "一、营业收入",
        "currentAmount": 500000.00,
        "yearAmount": 500000.00
      }
    ]
  }
}
```

---

### 5.2 资产负债表

查询指定期间的资产负债表数据。

- **接口路径**: `GET /api/report/balance-sheet`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| start_period | int | 是 | 起始期间 |
| end_period | int | 是 | 结束期间 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/report/balance-sheet?start_period=202301&end_period=202312" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回资产负债表各项目数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "itemName": "货币资金",
        "endBalance": 100000.00,
        "beginBalance": 80000.00
      }
    ]
  }
}
```

---

### 5.3 现金流量表

查询指定期间的现金流量表数据。

- **接口路径**: `GET /api/report/cash-flow`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| start_period | int | 是 | 起始期间 |
| end_period | int | 是 | 结束期间 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/report/cash-flow?start_period=202301&end_period=202312" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回现金流量表各项目数据。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "itemName": "销售商品、提供劳务收到的现金",
        "currentAmount": 300000.00,
        "yearAmount": 300000.00
      }
    ]
  }
}
```

---

### 5.4 费用明细表

查询指定期间和科目的费用明细数据。

- **接口路径**: `GET /api/report/expense-detail`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| from_period | int | 是 | 起始期间 |
| to_period | int | 是 | 结束期间 |
| account_num | string | 是 | 科目编码 |
| show_type | int | 否 | 显示类型，默认 `1` |
| show_item | int | 否 | 是否显示核算项目，默认 `0` |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/report/expense-detail?from_period=202301&to_period=202312&account_num=6601&show_type=1&show_item=0" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回费用明细数据列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "accountNum": "660101",
        "accountName": "工资",
        "currentAmount": 50000.00,
        "yearAmount": 50000.00
      }
    ]
  }
}
```

---

### 5.5 主要应交税金明细表

查询指定期间的主要应交税金数据。

- **接口路径**: `GET /api/report/tax-payable`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| period | int | 是 | 会计期间，如 `202301` |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/report/tax-payable?period=202301" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回各税种的应交税金明细。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "taxName": "增值税",
        "beginBalance": 0,
        "currentDebit": 13000.00,
        "currentCredit": 15000.00,
        "endBalance": 2000.00
      }
    ]
  }
}
```

---

## 6. 出纳模块 (`/api/cashier`)

### 6.1 日记账查询

查询出纳日记账记录。

- **接口路径**: `GET /api/cashier/journal/list`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| period | int | 是 | 会计期间，如 `202301` |
| cashierAccountNumber | string | 否 | 出纳账户编码 |
| includeVch | int | 否 | 是否包含关联凭证信息 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/cashier/journal/list?period=202301&cashierAccountNumber=1001&includeVch=1" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回日记账记录列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "id": 1001,
        "date": "2023-01-15",
        "cashierAccountNumber": "1001",
        "explanation": "收到货款",
        "debit": 10000.00,
        "credit": 0,
        "balance": 15000.00
      }
    ]
  }
}
```

---

### 6.2 日记账新增

新增出纳日记账记录。

- **接口路径**: `POST /api/cashier/journal/add`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，每个元素为一条日记账记录:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| cashierAccountNumber | string | 是 | 出纳账户编码 |
| date | string | 是 | 日期，格式 `yyyy-MM-dd` |
| explanation | string | 是 | 摘要 |
| credit | float | 是 | 支出金额 |
| debit | float | 是 | 收入金额 |
| serialNum | string | 否 | 流水号 |
| accountName | string | 否 | 对方科目名称 |
| accountNo | string | 否 | 对方科目编码 |
| accountNumber | string | 否 | 对方账号 |
| accountItem | string | 否 | 结算方式 |
| bankField | string | 否 | 银行字段 |
| remark | string | 否 | 备注 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/journal/add \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "cashierAccountNumber": "1001",
      "date": "2023-01-15",
      "explanation": "收到客户A货款",
      "debit": 10000.00,
      "credit": 0
    }
  ]'
```

**响应说明**:

返回新增日记账结果。

```json
{
  "success": true,
  "data": null,
  "message": "日记账新增成功"
}
```

---

### 6.3 日记账修改

修改已有的出纳日记账记录。请求参数与新增相同，但需包含记录的 `id` 字段。

- **接口路径**: `POST /api/cashier/journal/update`
- **Content-Type**: `application/json`

**请求参数 (Body)**: 同日记账新增，额外需包含:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | int | 是 | 日记账记录 ID |
| (其余字段) | - | - | 同日记账新增 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/journal/update \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "id": 1001,
      "cashierAccountNumber": "1001",
      "date": "2023-01-15",
      "explanation": "收到客户A货款（已修改）",
      "debit": 12000.00,
      "credit": 0
    }
  ]'
```

**响应说明**:

返回修改操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "日记账修改成功"
}
```

---

### 6.4 日记账删除

删除指定的出纳日记账记录。

- **接口路径**: `POST /api/cashier/journal/delete`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，元素为日记账记录 ID (int)。

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| (数组元素) | int | 是 | 日记账记录 ID |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/journal/delete \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[1001, 1002]'
```

**响应说明**:

返回删除操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "日记账删除成功"
}
```

---

### 6.5 账户查询

查询出纳账户列表。

- **接口路径**: `GET /api/cashier/account/list`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | int | 否 | 账户类型: `1` - 现金, `2` - 银行 |
| isForbid | int | 否 | 是否已禁用 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/cashier/account/list?type=2&isForbid=0" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回账户列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "id": "acc001",
        "number": "1002001",
        "name": "工商银行",
        "type": 2,
        "bankNo": "6222021234567890",
        "isForbid": false
      }
    ]
  }
}
```

---

### 6.6 账户新增

新增出纳账户。

- **接口路径**: `POST /api/cashier/account/add`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，每个元素为一个账户:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| number | string | 是 | 账户编码 |
| name | string | 是 | 账户名称 |
| type | int | 是 | 账户类型: `1` - 现金, `2` - 银行 |
| bankNo | string | 否 | 银行账号 |
| isForbid | int | 否 | 是否禁用 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/account/add \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "number": "1002002",
      "name": "建设银行",
      "type": 2,
      "bankNo": "6227001234567890"
    }
  ]'
```

**响应说明**:

返回新增账户结果。

```json
{
  "success": true,
  "data": null,
  "message": "账户新增成功"
}
```

---

### 6.7 账户修改

修改已有的出纳账户信息。请求参数与新增相同，但需包含账户的 `id` 字段。

- **接口路径**: `POST /api/cashier/account/update`
- **Content-Type**: `application/json`

**请求参数 (Body)**: 同账户新增，额外需包含:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 | 账户 ID |
| (其余字段) | - | - | 同账户新增 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/account/update \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "id": "acc001",
      "number": "1002002",
      "name": "建设银行（更新）",
      "type": 2,
      "bankNo": "6227001234567890"
    }
  ]'
```

**响应说明**:

返回修改操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "账户修改成功"
}
```

---

### 6.8 账户删除

删除指定的出纳账户。

- **接口路径**: `POST /api/cashier/account/delete`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，元素为账户编码 (string)。

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| (数组元素) | string | 是 | 账户编码 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/cashier/account/delete \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '["1002002", "1002003"]'
```

**响应说明**:

返回删除操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "账户删除成功"
}
```

---

## 7. 设置模块 (`/api/settings`)

### 7.1 系统参数

查询系统参数配置。

- **接口路径**: `GET /api/settings/profile`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| key | string | 否 | 参数键名，不传则返回所有参数 |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/settings/profile?key=companyName" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回系统参数值。

```json
{
  "success": true,
  "data": {
    "key": "companyName",
    "value": "示例公司"
  }
}
```

---

### 7.2 科目查询

查询会计科目列表，支持多种筛选条件。

- **接口路径**: `GET /api/settings/account-subjects`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| number | string | 否 | 科目编码 |
| name | string | 否 | 科目名称 |
| groupName | string | 否 | 科目类别名称 |
| classId | string | 否 | 科目类别 ID |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/settings/account-subjects?number=1001&name=库存现金" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回科目列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "number": "1001",
        "name": "库存现金",
        "dc": 1,
        "groupName": "资产",
        "level": 1
      }
    ]
  }
}
```

---

### 7.3 科目保存

新增或更新会计科目。

- **接口路径**: `POST /api/settings/account-subjects`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，每个元素为一个科目:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| number | string | 是 | 科目编码 |
| name | string | 是 | 科目名称 |
| dc | int | 是 | 借贷方向: `1` - 借, `-1` - 贷 |
| groupName | string | 是 | 科目类别名称 |
| itemClsName | string | 否 | 辅助核算类别名称 |
| currency | string | 条件必填 | 币别。**重要**：若科目已配置币种，更新时必须显式传入与原值一致的 `currency`，否则金蝶 API 会返回"币别已被使用，不能修改"错误 |
| useCustomer | int | 否 | 是否启用客户辅助核算 |
| useSupplier | int | 否 | 是否启用供应商辅助核算 |
| useDept | int | 否 | 是否启用部门辅助核算 |
| useEmp | int | 否 | 是否启用员工辅助核算 |
| useInventory | int | 否 | 是否启用存货辅助核算 |
| useProject | int | 否 | 是否启用项目辅助核算 |
| useQtyAux | int | 否 | 是否启用数量辅助核算 |
| qtyUnit | string | 否 | 数量单位 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/settings/account-subjects \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "number": "100101",
      "name": "人民币现金",
      "dc": 1,
      "groupName": "资产"
    }
  ]'
```

**响应说明**:

返回保存结果。

```json
{
  "success": true,
  "data": null,
  "message": "科目保存成功"
}
```

---

### 7.4 凭证字查询

查询系统中配置的凭证字列表。

- **接口路径**: `GET /api/settings/voucher-words`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| page | int | 否 | 页码，默认 `1` |
| pageSize | int | 否 | 每页条数，默认 `100` |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/settings/voucher-words?page=1&pageSize=100" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回凭证字列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "name": "记",
        "isDefault": true
      },
      {
        "name": "收",
        "isDefault": false
      },
      {
        "name": "付",
        "isDefault": false
      },
      {
        "name": "转",
        "isDefault": false
      }
    ]
  }
}
```

---

### 7.5 辅助核算类别查询

查询系统中配置的辅助核算类别列表。

- **接口路径**: `GET /api/settings/auxiliary-item-classes`

**请求参数**: 无

**请求示例**:

```bash
curl -X GET http://localhost:9034/api/settings/auxiliary-item-classes \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回辅助核算类别列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "name": "客户",
        "isSystem": true
      },
      {
        "name": "供应商",
        "isSystem": true
      },
      {
        "name": "部门",
        "isSystem": true
      },
      {
        "name": "员工",
        "isSystem": true
      }
    ]
  }
}
```

---

### 7.6 辅助核算查询

查询指定类别下的辅助核算项目列表。

- **接口路径**: `GET /api/settings/auxiliary-items`

**请求参数 (Query)**:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| itemClsName | string | 否 | 辅助核算类别名称 |
| number | string | 否 | 辅助核算编码 |
| name | string | 否 | 辅助核算名称 |
| isDeleted | int | 否 | 是否已删除 |
| page | int | 否 | 页码，默认 `1` |
| pageSize | int | 否 | 每页条数，默认 `100` |

**请求示例**:

```bash
curl -X GET "http://localhost:9034/api/settings/auxiliary-items?itemClsName=客户&page=1&pageSize=100" \
  -H "X-API-Key: your-api-key"
```

**响应说明**:

返回辅助核算项目列表。

```json
{
  "success": true,
  "data": {
    "list": [
      {
        "itemClsName": "客户",
        "number": "C001",
        "name": "客户A公司",
        "isDeleted": false
      }
    ],
    "total": 50,
    "page": 1,
    "pageSize": 100
  }
}
```

---

### 7.7 辅助核算保存

新增或更新辅助核算项目。

- **接口路径**: `POST /api/settings/auxiliary-items`
- **Content-Type**: `application/json`

**请求参数 (Body)**: JSON 数组，每个元素为一个辅助核算项目:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| itemClsName | string | 是 | 辅助核算类别名称 |
| number | string | 是 | 编码 |
| name | string | 是 | 名称 |
| unit | string | 否 | 单位 |
| spec | string | 否 | 规格 |
| isDeleted | int | 否 | 是否删除 |

**请求示例**:

```bash
curl -X POST http://localhost:9034/api/settings/auxiliary-items \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[
    {
      "itemClsName": "客户",
      "number": "C002",
      "name": "客户B公司"
    }
  ]'
```

**响应说明**:

返回保存结果。

```json
{
  "success": true,
  "data": null,
  "message": "辅助核算保存成功"
}
```

---

### 7.8 辅助核算删除

删除指定类别下的辅助核算项目。

- **接口路径**: `POST /api/settings/auxiliary-items/delete`

**请求参数**:

Query 参数:

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| item_class_name | string | 是 | 辅助核算类别名称 |

Body (JSON 数组): 需要删除的辅助核算编码列表 (string[])。

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| (数组元素) | string | 是 | 辅助核算编码 |

**请求示例**:

```bash
curl -X POST "http://localhost:9034/api/settings/auxiliary-items/delete?item_class_name=客户" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '["C002", "C003"]'
```

**响应说明**:

返回删除操作结果。

```json
{
  "success": true,
  "data": null,
  "message": "辅助核算删除成功"
}
```
