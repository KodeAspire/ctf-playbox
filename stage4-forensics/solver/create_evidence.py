
from pathlib import Path
import hashlib
import json

# Stage 4: The Onboarding Evidence
# Fictional evidence generator for the CTF challenge.

BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = BASE_DIR / "challenge" / "evidence"

CASE_ID = "CASE-ONB-2048"
EVENT_TIME = "2026-08-01T09:42:18Z"
USERNAME = "lizard"
TARGET_FILE = "rabbit_id.jpg"

def generate_evidence():
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    access_log = f"""timestamp,user,action,filename,case_id
2026-08-01T09:15:02Z,rabbit,login,onboarding_portal,CASE-ONB-2048
2026-08-01T09:38:11Z,lizard,login,onboarding_portal,CASE-ONB-2048
{EVENT_TIME},{USERNAME},download,{TARGET_FILE},{CASE_ID}
2026-08-01T09:45:03Z,lizard,logout,onboarding_portal,CASE-ONB-2048
"""

    auth_log = f"""timestamp,user,event,service,result
2026-08-01T09:15:02Z,rabbit,authentication,onboarding_portal,success
2026-08-01T09:38:11Z,lizard,authentication,onboarding_portal,success
{EVENT_TIME},{USERNAME},file_access,onboarding_storage,success
2026-08-01T09:45:03Z,lizard,logout,onboarding_portal,success
"""

    files = {
        "file_access.csv": access_log,
        "authentication.log": auth_log,
        "case_notes.txt": (
            "FICTIONAL TRAINING CASE\n"
            f"Case identifier: {CASE_ID}\n"
            "Subject: Rabbit employee onboarding\n"
            f"Relevant file: {TARGET_FILE}\n"
            "Review access and authentication records together.\n"
        ),
    }

    for filename, content in files.items():
        path = EVIDENCE_DIR / filename
        path.write_text(content, encoding="utf-8")
        print(f"[+] Created: {path}")

    manifest = {}
    for filename in files:
        data = (EVIDENCE_DIR / filename).read_bytes()
        manifest[filename] = hashlib.sha256(data).hexdigest()

    manifest_path = EVIDENCE_DIR / "SHA256SUMS.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[+] Created: {manifest_path}")

def verify_evidence():
    access_path = EVIDENCE_DIR / "file_access.csv"
    auth_path = EVIDENCE_DIR / "authentication.log"

    access_text = access_path.read_text(encoding="utf-8")
    auth_text = auth_path.read_text(encoding="utf-8")

    checks = {
        "target filename present": TARGET_FILE in access_text,
        "expected user present": USERNAME in access_text,
        "expected timestamp present": EVENT_TIME in access_text,
        "case identifier present": CASE_ID in access_text,
        "authentication corroborates access": (
            USERNAME in auth_text
            and EVENT_TIME in auth_text
            and "file_access,onboarding_storage,success" in auth_text
        ),
    }

    print("\nVerification:")
    for label, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")

    if not all(checks.values()):
        raise SystemExit("Evidence verification failed.")

    print("\n[SUCCESS] Stage 4 evidence generated and verified.")

if __name__ == "__main__":
    generate_evidence()
    verify_evidence()
    