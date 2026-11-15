# Security policy

## Supported versions
Only the latest commit on `main` is supported.

## Reporting a vulnerability
Please **do not open a public issue**. Use GitHub's private reporting: **Security → Report a vulnerability** on this repository. Include what you found, how to reproduce it, and the impact. We aim to acknowledge within 7 days and to fix or explain within 30 days.

## Scope
The `pmap` tools run locally on a repository you choose and read only its map and git history. Reports we care about include: command or path injection through map files or git data, writing outside the chosen repo, leaking data into exports, and unsafe handling in the GitHub workflows of this repo.

## Privacy of contributed data
Never put secrets, personal data or private repository content in issues, pull requests or data files. If you did by mistake, report it privately as above so we can remove it from history.
