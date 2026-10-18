"""Quest chapter: worlds. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("worlds", "Other Worlds", "deeperdarker:heart_of_the_deep",
        ["Realms beyond the Overworld."], SIDE, [
    # --- The End (y=0) -------------------------------------------------------------------------
    Q("w_end", 0, 0, [dim("minecraft:the_end")], "The End", deps=["t2_nether"], xp=200,
      subtitle="Eyes of ender, a stronghold, a portal", desc=[
        "&6You remember the edge of the world. It's closer than it used to be.&r",
        "&eWhat:&r the End holds the dragon, End Cities, shulkers and azure silver ore. End Crystals power Just Dire Things' flight upgrade.",
        "&eHow:&r throw eyes of ender to find a stronghold, fill the portal frame and jump in.",
        "&eTip:&r bring blocks, a bow and slow-falling potions. YUNG's Better Strongholds make the hunt more interesting."]),
    Q("w_dragon", 2, 0, [item("minecraft:dragon_breath", 4)], "The Dragon", deps=["w_end"], xp=200,
      subtitle="Defeat the dragon and bottle its breath", desc=[
        "&eWhat:&r defeating the Ender Dragon opens the outer End islands. Its breath makes lingering potions.",
        "&eHow:&r destroy the End Crystals on the pillars first, then fight. Catch the purple breath cloud in glass bottles.",
        "&eTip:&r crystals respawn the dragon when placed on the exit portal, if you need it again."]),
    Q("w_elytra", 4, 0, [item("minecraft:elytra"), item("minecraft:shulker_shell", 4)], "End City Loot", deps=["w_dragon"], xp=250,
      subtitle="Wings and shulker shells", desc=[
        "&eWhat:&r End Cities hold elytra (on the end ships) and shulkers whose shells make shulker boxes.",
        "&eHow:&r take an End Gateway from the main island, then search the outer islands for purple towers.",
        "&eTip:&r the Angel Ring needs an elytra; shulker shells feed Silent Gear's tyrian steel."]),

    # --- The Deep Dark (y=2.5) -----------------------------------------------------------------
    Q("w_ancient", 0, 2.5, [tick()], "An Ancient City", deps=["t2_nether"], xp=100,
      subtitle="Find the city beneath the deep dark", desc=[
        "&eWhat:&r Ancient Cities sit deep below the Overworld in the deep dark. Each one's centre holds the frame of a portal to the Otherside.",
        "&eHow:&r the Explorer's Compass can find one. Sneak everywhere: shriekers summon the Warden. Click the checkmark once you're inside.",
        "&eTip:&r sneaking never triggers sculk sensors, and walking on wool doesn't either."]),
    Q("w_otherside", 2, 2.5, [item("deeperdarker:heart_of_the_deep"), dim("deeperdarker:otherside")], "The Otherside", deps=["w_ancient"], xp=300,
      subtitle="Take the Warden's heart and step through", desc=[
        "&6You remember a silence older than the world. You can hear it again.&r",
        "&eWhat:&r beyond the Ancient City lies the Otherside, a dark dimension of sculk and echo trees.",
        "&eHow:&r defeat a Warden for its Heart of the Deep, then use it to light the portal frame in the city's centre.",
        "&eTip:&r the Warden is blind but hears everything. Fight from range and keep moving."]),
    Q("w_echo", 4, 2.5, [item("deeperdarker:reinforced_echo_shard", 4)], "Echoes of the Deep", deps=["w_otherside"], xp=200,
      subtitle="The Otherside's strongest material", desc=[
        "&eWhat:&r reinforced echo shards make Warden gear that rivals netherite.",
        "&eHow:&r check JEI for the recipe; echo shards come from Ancient City chests and Otherside loot.",
        "&eTip:&r Warden armour is a netherite smithing upgrade, so keep your netherite gear."]),
    Q("w_soul_elytra", 3, 4, [item("deeperdarker:soul_elytra")], "Soul Elytra", deps=["w_otherside", "w_elytra"], xp=150,
      optional=True, tokens=1, subtitle="Optional: an elytra with its own boost", desc=[
        "&eWhat:&r an upgraded elytra that boosts itself, no rockets needed.",
        "&eHow:&r an elytra, sculk bones (from Shattered), a soul crystal (from Stalkers) and soul dust (check JEI).",
        "&eTip:&r Stalkers and Shattered roam the Otherside; fight them at range."]),
    Q("w_warden_armor", 5, 4, [item("deeperdarker:warden_chestplate")], "Warden Armour", deps=["w_echo"], xp=200,
      optional=True, tokens=2, subtitle="Optional: beyond netherite", desc=[
        "&eWhat:&r Warden armour is tougher than netherite.",
        "&eHow:&r netherite chestplate + reinforced echo shard + Warden upgrade template in a smithing table.",
        "&eTip:&r check JEI for where the Warden upgrade template comes from."]),

    # --- The Undergarden (y=6) -----------------------------------------------------------------
    Q("w_undergarden", 0, 6, [item("undergarden:cloggrum_ingot", 8), item("undergarden:froststeel_ingot", 4), item("undergarden:utherium_crystal", 4)], "Undergarden Metals",
      deps=["t4_undergarden"], xp=200, subtitle="Cloggrum, froststeel and utherium", desc=[
        "&eWhat:&r new ores beneath the world: cloggrum (tough), froststeel (slows what it hits) and utherium (hurts rotspawn).",
        "&eHow:&r mine them in depthrock and shiverstone, then smelt.",
        "&eTip:&r run them through the Alchemistry Dissolver: what are these strange metals made of?"]),
    Q("w_regalium", 2, 6, [item("undergarden:regalium_crystal", 4)], "Regalium", deps=["w_undergarden"], xp=150,
      subtitle="The Undergarden's precious crystal", desc=[
        "&eWhat:&r regalium is the Undergarden's treasure: a rare crystal in depthrock and shiverstone.",
        "&eHow:&r smelt regalium ore. It also turns up in catacomb chests.",
        "&eTip:&r catacombs are also where the Forgotten Guardian waits."]),
    Q("w_forgotten", 4, 6, [item("undergarden:forgotten_ingot")], "The Forgotten Guardian", deps=["w_regalium"], xp=300,
      size=1.5, subtitle="Defeat the catacombs' guardian", desc=[
        "&6You remember the old guardians and the oaths they swore. This one has forgotten its own.&r",
        "&eWhat:&r the Forgotten Guardian drops forgotten nuggets; nine make a Forgotten Ingot for the strongest Undergarden tools.",
        "&eHow:&r find a catacomb, beat the guardian, and craft the nuggets into an ingot. The smithing template is in catacomb chests.",
        "&eTip:&r it hits hard; armour up and keep your distance between swings."]),

    # --- The Twilight Forest (y=8.5 and 10) ----------------------------------------------------
    Q("w_naga", 0, 8.5, [item("twilightforest:naga_scale", 4)], "The Naga", deps=["t5_twilight"], xp=200,
      subtitle="The Twilight Forest's first boss", desc=[
        "&6You remember this twilight. You walked here once, when the forest was young.&r",
        "&eWhat:&r a great serpent coiled in a stone courtyard. Its scales unlock the path forward.",
        "&eHow:&r find the courtyard (the Magic Map helps). Hit it when it stops charging; stay out of its coils.",
        "&eTip:&r each boss you beat lifts the barrier on the next region."]),
    Q("w_lich", 2, 8.5, [item("twilightforest:lich_trophy")], "The Lich", deps=["w_naga"], xp=300,
      subtitle="A sorcerer atop a tower", desc=[
        "&eWhat:&r the Lich commands shields and clones from its tower. Beating it opens the swamp and the snowy forest.",
        "&eHow:&r break the shields orbiting it, then attack. Watch out for its shadow clones.",
        "&eTip:&r its tower is a long climb; bring food and blocks."]),
    Q("w_minoshroom", 4, 8.5, [item("twilightforest:minoshroom_trophy")], "The Minoshroom", deps=["w_lich"], xp=300,
      subtitle="The boss at the labyrinth's heart", desc=[
        "&eWhat:&r a mushroom minotaur in the swamp labyrinth. It drops meef stroganoff and a mighty axe.",
        "&eHow:&r the Maze Map helps you find it in the maze. Sidestep its charges.",
        "&eTip:&r meef stroganoff is one of the best foods in the forest."]),
    Q("w_hydra", 6, 8.5, [item("twilightforest:hydra_trophy"), item("twilightforest:fiery_blood", 2)], "The Hydra", deps=["w_minoshroom"], xp=400,
      subtitle="Three heads in the fire swamp", desc=[
        "&eWhat:&r the Hydra breathes fire from three heads. Its fiery blood makes fiery ingots.",
        "&eHow:&r fire resistance potions help. Hit the heads when they lunge at you; they regrow, so keep up the pressure.",
        "&eTip:&r its fire swamp is full of lava and fire; fire resistance is a must."]),
    Q("w_tf_metals", 8, 8.5, [item("twilightforest:ironwood_ingot", 4), item("twilightforest:knightmetal_ingot", 4), item("twilightforest:fiery_ingot", 2)], "Twilight Metals",
      deps=["w_hydra"], xp=250, subtitle="Ironwood, knightmetal and fiery metal", desc=[
        "&eWhat:&r alloys found nowhere else, for strong tools and armour.",
        "&eHow:&r ironwood: smelt raw ironwood (liveroot, iron, gold). Knightmetal: smelt armour shard clusters from the dark forest. Fiery: iron + a vial of fiery blood or tears.",
        "&eTip:&r knightmetal armour and tools are great against the Knight Phantoms."]),
    Q("w_knight", 10, 8.5, [item("twilightforest:knight_phantom_trophy")], "The Knight Phantoms", deps=["w_tf_metals"], xp=400,
      subtitle="Six ghosts in the goblin stronghold", desc=[
        "&eWhat:&r six phantom knights guard the Goblin Stronghold in the dark forest.",
        "&eHow:&r they wait deep inside the stronghold. Knightmetal armour helps.",
        "&eTip:&r they come in waves; fight near a wall so they can't surround you."]),
    Q("w_urghast", 12, 8.5, [item("twilightforest:ur_ghast_trophy")], "The Ur-Ghast", deps=["w_knight"], xp=500,
      size=1.5, shape="hexagon", subtitle="The ghast queen of the Dark Tower", desc=[
        "&6You remember the last tower of the twilight. Its keeper remembers you too.&r",
        "&eWhat:&r the great ghast at the top of the Dark Tower. Its fiery tears make more fiery metal.",
        "&eHow:&r climb the tower. Kill ghastlings near the ghast traps to charge them; charged traps pull the Ur-Ghast down so you can strike.",
        "&eTip:&r carminite from the tower makes redstone gadgets of the twilight."]),
    Q("w_yeti", 4, 10, [item("twilightforest:alpha_yeti_trophy")], "The Alpha Yeti", deps=["w_lich"], xp=300,
      subtitle="The snowy forest's boss", desc=[
        "&eWhat:&r the Alpha Yeti lives in a cave in the snowy forest. Its fur makes warm armour.",
        "&eHow:&r dodge the ice it throws and the icicles that fall from the cave roof.",
        "&eTip:&r alpha yeti fur makes warm armour for the glacier."]),
    Q("w_snow_queen", 6, 10, [item("twilightforest:snow_queen_trophy")], "The Snow Queen", deps=["w_yeti"], xp=400,
      subtitle="The glacier's ice palace", desc=[
        "&eWhat:&r the Snow Queen rules the Aurora Palace on the glacier.",
        "&eHow:&r climb the palace, then break her ice shields and avoid her drop attacks.",
        "&eTip:&r beating her finishes the snowy branch of the twilight."]),
    Q("w_uncrafting", 1, 7, [item("twilightforest:uncrafting_table")], "Uncrafting Table", deps=["w_naga"], xp=75,
      optional=True, tokens=1, subtitle="Optional: undo a crafting recipe", desc=[
        "&eWhat:&r the Twilight Forest's table that turns items back into their ingredients, for XP.",
        "&eChemistry:&r the Alchemistry Dissolver goes further: it uncrafts all the way down to elements.",
        "&eHow:&r check JEI for its recipe."]),

    # --- Structures (optional, y=12) -----------------------------------------------------------
    Q("w_dungeon", 0, 12, [tick()], "Better Dungeons", deps=["gs_iron"], xp=50,
      optional=True, tokens=1, subtitle="Optional: clear a YUNG's dungeon", desc=[
        "&eWhat:&r YUNG's Better Dungeons adds catacombs, fortresses and spider caves underground.",
        "&eHow:&r find one (the Explorer's Compass lists them), clear it and loot it. Click the checkmark when done.",
        "&eTip:&r some dungeon chests hold Relics and Artifacts items."]),
    Q("w_mineshaft", 2, 12, [tick()], "Better Mineshafts", deps=["gs_iron"], xp=30,
      optional=True, tokens=1, subtitle="Optional: explore a YUNG's mineshaft", desc=[
        "&eWhat:&r YUNG's Better Mineshafts are longer, with ore deposits, carts and loot.",
        "&eHow:&r explore one and loot a chest. Click the checkmark when done.",
        "&eTip:&r look for minecarts with chests along the tracks."]),
    Q("w_town", 4, 12, [tick()], "Towns and Towers", deps=["gs_iron"], xp=50,
      optional=True, tokens=1, subtitle="Optional: visit a new village or tower", desc=[
        "&eWhat:&r Towns and Towers adds new village styles and pillager outposts across the biomes.",
        "&eHow:&r find a village or outpost you haven't seen before. Click the checkmark when done.",
        "&eTip:&r villages often have a waystone."]),

    # --- Space (y=14) --------------------------------------------------------------------------
    Q("w_desh", 0, 14, [item("ad_astra:raw_desh", 8)], "Desh on the Moon", deps=["t7_rocket"], xp=300,
      subtitle="The Moon's metal builds the next rocket", desc=[
        "&6You remember the Moon from above. Now you're standing on it.&r",
        "&eWhat:&r desh ore is found only on the Moon. Desh blocks, engines and tanks build the Tier 2 rocket.",
        "&eChemistry:&r the Moon has no atmosphere and its days swing from about +120 °C to −170 °C, so bring oxygen.",
        "&eHow:&r mine desh ore on the Moon and process it like any ore."]),
    Q("w_mars", 2, 14, [dim("ad_astra:mars"), item("ad_astra:tier_2_rocket")], "Mars", deps=["w_desh"], xp=500,
      subtitle="The red planet", desc=[
        "&eWhat:&r Mars holds ostrum ore, the metal for the Tier 3 rocket.",
        "&eChemistry:&r Mars is red because its dust is rich in iron(III) oxide, Fe₂O₃: rust. Its thin air is about 95% CO₂.",
        "&eHow:&r build the Tier 2 rocket from desh at the NASA Workbench, fuel it with diesel and launch."]),
    Q("w_ostrum", 4, 14, [item("ad_astra:raw_ostrum", 8)], "Ostrum", deps=["w_mars"], xp=300,
      subtitle="Mars's metal for the Tier 3 rocket", desc=[
        "&eWhat:&r ostrum ore is found only on Mars. It builds the Tier 3 rocket.",
        "&eHow:&r mine ostrum ore on Mars and process it.",
        "&eTip:&r grab some extra for the Tier 3 rocket's engine and tank."]),
    Q("w_suit", 6, 14, [item("ad_astra:netherite_space_suit")], "Heat Shielding", deps=["w_ostrum"], xp=300,
      subtitle="A suit that survives 464 °C", desc=[
        "&eWhat:&r Venus and Mercury are hot enough to kill in a normal space suit. The netherite space suit handles the heat.",
        "&eHow:&r check JEI for the netherite suit pieces. Fill it with oxygen at the Oxygen Loader.",
        "&eTip:&r the jet suit (later, check JEI) also handles the heat, and flies."]),
    Q("w_venus", 8, 14, [dim("ad_astra:venus"), item("ad_astra:tier_3_rocket")], "Venus", deps=["w_suit"], xp=600,
      subtitle="Acid clouds and crushing pressure", desc=[
        "&eWhat:&r Venus holds calorite ore, the metal for the Tier 4 rocket.",
        "&eChemistry:&r its atmosphere is about 96% CO₂ at roughly 92 times Earth's pressure, under clouds of sulfuric acid (H₂SO₄). A runaway greenhouse keeps it near 464 °C.",
        "&eHow:&r Tier 3 rocket from ostrum, plus your netherite space suit."]),
    Q("w_space_metals", 10, 14, [item("ad_astra:desh_ingot", 8), item("ad_astra:ostrum_ingot", 4), item("ad_astra:calorite_ingot", 4)], "Alien Metals", deps=["w_venus"], xp=600,
      subtitle="Desh, ostrum and calorite", desc=[
        "&eWhat:&r one metal from each world: desh (Moon), ostrum (Mars) and calorite (Venus). Each builds the next rocket tier.",
        "&eHow:&r process the raw ores; MI and Mekanism ore lines work on them too (check JEI).",
        "&eTip:&r the Dissolver can tell you what these metals break down into."]),
    Q("w_glacio", 12, 14, [dim("ad_astra:glacio"), item("ad_astra:tier_4_rocket")], "Glacio", deps=["w_space_metals"], xp=800,
      size=1.75, shape="hexagon", subtitle="A frozen world around another star", desc=[
        "&6You remember stars that were yours to name. This one you'll have to visit first.&r",
        "&eWhat:&r Glacio orbits Proxima Centauri, the nearest star to the Sun, about 4.2 light-years away. Unlike the others, it has breathable air.",
        "&eHow:&r build the Tier 4 rocket from calorite and launch."]),
    Q("w_cheese", 1, 15.5, [item("ad_astra:cheese", 4)], "The Moon Is Cheese", deps=["w_desh"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the old joke is true here", desc=[
        "&eWhat:&r Ad Astra hides cheese ore on the Moon.",
        "&eChemistry:&r the real Moon is mostly silicate rock: oxygen, silicon, magnesium, iron, calcium and aluminum.",
        "&eHow:&r mine moon cheese ore. Eat responsibly."]),
    Q("w_oxygen", 5, 15.5, [item("ad_astra:oxygen_distributor")], "Breathable Bases", deps=["w_mars"], xp=150,
      optional=True, tokens=1, subtitle="Optional: fill a sealed room with air", desc=[
        "&eWhat:&r the Oxygen Distributor fills a sealed room with breathable air, so you can work without a helmet.",
        "&eChemistry:&r it makes oxygen from water with FE, the same idea as your Electrolytic Separator: 2H₂O → 2H₂ + O₂.",
        "&eHow:&r check JEI. Seal the room completely; any gap stops it working."]),
    Q("w_mercury", 9, 15.5, [dim("ad_astra:mercury")], "Mercury", deps=["w_venus"], xp=200,
      optional=True, tokens=1, subtitle="Optional: the planet closest to the Sun", desc=[
        "&eWhat:&r a scorched, airless world reachable with the Tier 3 rocket.",
        "&eChemistry:&r with almost no atmosphere, Mercury can't hold heat: about 430 °C by day and −180 °C at night.",
        "&eHow:&r Tier 3 rocket plus the netherite space suit."]),
])
