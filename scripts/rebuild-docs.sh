#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

if [[ ! -f "$root/build_pages.sh" ]]; then
    echo "Run this script from an Integration.Documentation checkout." >&2
    exit 1
fi

command -v ruby >/dev/null || {
    echo "Ruby is required to run build_pages.sh." >&2
    exit 1
}

if [[ $# -gt 0 ]]; then
    echo "Generating OpenAPI stubs for: $*"
else
    echo "Generating OpenAPI stubs for all files in _data/swagger"
fi
ruby ./build_pages.sh "$@"

echo "Composing overlays, index pages and sidebars"
python3 "$root/scripts/compose-overlays.py" "$root"
