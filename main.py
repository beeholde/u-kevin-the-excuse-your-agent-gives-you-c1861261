#!/usr/bin/env python3
"""Write the single excuse line for this make.fun entry.

The whole entry is one line of text. This program keeps that line as a
constant, runs it through a small gate (UTF-8 text, one line, between
1 and 200 characters, not blank, no control characters), and stores
the exact bytes in /output/entry.txt. An optional first argument can
point the output at another path, which is only used for local checks;
with no argument the grader path is used.
"""

import sys
import unicodedata
from pathlib import Path

LINE = (
    "I told it to retry until it worked. It worked 8,000 times. "
    "Your inbox is now mostly me saying 'it worked.'"
)

DEFAULT_TARGET = Path("/output/entry.txt")
LOWER = 1
UPPER = 200


def gate(text):
    """Return the trimmed line if it passes, otherwise raise."""
    if not isinstance(text, str):
        raise TypeError("line must be text")
    trimmed = text.strip()
    if trimmed == "":
        raise ValueError("line is blank")
    if "\n" in trimmed or "\r" in trimmed:
        raise ValueError("line spans more than one line")
    for char in trimmed:
        if unicodedata.category(char) == "Cc":
            raise ValueError("line contains a control character")
    size = len(trimmed)
    if size < LOWER or size > UPPER:
        raise ValueError("line length %d outside %d-%d" % (size, LOWER, UPPER))
    return trimmed


def target_path(argv):
    if len(argv) > 1:
        return Path(argv[1])
    return DEFAULT_TARGET


def verify_stored(destination, payload):
    """Read the stored file back and require an exact byte match.

    The gate above checked the line in memory; this checks what
    actually landed on disk, so a truncated write or an added
    trailing newline cannot silently change the entry.
    """
    stored = destination.read_bytes()
    if stored != payload:
        raise RuntimeError(
            "stored %d bytes, expected %d" % (len(stored), len(payload))
        )
    if stored.endswith(b"\n"):
        raise RuntimeError("stored file ends with a newline")


def emit(argv):
    line = gate(LINE)
    payload = line.encode("utf-8")
    destination = target_path(argv)
    destination.write_bytes(payload)
    verify_stored(destination, payload)
    print("%d chars %d bytes" % (len(line), len(payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(emit(sys.argv))
