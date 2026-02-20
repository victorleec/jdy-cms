import logging
from fastapi import FastAPI
from src.config.settings import settings
from src.api.routes.voucher import router as voucher_router, evidence_router
from src.api.routes.ledger import router as ledger_router
from src.api.routes.report import router as report_router
from src.api.routes.cashier import router as cashier_router
from src.api.routes.settings import router as settings_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="金蝶精斗云会计 API",
    description="金蝶精斗云 (JDY) 云会计系统的 REST API 封装，提供凭证、账簿、报表、出纳、设置等模块的接口。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 注册路由
app.include_router(voucher_router, prefix="/api")
app.include_router(evidence_router, prefix="/api")
app.include_router(ledger_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(cashier_router, prefix="/api")
app.include_router(settings_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    if not settings.API_KEY:
        logger.warning("⚠ 未配置 API_KEY 环境变量，API 端点处于无认证开发模式！请在 .env 中设置 API_KEY。")
    else:
        logger.info("✓ API Key 认证已启用")


@app.get("/health", tags=["系统"])
def health_check():
    """健康检查端点。"""
    return {"status": "ok"}
