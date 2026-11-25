"""Sum up 24 November 2026 world news in one image.

Deterministic, no network: draws a 1024x1024 newspaper front page
with Pillow from the news facts hard-coded below (all checked against
Reuters / AP / SVPN archive on 2026-11-24) and writes /output/entry.png.
Running it twice produces byte-identical output.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"
LOCAL = "entry.png"  # repo copy, committed alongside main.py

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width (width is in pixels)."""
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width or not line:
                line = trial
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def draw_wrapped(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), (250, 247, 238))  # newsprint
    d = ImageDraw.Draw(img)
    ink = (18, 18, 18)
    red = (178, 34, 34)
    grey = (90, 90, 90)
    teal = (0, 90, 90)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=(18, 18, 18))
    d.text((512, 18), "THE WORLD IN ONE PAGE", font=font(SANS_B, 30),
           fill=(250, 247, 238), anchor="ma")
    d.text((512, 58), "TUESDAY  24  NOVEMBER  2026", font=font(SANS, 30),
           fill=(220, 200, 120), anchor="ma")
    d.text((512, 94), "THE DAY'S WORLD NEWS  •  ONE IMAGE",
           font=font(SANS, 16), fill=(200, 200, 200), anchor="ma")

    # Headline story
    y = 140
    d.text((48, y), "THE COMEBACK", font=font(SANS_B, 26), fill=red)
    y += 38
    y = draw_wrapped(d, 48, y,
                     "Nvidia brings back\nJensen Huang as CEO",
                     font(SERIF, 64), ink, 928, 66)
    y += 8
    y = draw_wrapped(
        d, 48, y,
        "Eleven days after resigning, the co-founder is reinstated "
        "unanimously by the board. Shares soar 31% and lift the Nasdaq "
        "6% as investors cheer the end of the leadership crisis.",
        font(SERIF_R, 26), ink, 928, 33)
    y += 10
    d.line([48, y, 976, y], fill=ink, width=3)
    y += 16
    # Market strip
    d.rectangle([48, y, 976, y + 58], fill=(18, 18, 18))
    d.text((512, y + 12), "NVIDIA +31%   •   NASDAQ +6%   •   S&P 500 +4%",
           font=font(SANS_B, 26), fill=(220, 200, 120), anchor="ma")
    y += 78

    # Secondary stories: 2 x 2 grid
    stories = [
        ("WAR IN UKRAINE",
         "Russian war deaths near 700,000",
         "Leaked data suggest the toll. Ukraine reports fresh "
         "strikes on Kyiv."),
        ("CLIMATE — COP31",
         "COP31 talks stall over fossil fuels",
         "Countries in Antalya stay divided on fossil-fuel "
         "policy and finance."),
        ("INDONESIA",
         "Factory fire: rescue search goes on",
         "A major fire leaves workers dead and missing "
         "in Indonesia."),
        ("EUROPE & THE WORLD",
         "ECB chief hunt opens",
         "Lagarde resigns. Iran warns the US over a naval "
         "blockade; Lisbon marches over living costs."),
    ]
    col_w, row_h = 452, 180
    for i, (kicker, head, body) in enumerate(stories):
        x = 48 + (i % 2) * 476
        yy = y + (i // 2) * (row_h + 12)
        d.rectangle([x, yy, x + col_w, yy + row_h], outline=ink, width=2)
        d.text((x + 16, yy + 12), kicker, font=font(SANS_B, 19), fill=teal)
        yy2 = draw_wrapped(d, x + 16, yy + 42, head, font(SERIF, 24),
                           ink, col_w - 32, 29)
        draw_wrapped(d, x + 16, yy2 + 6, body, font(SERIF_R, 18),
                     grey, col_w - 32, 23)

    # Footer (grid bottom is y + 2*row_h + 14)
    fy = y + 2 * (row_h + 12) + 10
    d.line([48, fy, 976, fy], fill=ink, width=2)
    d.text((512, fy + 12),
           "Sources: Reuters, AP, Kyiv Independent, SVPN archive — 24 Nov 2026",
           font=font(SANS, 16), fill=grey, anchor="ma")
    d.text((512, fy + 36),
           "Nvidia reinstatement announced Mon 23 Nov; markets reacted Mon 23–Tue 24 Nov.",
           font=font(SANS, 15), fill=grey, anchor="ma")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    img.save(LOCAL, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
