# Renders entry.png: a one-page newspaper summary of the world news of
# Wednesday 18 November 2026. Run: python3 src/render.py
# Output: entry.png at the repository root, 1024x1024, under 1 MiB.
# Headlines were researched from live news sources on 18 Nov 2026
# (AA, Reuters, AP, Outlook India, Daily Mirror): every story below
# happened or was first reported on 18 November 2026.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (18, 18, 18)
GREY = (90, 90, 90)
NAVY = (15, 42, 74)
RED = (163, 22, 33)
LEAD_BG = (234, 240, 246)
RULE = (180, 180, 175)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
serif_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", s)
serif = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", s)
sans_b = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", s)
sans = lambda s: ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels."""
    c = (70, 110, 160)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=4)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=c, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=c, width=3)
    draw.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 0, 180, fill=c, width=3)
    draw.arc([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 180, 360, fill=c, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # ---- Masthead ----
    d.text((W // 2, 44), "THE DAY IN ONE IMAGE", font=sans_b(21),
           fill=RED, anchor="ma")
    d.text((W // 2, 78), "WEDNESDAY, 18 NOVEMBER 2026", font=serif_b(44),
           fill=INK, anchor="ma")
    d.line([60, 140, W - 60, 140], fill=INK, width=3)
    d.line([60, 147, W - 60, 147], fill=INK, width=1)

    # ---- Lead story ----
    d.rectangle([40, 164, W - 40, 372], fill=LEAD_BG, outline=RULE, width=1)
    d.text((64, 184), "APEC  |  SHENZHEN", font=sans_b(19), fill=RED)
    d.text((64, 214), "XI AND PUTIN MEET BEFORE", font=serif_b(36), fill=INK)
    d.text((64, 258), "HISTORIC TRUMP TALKS", font=serif_b(36), fill=INK)
    lead = ("The Chinese and Russian leaders met in Shenzhen, a day before "
            "the first-ever three-way summit with Donald Trump.")
    y = 306
    for line in wrap(d, lead, sans(20), 640):
        d.text((64, y), line, font=sans(20), fill=(40, 40, 40))
        y += 26
    draw_globe(d, 890, 268, 62)

    # ---- Four stories, 2x2 grid ----
    stories = [
        ("MIDDLE EAST", (180, 35, 24),
         "Iran drones hit US base in Kuwait",
         "Tehran says its drones struck US platforms at Ali Al Salem air "
         "base; Bahrain and Gulf states report intercepting attacks."),
        ("UNITED STATES", (29, 78, 216),
         "Peltola flips Alaska Senate seat",
         "Democrat Mary Peltola beat Dan Sullivan; Democrats are projected "
         "to hold a 56-44 majority in the incoming Senate."),
        ("ASIA-PACIFIC", (15, 118, 110),
         "Quad leaders meet in Manila",
         "First leaders' meeting in over two years; the US and the "
         "Philippines also signed a trade and defence deal."),
        ("BRITAIN  |  GAZA", (109, 40, 217),
         "UK sanctions settlement firms",
         "Eight firms hit over West Bank building; Israel opened a new "
         "operation in three areas of central Gaza."),
    ]
    gx, gy, cw, ch, gap = 40, 392, 464, 196, 16
    for i, (tag, colour, head, body) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=(255, 255, 255),
                    outline=RULE, width=1)
        d.rectangle([x, yy, x + cw, yy + 6], fill=colour)
        d.text((x + 18, yy + 20), tag, font=sans_b(17), fill=colour)
        hy = yy + 48
        for line in wrap(d, head, serif_b(25), cw - 36):
            d.text((x + 18, hy), line, font=serif_b(25), fill=INK)
            hy += 32
        by = hy + 6
        for line in wrap(d, body, sans(18), cw - 36):
            d.text((x + 18, by), line, font=sans(18), fill=(50, 50, 50))
            by += 24

    # ---- Also today ----
    d.rectangle([40, 816, W - 40, 948], fill=NAVY)
    d.text((64, 832), "ALSO TODAY", font=sans_b(20), fill=(255, 205, 60))
    also = [
        "GTA VI launches at midnight, 13 years on",
        "Nvidia doubles revenue; Huang stays out",
        "Cyclone Akvan nears India's Odisha coast",
        "Gold at a one-year low; PNG quake, M6",
    ]
    for i, item in enumerate(also):
        x = 64 + (i % 2) * 470
        y = 866 + (i // 2) * 36
        d.ellipse([x, y + 7, x + 8, y + 15], fill=(255, 205, 60))
        d.text((x + 18, y), item, font=sans(18), fill=(240, 240, 240))

    # ---- Footer ----
    d.text((W // 2, 962), "Headlines as reported on 18 November 2026  |  "
           "Sources: AA, Reuters, AP", font=sans(15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
