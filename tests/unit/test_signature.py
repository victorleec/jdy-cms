import unittest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.signature import get_header_signature

class TestSignature(unittest.TestCase):
    def test_kingdee_signature_example(self):
        """
        Verifies that the signature generation matches the example provided in the Kingdee documentation.
        
        Example Data:
        ClientId: 200421
        ClientSecret: f2adcfef73369bfc4e1384677d38a0ff
        Method: GET
        Path: /jdyconnector/app_management/kingdee_auth_token
        Params: 
            app_key: bVZgAZOv1
            app_signature: MzZlYTk0ODk4MWZlNjdiODNmNWU4YzViNzYxNGM5MTFlOGJkN2NjMzk0MTJkZGNhZGM0NzZhN2YxZDJmOTlkZA==
        Headers:
            X-Api-Nonce: 4427456950
            X-Api-TimeStamp: 1670305063559
            
        Expected X-Api-Signature: 
        OTFiZTliNDFiMjNkYTI3YzVhNzg4MDI4ZGU3MWY1ZTA5ZTk1NjVlNGM1YTI1ZjIxY2Y5YTA3ZGY2OGI1MGQ1MQ==
        """
        client_secret = "f2adcfef73369bfc4e1384677d38a0ff"
        method = "GET"
        path = "/jdyconnector/app_management/kingdee_auth_token"
        
        # Note: The raw value of app_signature in the example (before URL encoding) ends with ==
        # The example signature base string has it double encoded as %253D%253D
        # My utility expects the raw param value and handles double encoding.
        params = {
            "app_key": "bVZgAZOv1",
            "app_signature": "MzZlYTk0ODk4MWZlNjdiODNmNWU4YzViNzYxNGM5MTFlOGJkN2NjMzk0MTJkZGNhZGM0NzZhN2YxZDJmOTlkZA=="
        }
        
        nonce = "4427456950"
        timestamp = "1670305063559"
        
        expected_signature = "OTFiZTliNDFiMjNkYTI3YzVhNzg4MDI4ZGU3MWY1ZTA5ZTk1NjVlNGM1YTI1ZjIxY2Y5YTA3ZGY2OGI1MGQ1MQ=="
        
        calculated_signature = get_header_signature(
            client_secret=client_secret,
            method=method,
            path=path,
            params=params,
            nonce=nonce,
            timestamp=timestamp
        )
        
        self.assertEqual(calculated_signature, expected_signature)

if __name__ == "__main__":
    unittest.main()
