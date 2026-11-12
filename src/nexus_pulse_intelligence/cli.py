"""Safe command-line checks for the bootstrap phase."""

from __future__ import annotations

import argparse
import platform
import sys

from nexus_pulse_intelligence import __version__


def run_doctor() -> int:
    """Report non-sensitive runtime information; never print environment secrets."""
    major, minor = sys.version_info[:2]
    print(f"NEXUS PULSE Intelligence Engine {__version__}")
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.system()} {platform.machine()}")
    if (major, minor) < (3, 11):
        print("Status: FAIL — Python 3.11 or newer is required.")
        return 1
    print("Status: OK — bootstrap runtime is compatible.")
    print("Mode: bootstrap only; no sources, secrets, or production services are accessed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="np-intel", description="NEXUS PULSE Intelligence Engine")
    parser.add_argument("command", choices=("doctor", "version"), help="Safe diagnostic command")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "doctor":
        return run_doctor()
    print(__version__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
