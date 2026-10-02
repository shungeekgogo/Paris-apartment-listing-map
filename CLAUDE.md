# Working rules

## Always stay in sync with GitHub (work spans multiple PCs)
- At the start of every session, sync this PC with the latest version on GitHub (the current branch's upstream). The SessionStart hook `.claude/hooks/sync-from-github.sh` fetches and fast-forwards automatically and reports the result at the top of the session. If it says it could not update (uncommitted changes or a conflict), tell the user and resolve it before starting work.
- After changing files, commit and push to GitHub. Before finishing, make sure every change is committed and pushed (the Stop hook `.claude/hooks/check-pushed.sh` sends you back if anything is not on GitHub yet).
