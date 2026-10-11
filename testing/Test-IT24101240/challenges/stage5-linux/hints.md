# Stage 5 Hints

## Hint 1 (General direction)
Investigate Lizard's account. What groups does it belong to?

## Hint 2 (Relevant technique)
Linux groups can provide access to files and directories. Check the
investigator account's sudo permissions.

## Hint 3 (Stronger guidance)
Look for a group related to an older project. Use `sudo -u lizard` to
run commands as Lizard and search for files owned by that group.