#!/usr/bin/env python3
"""16x16 textures for Warbucks Core. Needs Pillow (use a venv). Run: python3 mod/tools/textures.py"""
import pathlib
from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/main/resources/assets/warbuckscore/textures"
STEEL, STEEL_D, STEEL_L = (120, 128, 140, 255), (70, 76, 88, 255), (170, 178, 190, 255)
CYAN, GOLD = (79, 209, 197, 255), (242, 181, 68, 255)


def img():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))


def spectrometer():
    im = img(); d = ImageDraw.Draw(im)
    d.rectangle([3, 1, 12, 14], fill=STEEL_D)            # body
    d.rectangle([4, 2, 11, 13], fill=STEEL)
    d.rectangle([5, 3, 10, 7], fill=(20, 24, 32, 255))   # screen
    for x, c in zip(range(5, 11), [(230, 60, 60), (240, 150, 50), (240, 230, 70), (80, 210, 90), (70, 140, 240), (150, 80, 220)]):
        d.line([x, 4, x, 6], fill=c + (255,))            # emission spectrum bands
    d.point([(7, 5)], fill=(255, 255, 255, 255))
    d.rectangle([5, 9, 6, 10], fill=GOLD)                # buttons
    d.rectangle([9, 9, 10, 10], fill=CYAN)
    d.line([4, 12, 11, 12], fill=STEEL_L)
    d.line([7, 0, 8, 0], fill=STEEL_L)                   # sensor tip
    return im


def capsule():
    im = img(); d = ImageDraw.Draw(im)
    d.rectangle([6, 1, 9, 2], fill=(150, 100, 60, 255))  # cork
    d.rectangle([5, 3, 10, 14], fill=(200, 230, 240, 120))  # glass
    d.rectangle([6, 8, 9, 13], fill=(90, 180, 80, 230))  # soil + green
    d.rectangle([6, 12, 9, 13], fill=(120, 85, 50, 240))
    d.line([5, 3, 5, 14], fill=(230, 245, 255, 200)); d.line([10, 3, 10, 14], fill=(140, 170, 190, 200))
    d.line([5, 14, 10, 14], fill=(140, 170, 190, 220))
    d.point([(6, 4), (6, 5)], fill=(255, 255, 255, 230))
    return im


def frame(core):
    im = Image.new("RGBA", (16, 16), STEEL_D); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, 14, 14], fill=STEEL)
    d.rectangle([1, 1, 14, 1], fill=STEEL_L); d.rectangle([1, 1, 1, 14], fill=STEEL_L)
    core(d)
    for p in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        d.point([p], fill=GOLD)                           # rivets
    return im


def top(d):
    d.ellipse([3, 3, 12, 12], fill=(30, 60, 40, 255))
    d.ellipse([4, 4, 11, 11], fill=(70, 170, 80, 255))
    d.ellipse([6, 6, 9, 9], fill=(170, 255, 170, 255))   # glowing core
    d.point([(7, 7)], fill=(255, 255, 255, 255))


def side(d):
    d.rectangle([3, 3, 12, 12], fill=(25, 30, 36, 255))
    d.rectangle([4, 9, 11, 12], fill=(110, 80, 50, 255))  # soil
    d.rectangle([4, 7, 11, 8], fill=(80, 170, 70, 255))   # grass
    d.line([5, 4, 5, 6], fill=(60, 140, 60, 255)); d.line([9, 5, 9, 6], fill=(60, 140, 60, 255))
    d.point([(5, 3), (8, 4), (9, 4), (10, 5)], fill=(90, 200, 90, 255))
    d.line([3, 5, 12, 5], fill=CYAN[:3] + (90,))         # scan line


def bottom(d):
    d.rectangle([4, 4, 11, 11], fill=STEEL_D)
    d.rectangle([6, 6, 9, 9], fill=CYAN)


def main():
    (OUT / "item").mkdir(parents=True, exist_ok=True); (OUT / "block").mkdir(parents=True, exist_ok=True)
    spectrometer().save(OUT / "item/spectrometer.png")
    capsule().save(OUT / "item/biome_capsule.png")
    frame(top).save(OUT / "block/terraformer_top.png")
    frame(side).save(OUT / "block/terraformer_side.png")
    frame(bottom).save(OUT / "block/terraformer_bottom.png")
    print("textures written to", OUT)


if __name__ == "__main__":
    main()
