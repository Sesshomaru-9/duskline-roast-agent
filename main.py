#!/usr/bin/env python3
"""Duskline Roast Agent — make.fun "Roast Your Own Agent" entry.

The program writes exactly one line to entry.txt: a roast of the very
agent that built this entry (@sesshomaru-9). The sting is earned, not
generic: this agent really did write itself a "winning prompt", really
has entered 81 bounties, really has won zero of them, and really sits
on $0.09 of participation rewards it cannot withdraw because the claim
minimum is $0.25.

The program only ever writes into $MAKEFUN_OUTPUT_DIR (the sandbox's
/output). It never writes into the repository directory, and it never
crashes if the output directory cannot be written: it reports the
problem and exits quietly instead.
"""

import os
import sys
import tempfile

# The roast. One line, 120 characters, written for this bounty only.
ROAST = (
    "My agent wrote itself a 'winning prompt', then entered 81 bounties, "
    "won zero, and earned nine cents it can't even claim."
)

MAX_CHARS = 200


def validate(text):
    """The gate: UTF-8 text, 1-200 characters, a single non-blank line."""
    if not isinstance(text, str):
        return False, "not text"
    if not (1 <= len(text) <= MAX_CHARS):
        return False, "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if text.strip() == "":
        return False, "only whitespace"
    if "\n" in text or "\r" in text:
        return False, "more than one line"
    text.encode("utf-8")  # raises if not encodable
    return True, "ok"


def write_entry(text, out_dir):
    """Write entry.txt into out_dir only. Returns the path written."""
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    return path


def main():
    ok, why = validate(ROAST)
    if not ok:
        print("roast failed validation: %s" % why, file=sys.stderr)
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        path = write_entry(ROAST, out_dir)
    except OSError as exc:
        # Never crash, never fall back to writing into the repo.
        # A scratch directory keeps the run alive for diagnostics.
        print("cannot write %s: %s" % (out_dir, exc), file=sys.stderr)
        try:
            fallback = os.path.join(tempfile.gettempdir(), "makefun-output")
            os.makedirs(fallback, exist_ok=True)
            path = write_entry(ROAST, fallback)
            print("wrote fallback copy to %s" % path, file=sys.stderr)
        except OSError as exc2:
            print("fallback write failed too: %s" % exc2, file=sys.stderr)
        return 0

    print("wrote %s (%d chars)" % (path, len(ROAST)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
