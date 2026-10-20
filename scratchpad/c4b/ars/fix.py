import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
rep('deps=["ars_conjuration", "m_brazier"], xp=300,', 'deps=["ars_conjuration", "ars_wilden_ritual"], xp=300,')
rep('craft the Ritual of Wilden Summoning (purple archwood log, 3 Wilden drops, a lapis block), place it in a brazier away from your base, and fight."',
    'run the Ritual of Wilden Summoning (quest above) in a brazier away from your base, and fight."')
rep('"Storage Lectern", deps=["m_apparatus"], xp=50,', '"Storage Lectern", deps=["m_apparatus"], xp=50, section="Storage and Additions",')
rep('"Fire Essence", deps=["ars_source_gem"], xp=40,', '"Fire Essence", deps=["ars_source_gem"], xp=40, section="Essences",')
rep('"Wilden Hunt", deps=["m_book"], xp=75, loot="hunt",', '"Wilden Hunt", deps=["m_book"], xp=75, loot="hunt", section="The Wilden",')
rep('"Mark of Mastery", deps=["ars_chimera", "ars_anima"], xp=100,', '"Mark of Mastery", deps=["ars_chimera", "ars_anima"], xp=100, section="Ars Elemental",')
rep('"Mage Armor", deps=["ars_magebloom"], xp=75,', '"Mage Armor", deps=["ars_fiber"], xp=75, section="Mage Armor",')
s += '''    Q("ars_greater_discount", 0, 0, [tick()], "Two Ring Slots", deps=["ars_discount"], xp=30,
      optional=True, tokens=1, icon="ars_nouveau:ring_of_greater_discount", subtitle="Optional: how the discounts stack", desc=[
        "&eWhat:&r you can wear two rings at once, and their discounts add up.",
        "&eHow:&r wear a Greater and a Lesser ring together, or two Greater rings once you can afford them. Click the checkmark when both slots are full.",
        "&eTip:&r the rings quest above asks for one of each; this is the reminder to wear both."]),
'''
open(p, "w", encoding="utf-8", newline="\n").write(s)
