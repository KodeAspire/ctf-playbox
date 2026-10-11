| ART-02 | 2 | Run Stage 2 solver script | Decoded message + flag output | PASS | Flag: FLAG{l1z4rd_c1ph3r} |
| ART-01 | 1 | Run steghide on rabbit_id.jpg | Hidden message extracted | DEFERRED | steghide not available on Windows host; to be tested in Kali VM |
| ART-03 | 5 | SSH into Stage 5 as investigator | Successful login | PASS | |
| ART-03b | 5 | Check sudo permissions | `(lizard) NOPASSWD: ALL` | PASS | Intended path found |
| ART-03c | 5 | Check /etc/group | `legacy_proj:x:1002:lizard` | PASS | Stale privilege identified |
| ART-03d | 5 | Solve Stage 5 via sudo -u lizard | Flag retrieved | PASS | FLAG{stale_gr0up_m3mb3rsh1p} |
| ART-04 | 4 | Examine forensic evidence files | All 4 evidence files present | PASS | |
| ART-04b | 4 | Correlate file_access.csv + authentication.log | Lizard downloaded rabbit_id.jpg at 2026-08-01T09:42:18Z | PASS | Case ID: CASE-ONB-2048 |
| ART-04c | 4 | Verify SHA-256 evidence integrity | All 3 hashes match SHA256SUMS.json | PASS | Evidence untampered |
| ART-06 | 6 | Open rabbit_traffic.pcap in Wireshark | Suspicious POST to /synthetic-transfer | PASS | Packet 11 → 203.0.113.66:8088 |
| ART-06b | 6 | Follow HTTP Stream | Transfer ID found | PASS | XFER-6F2A-ONB2048 |
| ART-06c | 6 | Identify exfiltration destination | Recipient identified | PASS | fish@badcomp.com |
| ART-06d | 6 | Verify PCAP SHA-256 | Matches manifest | PASS | 32147a09...a5a0e |
| ART-06e | 6 | Confirm intended solution path | Flag derived from PCAP | PASS | FLAG{...} |
| ART-03 | 3 | Open Stage 3 OSINT pages in browser | Lizard profile + connections found | PASS | |
| ART-03b | 3 | Find confidential record | Record LZ-042 shows Rabbit's ID access | PASS | Flag: FLAG{lz_042_0n_b0arding} |
| ART-06 | 6 | Open PCAP in Wireshark | Suspicious POST found | PASS | Packet 11 → 203.0.113.66:8088 |
| ART-06b | 6 | Follow HTTP Stream | Transfer details extracted | PASS | XFER-6F2A-ONB2048, fish@badcomp.com |
| ART-06c | 6 | Verify PCAP SHA-256 | Matches manifest | PASS | |
| DEF-08 | Deployment | seed.sql auto-init fails | DB empty on first boot | FIXED | Root cause: MariaDB runs init scripts before CTFd creates schema. Workaround: import seed.sql after CTFd starts. |
| DEF-09 | Integration | Challenge artifacts not attached in seed.sql | Files tab empty in Admin Panel | OPEN | Reported to Member 1, re-exporting seed.sql with files |
| DEF-10 | Integration | Player view only shows Introduction | Stages 1-6 hidden/locked | EXPECTED | Challenges require Intro to be solved first (prerequisite chain) |
