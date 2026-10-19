"""Quest chapter: harvest (Tools, Armour and Harvest Tiers). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Plan: docs/research/tools_harvest_plan.md. Prefix hv_.
Layout (auto-placed at build time; x/y are only hints): y=0 the harvest spine, one milestone per tier, each asking for
something the new tier lets you mine; y=-2 tools that reach that tier (any-of across mods); y=2 armour of matching
strength; y=4 optional material-science side quests.
Tier facts (1.21.1 block tags + this pack's KubeJS raises): stone tier = iron, copper, lapis, most MI and Mekanism ores;
iron tier = gold, redstone, diamond, emerald, zinc, sky stone, crimson iron, and (pack raise) MI titanium, tungsten,
platinum and iridium ores, Ad Astra desh; diamond tier = obsidian, crying obsidian, ancient debris, Ad Astra ostrum;
netherite tier = Silent Gear azure silver, Mekanism Extras naquadah, Ad Astra calorite; dreadrock needs Forgotten tools.
Existing tool/armour quests stay on their own pages (start, t0, t1, tools, mekanism, twilight, undergarden,
deeperdarker, justdirethings); this page links to them instead of repeating them.
"""
from questlib import Q, Chapter, item, dim, tick, structure, anyof, MAIN, SIDE  # noqa: F401

MC = "minecraft:"
MT = "mekanismtools:"
MI = "modern_industrialization:"


def vset(metal, ns=MC):
    return [item(f"{ns}{metal}_{p}") for p in ("helmet", "chestplate", "leggings", "boots")]


