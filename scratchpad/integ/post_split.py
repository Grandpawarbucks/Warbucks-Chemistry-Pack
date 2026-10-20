import pathlib
Qd = pathlib.Path(__file__).resolve().parents[2] / "tools/quests"
p = Qd / "power.py"; t = p.read_text(encoding="utf-8")
t = t.replace('''It also carries ATM10's "Generators" chapter (Iron Furnaces and
Generator Galore), quest for quest, in sections of its own. The engine takes one mirror target per chapter, so those
quests carry no mirror id; their ATM10 ids are in GEN_MIRROR below, ready if the page is ever split out.''',
'''ATM10's "Generators" chapter (Iron Furnaces and
Generator Galore) is its own page now (generators.py, split out 2026-10-20 with the keys unchanged).''')
t = t.replace('ATM10 Generators quests skipped: the credits checkmark and "Rainbow Furnace" (a renamed vanilla item, not a real item).\n', "")
t = t.replace('MEK, GEN, IF, GG, FLUX = "mekanism:", "mekanismgenerators:", "ironfurnaces:", "generatorgalore:", "fluxnetworks:"',
              'MEK, GEN, GG, FLUX = "mekanism:", "mekanismgenerators:", "generatorgalore:", "fluxnetworks:"')
t = t.replace('S_FURN, S_IF, S_RAINBOW, S_AUG, S_GG = "The Furnace", "Iron Furnaces", "The Rainbow Generator", "Furnace Augments", "Generator Galore"\n', "")
t = t.replace("mid-game and end-game plants, plus furnaces and Generator Galore.", "mid-game and end-game plants. Furnaces and Generator Galore have their own page, Generators.")
t = t.replace('''        "&eTip:&r refined fuels (like boosted diesel) burn for more EU per bucket. Check JEI."]),

], links=''', '''        "&eTip:&r refined fuels (like boosted diesel) burn for more EU per bucket. Check JEI."]),
], links=''')
assert "IF +" not in t and "S_IF" not in t
p.write_text(t, encoding="utf-8", newline="\n")
p = Qd / "logic.py"; t = p.read_text(encoding="utf-8")
o = '], links=[("gs_iron", 0, 0), ("t3_hull", 0, 0), ("t3_infuser", 0, 0), ("t5_ae2", 0, 0)])'
assert o in t
t = t.replace(o, '], links=[("gs_iron", 0, 0), ("t3_hull", 0, 0), ("t3_infuser", 0, 0), ("t5_ae2", 0, 0), ("lg_menril", 0, 0)])')
p.write_text(t, encoding="utf-8", newline="\n")
p = Qd / "shop_world.py"; t = p.read_text(encoding="utf-8")
t = t.replace('    "tf_carminite": "Carminite", "w_naga"', '    "tf_carminite": "Carminite", "hv_mat_carminite": "Carminite", "w_naga"')
p.write_text(t, encoding="utf-8", newline="\n")
print("ok")
