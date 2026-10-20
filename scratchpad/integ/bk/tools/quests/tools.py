"""Quest chapter: tools. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

# ATM10 mirror (2026-10-20, user decision): this page follows ATM10's "basic_tools" chapter quest for quest where we
# have the mod: a hub, a short ore ladder, then one optional quest per pickaxe and per sword family. Only its item
# list, order and shape are used; every word here is ours. The older gear quests stay on the page as side quests.
LADDER, PICKS, SWORDS = "The Ore Ladder", "Pickaxes", "Blades"
MT, MA, JDT, UG, ATM = "mekanismtools:", "mysticalagriculture:", "justdirethings:", "undergarden:", "allthemodium:"


def col(key, ids, title, subtitle, what, how, tip, mirror, section, xp=20):
    """One optional collection quest off the hub: any one of `ids` counts."""
    task = item(ids[0]) if len(ids) == 1 else anyof(ids)
    return Q(key, 0, 0, [task], title, deps=["tc_hub"], xp=xp, optional=True, subtitle="Optional: " + subtitle,
             section=section, mirror=mirror, desc=["&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip])


def pick(key, ids, title, subtitle, what, how, tip, mirror, xp=20):
    return col(key, ids, title, subtitle, what, how, tip, mirror, PICKS, xp)


def sword(key, ids, title, subtitle, what, how, tip, mirror, xp=20):
    return col(key, ids, title, subtitle, what, how, tip, mirror, SWORDS, xp)


CHAPTER = Chapter("tools", "Gear and Comfort", "mekanismtools:osmium_paxel",
        ["Better tools from better materials, and a soft place to land."], SIDE, [
    # --- Silent Gear: core line (y=0) ---------------------------------------------------------
    Q("tc_sg_repair", 0, 0, [item("silentgear:crude_repair_kit")], "Repair Kits", deps=["gs_silent"], xp=25,
      subtitle="Mend your parts instead of throwing them away", desc=[
        "&6You remember tools that never wore out. These will, but you can mend them.&r",
        "&eWhat:&r Silent Gear tools don't break for good; at zero durability they just stop working until repaired.",
        "&eHow:&r craft a Crude Repair Kit, load it with matching material, then combine it with the tool in a crafting grid.",
        "&eTip:&r a better kit (Sturdy, then Crimson and Azure) holds more material and repairs more per use."]),
    Q("tc_blaze_gold", 2, 0, [item("silentgear:blaze_gold_ingot", 4)], "Blaze Gold", deps=["tc_sg_repair", "t2_nether"], xp=40,
      optional=True, tokens=1, subtitle="Optional: gold, fired with blaze powder", desc=[
        "&eWhat:&r Silent Gear's first magic alloy. It's a key ingredient of the Material Grader and the Starlight Charger.",
        "&eChemistry:&r gold (Au) is a noble metal: it barely reacts with anything, which is why it's found as native nuggets. Blaze gold is fictional; the blaze powder does the work.",
        "&eHow:&r gold ingot + 2 blaze powder in the Alloy Forge, or check JEI for the early crafting route.",
        "&eTip:&r keep a stack spare. Blaze gold blocks also go into the Starlight Charger."]),
    Q("tc_grader", 0, 0, [tick()], "Material Grader", deps=["tc_blaze_gold"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_salvager", 0, 0, [tick()], "Salvager", deps=["tc_grader"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),

    # --- Silent Gear: special metals (y=-2) ----------------------------------------------------
    Q("tc_crimson", 2, -2, [item("silentgear:crimson_iron_ingot", 8)], "Crimson Iron", deps=["tc_sg_repair", "t2_nether"], xp=50,
      subtitle="An ore that only grows in the Nether", desc=[
        "&eWhat:&r crimson iron ore generates in Nether biomes. It's the base of crimson steel and the Alloy Forge.",
        "&eHow:&r mine crimson iron ore in the Nether (Jade shows the name), then smelt the raw ore.",
        "&eTip:&r run a few through the Alchemistry Dissolver and see which real elements it gives back."]),
    Q("tc_crimson_steel", 4, -2, [item("silentgear:crimson_steel_ingot", 4)], "Crimson Steel", deps=["tc_crimson"], xp=60,
      subtitle="Crimson iron, blaze rods and magma cream", desc=[
        "&eWhat:&r a tough, heat-loving alloy for tool heads and the Alloy Forge frame.",
        "&eChemistry:&r real steel is iron with a little carbon (under about 2%); the carbon atoms jam the iron lattice so it can't slip. Crimson steel is the fictional cousin.",
        "&eHow:&r the first ingots are a shaped craft (crimson iron, blaze rods, magma cream); check JEI."]),
    Q("tc_alloy_forge", 6, -2, [item("silentgear:alloy_forge")], "The Alloy Forge", deps=["tc_crimson_steel"], xp=75,
      subtitle="Silent Gear's alloy machine", desc=[
        "&eWhat:&r mixes metals into Silent Gear alloys: blaze gold, crimson steel (3 per batch), azure electrum and tyrian steel.",
        "&eHow:&r crimson steel ingots, blackstone and an iron block (check JEI). Fuel it like a furnace.",
        "&eTip:&r alloying in the forge gives more ingots per batch than the crafting-table route."]),
    Q("tc_azure", 8, -2, [item("silentgear:azure_electrum_ingot", 4)], "Azure Electrum", deps=["tc_alloy_forge", "w_end"], xp=100,
      optional=True, tokens=1, subtitle="Optional: azure silver from the End, plus gold", desc=[
        "&eWhat:&r azure silver ore generates in the End. Alloyed with gold it becomes azure electrum, a fast, enchantable metal.",
        "&eChemistry:&r real electrum is a natural gold–silver alloy (Au–Ag); the ancient Lydians struck the first coins from it.",
        "&eHow:&r azure silver ore needs a netherite-tier pickaxe (netherite, refined obsidian, crimson steel or better; see the Harvest Tiers chapter). Then Alloy Forge: an azure silver block, 2 gold ingots and an ender pearl."]),
    Q("tc_tyrian", 10, -4, [item("silentgear:tyrian_steel_ingot", 4)], "Tyrian Steel", deps=["tc_azure"], xp=200,
      optional=True, tokens=2, subtitle="Optional: Silent Gear's finest metal", desc=[
        "&eWhat:&r the top Silent Gear alloy: crimson steel, azure electrum, crushed shulker shell and netherite scrap.",
        "&eChemistry:&r Tyrian purple was a real dye made from sea snails, once worth its weight in silver. The steel just borrowed the colour.",
        "&eHow:&r Alloy Forge (check JEI). Crush shulker shells first."]),

    # --- Mekanism paxels (y=2). The iron paxel (gs_paxel) moved here from Getting Started. Bronze and steel paxels are on the main path (t0_opt_paxel, t1_steel_paxel);
    #     harvest tiers are in the harvest chapter. -------------------------------------------------
    Q("gs_paxel", 0, 2, [item("mekanismtools:iron_paxel")], "The Paxel", subtitle="Pickaxe, axe and shovel in one", deps=["gs_irontools"], xp=25, desc=[
        "&eWhat:&r A &epaxel&r is a pickaxe, axe and shovel in one tool. Mekanism Tools adds them for every material, from wood to refined obsidian.",
        "&eHow:&r Craft an iron pickaxe, axe and shovel together with 2 sticks (check JEI).",
        "&eTip:&r One tool slot instead of three leaves more room for ore."]),
    Q("gs_opt_paxels", 0, 3.5, [item("mekanismtools:wood_paxel"), item("mekanismtools:stone_paxel"), item("mekanismtools:gold_paxel"), item("mekanismtools:diamond_paxel")],
      "Paxel Collector", subtitle="Wood, stone, gold and diamond", deps=["gs_paxel"], optional=True, tokens=2, xp=30, desc=[
        "&eWhat:&r Craft the early paxels you skipped, plus a diamond one for the long haul.",
        "&eChemistry:&r Gold is soft because its atoms slide past each other easily. Diamond is the hardest natural material because every carbon atom is locked to four neighbours.",
        "&eHow:&r Same recipe as the iron paxel: pickaxe, axe and shovel of one material, plus 2 sticks."]),
    # gs_opt_smithing moved to harvest.py (it is the Armour page's hub, as in ATM10).
    Q("tc_osmium_paxel", 2, 2, [item("mekanismtools:osmium_paxel")], "Osmium Paxel", deps=["t3_infuser"], xp=40,
      subtitle="The densest natural element, as a tool", desc=[
        "&eWhat:&r Mekanism's signature metal as a paxel: more durability and speed than bronze, iron tier for mining.",
        "&eChemistry:&r osmium (Os) is the densest natural element at about 22.6 g/cm³, twice as dense as lead.",
        "&eHow:&r osmium ore generates in the Overworld; smelt or process it, then craft the pickaxe, axe and shovel and combine them with a stick (check JEI).",
        "&eTip:&r your steel paxel from T1 already mines at diamond tier. This one is about durability and speed."]),
    Q("tc_obsidian_paxel", 6, 2, [item("mekanismtools:refined_obsidian_paxel")], "The Ultimate Paxel", deps=["tc_osmium_paxel"], xp=100,
      size=1.5, shape="hexagon", subtitle="Refined obsidian: Mekanism's toughest metal", desc=[
        "&6You remember a hammer that could split mountains. This is a start.&r",
        "&eWhat:&r refined obsidian is Mekanism's toughest material, and its paxel is the best of the line (netherite tier).",
        "&eHow:&r infuse obsidian dust with diamond in the Metallurgic Infuser, then press the refined obsidian dust in the Osmium Compressor (check JEI).",
        "&eTip:&r the same ingots make the Atomic Disassembler and much of Mekanism's late gear."]),
    Q("tc_disassembler", 7, 3.5, [item("mekanism:atomic_disassembler")], "Atomic Disassembler", deps=["tc_obsidian_paxel"], xp=150,
      optional=True, tokens=1, subtitle="Optional: an FE-powered everything-tool", desc=[
        "&eWhat:&r an electric tool that mines, chops and digs, with vein and area modes. It runs on FE instead of durability.",
        "&eHow:&r refined obsidian, atomic alloy, infused alloy and an Energy Tablet (check JEI). Charge it in an energy cube.",
        "&eTip:&r sneak + right-click to switch modes."]),

    # --- Mekanism gear (y=5.5) -----------------------------------------------------------------
    Q("tc_scuba", 0, 5.5, [item("mekanism:scuba_mask"), item("mekanism:scuba_tank")], "Bottled Oxygen", deps=["t3_infuser"], xp=60,
      subtitle="Breathe underwater on O₂ from your separator", desc=[
        "&eWhat:&r the Scuba Mask and Tank let you breathe underwater for as long as the tank has oxygen.",
        "&eChemistry:&r the Electrolytic Separator splits water: 2H₂O → 2H₂ + O₂. The O₂ fills the tank; the H₂ is fuel.",
        "&eHow:&r steel, a control circuit and a chemical tank (check JEI). Fill the tank from a Chemical Tank or the separator's oxygen output.",
        "&eTip:&r great for ocean monuments and underwater prospecting."]),
    Q("tc_free_runners", 2, 5.5, [item("mekanism:free_runners")], "Free Runners", deps=["tc_scuba"], xp=60,
      subtitle="Step up blocks and never take fall damage", desc=[
        "&eWhat:&r electric boots: auto step-up and no fall damage while charged.",
        "&eHow:&r infused alloy, a basic control circuit and an Energy Tablet (check JEI).",
        "&eTip:&r the armoured version adds protection; upgrade once you have more alloy."]),
    Q("tc_mekasuit", 4, 5.5, [item("mekanism:mekasuit_helmet"), item("mekanism:mekasuit_bodyarmor")], "MekaSuit", deps=["tc_free_runners", "t6_pu"], xp=500,
      size=1.5, shape="hexagon", subtitle="Polonium, HDPE and a netherite core", desc=[
        "&6You remember armour that was never armour, only certainty. This is the closest a mortal gets.&r",
        "&eWhat:&r Mekanism's modular power armour. Add modules for flight, night vision, magnet, radiation shielding and more.",
        "&eChemistry:&r it needs HDPE sheets (polyethylene: long C₂H₄ chains) and polonium pellets. Real ²¹⁰Po is made by hitting bismuth-209 with neutrons; Mekanism makes it from nuclear waste in the Solar Neutron Activator.",
        "&eHow:&r netherite armour, HDPE sheets, ultimate control circuits, polonium pellets and induction cells (check JEI). Install modules in the Modification Station."]),
    Q("tc_hazmat", 1, 7, [item("mekanism:hazmat_mask")], "Hazmat Gear", deps=["tc_scuba"], xp=40,
      optional=True, tokens=1, subtitle="Optional: lead against radiation", desc=[
        "&eWhat:&r the full hazmat suit stops Mekanism radiation from building up in you. Cheap and worth having before fission.",
        "&eChemistry:&r lead (Pb) is dense and has many electrons, so it absorbs gamma rays well.",
        "&eHow:&r lead ingots and orange dye for each piece (check JEI)."]),
    Q("tc_mek_jetpack", 3, 7, [item("mekanism:jetpack")], "Hydrogen Jetpack", deps=["tc_scuba"], xp=60,
      optional=True, tokens=1, subtitle="Optional: fly on the other half of water", desc=[
        "&eWhat:&r Mekanism's jetpack burns hydrogen gas. Short hops, not true flight.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O. Burning hydrogen gives only water and a lot of energy.",
        "&eHow:&r steel, tin, a basic control circuit and a chemical tank. Fill it with H₂ from the Electrolytic Separator."]),

    # --- Jetpacks and the Angel Ring (y=9.5) ---------------------------------------------------
    Q("tc_jetpack", 0, 9.5, [item("ironjetpacks:basic_coil"), item("ironjetpacks:jetpack")], "Jetpacks", deps=["t3_analog"], xp=100,
      subtitle="Electric flight, one coil at a time", desc=[
        "&eWhat:&r Iron Jetpacks run on FE. Every tier needs a coil, and in this pack the coils need MI circuits.",
        "&eHow:&r Basic coil = analog circuit (LV). Craft the coil, then cells, thrusters, strap and the jetpack for your metal (check JEI).",
        "&eTip:&r better metals fly faster and hold more FE. Charge it in any energy cube."]),
    Q("tc_jet_adv", 1, 11, [item("ironjetpacks:advanced_coil")], "Advanced Coil", deps=["tc_jetpack", "t4_mv"], xp=100,
      optional=True, tokens=1, subtitle="Optional: MV jetpacks", desc=[
        "&eWhat:&r unlocks the middle jetpack tiers.",
        "&eHow:&r needs an MI electronic circuit (MV, aluminum chemistry). Check JEI for which jetpacks use it.",
        "&eTip:&r JEI shows which jetpacks use this coil."]),
    Q("tc_jet_elite", 3, 11, [item("ironjetpacks:elite_coil")], "Elite Coil", deps=["tc_jet_adv", "t5_hv"], xp=150,
      optional=True, tokens=1, subtitle="Optional: HV jetpacks", desc=[
        "&eWhat:&r faster, longer flights.",
        "&eHow:&r needs an MI digital circuit (HV, polyethylene).",
        "&eTip:&r the digital circuit is your polyethylene line paying off; make a few extra."]),
    Q("tc_jet_ult", 5, 11, [item("ironjetpacks:ultimate_coil")], "Ultimate Coil", deps=["tc_jet_elite", "t6_pu"], xp=250,
      optional=True, tokens=2, subtitle="Optional: the best jetpacks", desc=[
        "&eWhat:&r the top jetpack tier.",
        "&eHow:&r needs an MI processing unit (EV, PVC chemistry).",
        "&eTip:&r by now the Angel Ring may suit you better; the jetpack still has the best speed."]),
    Q("tc_angel", 4, 9.5, [item("angelring:diamond_ring"), item("angelring:angel_ring")], "The Angel Ring", deps=["tc_jetpack", "t5_hv", "w_end"], xp=500,
      size=1.5, shape="hexagon", subtitle="Creative flight from a ring", desc=[
        "&6You remember the sky being yours. Now it is again.&r",
        "&eWhat:&r portable creative flight, no fuel, from a Curios ring slot.",
        "&eChemistry:&r its &eMI digital circuit&r needs polyethylene: n C₂H₄ → (C₂H₄)ₙ, ethylene from your distillation tower.",
        "&eHow:&r Elytra, ghast tears, diamond blocks and Nether Stars plus the digital circuit. Craft the Diamond Ring first, then the Angel Ring."]),

    # --- Comfort (y=13.5) ----------------------------------------------------------------------
    Q("tc_hammock", 0, 13.5, [anytag("comforts:hammocks")], "Hammock", deps=["gs_sleep"], xp=15,
      optional=True, tokens=1, subtitle="Optional: sleep through the day", desc=[
        "&eWhat:&r skips the day the way a sleeping bag skips the night, without moving your spawn.",
        "&eHow:&r wool of any colour, string and sticks. Hang it between two Rope and Nails placed on facing walls (check JEI).",
        "&eTip:&r useful when you want night-only mobs, like the ones a Deep Learner needs."]),
    Q("tc_mining_gadget", 6, 13.5, [anyof(["mininggadgets:mininggadget_simple", "mininggadgets:mininggadget_fancy", "mininggadgets:mininggadget"])],
      "Mining Gadget", deps=["tc_hub"], xp=60, section=PICKS, mirror="3B88D58B11B5DC78",
      optional=True, tokens=1, subtitle="Optional: a mining laser powered by FE", desc=[
        "&eWhat:&r a mining laser that breaks blocks at range. Upgrades add 3x3 (and bigger) size, efficiency, magnet and void filters.",
        "&eHow:&r iron, gold, diamond and redstone (check JEI). Charge it with FE.",
        "&eTip:&r a void filter for stone and dirt keeps your inventory clean on long ore runs."]),

    # --- More Silent Gear (y=15.5) -------------------------------------------------------------
    Q("tc_sg_parts", 0, 15.5, [item("silentgear:binding"), item("silentgear:grip")], "Bindings and Grips", deps=["gs_silent"], xp=25,
      optional=True, tokens=1, subtitle="Optional: parts that change a tool's stats", desc=[
        "&eWhat:&r bindings and grips are optional Silent Gear parts. Each adds its material's traits and stats to the tool.",
        "&eHow:&r make the Binding and Grip blueprints, then craft the parts from string, vines, leather or wool (check JEI). Add them to a tool in a crafting grid.",
        "&eTip:&r the Material Book (or JEI) shows every material's traits. Hover a part to see what it adds."]),
    Q("tc_sg_coating", 2, 15.5, [item("silentgear:coating_smithing_template")], "Coatings", deps=["tc_sg_parts", "tc_grader"], xp=40,
      optional=True, tokens=1, subtitle="Optional: plate a tool in a better material", desc=[
        "&eWhat:&r a coating covers a finished tool's main part in another material, like diamond or netherite, changing its stats and colour.",
        "&eChemistry:&r real tools are coated too: drill bits get a thin layer of titanium nitride (TiN) or diamond to stay sharp much longer.",
        "&eHow:&r craft the coating smithing template (check JEI), then apply the coating material at a smithing table."]),
    Q("tc_sg_ring", 0, 0, [tick()], "Silent Jewellery", deps=["tc_sg_parts"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_armor", 0, 0, [tick()], "Armour from Parts", deps=["tc_sg_parts", "tc_crimson_steel"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),

    # --- Just Dire Things (y=17.5): the goo line itself lives in the justdirethings chapter --------
    Q("tc_jdt_goo", 0, 17.5, [item("justdirethings:gooblock_tier1")], "Primordial Goo", deps=["gs_iron"], xp=25,
      optional=True, tokens=1, subtitle="Optional: the door into Just Dire Things", desc=[
        "&eWhat:&r Just Dire Things goo converts the blocks it touches. Tier 1 goo turns an iron block into raw ferricore ore.",
        "&eHow:&r clay, sugar, rotten flesh and dirt (check JEI). The full goo line, from ferricore to eclipse alloy, is in the Just Dire Things chapter.",
        "&eTip:&r JEI's goo tab shows every conversion and which goo tier it needs."]),
    Q("tc_jdt_pocket", 1, 19, [item("justdirethings:pocket_generator")], "Pocket Generator", deps=["jdt_ferricore"], xp=40,
      optional=True, tokens=1, subtitle="Optional: charge tools on the go", desc=[
        "&eWhat:&r the Pocket Generator burns fuel in your inventory and charges your FE items.",
        "&eHow:&r ferricore, a furnace, coal and a redstone block (check JEI).",
        "&eChemistry:&r burning coal is oxidation: C + O₂ → CO₂ releases about 394 kJ per mole of carbon as heat."]),
    Q("tc_jdt_portal", 7, 19, [item("justdirethings:portalgun")], "Thinking with Portals", deps=["jdt_celestigem"], xp=100,
      secret=True, loot="secret", subtitle="Secret: now you're thinking", desc=[
        "&6You remember stepping between places without walking. You'd forgotten how much fun it was.&r",
        "&eWhat:&r the Portal Gun shoots two linked portals onto walls. Walk in one, come out the other.",
        "&eTip:&r there is an upgraded Portal Gun too; JEI has its recipe."]),

    # --- Silent Gear: catalysts, dusts and the late blocks (ATM10-aligned round, 2026-10-19) ------
    Q("tc_sg_catalyst", 0, 0, [tick()], "Grading Catalysts", deps=["tc_grader", "tc_sg_dust"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_glittery", 0, 0, [tick()], "Glittery Dust", deps=["tc_sg_catalyst", "w_end"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_dust", 0, 0, [tick()], "Hammered Dust", deps=["tc_blaze_gold"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_charger", 0, 0, [tick()], "Starlight Charger", deps=["tc_sg_dust"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_starmetal", 0, 0, [tick()], "Starmetal", deps=["tc_azure", "tc_sg_dust", "hn_wither"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_recrystallizer", 0, 0, [tick()], "Recrystallizer", deps=["tc_azure"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),
    Q("tc_sg_blocks", 0, 0, [tick()], "A Metallurgist's Shelf", deps=["tc_tyrian"], xp=0, optional=True, tokens=0,
      subtitle="Retired: now on the Silent Gear page", desc=[
        "&eWhat:&r this quest moved to the Silent Gear page, which covers the same item. Click the check to clear it here."]),

    # ===== ATM10 mirror: basic_tools (2026-10-20) ==========================================================
    # --- the hub and the ore ladder (required) ------------------------------------------------------------
    Q("tc_hub", 0, 0, [item("minecraft:stick")], "Every Tool Starts Here", deps=[], xp=10, size=2.0, shape="gear",
      section=LADDER, mirror="5151CDD8FCDE7A07", subtitle="A stick: the handle of everything", desc=[
        "&6You remember holding a hammer that had no handle, because it didn't need one. Mortal tools do.&r",
        "&eWhat:&r this page is a tour of tools: a short ladder of ores, then one quest for each pickaxe and sword family in the pack.",
        "&eChemistry:&r a stick is wood, a composite of cellulose fibres in a lignin glue: stiff along the grain, light, and easy to replace.",
        "&eHow:&r two planks stacked make four sticks. Only the ore ladder is required; the collections are optional.",
        "&eTip:&r the Harvest Tiers page explains which pick mines what; this page is about owning them."]),
    Q("tc_cobble", 0, 0, [item("minecraft:cobblestone")], "Cobblestone", deps=["tc_hub"], xp=10, section=LADDER,
      mirror="57F47BA495B27F83", subtitle="The first rung: stone", desc=[
        "&eWhat:&r the rock under every Overworld biome. A wooden pick breaks stone into cobblestone.",
        "&eChemistry:&r Overworld stone stands in for real crustal rock: mostly silicate minerals, feldspars and quartz, built on SiO₄ tetrahedra.",
        "&eHow:&r mine any stone with a wooden pickaxe.",
        "&eTip:&r keep a stack: furnaces, stone tools and many early machines eat it."]),
    Q("tc_raw_iron", 0, 0, [item("minecraft:raw_iron")], "Raw Iron", deps=["tc_cobble"], xp=15, section=LADDER,
      mirror="3917DECAEF56A06A", subtitle="The second rung: a stone pick's reward", desc=[
        "&eWhat:&r iron ore needs a stone pick. Raw iron smelts into the metal most of your early gear is made of.",
        "&eChemistry:&r iron ores are oxides such as haematite, Fe₂O₃. Smelting strips the oxygen with carbon: Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eHow:&r mine iron ore with a stone pickaxe or better.",
        "&eTip:&r ore processing multiplies it later; don't smelt your whole stock on day one."]),
    Q("tc_diamond", 0, 0, [item("minecraft:diamond")], "Diamond", deps=["tc_raw_iron"], xp=25, section=LADDER,
      mirror="6601450C63FEEE61", subtitle="The third rung: carbon under pressure", desc=[
        "&eWhat:&r diamond ore needs an iron pick and sits deep in the deepslate.",
        "&eChemistry:&r diamond is pure carbon with each atom bonded to four others in a rigid 3D network. Graphite is the same element in flat sheets.",
        "&eHow:&r branch-mine near the bottom of the world with an iron pickaxe.",
        "&eTip:&r Fortune works on diamond ore. Save one good pick for it."]),
    Q("tc_debris", 0, 0, [item("minecraft:ancient_debris")], "Ancient Debris", deps=["tc_diamond"], xp=40, section=LADDER,
      mirror="17FE0C7748DD65CA", subtitle="The fourth rung: the Nether's buried metal", desc=[
        "&eWhat:&r ancient debris hides low in the Nether and needs a diamond-tier pick. It smelts into netherite scrap.",
        "&eChemistry:&r netherite is fiction, but its trick is real: some alloys keep their strength far above the temperature where steel softens.",
        "&eHow:&r dig tunnels around Y 15 in the Nether with a diamond (or steel) pick. It ignores explosions, so beds and TNT work.",
        "&eTip:&r it doesn't burn in lava either. Neither does anything made from it."]),
    Q("tc_raw_atm", 0, 0, [item(ATM + "raw_allthemodium")], "Raw Allthemodium", deps=["tc_debris"], xp=60, section=LADDER,
      mirror="03E05018D64DDEE1", subtitle="The fifth rung: a metal from deep places", desc=[
        "&eWhat:&r allthemodium ore sits deep in the Mining dimension and the lowest layers of the world. It needs a netherite-tier pick.",
        "&eHow:&r see the Allthemodium page for where it spawns and what mines it.",
        "&eTip:&r a Mining dimension trip is the fastest route; bring torches and food."]),
    Q("tc_raw_unob", 0, 0, [item(ATM + "raw_unobtainium")], "Raw Unobtainium", deps=["tc_raw_atm"], xp=100, section=LADDER,
      mirror="09733948CBCB3FB9", subtitle="The top rung", desc=[
        "&6The ladder ends where the world runs out of rock. You remember a time when it never did.&r",
        "&eWhat:&r the rarest ore of the Allthemodium family, and the top of the ladder.",
        "&eHow:&r the Allthemodium page shows where it grows and which pick it needs.",
        "&eTip:&r it alloys with the other two into that mod's best metals."]),

    # --- pickaxes (optional, off the hub) -----------------------------------------------------------------
    pick("tc_pk_wood", ["minecraft:wooden_pickaxe"], "Wooden Pickaxe", "the very first pick",
         "the weakest pick: stone and coal, nothing more.", "3 planks over 2 sticks.",
         "burn it as fuel once a stone pick replaces it.", "2EE4E88FC814AFA4"),
    pick("tc_pk_stone", ["minecraft:stone_pickaxe"], "Stone Pickaxe", "a rock on a stick",
         "opens iron, copper, lapis and nearly every MI and Mekanism ore.", "3 cobblestone (or another stone tool material) over 2 sticks.",
         "make two; they're cheap and wear out fast.", "2E6D11A5F5626A6C"),
    pick("tc_pk_iron", ["minecraft:iron_pickaxe"], "Iron Pickaxe", "the workhorse",
         "mines gold, redstone and diamond, and in this pack the hard MI ores (titanium, tungsten, platinum, iridium).",
         "3 iron ingots over 2 sticks.", "a Mekanism paxel of the same tier saves two inventory slots.", "70ED849A2EB44DEE"),
    pick("tc_pk_diamond", ["minecraft:diamond_pickaxe"], "Diamond Pickaxe", "hard, fast, and brittle in real life",
         "mines obsidian, crying obsidian and ancient debris.", "3 diamonds over 2 sticks.",
         "enchant it before you upgrade it; netherite keeps the enchantments.", "29A05589E96C0569", 30),
    pick("tc_pk_netherite", ["minecraft:netherite_pickaxe"], "Netherite Pickaxe", "upgrade, don't rebuild",
         "the vanilla top pick; it floats in lava and keeps every enchantment from the diamond one.",
         "smithing table: netherite upgrade template, diamond pickaxe and a netherite ingot.",
         "copy the template with diamonds and netherrack before you spend it.", "299F56B753286D0C", 40),
    pick("tc_pk_gold", ["minecraft:golden_pickaxe"], "Golden Pickaxe", "very fast, very soft",
         "the fastest vanilla pick and the weakest: wood tier, tiny durability.", "3 gold ingots over 2 sticks.",
         "with Silk Touch it is a quick glass and ice collector.", "3BF1900346772703"),
    pick("tc_pk_refobs", [MT + "refined_obsidian_pickaxe"], "Refined Obsidian Pickaxe", "Mekanism's best pick",
         "netherite tier without a Nether trip, and very durable.",
         "refined obsidian ingots and sticks (check JEI); the ingots come from the Metallurgic Infuser and Osmium Compressor.",
         "the paxel version is on this page's older Mekanism line.", "512396B331108BAF", 40),
    pick("tc_pk_mek", [MT + "steel_pickaxe", MT + "refined_glowstone_pickaxe"], "Steel or Glowstone Pickaxe", "Mekanism's middle picks",
         "both are diamond tier: steel is the cheap one, refined glowstone the fast one.",
         "steel or refined glowstone ingots and sticks (check JEI).",
         "steel is the one to carry early; you make steel anyway.", "51DBE688ED630DB1", 25),
    pick("tc_pk_ma_top", [MA + "supremium_pickaxe", MA + "awakened_supremium_pickaxe"], "Supremium Pickaxe", "a pick grown from a field",
         "the top Mystical Agriculture picks; they ignore 'can't mine' lists and hold augments.",
         "upgrade a lower essence pick with supremium (or awakened supremium) ingots and gemstones (check JEI).",
         "its augment slots are the point: area mining, speed, magnetism.", "58DDD32F849940A0", 60),
    pick("tc_pk_atm", [ATM + "allthemodium_pickaxe", ATM + "vibranium_pickaxe", ATM + "unobtainium_pickaxe"], "Allthemodium Pickaxe", "the deep metals as a tool",
         "the Allthemodium family's own picks, each one needed for the next metal's ore.",
         "see the Allthemodium page for the recipes and smithing templates.",
         "any one of the three counts here.", "609D03E335CF32E2", 60),
    pick("tc_pk_ae2", ["ae2:fluix_pickaxe", "ae2:certus_quartz_pickaxe", "ae2:nether_quartz_pickaxe"], "Quartz Pickaxe", "AE2's crystal tools",
         "Applied Energistics makes tools from certus, nether quartz and fluix; iron tier.",
         "crystals and sticks, like any pick (check JEI).", "the fluix pick smelts what it mines.", "1D3F11194EA3BB73"),
    pick("tc_pk_metal", [MT + "bronze_pickaxe", MT + "osmium_pickaxe", JDT + "ferricore_pickaxe"], "A Metal Pickaxe", "bronze, osmium or ferricore",
         "three iron-tier picks from two mods: Mekanism bronze and osmium, Just Dire Things ferricore.",
         "ingots and sticks; ferricore comes from goo-converted iron (check JEI).",
         "they mine the same blocks; durability and speed differ.", "64EED65F80A91D9E"),
    pick("tc_pk_occult", ["occultism:infused_pickaxe", "occultism:iesnium_pickaxe"], "Spirit Pickaxe", "Occultism's picks",
         "the spirit-infused pick can mine otherworld ores; the iesnium pick is its stronger cousin.",
         "check the Occultism page and JEI; both start from a spirit-attuned gem.", "otherworld ores only show while you have the Third Eye effect.", "275D97BF0CE9DCD4", 30),
    pick("tc_pk_deep", ["deeperdarker:resonarium_pickaxe", UG + "utherium_pickaxe"], "Resonarium or Utherium Pickaxe", "picks from the deep places",
         "resonarium from the Otherside and utherium from the Undergarden: both diamond tier.",
         "craft from the matching material (check JEI).", "Jade tells you if a block needs more before you swing.", "01046CFBD7411AA6", 30),
    pick("tc_pk_under", [UG + "froststeel_pickaxe", UG + "cloggrum_pickaxe"], "Undergarden Pickaxe", "cloggrum or froststeel",
         "the Undergarden's first metals; iron tier with their own traits (froststeel slows what it hits).",
         "ingots and sticks (check JEI).", "cloggrum is the easier of the two to find.", "01EE2526B43B6502"),
    pick("tc_pk_lapis", [MT + "lapis_lazuli_pickaxe"], "Lapis Pickaxe", "pretty, and stone tier",
         "a blue pick that enchants very well.", "lapis and sticks (check JEI).",
         "use it to practise enchanting while diamonds go into machines.", "79EF24E396779B9F"),
    pick("tc_pk_forgotten", [UG + "forgotten_pickaxe", "deeperdarker:warden_pickaxe"], "Forgotten or Warden Pickaxe", "the deepest picks",
         "the only picks besides energy tools that mine dreadrock.", "check the Undergarden and Deeper and Darker pages.",
         "either one finishes the Harvest Tiers line's last tier.", "7EC7E12C0880F8F5", 50),
    pick("tc_pk_eclipse", [JDT + "eclipsealloy_pickaxe"], "Eclipse Alloy Pickaxe", "Just Dire Things' best",
         "netherite tier, with abilities you switch on in its menu.", "eclipse alloy from tier 4 goo (see the Just Dire Things page).",
         "its abilities run on FE; charge it.", "1756F81ACFC56C58", 50),
    pick("tc_pk_jdt", [JDT + "blazegold_pickaxe", JDT + "celestigem_pickaxe"], "Blazegold or Celestigem Pickaxe", "goo-made picks",
         "diamond-tier picks from goo-converted gold and gems, each with switchable abilities.",
         "see the Just Dire Things page for the goo tiers.", "check each tool's menu; the abilities differ by material.", "5A2908437EC43AC6", 30),
    pick("tc_pk_ma", [MA + "inferium_pickaxe", MA + "prudentium_pickaxe", MA + "tertium_pickaxe", MA + "imperium_pickaxe"], "Essence Pickaxe", "Mystical Agriculture's lower picks",
         "essence picks have no 'can't mine' list; higher tiers are faster and hold more augments.",
         "a diamond pick with two ingots and two gemstones of the tier (check JEI).", "upgrade the same pick each tier; it keeps its enchantments.", "5CD65553EF60029B", 30),

    # --- swords (optional, off the hub) --------------------------------------------------------------------
    sword("tc_sw_wood", ["minecraft:wooden_sword"], "Wooden Sword", "better than a fist",
          "the first weapon: weak, cheap, and fuel when it wears out.", "2 planks over a stick.", "a stone sword is one cobblestone away.", "0583862ED0114442"),
    sword("tc_sw_stone", ["minecraft:stone_sword"], "Stone Sword", "a sharp rock",
          "the first real weapon, and still fine for the first nights.", "2 cobblestone over a stick.", "swing when the cooldown bar is full; spamming does little.", "54D3D6806C1F33F3"),
    sword("tc_sw_iron", ["minecraft:iron_sword"], "Iron Sword", "the standard blade",
          "the weapon for most of the early game.", "2 iron ingots over a stick.", "Mekanism's steel sword is the next step up.", "2B9AF0D6ED8BA628"),
    sword("tc_sw_diamond", ["minecraft:diamond_sword"], "Diamond Sword", "a hard edge",
          "the vanilla blade to beat until netherite.", "2 diamonds over a stick.", "enchant it now; the upgrade keeps it.", "55A9EB63F4964FCF", 25),
    sword("tc_sw_netherite", ["minecraft:netherite_sword"], "Netherite Sword", "lava-proof",
          "the vanilla top sword.", "smithing table: template, diamond sword, netherite ingot.", "a dropped netherite sword floats on lava; you can get it back.", "36A3ECD4F6CA2732", 40),
    sword("tc_sw_gold", ["minecraft:golden_sword"], "Golden Sword", "for show",
          "as weak as wood, but it enchants well.", "2 gold ingots over a stick.", "gold is so soft a fingernail almost scratches it.", "6EE68EEFE388CF8A"),
    sword("tc_sw_fluix", ["ae2:fluix_sword"], "Fluix Sword", "a crystal blade",
          "AE2's fluix sword: iron tier, made from the crystal your network runs on.", "fluix crystals and a stick (check JEI).", "spare a few crystals from the growth chambers.", "077A214422FEFF02"),
    sword("tc_sw_quartz", ["ae2:nether_quartz_sword", "ae2:certus_quartz_sword"], "Quartz Sword", "certus or nether quartz",
          "AE2's quartz swords: iron tier.", "quartz and a stick (check JEI).", "quartz is SiO₂: harder than steel, but brittle as a blade.", "3B542DC05240242C"),
    sword("tc_sw_osmium", [MT + "osmium_sword"], "Osmium Sword", "the densest metal",
          "Mekanism's osmium blade: durable, iron tier.", "osmium ingots and a stick (check JEI).", "osmium is the densest natural element, 22.6 g/cm³.", "2664388EBA1E8F90"),
    sword("tc_sw_mek", [MT + "refined_glowstone_sword", MT + "bronze_sword"], "Bronze or Glowstone Sword", "Mekanism's alloys",
          "bronze is the cheap one; refined glowstone hits harder.", "ingots and a stick (check JEI).", "bronze is copper with about 12% tin.", "149BD1A9F82FA19A"),
    sword("tc_sw_lapis", [MT + "lapis_lazuli_sword"], "Lapis Sword", "blue and enchantable",
          "weak, but it takes enchantments very well.", "lapis and a stick (check JEI).", "a cheap base for practising enchantments.", "480FA9FE57743B66"),
    sword("tc_sw_steel", [MT + "steel_sword"], "Steel Sword", "the honest upgrade",
          "a step above iron, from metal you already make.", "steel ingots and a stick (check JEI).", "any c:ingots/steel works.", "79E30114ED8870EE"),
    sword("tc_sw_refobs", [MT + "refined_obsidian_sword"], "Refined Obsidian Sword", "Mekanism's top blade",
          "the strongest Mekanism Tools sword.", "refined obsidian ingots and a stick (check JEI).", "the same ingots go into the Atomic Disassembler.", "7338CA23B27B2AF8", 40),
    sword("tc_sw_inferium", [MA + "inferium_sword"], "Inferium Sword", "essence blade, tier 1",
          "the first essence sword; higher tiers take augments.", "a diamond sword with inferium ingots and gemstones (check JEI).", "upgrade the same sword each tier.", "7F076FC4F2187692"),
    sword("tc_sw_prudentium", [MA + "prudentium_sword"], "Prudentium Sword", "essence blade, tier 2",
          "the second essence sword.", "upgrade the inferium sword with prudentium ingots and gemstones (check JEI).", "augment slots start here.", "7EDF2CC08FC774F9", 25),
    sword("tc_sw_tertium", [MA + "tertium_sword"], "Tertium Sword", "essence blade, tier 3",
          "the third essence sword.", "upgrade with tertium ingots and gemstones (check JEI).", "tertium essence sits behind the LV circuit gate.", "680ECE3D8DCDC515", 30),
    sword("tc_sw_imperium", [MA + "imperium_sword"], "Imperium Sword", "essence blade, tier 4",
          "the fourth essence sword.", "upgrade with imperium ingots and gemstones (check JEI).", "imperium essence sits behind the MV circuit gate.", "4DCEC4B97E24B6F1", 40),
    sword("tc_sw_supremium", [MA + "supremium_sword"], "Supremium Sword", "essence blade, tier 5",
          "the fifth essence sword.", "upgrade with supremium ingots and gemstones (check JEI).", "with Mystical Enlightenment it collects cognizant dust from bosses.", "2007EF64F0406090", 50),
    sword("tc_sw_awakened", [MA + "awakened_supremium_sword"], "Awakened Supremium Sword", "essence blade, awakened",
          "the best essence sword.", "upgrade with awakened supremium ingots and gemstones (check JEI).", "awakened supremium comes from the Awakening Altar.", "5A6670364ADE0858", 80),
    sword("tc_sw_utherium", [UG + "utherium_sword"], "Utherium Sword", "bane of the rotspawn",
          "the Undergarden's crystal blade; it hits that dimension's rotting mobs harder.", "utherium and a stick (check JEI).", "keep it for Undergarden trips.", "7CFEE836C68B3903", 30),
    sword("tc_sw_froststeel", [UG + "froststeel_sword"], "Froststeel Sword", "a cold edge",
          "slows what it hits.", "froststeel ingots and a stick (check JEI).", "good against anything that runs.", "579DA82672BF632C", 25),
    sword("tc_sw_dark", ["deeperdarker:resonarium_sword", UG + "forgotten_sword", UG + "cloggrum_sword"], "A Sword from Below", "resonarium, forgotten or cloggrum",
          "three blades from two underground mods; any one counts.", "check JEI for each material.", "the forgotten sword is the strongest of the three.", "56970D44D4C9015A", 30),
    sword("tc_sw_warden", ["deeperdarker:warden_sword"], "Warden Sword", "from the Otherside",
          "one of the strongest blades in the pack.", "warden carapace and a netherite sword (see the Deeper and Darker page).", "the upgrade happens at a smithing table.", "464DDEAF167BD0D5", 60),
    sword("tc_sw_ferricore", [JDT + "ferricore_sword"], "Ferricore Sword", "goo-made iron",
          "the first Just Dire Things sword.", "ferricore ingots and a stick (check JEI).", "its abilities switch on in the tool menu.", "161878AB4236C58B"),
    sword("tc_sw_blazegold", [JDT + "blazegold_sword"], "Blazegold Sword", "goo-made gold",
          "a diamond-tier blade with fire in it.", "blazegold ingots and a stick (check JEI).", "see the Just Dire Things page for tier 2 goo.", "6EFA73A4D01F0052", 25),
    sword("tc_sw_celestigem", [JDT + "celestigem_sword"], "Celestigem Sword", "goo-made gem",
          "a diamond-tier blade with FE-powered abilities.", "celestigem and a stick (check JEI).", "charge it before a fight.", "36B9D5A99E1AA85C", 30),
    sword("tc_sw_eclipse", [JDT + "eclipsealloy_sword"], "Eclipse Alloy Sword", "goo-made, netherite tier",
          "Just Dire Things' best blade.", "eclipse alloy from tier 4 goo (check JEI).", "it runs its abilities on FE.", "252169A6EB4DD75B", 50),
    sword("tc_sw_atm", [ATM + "allthemodium_sword"], "Allthemodium Sword", "deep metal, first of three",
          "the first Allthemodium blade.", "see the Allthemodium page (smithing template plus ingots).", "each of the three metals upgrades the last.", "47AED7219704EB3E", 60),
    sword("tc_sw_vib", [ATM + "vibranium_sword"], "Vibranium Sword", "deep metal, second of three",
          "the Nether's deep metal as a blade.", "see the Allthemodium page.", "vibranium ore needs an allthemodium pick.", "744AC6BD82FC2DEE", 80),
    sword("tc_sw_unob", [ATM + "unobtainium_sword"], "Unobtainium Sword", "deep metal, third of three",
          "the End's deep metal as a blade.", "see the Allthemodium page.", "the rarest of the three; take your time.", "4C8C56F960D92E9D", 100),
    sword("tc_sw_quantum", ["modern_industrialization:quantum_sword"], "Quantum Sword", "MI's endgame blade",
          "Modern Industrialization's quantum sword.",
          "a netherite sword plus a quantum upgrade in an MI Packer (check JEI).",
          "the quantum upgrade is deep in the MI chain; this is a trophy.", "2A6753C806D2AF8D", 150),
    sword("tc_sw_dagger", [MA + "soulium_dagger"], "Soulium Dagger", "a blade that gathers souls",
          "kills with it fill Soul Jars for Mystical Agriculture's mob seeds.", "a golden sword with soulium ingots and dust (check JEI).", "keep an empty jar in your inventory while you use it.", "6552E301C370D203", 25),
    sword("tc_sw_soul_daggers", [MA + "passive_soulium_dagger", MA + "hostile_soulium_dagger"], "Passive or Hostile Dagger", "a dagger tuned to one kind of mob",
          "these collect more souls from passive or from hostile mobs.", "upgrade a soulium dagger (check JEI).", "pick the one for the seeds you're working on.", "4CE6EB54B12EF6C5", 30),
], links=[("gs_silent", -2, 0), ("gs_irontools", -2, 2), ("t1_steel_paxel", 0, 2), ("t3_infuser", -2, 5.5), ("t3_analog", -2, 9.5), ("jdt_goo", 2, 17.5)], mirror="basic_tools")
