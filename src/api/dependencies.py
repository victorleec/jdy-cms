import secrets
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src.config.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    验证 X-API-Key 请求头。
    如果环境变量 API_KEY 未配置，则跳过验证（开发模式）。
    """
    if not settings.API_KEY:
        # 未配置 API_KEY 时跳过验证（开发模式警告已在 app.py 启动时输出）
        return "dev-mode"

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少 X-API-Key 请求头",
        )

    if not secrets.compare_digest(api_key, settings.API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无效的 API Key",
        )

    return api_key
