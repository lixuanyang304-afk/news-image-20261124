"""Entry point for make.fun news-image-20261124.

Writes one image to /output/entry.png. The image itself is built
offline by generate.py (Pillow, local fonts only) and committed as
entry.png in this repository; this program is stdlib-only and copies
it, which the bounty description explicitly allows ("the simplest
program copies an image the repository holds"). No network, no
randomness: two runs write byte-identical output.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)


if __name__ == "__main__":
    main()
