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
MA = "mysticalagriculture:"
TF = "twilightforest:"
UG = "undergarden:"
ATM = "allthemodium:"
# ATM10 mirror (2026-10-20, user decision): this page follows ATM10's "basic_armor" chapter quest for quest where we
# have the mod: a row of armour sets, the smithing table as the hub, armour trims and the trim materials. Its item
# list, order and shape only; every word is ours. The harvest-tier line (hv_intro ... hv_all) stays as side content.
SETS, TRIMS, MATS = "Armour Sets", "Armour Trims", "Trim Materials"


def vset(metal, ns=MC):
    return [item(f"{ns}{metal}_{p}") for p in ("helmet", "chestplate", "leggings", "boots")]


def aset(key, ids, title, subtitle, what, how, mirror, xp=30, optional=True, size=None, tip=None):
    """A full armour set (four pieces)."""
    desc = ["&eWhat:&r " + what, "&eHow:&r " + how]
    if tip:
        desc.append("&eTip:&r " + tip)
    else:
        desc.append("&eTip:&r a full set beats mixed pieces only when the set has a bonus; check the tooltips.")
    return Q(key, 0, 0, [i if isinstance(i, tuple) else item(i) for i in ids], title, deps=[], xp=xp, optional=optional, size=size,
             subtitle=("Optional: " if optional else "") + subtitle, section=SETS, mirror=mirror, desc=desc)


def trim(key, name, where, mirror):
    """One armour trim smithing template (found, then copied)."""
    return Q(key, 0, 0, [item(f"{MC}{name}_armor_trim_smithing_template")], name.capitalize() + " Trim", deps=[], xp=25,
             optional=True, subtitle="Optional: found in " + where, section=TRIMS, mirror=mirror, desc=[
                 f"&eWhat:&r a template that paints the {name} pattern onto any armour piece at a smithing table.",
                 f"&eHow:&r loot it from {where}. Once you have one, 7 diamonds and the template's base block copy it (check JEI).",
                 "&eTip:&r the pattern's colour comes from the material you add: a vanilla ingot or gem, as listed under Trim Materials."])


def mat(key, id_, title, chem, mirror, optional=False, xp=10):
    """A trim material: an ingot, gem or crystal that colours a trim."""
    return Q(key, 0, 0, [item(id_)], title, deps=[], xp=xp, optional=optional,
             subtitle=("Optional: " if optional else "") + "for the collection", section=MATS, mirror=mirror, desc=[
                 "&eWhat:&r a material for the collection. Vanilla ingots and gems colour armour trims; some modded ones do too (try it at a smithing table).",
                 "&eChemistry:&r " + chem,
                 "&eHow:&r keep one in your inventory. At a smithing table: trim template + armour piece + material."])


