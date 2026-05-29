#!/usr/bin/env bash

# This script is run automatically by GitHub Actions (see .github/workflows/docs.yml),
# along with `zensical build`.

# Build the example marimo notebook for hosting/serving via Zensical with interactivity via Wasm.
# This script should be run from the root directory of the project.
# After this script runs, the site can be built via, e.g., `uv run zensical build`.

# Export the notebook to HTML with Wasm.
uv run marimo export html-wasm --mode edit --sandbox examples/example.py -o docs/example/

# Turn "auto_instantiate" on so the Wasm notebook runs on startup...by "manually" editing the HTML.
# Specifically, replace `"auto_instantiate": false` with `"auto_instantiate": true`.
sed -i.bak 's/"auto_instantiate": false/"auto_instantiate": true/' docs/example/index.html
rm docs/example/index.html.bak

# Build a wheel for `disperse` and move it to `docs/` so it can be served alongside the notebook.
uv build --wheel
mv dist/disperse-0.2.0-py3-none-any.whl docs/
rm dist/.gitignore
rmdir dist/
