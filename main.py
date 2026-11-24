#!/usr/bin/env python3
"""Make the AI Judge Laugh: the Office Joke Open.

The program keeps a shortlist of one-line office jokes with the reason
each one was kept or rejected, picks the winner against the judge's
brief (an office joke first, then an earned turn in the last words, a
specific office detail, freshness, tightness), and writes the selected
line to the entry file untouched, so both runs of the program produce
byte-identical output.

The joke: inbox zero finally reached — and Outlook celebrates it by
scheduling a meeting about it.
"""

import os

# Candidate jokes, with the reason each one was kept or rejected.
# The judge weighs the office joke first, then a turn that pays off in
# the last few words, a specific office detail, freshness and
# tightness — so a candidate wins only if it lands a surprising turn
# on a concrete office artifact without reading as a complaint.
_CANDIDATES = [
    # Winner (local score 68.2, one-liner archetype): the payoff lands
    # in the last three words ("to celebrate it") on a quoted, concrete
    # artifact — a meeting called 'Inbox Zero'. Pure joke, no complaint;
    # the app celebrates the achievement by creating the very thing the
    # worker escaped. Original phrasing, 18 words, 99 characters.
    (
        "I finally got my inbox to zero, so Outlook scheduled a meeting "
        "called 'Inbox Zero' to celebrate it.",
        "selected",
    ),
    # Rejected: highest local pattern score (97.0 — two quoted segments,
    # detected twist) but the payoff is a cynical complaint ("we will
    # never hire anyone to help you"), and the judge's first criterion
    # penalises a joke that reads as a complaint or a remark.
    (
        "My review says I 'thrive under pressure', which is HR for 'we "
        "will never hire anyone to help you'.",
        "rejected: payoff reads as a complaint, not a joke beat",
    ),
    # Rejected: clean joke on the canonical detail (the meeting that
    # could have been an email) and a sharp ironic escalation, but the
    # "meeting about the meeting" setup is the most familiar trope in
    # the pool — freshness risk against the winner.
    (
        "I asked HR if my meeting could have been an email; they "
        "scheduled a meeting to discuss it.",
        "rejected: familiar setup, freshness risk",
    ),
    # Rejected: the 'per my last email' detail is specific, but the
    # payoff ("even my absence is passive-aggressive") is a remark
    # about the setup, not a turn that lands in the last words.
    (
        "I put 'per my last email' in my out-of-office reply, so now "
        "even my absence is passive-aggressive.",
        "rejected: payoff is a remark, not a turn",
    ),
    # Rejected: addresses the judge directly, which the rules allow,
    # but it risks reading as pandering to the judge rather than an
    # office joke — the judge's first criterion wants the joke to be
    # about office life first.
    (
        "Dear judge, I wrote this joke in a meeting that could have been "
        "an email — so you're reading my timesheet.",
        "rejected: direct judge address risks reading as pandering",
    ),
]


def select_joke() -> str:
    """Pick the winning candidate.

    A candidate is eligible only if it is 1 to 200 characters and not
    only white space; among the eligible ones the one marked
    "selected" wins. Exactly one candidate must be selected.
    """
    selected = [text for text, verdict in _CANDIDATES if verdict == "selected"]
    if len(selected) != 1:
        raise ValueError("exactly one candidate must be marked selected")
    joke = selected[0]
    if not 1 <= len(joke) <= 200:
        raise ValueError("the joke must be 1 to 200 characters long")
    if not joke.strip():
        raise ValueError("the joke must contain a non-space character")
    return joke


# The joke this program writes: the selected candidate, unchanged.
JOKE = select_joke()


def entry_path() -> str:
    """Return where the joke file goes.

    The grader points MAKEFUN_OUTPUT_DIR at the output folder; outside
    the grader the joke lands in /output, as the competition requires.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main() -> None:
    # Re-select at run time so the written file always comes from the
    # same selection logic the module validated at import.
    joke = select_joke()
    path = entry_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(joke)
    print(f"wrote {path} ({len(joke.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
