import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from src.services.evidence_service import evidence_service

def test_evidence_workflow():
    print("Starting Evidence Service Test...")
    
    import time
    timestamp = int(time.time())
    test_file = f"test_voucher_{timestamp}.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Test Evidence Content " * 10)
        
    try:
        # 2. Test Upload
        period = 202312 
        print(f"\n[1] Uploading evidence (Period: {period})...")
        upload_res = evidence_service.upload_evidence(test_file, period=period)
        print("Upload Response:", json.dumps(upload_res, ensure_ascii=False, indent=2))
        
        if str(upload_res.get("code")) == "0":
            data = upload_res.get("data", {})
            evid_id = data.get("evidId")
            file_id = data.get("fileId")
            print(f"Success! EvidId: {evid_id}, FileId: {file_id}")
            
            # 3. Test Query
            try:
                print(f"\n[2] Querying evidence list ({period})...")
                list_res = evidence_service.get_evidence_list(str(period), str(period))
                print("List Response:", json.dumps(list_res, ensure_ascii=False, indent=2))
                
                # Check if our uploaded file is in the list
                found = False
                for item in list_res.get("list", []):
                    if str(item.get("evidId")) == str(evid_id):
                        print("Found uploaded evidence in list!")
                        found = True
                        break
                
                if not found:
                    print("Warning: Uploaded evidence not found in list immediately (might be delay or filter issue).")
            except Exception as e:
                print(f"Querying evidence list failed: {e}")
                
            # 4. Test Attachment List
            try:
                print(f"\n[3] Querying attachment list ({period})...")
                att_res = evidence_service.get_attachment_list(str(period), str(period))
                print("Attachment List Response:", json.dumps(att_res, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"Querying attachment list failed: {e}")
             
        else:
            print(f"Upload failed: {upload_res}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nCleaned up local test file: {test_file}")

if __name__ == "__main__":
    test_evidence_workflow()
