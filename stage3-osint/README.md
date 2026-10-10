# Stage 3 – Who is Lizard?

## Category
OSINT / Reconnaissance

## Difficulty
Moderate

## Flag
FLAG{lz_042_0n_b0ard1ng}

## Scenario
After identifying Lizard as a person of interest, players must investigate
the fictional company intranet to determine Lizard's role, project history,
and his connection to Rabbit.

## Player Task
Investigate the fictional company information and correlate Lizard's profile,
project history, and relationship with Rabbit.

## Required Tools
- Web browser

## How to Solve
1. Browse the intranet pages
2. Find Lizard's profile via Employees page
3. Extract his employee ID (LZ-042)
4. Access the hidden record page: /records/LZ-042.html
5. Read the flag

## Files
- pages/index.html
- pages/employees.html
- pages/lizard.html
- pages/rabbit.html
- pages/projects.html
- pages/onboarding.html
- pages/records/LZ-042.html
- solver/solve.py

## Reset
Run `./reset.sh`