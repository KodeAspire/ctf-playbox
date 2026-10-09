# Stage 4 - Forensics

## Scenario
A fictional employee onboarding portal may have been used to access
an employee identity image without authorization.

## Objective
Analyze the provided evidence to identify:
- The user who downloaded the target file
- The filename that was downloaded
- The exact UTC timestamp of the download
- The associated case identifier

## Evidence
- challenge/evidence/file_access.csv
- challenge/evidence/authentication.log
- challenge/evidence/case_notes.txt
- challenge/evidence/SHA256SUMS.json

## Instructions
Correlate the file access records with the authentication log.
Use the case notes to confirm the target file and case identifier.
Check the SHA-256 hashes if you want to verify evidence integrity.

## Learning objectives
- Log analysis
- Timeline correlation
- Digital evidence integrity
- Incident investigation

