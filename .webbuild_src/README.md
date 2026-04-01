# 3D2048

A `pygame`-based 3D-style 2048 game that can run locally and be packaged for the web with `pygbag`.

## Local desktop run

```zsh
python3 -m pip install -r requirements.txt
python3 main.py
```

## Build for web (WASM)

```zsh
python3 -m pip install -r requirements.txt
/Users/wuminghan/Documents/trae_projects/3D2048/.venv/bin/python scripts/build_web.py
```

The generated static site is expected at `build/web`.
The build script stages source files into `.webbuild_src` and excludes local folders like `.venv`.

## Local preview (same files as GitHub Pages)

To debug the exact artifact that GitHub Pages deploys, build first and then serve `build/web` locally.

```zsh
python3 -m pip install -r requirements.txt
/Users/wuminghan/Documents/trae_projects/3D2048/.venv/bin/python scripts/build_web.py
python3 scripts/serve_web.py
```

Then open: `http://127.0.0.1:8000`

If you want to inspect raw `pygbag` output before the project-specific post-processing, you can still run:

```zsh
/Users/wuminghan/Documents/trae_projects/3D2048/.venv/bin/python -m pygbag .webbuild_src
```

## Deploy to GitHub Pages

A workflow is included at `.github/workflows/deploy-pages.yml`.

1. Push to `main`.
2. In GitHub repo settings, enable **Pages** with source: **GitHub Actions**.
3. The workflow builds with `pygbag` and publishes `build/web`.

## Controls

- Arrow keys / `WASD`: move on plane
- `Q` / `E`: move between layers
- Mouse drag: rotate the 3D view
