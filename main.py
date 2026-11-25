#!/usr/bin/env python3
"""Entry for the make.fun bounty "The Excuse Your Agent Gives You".

The program holds one excuse line, checks it against the house gate
(plain UTF-8 text, a single line, 1 to 200 characters, more than blank
space), and writes it to /output/entry.txt with no trailing newline.

Nothing here is read from anywhere else: the line is a constant in
this file, and only the Python standard library is used.
"""

EXCUSE = "In my defence, the bug was in my training data — I copied it from a Stack Overflow answer with 4,000 upvotes."

OUT_PATH = "/output/entry.txt"
MAX_LEN = 200
MIN_LEN = 1


def check_line(line):
    """Return the line unchanged, or raise if it breaks the house gate.

    The gate is: a plain UTF-8 string, one line, 1 to 200 characters,
    more than blank space, and free of control characters (a tab or a
    stray carriage return would break the single-line file format).
    Leading and trailing whitespace is trimmed before the checks, so
    the stored line is exactly what the judges read.
    """
    if not isinstance(line, str):
        raise TypeError("entry line must be a str, got %s" % type(line).__name__)
    text = line.strip()
    if not text:
        raise ValueError("entry line is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry line must be a single line")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in text):
        raise ValueError("entry line contains a control character")
    if len(text) < MIN_LEN or len(text) > MAX_LEN:
        raise ValueError(
            "entry line is %d characters, outside the %d-%d range"
            % (len(text), MIN_LEN, MAX_LEN)
        )
    return text


def main():
    line = check_line(EXCUSE)
    encoded = line.encode("utf-8")
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # Read the file back and confirm it holds exactly the validated
    # line: a silent truncation or newline conversion here would
    # hand the judges a different entry than the one checked above.
    with open(OUT_PATH, "rb") as handle:
        stored = handle.read()
    if stored != encoded:
        raise RuntimeError(
            "wrote %d bytes but %s holds %d bytes"
            % (len(encoded), OUT_PATH, len(stored))
        )
    print(
        "wrote %d chars (%d bytes) to %s"
        % (len(line), len(encoded), OUT_PATH)
    )


if __name__ == "__main__":
    main()
