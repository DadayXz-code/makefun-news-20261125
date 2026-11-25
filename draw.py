#!/usr/bin/env python3
"""Draw THE WORLD TODAY - Wednesday 25 November 2026.

A one-page newspaper front page summarising the world's news of
25 November 2026, drawn from scratch with Pillow. Deterministic:
no timestamps, no randomness, so repeated runs are byte-identical.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)          # newsprint cream
INK = (22, 22, 22)            # near-black
RED = (158, 27, 24)           # headline red
NAVY = (24, 48, 92)           # section navy
GREY = (96, 94, 88)           # muted grey
RULE = (180, 175, 162)        # hairline rule
BOX_BG = (255, 253, 247)      # story box paper
LEAD_BG = (24, 48, 92)        # lead banner navy

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_story(d, x, y, w, title, body, max_body_lines=2):
    """One short story: bold title (1 line, shrunk if needed) + body."""
    tf = font(SANS_B, 14)
    bf = font(SANS, 12)
    # Title: keep to one line by trimming with an ellipsis if needed.
    t = title
    while d.textlength(t, font=tf) > w and len(t) > 12:
        t = t[:-4].rstrip() + "..."
    d.text((x, y), t, font=tf, fill=INK)
    y += 17
    lines = wrap(d, body, bf, w)[:max_body_lines]
    for ln in lines:
        d.text((x, y), ln, font=bf, fill=(52, 50, 46))
        y += 14
    return y + 3


def draw_box(d, x, y, w, h, region, stories, accent=NAVY):
    """A region box: coloured header bar + short stories."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=4,
                        fill=BOX_BG, outline=RULE, width=1)
    d.rounded_rectangle([x, y, x + w, y + 24], radius=4, fill=accent)
    d.rectangle([x, y + 12, x + w, y + 24], fill=accent)
    hf = font(SANS_B, 13)
    d.text((x + 8, y + 5), region, font=hf, fill=(255, 255, 255))
    cy = y + 30
    for title, body in stories:
        cy = draw_story(d, x + 8, cy, w - 16, title, body)
    return cy


