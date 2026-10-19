"""Quest chapter: explore (structure and biome discovery). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Moved here from worlds.py (keys unchanged): w_dungeon, w_mineshaft. New quests use the ex_ prefix.
2026-10-18: ex_compass removed (same tasks as q_compass in qol.py, linked instead); w_town merged into ex_village;
the optional villages are siblings of ex_village instead of a chain.
Only structures that generate in this pack: vanilla, YUNG's Better Dungeons/Mineshafts/Strongholds, Towns and Towers.
Biome quests avoid the biomes already used by the completionist tours (completionist.py).
Rows: villages y=0, dungeons and ruins y=3/5/7, oceans y=9, the Nether y=12.5, biomes y=16/17.5.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

MC = "minecraft:"
TT = "towns_and_towers:"
BOP = "biomesoplenty:"
RU = "regions_unexplored:"

CHAPTER = Chapter("explore", "Exploration", "naturescompass:naturescompass",
        ["Go and see what the world has made without you."], SIDE, [
    # --- villages and outposts (y=0) -----------------------------------------------------------
    Q("ex_village", 0, 0, [structure(MC + "village_plains")], "A Plains Village", deps=["gs_iron"], xp=40,
      loot="hunt", subtitle="Neighbours, at last", desc=[
        "&6You remember knowing every corner of this world by heart. For now, a compass will do.&r",
        "&eWhat:&r villagers trade emeralds for crops, tools and enchanted books, and their beds and fields are free for the taking (politely).",
        "&eHow:&r plains villages generate in plains and a few grassy modded biomes. Walk into one. Nature's Compass and Explorer's Compass (the &eFind Anything&r quest, linked on the left) point you to any biome or structure on this page.",
        "&eTip:&r Towns and Towers adds a village style for most biomes (the optional villages next to this one), and villages often have a waystone. A cartographer villager sells maps to ocean monuments and woodland mansions."]),
    Q("ex_tt_forest", 6, 0, [structure(TT + "village_forest")], "A Forest Village", deps=["ex_village"], xp=40,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: timber houses under the trees", desc=[
        "&eWhat:&r Towns and Towers builds a village style for each biome. The forest village is timber and cobblestone.",
        "&eHow:&r find one in a forest biome (Explorer's Compass: Towns and Towers) and walk in.",
        "&eTip:&r each biome style has its own loot chests."]),
    Q("ex_tt_meadow", 8, 0, [structure(TT + "village_meadow")], "A Meadow Village", deps=["ex_village"], xp=40,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: a village in the mountain meadows", desc=[
        "&eWhat:&r high meadows below the peaks get their own village style.",
        "&eHow:&r find a meadow biome on a mountainside and the village in it.",
        "&eTip:&r meadows are where bees and wildflowers are thickest."]),
    Q("ex_tt_snowy", 10, 0, [structure(TT + "village_snowy_taiga")], "A Snowy Taiga Village", deps=["ex_village"], xp=40,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: spruce and snow", desc=[
        "&eWhat:&r a village built for the cold, in the snowy taiga.",
        "&eHow:&r find a snowy taiga and the village in it.",
        "&eTip:&r bring leather boots for powder snow."]),
    Q("ex_tt_swamp", 12, 0, [structure(TT + "village_swamp")], "A Swamp Village", deps=["ex_village"], xp=40,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: houses on stilts", desc=[
        "&eWhat:&r vanilla never put villages in swamps. Towns and Towers does.",
        "&eHow:&r find a swamp and the village in it.",
        "&eTip:&r witches love swamps too; keep a milk bucket handy."]),
    Q("ex_desert_village", 4, 0, [structure(MC + "village_desert")], "A Desert Village", deps=["ex_village"], xp=40,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: sandstone in the sun", desc=[
        "&eWhat:&r a sandstone village in the desert.",
        "&eChemistry:&r sandstone is sand grains (mostly quartz, SiO₂) cemented by minerals like calcite or iron oxides that precipitated from groundwater.",
        "&eHow:&r find a desert village (Explorer's Compass) and walk in."]),
    Q("ex_outpost", 2, 0, [structure(TT + "pillager_outpost_forest")], "A Pillager Outpost", deps=["ex_village"], xp=60,
      loot="hunt", subtitle="The villagers' enemies have towers too", desc=[
        "&eWhat:&r pillagers build watchtowers. Towns and Towers gives each biome its own design.",
        "&eHow:&r find a forest outpost and walk in. Expect crossbow fire.",
        "&eTip:&r killing a pillager captain gives Bad Omen; in 1.21 you drink the ominous bottle it drops to start a raid."]),
    Q("ex_mansion", 2, -2, [structure(MC + "mansion")], "A Woodland Mansion", deps=["ex_outpost"], xp=150,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: the illagers' stronghold", desc=[
        "&eWhat:&r huge dark-oak mansions, very rare, deep in dark forests. Vindicators and evokers live inside.",
        "&eHow:&r a cartographer's woodland explorer map or the Explorer's Compass. Step inside.",
        "&eTip:&r evokers drop totems of undying; vindicators hit very hard."]),

    # --- ruins and dungeons (y=3, 5, 7) ---------------------------------------------------------
    Q("w_dungeon", 0, 5, [tick()], "Better Dungeons", deps=["gs_iron"], xp=50,
      optional=True, tokens=1, subtitle="Optional: clear a YUNG's dungeon", desc=[
        "&eWhat:&r YUNG's Better Dungeons adds catacombs, fortresses and spider caves underground.",
        "&eHow:&r find one (the Explorer's Compass lists them), clear it and loot it. Click the checkmark when done.",
        "&eTip:&r some dungeon chests hold Relics and Artifacts items."]),
    Q("ex_zombie_dungeon", 0, 3, [structure("betterdungeons:zombie_dungeon")], "Zombie Catacombs", deps=["gs_iron"], xp=60,
      loot="hunt", subtitle="A tomb full of the restless dead", desc=[
        "&eWhat:&r YUNG's zombie dungeon: a tomb with spawners, coffins and loot.",
        "&eHow:&r find it with the Explorer's Compass (Better Dungeons) and step inside.",
        "&eTip:&r break or torch the spawners first; then loot at your leisure."]),
    Q("ex_skeleton_dungeon", 2, 3, [structure("betterdungeons:skeleton_dungeon")], "Skeleton Fortress", deps=["ex_zombie_dungeon"], xp=80,
      loot="hunt", subtitle="A buried fort of archers", desc=[
        "&eWhat:&r YUNG's skeleton dungeon is a sprawling underground fort.",
        "&eHow:&r find it and step inside. Bring a shield.",
        "&eTip:&r torches on every spawner; skeletons will pick you off from the dark otherwise."]),
    Q("ex_spider_dungeon", 4, 3, [structure("betterdungeons:spider_dungeon")], "Spider Caves", deps=["ex_skeleton_dungeon"], xp=80,
      loot="hunt", subtitle="Webs everywhere", desc=[
        "&eWhat:&r a natural-looking cave full of webs, cave spiders and their spawners.",
        "&eChemistry:&r real spider silk is a protein (spidroin) with crystalline β-sheets that make it, weight for weight, stronger than steel.",
        "&eHow:&r find one and step inside. A sword or shears cut webs fast.",
        "&eTip:&r cave spiders poison; carry milk."]),
    Q("ex_stronghold", 6, 3, [structure("betterstrongholds:stronghold")], "A Better Stronghold", deps=["ex_spider_dungeon"], xp=120,
      loot="hunt", subtitle="Where the End portal hides", desc=[
        "&eWhat:&r YUNG's Better Strongholds replaces the vanilla stronghold with a much larger, trapped maze. The End portal room is inside.",
        "&eHow:&r throw eyes of ender, or use the Explorer's Compass. Step inside.",
        "&eTip:&r mark your path with torches on one side; the halls all look alike."]),
    Q("w_mineshaft", 4, 7, [tick()], "Better Mineshafts", deps=["gs_iron"], xp=30,
      optional=True, tokens=1, subtitle="Optional: explore a YUNG's mineshaft", desc=[
        "&eWhat:&r YUNG's Better Mineshafts are longer, with ore deposits, carts and loot.",
        "&eHow:&r explore one and loot a chest. Click the checkmark when done.",
        "&eTip:&r look for minecarts with chests along the tracks."]),
    Q("ex_mineshaft", 0, 7, [structure("bettermineshafts:mineshaft_oak")], "An Old Mineshaft", deps=["gs_iron"], xp=40,
      loot="hunt", subtitle="Someone mined here before you", desc=[
        "&eWhat:&r YUNG's mineshafts come in styles for each biome. The oak style is the common one.",
        "&eHow:&r find one under a forest or plains (Explorer's Compass) and walk in.",
        "&eTip:&r the rails and planks are free building material."]),
    Q("ex_mineshaft_deep", 2, 7, [structure("bettermineshafts:mineshaft_dripstone"), structure("bettermineshafts:mineshaft_lush")], "Mineshafts of the Caves",
      deps=["ex_mineshaft"], xp=80, optional=True, tokens=1, loot="hunt", subtitle="Optional: dripstone and lush styles", desc=[
        "&eWhat:&r two mineshafts built into cave biomes: one among dripstone, one among moss and glow berries.",
        "&eChemistry:&r dripstone is calcium carbonate: water carrying dissolved Ca(HCO₃)₂ drips, loses CO₂, and leaves CaCO₃ behind, a millimetre at a time.",
        "&eHow:&r find a mineshaft under dripstone caves and one under lush caves."]),
    Q("ex_trail_ruins", 8, 5, [structure(MC + "trail_ruins"), item(MC + "brush")], "Trail Ruins", deps=["gs_iron"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: dig like an archaeologist", desc=[
        "&eWhat:&r half-buried ruins of an old people. Suspicious gravel hides pottery sherds and armour trims.",
        "&eHow:&r find the ruins (Explorer's Compass) and bring a brush (feather, copper ingot, stick).",
        "&eTip:&r brush slowly; breaking suspicious blocks destroys the loot."]),
    Q("ex_trial", 8, 3, [structure(MC + "trial_chambers"), item(MC + "trial_key")], "Trial Chambers", deps=["ex_stronghold"], xp=120,
      loot="hunt", subtitle="Copper halls and trial spawners", desc=[
        "&eWhat:&r copper and tuff vaults deep underground. Trial spawners give keys; keys open vaults.",
        "&eChemistry:&r the halls show copper's patina: Cu weathers to green basic copper carbonate, Cu₂CO₃(OH)₂, unless you wax it.",
        "&eHow:&r find a chamber, beat a trial spawner's wave and take the key.",
        "&eTip:&r breezes deflect arrows; fight them up close."]),
    Q("ex_temples", 2, 5, [structure(MC + "desert_pyramid"), structure(MC + "jungle_pyramid")], "Temples", deps=["gs_iron"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: desert and jungle", desc=[
        "&eWhat:&r a desert pyramid and a jungle temple, each with treasure and a trap.",
        "&eChemistry:&r the desert trap is TNT: trinitrotoluene, C₇H₅N₃O₆, which carries its oxygen inside the molecule.",
        "&eHow:&r find one of each. Don't stand on the pressure plate in the desert."]),
    Q("ex_huts", 4, 5, [structure(MC + "swamp_hut"), structure(MC + "igloo")], "Odd Little Houses", deps=["gs_iron"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: a witch's hut and an igloo", desc=[
        "&eWhat:&r a witch's hut in the swamp and an igloo on the snow. Some igloos hide a basement.",
        "&eHow:&r find one of each and step inside.",
        "&eTip:&r the igloo basement has a brewing stand and a golden apple for curing a zombie villager."]),
    Q("ex_ruined_portal", 6, 5, [structure(MC + "ruined_portal")], "A Ruined Portal", deps=["gs_iron"], xp=50,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: someone tried to leave", desc=[
        "&eWhat:&r broken Nether portals, with crying obsidian and a chest of gold.",
        "&eChemistry:&r obsidian forms when lava (molten silicate) cools so fast it can't crystallise: it's volcanic glass.",
        "&eHow:&r find one and stand inside it. Fill the missing blocks to repair the portal."]),

    # --- oceans (y=9) --------------------------------------------------------------------------
    Q("ex_shipwreck", 0, 9, [structure(MC + "shipwreck")], "A Shipwreck", deps=["gs_iron"], xp=50,
      loot="hunt", subtitle="Someone else's bad day at sea", desc=[
        "&eWhat:&r sunken ships with supply, treasure and map chests. The map leads to buried treasure.",
        "&eHow:&r find a wreck (Explorer's Compass) and swim inside.",
        "&eTip:&r a potion of water breathing or a turtle shell helmet makes this easy."]),
    Q("ex_treasure", 2, 9, [structure(MC + "buried_treasure"), item(MC + "heart_of_the_sea")], "Buried Treasure", deps=["ex_shipwreck"], xp=80,
      loot="hunt", subtitle="X marks the spot", desc=[
        "&eWhat:&r buried chests on beaches, each with a Heart of the Sea for a conduit.",
        "&eHow:&r follow a shipwreck's treasure map to the X and dig down.",
        "&eTip:&r the chest is usually right under the X, a few blocks down."]),
    Q("ex_ocean_ruins", 2, 10.5, [structure(MC + "ocean_ruin_warm"), structure(MC + "ocean_ruin_cold")], "Ocean Ruins", deps=["ex_shipwreck"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: sandstone and stone ruins underwater", desc=[
        "&eWhat:&r ruins on the sea floor: sandstone ones in warm water, stone bricks in cold.",
        "&eChemistry:&r warm-water coral reefs are calcium carbonate skeletons; more dissolved CO₂ makes seawater more acidic and dissolves them.",
        "&eHow:&r find one of each. Drowned guard them."]),
    Q("ex_wreckage", 0, 10.5, [structure(TT + "wreckage_ocean")], "Wreckage", deps=["ex_shipwreck"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: a Towns and Towers wreck", desc=[
        "&eWhat:&r Towns and Towers scatters its own wreckage across the oceans.",
        "&eHow:&r find it with the Explorer's Compass (Towns and Towers) and swim in.",
        "&eTip:&r boats are faster than swimming between ocean structures."]),
    Q("ex_monument", 4, 9, [structure(MC + "monument"), item(MC + "wet_sponge", 4)], "An Ocean Monument", deps=["ex_treasure"], xp=150,
      loot="hunt", subtitle="The guardians' temple", desc=[
        "&eWhat:&r a prismarine temple guarded by guardians and three elder guardians. Its sponge rooms and gold block vault are the prize.",
        "&eChemistry:&r a sponge holds water by capillary action in its pores; dry it in a furnace to drive the water off.",
        "&eHow:&r find it with a cartographer's map or the Explorer's Compass. Bring water breathing and Respiration.",
        "&eTip:&r elder guardians give Mining Fatigue; kill all three to lift it (see the hunting page)."]),

    # --- the Nether (y=12.5) --------------------------------------------------------------------
    Q("ex_fortress", 0, 12.5, [structure(MC + "fortress")], "A Nether Fortress", deps=["t2_nether"], xp=80,
      loot="hunt", subtitle="Blazes and wither skeletons", desc=[
        "&eWhat:&r dark nether-brick bridges and halls. Blazes give blaze rods; wither skeletons drop skulls for the Wither.",
        "&eHow:&r fortresses run in long lines across the Nether; the Explorer's Compass finds them quickly.",
        "&eTip:&r nether wart grows in the fortress stairwells; take some for brewing."]),
    Q("ex_bastion", 2, 12.5, [structure(MC + "bastion_remnant")], "A Bastion Remnant", deps=["ex_fortress"], xp=100,
      loot="hunt", subtitle="The piglins' castle", desc=[
        "&eWhat:&r blackstone castles full of piglins and gold. Some hide netherite upgrade templates and ancient debris.",
        "&eChemistry:&r gold doesn't tarnish because it's the least reactive metal: it won't oxidise in air, even at high temperatures.",
        "&eHow:&r wear one piece of gold armour so piglins stay calm, then step inside.",
        "&eTip:&r opening chests angers piglins anyway; piglin brutes ignore gold entirely."]),
    Q("ex_nether_fossil", 0, 14, [structure(MC + "nether_fossil")], "Nether Fossils", deps=["ex_fortress"], xp=50,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: bones in the soul sand", desc=[
        "&eWhat:&r giant bone fossils in the soul sand valleys.",
        "&eChemistry:&r bone is mostly hydroxyapatite, Ca₅(PO₄)₃(OH): a calcium phosphate mineral, the same family as phosphate rock for fertiliser.",
        "&eHow:&r find a soul sand valley and walk into one of the bone arches."]),
    Q("ex_nether_dungeon", 2, 14, [structure("betterdungeons:small_nether_dungeon")], "A Nether Dungeon", deps=["ex_fortress"], xp=60,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: YUNG's small Nether dungeon", desc=[
        "&eWhat:&r Better Dungeons adds small dungeons to the Nether too, with spawners and loot.",
        "&eHow:&r find one with the Explorer's Compass and step inside.",
        "&eTip:&r fire resistance first; everything here burns."]),
    Q("ex_nether_portal", 4, 14, [structure(MC + "ruined_portal_nether")], "Ruins in the Fire", deps=["ex_bastion"], xp=50,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: a ruined portal on the other side", desc=[
        "&eWhat:&r ruined portals turn up in the Nether as well, with the same gold chest.",
        "&eHow:&r find one in the Nether and stand inside it.",
        "&eTip:&r crying obsidian makes respawn anchors, which let you respawn in the Nether."]),
    Q("ex_inferno", 4, 12.5, [biome(BOP + "erupting_inferno")], "Erupting Inferno", deps=["ex_bastion"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: Biomes O' Plenty's angriest Nether biome", desc=[
        "&eWhat:&r a Nether biome of lava, ash and erupting vents.",
        "&eChemistry:&r volcanic gas is mostly water vapour, CO₂ and SO₂; the SO₂ is what makes volcanic air sting.",
        "&eHow:&r Nature's Compass finds it. Fire resistance is a must."]),

    # --- biomes of Biomes O' Plenty and Regions Unexplored (y=16, 17.5) -----------------------
    Q("ex_bio_chalk", 0, 16, [biome(RU + "chalk_cliffs"), biome(RU + "towering_cliffs")], "Cliffs of Chalk", deps=["gs_iron"], xp=60,
      loot="hunt", subtitle="White cliffs and tall stone", desc=[
        "&eWhat:&r two Regions Unexplored cliff biomes: white chalk and towering stone.",
        "&eChemistry:&r chalk is calcium carbonate (CaCO₃) made of the shells of tiny sea plankton. Heat it and it gives quicklime: CaCO₃ → CaO + CO₂.",
        "&eHow:&r Nature's Compass finds each one. Visit both."]),
    Q("ex_bio_springs", 2, 16, [biome(BOP + "hot_springs"), biome(BOP + "volcanic_plains")], "Hot Ground", deps=["ex_bio_chalk"], xp=60,
      loot="hunt", subtitle="Springs and volcanic plains", desc=[
        "&eWhat:&r two Biomes O' Plenty biomes warmed from below.",
        "&eChemistry:&r hot springs carry dissolved minerals; when the water cools at the surface, silica and carbonates precipitate as terraces.",
        "&eHow:&r visit both (Nature's Compass)."]),
    Q("ex_bio_wetlands", 4, 16, [biome(BOP + "bog"), biome(BOP + "marsh"), biome(RU + "fen")], "Wetlands", deps=["ex_bio_springs"], xp=80,
      loot="hunt", subtitle="Bog, marsh and fen", desc=[
        "&eWhat:&r three kinds of wetland from the two biome mods.",
        "&eChemistry:&r waterlogged peat has almost no oxygen, so it barely rots; microbes there make methane (CH₄), the original \"marsh gas\".",
        "&eHow:&r visit all three. Bring a boat."]),
    Q("ex_bio_caves", 6, 16, [biome(RU + "redstone_caves"), biome(RU + "bioshroom_caves"), biome(BOP + "glowing_grotto")], "Caves That Glow", deps=["ex_bio_wetlands"], xp=100,
      loot="hunt", subtitle="Three cave biomes with their own light", desc=[
        "&eWhat:&r cave biomes lit by redstone, giant glowing mushrooms and glowing fungi.",
        "&eChemistry:&r real glowing fungi use the same chemistry as fireflies: luciferin oxidised by O₂ with the help of an enzyme, luciferase.",
        "&eHow:&r these are underground; Nature's Compass gives the location, then dig down."]),
    Q("ex_bio_forests", 0, 17.5, [biome(BOP + "maple_woods"), biome(RU + "eucalyptus_forest"), biome(BOP + "orchard")], "Useful Forests", deps=["ex_bio_chalk"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: maple, eucalyptus and fruit trees", desc=[
        "&eWhat:&r three forests whose real trees give us chemicals.",
        "&eChemistry:&r maple sap is about 2% sucrose (C₁₂H₂₂O₁₁), boiled down 40:1 into syrup. Eucalyptus oil is mostly eucalyptol (C₁₀H₁₈O).",
        "&eHow:&r visit all three."]),
    Q("ex_bio_dry", 2, 17.5, [biome(RU + "joshua_desert"), biome(RU + "saguaro_desert"), biome(RU + "outback")], "Dry Country", deps=["ex_bio_springs"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: three Regions Unexplored deserts", desc=[
        "&eWhat:&r Joshua trees, saguaro cacti and the red outback.",
        "&eChemistry:&r red desert soil is coloured by a thin coat of iron(III) oxide, Fe₂O₃, on every grain: the same rust that colours Mars.",
        "&eHow:&r visit all three. Carry water."]),
    Q("ex_bio_cold", 4, 17.5, [biome(BOP + "tundra"), biome(RU + "icy_heights"), biome(BOP + "snowblossom_grove")], "Cold Places", deps=["ex_bio_wetlands"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: tundra, icy heights and snowblossoms", desc=[
        "&eWhat:&r three cold biomes from the biome mods.",
        "&eChemistry:&r ice floats because water expands about 9% when it freezes: hydrogen bonds lock the molecules into an open hexagonal lattice.",
        "&eHow:&r visit all three. Warm clothes not required, but recommended."]),
    Q("ex_bio_flowers", 6, 17.5, [biome(RU + "poppy_fields"), biome(BOP + "jacaranda_glade"), biome(RU + "wisteria_grove")], "Colour Fields", deps=["ex_bio_caves"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: red, purple and violet", desc=[
        "&eWhat:&r biomes full of flowers: poppies, jacarandas and wisteria.",
        "&eChemistry:&r most red, purple and blue petals owe their colour to anthocyanins, pigments that change colour with pH (red in acid, blue in base).",
        "&eHow:&r visit all three. Collect the flowers for dyes."]),
    Q("ex_bio_heights", 8, 16, [biome(RU + "spires"), biome(BOP + "crag")], "Strange Heights", deps=["ex_bio_caves"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: spires and crags", desc=[
        "&eWhat:&r tall rock spires and broken crags: two of the most dramatic landscapes in the pack.",
        "&eChemistry:&r rock spires are what's left when softer rock around them is weathered away by water, frost and slow acid rain (H₂CO₃ from dissolved CO₂).",
        "&eHow:&r visit both. Bring a water bucket for the way down."]),
    Q("ex_bio_waste", 8, 17.5, [biome(BOP + "wasteland"), biome(BOP + "dead_forest")], "Dead Lands", deps=["ex_bio_caves"], xp=80,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: where nothing grows", desc=[
        "&eWhat:&r cracked wasteland and grey dead forest.",
        "&eChemistry:&r soil dies when it loses organic matter and nitrogen; your Haber-Bosch ammonia (N₂ + 3H₂ → 2NH₃) is how real farms put nitrogen back.",
        "&eHow:&r visit both. A demigod might one day make them green again."]),
    Q("ex_origin", 10, 16, [biome(BOP + "origin_valley")], "The Origin Valley", deps=["ex_bio_heights"], xp=100,
      secret=True, loot="secret", subtitle="Secret: the world as it first was", desc=[
        "&6Blocky trees, bright grass, a sky of old. You remember the world looking exactly like this, once.&r",
        "&eWhat:&r a rare Biomes O' Plenty biome styled after Minecraft's earliest days.",
        "&eTip:&r there's a snowy version too, the wintry origin valley."]),
], links=[("gs_iron", -2, 0), ("q_compass", -2, 2), ("t2_nether", -2, 12.5)])
