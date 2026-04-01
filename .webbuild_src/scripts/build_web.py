from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE_DIR = ROOT / ".webbuild_src"

EXCLUDE_DIRS = {
    ".venv",
    "build",
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
}

EXCLUDE_FILES = {
    ".DS_Store",
}


def should_ignore(directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in EXCLUDE_DIRS or name in EXCLUDE_FILES:
            ignored.add(name)
    return ignored


def main() -> int:
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)

    shutil.copytree(ROOT, STAGE_DIR, ignore=should_ignore)

    cmd = [sys.executable, "-m", "pygbag", "--build", str(STAGE_DIR)]
    completed = subprocess.run(cmd, cwd=ROOT)
    if completed.returncode != 0:
        return completed.returncode

    staged_web = STAGE_DIR / "build" / "web"
    target_web = ROOT / "build" / "web"

    if target_web.exists():
        shutil.rmtree(target_web)
    target_web.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(staged_web, target_web)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
