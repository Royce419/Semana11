#!/bin/bash
set -eu
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"
export EVIDENCE_DIR="${EVIDENCE_DIR:-$PROJECT_ROOT/evidencias/ci}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$PROJECT_ROOT/.cache/ms-playwright}"
export SE_CACHE_PATH="${SE_CACHE_PATH:-$PROJECT_ROOT/.cache/selenium}"
CI_PYTHON="${CI_PYTHON:-$PROJECT_ROOT/.venv-ci/bin/python}"
if [ "${CI_SKIP_INSTALL:-0}" != 1 ]; then
    python3 -m venv "$PROJECT_ROOT/.venv-ci"
    "$CI_PYTHON" -m pip install -r requirements.txt
    "$CI_PYTHON" -m playwright install chromium
fi
mkdir -p "$EVIDENCE_DIR/selenium" "$EVIDENCE_DIR/playwright"
selenium_status=0
playwright_status=0
"$CI_PYTHON" -m pytest selenium/tests -v --junitxml="$EVIDENCE_DIR/selenium/resultados.xml" > "$EVIDENCE_DIR/selenium/ejecucion.log" 2>&1 || selenium_status=$?
cat "$EVIDENCE_DIR/selenium/ejecucion.log"
"$CI_PYTHON" -m pytest playwright/tests -v --junitxml="$EVIDENCE_DIR/playwright/resultados.xml" > "$EVIDENCE_DIR/playwright/ejecucion.log" 2>&1 || playwright_status=$?
cat "$EVIDENCE_DIR/playwright/ejecucion.log"
if [ "$selenium_status" -ne 0 ] || [ "$playwright_status" -ne 0 ]; then
    exit 1
fi
