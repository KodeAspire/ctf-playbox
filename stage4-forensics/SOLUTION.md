# Stage 4 - Solution

## Findings

- Case ID: CASE-ONB-2048
- User: lizard
- Action: download
- Target file: rabbit_id.jpg
- Timestamp: 2026-08-01T09:42:18Z

## Analysis
The file_access.csv record identifies lizard as the user who
downloaded rabbit_id.jpg.

The authentication.log contains a corresponding successful
file_access event at the same timestamp.

The case_notes.txt file confirms the target filename and case ID.

SHA256SUMS.json contains hashes for the three evidence files.
These can be recalculated to check whether the files have changed.

## Conclusion
The intended finding is that lizard downloaded rabbit_id.jpg
at 2026-08-01T09:42:18Z in case CASE-ONB-2048.

