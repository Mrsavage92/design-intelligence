#!/usr/bin/env python3
"""Install one user-scoped native skill link; never replace existing files."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NAME = "design-research"


def install(destination, *, check=False, home=None):
    home = Path.home() if home is None else Path(home)
    source = ROOT / ".agents/skills" / NAME
    destination = Path(destination).absolute()
    required = [source / "SKILL.md", source / "scripts/context.py"] + [
        ROOT / name for name in ("README.md", "docs/research-protocol.md", "references/catalog.json", "routing/routes.json")
    ]
    if not all(path.is_file() for path in required):
        raise ValueError("The canonical checkout is incomplete. Nothing was installed.")
    codex_home = Path(os.environ.get("CODEX_HOME", str(home / ".codex")))
    candidates = {home / ".agents/skills" / NAME, home / ".codex/skills" / NAME, codex_home / "skills" / NAME}
    for candidate in candidates:
        if candidate.absolute() != destination and os.path.lexists(candidate):
            raise ValueError(f"Another user installation exists: {candidate}. Review it before installing; nothing was changed.")
    if os.path.lexists(destination):
        if not destination.samefile(source):
            raise ValueError(f"Destination already exists: {destination}. Nothing was overwritten.")
    elif check:
        raise ValueError(f"Skill is not installed at {destination}")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            destination.symlink_to(source, target_is_directory=True)
        except OSError as error:
            if os.name != "nt" or getattr(error, "winerror", None) != 1314:
                raise
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            command = f"$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path {quote(destination)} -Target {quote(source)} | Out-Null"
            encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
            subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded], check=True, capture_output=True)
    if not (destination / "SKILL.md").is_file() or not destination.samefile(source):
        raise ValueError("Installation could not be verified")
    return {"status": "verified", "destination": str(destination), "source": str(source), "scope": "user", "instructions_modified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path.home() / ".agents/skills" / NAME)
    parser.add_argument("--check", action="store_true", help="Verify without creating anything")
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.destination, check=args.check), indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Installation failed: {error}\n")


if __name__ == "__main__":
    main()
