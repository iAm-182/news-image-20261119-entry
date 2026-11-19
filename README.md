# The World in One Day — Thursday 19 November 2026

Entry for the make.fun competition `news-image-20261119`: one image that
sums up Thursday 19 November 2026's world news.

## The image

A newspaper front page, drawn entirely with PIL primitives (no external
images): a masthead naming the day, a lead story on the Trump–Xi–Putin
trilateral meeting in Shenzhen, nine more numbered illustrated stories
(Anthropic's record $81.3bn IPO, GTA VI's global rollout, Jeffries poised
to become the first Black Speaker, the Crimean Bridge attacked again, a
record $190.4m Van Gogh sale, the ICJ's Rohingya verdict, Cyclone Akvan,
Israeli tanks crossing Gaza's Yellow Line, Voyager 1 reaching one
light-day), a by-the-numbers strip and twelve one-line briefs — 22 stories
in one 1024×1024 picture.

Every story was verified against reports published on 19 November 2026
(BBC, NYT, Reuters, AP, NDTV, The Hindu). Nothing is invented: where a
story's outcome was still pending at build time, the wording states only
what was reported.

## Files

- `entry.png` — the image (1024×1024, ~140 KB)
- `draw.py` — the original generator that draws it (run `python3 draw.py`
  to rebuild byte-identically)
- `main.py` — the entrypoint: copies `entry.png` to `/output/entry.png`
  (standard library only, deterministic)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
