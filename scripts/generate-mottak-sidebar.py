#!/usr/bin/env python3
"""Compatibility wrapper. Overlay compose owns Mottak sidebar and index pages."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: scripts/generate-mottak-sidebar.py <pages-checkout>", file=sys.stderr)
        return 2
    compose = Path(__file__).with_name("compose-overlays.py")
    argv = [sys.executable, str(compose), sys.argv[1]]
    raise SystemExit(__import__("subprocess").call(argv))


if __name__ == "__main__":
    raise SystemExit(main())
