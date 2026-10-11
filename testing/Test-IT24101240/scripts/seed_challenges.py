"""
seed_challenges.py - Member 4 (IT24101240)
Automatically creates all 6 Operation Rabbit challenges in CTFd via the API.
Usage: python scripts/seed_challenges.py
"""
import requests
import os
import sys

BASE_URL = "http://localhost:8000"
API_KEY = "ctfd_adbb39b1a269b8965dab57889091c693a41f02446ed7f01ba1313a8c592b2cc2"  # Replace with your admin API key

HEADERS = {"Authorization": f"Token {API_KEY}"}

# Get the repo root (one level up from scripts/)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHALLENGES = [
    {
        "name": "The Altered ID",
        "category": "Steganography",
        "description": "The ID photo submitted for Rabbit's credential change looks suspicious. "
                       "Security believes someone modified it and hid information inside. "
                       "Download the image and find the hidden message.",
        "flag": "FLAG{...stage1_flag...}",  # Get from stage1-stegnography/SOLUTION.md
        "file": "stage1-stegnography/challenge/rabbit_id.jpg",
    },
    {
        "name": "The Lizard Cipher",
        "category": "Cryptography",
        "description": "The hidden information from Stage 1 contains an encoded message. "
                       "Decode it using CyberChef (Base64 then Caesar cipher).",
        "flag": "FLAG{l1z4rd_c1ph3r}",
        "file": "stage2-cryptography/challenge/encoded_message.txt",
    },
    {
        "name": "Who is Lizard?",
        "category": "OSINT",
        "description": "Investigate the fictional company information to find out who Leopold Lizard is "
                       "and what connection he has to Rabbit.",
        "flag": "FLAG{lz_042_0n_b0arding}",
        "file": None,  # OSINT is web-based, no file upload
    },
    {
        "name": "The Onboarding Evidence",
        "category": "Digital Forensics",
        "description": "Examine the forensic evidence package (file_access.csv, authentication.log, "
                       "case_notes.txt) to prove Lizard accessed Rabbit's ID.",
        "flag": "FLAG{CASE-ONB-2048}",  # Confirm from stage4-forensics/SOLUTION.md
        "file": "stage4-forensics/challenge/evidence/file_access.csv",
    },
    {
        "name": "The Forgotten Permission",
        "category": "Linux Security",
        "description": "SSH into the challenge container as investigator (port 2222). "
                       "Investigate Lizard's account and find the stale privilege. "
                       "Connection: ssh investigator@<host> -p 2222",
        "flag": "FLAG{stale_gr0up_m3mb3rsh1p}",
        "file": None,  # Linux challenge via SSH
    },
    {
        "name": "The Final Trace",
        "category": "Networking",
        "description": "Analyze the PCAP with Wireshark. Find the suspicious session, "
                       "follow the TCP stream, and identify the transfer ID and destination.",
        "flag": "FLAG{XFER-6F2A-ONB2048}",  # Confirm from stage6-networking/SOLUTION.md
        "file": "stage6-networking/challenge/rabbit_traffic.pcap",
    },
]


def create_challenge(challenge):
    """Create a single challenge and upload its file if provided."""
    name = challenge["name"]
    print(f"\n[*] Creating: {name}")

    # 1. Create the challenge
    payload = {
        "name": name,
        "category": challenge["category"],
        "description": challenge["description"],
        "type": "standard",
        "state": "visible",
        "flags": [{"content": challenge["flag"], "type": "static"}],
    }
    r = requests.post(f"{BASE_URL}/api/v1/challenges", json=payload, headers=HEADERS)

    if r.status_code != 200:
        print(f"    [X] Failed to create: {r.status_code} {r.text}")
        return False

    cid = r.json()["data"]["id"]
    print(f"    [+] Created with ID {cid}")

    # 2. Upload file if one is specified
    if challenge["file"]:
        filepath = os.path.join(REPO_ROOT, challenge["file"])
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                files = {"file": (os.path.basename(filepath), f, "application/octet-stream")}
                r_file = requests.post(
                    f"{BASE_URL}/api/v1/challenges/{cid}/files",
                    files=files,
                    headers=HEADERS,
                )
            if r_file.status_code == 200:
                print(f"    [+] Uploaded {challenge['file']}")
            else:
                print(f"    [X] File upload failed: {r_file.status_code} {r_file.text}")
        else:
            print(f"    [!] File not found: {filepath}")
    return True


def list_existing():
    """List existing challenges so we don't duplicate."""
    r = requests.get(f"{BASE_URL}/api/v1/challenges", headers=HEADERS)
    print(f"    [i] GET /api/v1/challenges -> {r.status_code}")
    if r.status_code != 200:
        print(f"    [X] Response body (first 200 chars): {r.text[:200]}")
        return []
    try:
        return [c["name"] for c in r.json()["data"]]
    except Exception as e:
        print(f"    [X] Could not parse JSON: {e}")
        print(f"    [i] Raw response: {r.text[:300]}")
        return []


def main():
    print(f"Seeding challenges to {BASE_URL}")

    # FIXED: only check if the key is empty or still the placeholder
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE" or not API_KEY.startswith("ctfd_"):
        print("[!] You must set a valid API_KEY first!")
        print("    Get one from CTFd: Settings > API Tokens > Generate")
        sys.exit(1)

    existing = list_existing()
    print(f"[i] Existing challenges: {existing}")

    created = 0
    for ch in CHALLENGES:
        if ch["name"] in existing:
            print(f"[!] Skipping '{ch['name']}' (already exists)")
            continue
        if create_challenge(ch):
            created += 1

    print(f"\n[✓] Done. Created {created} new challenges.")