CHAPTER = Chapter("harvest", "Tools, Armour and Harvest Tiers", "minecraft:diamond_pickaxe",
        ["Which pickaxe mines what, and why harder is not the same as tougher."], SIDE, [
    # --- the harvest spine (y=0) ---------------------------------------------------------------
    Q("hv_intro", 0, 0, [tick()], "The Hardness of Things", deps=["gs_woodpick"], xp=10,
      subtitle="Why some blocks ignore your pickaxe", desc=[
        "&6Once you could split a mountain with a look. Now you need the right pick. You remember why: everything has a hardness.&r",
        "&eWhat:&r every ore needs a pickaxe of a certain tier: wood, stone, iron, diamond, netherite. Too weak a pick breaks the block slowly and drops nothing.",
        "&eChemistry:&r hardness is resistance to scratching and denting; toughness is resistance to cracking. A good tool needs both, and they pull against each other.",
        "&eHow:&r look at a block: Jade shows the tool it needs and turns red when yours is too weak. This page walks up the tiers.",
        "&eTip:&r this pack raises some tiers: MI titanium, tungsten, platinum and iridium ores need iron, and the rocket metals climb from iron to netherite."]),
    Q("hv_flint", 0, 4, [item(MC + "flint", 4)], "Flint", deps=["hv_intro"], xp=10, optional=True, tokens=1,
      subtitle="Optional: the first sharp edge", desc=[
        "&eWhat:&r flint drops from gravel. Silent Gear makes tool heads from it, and it lights the Nether portal.",
        "&eChemistry:&r flint and chert are microcrystalline quartz, SiO₂, about 7 on the Mohs scale: harder than steel. It breaks with a curved, shell-like (conchoidal) fracture that leaves a razor edge.",
        "&eHow:&r dig gravel with a shovel; each block has a small chance to drop flint instead.",
        "&eTip:&r a Silent Gear pickaxe with a flint head mines like stone, but you can repair and upgrade it."]),
    Q("hv_stone", 2, 0, [item(MC + "raw_iron", 8), item(MC + "raw_copper", 8)], "Stone Tier", deps=["hv_intro", "gs_stone"], xp=25,
      size=1.5, shape="hexagon", subtitle="Now you can mine iron, copper and lapis", desc=[
        "&eWhat:&r a stone pickaxe (or better) opens iron, copper and lapis, plus almost every Modern Industrialization and Mekanism ore: tin, lead, nickel, antimony, bauxite, salt, monazite, uranium, osmium and fluorite.",
        "&eChemistry:&r a stone pick is a rock hitting a rock. It works on iron ore because the iron minerals (haematite Fe₂O₃, magnetite Fe₃O₄) are softer than the granite-like stone of the head... roughly.",
        "&eHow:&r mine 8 raw iron and 8 raw copper with any stone-tier pick.",
        "&eTip:&r you can't mine gold, redstone or diamond yet. Mark where you saw them and come back with iron."]),
    Q("hv_bronze", 4, 0, [item(MI + "raw_tin", 8)], "Bronze Age", deps=["hv_stone", "t0_bronze"], xp=40,
      subtitle="Same tier, much longer life", desc=[
        "&eWhat:&r bronze tools are iron tier (Mekanism bronze, Silent Gear bronze): more durable than stone, and they reach gold, redstone and diamond.",
        "&eChemistry:&r pure copper is soft, about Mohs 3. Add roughly 12% tin and the bigger tin atoms sit in the copper lattice and pin the defects (dislocations) that let metal bend. That is solid-solution strengthening, and it started an age.",
        "&eHow:&r mine 8 raw tin. Tin ore needs only a stone pick; its mineral, cassiterite (SnO₂), is actually harder than iron ore.",
        "&eTip:&r the bronze paxel (Bronze Age on the T0 page) is a pick, axe and shovel in one."]),
    Q("hv_iron", 6, 0, [item(MC + "raw_gold", 4), item(MC + "redstone", 8), item(MC + "diamond")], "Iron Tier", deps=["hv_stone", "gs_ironpick"], xp=60,
      size=1.5, shape="hexagon", subtitle="Now you can mine gold, redstone and diamond", desc=[
        "&6Iron rings against stone, and something in you rings back. You remember iron.&r",
        "&eWhat:&r an iron-tier pick opens gold, redstone, diamond and emerald, Create zinc, AE2 sky stone, Silent Gear crimson iron, and in this pack the hard MI ores: titanium, tungsten, platinum and iridium.",
        "&eChemistry:&r pure iron is soft (about Mohs 4). Iron from a blast furnace (pig iron) carries about 4% carbon as brittle iron carbide, so it shatters. Useful iron sits between the two.",
        "&eHow:&r mine 4 raw gold, 8 redstone and a diamond with an iron pickaxe, iron paxel, bronze or osmium tools.",
        "&eTip:&r diamonds sit deep (near Y -58). Branch-mine in deepslate."]),
    Q("hv_hard_ores", 8, 2, [item(MI + "raw_tungsten", 4)], "Hard Ores", deps=["hv_iron"], xp=60,
      subtitle="Tungsten and titanium need an iron pick", desc=[
        "&eWhat:&r in this pack MI titanium, tungsten, platinum and iridium ores need an iron-tier pick. The metals inside still need the chemistry lines.",
        "&eChemistry:&r their real minerals are hard: wolframite ((Fe,Mn)WO₄) about 4-4.5, ilmenite (FeTiO₃) 5-6, sperrylite (PtAs₂) 6-7. Tungsten itself melts at 3422 °C, higher than any other metal.",
        "&eHow:&r mine 4 raw tungsten. Rich tungsten deposits sit at their own depth; check the ore pages in JEI.",
        "&eTip:&r a stone pick on these ores gets you nothing but a broken block. Bring iron."]),
    Q("hv_steel", 8, 0, [item(MC + "obsidian", 4), item(MC + "crying_obsidian")], "Diamond Tier, Without Diamonds", deps=["hv_iron", "t1_steel_paxel"], xp=80,
      size=1.5, shape="hexagon", subtitle="Now you can mine obsidian and ancient debris", desc=[
        "&6You remember quenching a blade in a cold river, and the hiss of it.&r",
        "&eWhat:&r Mekanism steel tools are diamond tier. Your steel paxel already mines obsidian, crying obsidian and ancient debris, long before you own a diamond pick.",
        "&eChemistry:&r steel is iron with 0.2-2% carbon. Heat it red hot and quench it in water and it becomes martensite: very hard, but brittle. Temper it (reheat to 200-600 °C) and it trades a little hardness for toughness.",
        "&eHow:&r mine 4 obsidian and a crying obsidian with the steel paxel (or any diamond-tier tool). Obsidian forms where water meets lava.",
        "{@pagebreak}",
        "&eChemistry:&r obsidian isn't actually hard: it's volcanic glass, mostly SiO₂ that cooled too fast to crystallise, about Mohs 5.5. It snaps to edges sharper than steel, which is why surgeons still sometimes use obsidian blades.",
        "&eTip:&r the game makes obsidian slow to mine for its blast resistance, not its hardness. Real obsidian shatters under a hammer."]),
    Q("hv_netherite", 10, 0, [item(MC + "netherite_scrap", 4), item(MC + "netherite_upgrade_smithing_template")], "Netherite Tier", deps=["hv_steel", "t2_nether"], xp=150,
      size=1.5, shape="hexagon", subtitle="Now you can mine azure silver and naquadah", desc=[
        "&eWhat:&r a netherite-tier tool opens Silent Gear azure silver ore (the End), Mekanism Extras naquadah ore and, much later, Ad Astra calorite.",
        "&eChemistry:&r netherite is fiction. The real champion of hard tools is tungsten carbide (WC, Mohs about 9), cemented with a little cobalt so it doesn't shatter: a ceramic-metal composite, or cermet.",
        "&eHow:&r smelt ancient debris into scrap; four scrap and four gold make a netherite ingot. The upgrade template comes from bastion chests.",
        "&eTip:&r copy a template with 7 diamonds and a netherrack before you use your last one."]),
    Q("hv_azure", 12, -2, [item("silentgear:raw_azure_silver", 4)], "Azure Silver", deps=["hv_netherite", "w_end"], xp=100, optional=True, tokens=1,
      subtitle="Optional: an End ore only netherite can mine", desc=[
        "&eWhat:&r azure silver ore grows on End islands and needs a netherite-tier tool. It's the base of Silent Gear's azure electrum.",
        "&eHow:&r mine 4 raw azure silver in the End with a netherite, refined obsidian or eclipse alloy pick.",
        "&eTip:&r a diamond pick just bounces off it; check the Jade tooltip first."]),
    Q("hv_refined", 12, 0, [item("mekanism:ingot_refined_obsidian", 2)], "Refined Obsidian", deps=["hv_steel", "t3_infuser"], xp=100,
      subtitle="Mekanism's road to netherite tier", desc=[
        "&eWhat:&r refined obsidian tools are netherite tier, no Nether trip needed. They're also Mekanism Tools' strongest set.",
        "&eChemistry:&r infusing osmium into obsidian dust is invented, but the idea is real: cermets (ceramic grains in a metal binder) are what drill bits and cutting inserts are made of.",
        "&eHow:&r Metallurgic Infuser: obsidian dust + diamond infusion → refined obsidian dust, then the Osmium Compressor (check JEI).",
        "&eTip:&r the refined obsidian paxel is on the Tools page; the armour is on the Mekanism page."]),
    Q("hv_forgotten", 14, 0, [item("undergarden:dreadrock", 16)], "Beyond Netherite", deps=["hv_netherite", "t4_undergarden", "ug_forgotten_tools"], xp=150,
      size=1.5, shape="hexagon", subtitle="Now you can mine dreadrock", desc=[
        "&6Harder was never the whole answer. You remember a stone that only its own metal could cut.&r",
        "&eWhat:&r dreadrock and its utherium and rogdorium ores need a Forgotten tool. Netherite fails here: dreadrock is on its 'can't mine' list.",
        "&eChemistry:&r 'harder' is not one number. A cutting edge has to out-scratch the mineral, survive the impact and not wear or react away. A diamond bit cuts granite but dissolves into hot steel, because carbon diffuses into iron.",
        "&eHow:&r mine 16 dreadrock at the bottom of the Undergarden with a Forgotten pickaxe.",
        "&eTip:&r warden and resonarium tools (Deeper and Darker) also mine it."]),
    Q("hv_space", 16, 0, [tick()], "Ores of Other Worlds", deps=["hv_steel", "t7_rocket"], xp=100,
      subtitle="Desh, ostrum and calorite climb the tiers", desc=[
        "&eWhat:&r in this pack the rocket metals climb the ladder: Moon desh needs an iron pick, Mars ostrum a diamond-tier pick, Venus calorite a netherite-tier pick.",
        "&eChemistry:&r the three are fiction, but real space mining would face the same problem: unknown minerals, unknown hardness. Geologists still carry a steel knife and a glass plate to test them.",
        "&eHow:&r bring a netherite-tier tool on every trip past the Moon. The desh, ostrum and calorite quests are on the T7 and Space pages.",
        "&eTip:&r a refined obsidian paxel covers all three and doesn't need the Nether."]),
    Q("hv_all", 18, 0, [anyof(["mekanism:atomic_disassembler", "mekanism:meka_tool", "deeperdarker:warden_pickaxe"])], "Every Block", deps=["hv_refined"], xp=200,
      size=2.0, shape="gear", subtitle="A tool with no tier at all", desc=[
        "&6No block refuses you now. You remember this: not strength, but understanding.&r",
        "&eWhat:&r the Atomic Disassembler, the Meka-Tool and the warden pickaxe have no 'can't mine' list. They break every block in the pack, dreadrock included.",
        "&eChemistry:&r an energy tool doesn't scratch. It's closer to a laser or plasma cutter: put enough energy into a spot and the bonds break whatever the hardness.",
        "&eHow:&r the Atomic Disassembler is on the Tools page, the Meka-Tool on the Mekanism page, the warden pickaxe on the Deeper and Darker page. Any one of them counts.",
        "&eTip:&r energy tools need charging; keep a charger or an Energy Cube near your base."]),

    # --- tools by tier (y=-2) ------------------------------------------------------------------
    Q("hv_lapis_tools", 2, -2, [anyof([MT + "lapis_lazuli_pickaxe", MT + "lapis_lazuli_paxel"])], "Lapis Tools", deps=["hv_stone"], xp=20,
      optional=True, tokens=1, subtitle="Optional: pretty, and only stone tier", desc=[
        "&eWhat:&r Mekanism Tools makes a lapis pickaxe and paxel. They mine at stone tier but enchant very well.",
        "&eChemistry:&r lapis lazuli is a rock, not one mineral: mostly lazurite (a sodium aluminosilicate with sulfur) about Mohs 5-5.5. The blue comes from S₃⁻ radical ions trapped in the crystal.",
        "&eHow:&r lapis and sticks, shaped like any pick (check JEI).",
        "&eTip:&r ground lapis was ultramarine, once worth more than gold to painters."]),
    Q("hv_iron_cousins", 6, -2, [anyof(["justdirethings:ferricore_pickaxe", "twilightforest:ironwood_pickaxe", "undergarden:cloggrum_pickaxe",
                                        MT + "bronze_pickaxe", MT + "osmium_pickaxe", MT + "osmium_paxel"])],
      "Iron-Tier Cousins", deps=["hv_iron"], xp=30, optional=True, tokens=1, subtitle="Optional: one tier, many mods", desc=[
        "&eWhat:&r each of these mines exactly what an iron pick does: ferricore (Just Dire Things), ironwood (Twilight), cloggrum (Undergarden), bronze and osmium (Mekanism Tools).",
        "&eChemistry:&r osmium is the densest element (22.6 g/cm³) and quite hard, but brittle: real osmium is almost never used for tools, only for tiny wear-proof tips like old pen nibs.",
        "&eHow:&r craft any one of them; their mods' pages show the recipes.",
        "&eTip:&r durability and speed differ a lot between them even at the same tier. Check the tooltip."]),
    Q("hv_diamond_pick", 8, -2, [item(MC + "diamond_pickaxe")], "Diamond Pickaxe", deps=["hv_iron"], xp=60,
      subtitle="Hard is not tough", desc=[
        "&eWhat:&r the vanilla road to diamond tier: obsidian, crying obsidian and ancient debris. Also the base for Mystical Agriculture tools.",
        "&eChemistry:&r diamond is carbon with every atom bonded to four neighbours in a 3D network (sp³). It's Mohs 10, the hardest natural material, but it cleaves along flat planes: a sharp knock in the right direction splits it.",
        "&eHow:&r three diamonds and two sticks.",
        "&eTip:&r a steel paxel (T1) is already diamond tier. Spend early diamonds on machines, not picks, if you're short."]),
    Q("hv_diamond_cousins", 10, -2, [anyof([MT + "steel_pickaxe", MT + "refined_glowstone_pickaxe", MT + "refined_glowstone_paxel",
                                            "justdirethings:blazegold_pickaxe", "justdirethings:celestigem_pickaxe",
                                            "twilightforest:steeleaf_pickaxe", "twilightforest:knightmetal_pickaxe",
                                            "undergarden:utherium_pickaxe", MI + "steam_mining_drill"])],
      "Diamond-Tier Cousins", deps=["hv_steel"], xp=40, optional=True, tokens=1, subtitle="Optional: steel, glowstone, blazegold and more", desc=[
        "&eWhat:&r all of these are diamond tier: Mekanism steel and refined glowstone, JDT blazegold and celestigem, Twilight steeleaf and knightmetal, Undergarden utherium, and MI's Steam Mining Drill.",
        "&eChemistry:&r the Steam Mining Drill is honest engineering: a hardened bit turned by a steam engine. Real drill bits use tungsten carbide or industrial diamond tips on a tough steel body.",
        "&eHow:&r craft any one of them; each mod page and JEI have the recipe.",
        "&eTip:&r the steam drill burns fuel instead of wearing out, and digs 3x3. Its tooltip lists the modes."]),
    Q("hv_netherite_pick", 12, -4, [item(MC + "netherite_pickaxe")], "Netherite Pickaxe", deps=["hv_netherite", "hv_diamond_pick"], xp=80,
      subtitle="Upgrade, don't rebuild", desc=[
        "&eWhat:&r the vanilla netherite-tier pick. Upgrading keeps every enchantment on your diamond pick.",
        "&eHow:&r smithing table: netherite upgrade template + diamond pickaxe + netherite ingot.",
        "&eTip:&r netherite items float in lava and don't burn. Drop one in the Nether and it can be fished back out."]),
    Q("hv_netherite_cousins", 14, -4, [anyof([MT + "refined_obsidian_pickaxe", MT + "refined_obsidian_paxel", MT + "netherite_paxel",
                                              "justdirethings:eclipsealloy_pickaxe", "justdirethings:eclipsealloy_paxel",
                                              "twilightforest:fiery_pickaxe", MI + "diesel_mining_drill"])],
      "Netherite-Tier Cousins", deps=["hv_netherite"], xp=60, optional=True, tokens=1, subtitle="Optional: refined obsidian, eclipse, fiery", desc=[
        "&eWhat:&r all netherite tier: Mekanism refined obsidian and netherite paxel, JDT eclipse alloy, Twilight fiery, MI's Diesel Mining Drill. A Silent Gear pick with a crimson steel, azure electrum or tyrian steel head counts too (its tier comes from the head).",
        "&eChemistry:&r fiery metal is 'quenched' in fiery blood; real metallurgists do the same with oil, brine or polymer baths to control how fast the steel cools.",
        "&eHow:&r craft any one of the listed tools (check JEI).",
        "&eTip:&r the diesel drill is listed on the T5 page as part of Diesel Toys."]),
    Q("hv_ma_pick", 10, -4, [anyof(["mysticalagriculture:inferium_pickaxe", "mysticalagriculture:prudentium_pickaxe", "mysticalagriculture:tertium_pickaxe",
                                    "mysticalagriculture:imperium_pickaxe", "mysticalagriculture:supremium_pickaxe"])],
      "A Grown Pickaxe", deps=["hv_diamond_pick"], xp=40, optional=True, tokens=1, subtitle="Optional: Mystical Agriculture ignores tiers", desc=[
        "&eWhat:&r Mystical Agriculture tools have no 'can't mine' list: even an inferium pick breaks azure silver, naquadah and dreadrock.",
        "&eHow:&r a diamond pickaxe with two inferium ingots and two inferium gemstones around it (check JEI). Higher essences make it faster, not 'higher tier'.",
        "&eTip:&r it still can't give you the metal: the ores need the same chemistry lines as ever."]),
    Q("hv_gold_pick", 4, -2, [item(MC + "golden_pickaxe")], "Fast and Useless", deps=["hv_stone"], xp=15,
      optional=True, tokens=1, subtitle="Optional: the fastest, weakest pick", desc=[
        "&eWhat:&r a golden pick mines faster than any vanilla pick, but only at wood tier and with almost no durability.",
        "&eChemistry:&r gold is about Mohs 2.5-3: a fingernail nearly scratches it. Real gold is so soft it's alloyed with copper or silver for jewellery (18 carat is 75% gold).",
        "&eHow:&r three gold ingots and two sticks.",
        "&eTip:&r enchant it with Silk Touch and it's a quick glass and ice collector."]),

    # --- armour by strength (y=2) --------------------------------------------------------------
    Q("hv_bronze_armor", 4, 2, vset("bronze", MT), "Bronze Armour", deps=["hv_bronze"], xp=40, optional=True, tokens=1,
      subtitle="Optional: a little better than iron", desc=[
        "&eWhat:&r Mekanism Tools bronze armour is a touch better than iron, and it saves your iron for machines.",
        "&eChemistry:&r Bronze Age armour really was bronze, often hammered cold: working the metal (work hardening) piles up dislocations and makes it harder still.",
        "&eHow:&r 24 bronze ingots, shaped like any armour set. MI bronze counts (it's a c:ingots/bronze ingot)."]),
    Q("hv_steel_armor", 8, 4, vset("steel", MT), "Steel Armour", deps=["hv_steel"], xp=60, optional=True, tokens=1,
      subtitle="Optional: plate for the steel age", desc=[
        "&eWhat:&r Mekanism Tools steel armour: better than iron, from the steel you already make in MI.",
        "&eChemistry:&r real plate armour was hardened on the outside and left soft inside (case hardening): a hard face to stop blades, a tough core so it dents instead of cracking.",
        "&eHow:&r 24 steel ingots, shaped like any armour set (any c:ingots/steel counts)."]),
    Q("hv_diamond_armor", 8, 2, vset("diamond"), "Diamond Armour", deps=["hv_iron"], xp=80,
      subtitle="Four pieces of the hardest gem", desc=[
        "&eWhat:&r the full vanilla diamond set: the step before netherite, and the base you'll upgrade.",
        "&eChemistry:&r real diamond armour would be a disaster: diamond is hard but brittle, and a solid plate would crack on the first heavy blow. Real body armour stacks hard ceramic plates (boron carbide, B₄C) on tough fibres.",
        "&eHow:&r 24 diamonds. If that hurts, make the steel set first and come back."]),
    Q("hv_netherite_armor", 12, 2, vset("netherite"), "Netherite Armour", deps=["hv_netherite", "hv_diamond_armor"], xp=150,
      subtitle="Upgrade the diamond set", desc=[
        "&6Your skin is mortal now, so you wear the strongest shell the world allows. You remember not needing one.&r",
        "&eWhat:&r the full vanilla netherite set: the best plain armour, with knockback resistance and immunity to burning up in lava as an item.",
        "&eHow:&r smithing table, one piece at a time: template + diamond piece + netherite ingot. Four templates, four ingots.",
        "&eTip:&r copy templates with diamonds and netherrack so you never run out."]),
    Q("hv_bastion", 10, 4, [structure("minecraft:bastion_remnant")], "Bastion Remnant", deps=["hv_netherite"], xp=80,
      optional=True, tokens=1, subtitle="Optional: where the templates come from", desc=[
        "&eWhat:&r every bastion has a netherite upgrade template in its chests, often gold blocks and ancient debris too.",
        "&eHow:&r find a bastion in the Nether (anywhere except basalt deltas) and step inside.",
        "&eTip:&r piglin brutes don't care about gold armour. Bring a shield and a bow."]),

    # --- material science side quests (y=4) ----------------------------------------------------
    Q("hv_opt_mohs", 2, 6, [item(MC + "calcite"), item("chemlib:calcium_sulfate"), item("mekanism:fluorite_gem"), item("chemlib:hydroxylapatite"),
                            item(MC + "quartz"), item("chemlib:aluminum_oxide"), item(MC + "diamond")],
      "The Scratch Test", deps=["hv_iron"], xp=100, optional=True, tokens=2, subtitle="Optional: seven of Mohs' ten minerals", desc=[
        "&eWhat:&r in 1812 Friedrich Mohs ranked ten minerals by which scratches which. Seven of them exist here.",
        "&eChemistry:&r gypsum CaSO₄·2H₂O (2), calcite CaCO₃ (3), fluorite CaF₂ (4), apatite Ca₅(PO₄)₃(OH) (5), quartz SiO₂ (7), corundum Al₂O₃ (9), diamond C (10). Talc (1), orthoclase (6) and topaz (8) are missing.",
        "&eHow:&r calcite in dripstone caves and amethyst geodes; fluorite from Mekanism ore; nether quartz; diamond. Calcium sulfate, hydroxylapatite and aluminium oxide come from the Alchemistry machines (check JEI).",
        "{@pagebreak}",
        "&eChemistry:&r the scale only ranks, it doesn't measure. Diamond (10) is about four times harder than corundum (9), while corundum is only a bit harder than topaz (8).",
        "&eTip:&r a fingernail is about 2.5, a copper coin 3.5, a steel knife 5.5, window glass 5.5. That's the field geologist's whole kit."]),
    Q("hv_opt_ore_hardness", 4, 6, [tick()], "Hard Rock, Soft Ore", deps=["hv_opt_mohs"], xp=30, optional=True, tokens=1,
      subtitle="Optional: why game tiers don't follow Mohs", desc=[
        "&eWhat:&r the ores you mine have real hardnesses, and they don't line up with the game's tiers at all.",
        "&eChemistry:&r galena (PbS, lead ore) 2.5; bauxite 1-3; fluorite 4; wolframite 4-4.5; uraninite (UO₂) 5-6; ilmenite 5-6; cassiterite (SnO₂) 6-7; sperrylite (PtAs₂) 6-7. Tin ore is harder than iron ore, yet the game puts it lower.",
        "&eHow:&r read it, then click the check.",
        "&eTip:&r real miners don't pick ore apart by hand: they blast the rock and crush it, then separate by density and froth flotation."]),
    Q("hv_opt_emerald", 6, 4, [item(MC + "emerald", 4)], "Green Beryl", deps=["hv_iron"], xp=30, optional=True, tokens=1,
      subtitle="Optional: an iron-tier gem", desc=[
        "&eWhat:&r emerald ore is iron tier; in the Overworld it only appears in mountain biomes.",
        "&eChemistry:&r emerald is beryl, Be₃Al₂Si₆O₁₈, Mohs 7.5-8, coloured green by a trace of chromium or vanadium. Pure beryl is colourless; iron makes it blue (aquamarine).",
        "&eHow:&r mine 4 emeralds with an iron pick, or trade with villagers.",
        "&eTip:&r beryllium from beryl makes copper-beryllium alloy: hard, and it doesn't spark, so it's used for tools near explosives."]),
    Q("hv_opt_carbide", 10, 6, [item(MI + "tungsten_dust", 2)], "Tungsten Carbide", deps=["hv_hard_ores"], xp=60, optional=True, tokens=1,
      subtitle="Optional: the real super-hard tool", desc=[
        "&eWhat:&r the real material that nearly every drill bit and cutting insert on Earth is made of.",
        "&eChemistry:&r heat tungsten powder with carbon at 1400-2000 °C: W + C → WC. Tungsten carbide is about Mohs 9 and keeps its hardness when red hot. Pressed with 6-12% cobalt as a binder it becomes 'cemented carbide', hard and tough at once.",
        "&eHow:&r macerate raw tungsten into 2 tungsten dust.",
        "&eTip:&r tungsten carbide is about twice as dense as steel. Pick up a carbide drill bit and it feels wrong."]),

    # --- weapons and the rest of the armour (ATM10-aligned round, 2026-10-19) --------------------
    Q("hv_opt_wood_set", 0, 0, [item(MC + "wooden_sword"), item(MC + "wooden_axe"), item(MC + "wooden_shovel")], "Wooden Tools",
      deps=["hv_intro"], xp=10, optional=True, tokens=1, subtitle="Optional: the oldest composite you own", desc=[
        "&eWhat:&r the full wooden set: weak, cheap, and a fine fuel once it wears out.",
        "&eChemistry:&r wood is a natural composite: long cellulose fibres, (C₆H₁₀O₅)ₙ chains of glucose, glued together by lignin. It's strong along the grain and splits easily across it.",
        "&eHow:&r planks and sticks, shaped like any tool.",
        "&eTip:&r a broken wooden tool burns in a furnace for as long as a plank. Nothing goes to waste."]),
    Q("hv_gold_sword", 0, 0, [item(MC + "gold_ingot", 8), item(MC + "golden_sword")], "Soft Gold", deps=["hv_iron"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a ceremonial blade", desc=[
        "&eWhat:&r a golden sword hits about as hard as a wooden one and wears out faster. Piglins like it, though.",
        "&eChemistry:&r gold is the most malleable metal: one gram can be beaten into a leaf about a square metre wide and a few hundred atoms thick. Great for leaf, useless for an edge.",
        "&eHow:&r smelt 8 gold ingots from raw gold (needs an iron-tier pick), then craft the sword.",
        "&eTip:&r wearing one piece of gold armour keeps most piglins calm in the Nether."]),
    Q("hv_diamond_kit", 0, 0, [item(MC + "diamond_sword"), item(MC + "diamond_shovel")], "Diamond Sword and Shovel", deps=["hv_diamond_pick"], xp=40,
      optional=True, tokens=1, subtitle="Optional: rounding out the diamond kit", desc=[
        "&eWhat:&r the diamond sword is the vanilla weapon to beat until netherite; the shovel digs sand and gravel at speed.",
        "&eChemistry:&r real diamond blades exist: diamond scalpels cut with an edge only a few nanometres wide. They're kept for eye surgery because one sideways knock can chip them.",
        "&eHow:&r two diamonds and a stick for the sword, one diamond and two sticks for the shovel.",
        "&eTip:&r enchant before you upgrade to netherite: the enchantments carry over."]),
    Q("hv_netherite_sword", 0, 0, [item(MC + "netherite_sword")], "Netherite Sword", deps=["hv_netherite", "hv_diamond_kit"], xp=60,
      optional=True, tokens=1, subtitle="Optional: upgrade the blade too", desc=[
        "&eWhat:&r the strongest vanilla sword, and it can't burn up in lava.",
        "&eHow:&r smithing table: netherite upgrade template + diamond sword + netherite ingot.",
        "&eTip:&r copy a template with 7 diamonds and a netherrack first, so the sword doesn't cost your last one."]),
    Q("hv_mek_swords", 0, 0, [anyof([MT + "bronze_sword", MT + "lapis_lazuli_sword", MT + "osmium_sword", MT + "steel_sword",
                                     MT + "refined_glowstone_sword", MT + "refined_obsidian_sword"])],
      "Mekanism Blades", deps=["hv_bronze"], xp=30, optional=True, tokens=1, subtitle="Optional: a sword from your own alloys", desc=[
        "&eWhat:&r Mekanism Tools makes a sword in every one of its metals: bronze, lapis, osmium, steel, refined glowstone and refined obsidian. Any one counts.",
        "&eChemistry:&r a good sword is a compromise. Hard steel keeps an edge; soft steel bends instead of snapping. Japanese smiths welded both into one blade and quenched it with clay on the spine.",
        "&eHow:&r two ingots (or gems) of the metal and a stick, like any sword (check JEI).",
        "&eTip:&r refined obsidian is the best of the set; steel is the cheapest one worth carrying."]),
    Q("hv_lapis_armor", 0, 0, vset("lapis_lazuli", MT), "Lapis Armour", deps=["hv_lapis_tools"], xp=30, optional=True, tokens=1,
      subtitle="Optional: blue and very enchantable", desc=[
        "&eWhat:&r Mekanism Tools lapis armour protects about as well as chainmail but takes enchantments very well.",
        "&eChemistry:&r the blue of lapis is the S₃⁻ radical ion caged in lazurite. Grind it, wash out the grey minerals, and you have ultramarine pigment.",
        "&eHow:&r 24 lapis lazuli, shaped like any armour set (check JEI).",
        "&eTip:&r a cheap set to practise enchanting on while your diamonds go into machines."]),
    Q("hv_leather_set", 0, 0, [item(MC + "leather_helmet"), item(MC + "leather_leggings")], "A Full Leather Set", deps=["gs_leather"], xp=15,
      optional=True, tokens=1, subtitle="Optional: cap and trousers to match", desc=[
        "&eWhat:&r the helmet and leggings that finish the leather set from Getting Started. Leather can be dyed any colour.",
        "&eChemistry:&r leather is tanned hide: tannins (plant polyphenols) or chromium(III) salts cross-link the collagen protein chains, so the skin stops rotting and stays flexible.",
        "&eHow:&r 5 leather for the cap, 7 for the leggings. Craft a piece with dye to colour it; a water cauldron washes the dye out.",
        "&eTip:&r leather boots let you walk on powder snow without sinking."]),
    Q("hv_wolf_armor", 0, 0, [item(MC + "wolf_armor"), item(MC + "armadillo_scute", 2)], "Armour for a Friend", deps=["hv_leather_set"], xp=30,
      optional=True, tokens=1, subtitle="Optional: armadillo scutes for your wolf", desc=[
        "&eWhat:&r wolf armour soaks up damage for a tamed wolf. When it cracks, repair it with scutes.",
        "&eChemistry:&r scutes are keratin plates, the same protein as hair, horn and nails. Disulfide (S–S) bridges between the chains make keratin tough; that's also why burning hair smells of sulfur.",
        "&eHow:&r brush an armadillo (savanna and badlands) with a brush for scutes. 6 scutes make the armour; keep 2 for repairs.",
        "&eTip:&r right-click a tamed wolf with the armour to put it on. Dye it if you like."]),
    Q("hv_horse_armor", 0, 0, [anyof([MC + "leather_horse_armor", MC + "iron_horse_armor", MC + "golden_horse_armor", MC + "diamond_horse_armor"])],
      "Barding", deps=["hv_leather_set"], xp=20, optional=True, tokens=1, subtitle="Optional: armour for your horse", desc=[
        "&eWhat:&r horse armour, any kind. Leather horse armour can be crafted and dyed; iron, gold and diamond only turn up in chests.",
        "&eHow:&r 7 leather for the leather one, or loot dungeons, temples, villages and Ancient Cities for the metal ones.",
        "&eTip:&r Farmer's Delight Horse Feed heals a horse and speeds it up (Farming page)."]),
], links=[("gs_stone", 2, -6), ("gs_ironpick", 6, -6), ("gs_paxel", 6, -8), ("gs_silent", 8, -8), ("gs_opt_paxels", 4, -8),
          ("gs_leather", 2, 4), ("gs_armor", 6, 2), ("gs_opt_chain", 6, 6), ("gs_opt_gold", 4, 4),
          ("t0_opt_paxel", 4, -4), ("t0_opt_drill", 10, -6), ("t1_steel_paxel", 8, -6), ("t2_obsidian", 8, 6), ("t2_debris", 10, 2),
          ("t5_opt_tools", 14, -6), ("t7_desh", 16, 2),
          ("tc_osmium_paxel", 6, -4), ("tc_obsidian_paxel", 12, -6), ("tc_disassembler", 18, -2), ("tc_azure", 14, -2),
          ("mk2_armor_osmium", 12, 4), ("mk2_armor_obsidian", 14, 4), ("mk2_mekatool", 18, -4), ("mk2_mekasuit_full", 18, 2),
          ("jdt_tools_t1", 6, -10), ("jdt_tools_t4", 14, -8),
          ("tf_ironwood_gear", 8, -10), ("tf_knight_gear", 10, -8), ("tf_fiery_gear", 16, -6),
          ("ug_forgotten_tools", 14, -2), ("ug_utherium_gear", 16, 4), ("dd_warden_tools", 18, -6),
          ("w_ostrum", 18, 4), ("sp_calorite", 20, 4), ("cp_trims_overworld", 14, 6)])
