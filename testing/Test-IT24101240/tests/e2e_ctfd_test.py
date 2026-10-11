"""
e2e_ctfd_test.py - Member 4 (IT24101240)
End-to-end test using CTFd API token (bypasses CSRF).
Usage: python tests/e2e_ctfd_test.py
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

# API token from seed.sql (user 2 - Kas)
API_TOKEN = "ctfd_80a1c3aeed204cedab567a6d542f8a5ff1d112eb57575a38b8d3fc93dabe05ff"
HEADERS = {"Authorization": f"Token {API_TOKEN}", "Content-Type": "application/json"}

STAGE_ORDER = [
    "Welcome to Operation: Rabbit!",
    "CASE FILE Stage 0001 - \"The Altered ID\"",
    "CASE FILE Stage 0002 - The Lizard Cipher",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"",
    "CASE FILE Stage 0004 - \"The Onboarding Evidence\"",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"",
    "CASE FILE Stage 0006 - \"The Final Trace\"",
]

FLAGS = {
    "Welcome to Operation: Rabbit!":                          "FLAG{stgae_0_inestigator_welcome}",
    "CASE FILE Stage 0001 - \"The Altered ID\"":              "FLAG{St3g4n0gr4phy_1s_Fun}",
    "CASE FILE Stage 0002 - The Lizard Cipher":               "FLAG{liz4rd_c1ph3r}",
    "CASE FILE Stage 0003 - \"Who is Lizard?\"":              "FLAG{lz_042_0n_b0ard1ng}",
    "CASE FILE Stage 0004 - \"The Onboarding Evidence\"":     "FLAG{l1z4rd_r4bb1t_1d_2026-08-01T09:42:18Z_CASE-ONB-2048}",
    "CASE FILE Stage 0005 - \"The Forgotten Permission\"":    "FLAG{stale_gr0up_m3mb3rsh1p}",
    "CASE FILE Stage 0006 - \"The Final Trace\"":             "FLAG{XFER-6F2A-ONB2048_rabbit_id.jpg_fish@badcomp.com}",
}

results = []


def get_challenges():
    r = requests.get(f"{BASE_URL}/api/v1/challenges", headers=HEADERS)
    if r.status_code != 200:
        print(f"[X] API error: {r.status_code}")
        print(f"    Response: {r.text[:200]}")
        return {}
    return {c["name"]: c["id"] for c in r.json().get("data", [])}


def submit(challenge_id, flag):
    r = requests.post(
        f"{BASE_URL}/api/v1/challenges/attempt",
        json={"challenge_id": challenge_id, "submission": flag},
        headers=HEADERS,
    )
    if r.status_code != 200:
        return f"http_{r.status_code}"
    try:
        return r.json().get("data", {}).get("status", "unknown")
    except Exception:
        return "parse_error"


def test(name, passed, notes=""):
    results.append((name, passed, notes))
    sym = "✓" if passed else "✗"
    print(f"  [{sym}] {name}" + (f" - {notes}" if notes else ""))


def main():
    print("=" * 60)
    print("  Operation Rabbit - End-to-End Test (API token)")
    print("=" * 60)
    print()

    # Verify auth
    r = requests.get(f"{BASE_URL}/api/v1/users/me", headers=HEADERS)
    if r.status_code != 200:
        print(f"[X] Token auth failed: {r.status_code}")
        print(f"    {r.text[:200]}")
        sys.exit(1)
    user = r.json().get("data", {})
    print(f"[*] Authenticated as: {user.get('name')} (id={user.get('id')})")
    print()

    # Get challenges
    challenges = get_challenges()
    print(f"[*] Found {len(challenges)} visible challenges")
    print()

    # Wrong flag test
    print("[*] Testing wrong-flag rejection...")
    if "Welcome to Operation: Rabbit!" in challenges:
        status = submit(challenges["Welcome to Operation: Rabbit!"], "FLAG{wrong_xyz}")
        test("Wrong flag rejected", status == "incorrect", f"status={status}")
    print()

    # Solve in order
    print("[*] Solving all stages in order...")
    for name in STAGE_ORDER:
        ch = get_challenges()  # refetch — next unlocks after each solve
        if name not in ch:
            test(f"Solve '{name}'", False, "not visible")
            continue
        status = submit(ch[name], FLAGS[name])
        test(f"Solve '{name}'", status in ("correct", "already_solved"), f"status={status}")
        if status == "incorrect":
            print(f"    [!] Wrong flag for: {name}")
    print()

    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    print("=" * 60)
    print(f"  RESULTS: {passed}/{total} passed")
    print("=" * 60)
    for name, p, notes in results:
        sym = "✓" if p else "✗"
        print(f"  [{sym}] {name}  {notes}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()