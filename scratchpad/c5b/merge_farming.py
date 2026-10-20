"""Merge the food_and_farming mirror into tools/quests/farming.py."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests/farming.py"
s = p.read_text(encoding="utf-8")
new = (ROOT / "scratchpad/c5b/farming_new.txt").read_text(encoding="utf-8")

anchor = "# Any hopper botany pot (every material and colour) counts.\n"
if "FIELD, PASTURE" not in s:
    s = s.replace(anchor, "# ATM10 mirror (2026-10-20, user decision): ATM10's \"food_and_farming\" chapter, quest for quest where we have\n"
                  "# the mod (its item list, order and shape only; all text is ours). Our Farmer's Delight, Botany Pots and fertiliser\n"
                  "# quests stay as side quests.\n"
                  'FIELD, PASTURE, SEA = "The Field", "The Pasture", "The Sea"\n\n' + anchor)


def patch(key, old, new_):
    global s
    m = re.search(r'    Q\("' + key + r'".*?\]\),\n', s, re.S)
    assert m, key
    b = m.group(0)
    assert old in b, (key, old)
    s = s.replace(b, b.replace(old, new_, 1))


patch("fd_breed", '[item("minecraft:lead", 2), item("minecraft:wheat", 16)], "Animal Husbandry", deps=["f_knife"], xp=20,\n      optional=True, tokens=1, subtitle="Optional: breeding, explained by Just Enough Breeding"',
      '[item("minecraft:lead")], "Animal Husbandry", deps=[], xp=20, section=PASTURE, mirror="2E9C035EEE7E5C34",\n      subtitle="A lead, and the animals at the end of it"')
patch("fd_milk", 'deps=["fd_breed", "gs_bucket"], xp=15,\n      optional=True, tokens=1, subtitle="Optional: the cure',
      'deps=["fd_leather"], xp=15, section=PASTURE, mirror="73B8A70240E6070E",\n      subtitle="The cure')
patch("fd_sugar", '[item("minecraft:sugar", 16)], "Sugar", deps=["gs_opt_canes"], xp=15,\n      optional=True, tokens=1, subtitle="Optional: crystallised sucrose"',
      '[item("minecraft:sugar", 3)], "Sugar", deps=["fd_cane"], xp=15, section=FIELD, mirror="1D48298525EEADC9",\n      subtitle="Crystallised sucrose"')
patch("fd_baking", '[item("minecraft:cake"), item("minecraft:pumpkin_pie", 2)], "Bake Sale", deps=["fd_sugar", "fd_milk", "fd_barnyard"], xp=30,\n      optional=True, tokens=1, subtitle="Optional: a cake and two pies"',
      '[item("minecraft:cake")], "Bake Sale", deps=["fd_sugar", "fd_wheat"], xp=40, size=1.5, section=FIELD, mirror="0893EFCAC7031FEA",\n      subtitle="A whole cake"')
patch("fd_baking", '"&eWhat:&r a cake (placed and eaten a slice at a time) and pumpkin pie, the best vanilla snack per bite."',
      '"&6Wheat, sugar, milk and eggs from your own field and pasture. You remember feasts; this is a good start.&r",\n        "&eWhat:&r a cake, placed and eaten a slice at a time. It needs something from every part of this page."')
patch("fd_baking", '"&eHow:&r cake: 3 milk buckets, 2 sugar, an egg and 3 wheat (you keep the buckets). Pie: a pumpkin, sugar and an egg."',
      '"&eHow:&r 3 milk buckets, 2 sugar, an egg and 3 wheat (you keep the buckets)."')
patch("fd_flax", '[item("silentgear:flax_seeds", 4), item("silentgear:flax_string", 8)], "Flax", deps=["fd_crops"], xp=20,\n      optional=True, tokens=1, subtitle="Optional: string without spiders"',
      '[item("silentgear:flax_string", 3)], "Flax String", deps=["fd_flax_seeds"], xp=20, section=FIELD, mirror="04D0543FE2820F64",\n      subtitle="String without spiders"')
patch("fd_flax", '"&eHow:&r find flax seeds (check JEI for where they drop), grow them, and craft 2 flax fibre into a flax string."',
      '"&eHow:&r grow flax and craft its fibre into flax string (check JEI for the recipe)."')

if 'Q("fd_hub"' not in s:
    i = s.rindex("], links=[")
    s = s[:i] + new + s[i:]
if 'mirror="food_and_farming"' not in s:
    s = s.replace('("t6_haber", -1.5, 7.5)])', '("t6_haber", -1.5, 7.5)], mirror="food_and_farming")')
assert 'mirror="food_and_farming"' in s
p.write_text(s, encoding="utf-8", newline="\n")
print("done")
