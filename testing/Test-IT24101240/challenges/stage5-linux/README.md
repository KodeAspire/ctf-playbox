# Stage 5 – The Forgotten Permission

## Category
Linux / System Security

## Difficulty
Moderate-Hard

## Flag
FLAG{stale_gr0up_m3mb3rsh1p}

## Scenario
Security discovers that Lizard previously worked on an older project. Although
the project was completed, Lizard's account may still retain access through an
old group membership.

## Player Task
Investigate Lizard's account and the relevant filesystem permission to determine
how access to the onboarding information remained possible.

## Required Tools
- SSH client
- Linux terminal / Bash

## SSH Access
ssh investigator@<UBUNTU_VM_IP> -p 2222
Password: investigator123

## How to Solve
1. SSH into the challenge container as investigator
2. Check `sudo -l` to see available sudo permissions
3. Use `sudo -u lizard` to run commands as lizard
4. Find files owned by the `legacy_proj` group
5. Read `/srv/onboarding_evidence/rabbit_id.txt`

## Reset
Run `./reset.sh` (rebuilds the container from scratch)