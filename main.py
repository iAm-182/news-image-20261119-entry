#!/usr/bin/env python3
"""news-image-20261119 entry: copy the pre-drawn front page to the output.

The image (entry.png, drawn by draw.py in this repo) sums up Thursday
19 November 2026 in one picture: ten illustrated lead stories, a
by-the-numbers strip and twelve one-line briefs. The grader runs with no
network and standard library only, so the program just copies the file.
Deterministic: both runs write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
# Guard the gate: the copy must be byte-identical to the source image.
assert os.path.getsize(dst) == os.path.getsize(src), "copy size mismatch"
print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
