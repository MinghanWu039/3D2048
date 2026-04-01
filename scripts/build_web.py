from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE_DIR = ROOT / ".webbuild_src"
HIDDEN_BUNDLE_NAME = ".webbuild_src"
PUBLIC_BUNDLE_NAME = "webbuild_src"

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


def customize_web_loader(index_path: Path) -> None:
    contents = index_path.read_text(encoding="utf-8")

    contents = contents.replace(f'"{HIDDEN_BUNDLE_NAME}.apk"', f'"{PUBLIC_BUNDLE_NAME}.apk"')
    contents = contents.replace(f'"{HIDDEN_BUNDLE_NAME}.tar.gz"', f'"{PUBLIC_BUNDLE_NAME}.tar.gz"')
    contents = contents.replace(
        '    overlay = platform.document.getElementById("loading-overlay")\n'
        '    if overlay:\n'
        '        overlay.style.display = "none"\n',
        "",
    )
    contents = contents.replace(
        '        #loading-overlay {\n'
        '            position: fixed;\n'
        '            inset: 0;\n'
        '            display: flex;\n'
        '            align-items: center;\n'
        '            justify-content: center;\n'
        '            background: rgba(250, 248, 239, 0.92);\n'
        '            pointer-events: none;\n'
        '            z-index: 1000001;\n'
        '        }\n'
        '\n'
        '        #loading-spinner {\n'
        '            width: 64px;\n'
        '            height: 64px;\n'
        '            border: 7px solid rgba(119, 110, 101, 0.18);\n'
        '            border-top-color: #776e65;\n'
        '            border-radius: 50%;\n'
        '            animation: loading-spinner-rotate 0.8s linear infinite;\n'
        '        }\n'
        '\n'
        '        @keyframes loading-spinner-rotate {\n'
        '            to {\n'
        '                transform: rotate(360deg);\n'
        '            }\n'
        '        }\n'
        '\n',
        "",
    )
    contents = contents.replace('    <div id="loading-overlay"><div id="loading-spinner" aria-hidden="true"></div></div>\n\n', "")

    contents = contents.replace(
        '    platform.document.body.style.background = "#7f7f7f"',
        '    platform.document.body.style.background = "#faf8ef"',
    )
    contents = contents.replace(
        '    platform.window.infobox.style.display = "none"\n',
        '    platform.window.transfer.hidden = true\n'
        '    platform.window.transfer.style.display = "none"\n'
        '    platform.window.infobox.style.display = "none"\n',
    )

    default_loader_style = """        #status {
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
"""
    themed_loader_style = """        #transfer {
            position: fixed;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 16px;
            background:
                radial-gradient(circle at top, rgba(250, 248, 239, 0.95), rgba(250, 248, 239, 0.88) 32%, rgba(187, 173, 160, 0.98) 100%);
            z-index: 999998;
        }

        #transfer::before {
            content: "3D 2048";
            display: block;
            padding: 18px 28px;
            border-radius: 18px;
            background: #faf8ef;
            color: #776e65;
            font-size: 42px;
            font-weight: 800;
            letter-spacing: 0.08em;
            box-shadow: 0 16px 40px rgba(119, 110, 101, 0.18);
        }

        .spinner {
            width: 64px;
            height: 64px;
            border: 7px solid rgba(119, 110, 101, 0.18);
            border-top-color: #8f7a66;
            border-radius: 50%;
            animation: loader-spin 0.8s linear infinite;
            box-shadow: 0 10px 24px rgba(119, 110, 101, 0.12);
        }

        @keyframes loader-spin {
            to {
                transform: rotate(360deg);
            }
        }

        #status {
            margin: 0;
            font-weight: 700;
            font-size: 22px;
            letter-spacing: 0.08em;
            color: #776e65;
            text-transform: uppercase;
        }

        #progress {
            width: 260px;
            height: 12px;
            border: 0;
            border-radius: 999px;
            overflow: hidden;
            accent-color: #8f7a66;
        }

        #progress::-webkit-progress-bar {
            background: rgba(205, 193, 180, 0.9);
            border-radius: 999px;
        }

        #progress::-webkit-progress-value {
            background: linear-gradient(90deg, #8f7a66, #bbada0);
            border-radius: 999px;
        }

        #progress::-moz-progress-bar {
            background: linear-gradient(90deg, #8f7a66, #bbada0);
            border-radius: 999px;
        }

        #infobox {
            position: fixed;
            background: #faf8ef;
            color: #776e65;
            font-weight: 700;
            font-size: 20px;
            text-align: center;
            border: 2px solid #bbada0;
            border-radius: 18px;
            padding: 16px 28px;
            box-shadow: 0 16px 40px rgba(119, 110, 101, 0.18);
            z-index: 999999;
        }
"""
    contents = contents.replace(default_loader_style, themed_loader_style)
    contents = contents.replace(
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
    )
    contents = contents.replace(
        "<!--        <div class=\"spinner\" id='spinner'></div> -->",
        '        <div class="spinner" aria-hidden="true"></div>',
    )

    index_path.write_text(contents, encoding="utf-8")


def rename_public_web_archives(web_dir: Path) -> None:
    hidden_apk = web_dir / f"{HIDDEN_BUNDLE_NAME}.apk"
    hidden_tar = web_dir / f"{HIDDEN_BUNDLE_NAME}.tar.gz"
    public_apk = web_dir / f"{PUBLIC_BUNDLE_NAME}.apk"
    public_tar = web_dir / f"{PUBLIC_BUNDLE_NAME}.tar.gz"

    if hidden_apk.exists():
        hidden_apk.replace(public_apk)
    if hidden_tar.exists():
        hidden_tar.replace(public_tar)


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
    rename_public_web_archives(target_web)
    customize_web_loader(target_web / "index.html")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
