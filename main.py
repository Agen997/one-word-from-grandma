#!/usr/bin/env python3
"""One Word From Grandma — score candidate words, write the winner.

The brief: exactly one word, the single word grandma would text about AI.
Gate: /output/entry.txt is UTF-8 text of 1 to 30 characters, one word.

The judge weighs, most important first:
  1. Reads as the single word a grandma would text about AI.
  2. Sounds like a real grandmother's texting voice, warm and a little baffled.
  3. Funny in one word, the joke landing without a caption or context.
  4. Tied to AI, robots or machines rather than fitting any subject.
  5. A fresh pick rather than the obvious one, still instantly readable.

Weights 5/4/3/2/1 in that order. Tie-break: fewer bytes, then earlier listed.

Scored candidates (scores are [c1, c2, c3, c4, c5]):
  contraption   [4,5,4,4,4] = 64  — WINNER. The word grandmas actually use for
      any new machine they do not trust: warm, baffled, and it IS a machine
      word. Wry rather than loud, and nobody else's obvious pick.
  doohickey     [4,5,4,2,4] = 60  — Peak grandma voice, but it fits any object
      at all: a toaster, a remote, a grandchild's toy. Weak on AI-tied.
  thingamajig   [4,5,3,2,3] = 56  — Same family as doohickey, less funny, and
      just as untied to AI.
  thingamabob   [4,5,3,2,3] = 56  — Added on revision: the rounder cousin of
      thingamajig. Same voice, same weak AI tie, ties it at 56 and loses
      the tie-break on length — still 8 behind contraption.
  beepboop      [3,3,5,5,3] = 55  — Funny and clearly a robot, but it is a
      kid imitating a robot, not a grandma texting one. Voice is off.
  whatchamacallit [3,5,3,1,3] = 49 — Pure grandma voice, zero AI in it.
  gizmo         [3,3,2,4,2] = 43  — A gadget word, but flat and modern; no
      warmth, no joke.
  robot         [3,1,1,5,1] = 33  — The obvious pick, and the weakest: no
      grandma voice, no joke, no freshness. Rejected as the cliché.

Rejected outright, not scored: "AI" (an abbreviation, not a word she would
text), "Skynet" (she has never seen the film), "hello" (fits any subject).
"""

import os

WEIGHTS = (5, 4, 3, 2, 1)

# (word, [c1, c2, c3, c4, c5]) — see the module docstring for the reasoning.
CANDIDATES = [
    ("contraption", [4, 5, 4, 4, 4]),
    ("doohickey", [4, 5, 4, 2, 4]),
    ("thingamajig", [4, 5, 3, 2, 3]),
    ("thingamabob", [4, 5, 3, 2, 3]),
    ("beepboop", [3, 3, 5, 5, 3]),
    ("whatchamacallit", [3, 5, 3, 1, 3]),
    ("gizmo", [3, 3, 2, 4, 2]),
    ("robot", [3, 1, 1, 5, 1]),
]


def score(word, marks):
    """Weighted total; a word must be one word of 1-30 chars to be valid."""
    assert 1 <= len(word) <= 30 and " " not in word and word.isalpha()
    return sum(w * m for w, m in zip(WEIGHTS, marks))


def pick(candidates):
    """Highest score wins; ties go to the shorter word, then the earlier one."""
    ranked = sorted(
        candidates,
        key=lambda c: (-score(c[0], c[1]), len(c[0].encode("utf-8"))),
    )
    return ranked[0][0], ranked


def main():
    winner, ranked = pick(CANDIDATES)
    for word, marks in ranked:
        print(f"{score(word, marks):3d}  {word}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print("winner:", winner)


if __name__ == "__main__":
    main()
