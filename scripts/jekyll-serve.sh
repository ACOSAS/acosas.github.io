#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

command -v bundle >/dev/null || {
    echo "Bundler is required. Install Ruby 3.2+ and: gem install bundler -v '~> 2.4.22'" >&2
    exit 1
}

jekyll_exe="$(bundle show jekyll)/exe/jekyll"
if [[ ! -f "$jekyll_exe" ]]; then
    echo "Jekyll executable not found at $jekyll_exe. Run: bundle install" >&2
    exit 1
fi

if [[ $# -eq 0 ]]; then
    set -- serve --incremental --host 127.0.0.1
fi

exec bundle exec ruby "$jekyll_exe" "$@"
