#!/usr/bin/env bash
# Rebuild the dashboard from the latest digests + resumes, then open it.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$DIR/build.py"
open "$DIR/index.html"
