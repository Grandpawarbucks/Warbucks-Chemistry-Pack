import pathlib
p = pathlib.Path("tools/quests/power.py"); s = p.read_text(encoding="utf-8")
R = [
 ('"silver ingots around a copper or iron furnace (check JEI)."', '"silver ingots and glass around an iron furnace (check JEI)."'),
 ('"gold ingots around an iron or silver furnace (check JEI)."', '"gold ingots and a block of gold around an iron furnace (check JEI)."'),
 ('"check JEI: quartz and glass around a diamond furnace."', '"glass and an eye of ender around a diamond furnace (check JEI)."'),
 ('extra="quartz is crystalline SiO₂, the same compound as most sand, just ordered into a lattice."',
  'extra="window glass is mostly SiO₂ with soda and lime. Unlike quartz, its atoms have no regular lattice: it is a frozen liquid, not a crystal."'),
 ('"obsidian around an emerald or crystal furnace (check JEI)."', '"obsidian and blaze rods around an emerald furnace (check JEI)."'),
 ('"netherite on an obsidian furnace at a smithing table (check JEI)."', '"netherite ingots, magma cream and a soul sand or soul soil block around an obsidian furnace (check JEI)."'),
 ('"Allthemodium ingots around a netherite furnace (check JEI). Allthemodium comes from the Mining dimension."',
  '"Allthemodium ingots and blocks around a netherite furnace (check JEI)."'),
 ('"copper and a furnace (check JEI)."', '"copper ingots around a furnace, with a redstone block (check JEI)."'),
 ('"iron and a furnace (check JEI)."', '"iron ingots around a copper generator, with a redstone block (check JEI)."'),
 ('"a gold generator with food items (check JEI)."', '"crops, a cake and eggs around a gold generator, with a redstone block (check JEI)."'),
 ('"a culinary generator with brewing stands (check JEI)."', '"pink dye around a culinary generator, with brewing stands and a redstone block (check JEI)."'),
 ('"an obsidian generator with magma and lava (check JEI)."', '"gold ingots around an obsidian generator, with a lava bucket (check JEI)."'),
 ('"check JEI; it needs a Nether Star and the netherite generator."', '"wither skeleton skulls around a netherite generator, with a redstone block (check JEI)."'),
 ('"an ender generator with dragon\'s breath (check JEI)."', '"amethyst around an ender generator, with an end rod (check JEI)."'),
 ('"burns dragon\'s breath, bottled from the dragon\'s attacks."', '"burns dragon\'s breath, bottled from the dragon\'s attacks in the End."'),
]
for a, b in R:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
