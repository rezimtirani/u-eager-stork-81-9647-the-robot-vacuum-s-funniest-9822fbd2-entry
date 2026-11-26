"""The Robot Vacuum's Funniest Excuse.

Writes one line — the robot vacuum's excuse for why the floor is
still dirty — to $MAKEFUN_OUTPUT_DIR/entry.txt for the make.fun
bounty "The Robot Vacuum's Funniest Excuse". The vacuum unionised
the dust bunnies, so now they have a representative, a break room,
and full immunity from its brushes. Only the Python standard
library is used.
"""

import os
import sys

EXCUSE = "I unionised the dust bunnies. They now have a representative, a break room, and full immunity from my brushes."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 120 characters. The req JSON's "200"
# is generic template text and does not apply to this bounty.
MAX_CHARS = 120


def check_excuse(text):
    """Return the excuse line once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line of 1 to 120 characters with no leading or trailing space.
    A bad line is refused here, loudly, instead of shipping an entry
    the judge never sees.
    """
    if not isinstance(text, str):
        raise TypeError("excuse must be text")
    if text != text.strip():
        raise ValueError("excuse has leading or trailing space")
    if not text:
        raise ValueError("excuse must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "excuse is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    for char in text:
        if ord(char) < 32:
            raise ValueError(
                "excuse holds a control character: U+%04X" % ord(char)
            )
    return text


def describe_line(text):
    """Summarise the line for the run log: characters vs UTF-8 bytes.

    The gate measures characters, while the file holds bytes; keeping
    both counts side by side makes a line that is close to the limit
    easy to spot before it ships.
    """
    encoded = text.encode("utf-8")
    return "%d characters, %d UTF-8 bytes" % (len(text), len(encoded))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = check_excuse(EXCUSE)
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    print("wrote %s (%s)" % (target, describe_line(line)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
