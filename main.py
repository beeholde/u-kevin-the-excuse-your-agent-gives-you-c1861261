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


def check_line(line):
    """Return the line unchanged, or raise if it breaks the house gate."""
    text = line.strip()
    if not text:
        raise ValueError("entry line is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry line must be a single line")
    if len(text) > 200:
        raise ValueError(
            "entry line is %d characters, over the 200 limit" % len(text)
        )
    return text


def main():
    line = check_line(EXCUSE)
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    print(
        "wrote %d chars (%d bytes) to %s"
        % (len(line), len(line.encode("utf-8")), OUT_PATH)
    )


if __name__ == "__main__":
    main()
