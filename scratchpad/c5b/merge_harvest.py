"""Merge the basic_armor mirror into tools/quests/harvest.py."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests/harvest.py"
s = p.read_text(encoding="utf-8")
head = (ROOT / "scratchpad/c5b/harvest_head.txt").read_text(encoding="utf-8")
new = (ROOT / "scratchpad/c5b/harvest_new.txt").read_text(encoding="utf-8")
new = new.replace('"1004D61425172324F"[1:]', '"004D61425172324F"')
new = new.replace('"5E6D7C1D7957DD4D"[:0] + "5E6D7C1D7957DD4D"', '"5E6D7C1D7957DD4D"')
new = new.replace('"Allthemodium Ingot", "allthemodium is fictional; the Allthemodium page covers where it comes from.", "5E6D7C1D7957DD4D"',
                  '"Allthemodium Ingot", "allthemodium is fictional; the Allthemodium page covers where it comes from.", "5E7CCDE9229A646A"')
head = head.replace('any of the Trim Materials on this page.', 'a vanilla ingot or gem, as listed under Trim Materials.')
head = head.replace('"a trim colour"', '"for the collection"')

old_head = s[s.index("from questlib import"):s.index("CHAPTER = Chapter(")]
s = s.replace(old_head, head)
s = s.replace('CHAPTER = Chapter("harvest", "Tools, Armour and Harvest Tiers", "minecraft:diamond_pickaxe",\n'
              '        ["Which pickaxe mines what, and why harder is not the same as tougher."]',
              'CHAPTER = Chapter("harvest", "Armour and Harvest Tiers", "minecraft:diamond_chestplate",\n'
              '        ["Every armour set in the pack, trims and their materials, and which pickaxe mines what."]')
assert '"Armour and Harvest Tiers"' in s


def patch(key, old, new_):
    global s
    m = re.search(r'    Q\("' + key + r'".*?\]\),\n', s, re.S)
    assert m, key
    b = m.group(0)
    assert old in b, (key, old)
    s = s.replace(b, b.replace(old, new_, 1))


patch("hv_leather_set", '[item(MC + "leather_helmet"), item(MC + "leather_leggings")], "A Full Leather Set"',
      'vset("leather"), "A Full Leather Set"')
patch("hv_leather_set", 'deps=["gs_leather"], xp=15,', 'deps=["gs_leather"], xp=15, size=1.5, section=SETS, mirror="28408BFAA54E4FC6",')
patch("hv_leather_set", 'subtitle="Optional: cap and trousers to match"', 'subtitle="Optional: all four pieces, dyed if you like"')
patch("hv_leather_set", '"&eWhat:&r the helmet and leggings that finish the leather set from Getting Started. Leather can be dyed any colour."',
      '"&eWhat:&r the whole leather set: cap, tunic, trousers and boots. Getting Started asked for two of them; this is all four. Leather can be dyed any colour."')
patch("hv_leather_set", '"&eHow:&r 5 leather for the cap, 7 for the leggings.', '"&eHow:&r 24 leather for the set (5, 8, 7 and 4).')
patch("hv_diamond_armor", 'deps=["hv_iron"], xp=80,', 'deps=["hv_iron"], xp=80, size=1.5, section=SETS, mirror="5DDC15AAFD2CAF47",')
patch("hv_netherite_armor", 'xp=150,', 'xp=150, size=1.5, section=SETS, mirror="074EC1E636CD6605",')
patch("hv_bronze_armor", 'xp=40,', 'xp=40, section=SETS, mirror="7B500E0577BDFF8F",')
patch("hv_lapis_armor", 'xp=30,', 'xp=30, section=SETS, mirror="65A529C8238E89F1",')
patch("hv_steel_armor", 'xp=60,', 'xp=60, section=SETS, mirror="3ABE7074E500494D",')

if 'Q("gs_opt_smithing"' not in s:
    i = s.rindex("], links=[")
    s = s[:i] + new + s[i:]
s = s.replace('("w_ostrum", 18, 4), ("sp_calorite", 20, 4), ("cp_trims_overworld", 14, 6)])',
              '("w_ostrum", 18, 4), ("sp_calorite", 20, 4), ("cp_trims_overworld", 14, 6)], mirror="basic_armor")')
assert 'mirror="basic_armor"' in s
p.write_text(s, encoding="utf-8", newline="\n")
print("done")