def draw_globe(d, cx, cy, r):
    """Simple line-art globe: circle, meridians, parallels, shield."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255),
              width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          180, 360, fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          0, 180, fill=(255, 255, 255), width=2)
    # Shield with an exclamation mark, lower right of the globe.
    sx, sy = cx + r * 0.35, cy + r * 0.30
    sw, sh = 34, 40
    d.polygon([(sx, sy), (sx + sw, sy), (sx + sw, sy + sh - 12),
               (sx + sw / 2, sy + sh), (sx, sy + sh - 12)],
              fill=RED, outline=(255, 255, 255), width=2)
    sf = font(SANS_B, 26)
    d.text((sx + sw / 2 - 4, sy + 3), "!", font=sf, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.text((16, 8), "THE WORLD TODAY", font=font(SERIF_B, 56), fill=INK)
    d.text((16, 72), "WEDNESDAY 25 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=RED)
    d.text((700, 76), "ONE DAY  ·  ONE PAGE  ·  THE WORLD",
           font=font(SANS_B, 12), fill=GREY)
    d.line([16, 96, 1008, 96], fill=INK, width=3)
    d.line([16, 100, 1008, 100], fill=INK, width=1)

    # ---- Lead story ----------------------------------------------
    lx, ly, lw, lh = 16, 106, 992, 140
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=6, fill=LEAD_BG)
    d.text((lx + 16, ly + 10), "LEAD STORY  •  CYBERSECURITY  •  WASHINGTON",
           font=font(SANS_B, 12), fill=(255, 214, 90))
    head = "CIA and spy chief's office hit by cyber breach"
    d.text((lx + 16, ly + 32), head, font=font(SERIF_B, 30),
           fill=(255, 255, 255))
    dek = ("CNN reports the CIA and the Office of the Director of National "
           "Intelligence were hit by a cyberattack affecting some "
           "classified information — the latest breach to rock US "
           "government systems, sources say.")
    y = ly + 68
    for ln in wrap(d, dek, font(SANS, 15), 700):
        d.text((lx + 16, y), ln, font=font(SANS, 15), fill=(226, 232, 240))
        y += 19
    draw_globe(d, lx + lw - 118, ly + 70, 52)
    d.text((lx + lw - 236, ly + 122), "A breach at the heart of US intelligence",
           font=font(SANS, 11), fill=(180, 196, 216))

    # ---- Timeline strip ------------------------------------------
    ty = 254
    d.text((16, ty), "THE DAY IN TIME — first reported (IST)",
           font=font(SANS_B, 12), fill=NAVY)
    d.line([16, ty + 20, 1008, ty + 20], fill=RULE, width=2)
    ticks = [
        ("00:50", "Sooryavanshi's 204"),
        ("01:31", "Nvidia's Huang"),
        ("02:03", "Gukesh holds Sindarov"),
        ("03:46", "BJP–Akali alliance"),
        ("04:41", "BBC: sixes record"),
        ("04:57", "Huawei guilty verdict"),
    ]
    tx = 16
    step = 165
    for i, (t, label) in enumerate(ticks):
        x = tx + i * step
        d.ellipse([x, ty + 15, x + 10, ty + 25], fill=RED)
        d.text((x - 2, ty + 28), t, font=font(SANS_B, 11), fill=INK)
        d.text((x - 2, ty + 42), label, font=font(SANS, 10), fill=GREY)

    # ---- Region grid ----------------------------------------------
    gx, gy = 16, 314
    cw, ch, gap = 320, 224, 12

    north_america = [
        ("Huawei found guilty in US trial",
         "A New York jury convicts Huawei on 10 of 12 counts, including "
         "stealing trade secrets."),
        ("Giuliani gets Medal of Freedom",
         "President Trump awards former New York mayor Rudy Giuliani the "
         "Presidential Medal of Freedom."),
        ("Turkeys spared for Thanksgiving",
         "Trump pardons turkeys Freedom and Feathers in the annual "
         "Thanksgiving ceremony."),
        ("Fort Hood gunman seeks stay",
         "Nidal Hasan, who killed 13 at Fort Hood in 2009, asks a court to "
         "stay his execution."),
    ]
    europe = [
        ("Kyiv confirms Gulf of Finland strike",
         "Zelenskiy says Ukraine was behind Saturday's drone strike on a "
         "Russian cargo ship."),
        ("NATO jets for Poland",
         "NATO plans to deploy early-warning aircraft in Poland after "
         "missiles landed there."),
        ("Sarkozy case goes to trial",
         "French officials order ex-president Nicolas Sarkozy and his wife "
         "Carla Bruni to trial."),
        ("Sweden sets PM vote for 30 Nov",
         "Parliament will vote on Ulf Kristersson as prime minister on "
         "30 November."),
    ]
    middle_east = [
        ("Houthis hit Riyadh's tallest tower",
         "A Houthi drone strike on Riyadh's tallest tower wounds 11 "
         "people, civil defence says."),
        ("Houthis close in on Aden",
         "Yemen's Houthis push to within 60 km of Aden, but government "
         "forces say it will hold."),
        ("Tankers hit in Strait of Hormuz",
         "Iran's Revolutionary Guard Navy says three oil tankers were hit "
         "by naval mines."),
        ("UN warns over Gaza",
         "The UN highlights continuing humanitarian difficulties in Gaza "
         "for civilians."),
    ]
    asia = [
        ("BJP and Akali Dal reunite",
         "Six years after splitting, the BJP and Shiromani Akali Dal "
         "announce a 2027 alliance."),
        ("Modi meets Germany's Merz",
         "PM Modi holds talks with German Chancellor Friedrich Merz on the "
         "strategic partnership."),
        ("Nepal quake: magnitude 5.6",
         "A 5.6-magnitude earthquake strikes Nepal's Koshi Province near "
         "the Chinese border."),
        ("Sensex drops 1,484 points",
         "India's Sensex falls 1,484 points and the Nifty slips below "
         "25,400."),
    ]
    africa = [
        ("WHO flees Ebola hospital in DRC",
         "WHO staff are evacuated from a hospital in Akwe, Ituri, after "
         "three days of fighting."),
        ("COP31 ends without a pact",
         "The UN climate summit in Antalya closes with no climate pact."),
        ("ECOWAS plans single currency",
         "West African ministers review preparations for a single ECOWAS "
         "currency in 2027."),
        ("Libya's frozen conflict stirs",
         "Ukraine's sinking of a Russian vessel in a Libyan port stirs "
         "Libya's frozen conflict."),
    ]
    sport = [
        ("Sooryavanshi, 15, smashes 204",
         "Vaibhav Sooryavanshi hits the fastest List A double hundred — "
         "204 off 53 balls."),
        ("England level T20 series",
         "England beat Australia by eight wickets in the second T20I, "
         "chasing 185."),
        ("Gukesh holds Sindarov",
         "World champion Gukesh holds Javokhir Sindarov in Game 1 of the "
         "World Championship."),
        ("New Zealand hold India to a draw",
         "Determined New Zealand batting holds India to a draw in the "
         "first Test."),
    ]
    science = [
        ("A star system that 'should not exist'",
         "Astronomers find a cosmic mystery just 28 light-years away."),
        ("One asteroid eclipses another",
         "A spacecraft beams home a rare sight: one asteroid eclipsing "
         "another."),
        ("Nvidia's Huang 'violated code of conduct'",
         "Reuters reports Nvidia's Jensen Huang told staff he violated "
         "the code of conduct."),
        ("Dell rides AI server boom",
         "Dell lifts its annual forecasts after a record quarter driven "
         "by AI server demand."),
        ("India's space economy to hit $45bn",
         "India's space economy is expected to grow to $40–45 billion, "
         "a minister says."),
        ("Great Barrier Reef corals 'resurrected'",
         "A genetic analysis revives 12 Acropora coral species on the "
         "Great Barrier Reef."),
    ]

    draw_box(d, gx, gy, cw, ch, "NORTH AMERICA", north_america, NAVY)
    draw_box(d, gx + cw + gap, gy, cw, ch, "EUROPE", europe, RED)
    draw_box(d, gx + 2 * (cw + gap), gy, cw, ch, "MIDDLE EAST", middle_east,
             (122, 84, 20))
    draw_box(d, gx, gy + ch + gap, cw, ch, "ASIA", asia, (0, 110, 80))
    draw_box(d, gx + cw + gap, gy + ch + gap, cw, ch, "AFRICA", africa,
             (150, 84, 0))
    draw_box(d, gx + 2 * (cw + gap), gy + ch + gap, cw, ch, "SPORT", sport,
             (20, 90, 60))

    # Wide science & tech box, two columns.
    wy = gy + 2 * (ch + gap)
    ww = 3 * cw + 2 * gap
    wh = 190
    d.rounded_rectangle([gx, wy, gx + ww, wy + wh], radius=4,
                        fill=BOX_BG, outline=RULE, width=1)
    d.rounded_rectangle([gx, wy, gx + ww, wy + 24], radius=4, fill=NAVY)
    d.rectangle([gx, wy + 12, gx + ww, wy + 24], fill=NAVY)
    d.text((gx + 8, wy + 5), "SCIENCE, TECH & MARKETS",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    half = (ww - 16) // 2
    cy = wy + 30
    for title, body in science[:3]:
        cy = draw_story(d, gx + 8, cy, half - 8, title, body)
    cy = wy + 30
    for title, body in science[3:]:
        cy = draw_story(d, gx + 8 + half, cy, half - 8, title, body)

    # ---- Footer ----------------------------------------------------
    fy = 1000
    d.line([16, fy - 8, 1008, fy - 8], fill=INK, width=2)
    d.text((16, fy), "THE WORLD TODAY  •  WEDNESDAY 25 NOVEMBER 2026  •  "
           "Sources: Reuters, BBC, CNN, AP, AFP, The Hindu, Times of India",
           font=font(SANS, 11), fill=GREY)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
