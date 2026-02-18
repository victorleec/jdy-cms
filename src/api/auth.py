import time
import uuid
import json
import os
import requests
from typing import Optional, Dict, Any

from src.config.settings import settings
from src.utils.signature import get_app_signature, get_header_signature

AUTH_CACHE_FILE = ".kingdee_auth_cache.json"

class AuthManager:
    def __init__(self):
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0
        self.app_secret: Optional[str] = settings.JDY_APP_SECRET
        self.app_secret_expires_at: float = 0
        self.session = requests.Session()
        self._load_cache()

    def _load_cache(self):
        """Load cached tokens and secrets from disk."""
        if os.path.exists(AUTH_CACHE_FILE):
            try:
                with open(AUTH_CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Load Access Token
                    self.access_token = data.get("access_token")
                    self.token_expires_at = data.get("token_expires_at", 0)
                    # Load App Secret
                    # Only override if not static setting (or if strict dynamic needed)
                    # Current logic: preference for dynamic if available
                    cached_secret = data.get("app_secret")
                    cached_secret_expiry = data.get("app_secret_expires_at", 0)
                    if cached_secret and time.time() < cached_secret_expiry:
                        self.app_secret = cached_secret
                        self.app_secret_expires_at = cached_secret_expiry
            except Exception as e:
                print(f"Warning: Failed to load auth cache: {e}")

    def _save_cache(self):
        """Save tokens and secrets to disk."""
        data = {
            "access_token": self.access_token,
            "token_expires_at": self.token_expires_at,
            "app_secret": self.app_secret,
            "app_secret_expires_at": self.app_secret_expires_at
        }
        try:
            with open(AUTH_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save auth cache: {e}")

    def get_app_secret(self) -> str:
        """
        Returns a valid App Secret. Fetches new one if expired or missing.
        Priority:
        1. Cached/InMemory valid secret
        2. Fetch from push_app_authorize
        3. Static setting (fallback)
        """
        # If we have a secret and it's either static (no expiry) or valid dynamic
        if self.app_secret:
             # If it has an expiry (dynamic) and is expired, refresh.
             if self.app_secret_expires_at > 0 and time.time() > self.app_secret_expires_at:
                 pass # Go to refresh
             else:
                 return self.app_secret
        
        # Determine if we should fetch
        if settings.JDY_OUTER_INSTANCE_ID:
            print("[Auth] Fetching new App Secret via push_app_authorize...")
            return self._fetch_app_secret()
            
        if self.app_secret:
            return self.app_secret
            
        raise Exception("Missing JDY_APP_SECRET and JDY_OUTER_INSTANCE_ID not configured.")

    def _fetch_app_secret(self) -> str:
        """
        Calls /jdyconnector/app_management/push_app_authorize to get appSecret
        """
        method = "POST"
        path = "/jdyconnector/app_management/push_app_authorize"
        url = f"{settings.JDY_API_BASE_URL}{path}"
        
        params = {"outerInstanceId": settings.JDY_OUTER_INSTANCE_ID}
        timestamp = str(int(time.time() * 1000))
        nonce = str(time.time_ns())
        
        signature = get_header_signature(
            client_secret=settings.JDY_CLIENT_SECRET,
            method=method, path=path, params=params, 
            nonce=nonce, timestamp=timestamp
        )
        
        headers = {
            "Content-Type": "application/json",
            "X-Api-ClientID": settings.JDY_CLIENT_ID,
            "X-Api-Auth-Version": "2.0",
            "X-Api-TimeStamp": timestamp,
            "X-Api-Nonce": nonce,
            "X-Api-SignHeaders": "X-Api-TimeStamp,X-Api-Nonce",
            "X-Api-Signature": signature
        }
        
        try:
            res = self.session.post(url, params=params, headers=headers)
            if res.status_code != 200:
                raise Exception(f"Fetch AppSecret Failed: {res.status_code} {res.text}")
            
            data = res.json()
            if data.get("code") == 200 and data.get("data"):
                auth_data = data["data"][0]
                new_secret = auth_data.get("appSecret")
                if not new_secret:
                    raise Exception("No appSecret in response")
                
                self.app_secret = new_secret
                # Doc says "24 hours dynamic refresh". Let's cache for 23 hours.
                self.app_secret_expires_at = time.time() + (23 * 3600)
                self._save_cache()
                return new_secret
            else:
                raise Exception(f"Fetch AppSecret Error: {data}")
        except Exception as e:
            # If fetch fails and we have a static setting, fallback? 
            # Or raise? User said it CHANGES every 24h, so static is likely invalid.
            raise Exception(f"Failed to fetch dynamic App Secret: {e}")

    def get_access_token(self) -> str:
        """
        Returns a valid access token. Refreshes if expired.
        """
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """
        Calls Kingdee API to get a new access token.
        Endpoint: /jdyconnector/app_management/kingdee_auth_token
        """
        path = "/jdyconnector/app_management/kingdee_auth_token"
        url = f"{settings.JDY_API_BASE_URL}{path}"
        
        # 1. Prepare Params
        app_key = settings.JDY_APP_KEY
        # Ensure we have a valid secret
        app_secret = self.get_app_secret()
        
        app_signature = get_app_signature(app_key, app_secret)
        
        params = {
            "app_key": app_key,
            "app_signature": app_signature
        }
        
        # 2. Prepare Headers
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4().int)[:10] 
        
        client_secret = settings.JDY_CLIENT_SECRET
        
        x_api_signature = get_header_signature(
            client_secret=client_secret,
            method="GET",
            path=path,
            params=params,
            nonce=nonce,
            timestamp=timestamp
        )
        
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "X-Api-ClientID": settings.JDY_CLIENT_ID,
            "X-Api-Auth-Version": "2.0",
            "X-Api-TimeStamp": timestamp,
            "X-Api-Nonce": nonce,
            "X-Api-SignHeaders": "X-Api-TimeStamp,X-Api-Nonce",
            "X-Api-Signature": x_api_signature
        }
        
        # 3. Execute Request
        response = self.session.get(url, params=params, headers=headers)
        
        # 4. Handle Response
        if response.status_code != 200:
            raise Exception(f"Auth Failed: {response.status_code} {response.text}")
            
        data = response.json()
        
        # Check success code (Kingdee sometimes uses code=0 or errcode=0)
        # Auth token endpoint usually returns data wrapper on success
        if data.get("state") == "error" or (data.get("code") != "0" and data.get("code") != 0 and "data" not in data):
             # Try to be robust about success checks
             if not data.get("data"):
                 raise Exception(f"Auth Error: {data}")

        # Parse Token
        token_data = data.get("data", {})
        self.access_token = token_data.get("access_token")
        
        # Expires
        expires_timestamp = token_data.get("expires")
        if expires_timestamp:
            self.token_expires_at = (float(expires_timestamp) / 1000.0) - 60
        else:
            # Default 7200s if not provided?
            self.token_expires_at = time.time() + 7000
            
        self._save_cache()
        return self.access_token

auth_manager = AuthManager()
