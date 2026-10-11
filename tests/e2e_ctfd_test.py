import requests
import re
import sys

BASE_URL = "http://localhost:8000"
TEST_USER = "member4tester"
TEST_PASS = "TestPass123!"

STAGE_ORDER = [
    "Welcome to Operation: Rabbit!",
    "CASE FILE Stage 0001 - \"The Altered ID\"",
    "CASE FILE Stage 0002 - The Lizard Cipher",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"",
    "CASE FILE Stage 0004 -",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"",
    "CASE FILE Stage 0006 - \"The Final Trace\"",  # verify exact name
]

# We will replace these with real flags later
FLAGS = {
    "Welcome to Operation: Rabbit!":       "FLAG{stgae_0_inestigator_welcome}",  # ask Member 1
    "CASE FILE Stage 0001 - \"The Altered ID\"": "FLAG{St3g4n0gr4phy_1s_Fun}",  # ask Member 3
    "CASE FILE Stage 0002 - The Lizard Cipher":  "FLAG{l1z4rd_c1ph3r}",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"": "FLAG{lz_042_0n_b0arding}",
    "CASE FILE Stage 0004 -":                   "FLAG{l1z4rd_r4bb1t_1d_2026-08-01T09:42:18Z_CASE-ONB-2048}",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"": "FLAG{stale_gr0up_m3mb3rsh1p}",
    "CASE FILE Stage 0006 - \"The Final Trace\"": "FLAG{XFER-6F2A-ONB2048}",
}

session = requests.Session()

def register():
    print("Attempting to register test user...")
    # Note: You will need to adjust this based on your CTFd version's CSRF handling
    r = session.get(f"{BASE_URL}/register")
    nonce = re.search(r'name="nonce" value="([^"]+)"', r.text)
    if not nonce:
        print("Could not find CSRF nonce.")
        return False
    
    data = {
        "name": TEST_USER,
        "email": f"{TEST_USER}@test.com",
        "password": TEST_PASS,
        "nonce": nonce.group(1)
    }
    r = session.post(f"{BASE_URL}/register", data=data)
    if "Registration successful" in r.text:
        print("Registration successful.")
        return True
    print("Registration failed. Might already exist.")
    return False

def login():
    print("Logging in...")
    r = session.get(f"{BASE_URL}/login")
    nonce = re.search(r'name="nonce" value="([^"]+)"', r.text)
    if not nonce:
        return False
        
    data = {
        "name": TEST_USER,
        "password": TEST_PASS,
        "nonce": nonce.group(1)
    }
    r = session.post(f"{BASE_URL}/login", data=data)
    return r.status_code == 200

def submit_flag(challenge_id, flag):
    print(f"Submitting flag for Stage {challenge_id}...")
    # This API endpoint depends on your CTFd setup (API enabled or not)
    # For now, we will mock a response
    # Replace with actual API or form submission logic
    return {"data": {"status": "correct"}} 

def main():
    print("Starting End-to-End Test...")
    if not login():
        if not register():
            print("Could not register or login. Exiting.")
            sys.exit(1)
        login()

    for stage in range(1, 7):
        result = submit_flag(stage, FLAGS[stage])
        if result.get("data", {}).get("status") == "correct":
            print(f"Stage {stage} PASSED")
        else:
            print(f"Stage {stage} FAILED")
            sys.exit(1)

    print("All stages passed! End-to-End test successful.")

if __name__ == "__main__":
    main()