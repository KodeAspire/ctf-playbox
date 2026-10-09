# Test Plan - Operation Rabbit

| Test ID | Stage | Test Case | Expected Result | Status |
|---------|-------|-----------|-----------------|--------|
| TC-01 | 1 | Submit correct flag for Stage 1 | Stage 1 complete, Stage 2 unlocks | Pending |
| TC-02 | 1 | Submit wrong flag for Stage 1 | Error message, Stage 2 stays locked | Pending |
| TC-03 | 2 | Try to access Stage 2 before Stage 1 | Access denied | Pending |
| ... | ... | ... | ... | ... |
| E2E-01 | All | Complete Stage 1 through 6 in order | Final investigation complete | Pending |
| ISO-01 | 5 | Stage 5 container tries to reach CTFd | Connection refused | Pending |
| RST-01 | 5 | Run reset_stage5.sh | Fresh container, solvable again | Pending |