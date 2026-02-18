import hashlib
import hmac
import base64
import urllib.parse

def kingdee_sha256_signature(secret: str, data: str) -> str:
    """
    Implements Kingdee's signature algorithm: Base64(Hex(HMAC-SHA256(secret, data)))
    """
    # 1. HMAC-SHA256
    signature = hmac.new(
        secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest() # 2. Hex Output
    
    # 3. Base64 Encode
    # hexdigest returns a string, we need to encode it to bytes for b64encode, then decode back to string
    return base64.b64encode(signature.encode('utf-8')).decode('utf-8')

def get_app_signature(app_key: str, app_secret: str) -> str:
    """
    Calculates app_signature for params.
    Formula: Base64(Hex(HMAC-SHA256(AppSecret, AppKey)))
    """
    return kingdee_sha256_signature(app_secret, app_key)

def get_header_signature(
    client_secret: str, 
    method: str, 
    path: str, 
    params: dict[str, str], 
    nonce: str, 
    timestamp: str
) -> str:
    """
    Calculates X-Api-Signature for headers.
    
    Signature String Component:
    1. Method (UPPERCASE)
    2. Path (Encoded)
    3. Params (Encoded twice, Sorted)
    4. Headers (nonce, timestamp)
    """
    # 1. Method
    method_str = method.upper()
    
    # 2. Path
    # "取红色部分，进行url编码" -> e.g., /jdyconnector/app_management/kingdee_auth_token
    # verify if we need to encode the slashes. 
    # Example in doc: %2Fjdyconnector%2Fapp_management%2Fkingdee_auth_token
    # This implies full quoting including slashes.
    path_encoded = urllib.parse.quote(path, safe='')
    
    # 3. Params
    # "进行两次url编码（编码后字母应是大写）... 加密时按参数名ASCII码升序顺序进行排序"
    # Example: app_key=bVZ...
    # Step 3a: Sort params
    sorted_keys = sorted(params.keys())
    
    param_list = []
    for k in sorted_keys:
        val = str(params[k])
        # "进行两次url编码" - Verify this.
        # User doc example: app_key=bVZ...&app_signature=MzZ...
        # Wait, the example string in the doc shows:
        # app_key=bVZgAZOv1&app_signature=MzZlYTk0ODk4MWZlNjdiODNmNWU4YzViNzYxNGM5MTFlOGJkN2NjMzk0MTJkZGNhZGM0NzZhN2YxZDJmOTlkZA%253D%253D
        # Notice %253D at the end. %3D is '=', %253D is % encoded.
        # So the VALUE is encoded twice? OR the whole `key=value` string?
        # Standard signature usually normalizes `key=value`.
        # Doc says: "params请求参数（进行两次url编码..."
        # Let's assume: Encode(Encode(key) + "=" + Encode(value))? No that's weird.
        # Usually it means: Construct query string, then Encode it?
        # Example line: `app_key=bVZ...&app_signature=MzZ...`
        # It looks like a standard query string where the VALUES are encoded, and then maybe the equals/ampersands are NOT encoded?
        # WAIT. `app_signature` value in example `MzZ...` ends with `ZA==`.
        # In the signature string it allows `ZA%253D%253D`.
        # `==` -> `%3D%3D` (1st encode) -> `%253D%253D` (2nd encode).
        # So it seems valid values are Double Url Encoded.
        
        # Let's verify the key. `app_key` is not encoded?
        # If I have a param `a space b`, 
        # 1. `a%20space%20b`
        # 2. `a%2520space%2520b`
        
        encoded_val = urllib.parse.quote(val, safe='')
        double_encoded_val = urllib.parse.quote(encoded_val, safe='')
        
        # Doc Example: `app_key=bVZ...` (app_key is NOT encoded? OR it is simplified?)
        # "params请求参数（进行两次url编码"
        # It might mean the WHOLE parameter string is encoded? 
        # But the example shows: 
        # GET
        # %2Fjdyconnector...
        # app_key=bVZ...&app_signature=MzZ...
        # The params line looks unencoded mostly except for the values?
        # Actually `app_signature` value IS double encoded.
        # `app_key` value `bVZ...` (alphanumeric) doesn't change.
        # So it implies: `key=DoubleEncodedValue`.
        # And connected by `&`.
        
        param_list.append(f"{k}={double_encoded_val}")
        
    param_str = "&".join(param_list)
    
    # 4. Headers
    # "headers请求参数（只需要x-api-nonce、x-api-timestamp参与加密，必须小写）"
    header_str = f"x-api-nonce:{nonce}\nx-api-timestamp:{timestamp}"
    
    # 5. Concatenate with newlines
    # "每段签名字符拼接均需要换行符（x-api-timestamp时间戳后需要换行符）"
    # Format:
    # METHOD\n
    # PathEncoded\n
    # ParamStr\n
    # HeadStr\n
    
    # If no params? "无params请求参数时需传空签名字符" -> Empty line.
    
    signature_base = f"{method_str}\n{path_encoded}\n{param_str}\n{header_str}\n"
    
    return kingdee_sha256_signature(client_secret, signature_base)
