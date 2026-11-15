# Contributing to 3w-map

Thank you for helping. This project is a **trial**: a small decision map for AI-assisted projects, plus the telemetry and experiments that test whether it helps. Improvements, bug reports, new experiments and honest counter-evidence are all welcome. Counter-evidence is especially valuable.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute
- **Report a bug** or **suggest a feature**: open an issue using the templates.
- **Share data**: run the experiment protocol on your own repo and send the anonymised results (see [Data contributions](#data-contributions)).
- **Improve the docs or the tools** (`bin/`, `docs/`, `examples/`, `skill/`).
- **Challenge a claim**: if the data does not support a sentence in the README or `docs/results.md`, say so with evidence.

## Workflow (fork, branch, pull request)
1. **Search first.** Look through open and closed issues and pull requests so you do not duplicate work. For anything bigger than a small fix, open an issue and wait for a maintainer reply before you build it.
2. **Fork** the repository and clone your fork.
3. **Create a branch from the latest `main`, named by type:**
   - `feature/<short-description>` for new things, e.g. `feature/pmap-json-output`
   - `bug/<short-description>` for fixes, e.g. `bug/export-crashes-on-empty-map`
   - `docs/<short-description>` for documentation only
   Use lowercase letters, digits and hyphens. A maintainer will ask you to rename and reopen a pull request from `main` or from any other name.
4. **Make small, focused commits.** One logical change per pull request. Write the commit message in the imperative ("Add ...", "Fix ...") and explain *why*.
5. **Sign off** every commit (`git commit -s`). This adds `Signed-off-by: Your Name <you@example.com>` and certifies the [Developer Certificate of Origin](https://developercertificate.org/): you wrote the change or have the right to submit it under the MIT license.
6. **Run the checks locally** (see below) and fill in the pull request template.
7. **Open the pull request against `main`.** A maintainer reviews it. Expect questions; reviews usually take a few days. Please do not force-push over review comments; add new commits and we squash on merge.

## Pull request limits
To keep reviews manageable, please keep **at most 3 open pull requests** at a time. This is checked by a maintainer, not automatically: this project deliberately uses no paid services or hosted automation. If you go over, a maintainer asks you to finish or close one first. It is about review capacity, not a judgement on your work.

## Local checks
`pmap` needs only Python 3 and git.
```bash
python3 -m py_compile bin/pmap bin/pmap-export bin/agent-usage bin/agent-final
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('data/**/*.json', recursive=True)]"
bin/pmap examples check          # the example map must have no gaps
```
Maintainers run the same checks locally before merging. Please paste the output in your pull request.

## Style
- Python: standard library only, no new dependencies without discussion. Match the surrounding code (naming, comment density).
- Docs: plain, specific, and honest about limits. State what a number shows **and what it does not**.
- Do not add secrets, personal data, private project names or private decisions anywhere.

## Data contributions
The point of this repo is evidence. A good data contribution:
- follows [`docs/experiment-protocol.md`](docs/experiment-protocol.md) (same questions to both arms, answers written to files, blind grading);
- states the project size, the agent and model, and the dates;
- reports **failures, discarded runs and contamination** as plainly as successes;
- contains **no private content**: raw agent answers and fact lists that quote a private repo stay out; publish aggregate scores and anonymised excerpts only;
- adds a new file under `data/experiments/` named `YYYY-MM-DD-<repo-alias>.json` (valid JSON, same keys as the existing files).

## Recognition
Contributors are listed in the release notes. Significant data contributions are credited by name or alias, as you prefer.

## Questions
Open an issue with the "question" label. Please do not email maintainers for support.
