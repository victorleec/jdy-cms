import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Configuration
    JDY_API_BASE_URL: str = "https://api.kingdee.com"
    
    # Client Credentials (Header Auth)
    JDY_CLIENT_ID: str
    JDY_CLIENT_SECRET: str  # Used for X-Api-Signature
    
    # App/Tenant Credentials (Param Auth)
    JDY_APP_KEY: str
    JDY_APP_SECRET: str | None = None     # Used for app_signature (Dynamic)
    
    # Third-party Instance ID (For push_app_authorize)
    JDY_OUTER_INSTANCE_ID: str | None = None

    # Business Context
    JDY_ENTERPRISE_ID: str | None = None # dbId
    JDY_SERVICE_ID: str | None = None    # sId
    
    # Gateway Router (IDC Domain)
    JDY_IDC_DOMAIN: str | None = None   # X-GW-Router-Addr (e.g. https://tf.jdy.com)

    # REST API 认证密钥
    API_KEY: str | None = None  # X-API-Key 请求头，用于保护 REST API 端点

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
