| ART-02 | 2 | Run Stage 2 solver script | Decoded message + flag output | PASS | Flag: FLAG{l1z4rd_c1ph3r} |
| ART-01 | 1 | Run steghide on rabbit_id.jpg | Hidden message extracted | DEFERRED | steghide not available on Windows host; to be tested in Kali VM |
| ART-03 | 5 | SSH into Stage 5 as investigator | Successful login | PASS | |
| ART-03b | 5 | Check sudo permissions | `(lizard) NOPASSWD: ALL` | PASS | Intended path found |
| ART-03c | 5 | Check /etc/group | `legacy_proj:x:1002:lizard` | PASS | Stale privilege identified |
| ART-03d | 5 | Solve Stage 5 via sudo -u lizard | Flag retrieved | PASS | FLAG{stale_gr0up_m3mb3rsh1p} |