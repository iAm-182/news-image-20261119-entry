#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a dense front page summing up
Thursday 19 November 2026. Ten illustrated lead stories, a by-the-numbers
strip and twelve one-line briefs -- 22 stories in one 1024x1024 picture.

All artwork is drawn with PIL primitives (flags, charts, icons); no external
images, no copied text. Stories were verified against BBC, NYT, Reuters, AP,
NDTV and The Hindu reports published on 19 November 2026.
Output: entry.png (1024x1024, well under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (24, 24, 24)
RED = (178, 32, 44)
PAPER = (248, 244, 236)
PANEL = (255, 255, 255)
GREY = (96, 92, 84)
RULE = (205, 197, 180)
NAVY = (24, 48, 84)
GOLD = (176, 132, 30)
BLUE = (31, 78, 121)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, color, max_w, leading):
    """Draw wrapped text; return y after the last line."""
    for ln in wrap(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def fit_font(d, text, path, max_w, start):
    """Largest font size (<= start) that fits text in max_w."""
    size = start
    while size > 10 and d.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


# ---------------------------------------------------------------- icons ----
# Each icon draws into the box (x, y, w, h) and returns nothing.

def icon_flags(d, x, y, w, h):
    """US / China / Russia flags side by side."""
    pw = w // 3
    # United States: stripes + canton
    d.rectangle([x, y, x + pw - 4, y + h], fill=(255, 255, 255),
                outline=INK, width=2)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x + 2, y + 2 + i * (h - 4) // 7,
                         x + pw - 6, y + 2 + (i + 1) * (h - 4) // 7],
                        fill=(178, 34, 52))
    d.rectangle([x + 2, y + 2, x + pw // 2, y + h // 2], fill=(30, 58, 120))
    for sx in (x + 8, x + 20, x + 32):
        for sy in (y + 8, y + 20):
            d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    # China: red field, yellow stars
    cx = x + pw
    d.rectangle([cx, y, cx + pw - 4, y + h], fill=(222, 41, 16),
                outline=INK, width=2)
    d.ellipse([cx + 8, y + 8, cx + 20, y + 20], fill=(255, 222, 0))
    for sx, sy in ((cx + 26, y + 8), (cx + 30, y + 18), (cx + 26, y + 28),
                   (cx + 16, y + 32)):
        d.ellipse([sx, sy, sx + 5, sy + 5], fill=(255, 222, 0))
    # Russia: white / blue / red horizontal bands
    rx = x + 2 * pw
    bands = [(255, 255, 255), (0, 57, 166), (213, 0, 50)]
    for i, col in enumerate(bands):
        d.rectangle([rx, y + i * h // 3, rx + pw - 4,
                     y + (i + 1) * h // 3], fill=col,
                    outline=INK, width=2)


def icon_chart(d, x, y, w, h):
    """Rising bars and an arrow: a record IPO."""
    d.line([x + 4, y + h - 6, x + w - 4, y + h - 6], fill=INK, width=3)
    d.line([x + 4, y + h - 6, x + 4, y + 6], fill=INK, width=3)
    bars = [(0.55, NAVY), (0.72, BLUE), (0.92, (34, 139, 34))]
    bw = (w - 16) // 3
    for i, (frac, col) in enumerate(bars):
        bx = x + 8 + i * bw
        bh = int((h - 16) * frac)
        d.rectangle([bx, y + h - 8 - bh, bx + bw - 4, y + h - 8], fill=col)
    d.line([x + 8, y + h - 22, x + w // 2, y + h - 34,
            x + w - 6, y + 8], fill=RED, width=4)
    d.polygon([(x + w - 6, y + 8), (x + w - 18, y + 6), (x + w - 8, y + 18)],
              fill=RED)


def icon_controller(d, x, y, w, h):
    """A game controller with a VI badge."""
    d.rounded_rectangle([x + 2, y + 8, x + w - 2, y + h - 14], radius=12,
                        fill=(40, 40, 48), outline=INK, width=2)
    d.ellipse([x + 10, y + h - 26, x + 26, y + h - 10], fill=(60, 60, 70),
              outline=(120, 120, 130), width=2)
    d.ellipse([x + w - 26, y + h - 26, x + w - 10, y + h - 10],
              fill=(60, 60, 70), outline=(120, 120, 130), width=2)
    cx, cy = x + 18, y + 22
    d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=(220, 220, 220))
    d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=(220, 220, 220))
    for bx, by, col in ((x + w - 22, y + 16, (255, 80, 80)),
                        (x + w - 12, y + 24, (80, 200, 120)),
                        (x + w - 32, y + 24, (90, 140, 255)),
                        (x + w - 22, y + 32, (255, 210, 60))):
        d.ellipse([bx, by, bx + 8, by + 8], fill=col)
    d.text((x + w // 2, y + h - 12), "VI", font=font(SANS_B, 13),
           fill=(255, 210, 60), anchor="ma")


def icon_capitol(d, x, y, w, h):
    """The US Capitol dome."""
    d.polygon([(x + w // 2, y + 2), (x + 6, y + h // 2),
               (x + w - 6, y + h // 2)], fill=(230, 228, 222),
              outline=INK, width=2)
    d.rectangle([x + w // 2 - 2, y - 2, x + w // 2 + 2, y + 6], fill=INK)
    d.rectangle([x + 4, y + h // 2, x + w - 4, y + h // 2 + 6],
                fill=(200, 196, 188), outline=INK, width=2)
    for i in range(5):
        cx = x + 10 + i * (w - 20) // 4
        d.line([cx, y + h // 2 + 8, cx, y + h - 8], fill=INK, width=3)
    d.rectangle([x + 2, y + h - 8, x + w - 2, y + h - 2], fill=NAVY)


def icon_bridge(d, x, y, w, h):
    """A bridge deck over waves."""
    d.rectangle([x + 4, y + 8, x + 10, y + h - 18], fill=INK)
    d.rectangle([x + w - 10, y + 8, x + w - 4, y + h - 18], fill=INK)
    d.line([x + 2, y + h // 2, x + w - 2, y + h // 2], fill=RED, width=5)
    for i in range(5):
        cx = x + 10 + i * (w - 20) // 4
        d.line([cx, y + h // 2, cx, y + 8], fill=INK, width=2)
    for i, wy in enumerate((y + h - 12, y + h - 6)):
        for j in range(4):
            sx = x + 4 + j * (w - 8) // 4 + (i * 8)
            d.arc([sx, wy, sx + 16, wy + 8], 0, 180, fill=BLUE, width=3)


def icon_painting(d, x, y, w, h):
    """A framed Van Gogh-style canvas: sun, swirls, field."""
    d.rectangle([x, y, x + w, y + h], fill=GOLD, outline=INK, width=2)
    d.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], fill=(70, 110, 180))
    d.ellipse([x + w - 26, y + 12, x + w - 8, y + 30], fill=(255, 214, 64))
    d.arc([x + 8, y + 10, x + w - 16, y + 34], 200, 340, fill=(255, 255, 255),
          width=3)
    d.arc([x + 12, y + 22, x + w - 8, y + 44], 180, 360, fill=(255, 255, 255),
          width=3)
    d.rectangle([x + 6, y + h - 18, x + w - 6, y + h - 6],
                fill=(90, 140, 60))


def icon_scales(d, x, y, w, h):
    """Scales of justice."""
    cx = x + w // 2
    d.line([cx, y + 4, cx, y + h - 8], fill=INK, width=3)
    d.line([x + 6, y + 12, x + w - 6, y + 12], fill=INK, width=3)
    d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=GOLD, outline=INK)
    for side in (-1, 1):
        px = cx + side * (w // 2 - 10)
        d.line([px, y + 12, px, y + 26], fill=INK, width=2)
        d.chord([px - 14, y + 24, px + 14, y + 40], 0, 180, fill=GOLD,
                outline=INK, width=2)
    d.rectangle([x + 6, y + h - 6, x + w - 6, y + h - 2], fill=NAVY)


def icon_cyclone(d, x, y, w, h):
    """A spiral storm with rain."""
    cx, cy = x + w // 2 - 2, y + h // 2 - 4
    for r in (6, 12, 18, 24):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=BLUE, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    for i in range(3):
        rx = x + 8 + i * 14
        d.line([rx, y + h - 10, rx - 4, y + h - 2], fill=BLUE, width=3)


def icon_tank(d, x, y, w, h):
    """A tank crossing a dashed line."""
    d.line([x + 2, y + h - 6, x + w - 2, y + h - 6], fill=INK, width=2)
    for i in range(5):
        sx = x + 4 + i * (w - 8) // 5
        d.line([sx, y + h - 6, sx + 8, y + h - 6], fill=(255, 200, 0),
               width=3)
    d.rectangle([x + 8, y + h - 30, x + w - 8, y + h - 14], fill=(90, 96, 80),
                outline=INK, width=2)
    d.rectangle([x + w // 2 - 8, y + h - 44, x + w // 2 + 14, y + h - 30],
                fill=(90, 96, 80), outline=INK, width=2)
    d.line([x + w // 2 + 14, y + h - 38, x + w - 2, y + h - 40], fill=INK,
           width=4)
    for i in range(3):
        wx = x + 14 + i * 16
        d.ellipse([wx, y + h - 14, wx + 10, y + h - 4], fill=INK)


def icon_voyager(d, x, y, w, h):
    """Voyager: gold dish, body, boom, stars."""
    for sx, sy in ((x + 6, y + 6), (x + w - 10, y + 10), (x + 10, y + h - 14),
                   (x + w - 14, y + h - 18), (x + w // 2, y + 4)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.polygon([(x + 4, y + h // 2), (x + w // 2 + 4, y + h // 2 - 16),
               (x + w // 2 + 4, y + h // 2 + 16)], fill=GOLD, outline=INK,
              width=2)
    d.rectangle([x + w // 2 + 4, y + h // 2 - 8, x + w // 2 + 20,
                 y + h // 2 + 8], fill=(200, 200, 200), outline=INK, width=2)
    d.line([x + w // 2 + 20, y + h // 2, x + w - 4, y + h // 2 - 10],
           fill=INK, width=2)
    d.arc([x + w - 18, y + h - 18, x + w - 2, y + h - 2], 270, 360,
          fill=GOLD, width=2)


# ------------------------------------------------------------------ page ----
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 28                      # side margin
CW = W - 2 * M              # content width

# ---- masthead ----
d.rectangle([0, 0, W, 8], fill=RED)
d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SANS_B, 24),
       fill=RED, anchor="ma")
date_f = fit_font(d, "THURSDAY 19 NOVEMBER 2026", SERIF_B, CW, 62)
d.text((512, 56), "THURSDAY 19 NOVEMBER 2026", font=date_f, fill=INK,
       anchor="ma")
d.text((512, 118), "ONE DAY  ·  EVERY STORY THAT MATTERED",
       font=font(SANS_B, 15), fill=GREY, anchor="ma")
d.line([M, 142, W - M, 142], fill=INK, width=3)
d.line([M, 147, W - M, 147], fill=INK, width=1)

# ---- lead story: Shenzhen summit ----
LY, LH = 158, 168
d.rectangle([M, LY, W - M, LY + LH], fill=PANEL, outline=RULE, width=1)
d.rectangle([M, LY, M + 34, LY + 34], fill=RED)
d.text((M + 17, LY + 17), "1", font=font(SANS_B, 20), fill=(255, 255, 255),
       anchor="mm")
d.text((M + 44, LY + 14), "SHENZHEN  ·  APEC SUMMIT", font=font(SANS_B, 15),
       fill=RED)
block(d, M + 44, LY + 36, "THREE LEADERS,", font(SERIF_B, 40), INK, 600, 44)
block(d, M + 44, LY + 80, "ONE TABLE", font(SERIF_B, 40), INK, 600, 44)
block(d, M + 44, LY + 126,
      "Trump, Xi and Putin shake hands in Shenzhen and meet for "
      "trilateral talks — the first time the three leaders have sat "
      "down together.", font(SANS, 17), (60, 58, 52), 600, 22)
icon_flags(d, W - M - 300, LY + 12, 288, 118)
d.text((W - M - 156, LY + 138), "USA  ·  CHINA  ·  RUSSIA",
       font=font(SANS_B, 13), fill=GREY, anchor="ma")

# ---- numbered leads 2-10: 3 columns x 3 rows ----
LEADS = [
    (2, "BUSINESS · NEW YORK", "THE BIGGEST IPO EVER",
     "Record $81.3bn raised at $83 a share; trading starts today.",
     icon_chart),
    (3, "CULTURE · GAMING", "VICE CITY OPENS",
     "Grand Theft Auto VI begins its global rollout after a 13-year "
     "wait.", icon_controller),
    (4, "POLITICS · WASHINGTON", "JEFFRIES TO MAKE HISTORY",
     "Democrats nominate Hakeem Jeffries as the first Black Speaker.",
     icon_capitol),
    (5, "WAR · UKRAINE", "BRIDGE HIT AGAIN",
     "A Russian official confirms a new attack on the Crimean "
     "Bridge.", icon_bridge),
    (6, "ART · NEW YORK", "VAN GOGH'S $190.4M RECORD",
     "Van Gogh's 'Chestnut Trees' sets an artist record at Sotheby's.",
     icon_painting),
    (7, "JUSTICE · THE HAGUE", "THE HAGUE DECIDES",
     "The world court rules on the Rohingya genocide case against "
     "Myanmar.", icon_scales),
    (8, "WEATHER · INDIA", "CYCLONE AKVAN NEARS INDIA",
     "Storm to cross the east coast between Machilipatnam and Puri.",
     icon_cyclone),
    (9, "WAR · GAZA", "TANKS CROSS THE YELLOW LINE",
     "Rare Israeli ground operation beyond Gaza's ceasefire line.",
     icon_tank),
    (10, "SPACE · NASA", "ONE LIGHT-DAY FROM HOME",
     "First human-made object a light-day from Earth.", icon_voyager),
]

GY = LY + LH + 14
CELL_W, CELL_H = 312, 112
GAP_X, GAP_Y = 16, 10
for i, (num, kicker, head, deck, icon) in enumerate(LEADS):
    col, row = i % 3, i // 3
    x = M + col * (CELL_W + GAP_X)
    y = GY + row * (CELL_H + GAP_Y)
    d.rectangle([x, y, x + CELL_W, y + CELL_H], fill=PANEL, outline=RULE,
                width=1)
    d.rectangle([x, y, x + 26, y + 26], fill=NAVY)
    d.text((x + 13, y + 13), str(num), font=font(SANS_B, 15),
           fill=(255, 255, 255), anchor="mm")
    d.text((x + 32, y + 6), kicker, font=font(SANS_B, 11), fill=RED)
    icon(d, x + 8, y + 34, 62, 62)
    hx = x + 80
    hy = block(d, hx, y + 28, head, font(SANS_B, 19), INK, CELL_W - 88, 22)
    block(d, hx, hy + 2, deck, font(SANS, 13), (60, 58, 52),
          CELL_W - 88, 15)

# ---- by the numbers ----
NY = GY + 3 * CELL_H + 2 * GAP_Y + 14
d.rectangle([M, NY, W - M, NY + 62], fill=NAVY)
NUMS = [
    ("$81.3bn", "biggest IPO ever"),
    ("$190.4m", "Van Gogh record"),
    ("\u20ac45bn", "EU loan for Kyiv"),
    ("1 light-day", "Voyager 1"),
    ("13 years", "wait for GTA VI"),
]
seg = CW // 5
for i, (big, small) in enumerate(NUMS):
    cx = M + seg * i + seg // 2
    d.text((cx, NY + 10), big, font=font(SANS_B, 24), fill=(255, 255, 255),
           anchor="ma")
    d.text((cx, NY + 38), small, font=font(SANS, 13), fill=(190, 200, 220),
           anchor="ma")
    if i:
        d.line([M + seg * i, NY + 8, M + seg * i, NY + 54],
               fill=(70, 95, 130), width=1)

# ---- in brief ----
BY = NY + 62 + 12
d.text((M, BY), "IN BRIEF", font=font(SANS_B, 16), fill=RED)
d.line([M + 92, BY + 8, W - M, BY + 8], fill=RULE, width=1)
BRIEFS = [
    "EU proposes a \u20ac45bn loan for Ukraine.",
    "US and Iran exchange fire again in the Gulf.",
    "US loses measles elimination status after 26 years.",
    "Waymo pulls all its driverless cars from US freeways.",
    "Nvidia stops H-series chip shipments to mainland China.",
    "Fed minutes: most officials expect more rate hikes.",
    "Haaland's late penalty sends Norway through.",
    "No. 8 Houston stuns No. 1 Florida in college basketball.",
    "Littler shocked by Wattimena at the Grand Slam of Darts.",
    "Eisenkot tapped to form Israel's next government.",
    "Four nations urge Israel to let aid reach flooded Gaza.",
    "IMF lifts Germany's growth forecast to 1.3%.",
]
bw = (CW - 24) // 2
by = BY + 26
for i, b in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    bx = M + col * (bw + 24)
    byy = by + row * 30
    d.text((bx, byy), "\u2022", font=font(SANS_B, 14), fill=RED)
    block(d, bx + 14, byy, b, font(SANS, 14), INK, bw - 14, 15)

# ---- footer ----
FY = by + 6 * 30 + 8
d.line([M, FY, W - M, FY], fill=INK, width=2)
d.text((512, FY + 8),
       "THE WORLD IN ONE DAY  —  THURSDAY 19 NOVEMBER 2026  ·  22 STORIES",
       font=font(SANS_B, 13), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
