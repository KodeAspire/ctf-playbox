import requests
from bs4 import BeautifulSoup
import re

BASE = "http://localhost:8081"

print("[*] Starting Stage 3 OSINT solver...")

# Step 1: Fetch Lizard profile
r = requests.get(f"{BASE}/lizard.html")
soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text()

# Step 2: Extract employee ID
match = re.search(r"Employee ID\s*([A-Z0-9-]+)", text)
if not match:
    print("[-] Could not find employee ID")
    exit(1)

emp_id = match.group(1).strip()
print(f"[+] Found employee ID: {emp_id}")

# Step 3: Access the hidden record
r2 = requests.get(f"{BASE}/records/{emp_id}.html")

# Step 4: Extract flag
flag = re.search(r"FLAG\{[^}]+\}", r2.text)
if flag:
    print(f"[+] Flag: {flag.group(0)}")
else:
    print("[-] Flag not found")