#!/usr/bin/env python3
"""Ship the entry image to the make.fun output directory.

Reads entry.png from this script's folder, confirms the PNG signature,
then drops an exact copy into $MAKEFUN_OUTPUT_DIR (or /output by default).
"""

import hashlib
import os
import sys
from pathlib import Path

EXPECTED_MAGIC = bytes.fromhex("89504e470d0a1a0a")
FILENAME = "entry.png"
FALLBACK_DIR = "/output"
LIMIT_BYTES = 1024 * 1024  # entry images must stay under 1 MiB


def die(reason):
    """Report a fatal problem and stop with a non-zero exit status."""
    print(f"fatal: {reason}", file=sys.stderr)
    sys.exit(1)


def read_png(script_folder):
    """Load entry.png next to the script, refusing anything that is not PNG."""
    path = script_folder / FILENAME
    if not path.exists():
        die(f"cannot find {path}")
    data = path.read_bytes()
    if len(data) > LIMIT_BYTES:
        die(f"entry.png is {len(data)} bytes, over the {LIMIT_BYTES} byte limit")
    if data[:8] != EXPECTED_MAGIC:
        die("entry.png does not start with the PNG signature")
    return data


def main():
    folder = Path(__file__).parent.resolve()
    data = read_png(folder)

    destination = Path(os.getenv("MAKEFUN_OUTPUT_DIR", FALLBACK_DIR))
    destination.mkdir(parents=True, exist_ok=True)
    outfile = destination / FILENAME
    outfile.write_bytes(data)

    print("output:", outfile)
    print("sha256:", hashlib.sha256(data).hexdigest())
    print("size:", len(data), "bytes")


if __name__ == "__main__":
    main()