CHAPTER = Chapter("harvest", "Armour and Harvest Tiers", "minecraft:diamond_chestplate",
        ["Every armour set in the pack, trims and their materials, and which pickaxe mines what."], SIDE, [
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
    Q("hv_gold_pick", 4, -2, [tick()], "Fast and Useless", deps=['hv_stone'], optional=True, tokens=0, xp=0, icon="minecraft:golden_pickaxe", subtitle="Moved: see Golden Pickaxe", desc=["&eMoved:&r this step is now \"Golden Pickaxe\" on the Gear and Comfort page. Click to dismiss."]),

    # --- armour by strength (y=2) --------------------------------------------------------------
    Q("hv_bronze_armor", 4, 2, vset("bronze", MT), "Bronze Armour", deps=["hv_bronze"], xp=40, section=SETS, mirror="7B500E0577BDFF8F", optional=True, tokens=1,
      subtitle="Optional: a little better than iron", desc=[
        "&eWhat:&r Mekanism Tools bronze armour is a touch better than iron, and it saves your iron for machines.",
        "&eChemistry:&r Bronze Age armour really was bronze, often hammered cold: working the metal (work hardening) piles up dislocations and makes it harder still.",
        "&eHow:&r 24 bronze ingots, shaped like any armour set. MI bronze counts (it's a c:ingots/bronze ingot)."]),
    Q("hv_steel_armor", 8, 4, vset("steel", MT), "Steel Armour", deps=["hv_steel"], xp=60, section=SETS, mirror="3ABE7074E500494D", optional=True, tokens=1,
      subtitle="Optional: plate for the steel age", desc=[
        "&eWhat:&r Mekanism Tools steel armour: better than iron, from the steel you already make in MI.",
        "&eChemistry:&r real plate armour was hardened on the outside and left soft inside (case hardening): a hard face to stop blades, a tough core so it dents instead of cracking.",
        "&eHow:&r 24 steel ingots, shaped like any armour set (any c:ingots/steel counts)."]),
    Q("hv_diamond_armor", 8, 2, vset("diamond"), "Diamond Armour", optional=True, deps=["hv_iron"], xp=80, size=1.5, section=SETS, mirror="5DDC15AAFD2CAF47",
      subtitle="Four pieces of the hardest gem", desc=[
        "&eWhat:&r the full vanilla diamond set: the step before netherite, and the base you'll upgrade.",
        "&eChemistry:&r real diamond armour would be a disaster: diamond is hard but brittle, and a solid plate would crack on the first heavy blow. Real body armour stacks hard ceramic plates (boron carbide, B₄C) on tough fibres.",
        "&eHow:&r 24 diamonds. If that hurts, make the steel set first and come back."]),
    Q("hv_netherite_armor", 12, 2, vset("netherite"), "Netherite Armour", optional=True, deps=["hv_netherite", "hv_diamond_armor"], xp=150, size=1.5, section=SETS, mirror="074EC1E636CD6605",
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
    Q("hv_opt_emerald", 6, 4, [tick()], "Green Beryl", deps=['hv_iron'], optional=True, tokens=0, xp=0, icon="minecraft:emerald", subtitle="Moved: see Emerald", desc=["&eMoved:&r this step is now \"Emerald\" on this page. Click to dismiss."]),
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
    Q("hv_netherite_sword", 0, 0, [tick()], "Netherite Sword", deps=['hv_netherite', 'hv_diamond_kit'], optional=True, tokens=0, xp=0, icon="minecraft:netherite_sword", subtitle="Moved: see Netherite Sword", desc=["&eMoved:&r this step is now \"Netherite Sword\" on the Gear and Comfort page. Click to dismiss."]),
    Q("hv_mek_swords", 0, 0, [anyof([MT + "bronze_sword", MT + "lapis_lazuli_sword", MT + "osmium_sword", MT + "steel_sword",
                                     MT + "refined_glowstone_sword", MT + "refined_obsidian_sword"])],
      "Mekanism Blades", deps=["hv_bronze"], xp=30, optional=True, tokens=1, subtitle="Optional: a sword from your own alloys", desc=[
        "&eWhat:&r Mekanism Tools makes a sword in every one of its metals: bronze, lapis, osmium, steel, refined glowstone and refined obsidian. Any one counts.",
        "&eChemistry:&r a good sword is a compromise. Hard steel keeps an edge; soft steel bends instead of snapping. Japanese smiths welded both into one blade and quenched it with clay on the spine.",
        "&eHow:&r two ingots (or gems) of the metal and a stick, like any sword (check JEI).",
        "&eTip:&r refined obsidian is the best of the set; steel is the cheapest one worth carrying."]),
    Q("hv_lapis_armor", 0, 0, vset("lapis_lazuli", MT), "Lapis Armour", deps=["hv_lapis_tools"], xp=30, section=SETS, mirror="65A529C8238E89F1", optional=True, tokens=1,
      subtitle="Optional: blue and very enchantable", desc=[
        "&eWhat:&r Mekanism Tools lapis armour protects about as well as chainmail but takes enchantments very well.",
        "&eChemistry:&r the blue of lapis is the S₃⁻ radical ion caged in lazurite. Grind it, wash out the grey minerals, and you have ultramarine pigment.",
        "&eHow:&r 24 lapis lazuli, shaped like any armour set (check JEI).",
        "&eTip:&r a cheap set to practise enchanting on while your diamonds go into machines."]),
    Q("hv_leather_set", 0, 0, vset("leather"), "A Full Leather Set", deps=["gs_leather"], xp=15, size=1.5, section=SETS, mirror="28408BFAA54E4FC6",
      optional=True, tokens=1, subtitle="Optional: all four pieces, dyed if you like", desc=[
        "&eWhat:&r the whole leather set: cap, tunic, trousers and boots. Getting Started asked for two of them; this is all four. Leather can be dyed any colour.",
        "&eChemistry:&r leather is tanned hide: tannins (plant polyphenols) or chromium(III) salts cross-link the collagen protein chains, so the skin stops rotting and stays flexible.",
        "&eHow:&r 24 leather for the set (5, 8, 7 and 4). Craft a piece with dye to colour it; a water cauldron washes the dye out.",
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

    # ===== ATM10 mirror: basic_armor (2026-10-20) ==========================================================
    # --- the hub (moved here from tools.py; key unchanged) ---------------------------------------------------
    Q("gs_opt_smithing", 0, 0, [item("minecraft:smithing_table")], "Smithing Table", subtitle="Upgrades without starting over",
      deps=["gs_iron"], xp=25, size=2.0, shape="gear", section=SETS, mirror="7F11ABFB2E21B7E4", loot="pick_early", desc=[
        "&6You remember armour that reshaped itself to fit. A smithing table is the mortal answer: upgrade, don't start over.&r",
        "&eWhat:&r the smithing table upgrades tools and armour in place (diamond to netherite) and paints armour trims. Every set on this page meets it sooner or later.",
        "&eHow:&r 2 iron ingots over 4 planks.",
        "&eTip:&r Apotheosis adds smithing recipes too, such as upgrading chainmail to iron (check JEI)."]),

    # --- vanilla sets (the milestones along the top row) ------------------------------------------------------
    aset("hv_chain_set", [MC + "chainmail_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Chainmail", "rings, not plates",
         "the chainmail set sits between leather and iron, and it can't be crafted in vanilla.",
         "trade with an armourer villager, or loot it from mobs that spawn wearing it (check JEI for any pack recipe).",
         "004D61425172324F", size=1.5,
         tip="real mail is thousands of riveted iron rings: flexible, and hard to cut, but a blunt blow goes straight through."),
    aset("hv_gold_set", vset("golden"), "Golden Armour", "shiny and soft",
         "weak armour that piglins respect: wear one piece and most of them leave you alone.",
         "24 gold ingots, shaped like any armour set.", "17A68C4E9E9EA2B7", size=1.5,
         tip="gold armour enchants better than any other vanilla set."),
    aset("hv_iron_set", vset("iron"), "Iron Armour", "the first real protection",
         "the full iron set: the armour you'll wear for the first chapters.", "24 iron ingots, shaped like any armour set.",
         "497D222F74A52DF5", xp=30, optional=True, size=1.5,
         tip="iron armour plus a shield handles nearly everything in the Overworld at night."),
    aset("hv_atm_set", vset("allthemodium", ATM), "Allthemodium Armour", "the first of the deep metals",
         "Allthemodium's first armour set, from the metal of the deepest layers.", "see the Allthemodium page (smithing template plus ingots).",
         "6C5F9D0D447EFB9C", xp=100, optional=True, size=1.5),
    aset("hv_vib_set", vset("vibranium", ATM), "Vibranium Armour", "the second of the deep metals",
         "the Nether's deep metal as armour.", "see the Allthemodium page.", "72DDA413D73E3235", xp=150, optional=True, size=1.5),
    aset("hv_unob_set", vset("unobtainium", ATM), "Unobtainium Armour", "the last of the deep metals",
         "the End's deep metal as armour, the top of that family.", "see the Allthemodium page.", "6F76DA3BBAE8337B", xp=200, optional=True, size=1.5,
         tip="each deep-metal set upgrades the one before at a smithing table."),
    aset("hv_quantum_mi", [MI + "quantum_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Quantum Armour", "Modern Industrialization's last word",
         "MI's quantum armour, made from netherite pieces and quantum upgrades in the Packer.",
         "netherite piece + quantum upgrade in an MI Packer, four times (check JEI).", "3403D7502F7BC897", xp=300, size=1.5,
         tip="the quantum upgrade sits at the very end of the MI chain. Wear it as a trophy."),
    aset("hv_mekasuit", ["mekanism:mekasuit_helmet", "mekanism:mekasuit_bodyarmor", "mekanism:mekasuit_pants", "mekanism:mekasuit_boots"], "The Full MekaSuit", "all four pieces",
         "the complete MekaSuit: modular power armour from Mekanism.", "see the MekaSuit quest on the Gear page and JEI; modules go in at the Modification Station.",
         "1C27C74722A19FC1", xp=300, size=1.5),
    aset("hv_aae_quantum", ["advanced_ae:quantum_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Quantum Armour (AE2)", "Advanced AE's armour",
         "Advanced AE's quantum set: netherite armour wired into your ME network, with its own modules.",
         "quantum alloy plates, quantum processors and netherite armour (check JEI).", "34D14B807A2DAC0F", xp=300, size=1.5),

    # --- magic sets ----------------------------------------------------------------------------------------------
    aset("hv_ars_fire", ["ars_elemental:fire_" + p for p in ("hat", "robes", "leggings", "boots")], "Fire Mage Set", "Ars Elemental",
         "Ars Elemental's fire armour: a mage set that boosts fire spells.", "check the Ars page and JEI (it starts from the Ars mage armour).", "79D3055DE0EEA6B0", xp=50),
    aset("hv_ars_air", ["ars_elemental:air_" + p for p in ("hat", "robes", "leggings", "boots")], "Air Mage Set", "Ars Elemental",
         "Ars Elemental's air armour, for wind spells.", "check the Ars page and JEI.", "7C1D407CF67786F6", xp=50),
    aset("hv_ars_earth", ["ars_elemental:earth_" + p for p in ("hat", "robes", "leggings", "boots")], "Earth Mage Set", "Ars Elemental",
         "Ars Elemental's earth armour, for stone and plant spells.", "check the Ars page and JEI.", "2E0F82F7E1B74033", xp=50),
    aset("hv_ars_aqua", ["ars_elemental:aqua_" + p for p in ("hat", "robes", "leggings", "boots")], "Water Mage Set", "Ars Elemental",
         "Ars Elemental's water armour, for water spells.", "check the Ars page and JEI.", "2EAA6BE598C83F24", xp=50),
    aset("hv_ars_sorcerer", ["ars_nouveau:sorcerer_" + p for p in ("hood", "robes", "leggings", "boots")], "Sorcerer Set", "Ars Nouveau",
         "the Ars Nouveau sorcerer set: mana and regeneration first.", "the Ars page covers the mage armour recipes (check JEI).", "19F58E291A543228", xp=40),
    aset("hv_ars_arcanist", ["ars_nouveau:arcanist_" + p for p in ("hood", "robes", "leggings", "boots")], "Arcanist Set", "Ars Nouveau",
         "the Ars Nouveau arcanist set: a mage set with its own threads.", "check the Ars page and JEI.", "0ABB2264CBB82470", xp=40),
    aset("hv_ars_battlemage", ["ars_nouveau:battlemage_" + p for p in ("hood", "robes", "leggings", "boots")], "Battlemage Set", "Ars Nouveau",
         "the Ars Nouveau battlemage set: more protection, less mana.", "check the Ars page and JEI.", "0E2515424291BB59", xp=40),

    # --- tech and dimension sets ---------------------------------------------------------------------------------
    aset("hv_warden_set", ["deeperdarker:warden_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Warden Armour", "from the Otherside",
         "Deeper and Darker's warden set, upgraded from netherite.", "warden carapace at a smithing table (see the Deeper and Darker page).", "15978093237448FE", xp=150),
    aset("hv_ferricore_set", ["justdirethings:ferricore_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Ferricore Armour", "goo-made iron",
         "Just Dire Things' first armour, with abilities you toggle.", "ferricore ingots (see the Just Dire Things page).", "10AA2B20D86747F7", xp=40),
    aset("hv_blazegold_set", ["justdirethings:blazegold_" + p for p in ("helmet", "chestplate", "leggings", "boots")], "Blazegold Armour", "goo-made gold",
         "Just Dire Things' fire-touched set.", "blazegold ingots (see the Just Dire Things page).", "1A8440C0048EEB02", xp=50),
    aset("hv_osmium_set", vset("osmium", MT), "Osmium Armour", "the densest metal, worn",
         "Mekanism Tools osmium armour: sturdier than iron.", "24 osmium ingots (check JEI).", "71C552678A0F649F", xp=40,
         tip="real osmium is too brittle and toxic (its oxide, OsO₄, is volatile) to wear. Mekanism is kinder."),
    aset("hv_glowstone_set", vset("refined_glowstone", MT), "Refined Glowstone Armour", "light and quick",
         "Mekanism Tools refined glowstone armour.", "refined glowstone ingots from the Osmium Compressor (check JEI).", "5865951E4F81C91F", xp=50),
    aset("hv_obsidian_set", vset("refined_obsidian", MT), "Refined Obsidian Armour", "Mekanism's strongest plate",
         "the best Mekanism Tools armour.", "refined obsidian ingots (check JEI).", "7FABB77A60E7962C", xp=80),
    aset("hv_ma_inferium", vset("inferium", MA), "Inferium Armour", "essence armour, tier 1",
         "the first Mystical Agriculture set.", "a diamond set with inferium ingots and gemstones (see the Mystical Agriculture page).", "13517D17E6BF015F", xp=40),
    aset("hv_ma_prudentium", vset("prudentium", MA), "Prudentium Armour", "essence armour, tier 2",
         "the second essence set; augment slots start here.", "upgrade the inferium set (check JEI).", "52B61FB01D7C12A4", xp=50),
    aset("hv_ma_tertium", vset("tertium", MA), "Tertium Armour", "essence armour, tier 3",
         "the third essence set.", "upgrade the prudentium set (check JEI).", "2A4FE9644F3B9DC1", xp=60),
    aset("hv_ma_imperium", vset("imperium", MA), "Imperium Armour", "essence armour, tier 4",
         "the fourth essence set.", "upgrade the tertium set (check JEI).", "1D27EE427ECFD6CE", xp=80),
    aset("hv_ma_supremium", vset("supremium", MA), "Supremium Armour", "essence armour, tier 5",
         "the fifth essence set.", "upgrade the imperium set (check JEI).", "5064D5F99E2C69C8", xp=100),
    aset("hv_ma_awakened", vset("awakened_supremium", MA), "Awakened Supremium Armour", "essence armour, awakened",
         "the best essence set, with the most augment slots.", "upgrade the supremium set with awakened supremium (check JEI).", "4A9CB8778D37049F", xp=200),
    aset("hv_cloggrum_set", vset("cloggrum", UG), "Cloggrum Armour", "the Undergarden's iron",
         "the Undergarden's first armour.", "cloggrum ingots (check JEI).", "2FA0F5B348322095", xp=40),
    aset("hv_froststeel_set", vset("froststeel", UG), "Froststeel Armour", "cold metal",
         "froststeel armour from the Undergarden.", "froststeel ingots (check JEI).", "041ED280691BB05D", xp=50),
    aset("hv_utherium_set", vset("utherium", UG), "Utherium Armour", "crystal plate",
         "utherium armour, strongest against the Undergarden's rotspawn.", "utherium crystals (check JEI).", "2C387BFA6EE6FDB7", xp=60),
    aset("hv_ironwood_set", vset("ironwood", TF), "Ironwood Armour", "Twilight's first set",
         "ironwood armour from the Twilight Forest.", "ironwood ingots (see the Twilight Forest page).", "3215A3D706CECCEF", xp=40),
    aset("hv_steeleaf_set", vset("steeleaf", TF), "Steeleaf Armour", "leaves as hard as steel",
         "steeleaf armour from the Twilight Forest.", "steeleaf ingots (check JEI).", "30A61E1A1EFA81E6", xp=50),
    aset("hv_knightmetal_set", vset("knightmetal", TF), "Knightmetal Armour", "from the Knight Phantoms",
         "knightmetal armour, made from what the Goblin Knights and phantoms guard.", "knightmetal ingots (see the Twilight Forest page).", "6F335B4F3FD660E7", xp=60),
    aset("hv_fiery_set", vset("fiery", TF), "Fiery Armour", "quenched in fiery blood",
         "fiery armour: hot to the touch, and it sets attackers alight.", "fiery ingots (see the Twilight Forest page).", "3061B67330367CE2", xp=80),
    aset("hv_arctic_set", vset("arctic", TF), "Arctic Armour", "fur for the snow",
         "arctic fur armour, dyeable, from the Twilight Forest's snowy biomes.", "arctic fur (check JEI).", "1452D9CF827782B5", xp=40),
    aset("hv_yeti_set", vset("yeti", TF), "Yeti Armour", "the Alpha Yeti's coat",
         "yeti armour, from the Alpha Yeti's fur.", "alpha yeti fur (see the Twilight Forest page).", "52A29269A23F85B3", xp=60),

    # --- armour trims ---------------------------------------------------------------------------------------------
    trim("hv_trim_sentry", "sentry", "pillager outposts", "338BD467EBE6EE1F"),
    trim("hv_trim_vex", "vex", "woodland mansions", "1245126B4338C019"),
    trim("hv_trim_wild", "wild", "jungle temples", "243008D4DCD789D0"),
    trim("hv_trim_coast", "coast", "shipwrecks", "3AE0198177A8E91B"),
    trim("hv_trim_dune", "dune", "desert pyramids", "39796D8EE440F318"),
    trim("hv_trim_wayfinder", "wayfinder", "trail ruins (brush the suspicious gravel)", "62161BDE9AAAA4BF"),
    trim("hv_trim_raiser", "raiser", "trail ruins (brush the suspicious gravel)", "1E3E688B3B52C4D2"),
    trim("hv_trim_shaper", "shaper", "trail ruins (brush the suspicious gravel)", "1CC627D3FB348C89"),
    trim("hv_trim_host", "host", "trail ruins (brush the suspicious gravel)", "4B9C54DA5CB6D5C9"),
    trim("hv_trim_ward", "ward", "Ancient City chests", "65E733AACBE62EDB"),
    trim("hv_trim_silence", "silence", "Ancient City chests (rare)", "76CDF08465700AA2"),
    trim("hv_trim_tide", "tide", "elder guardians in ocean monuments", "66C21934DAFFAC7F"),
    trim("hv_trim_snout", "snout", "bastion remnants", "5C83D5CDD980FD9A"),
    trim("hv_trim_rib", "rib", "nether fortresses", "0F1D6F4729CC38F3"),
    trim("hv_trim_eye", "eye", "strongholds", "68DABFFB6B3E1A57"),
    trim("hv_trim_spire", "spire", "End city ships", "351159C55159C316"),
    trim("hv_trim_flow", "flow", "trial chamber ominous vaults", "3EA3A6414AB8A39C"),
    trim("hv_trim_bolt", "bolt", "trial chamber vaults", "729DCB919A92B735"),

    # --- trim materials ---------------------------------------------------------------------------------------------
    mat("hv_mat_redstone", MC + "redstone", "Redstone", "redstone stands in for cinnabar, HgS, the bright red mercury ore once ground into the pigment vermilion.", "1FC7ABEAB5018E79"),
    mat("hv_mat_lapis", MC + "lapis_lazuli", "Lapis Lazuli", "lapis gets its blue from S₃⁻ radical ions trapped in the mineral lazurite.", "3AA836E8EDB52097"),
    mat("hv_mat_iron", MC + "iron_ingot", "Iron Ingot", "iron (Fe) is the most-used metal on Earth by far; about 95% of all metal made is iron or steel.", "4DF683461225690F"),
    mat("hv_mat_gold", MC + "gold_ingot", "Gold Ingot", "gold (Au) stays bright because almost nothing oxidises it; only aqua regia and a few cyanide solutions dissolve it.", "3685B52446DEC809"),
    mat("hv_mat_copper", MC + "copper_ingot", "Copper Ingot", "copper (Cu) slowly turns green as its surface becomes basic copper carbonate and sulfate: the patina on old roofs.", "211FD55DEB635A98"),
    mat("hv_mat_emerald", MC + "emerald", "Emerald", "emerald is beryl, Be₃Al₂Si₆O₁₈, tinted green by traces of chromium or vanadium.", "1D91E37BFD8CC911"),
    mat("hv_mat_diamond", MC + "diamond", "Diamond", "diamond is carbon in a tetrahedral network; it burns in pure oxygen to CO₂ like any other carbon.", "6B671CB07D046BEC"),
    mat("hv_mat_netherite", MC + "netherite_ingot", "Netherite Ingot", "netherite is fictional: four scrap and four gold make an ingot, an alloy no real metallurgist would recognise.", "1EABF2E7AE7B8F22", xp=30),
    mat("hv_mat_quartz", MC + "quartz", "Nether Quartz", "quartz is SiO₂. Squeeze a quartz crystal and it makes a voltage (piezoelectricity); that's what keeps time in quartz watches.", "3FCEF8FF45E51608"),
    mat("hv_mat_amethyst", MC + "amethyst_shard", "Amethyst Shard", "amethyst is quartz, SiO₂, coloured purple by iron impurities and natural radiation.", "452DC5EB02D592B8"),
    mat("hv_mat_atm", ATM + "allthemodium_ingot", "Allthemodium Ingot", "allthemodium is fictional; the Allthemodium page covers where it comes from.", "5E7CCDE9229A646A", xp=50),
    mat("hv_mat_vib", ATM + "vibranium_ingot", "Vibranium Ingot", "vibranium is fiction borrowed from comics; here it's the Nether's deep metal.", "5A9C646718EE92C2", xp=75),
    mat("hv_mat_unob", ATM + "unobtainium_ingot", "Unobtainium Ingot", "'unobtainium' is an old engineers' joke for a material with perfect properties that doesn't exist.", "7279700A93E8630B", xp=100),
    mat("hv_mat_cloggrum", UG + "cloggrum_ingot", "Cloggrum Ingot", "cloggrum is the Undergarden's iron analogue: a soft, workable metal.", "788A7A2F1F438B64", optional=True),
    mat("hv_mat_froststeel", UG + "froststeel_ingot", "Froststeel Ingot", "froststeel is fictional; real 'cold' metals don't exist, but some alloys stay tough at cryogenic temperatures (austenitic stainless steel).", "16359196D49A6223", optional=True),
    mat("hv_mat_utherium", UG + "utherium_crystal", "Utherium Crystal", "utherium is a fictional crystal of the Undergarden's depths.", "690DB8BEF80617E5", optional=True),
    mat("hv_mat_regalium", UG + "regalium_crystal", "Regalium Crystal", "regalium is the Undergarden's gold analogue, a rare crystal.", "498483750C18FCD6", optional=True),
    mat("hv_mat_forgotten", UG + "forgotten_ingot", "Forgotten Ingot", "forgotten metal is the Undergarden's endgame material.", "5E6D7C1D7957DD4D", optional=True),
    mat("hv_mat_ironwood", TF + "ironwood_ingot", "Ironwood Ingot", "ironwood mixes iron with living wood; real 'ironwoods' are just very dense timbers that sink in water.", "055CCAE237DF3EEF", optional=True),
    mat("hv_mat_steeleaf", TF + "steeleaf_ingot", "Steeleaf Ingot", "steeleaf is fictional; real leaves are mostly water, cellulose and chlorophyll.", "140DF670162C68DA", optional=True),
    mat("hv_mat_knightmetal", TF + "knightmetal_ingot", "Knightmetal Ingot", "knightmetal comes from armour shards; real armourers did recycle broken plate the same way.", "7FBC64E6408D8D7F", optional=True),
    mat("hv_mat_naga", TF + "naga_scale", "Naga Scale", "real reptile scales are keratin, the protein of hair and nails.", "1D23F53C585185B7", optional=True),
    mat("hv_mat_carminite", TF + "carminite", "Carminite", "carminite is fictional. Real carmine red came from crushed cochineal insects (carminic acid).", "606775701551F3EE", optional=True),
    mat("hv_mat_fiery", TF + "fiery_ingot", "Fiery Ingot", "fiery metal is iron quenched in the blood of the Hydra; real quenching uses water, oil or brine.", "7F8B6D5F360D985A", optional=True),
], links=[("gs_stone", 2, -6), ("gs_ironpick", 6, -6), ("gs_paxel", 6, -8), ("gs_silent", 8, -8), ("gs_opt_paxels", 4, -8),
          ("gs_leather", 2, 4), ("gs_armor", 6, 2), ("gs_opt_chain", 6, 6), ("gs_opt_gold", 4, 4),
          ("t0_opt_paxel", 4, -4), ("t0_opt_drill", 10, -6), ("t1_steel_paxel", 8, -6), ("t2_obsidian", 8, 6), ("t2_debris", 10, 2),
          ("t5_opt_tools", 14, -6), ("t7_desh", 16, 2),
          ("tc_osmium_paxel", 6, -4), ("tc_obsidian_paxel", 12, -6), ("tc_disassembler", 18, -2), ("tc_azure", 14, -2),
          ("mk2_armor_osmium", 12, 4), ("mk2_armor_obsidian", 14, 4), ("mk2_mekatool", 18, -4), ("mk2_mekasuit_full", 18, 2),
          ("jdt_tools_t1", 6, -10), ("jdt_tools_t4", 14, -8),
          ("tf_ironwood_gear", 8, -10), ("tf_knight_gear", 10, -8), ("tf_fiery_gear", 16, -6),
          ("ug_forgotten_tools", 14, -2), ("ug_utherium_gear", 16, 4), ("dd_warden_tools", 18, -6),
          ("w_ostrum", 18, 4), ("sp_calorite", 20, 4), ("cp_trims_overworld", 14, 6)], mirror="basic_armor")
