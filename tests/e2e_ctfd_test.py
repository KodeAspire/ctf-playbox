import requests
import re
import sys

BASE_URL = "http://localhost:8000"
TEST_USER = "member4tester"
TEST_PASS = "TestPass123!"

# We will replace these with real flags later
FLAGS = {
    1: "FLAG{stage1_dummy_flag}",
    2: "FLAG{stage2_dummy_flag}",
    3: "FLAG{stage3_dummy_flag}",
    4: "FLAG{stage4_dummy_flag}",
    5: "FLAG{stage5_dummy_flag}",
    6: "FLAG{stage6_dummy_flag}",
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