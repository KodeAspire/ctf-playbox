## Stage 5 Intended Solution Path (Validated)
1. SSH as investigator (port 2222)
2. `sudo -l` shows `(lizard) NOPASSWD: ALL`
3. `sudo -u lizard groups` → shows `legacy_proj`
4. `sudo -u lizard find / -group legacy_proj` → finds `/srv/onboarding_evidence/`
5. `sudo -u lizard cat /srv/onboarding_evidence/rabbit_id.txt` → flag