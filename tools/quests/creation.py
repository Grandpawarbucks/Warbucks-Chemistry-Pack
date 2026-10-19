"""Quest chapter: creation (post-Seed goals). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Opens with t7_creation (moved from t7.py). Right side: making matter (Nucleosynthesizer, MI quantum line,
fusion and endgame alloys, Extended Crafting singularities). Left side: walking the worlds (biome tasks)
and collecting the rarest elements. Every item here has a real recipe in the jars (checked 2026-10-18).
"""
from questlib import Q, Chapter, item, dim, tick, biome, anyof, MAIN, SIDE  # noqa: F401

MI = "modern_industrialization:"
MEK = "mekanism:"
GT = "kubejs:greater_demigod_token"
PB = "{@pagebreak}"
LANTHANIDES = ["chemlib:" + e for e in ("lanthanum", "cerium", "praseodymium", "neodymium", "promethium", "samarium", "europium",
                                        "gadolinium", "terbium", "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium")]
NOBLE = ["chemlib:" + e for e in ("helium", "neon", "argon", "krypton", "xenon", "radon")]

CHAPTER = Chapter("creation", "Creation", "extendedcrafting:ultimate_singularity",
        ["The Seed is planted. Now shape what grows."], MAIN, [
    # ---------------------------------------------------------------- opening (moved from t7)
    Q("t7_creation", 0, 0, [tick()], "A New World", deps=["t7_seed"], xp=2000, size=2.5, shape="gear", tokens=50,
      subtitle="The demigod, restored", desc=[
        "&6You took the world apart, element by element, and learned to build it again.&r",
        "Fire, steel, acid, oil, silicon, the atom, antimatter. Every tier was a lesson in chemistry, and you mastered them all.",
        "&6The worlds out there are blank canvases now. Go make them yours.&r",
        PB,
        "&eWhat now:&r this chapter is for after the Seed. Nothing here gates anything; it's what a demigod does with full power.",
        "&eTo the right:&r making matter. Rewrite nuclei with antimatter, compress a singularity, build armour from a collapsed star.",
        "&eTo the left:&r walking the worlds you can now reach, and holding the rarest parts of the periodic table in your hand."]),
    # ---------------------------------------------------------------- right, y=-4: rewriting nuclei
    # --- the Terraformer (Warbucks Core): the Seed, planted ------------------------------------------
    Q("cn_capsule", -1, 3, [item("warbuckscore:biome_capsule")], "A Sample of Somewhere", deps=["t7_creation"], xp=200,
      tokens=10, subtitle="Bottle a biome", desc=[
        "&6Every world you have walked through, you can carry with you.&r",
        "&eWhat:&r a Biome Capsule records the biome you stand in (sneak + right-click). It tells the Terraformer what to grow.",
        "&eHow:&r glass bottle, rubber sheet and any sapling. Travel to the biome you want, then record it.",
        "&eTip:&r capsules stack until filled; each one holds one biome."]),
    Q("cn_terraformer", 1, 3, [item("warbuckscore:terraformer")], "The Terraformer", deps=["cn_capsule"], xp=1500,
      size=1.5, shape="gear", tokens=20, choice="pick_late", subtitle="The Seed, planted", desc=[
        "&6The Seed was never meant to stay in your pocket.&r",
        "&eWhat:&r the Terraformer (Warbucks Core) rewrites the biome around it, nearest chunks first, out to a 9x9 chunk area.",
        "&eHow:&r craft it from the Seed of a New World, processing units, stainless plates and energy cores. Right-click it with a filled Biome Capsule, then with Charged Energy Cores (each powers 9 chunks; sneak to insert a stack). Right-click empty-handed for status.",
        "{@pagebreak}",
        "&eWhat changes:&r grass and leaf colours, weather (rain or snow), and which mobs spawn, just like vanilla /fillbiome. Blocks you placed stay as they are.",
        "&eTip:&r you can change it again later: a new capsule restarts the spread with the new biome."]),
    Q("cn_reshaped", 1, 5, [tick()], "A World You Chose", deps=["cn_terraformer"], xp=800, optional=True, tokens=10,
      loot="boss", subtitle="All 81 chunks", desc=[
        "&6This is what the power was for.&r",
        "&eWhat:&r let a Terraformer finish its whole area (status shows 81 / 81), then tick this off.",
        "&eTip:&r 9 Charged Energy Cores finish one Terraformer."]),
    Q("cn_nucleo", 3, -4, [item(MEK + "antiprotonic_nucleosynthesizer")], "Nucleosynthesis", deps=["t7_creation"], xp=500,
      tokens=10, choice="pick_late", subtitle="Turn one thing into another with antimatter", desc=[
        "&6Making something out of nothing was once your trade. This is close.&r",
        "&eWhat:&r Mekanism's Antiprotonic Nucleosynthesizer feeds a few millibuckets of antimatter into an item and rebuilds it as something rarer.",
        "&eChemistry:&r nucleosynthesis is how stars make elements: lighter nuclei fuse into heavier ones. This machine borrows the idea.",
        "&eHow:&r check JEI for the recipe and the full list of transmutations. Pipe antimatter in from your SPS.",
        "&eTip:&r it works slowly. Give it its own antimatter tank."]),
    Q("cn_heart", 5, -4, [item("minecraft:heart_of_the_sea", 4)], "Hearts of the Sea", deps=["cn_nucleo"], xp=400,
      tokens=10, loot="boss", subtitle="A Nether Star, rewritten", desc=[
        "&eWhat:&r four Hearts of the Sea, each nucleosynthesized from a Nether Star with 5 mB of antimatter.",
        "&eHow:&r Nether Star in, antimatter in, wait about a minute.",
        "&eTip:&r a Heart of the Sea plus nautilus shells makes a Conduit: permanent water breathing and night vision around an ocean base."]),
    Q("cn_skulls", 7, -4, [item("minecraft:wither_skeleton_skull", 6)], "Skulls on Demand", deps=["cn_heart"], xp=400,
      tokens=10, choice="pick_late", subtitle="Two Withers' worth, no fortress", desc=[
        "&eWhat:&r six wither skeleton skulls, made from ordinary skeleton skulls with 5 mB of antimatter each.",
        "&eHow:&r skeleton skulls drop when a charged creeper kills a skeleton, or from other sources (check JEI). Feed them to the Nucleosynthesizer.",
        "&eTip:&r that's enough for two more Withers, and two more Nether Stars for a second Seed."]),
    Q("cn_echo", 9, -4, [item("minecraft:echo_shard", 32)], "Echoes", deps=["cn_skulls"], xp=400,
      tokens=12, items=[(GT, 1)], subtitle="Amethyst in, Ancient City loot out", desc=[
        "&eWhat:&r 32 echo shards, rebuilt from amethyst shards with 2 mB of antimatter each.",
        "&eChemistry:&r real amethyst is quartz (SiO₂) coloured purple by traces of iron and natural radiation. Here it becomes something no chemist could make.",
        "&eHow:&r amethyst shards from geodes or a budding amethyst farm. Nucleosynthesizer, 2 mB antimatter each.",
        "&eTip:&r echo shards make Recovery Compasses, which point to where you last died."]),
    # ---------------------------------------------------------------- right, y=-2: MI quantum line
    Q("cn_nuke", 3, -2, [item(MI + "nuke", 64)], "Sixty-Four Nukes", deps=["t7_creation"], xp=600,
      tokens=15, loot="boss", subtitle="Not for throwing", desc=[
        "&eWhat:&r MI's Nuke block. Sixty-four of them are crushed together to make a singularity.",
        "&eChemistry:&r a nuke combines fission (plutonium) and fusion fuel (deuterium and tritium, the heavy isotopes of hydrogen) around industrial TNT.",
        "&eHow:&r MI Assembler: 6 industrial TNT, 4 plutonium ingots, 2 processing units, 4 nuclear alloy plates, 100 mB deuterium, 50 mB tritium → 2 nukes.",
        "&eTip:&r that's 32 crafts, 64 processing units and 128 plutonium ingots. Automate it.",
        PB,
        "&eDeep dive: two kinds of nuclear energy&r",
        "Fission splits heavy nuclei like Pu-239 into lighter ones. Fusion joins light nuclei like deuterium (²H) and tritium (³H) into helium.",
        "Both release energy because the products are more tightly bound than the inputs. Iron-56 sits at the bottom of that curve: nothing is gained by splitting it or fusing it.",
        "Real thermonuclear weapons use a fission stage to compress and heat a fusion stage. MI's recipe follows the same idea."]),
    Q("cn_mi_singularity", 5, -2, [item(MI + "singularity")], "A Singularity", deps=["cn_nuke", "cn_ultradense"], xp=800,
      tokens=20, items=[(GT, 2)], subtitle="Sixty-four nukes, one point", desc=[
        "&eWhat:&r MI's Singularity: an ultradense metal ball collapsed by 64 nukes in the Implosion Compressor.",
        "&eHow:&r ultradense metal ball (tungsten large plates, lead plates and an iridium plate, check JEI) + 64 nukes → Implosion Compressor.",
        "&eTip:&r it's never used up in the Electrolyzer: it slowly bleeds out UU-matter, 1 mB every 2500 ticks. Build several Electrolyzers and several singularities.",
        PB,
        "&eDeep dive: collapse&r",
        "A real singularity is the centre of a black hole, where matter is crushed past every limit we know. Stars more than about 20 times the Sun's mass end this way.",
        "Before that, there's neutron-star matter: electrons are pushed into protons until only neutrons remain. A teaspoon would weigh about a billion tonnes.",
        "MI's singularity is a game item, not physics. But the idea, matter compressed until it becomes a source of something new, fits a demigod well."]),
    Q("cn_quantum_upgrade", 7, -2, [item(MI + "quantum_upgrade")], "Quantum Upgrade", deps=["cn_mi_singularity"], xp=800,
      tokens=20, choice="pick_late", subtitle="UU-matter, circuits and a singularity", desc=[
        "&eWhat:&r the part that turns netherite armour into MI quantum armour.",
        "&eHow:&r MI Assembler: 32 highly advanced upgrades, 8 quantum circuits, 1 singularity, 1 quantum circuit board, 50 mB UU-matter.",
        "&eTip:&r 50 mB of UU-matter takes one Electrolyzer and singularity about 1.7 hours (1 mB per 2500 ticks). More singularities, more Electrolyzers."]),
    Q("cn_quantum_armor", 9, -2, [item(MI + "quantum_helmet"), item(MI + "quantum_chestplate"), item(MI + "quantum_leggings"), item(MI + "quantum_boots")],
      "Quantum Armour", deps=["cn_quantum_upgrade"], xp=2000, size=1.5, shape="hexagon",
      tokens=30, loot="boss", items=[(GT, 3)], subtitle="Armour fit for a god", desc=[
        "&6Once you needed no armour at all. This is the next best thing.&r",
        "&eWhat:&r MI's quantum armour: a full set, each piece a netherite piece plus a quantum upgrade.",
        "&eHow:&r MI Packer: netherite armour piece + 1 quantum upgrade, 200 ticks at 1,000,000 EU/t. Four upgrades for four pieces.",
        "&eTip:&r that draw is far above a plain Packer's limit. Check JEI and the MI guidebook for how machine upgrades raise it."]),
    Q("cn_replicator", 11, -2, [item(MI + "replicator")], "Replicator", deps=["cn_quantum_upgrade"], xp=1000,
      optional=True, tokens=2, items=[(GT, 2)], subtitle="Optional: copy anything with UU-matter", desc=[
        "&eWhat:&r MI's Replicator copies items using UU-matter.",
        "&eHow:&r MI Assembler: quantum machine hull, 2 quantum upgrades, 4 quantum circuits, 500 mB UU-matter. Check JEI for what it can copy.",
        "&eTip:&r 500 mB is about 17 hours for one Electrolyzer. A long-term goal for a server, not a weekend."]),
    # ---------------------------------------------------------------- right, y=0: fusion and alloys
    Q("cn_fusion", 3, 0, [item(MI + "fusion_reactor"), item(MI + "plasma_turbine")], "A Star in a Box", deps=["t7_creation"], xp=800,
      tokens=15, choice="pick_late", subtitle="MI's fusion reactor and plasma turbine", desc=[
        "&eWhat:&r MI's fusion reactor makes helium plasma; the plasma turbine turns it into a flood of EU.",
        "&eChemistry:&r D + T → ⁴He + n. MI's reactor turns 1000 mB each of deuterium and tritium into helium plasma and hydrogen.",
        "&eHow:&r fusion reactor: 6 fusion chambers, a quantum machine hull and 2 quantum circuits in the MI Assembler. The multiblock layout is in JEI and the MI guidebook.",
        "&eTip:&r deuterium-deuterium and helium-3 routes exist too (check JEI under the fusion reactor).",
        PB,
        "&eDeep dive: why fusion is hard&r",
        "Nuclei are positively charged and repel each other. To fuse, they need temperatures over 100 million °C, hotter than the Sun's core.",
        "The Sun manages at 15 million °C only because of its crushing gravity and its sheer size. On Earth we use magnetic bottles (tokamaks) or lasers instead.",
        "In 2022 the US National Ignition Facility got more energy out of a fusion shot than its lasers put in, for the first time."]),
    Q("cn_superconductor", 5, 0, [item(MI + "superconductor_ingot", 64)], "Sixty-Four Superconductors", deps=["cn_fusion"], xp=800,
      tokens=15, items=[(GT, 1)], subtitle="Wire with no resistance at all", desc=[
        "&eWhat:&r a stack of MI superconductor ingots, the material of MI's best cables and coils.",
        "&eChemistry:&r below a critical temperature, a superconductor carries current with zero resistance. Real high-temperature ones, like YBa₂Cu₃O₇, are copper oxides with yttrium and rare earths.",
        "&eHow:&r Mixer: iridium, annealed copper, yttrium and neodymium dusts → superconductor dust. Electric Blast Furnace → hot ingot → Vacuum Freezer.",
        "&eTip:&r 64 ingots need 64 EBF runs at 128 EU/t. Run several furnaces."]),
    Q("cn_shining", 7, 0, [item("mekanism_extras:alloy_shining", 8)], "Shining Alloy", deps=["cn_superconductor"], xp=800,
      tokens=15, choice="pick_late", subtitle="Mekanism Extras' antimatter alloy", desc=[
        "&eWhat:&r Mekanism Extras' alloys go beyond atomic: radiance → thermonuclear → shining → spectrum. Shining is the first that needs antimatter.",
        "&eHow:&r enriched thermonuclear material + antimatter in the Nucleosynthesizer gives enriched shining. Turn it into shining infusion and infuse a thermonuclear alloy (check JEI for each step).",
        "&eTip:&r these alloys build Mekanism Extras' higher tiers of factories, cables and energy cubes."]),
    Q("cn_atomic", 9, 0, [item(MEK + "alloy_atomic", 64)], "A Stack of Atomic Alloy", deps=["cn_shining"], xp=600,
      tokens=12, items=[(GT, 1)], subtitle="Quantity is its own kind of power", desc=[
        "&eWhat:&r 64 atomic alloys, Mekanism's top standard alloy.",
        "&eHow:&r Metallurgic Infuser: reinforced alloy + refined obsidian dust (check JEI). Each step up uses the alloy before it.",
        "&eTip:&r a Metallurgic Infusing Factory makes this a matter of minutes."]),
    # ---------------------------------------------------------------- right, y=2: Extended Crafting
    Q("cn_compressor", 3, 2, [item("extendedcrafting:compressor")], "Quantum Compressor", deps=["t7_creation"], xp=500,
      tokens=10, choice="pick_late", subtitle="Ten thousand of anything, made one", desc=[
        "&eWhat:&r Extended Crafting's Quantum Compressor squeezes huge amounts of one material into a singularity.",
        "&eHow:&r crafting table: black iron ingots, a black iron slate, 2 elite components, 2 elite catalysts and a frame (check JEI).",
        "&eTip:&r it uses 5,000 FE/t and holds 10 million FE. Power it well."]),
    Q("cn_ec_singularity", 5, 2, [item("extendedcrafting:singularity")], "Your First Singularity", deps=["cn_compressor"], xp=800,
      tokens=15, items=[(GT, 1)], subtitle="Ten thousand ingots in one item", desc=[
        "&eWhat:&r any Extended Crafting singularity: iron, copper, gold, steel, aluminium, platinum and more.",
        "&eHow:&r insert 10,000 of one material into the Quantum Compressor, plus 5 million FE. Check JEI for the full list.",
        "&eTip:&r iron or copper is the easiest first pick: your ore lines make thousands an hour."]),
    Q("cn_ultimate_singularity", 7, 2, [item("extendedcrafting:ultimate_singularity")], "Ultimate Singularity", deps=["cn_ec_singularity"], xp=2000,
      optional=True, tokens=2, items=[(GT, 5)], subtitle="Optional: every singularity, in one", desc=[
        "&eWhat:&r one of every singularity, combined on the Ultimate Table.",
        "&eHow:&r there are 19 singularities in this pack (check JEI for the list). That's about 190,000 items in total.",
        "&eTip:&r this is a server project. Split the materials between players."]),
    # ---------------------------------------------------------------- right, y=4: pocket worlds
    Q("cn_pocket", 3, 4, [item("compactmachines:wall", 64), dim("compactmachines:compact_world")], "Worlds Within Worlds", deps=["t7_creation"], xp=300,
      optional=True, tokens=2, choice="pick_late", subtitle="Optional: a demigod should have rooms to spare", desc=[
        "&eWhat:&r Compact Machines are small rooms in their own dimension. You've made a new world; now make a few small ones.",
        "&eHow:&r 64 machine walls, then step inside any of your machines with the Personal Shrinking Device.",
        "&eTip:&r one room per production line keeps your main base clean and your server's tick time low."]),
    # ---------------------------------------------------------------- left, y=-3: walking the worlds
    Q("cn_bio_overworld", -3, -3, [biome("minecraft:mushroom_fields"), biome("minecraft:ice_spikes"), biome("minecraft:cherry_grove")], "Rare Ground",
      deps=["t7_creation"], xp=400, tokens=10, choice="pick_late", subtitle="The Overworld's rarest places", desc=[
        "&6You saw these places from above, long ago. Walk them this time.&r",
        "&eWhat:&r visit a Mushroom Fields island, an Ice Spikes plain and a Cherry Grove.",
        "&eHow:&r Explorer's Compass or Nature's Compass (if you have one) finds biomes; otherwise fly and look. Each completes on arrival.",
        "&eTip:&r Mushroom Fields never spawn hostile mobs. A good place for a quiet base."]),
    Q("cn_bio_under", -5, -3, [biome("minecraft:deep_dark"), biome("deeperdarker:echoing_forest"), biome("undergarden:frostfields")], "Under Everything",
      deps=["cn_bio_overworld"], xp=500, tokens=12, loot="boss", subtitle="Deep Dark, the Otherside, the Undergarden", desc=[
        "&eWhat:&r the Deep Dark, the Otherside's Echoing Forest, and the Undergarden's Frostfields.",
        "&eHow:&r the Deep Dark is under mountains in the Overworld; the Echoing Forest is in Deeper and Darker's Otherside; the Frostfields are in the Undergarden.",
        "&eTip:&r the Warden still doesn't care how powerful you are. Sneak."]),
    Q("cn_bio_nether", -7, -3, [biome("minecraft:soul_sand_valley"), biome("biomesoplenty:crystalline_chasm"), biome("biomesoplenty:withered_abyss")], "Fire Below",
      deps=["cn_bio_under"], xp=500, tokens=12, choice="pick_late", subtitle="The Nether's strangest corners", desc=[
        "&eWhat:&r a Soul Sand Valley and two of Biomes O' Plenty's rarer Nether biomes: the Crystalline Chasm and the Withered Abyss.",
        "&eChemistry:&r soul sand and soul soil burn with a blue flame. Real blue flames mean complete combustion; these are just strange.",
        "&eTip:&r the Withered Abyss has bottomless drops. Bring a way to fly."]),
    Q("cn_bio_twilight", -9, -3, [biome("twilightforest:enchanted_forest"), biome("twilightforest:glacier"), biome("twilightforest:highlands")], "Twilight Wanderer",
      deps=["cn_bio_nether"], xp=600, tokens=15, loot="boss", subtitle="Deep into the Twilight Forest", desc=[
        "&eWhat:&r the Enchanted Forest, the Glacier and the Highlands of the Twilight Forest.",
        "&eHow:&r the Glacier and Highlands are locked behind Twilight bosses. If a biome hurts you, you haven't beaten the boss that guards it yet.",
        "&eTip:&r the Enchanted Forest is small and rare. The Magic Map shows biomes as you explore."]),
    Q("cn_bio_end", -11, -3, [biome("minecraft:end_highlands"), biome("biomesoplenty:end_wilds"), biome("biomesoplenty:end_reef"), biome("biomesoplenty:end_corruption")], "Gardens of the End",
      deps=["cn_bio_twilight"], xp=600, tokens=15, choice="pick_late", subtitle="The outer End islands", desc=[
        "&eWhat:&r the End Highlands and three Biomes O' Plenty End biomes: the Wilds, the Reef and the Corruption.",
        "&eHow:&r take an End Gateway out past the main island. The BOP biomes are scattered among the outer islands.",
        "&eTip:&r End Cities in the Highlands hold Elytra and shulker shells."]),
    Q("cn_bio_space", -11, -1, [biome("ad_astra:martian_polar_caps"), biome("ad_astra:infernal_venus_barrens"), biome("ad_astra:mercury_deltas"), biome("ad_astra:glacio_ice_peaks")],
      "Other Skies", deps=["cn_bio_end"], xp=800, tokens=20, items=[(GT, 2)], subtitle="Four planets, four strange landscapes", desc=[
        "&eWhat:&r Mars's polar caps, Venus's infernal barrens, Mercury's deltas and Glacio's ice peaks.",
        "&eChemistry:&r Mars's polar caps are water ice under a layer of frozen CO₂ (dry ice). Venus's air is 96% CO₂ at 90 times Earth's pressure.",
        "&eHow:&r Tier 2 rocket for Mars, Tier 3 for Venus and Mercury, Tier 4 for Glacio. Netherite space suit for the hot ones.",
        "&eTip:&r set up a launch pad on each planet before you go exploring."]),
    # ---------------------------------------------------------------- left, y=2: the rarest elements
    Q("cn_noble", -3, 2, [anyof(NOBLE, 64)], "A Breath of Noble Gas", deps=["t7_creation"], xp=500,
      tokens=10, choice="pick_late", subtitle="64 of helium, neon, argon, krypton, xenon or radon", desc=[
        "&eWhat:&r any 64 noble gas items from ChemLib, in any mix.",
        "&eChemistry:&r noble gases have full outer electron shells, so they almost never react. Neon glows red in a discharge tube; xenon glows blue; radon is radioactive.",
        "&eHow:&r Alchemistry Dissolver on air-rich or gas-bearing items, or the Fusion Chamber (check JEI for which inputs give which gas).",
        "&eTip:&r helium is the lightest: fuse two hydrogen and you're there."]),
    Q("cn_lanthanides", -5, 2, [anyof(LANTHANIDES, 64)], "The Rare Earths", deps=["cn_noble"], xp=600,
      tokens=12, items=[(GT, 1)], subtitle="64 of any lanthanide, element 57 to 71", desc=[
        "&eWhat:&r any 64 lanthanide items from ChemLib: lanthanum through lutetium.",
        "&eChemistry:&r the lanthanides fill the 4f electron shell, which sits deep inside the atom. That's why they're so alike and so hard to separate.",
        "&eHow:&r Fusion Chamber (pairs that add up to 57-71) or the Dissolver on rare-earth-bearing items (check JEI).",
        "&eTip:&r neodymium makes the strongest permanent magnets; europium makes red phosphors in screens.",
        PB,
        "&eDeep dive: why 'rare' earths?&r",
        "They aren't rare. Cerium is about as common as copper in the Earth's crust. They're 'rare' because they never form rich deposits on their own.",
        "Separating them took chemists over a century. Their outer electrons are nearly the same, so their chemistry is nearly the same; only the slow shrinking of the atoms across the row (the lanthanide contraction) tells them apart.",
        "Industry separates them by solvent extraction, hundreds of stages long. Your Fusion Chamber skips all that."]),
    Q("cn_superheavy", -7, 2, [anyof(["chemlib:oganesson", "chemlib:tennessine", "chemlib:livermorium", "chemlib:moscovium", "chemlib:flerovium", "chemlib:nihonium"], 64)],
      "Island of Stability", deps=["cn_lanthanides"], xp=800, tokens=20, items=[(GT, 2)], subtitle="64 superheavy atoms, elements 113 to 118", desc=[
        "&eWhat:&r any 64 of the six newest elements: nihonium, flerovium, moscovium, livermorium, tennessine and oganesson.",
        "&eChemistry:&r all six were made in the last 25 years, a few atoms at a time, and decay within seconds or less.",
        "&eHow:&r Alchemistry Fusion Chamber. Automate the inputs and let it run.",
        "&eTip:&r physicists predict an 'island of stability' near 114 protons and 184 neutrons, where superheavy nuclei might last much longer. No one has reached it yet."]),
    # ---------------------------------------------------------------- finale
    Q("cn_demigod", 0, 7, [tick()], "Demigod", deps=["cn_terraformer", "cn_quantum_armor", "cn_atomic", "cn_ec_singularity", "cn_bio_space", "cn_superheavy", "cn_echo"],
      xp=5000, size=2.0, shape="gear", tokens=30, loot="boss", items=[(GT, 5)], subtitle="Nothing left to remember", desc=[
        "&6You don't remember being this any more. You simply are.&r",
        "&eWhat:&r you've planted the Seed, walked every world, built armour from a collapsed star, and held the whole periodic table.",
        "&eNow:&r build. A city, a garden on Mars, a pocket world for every friend on the server. The tools are yours.",
        "&6The new world is waiting. It's whatever you make it.&r"]),
    # ---------------------------------------------------------------- secrets
    Q("cn_secret_diamond", 5, -6, [item("minecraft:diamond", 64)], "Pressure Not Required", deps=["cn_nucleo"], xp=300,
      secret=True, loot="secret", tokens=2, subtitle="Secret: coal, rewritten into diamond", desc=[
        "&eWhat:&r the Nucleosynthesizer turns coal into diamond with 4 mB of antimatter. You found it.",
        "&eChemistry:&r both are carbon. Graphite and diamond differ only in how the atoms bond: sheets of rings versus a rigid 3D lattice. Nature needs about 50,000 atmospheres to make the change.",
        "&eTip:&r 64 diamonds from 64 coal. Your younger self, swinging an iron pickaxe, would be furious."]),
    Q("cn_secret_origin", -5, -5, [biome("biomesoplenty:origin_valley")], "Where It Began", deps=["cn_bio_overworld"], xp=300,
      secret=True, loot="secret", tokens=2, subtitle="Secret: the oldest-looking valley", desc=[
        "&eWhat:&r Biomes O' Plenty's Origin Valley, built to look like the very first versions of Minecraft.",
        "&6Bright grass, roses, plain old trees. You remember a world this simple. It was the first one you made.&r",
        "&eTip:&r it's rare. If you found it by chance, consider it a gift."]),

    # ---------------------------------------------------------------- ATM10-aligned additions (2026-10-19)
    Q("cn_ultradense", 3, -3, [item(MI + "ultradense_metal_ball")], "Ultradense Metal Ball", deps=["t7_creation"], xp=500,
      tokens=10, subtitle="The heaviest thing you can hold", desc=[
        "&eWhat:&r the core that 64 nukes crush into a singularity.",
        "&eChemistry:&r tungsten, lead and iridium are among the densest metals there are. Iridium and osmium tie for the record at about 22.6 g/cm³, twice as dense as lead.",
        "&eHow:&r Assembler: 4 tungsten large plates, 4 lead plates and 1 iridium plate."]),
    Q("cn_opt_qsword", 9, -4, [item(MI + "quantum_sword")], "Quantum Sword", deps=["cn_quantum_upgrade"], xp=500,
      optional=True, tokens=5, subtitle="Optional: one upgrade, one blade", desc=[
        "&eWhat:&r MI's quantum sword: the MI guidebook claims it vaporises anything it hits.",
        "&eHow:&r MI Packer: netherite sword + 1 quantum upgrade, at the same huge draw as the armour (check JEI).",
        "&eTip:&r a quantum upgrade is a lot to spend on a sword. Finish the armour first."]),
], links=[("t7_seed", -3, 0), ("t7_opt_nucleo", 3, -6)])
