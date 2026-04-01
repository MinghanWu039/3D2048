from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE_DIR = ROOT / ".webbuild_src"
DEFAULT_INFOBOX_TEXT = "Loading, please wait ..."

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


def replace_once(contents: str, old: str, new: str) -> str:
    if old not in contents:
        raise RuntimeError(f"Expected snippet not found in generated web index: {old[:40]!r}")
    return contents.replace(old, new, 1)


def customize_web_loader(index_path: Path) -> None:
    contents = index_path.read_text(encoding="utf-8")

    replacements = [
        (
            """    platform.document.body.style.background = "#7f7f7f"
""",
            """    platform.document.body.style.background = "#faf8ef"
""",
        ),
        (
            """    platform.window.transfer.hidden = true
""",
            """    platform.window.transfer.hidden = false
""",
        ),
        (
            """        platform.window.infobox.innerText = msg
""",
            """        platform.window.infobox.innerText = msg
        platform.window.show_infobox()
""",
        ),
        (
            """        platform.window.infobox.innerText = f"installing {pkg}"
""",
            """        platform.window.infobox.innerText = f"installing {pkg}"
        platform.window.show_infobox()
""",
        ),
        (
            """    await shell.source(main, callback=ui_callback)

    # if you don't reach that step
    # your main.py has an infinite sync loop somewhere !

    platform.window.infobox.style.display = "none"
""",
            """    await shell.source(main, callback=ui_callback)

    # if you don't reach that step
    # your main.py has an infinite sync loop somewhere !

    platform.window.transfer.hidden = true
    platform.window.infobox.style.display = "none"
""",
        ),
        (
            """function show_infobox() {
    infobox.style.display = "block";

    // Measure box
    const w = infobox.offsetWidth;
    const h = infobox.offsetHeight;

    // Center in viewport
    const left = (window.innerWidth - w) / 2;
    const top = (window.innerHeight - h) / 2;

    infobox.style.left = left + "px";
    infobox.style.top = top + "px";
}
""",
            f"""function show_infobox() {{
    const message = infobox.innerText.trim();
    if (!message || message === "{DEFAULT_INFOBOX_TEXT}") {{
        infobox.style.display = "none";
        return;
    }}

    infobox.style.display = "block";

    // Measure box
    const w = infobox.offsetWidth;
    const h = infobox.offsetHeight;

    // Center in viewport
    const left = (window.innerWidth - w) / 2;
    const top = (window.innerHeight - h) / 2;

    infobox.style.left = left + "px";
    infobox.style.top = top + "px";
}}
""",
        ),
        (
            """        #status {
            display: inline-block;
            vertical-align: top;
            margin-top: 20px;
            margin-left: 30px;
            font-weight: bold;
            color: rgb(120, 120, 120);
        }

        #progress {
            height: 20px;
            width: 300px;
        }

        #infobox {
            position: fixed; /* center relative to viewport */
            background: green;
            color: blue;
            font-weight: bold;
            padding: 12px 24px;
 /*           display: none; */
            z-index: 999999;
        }
""",
            """        #transfer {
            position: fixed;
            inset: 0;
            display: flex;
            flex-direction: column;
            gap: 18px;
            align-items: center;
            justify-content: center;
            background: #faf8ef;
            z-index: 20;
        }

        #transfer .loading-title {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: #776e65;
        }

        #transfer .spinner {
            width: 72px;
            height: 72px;
            border: 7px solid rgba(119, 110, 101, 0.18);
            border-top-color: #776e65;
            border-radius: 50%;
            animation: spinner-rotate 0.8s linear infinite;
        }

        @keyframes spinner-rotate {
            to {
                transform: rotate(360deg);
            }
        }

        #status {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }

        #progress {
            display: none;
        }

        #infobox {
            position: fixed;
            background: transparent;
            color: #776e65;
            font-weight: 600;
            padding: 0;
            z-index: 21;
            display: none;
        }
""",
        ),
        (
            """        body {
            font-family: arial;
            margin: 0;
            padding: none;
            background-color:powderblue;
        }
""",
            """        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #faf8ef;
        }
""",
        ),
        (
            """    <div id="transfer" align=center>
<!--        <div class="spinner" id='spinner'></div> -->
        <div class="emscripten" id="status">Downloading...</div>
        <div class="emscripten">
            <progress value="0" max="100" id="progress"></progress>
        </div>
    </div>
""",
            """    <div id="transfer" align=center>
        <div class="loading-title">3D 2048</div>
        <div class="spinner" aria-hidden="true"></div>
        <div class="emscripten" id="status">Downloading...</div>
        <div class="emscripten">
            <progress value="0" max="100" id="progress"></progress>
        </div>
    </div>
""",
        ),
    ]

    for old, new in replacements:
        contents = replace_once(contents, old, new)

    index_path.write_text(contents, encoding="utf-8")


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
    customize_web_loader(target_web / "index.html")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
