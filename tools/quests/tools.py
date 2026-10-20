"""Quest chapter: tools. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

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
    Q("tc_grader", 4, 0, [item("silentgear:material_grader")], "Material Grader", deps=["tc_blaze_gold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: same metal, better grade, stronger part", desc=[
        "&eWhat:&r grades Silent Gear materials. A higher grade adds a stat bonus to every part made from that material.",
        "&eHow:&r quartz, iron, blaze gold and an Advanced Upgrade Base (check JEI). Feed it materials plus a catalyst (check JEI for which items count).",
        "&eTip:&r grade only the materials you'll use for heads and main parts; rods and bindings matter less."]),
    Q("tc_salvager", 6, 0, [item("silentgear:salvager")], "Salvager", deps=["tc_grader"], xp=40,
      optional=True, tokens=1, subtitle="Optional: old tools back into parts", desc=[
        "&eWhat:&r breaks old Silent Gear tools back into parts, so upgrading doesn't waste materials.",
        "&eHow:&r place it and drop in the old tool. Some material is lost on each salvage.",
        "&eTip:&r salvage before you throw anything in lava; the parts often have most of their value left."]),

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
    Q("gs_opt_smithing", 0, 5, [item("minecraft:smithing_table")], "Smithing Table", subtitle="Upgrades without starting over", deps=["gs_iron"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A smithing table upgrades tools and armour in place and applies armour trims. You'll use it for netherite later.",
        "&eHow:&r 2 iron ingots over 4 planks.",
        "&eTip:&r Apotheosis adds smithing recipes too, such as upgrading chainmail to iron (check JEI)."]),
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
    Q("tc_mining_gadget", 6, 13.5, [item("mininggadgets:mininggadget_simple")], "Mining Gadget", deps=["t3_hull"], xp=60,
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
    Q("tc_sg_ring", 4, 15.5, [anyof(["silentgear:ring", "silentgear:bracelet", "silentgear:necklace"], 1)], "Silent Jewellery", deps=["tc_sg_parts"], xp=40,
      optional=True, tokens=1, subtitle="Optional: rings, bracelets and necklaces", desc=[
        "&eWhat:&r Silent Gear jewellery carries material traits as curios: a ring of a lucky or magnetic material gives you that trait while worn.",
        "&eHow:&r a ring shank, bracelet band or necklace chain plus a gem setting, made with the matching blueprint (check JEI).",
        "&eTip:&r try different metals and gems. The traits list on each material shows what jewellery will do."]),
    Q("tc_sg_armor", 6, 15.5, [anyof(["silentgear:helmet", "silentgear:chestplate", "silentgear:leggings", "silentgear:boots"], 4)], "Armour from Parts", deps=["tc_sg_parts", "tc_crimson_steel"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a full set of Silent Gear armour", desc=[
        "&eWhat:&r Silent Gear armour is built from plates of any material, so your best alloy becomes your best armour.",
        "&eHow:&r helmet, chestplate, legging and boot plates from their blueprints, then assemble each piece (check JEI). Any four pieces.",
        "&eTip:&r crimson steel and azure electrum plates have strong traits; check the Material Book before choosing."]),

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
    Q("tc_sg_catalyst", 0, 0, [item("silentgear:glowing_dust", 4), item("silentgear:blazing_dust", 4)], "Grading Catalysts", deps=["tc_grader", "tc_sg_dust"], xp=40,
      optional=True, tokens=1, subtitle="Optional: fuel for the Material Grader", desc=[
        "&eWhat:&r the Material Grader needs a catalyst for each try. Glowing dust is tier 1, blazing dust tier 2; a better catalyst allows a higher grade.",
        "&eChemistry:&r a real catalyst speeds a reaction without being used up. These are spent on every try, so 'reagent' would be the honest word.",
        "&eHow:&r glowing dust: a stick, 2 glowstone dust and a quartz (makes 4). Blazing dust: blaze gold dust and 2 glowstone dust (makes 4).",
        "&eTip:&r grade the material for a tool head, not the rod; the head carries most of the stats."]),
    Q("tc_sg_glittery", 0, 0, [item("silentgear:glittery_dust", 8)], "Glittery Dust", deps=["tc_sg_catalyst", "w_end"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the tier 3 catalyst", desc=[
        "&eWhat:&r the best Grader catalyst, for the highest grades.",
        "&eHow:&r popped chorus fruit, emerald nuggets, glowstone dust and a nether banana make 8 (check JEI). Chorus grows in the End; nether bananas grow on netherwood trees.",
        "&eTip:&r popped chorus is just chorus fruit smelted in a furnace."]),
    Q("tc_sg_dust", 0, 0, [item("silentgear:blaze_gold_dust", 2)], "Hammered Dust", deps=["tc_blaze_gold"], xp=25,
      optional=True, tokens=1, subtitle="Optional: crush an ingot on an anvil", desc=[
        "&eWhat:&r Silent Gear turns its ingots into dust with a hammer: blaze gold, crimson iron, azure silver and more.",
        "&eChemistry:&r grinding a metal to powder hugely raises its surface area. That's why fine metal dusts burn or react so much faster than a solid bar.",
        "&eHow:&r a tool action with any hammer (the c:tools/hammer tag) on the ingot; JEI shows the steps and which block it needs.",
        "&eTip:&r blaze gold dust is the tier 1 Starlight Charger catalyst and the base of blazing dust."]),
    Q("tc_sg_charger", 0, 0, [item("silentgear:starlight_charger")], "Starlight Charger", deps=["tc_sg_dust"], xp=60,
      optional=True, tokens=1, subtitle="Optional: charge materials under the night sky", desc=[
        "&eWhat:&r the Starlight Charger collects starlight at night and charges Silent Gear materials, giving them a 'charged' bonus.",
        "&eHow:&r quartz blocks, glass, polished blackstone and a blaze gold block (check JEI). Place it under open sky, add a catalyst (blaze gold dust is tier 1) and the item.",
        "&eTip:&r the catalyst tier sets how strong the charge can get; JEI's tag view lists each tier."]),
    Q("tc_sg_starmetal", 0, 0, [item("silentgear:azure_silver_dust", 2), item("silentgear:starmetal_dust", 3)], "Starmetal", deps=["tc_azure", "tc_sg_dust", "hn_wither"], xp=100,
      optional=True, tokens=2, subtitle="Optional: azure metals and a piece of a star", desc=[
        "&eWhat:&r starmetal dust is a late Silent Gear material made from azure metals and a Nether Star fragment.",
        "&eChemistry:&r every atom heavier than iron was forged in dying stars or neutron-star collisions. Real 'starmetal' is just... metal.",
        "&eHow:&r azure electrum dust, 2 azure silver dust, blaze gold dust and a nether star fragment make 3 (check JEI). Hammer the ingots into dust first.",
        "&eTip:&r one Nether Star crafts into 9 fragments, so a single Wither kill goes a long way."]),
    Q("tc_sg_recrystallizer", 0, 0, [item("silentgear:recrystallizer")], "Recrystallizer", deps=["tc_azure"], xp=75,
      optional=True, tokens=1, subtitle="Optional: grow hybrid gems", desc=[
        "&eWhat:&r the Recrystallizer fuses gems and dusts into a hybrid gem material whose stats depend on what you put in.",
        "&eChemistry:&r real recrystallisation purifies a solid: dissolve it hot, cool slowly, and pure crystals grow while impurities stay in the liquid.",
        "&eHow:&r azure electrum ingots, an emerald, a diamond, purpur blocks and a gold block (check JEI).",
        "&eTip:&r the Material Book explains hybrid gems; experiment with cheap gems first."]),
    Q("tc_sg_blocks", 0, 0, [item("silentgear:crimson_steel_block"), item("silentgear:azure_electrum_block"), item("silentgear:tyrian_steel_block")],
      "A Metallurgist's Shelf", deps=["tc_tyrian"], xp=150, optional=True, tokens=2, subtitle="Optional: a block of each great alloy", desc=[
        "&6Three alloys, three blocks, each one a recipe you wrote yourself. You remember a forge like this.&r",
        "&eWhat:&r a storage block of crimson steel, azure electrum and tyrian steel: Silent Gear's three great alloys, side by side.",
        "&eChemistry:&r alloys aren't mixtures you can see: the atoms share one crystal lattice. Bronze, steel and electrum are all solid solutions or mixed phases at the atomic scale.",
        "&eHow:&r nine ingots of each make a block (check JEI)."]),
], links=[("gs_silent", -2, 0), ("gs_irontools", -2, 2), ("t1_steel_paxel", 0, 2), ("t3_infuser", -2, 5.5), ("t3_analog", -2, 9.5), ("jdt_goo", 2, 17.5)])
