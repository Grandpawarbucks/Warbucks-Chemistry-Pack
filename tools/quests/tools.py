"""Quest chapter: tools. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("tools", "Tools and Comfort", "silentgear:pickaxe",
        ["Better tools from better materials, and a soft place to land."], SIDE, [
    # --- Silent Gear: core line (y=0) ---------------------------------------------------------
    Q("tc_sg_repair", 0, 0, [item("silentgear:crude_repair_kit")], "Repair Kits", deps=["gs_silent"], xp=25,
      subtitle="Mend your parts instead of throwing them away", desc=[
        "&6You remember tools that never wore out. These will, but you can mend them.&r",
        "&eWhat:&r Silent Gear tools don't break for good; at zero durability they just stop working until repaired.",
        "&eHow:&r craft a Crude Repair Kit, load it with matching material, then combine it with the tool in a crafting grid.",
        "&eTip:&r a better kit (Sturdy, then Crimson and Azure) holds more material and repairs more per use."]),
    Q("tc_blaze_gold", 2, 0, [item("silentgear:blaze_gold_ingot", 4)], "Blaze Gold", deps=["tc_sg_repair", "t2_nether"], xp=40,
      subtitle="Gold, fired with blaze powder", desc=[
        "&eWhat:&r Silent Gear's first magic alloy. It's a key ingredient of the Material Grader and the Starlight Charger.",
        "&eChemistry:&r gold (Au) is a noble metal: it barely reacts with anything, which is why it's found as native nuggets. Blaze gold is fictional; the blaze powder does the work.",
        "&eHow:&r gold ingot + 2 blaze powder in the Alloy Forge, or check JEI for the early crafting route.",
        "&eTip:&r keep a stack spare. Blaze gold blocks also go into the Starlight Charger."]),
    Q("tc_grader", 4, 0, [item("silentgear:material_grader")], "Material Grader", deps=["tc_blaze_gold"], xp=40,
      subtitle="Same metal, better grade, stronger part", desc=[
        "&eWhat:&r grades Silent Gear materials. A higher grade adds a stat bonus to every part made from that material.",
        "&eHow:&r quartz, iron, blaze gold and an Advanced Upgrade Base (check JEI). Feed it materials plus a catalyst (check JEI for which items count).",
        "&eTip:&r grade only the materials you'll use for heads and main parts; rods and bindings matter less."]),
    Q("tc_salvager", 6, 0, [item("silentgear:salvager")], "Salvager", deps=["tc_grader"], xp=40,
      subtitle="Old tools back into parts", desc=[
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
      subtitle="Azure silver from the End, plus gold", desc=[
        "&eWhat:&r azure silver ore generates in the End. Alloyed with gold it becomes azure electrum, a fast, enchantable metal.",
        "&eChemistry:&r real electrum is a natural gold–silver alloy (Au–Ag); the ancient Lydians struck the first coins from it.",
        "&eHow:&r Alloy Forge: an azure silver block, 2 gold ingots and an ender pearl."]),
    Q("tc_tyrian", 10, -4, [item("silentgear:tyrian_steel_ingot", 4)], "Tyrian Steel", deps=["tc_azure"], xp=200,
      optional=True, tokens=2, subtitle="Optional: Silent Gear's finest metal", desc=[
        "&eWhat:&r the top Silent Gear alloy: crimson steel, azure electrum, crushed shulker shell and netherite scrap.",
        "&eChemistry:&r Tyrian purple was a real dye made from sea snails, once worth its weight in silver. The steel just borrowed the colour.",
        "&eHow:&r Alloy Forge (check JEI). Crush shulker shells first."]),

    # --- Mekanism paxels (y=2) -----------------------------------------------------------------
    Q("tc_bronze_paxel", 0, 2, [item("mekanismtools:bronze_paxel")], "Bronze Paxel", deps=["gs_paxel", "t0_bronze"], xp=25,
      subtitle="Pickaxe, axe and shovel in your first alloy", desc=[
        "&eWhat:&r a paxel is a pickaxe, axe and shovel in one tool. Bronze is tougher than iron.",
        "&eChemistry:&r bronze is copper with about 12% tin (Cu–Sn). Tin atoms stiffen copper's soft lattice.",
        "&eHow:&r craft a bronze pickaxe, axe and shovel, then combine them with a stick (check JEI)."]),
    Q("tc_osmium_paxel", 2, 2, [item("mekanismtools:osmium_paxel")], "Osmium Paxel", deps=["tc_bronze_paxel", "t3_infuser"], xp=40,
      subtitle="The densest natural element, as a tool", desc=[
        "&eWhat:&r Mekanism's signature metal as a paxel: more durability and speed than bronze.",
        "&eChemistry:&r osmium (Os) is the densest natural element at about 22.6 g/cm³, twice as dense as lead.",
        "&eHow:&r osmium ore generates in the Overworld; smelt or process it, then craft the tools and combine."]),
    Q("tc_diamond_paxel", 4, 2, [item("mekanismtools:diamond_paxel")], "Diamond Paxel", deps=["tc_osmium_paxel"], xp=50,
      subtitle="Carbon in its hardest form", desc=[
        "&eWhat:&r the diamond paxel mines everything the diamond pickaxe can, in one slot.",
        "&eChemistry:&r diamond is pure carbon with every atom bonded to four others in a rigid 3D lattice. Graphite is the same carbon in flat sheets.",
        "&eHow:&r diamond pickaxe, axe and shovel plus a stick (check JEI)."]),
    Q("tc_obsidian_paxel", 6, 2, [item("mekanismtools:refined_obsidian_paxel")], "The Ultimate Paxel", deps=["tc_diamond_paxel"], xp=100,
      size=1.5, shape="hexagon", subtitle="Refined obsidian: Mekanism's toughest metal", desc=[
        "&6You remember a hammer that could split mountains. This is a start.&r",
        "&eWhat:&r refined obsidian is Mekanism's toughest material, and its paxel is the best of the line.",
        "&eHow:&r infuse obsidian dust with diamond in the Metallurgic Infuser, then press the refined obsidian dust in the Osmium Compressor (check JEI).",
        "&eTip:&r the same ingots make the Atomic Disassembler and much of Mekanism's late gear."]),
    Q("tc_steel_paxel", 1, 3.5, [item("mekanismtools:steel_paxel")], "Steel Paxel", deps=["tc_bronze_paxel", "t1_steel"], xp=30,
      optional=True, tokens=1, subtitle="Optional: a paxel from your blast furnace", desc=[
        "&eWhat:&r a sidegrade to bronze, made from the steel you already produce.",
        "&eChemistry:&r steel is iron with a little carbon from coke. Too much carbon (cast iron) makes it brittle.",
        "&eHow:&r steel pickaxe, axe and shovel plus a stick (check JEI)."]),
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
    Q("tc_hammock", 0, 13.5, [item("comforts:hammock_white")], "Hammock", deps=["gs_sleep"], xp=15,
      subtitle="Sleep through the day", desc=[
        "&eWhat:&r skips the day the way a sleeping bag skips the night, without moving your spawn.",
        "&eHow:&r white wool, string and sticks. Hang it between two Rope and Nails placed on facing walls (check JEI).",
        "&eTip:&r useful when you want night-only mobs, like the ones a Deep Learner needs."]),
    Q("tc_waystone", 2, 13.5, [item("waystones:warp_stone")], "Warp Stone", deps=["gs_iron"], xp=40,
      subtitle="Teleport to any waystone from anywhere", desc=[
        "&eWhat:&r Waystones (found in villages, or crafted) let you teleport between places you've visited. A Warp Stone works from anywhere.",
        "&eHow:&r amethyst, ender pearls and emeralds (check JEI). Activate a waystone first by right-clicking it.",
        "&eTip:&r it has a cooldown, so don't count on it in an emergency."]),
    Q("tc_toolbelt", 4, 13.5, [item("toolbelt:belt")], "Tool Belt", deps=["gs_iron"], xp=20,
      subtitle="Swap tools from your belt with one key", desc=[
        "&eWhat:&r a belt worn in a Curios slot that holds tools and swaps them into your hand with a key.",
        "&eHow:&r leather, string and an iron ingot. Add pouches for more slots.",
        "&eTip:&r set the belt key in Controls. Great for paxel, sword, hoe and wrench."]),
    Q("tc_mining_gadget", 6, 13.5, [item("mininggadgets:mininggadget_simple")], "Mining Gadget", deps=["t3_hull"], xp=60,
      subtitle="A mining laser powered by FE", desc=[
        "&eWhat:&r a mining laser that breaks blocks at range. Upgrades add 3x3 (and bigger) size, efficiency, magnet and void filters.",
        "&eHow:&r iron, gold, diamond and redstone (check JEI). Charge it with FE.",
        "&eTip:&r a void filter for stone and dirt keeps your inventory clean on long ore runs."]),
])
