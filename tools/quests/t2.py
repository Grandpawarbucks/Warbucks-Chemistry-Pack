"""Quest chapter: t2. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, anytag, structure, biome, MAIN, SIDE  # noqa: F401

S_PORTAL, S_NCHEM, S_BREW = "Through the Portal", "Nether Chemistry", "The Brewer's Art"
S_PYLON, S_MAGIC = "Wings of a God", "Whispers of Magic"

CHAPTER = Chapter("t2", "III. Divine Ascent", "pylons:infusion_pylon",
        ["Walk through fire, brew in the dark, and take back the sky.",
         "Flight needs the Nether and your first Alchemistry machine: fire and chemistry together."], MAIN, [
    # --- through the portal ---------------------------------------------------------------
    Q("t2_obsidian", 0, 0, [item("minecraft:obsidian", 10), item("minecraft:flint_and_steel")], "A Door of Fire", section=S_PORTAL, deps=["gs_ironpick"], xp=30,
      subtitle="Ten blocks of obsidian and a spark", desc=[
        "&6You remember the sky. Not looking up at it: standing in it.&r",
        "&eWhat:&r a Nether portal is a 4x5 frame of obsidian (corners optional), lit with flint and steel.",
        "&eChemistry:&r obsidian is volcanic glass. Lava cooled so fast its atoms never had time to form crystals.",
        "&eHow:&r mine obsidian with a diamond pickaxe (or a steel paxel, which is diamond tier), or pour water over still lava to make it in place.",
        "&eTip:&r a bucket of water and a bucket of lava let you cast the frame block by block."]),
    Q("t2_nether", 2, 0, [dim("minecraft:the_nether")], "Into the Fire", section=S_PORTAL, deps=["t2_obsidian"], xp=100,
      subtitle="A dimension of quartz, fire and soul sand", desc=[
        "&eWhat:&r the Nether is a chemistry lab: quartz (SiO₂), blaze powder, glowstone and nether wart all come from here.",
        "&eHow:&r bring food, armour, blocks and a way home. NetherPortalFix keeps portals linked properly.",
        "&eTip:&r water evaporates instantly here and beds explode. Bring a respawn plan, not a bed."]),
    Q("t2_fortress", 4, -3, [item("minecraft:nether_brick", 32)], "Fortress Found", section=S_PORTAL, deps=["t2_nether"], xp=40, optional=True, tokens=1,
      subtitle="Bring home a piece of a fortress", desc=[
        "&eWhat:&r Nether Fortresses hold blazes, wither skeletons and nether wart.",
        "&eHow:&r Explorer's Compass points to structures. Mine nether bricks from the fortress walls.",
        "&eTip:&r build a small portal near the fortress and your next trip is much shorter."]),
    Q("t2_bastion", 0, 0, [structure("minecraft:bastion_remnant")], "A Bastion of Gold", subtitle="Piglin halls of blackstone", section=S_PORTAL,
      deps=["t2_nether"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r Bastion remnants are huge blackstone ruins full of piglins and gold. Stand inside one.",
        "&eHow:&r Explorer's Compass finds them. Wear at least one piece of gold armour so the piglins stay calm, and never open their chests in front of them.",
        "&eTip:&r the walls are polished blackstone already: a free start on the pylon's frame."]),
    Q("t2_deltas", 0, 0, [biome("minecraft:basalt_deltas")], "The Basalt Deltas", subtitle="Grey ash and black rock", section=S_PORTAL,
      deps=["t2_nether"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r the Nether's volcanic badlands: basalt columns, blackstone, magma cubes and falling ash.",
        "&eChemistry:&r basalt is the most common rock on Earth's ocean floors: lava rich in iron and magnesium that cooled slowly enough to form small crystals, unlike obsidian.",
        "&eTip:&r magma cubes here drop magma cream for Fire Resistance and the Dissolver's magma blocks."]),
    Q("t2_nether_gold", 0, 0, [item("minecraft:gold_nugget", 36)], "Nether Gold", subtitle="Specks of gold in netherrack", section=S_PORTAL,
      deps=["t2_nether"], optional=True, tokens=1, xp=25, desc=[
        "&eWhat:&r nether gold ore drops gold nuggets: four ingots' worth fills this quest.",
        "&eChemistry:&r gold is so unreactive that it occurs as the native metal, not as a compound. That's why it was the first metal people ever found.",
        "&eHow:&r mine the yellow-flecked netherrack with any pickaxe. Fortune helps."]),
    Q("t2_ghast", 8, -3, [item("minecraft:ghast_tear", 2)], "Ghast Tears", section=S_PORTAL, deps=["t2_nether"], xp=60, optional=True, tokens=1,
      subtitle="Regeneration, from a crying ghast", desc=[
        "&eWhat:&r ghast tears brew Regeneration and drop rarely, since the ghast must die over solid ground.",
        "&eHow:&r reflect a fireball back with a punch or arrow, then catch the tear before it burns in lava.",
        "&eTip:&r a bow and patience beat chasing ghasts across lava lakes."]),
    Q("t2_debris", 12, -3, [item("minecraft:ancient_debris", 2)], "Ancient Debris", section=S_PORTAL, deps=["t2_nether"], xp=100, optional=True, tokens=2,
      subtitle="The rarest ore in the Nether", desc=[
        "&eWhat:&r ancient debris smelts into netherite scrap, the base of netherite gear.",
        "&eHow:&r it hides deep in the Nether (around Y 8-22) and resists explosions, so bed or TNT mining works.",
        "&eTip:&r try the Dissolver on a scrap later and see what this 'element' really is."]),
    Q("t2_opt_netherite", 0, 0, [item("minecraft:netherite_ingot")], "Netherite", subtitle="Four scrap and four gold", section=S_PORTAL, deps=["t2_debris"],
      xp=100, optional=True, tokens=2, desc=[
        "&eWhat:&r The toughest metal in the game: netherite gear doesn't burn in lava and outlasts diamond.",
        "&eChemistry:&r Netherite isn't on the periodic table. In game terms it's an alloy: scrap from ancient debris fused with gold.",
        "&eHow:&r Smelt ancient debris into netherite scrap, then craft 4 scrap with 4 gold ingots. A smithing table and an upgrade template turn diamond gear into netherite.",
        "&eTip:&r Keep this in mind for later: calorite ore on Venus needs a netherite-tier pickaxe."]),
    Q("t2_wither_skull", 0, 0, [item("minecraft:wither_skeleton_skull")], "A Grim Trophy", subtitle="The rarest drop in a fortress", section=S_PORTAL,
      deps=["t2_fortress"], optional=True, tokens=2, xp=60, desc=[
        "&eWhat:&r wither skeletons drop their skull only now and then. Three of them summon the Wither, much later.",
        "&eHow:&r fight wither skeletons in fortress corridors with a Looting sword. Their hits cause Wither, so bring milk or a stack of food.",
        "&eTip:&r no rush: nothing in this chapter needs it. Put it on a shelf and admire it."]),

    # --- nether chemistry -----------------------------------------------------------------
    Q("t2_quartz", 10, -3, [item("minecraft:quartz", 16)], "Nether Quartz", section=S_NCHEM, deps=["t2_nether"], xp=25,
      subtitle="Silicon dioxide, straight from the rock", desc=[
        "&eWhat:&r Nether quartz ore is everywhere in Nether netherrack. The Infusion Pylon is capped with quartz.",
        "&eChemistry:&r quartz is silicon dioxide, SiO₂. Much later you'll reduce it with carbon to get pure silicon for circuits.",
        "&eTip:&r keep a spare stack. Quartz dust plus coke becomes silicon in Chapter V."]),
    Q("t2_blackstone", 10, -1, [item("minecraft:blackstone", 16)], "Blackstone", section=S_NCHEM, deps=["t2_nether"], xp=25,
      subtitle="Dark volcanic stone for the pylon", desc=[
        "&eWhat:&r the Infusion Pylon stands on polished blackstone.",
        "&eChemistry:&r blackstone is a basalt-like volcanic rock, rich in dark iron and magnesium minerals.",
        "&eHow:&r it fills basalt deltas and bastion remnants. Any pickaxe mines it."]),
    Q("t2_glowstone", 0, 0, [item("minecraft:glowstone_dust", 16)], "Glowstone", subtitle="Light that grows on the ceiling", section=S_NCHEM,
      deps=["t2_nether"], optional=True, tokens=1, xp=25, desc=[
        "&eWhat:&r glowstone clusters hang from the Nether's ceilings. The dust strengthens potions (Level II) at the cost of duration.",
        "&eHow:&r break glowstone blocks (they drop 2 to 4 dust) or kill witches. A Silk Touch tool gives the whole block.",
        "&eTip:&r a strengthened potion can't also be extended with redstone, so keep glowstone away from the potions you want to last."]),
    Q("t2_phosphorus", 0, 0, [item("chemlib:phosphorus", 16)], "The Light-Bearer", subtitle="Glowstone dissolves into phosphorus", section=S_NCHEM,
      deps=["t2_glowstone", "t1_dissolver"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r every glowstone dust dissolves into 4 phosphorus.",
        "&eChemistry:&r phosphorus means 'light-bearer' in Greek. White phosphorus glows in the dark as it slowly reacts with the oxygen in air. Hennig Brand found it in 1669 by boiling down urine.",
        "&eHow:&r put glowstone dust in the Dissolver."]),
    Q("t2_barium", 0, 0, [item("chemlib:barium", 16)], "Quartz, Undone", subtitle="One quartz, 32 silica and 16 barium", section=S_NCHEM,
      deps=["t2_quartz", "t1_dissolver"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r Nether quartz dissolves into 32 silicon dioxide and 16 barium.",
        "&eChemistry:&r pure quartz is only SiO₂, but real quartz veins often carry &ebarite&r (barium sulfate, BaSO₄). Barium salts burn green, which is how fireworks get that colour.",
        "&eHow:&r put Nether quartz in the Dissolver."]),
    Q("t2_germanium", 0, 0, [item("chemlib:germanium", 8)], "Blaze Powder, Undone", subtitle="Germanium, carbon and sulfur", section=S_NCHEM,
      deps=["t2_blaze_powder", "t1_dissolver"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r Alchemistry reads blaze powder as 8 germanium, 2 graphite and 8 sulfur.",
        "&eChemistry:&r germanium (Ge, 32) is a semiconductor. The first transistor, built at Bell Labs in 1947, was a sliver of germanium.",
        "&eTip:&r the sulfur is handy: Chapter IV's battery acid needs sulfur too."]),
    Q("t2_soul_sand", 0, 0, [item("minecraft:soul_sand", 16)], "Soul Sand", subtitle="Where nether wart grows", section=S_NCHEM,
      deps=["t2_nether"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r nether wart only grows on soul sand. Bring some home and plant a wart farm.",
        "&eHow:&r soul sand valleys are full of it, and fortress stairwells have small patches. A shovel digs it fast.",
        "&eTip:&r soul sand under water makes a bubble column that pushes you up."]),

    # --- the brewer's art -----------------------------------------------------------------
    Q("t2_blaze", 4, -1, [item("minecraft:blaze_rod", 4)], "Blaze Rods", section=S_BREW, deps=["t2_nether"], xp=50,
      subtitle="Fuel for the brewing stand", desc=[
        "&eWhat:&r blaze rods craft the brewing stand, and blaze powder fuels it.",
        "&eHow:&r blazes spawn around spawners in Nether Fortresses. Explorer's Compass can point you to one.",
        "&eTip:&r snowballs hurt blazes, and fire resistance makes the fight easy."]),
    Q("t2_blaze_powder", 0, 0, [item("minecraft:blaze_powder", 8)], "Blaze Powder", subtitle="Crushed rods burn the brew", section=S_BREW,
      deps=["t2_blaze"], xp=25, desc=[
        "&eWhat:&r blaze powder fuels the brewing stand: one powder lasts 20 brews.",
        "&eHow:&r 1 blaze rod makes 2 powder by hand. The Steam Macerator gets 4 per rod.",
        "&eTip:&r keep one rod back for the stand itself."]),
    Q("t2_wart", 4, 1, [item("minecraft:nether_wart", 8)], "Nether Wart", section=S_BREW, deps=["t2_nether"], xp=25,
      subtitle="The base of almost every potion", desc=[
        "&eWhat:&r the base reagent for almost every potion.",
        "&eHow:&r it grows on soul sand in fortress stairwells. Bring some soul sand home and replant it; it grows in the Overworld too.",
        "&eTip:&r one stack of wart grown at home covers every brew in this chapter."]),
    Q("t2_brewing", 6, 0, [item("minecraft:brewing_stand")], "The Brewer's Art", section=S_BREW, deps=["t2_blaze_powder", "t2_wart"], xp=75,
      subtitle="Applied chemistry, the old-fashioned way", desc=[
        "&6Tinctures and draughts: the first chemistry was done by people trying to bottle a little divinity. You can relate.&r",
        "&eWhat:&r a brewing stand turns water bottles into potions, one ingredient at a time.",
        "&eChemistry:&r brewing is extraction and reaction: each ingredient changes what's dissolved in the bottle.",
        "&eHow:&r 1 blaze rod + 3 cobblestone. Blaze powder in the top-left slot fuels 20 brews.",
        "&eTip:&r look up &ePotion of Flying&r in JEI (from Apothic Attributes). The next quests walk the whole chain."]),
    Q("t2_bottles", 0, 0, [item("minecraft:glass_bottle", 6)], "Glass Bottles", subtitle="Three glass, three bottles", section=S_BREW, deps=["t2_brewing"], xp=15, desc=[
        "&eWhat:&r every potion lives in a bottle. The stand brews three at a time.",
        "&eHow:&r 3 glass in a V shape make 3 bottles. The Steam Compressor presses 1 glass block into 2.",
        "&eTip:&r make plenty: the flight chain takes several rounds of three."]),
    Q("t2_water_bottles", 0, 0, [item("minecraft:potion", 3)], "Bottled Water", subtitle="The solvent for every brew", section=S_BREW, deps=["t2_bottles"], xp=15, desc=[
        "&eWhat:&r fill three bottles from any water source. Then brew nether wart into them to get &eAwkward Potions&r, the base of almost every recipe.",
        "&eChemistry:&r water is the universal solvent: its polar molecules pull apart salts and sugars, so whatever you add to the bottle ends up dissolved in it.",
        "&eHow:&r right-click water with empty bottles. Any potion counts for this quest."]),
    Q("t2_fireres", 6, -3, [item("minecraft:magma_cream", 4)], "Fire Resistance", section=S_BREW, deps=["t2_brewing"], xp=40, optional=True, tokens=1,
      subtitle="Awkward + magma cream", desc=[
        "&eWhat:&r Fire Resistance makes lava and blaze fire harmless. Swimming in lava becomes a shortcut.",
        "&eHow:&r magma cubes drop magma cream in basalt deltas, or craft it from blaze powder + slimeball. Brew it into an Awkward Potion.",
        "&eTip:&r add redstone for an 8-minute version before any lava-heavy trip."]),
    Q("t2_slowfall", 10, 0, [item("minecraft:phantom_membrane", 2)], "Slow Falling", section=S_BREW, deps=["t2_water_bottles"], xp=50,
      subtitle="Awkward + phantom membrane", desc=[
        "&eWhat:&r step 1 toward flight. Awkward Potion + phantom membrane = Potion of Slow Falling.",
        "&eHow:&r phantoms appear at night when someone in the world hasn't slept for three or more days. Fight them on a roof.",
        "&eTip:&r one membrane brews three bottles, so two membranes go a long way."]),
    Q("t2_spider_eye", 0, 0, [item("minecraft:spider_eye", 2), item("minecraft:sugar", 2), item("minecraft:brown_mushroom", 2)], "Fermenting Supplies",
      subtitle="Spider eye, sugar and a mushroom", section=S_BREW, deps=["t2_brewing"], xp=20, desc=[
        "&eWhat:&r the three ingredients of a fermented spider eye, the reagent that turns an effect into its opposite.",
        "&eChemistry:&r fermentation needs a sugar to feed on and a living culture to do the work. Here the mushroom plays the yeast and the sugar is its food.",
        "&eHow:&r spiders and cave spiders drop eyes, sugar comes from sugar cane, and brown mushrooms grow in dark places."]),
    Q("t2_levitation", 12, 0, [item("minecraft:fermented_spider_eye")], "Levitation", section=S_BREW, deps=["t2_slowfall", "t2_spider_eye"], xp=50,
      subtitle="Slow Falling + fermented spider eye", desc=[
        "&eWhat:&r step 2. Slow Falling + fermented spider eye = Potion of Levitation (Apothic Attributes).",
        "&eChemistry:&r fermentation is yeast turning sugar into alcohol and acids. Here it 'corrupts' the effect into its opposite.",
        "&eHow:&r fermented spider eye = spider eye + sugar + brown mushroom (shapeless). The Steam Mixer can make them too."]),
    Q("t2_chorus", 14, 0, [item("chemlib:hydrogen", 2)], "Lifting Gas", section=S_BREW, deps=["t2_levitation", "t2_hydrogen"], xp=100,
      subtitle="Levitation + hydrogen = Flying", desc=[
        "&eWhat:&r step 3. In this pack, Flying is made with &ehydrogen&r instead of End chorus fruit, so you can fly before the End.",
        "&eChemistry:&r hydrogen (H₂) is the lightest gas there is, about 14 times lighter than air. It lifted the first passenger balloons in 1783.",
        "&eHow:&r in a crafting grid, 1 Potion of Levitation + 2 hydrogen make a &ePotion of Flying&r: 8 minutes of creative-style flight (check JEI).",
        "&eTip:&r don't drink it yet; the next step makes it last longer. The brewing-stand route (popped chorus fruit) also works once you reach the End."]),
    Q("t2_longflying", 18, 0, [item("minecraft:redstone", 8)], "Extended Flight", section=S_BREW, deps=["t2_chorus"], xp=75,
      subtitle="Redstone, twice: 15 minutes, then 30", desc=[
        "&eWhat:&r redstone stretches a potion's duration. Flying + redstone = Long Flying (15 min). Add redstone again for Extra Long Flying (30 min).",
        "&eHow:&r brew redstone into your Flying potions, then into the Long ones.",
        "&eTip:&r a Potion Filter needs a full hour, which is just &etwo Extra Long&r potions. Brew at least two."]),

    # --- wings of a god -------------------------------------------------------------------
    Q("t2_hydrogen", 20, 2, [item("chemlib:hydrogen", 8)], "Lighter than Air", section=S_PYLON, deps=["t1_dissolver"], xp=75,
      subtitle="The lightest element, from your Dissolver", desc=[
        "&eWhat:&r your flight potion and the pylon itself need hydrogen, and only the &eDissolver&r can pull it out of matter as an item.",
        "&eChemistry:&r H is element 1: one proton, one electron. It makes up about three quarters of the ordinary matter in the universe.",
        "&eHow:&r dissolve logs (cellulose) or sugar (sucrose), or let the Atomizer turn piped water into ChemLib water and dissolve that: 2 hydrogen each.",
        "&eTip:&r feed the Dissolver from a hopper and it runs while you're in the Nether."]),
    Q("t2_emerald", 0, 0, [item("minecraft:emerald_block")], "A Block of Emerald", subtitle="Nine emeralds at the pylon's heart", section=S_PYLON,
      deps=["gs_ironpick"], xp=40, desc=[
        "&eWhat:&r the Infusion Pylon is built around a block of emerald, and the Potion Filter needs one more emerald.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈, coloured green by a trace of chromium. Without the chromium the same crystal is colourless.",
        "&eHow:&r emerald ore hides in mountain biomes. Trading with villagers is the steadier way: most professions pay emeralds for simple goods.",
        "&eTip:&r a farmer villager buys wheat, potatoes and carrots. Your field from the first day pays for this."]),
    Q("t2_dyes", 0, 0, [item("minecraft:cyan_terracotta", 2), item("minecraft:green_dye")], "Coloured Clay", subtitle="Cyan terracotta and green dye",
      section=S_PYLON, deps=["gs_ironpick"], xp=25, desc=[
        "&eWhat:&r the Potion Filter is framed in cyan terracotta with a green dye at its centre.",
        "&eChemistry:&r smelt cactus and its green pigment survives as dye. Mix it with lapis blue for cyan. Alchemistry agrees: 4 copper chloride compact into cyan dye, the colour of copper salts.",
        "&eHow:&r smelt clay blocks into terracotta, then 8 terracotta around 1 cyan dye make 8 cyan terracotta."]),
    Q("t2_filter", 20, 0, [item("pylons:potion_filter")], "Potion Filter", section=S_PYLON, deps=["t2_longflying", "t2_emerald", "t2_dyes"], xp=75, size=1.5,
      subtitle="Store an effect in a filter", desc=[
        "&6An hour of flight, folded into a pane of glass. Close enough to a feather from your old wings.&r",
        "&eWhat:&r a Potion Filter holds a potion effect for the Infusion Pylon.",
        "&eHow:&r 2 cyan terracotta, green dye, an emerald and 5 glass. Drink a potion, then right-click the filter to store the effect. It activates once it holds &e1 hour&r of Flying: two Extra Long (30 min each), four Long (15 min) or about eight regular potions.",
        "&eTip:&r drink and load one potion at a time so none of the effect runs out first. Two filters with the same effect combine: hold one in each hand and right-click."]),
    Q("t2_quartz_slab", 0, 0, [item("minecraft:quartz_slab", 2)], "Quartz Slabs", subtitle="The pylon's cap", section=S_PYLON, deps=["t2_quartz"], xp=20, desc=[
        "&eWhat:&r the pylon is topped with two quartz slabs.",
        "&eHow:&r 4 Nether quartz make a block of quartz; 3 blocks in a row make 6 slabs."]),
    Q("t2_polished", 0, 0, [item("minecraft:polished_blackstone", 3), item("minecraft:iron_bars", 2)], "The Pylon's Frame",
      subtitle="Polished blackstone and iron bars", section=S_PYLON, deps=["t2_blackstone"], xp=20, desc=[
        "&eWhat:&r the pylon stands on 3 polished blackstone with 2 iron bars at its sides.",
        "&eHow:&r 4 blackstone in a 2x2 make 4 polished blackstone. 6 iron ingots make 16 iron bars."]),
    Q("t2_pylon", 24, 0, [item("pylons:infusion_pylon")], "Wings of a God", section=S_PYLON,
      deps=["t2_filter", "t2_quartz_slab", "t2_polished", "t2_hydrogen", "t2_emerald"], xp=500, size=2.0, shape="hexagon",
      items=[("minecraft:experience_bottle", 32)], subtitle="Permanent flight, built from fire and hydrogen", desc=[
        "&6Your second gift returns, and the sky is yours again. You had forgotten how small the world looks from here.&r",
        "&eWhat:&r the &eInfusion Pylon&r applies a filter's effect to you anywhere. With a Flying filter, that's creative-style flight.",
        "&eHow:&r 2 quartz slabs, 2 iron bars, a block of emerald, 3 polished blackstone and 1 &ehydrogen&r from your Dissolver (see JEI). Place it and put the full (one-hour) filter inside.",
        "&eTip:&r the pylon only works while its chunk is loaded. Force-load it (see the next quest)."]),
    Q("t2_chunkload", 26, 2, [tick()], "Keep It Running", section=S_PYLON, deps=["t2_pylon"], xp=50, optional=True, tokens=1,
      subtitle="Force-load the pylon's chunk", desc=[
        "&eWhat:&r if the pylon's chunk unloads, your flight stops. Over a long trip that means a long fall.",
        "&eHow:&r open the FTB Chunks map (press M), claim the chunk with the pylon, then right-click it again to force-load it.",
        "&eTip:&r force-load your Dissolver and brewing setup too, so they keep working while you travel."]),
    Q("t2_opt_ender", 0, 0, [item("minecraft:ender_pearl", 4), item("minecraft:ender_eye", 2)], "Eyes of Ender", subtitle="Blaze powder and a pearl",
      section=S_PYLON, deps=["t2_blaze_powder"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r An Eye of Ender, thrown, flies towards the nearest stronghold, and twelve of them open the way to the End.",
        "&eHow:&r Endermen drop ender pearls; they spawn in every dimension but crowd the Nether's warped forests. Craft 1 pearl with 1 blaze powder (shapeless) for an eye.",
        "&eTip:&r No rush. Flight here runs on hydrogen, so the End can wait until you want its chorus fruit."]),

    # --- whispers of magic ----------------------------------------------------------------
    Q("t2_ars", 2, 2, [item("ars_nouveau:worn_notebook"), item("ars_nouveau:source_gem", 4)], "Whispers of Magic", section=S_MAGIC, deps=["t2_nether"], xp=50,
      subtitle="Light magic suits a demigod", desc=[
        "&eWhat:&r the Worn Notebook teaches Ars Nouveau spellcrafting. Source gems are its basic magical material.",
        "&eHow:&r the notebook is a book + lapis lazuli (shapeless). Source gems come from the Imbuement Chamber (lapis or amethyst + Source).",
        "&eTip:&r its Ritual of Flight is a second way to fly near your base. See the Ars Nouveau page (Magic and Relics)."]),
    Q("t2_sourcelink", 2, 3, [item("ars_nouveau:volcanic_sourcelink")], "Fire into Source", section=S_MAGIC, deps=["t2_ars"], xp=60, optional=True, tokens=1,
      subtitle="Burn fuel to make magical Source", desc=[
        "&eWhat:&r the Volcanic Sourcelink turns burning fuel into Source, the energy behind Ars Nouveau.",
        "&eHow:&r craft it from source gems, gold and a lava bucket, place it near a Source Jar and give it fuel. The Worn Notebook explains the details.",
        "&eTip:&r it suits a Nether-themed base: blaze rods and lava-adjacent fuels keep it going."]),
    Q("t2_archwood", 4, 3, [anytag("c:logs/archwood", 8)], "Archwood", section=S_MAGIC, deps=["t2_ars"], xp=40, optional=True, tokens=1,
      subtitle="Magic trees in the archwood forests", desc=[
        "&eWhat:&r archwood is Ars Nouveau's magic wood, used for its jars, tables and rituals.",
        "&eHow:&r look for brightly coloured trees in archwood forests; any colour of archwood log counts.",
        "&eTip:&r archwood saplings grow at home, so a few logs become a farm."]),
])
