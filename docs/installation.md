# Agent installation

Use a durable full checkout of https://github.com/Mrsavage92/design-intelligence. A skill-folder-only copy does not include the library. Python 3.10+ and Git are the only local prerequisites; scripts use the standard library. Use `python3` or the host's bundled Python executable if `python` is a Windows Store alias. Browsing is supplied by the agent host, not by this repository.

## Codex: one global native link

From the checkout, run:

```text
python scripts/install_codex.py
python scripts/install_codex.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```

This creates `$HOME/.agents/skills/design-research` linked to the checkout's `.agents/skills/design-research`. On Windows the installer uses a junction if symlink privileges are unavailable. It refuses conflicting destinations and duplicate native/legacy user installations, never replaces them, and never modifies `AGENTS.md`, `CLAUDE.md` or Codex configuration. Repeating the installer verifies the same link. Keep the checkout at the same path.

Codex's [official skills documentation](https://learn.chatgpt.com/docs/build-skills) documents user-scoped `.agents/skills`, symlink discovery, implicit matching by description, and explicit `$design-research` invocation. In the desktop composer use the skill selector; CLI/IDE also offer `/skills`. This installation is available on the next turn. Codex detects new skills automatically; restart only if discovery has not refreshed. Discovery makes the skill eligible for relevant tasks; it is not an interception hook or a guarantee of model selection on every prompt. Large skill lists may be shortened by the host.

The skill resolves the link to the canonical checkout. From any other project, run `python <discovered-skill-directory>/scripts/context.py` and verify the returned catalogue, methodology and routing paths. Never read these paths relative to the target project's CWD. Do not install a second copy into `.codex/skills`, paste the library's AGENTS.md into existing projects, or invent a `skills_path` config option. A project may have its own same-name skill: inspect the host's discovery results and resolve any conflict without overwriting project instructions.

The built-in skill-installer can obtain a pinned GitHub skill snapshot for inspection. A detached snapshot alone is not this full-library integration. Native links keep this checkout's resource changes available without copying parallel catalogues.

## Canonical updates and rollback

Inspect `git status --short --branch`, the current revision, and `git remote -v`. Fetch upstream and review changes. Fast-forward a clean intended branch with `git pull --ff-only` only after review; do not reset local work or switch an active linked checkout behind another task. A reviewed feature branch may be installed while its PR is pending; report the exact revision and that it has not merged. Nothing here auto-merges, auto-updates, schedules background work, or auto-pushes findings.

To uninstall, first verify the resolved target. Remove **only the skill link** using a non-recursive symlink/junction removal; do not recursively delete the checkout. Keep research records in Git and the checkout available for rollback.

## Claude Code

The repository includes a Claude skill in `.claude/skills/design-research`. For a user-scoped installation, use a native supported skill link to that folder from the complete checkout, preserving any existing same-name skill. The shared instructions resolve the canonical library through the discovered skill path. Codex's installer and discovery checks do not install or validate Claude Code. Confirm Claude's current conventions and run its own acceptance checks before claiming cross-agent compatibility. Existing Claude instructions remain untouched.

## Verification boundaries

Automated scripts check structure, routes, reference resolution, preservation and installation mechanics. A native `skills/list` host request can confirm discovery from unrelated working directories without starting a model session. A fresh host process repeats that check for persistence. Actual implicit selection after an app restart, Claude execution, mobile/keyboard behavior and conversion results are separate behavioral checks. Record what was actually executed; JSON validity does not establish these outcomes.
