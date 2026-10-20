"""Merge the Mystical Agriculture mirror into tools/quests/mystical.py."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests/mystical.py"
s = p.read_text(encoding="utf-8")
head = (ROOT / "scratchpad/c5b/mystical_head.txt").read_text(encoding="utf-8")
new = (ROOT / "scratchpad/c5b/mystical_new.txt").read_text(encoding="utf-8")
new = new.replace('("ma_accel_t5", "3E3CBDCEAB0FF28F")', '("ma_accel_t5", "3E555B364FD88B43")')
new = new.replace('"wither skeleton skulls and coal"', '"wither skeleton skulls"')
head = head.replace('how += "a full Soul Jar of that mob on the pedestals" if mob else f"{label} on the pedestals"',
                    'how += "a full Soul Jar of that mob on the pedestals" if mob and crop != "experience" else "the crop\'s materials on the pedestals"')
assert "crop's materials" in head

anchor = 'ACCEL_UP = [MA + t + "_growth_accelerator" for t in TIERS[1:] + ["awakened_supremium"]]\n'
if "def seed(" not in s:
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + head)


def block(key):
    m = re.search(r'    Q\("' + key + r'".*?\]\),\n', s, re.S)
    assert m, key
    return m.group(0)


def patch(key, old, new_):
    global s
    b = block(key)
    assert old in b, (key, old)
    s = s.replace(b, b.replace(old, new_, 1))


def require(key):
    """Make an optional quest required (ATM10 has it on its required line)."""
    global s
    b = block(key)
    nb = re.sub(r'\s*optional=True,', '', b)
    nb = re.sub(r'\s*tokens=\d,', '', nb)
    nb = nb.replace('subtitle="Optional: ', 'subtitle="').replace('subtitle="Optional: ', 'subtitle="')
    nb = re.sub(r'(subtitle=")(\w)', lambda m: m.group(1) + m.group(2).upper(), nb, count=1)
    s = s.replace(b, nb)


def setkw(key, kw):
    """Add keyword args after the deps=[...] of a quest."""
    global s
    b = block(key)
    nb = re.sub(r'(deps=\[[^\]]*\])', r'\1, ' + kw, b, count=1)
    s = s.replace(b, nb)


def setdeps(key, deps):
    global s
    b = block(key)
    nb = re.sub(r'deps=\[[^\]]*\]', 'deps=' + deps, b, count=1)
    s = s.replace(b, nb)


# spine
patch("f_altar", '[item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:inferium_essence", 16)]',
      '[item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:infusion_pedestal", 8)]')
setdeps("f_altar", '["ma_seed_base", "gs_iron"]'); setkw("f_altar", 'size=2.0, shape="gear", section=SPINE, mirror="0B37355262121DD5"')
patch("f_altar", '"&eHow:&r inferium ore gives inferium essence (mobs drop some too). The altar is gold, stone and red wool; pedestals are in JEI."',
      '"&eHow:&r the altar is gold, stone and red wool; 8 Infusion Pedestals stand around it (check JEI for both and the layout)."')
patch("f_prosperity", '[item("mysticalagriculture:prosperity_shard", 8), item("mysticalagriculture:prosperity_seed_base")]',
      '[item("mysticalagriculture:prosperity_shard", 4)]')
setdeps("f_prosperity", '["ma_hub"]'); setkw("f_prosperity", 'size=1.5, section=SPINE, mirror="2DDA04088C8220D2"')
patch("f_prosperity", '"&eHow:&r mine prosperity ore; 4 shards around wheat seeds make a Prosperity Seed Base."', '"&eHow:&r mine prosperity ore (an iron pick is enough)."')
setdeps("f_crystal", '["ma_inferium"]'); setkw("f_crystal", 'size=1.25, section=SPINE, mirror="217DB12EA32E1724"')
patch("f_prudentium", 'item("mysticalagriculture:prudentium_essence", 8)', 'item("mysticalagriculture:prudentium_essence")')
setkw("f_prudentium", 'size=1.5, section=SPINE, mirror="73350AD668200E99"')
patch("f_tertium", 'item("mysticalagriculture:tertium_essence", 8)', 'item("mysticalagriculture:tertium_essence")')
setkw("f_tertium", 'size=1.5, section=SPINE, mirror="2C9C9CB71941DC01"')
patch("f_imperium", 'item("mysticalagriculture:imperium_essence", 8)', 'item("mysticalagriculture:imperium_essence")')
setkw("f_imperium", 'size=1.5, section=SPINE, mirror="66C52B137A4FF869"')
patch("f_supremium", 'item("mysticalagriculture:supremium_essence", 8)', 'item("mysticalagriculture:supremium_essence")')
setkw("f_supremium", 'section=SPINE, mirror="67DBE6C59C0D9D1B"')
# tier 1 kit
patch("f_accelerator", 'item("mysticalagriculture:inferium_growth_accelerator", 4)', 'item("mysticalagriculture:inferium_growth_accelerator")')
setdeps("f_accelerator", '["ma_inferium"]'); setkw("f_accelerator", 'section=SPINE, mirror="4821419D44F8083F"'); require("f_accelerator")
patch("ma_farmland", '[item("mysticalagriculture:inferium_farmland", 8)]', '[item("mysticalagriculture:inferium_farmland"), item("mysticalagriculture:inferium_seeds")]')
setdeps("ma_farmland", '["ma_inferium"]'); setkw("ma_farmland", 'section=SPINE, mirror="7DFF18CFEB0B8DBE"'); require("ma_farmland")
patch("ma_farmland", 'subtitle="Better soil for inferium crops"', 'subtitle="Better soil, and the first seeds"')
patch("ma_gear", '[anyof(ARMOR)]', '[item(MA + "inferium_" + p) for p in ("helmet", "chestplate", "leggings", "boots")]')
patch("ma_gear", '"Essence Armor"', '"Inferium Armour"')
setdeps("ma_gear", '["ma_inferium"]'); setkw("ma_gear", 'section=SPINE, mirror="2A7E3F2CD335EAD0"'); require("ma_gear")
patch("ma_weapons", '[anyof(WEAPONS)]', '[anyof(tier_tools("inferium"))]')
patch("ma_weapons", '"Essence Weapons"', '"Inferium Tools"')
setdeps("ma_weapons", '["ma_inferium"]'); setkw("ma_weapons", 'section=SPINE, mirror="4EF5DE3FBA2A7AE3"'); require("ma_weapons")
# tier 2 kit (reused)
patch("ma_farmland_up", '[anyof(FARMLAND_UP, 8)]', '[item(MA + "prudentium_farmland")]')
setdeps("ma_farmland_up", '["f_prudentium"]'); setkw("ma_farmland_up", 'section=SPINE, mirror="576ABF43FCF886B7"'); require("ma_farmland_up")
patch("ma_accel_up", '[anyof(ACCEL_UP, 4)]', '[item(MA + "prudentium_growth_accelerator")]')
setdeps("ma_accel_up", '["f_prudentium"]'); setkw("ma_accel_up", 'section=SPINE, mirror="7655E1C6C5E5469F"'); require("ma_accel_up")
# machines and the rest
setdeps("ma_master", '["f_supremium"]'); setkw("ma_master", 'size=1.25, section=SPINE, mirror="219A5BDA5A01A420"'); require("ma_master")
patch("ma_augments", '[item(MA + "tinkering_table"), item(MA + "unattuned_augment")]', '[item(MA + "unattuned_augment")]')
setdeps("ma_augments", '["ma_weapons", "ma_gear"]'); setkw("ma_augments", 'any_dep=True, section=MACH, mirror="37B297640F537383"'); require("ma_augments")
patch("ma_augments", '"&eHow:&r the table is stone and soulium dust. An Unattuned Augment is prosperity shards and iron; attune it on the altar (check JEI)."',
      '"&eHow:&r an Unattuned Augment is prosperity shards and iron; attune it on the altar (check JEI). The Tinkering Table fits it."')
setdeps("ma_reprocessor", '["ma_hub"]'); setkw("ma_reprocessor", 'section=MACH, mirror="5C590DB2F3D935E5"'); require("ma_reprocessor")
setdeps("ma_spawner", '["ma_hub"]'); setkw("ma_spawner", 'section=MACH, mirror="16E3031D800B40D5"'); require("ma_spawner")
setdeps("ma_furnace", '["f_prosperity"]'); setkw("ma_furnace", 'section=MACH, mirror="21A90474590FCDB8"'); require("ma_furnace")
setdeps("ma_can", '["ma_hub"]'); setkw("ma_can", 'section=MACH, mirror="1636F3F12E92CAEA"')
setdeps("ma_harvester", '["ma_scythe"]'); setkw("ma_harvester", 'section=MACH, mirror="0EFEDB0DD90DFC81"'); require("ma_harvester")
patch("ma_fertilizer", 'item("mysticalagriculture:mystical_fertilizer", 4)', 'item("mysticalagriculture:mystical_fertilizer")')
setdeps("ma_fertilizer", '["ma_hub"]'); setkw("ma_fertilizer", 'section=MACH, mirror="6501A410F1543C70"')
setdeps("ma_enchanter", '["ma_hub"]'); setkw("ma_enchanter", 'section=MACH, mirror="6235B9923BE0AAEB"')
setdeps("ma_extractor", '["ma_hub"]'); setkw("ma_extractor", 'section=MACH, mirror="3EA2578C3A56FAE8"'); require("ma_extractor")
patch("ma_dagger", '[item("mysticalagriculture:soulium_dagger")]',
      '[item("mysticalagriculture:soulium_dagger"), item("mysticalagriculture:soul_jar", 4), item("mysticalagriculture:soul_extractor")]')
setdeps("ma_dagger", '["f_prudentium", "ma_soulium"]'); setkw("ma_dagger", 'section="Tier 2 Mobs", mirror="75560045ED084900"')
patch("ma_dagger", '"&eTip:&r JEI\'s soul extraction page shows how many souls each mob gives."',
      '"&eTip:&r carry 4 Soul Jars for four mob types; the Soul Extractor fills jars from drops instead of kills."')
# awakening
patch("ma_awaken_parts", '[item(MA + "awakening_pedestal", 4), item(MA + "essence_vessel", 4)]',
      '[item(MA + "awakening_altar"), item(MA + "awakening_pedestal", 4), item(MA + "essence_vessel", 4)]')
setdeps("ma_awaken_parts", '["f_supremium"]'); setkw("ma_awaken_parts", 'section=SPINE, mirror="33D23C65E7274A8F"'); require("ma_awaken_parts")
patch("ma_cognizant", '[item(MA + "cognizant_dust")]', '[item(MA + "cognizant_dust", 4)]')
setdeps("ma_cognizant", '["f_supremium"]'); setkw("ma_cognizant", 'section=SPINE, mirror="1CF8263756EE8F2A"'); require("ma_cognizant")
patch("f_awakening", '[item("mysticalagriculture:awakening_altar"), item("mysticalagriculture:awakened_supremium_essence", 4)]',
      '[item("mysticalagriculture:awakened_supremium_essence")]')
setdeps("f_awakening", '["ma_awaken_parts", "ma_cognizant"]'); setkw("f_awakening", 'size=2.0, shape="gear", section=SPINE, mirror="7A103577EAE7B3F1"'); require("f_awakening")
patch("ma_witherproof", '[item(MA + "witherproof_bricks", 16)]', '[anyof([MA + "witherproof_block", MA + "witherproof_bricks", MA + "witherproof_glass"])]')
setdeps("ma_witherproof", '["ma_s_wither_skeleton"]'); setkw("ma_witherproof", 'section="Tier 5 Mobs", mirror="408D8B1CFBA22BAF"')

if 'Q("ma_hub"' not in s:
    i = s.rindex("], links=[")
    s = s[:i] + new + s[i:]
if 'mirror="elmystical_agriculturerr"' not in s:
    s = s.replace('("f_pot", 6, 7.5)])', '("f_pot", 6, 7.5)], mirror="elmystical_agriculturerr")')
assert 'mirror="elmystical_agriculturerr"' in s
p.write_text(s, encoding="utf-8", newline="\n")
print("done")
