#!/usr/bin/env python3
"""
生成安全的API密钥
用于保护 jdy-cms 项目的 REST API 端点
"""

import secrets
import string


def generate_project_api_key(length: int = 48) -> str:
    """
    生成用于保护本项目API端点的安全密钥
    
    Args:
        length: 密钥长度
    
    Returns:
        安全的API密钥
    """
    chars = string.ascii_letters + string.digits + "-_"
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_env_line(api_key: str) -> str:
    """
    生成 .env 文件格式的配置行
    
    Args:
        api_key: API密钥
    
    Returns:
        .env 配置行
    """
    return f"API_KEY={api_key}"


def main():
    print("=== jdy-cms 项目 API 密钥生成器 ===\n")
    
    api_key = generate_project_api_key()
    
    print("生成的安全 API 密钥:")
    print(f"  {api_key}\n")
    
    print(".env 文件配置:")
    print(f"  {generate_env_line(api_key)}\n")
    
    print("=== 使用方法 ===")
    print("1. 将上面的配置行添加到项目根目录的 .env 文件中")
    print("2. 外部调用时需要在请求头中添加:")
    print("   X-API-Key: <你的API密钥>")
    print()
    
    print("=== 安全提示 ===")
    print("- 永远不要将 .env 文件提交到代码仓库")
    print("- 定期轮换API密钥")
    print("- 使用不同的密钥用于开发和生产环境")
    print("- 如果密钥泄露，立即生成新的密钥")


if __name__ == "__main__":
    main()
