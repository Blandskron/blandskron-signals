#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q apps
git diff --check
echo "Python compilation and diff checks passed."
