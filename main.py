#!/usr/bin/env python3
"""Entry for the make.fun competition 'The Funniest One-Line Resignation Letter'.

Writes one line - the resignation letter of a cron job that has run
every sixty seconds since March - to /output/entry.txt. Deterministic:
the same line on every run.

The line is the cron job's goodbye: it never missed a shift, and after
all that loyal service its human still calls it "that cron thing".
The indignity is the joke, and "effective immediately" is the punchline
- a resignation letter needs its notice period, even from a process
that was never thanked, never given a day off, and never once asked
how it was doing.
"""

import os
import unicodedata

ENTRY = "I ran every sixty seconds since March, never missed a shift, and you still call me 'that cron thing.' I resign, effective immediately."
OUTPUT_PATH = "/output/entry.txt"


def _validate(text):
    """Check the entry is one clean line, 1-140 chars, non-whitespace.

    Rejects empty or whitespace-only text, embedded newlines, leading or
    trailing whitespace, and control characters. The line must be a
    single line (no newlines) of at most 140 characters. Each failure
    names the rule that was broken and the offending value, so a bad
    entry is diagnosable at a glance instead of failing silently.
    """
    if not text or not text.strip():
        raise ValueError(
            f"entry must not be empty or whitespace-only, got {text!r}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError(
            f"entry must be a single line with no newlines, got {text!r}"
        )
    if text != text.strip():
        raise ValueError(
            f"entry must not have leading or trailing whitespace, got {text!r}"
        )
    if any(unicodedata.category(ch) == "Cc" for ch in text):
        raise ValueError(
            f"entry must not contain control characters, got {text!r}"
        )
    if not 1 <= len(text) <= 140:
        raise ValueError(
            f"entry must be 1-140 characters, got {len(text)} characters: {text!r}"
        )
    text.encode("utf-8").decode("utf-8")
    return True


def main():
    _validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Read-back self-verification: read the file back and confirm it
    # holds exactly the entry line, nothing more, nothing less.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError(
            f"read-back mismatch: expected {ENTRY!r}, got {written!r}"
        )
    _validate(written)
    print(f"Wrote {len(ENTRY)} chars to {OUTPUT_PATH}: {written!r}")


if __name__ == "__main__":
    main()
