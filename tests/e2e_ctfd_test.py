"""
e2e_ctfd_test.py - Member 4 (IT24101240)
End-to-end test: simulates a player registering and solving all Operation Rabbit stages.
Usage: python tests/e2e_ctfd_test.py
"""
import requests
import re
import sys
import time

BASE_URL = "http://localhost:8000"
TEST_USER = f"tester_{int(time.time())}"
TEST_PASS = "TestPass123!"
TEST_EMAIL = f"{TEST_USER}@test.com"

STAGE_ORDER = [
    "Welcome to Operation: Rabbit!",
    "CASE FILE Stage 0001 - \"The Altered ID\"",
    "CASE FILE Stage 0002 - The Lizard Cipher",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"",
    "CASE FILE Stage 0004 -",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"",
    "CASE FILE Stage 0006 - \"The Final Trace\"",
]

FLAGS = {
    "Welcome to Operation: Rabbit!":                          "FLAG{stgae_0_inestigator_welcome}",
    "CASE FILE Stage 0001 - \"The Altered ID\"":              "FLAG{St3g4n0gr4phy_1s_Fun}",
    "CASE FILE Stage 0002 - The Lizard Cipher":               "FLAG{l1z4rd_c1ph3r}",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"":              "FLAG{lz_042_0n_b0ard1ng}",
    "CASE FILE Stage 0004 -":                                  "FLAG{l1z4rd_r4bb1t_1d_2026-08-01T09:42:18Z_CASE-ONB-2048}",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"":    "FLAG{stale_gr0up_m3mb3rsh1p}",
    "CASE FILE Stage 0006 - \"The Final Trace\"":             "FLAG{XFER-6F2A-ONB2048_rabbit_id.jpg_fish@badcomp.com}",
}

s = requests.Session()
results = []


def _form_nonce(url):
    """Extract form CSRF nonce."""
    r = s.get(url)
    m = re.search(r'name="nonce"[^>]*value="([^"]+)"', r.text)
    return m.group(1) if m else None


def _js_nonce(url):
    """Extract csrfNonce from window.init JS block."""
    r = s.get(url)
    m = re.search(r"'csrfNonce':\s*\"([^\"]+)\"", r.text)
    return m.group(1) if m else None


def register():
    print(f"[*] Registering user '{TEST_USER}'...")
    nonce = _form_nonce(f"{BASE_URL}/register")
    if not nonce:
        print("    [X] No nonce")
        return False
    data = {"name": TEST_USER, "email": TEST_EMAIL, "password": TEST_PASS, "nonce": nonce}
    r = s.post(f"{BASE_URL}/register", data=data, allow_redirects=True)
    ok = "Registration successful" in r.text or "already" in r.text.lower()
    print(f"    [{'✓' if ok else 'X'}] Register: {r.status_code}")
    return True  # Even if it exists, proceed to login


def login():
    print(f"[*] Logging in as '{TEST_USER}'...")
    nonce = _form_nonce(f"{BASE_URL}/login")
    if not nonce:
        print("    [X] No nonce")
        return False
    data = {"name": TEST_USER, "password": TEST_PASS, "nonce": nonce}
    r = s.post(f"{BASE_URL}/login", data=data, allow_redirects=True)
    ok = "Login" not in r.text[:3000] or "Logout" in r.text
    print(f"    [{'✓' if ok else 'X'}] Login: {r.status_code}")
    return r.status_code == 200


def get_challenges():
    """Return {name: id} for all currently visible challenges."""
    r = s.get(f"{BASE_URL}/api/v1/challenges")
    if r.status_code != 200:
        return {}
    try:
        return {c["name"]: c["id"] for c in r.json().get("data", [])}
    except Exception:
        return {}


def submit(challenge_id, flag):
    """Submit via the web form (more reliable than API in some CTFd builds)."""
    # Get a fresh JS nonce from the challenges page
    nonce = _js_nonce(f"{BASE_URL}/challenges")
    if not nonce:
        return "no_nonce"

    # Try JSON API first
    r = s.post(
        f"{BASE_URL}/api/v1/challenges/attempt",
        json={"challenge_id": challenge_id, "submission": flag},
        headers={"CSRF-Token": nonce, "Content-Type": "application/json"},
    )
    if r.status_code == 200:
        try:
            return r.json().get("data", {}).get("status", "unknown")
        except Exception:
            return "parse_error"
    return f"http_{r.status_code}"


def test_case(name, passed, notes=""):
    results.append({"test": name, "result": "PASS" if passed else "FAIL", "notes": notes})
    sym = "✓" if passed else "✗"
    print(f"  [{sym}] {name}" + (f" - {notes}" if notes else ""))


def main():
    print("=" * 60)
    print("  Operation Rabbit - End-to-End Test")
    print("=" * 60)
    print()

    if not login():
        register()
        if not login():
            print("[X] Auth failed")
            sys.exit(1)

    # Test wrong flag rejection first (on visible intro)
    print("\n[*] Testing wrong-flag rejection...")
    ch = get_challenges()
    if "Welcome to Operation: Rabbit!" in ch:
        status = submit(ch["Welcome to Operation: Rabbit!"], "FLAG{wrong_xyz}")
        test_case("Wrong flag rejected", status == "incorrect", f"status={status}")

    # Solve each stage in order — refetch after each solve to see new challenges
    print("\n[*] Solving all stages in order...")
    for stage_name in STAGE_ORDER:
        # Refetch visible challenges (next one unlocks after each solve)
        ch = get_challenges()
        if stage_name not in ch:
            test_case(f"Solve '{stage_name}'", False, "not visible (previous stage not solved?)")
            continue

        status = submit(ch[stage_name], FLAGS[stage_name])
        test_case(f"Solve '{stage_name}'", status == "correct", f"status={status}")

        if status != "correct":
            print(f"    [!] Stopping — stage failed")
            break

    # Summary
    passed = sum(1 for r in results if r["result"] == "PASS")
    total = len(results)
    print("\n" + "=" * 60)
    print(f"  RESULTS: {passed}/{total} passed")
    print("=" * 60)
    for r in results:
        sym = "✓" if r["result"] == "PASS" else "✗"
        print(f"  [{sym}] {r['test']}  {r['notes']}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()