"""Quest chapter: twilight (the Twilight Forest). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Moved here from worlds.py (keys unchanged): w_naga, w_lich, w_minoshroom, w_hydra, w_tf_metals, w_knight, w_urghast,
w_yeti, w_snow_queen, w_uncrafting. New quests use the tf_ prefix.
Layout: each boss has a "lair" quest (find the structure and win, y=0 / y=5) and a "spoils" quest below it (y=2 / y=7).
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

TF = "twilightforest:"

CHAPTER = Chapter("twilight", "The Twilight Forest", "twilightforest:naga_trophy",
        ["A realm of permanent dusk, ruled by bosses in order."], SIDE, [
    # --- getting your bearings (y=-3) ----------------------------------------------------------
    Q("tf_map", 0, -3, [item(TF + "filled_magic_map")], "A Map of Dusk", deps=["t5_twilight"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the forest draws its own map", desc=[
        "&eWhat:&r the Magic Map shows Twilight biomes and marks every boss structure with an icon.",
        "&eHow:&r craft a Magic Map Focus and then the map (check JEI), and use it inside the Twilight Forest to fill it in.",
        "&eTip:&r the Maze Map does the same job inside the Minoshroom's labyrinth; Nature's Compass finds biomes, Explorer's Compass finds structures."]),
    Q("tf_hollow_hill", 2, -3, [structure(TF + "small_hollow_hill")], "Hollow Hills", deps=["t5_twilight"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a hill full of ore and spiders", desc=[
        "&eWhat:&r hollow hills are mounds with a cave inside, lined with ore blocks, spawners and a treasure chest.",
        "&eHow:&r find a small hollow hill (the mounds in the plain forest) and step inside.",
        "&eTip:&r break the spawners first. The ore inside is free feedstock for your ore lines."]),
    Q("tf_biomes_green", 4, -3, [biome(TF + "enchanted_forest"), biome(TF + "firefly_forest"), biome(TF + "mushroom_forest")], "The Green Twilight",
      deps=["t5_twilight"], xp=75, optional=True, tokens=1, subtitle="Optional: three of the open biomes", desc=[
        "&eWhat:&r the outer Twilight biomes are open from the start: a glowing enchanted forest, a firefly forest and giant mushrooms.",
        "&eChemistry:&r fireflies (and their real cousins) glow by bioluminescence: the enzyme luciferase oxidises luciferin with O₂ and ATP, releasing light instead of heat.",
        "&eHow:&r Nature's Compass can point you to each biome. Just walk in."]),
    Q("tf_cake", 6, -3, [item("telepastries:twilight_cake")], "Twilight Cake", deps=["t5_twilight"], xp=75,
      optional=True, tokens=1, subtitle="Optional: a portal you can eat", desc=[
        "&eWhat:&r a TelePastries cake: eat a slice and you're taken to the Twilight Forest. A tidy alternative to the flower pool.",
        "&eHow:&r cake, poppies and dandelions, with an MI digital circuit (HV) in the bottom centre (this pack's recipe; check JEI).",
        "&eTip:&r keep the cake at your base and the portal pool stays optional."]),
    Q("w_uncrafting", 0, 4, [item("twilightforest:uncrafting_table")], "Uncrafting Table", deps=["w_naga"], xp=75,
      optional=True, tokens=1, subtitle="Optional: undo a crafting recipe", desc=[
        "&eWhat:&r the Twilight Forest's table that turns items back into their ingredients, for XP.",
        "&eChemistry:&r the Alchemistry Dissolver goes further: it uncrafts all the way down to elements.",
        "&eHow:&r check JEI for its recipe."]),

    # --- the main line (lairs y=0, spoils y=2) -------------------------------------------------
    Q("tf_courtyard", 0, 0, [structure(TF + "naga_courtyard"), kill(TF + "naga")], "The Naga's Courtyard", deps=["t5_twilight"], xp=150,
      loot="boss", subtitle="Find the serpent's courtyard and win", desc=[
        "&6You remember this twilight. You walked here once, when the forest was young.&r",
        "&eWhat:&r the first boss. Every boss you beat lifts the magic barrier on the next region, so the order matters.",
        "&eHow:&r the courtyard is a walled stone garden in the plain forest (the Magic Map marks it). Fight inside it.",
        "&eTip:&r the Naga charges in straight lines; sidestep, then hit it while it turns."]),
    Q("w_naga", 0, 2, [item("twilightforest:naga_scale", 4)], "The Naga", deps=["tf_courtyard"], xp=200,
      subtitle="Scales from the forest's first boss", desc=[
        "&eWhat:&r a great serpent coiled in a stone courtyard. Its scales unlock the path forward and make naga armour.",
        "&eHow:&r the Naga drops scales when it dies. Hit it when it stops charging; stay out of its coils.",
        "&eTip:&r each boss you beat lifts the barrier on the next region."]),
    Q("tf_lich_tower", 2, 0, [structure(TF + "lich_tower"), kill(TF + "lich")], "The Lich Tower", deps=["w_naga"], xp=200,
      loot="boss", subtitle="Climb the tower and break the sorcerer", desc=[
        "&eWhat:&r the Lich waits at the top of a tall stone tower. Beating it opens the swamp and the snowy forest.",
        "&eHow:&r climb through the tower's rooms to the top. Break the shields orbiting it before you can hurt it.",
        "&eTip:&r the Lich's shadow clones are distractions; watch for the one that casts."]),
    Q("w_lich", 2, 2, [item("twilightforest:lich_trophy")], "The Lich", deps=["tf_lich_tower"], xp=300,
      subtitle="A sorcerer's trophy and scepters", desc=[
        "&eWhat:&r the Lich drops its trophy and one of its scepters (twilight, zombie, lifedrain or fortification).",
        "&eHow:&r pick up the trophy from the top of the tower once it falls.",
        "&eTip:&r the Lifedrain Scepter heals you as it hurts; recharge scepters with the item listed in JEI."]),
    Q("tf_labyrinth", 4, 0, [structure(TF + "labyrinth"), kill(TF + "minoshroom")], "The Labyrinth", deps=["w_lich"], xp=200,
      loot="boss", subtitle="A maze under the swamp", desc=[
        "&eWhat:&r beneath the swamp lies a maze of mossy stone. The Minoshroom waits in a room at its heart.",
        "&eHow:&r enter through the stairs in the swamp. A Maze Map (made with a Maze Map Focus) shows the corridors.",
        "&eTip:&r mosquito swarms bite in the swamp; bring plenty of food."]),
    Q("w_minoshroom", 4, 2, [item("twilightforest:minoshroom_trophy")], "The Minoshroom", deps=["tf_labyrinth"], xp=300,
      subtitle="The boss at the labyrinth's heart", desc=[
        "&eWhat:&r a mushroom minotaur in the swamp labyrinth. It drops meef stroganoff and a mighty axe.",
        "&eHow:&r the Maze Map helps you find it in the maze. Sidestep its charges.",
        "&eTip:&r meef stroganoff is one of the best foods in the forest."]),
    Q("tf_hydra_lair", 6, 0, [structure(TF + "hydra_lair"), kill(TF + "hydra")], "The Hydra's Lair", deps=["w_minoshroom"], xp=250,
      loot="boss", subtitle="A cave in the fire swamp", desc=[
        "&eWhat:&r the Hydra lives in a hill cave in the fire swamp, the hottest place in the forest.",
        "&eChemistry:&r swamps really do burn: rotting plants release methane (CH₄), which can ignite as marsh fire.",
        "&eHow:&r drink fire resistance before you enter the fire swamp. Strike the heads when they lunge.",
        "&eTip:&r the heads regrow if you're slow; pressure one at a time."]),
    Q("w_hydra", 6, 2, [item("twilightforest:hydra_trophy"), item("twilightforest:fiery_blood", 2)], "The Hydra", deps=["tf_hydra_lair"], xp=400,
      subtitle="Three heads in the fire swamp", desc=[
        "&eWhat:&r the Hydra breathes fire from three heads. Its fiery blood makes fiery ingots.",
        "&eHow:&r fire resistance potions help. Hit the heads when they lunge at you; they regrow, so keep up the pressure.",
        "&eTip:&r its fire swamp is full of lava and fire; fire resistance is a must."]),
    Q("w_tf_metals", 8, 1, [item("twilightforest:ironwood_ingot", 4), item("twilightforest:knightmetal_ingot", 4), item("twilightforest:fiery_ingot", 2)], "Twilight Metals",
      deps=["w_hydra"], xp=250, subtitle="Ironwood, knightmetal and fiery metal", desc=[
        "&eWhat:&r alloys found nowhere else, for strong tools and armour.",
        "&eHow:&r ironwood: smelt raw ironwood (liveroot, iron, gold). Knightmetal: smelt armour shard clusters from the dark forest. Fiery: iron + a vial of fiery blood or tears.",
        "&eTip:&r knightmetal armour and tools are great against the Knight Phantoms."]),
    Q("tf_stronghold", 10, 0, [structure(TF + "knight_stronghold"), kill(TF + "knight_phantom", 6)], "The Goblin Stronghold", deps=["w_tf_metals"], xp=300,
      loot="boss", subtitle="Six phantoms under the dark forest", desc=[
        "&eWhat:&r the Knight Phantoms haunt the deepest room of the Goblin Knight Stronghold, buried under the dark forest.",
        "&eHow:&r find the stronghold's entrance in the dark forest (the Magic Map marks it) and fight your way down. Kill all six phantoms.",
        "&eTip:&r the dark forest blinds you if you haven't beaten the Hydra, so do the bosses in order."]),
    Q("w_knight", 10, 2, [item("twilightforest:knight_phantom_trophy")], "The Knight Phantoms", deps=["tf_stronghold"], xp=400,
      subtitle="Six ghosts in the goblin stronghold", desc=[
        "&eWhat:&r six phantom knights guard the Goblin Stronghold in the dark forest. Their trophy drops with the last one.",
        "&eHow:&r they wait deep inside the stronghold. Knightmetal armour helps.",
        "&eTip:&r they come in waves; fight near a wall so they can't surround you."]),
    Q("tf_dark_tower", 12, 0, [structure(TF + "dark_tower"), kill(TF + "ur_ghast")], "The Dark Tower", deps=["w_knight"], xp=350,
      loot="boss", subtitle="Climb to the Ur-Ghast", desc=[
        "&eWhat:&r a huge tower of towerwood in the centre of the dark forest, with the Ur-Ghast at the top.",
        "&eHow:&r climb through the tower's floors using its carminite contraptions; redstone opens the way in many rooms.",
        "&eTip:&r towerwood borers eat through the walls; kill them before they swarm."]),
    Q("w_urghast", 12, 2, [item("twilightforest:ur_ghast_trophy")], "The Ur-Ghast", deps=["tf_dark_tower"], xp=500,
      size=1.5, shape="hexagon", subtitle="The ghast queen of the Dark Tower", desc=[
        "&6You remember the last tower of the twilight. Its keeper remembers you too.&r",
        "&eWhat:&r the great ghast at the top of the Dark Tower. Its fiery tears make more fiery metal.",
        "&eHow:&r climb the tower. Kill ghastlings near the ghast traps to charge them; charged traps pull the Ur-Ghast down so you can strike.",
        "&eTip:&r carminite from the tower makes redstone gadgets of the twilight."]),

    # --- the snowy branch (lairs y=5, spoils y=7) ----------------------------------------------
    Q("tf_yeti_cave", 4, 5, [structure(TF + "yeti_cave"), kill(TF + "alpha_yeti")], "The Yeti Cave", deps=["w_lich"], xp=200,
      loot="boss", subtitle="A cave in the snowy forest", desc=[
        "&eWhat:&r the Alpha Yeti rules a cave in the snowy forest, surrounded by its smaller yetis.",
        "&eChemistry:&r the snowy forest's blizzard chills you for real; warm armour (yeti or arctic) stops it.",
        "&eHow:&r the snowy forest opens after the Lich. Find the cave and fight inside.",
        "&eTip:&r when it roars, icicles fall from the roof; keep moving."]),
    Q("w_yeti", 4, 7, [item("twilightforest:alpha_yeti_trophy")], "The Alpha Yeti", deps=["tf_yeti_cave"], xp=300,
      subtitle="The snowy forest's boss", desc=[
        "&eWhat:&r the Alpha Yeti lives in a cave in the snowy forest. Its fur makes warm armour.",
        "&eHow:&r dodge the ice it throws and the icicles that fall from the cave roof.",
        "&eTip:&r alpha yeti fur makes warm armour for the glacier."]),
    Q("tf_aurora", 6, 5, [structure(TF + "aurora_palace"), kill(TF + "snow_queen")], "The Aurora Palace", deps=["w_yeti"], xp=300,
      loot="boss", subtitle="An ice palace on the glacier", desc=[
        "&eWhat:&r the Snow Queen's palace of packed ice and aurora blocks stands on the glacier.",
        "&eChemistry:&r real auroras are light from oxygen (green, red) and nitrogen (blue, purple) atoms excited by charged particles from the Sun.",
        "&eHow:&r the glacier opens after the Alpha Yeti. Climb the palace to the Queen's throne room.",
        "&eTip:&r break her ice shields first; she falls on you from above, so look up."]),
    Q("w_snow_queen", 6, 7, [item("twilightforest:snow_queen_trophy")], "The Snow Queen", deps=["tf_aurora"], xp=400,
      subtitle="The glacier's ice palace", desc=[
        "&eWhat:&r the Snow Queen rules the Aurora Palace on the glacier.",
        "&eHow:&r climb the palace, then break her ice shields and avoid her drop attacks.",
        "&eTip:&r beating her finishes the snowy branch of the twilight."]),

    # --- regions and the end of the road (y=9.5) -----------------------------------------------
    Q("tf_biomes_wild", 10, -3, [biome(TF + "swamp"), biome(TF + "fire_swamp"), biome(TF + "dark_forest")], "The Wild Regions",
      deps=["w_hydra"], xp=100, optional=True, tokens=1, subtitle="Optional: swamp, fire swamp and dark forest", desc=[
        "&eWhat:&r the regions you fought through on the main line. Walk through each once you've earned it.",
        "&eHow:&r Nature's Compass points to each biome. The barriers lift as you beat the Lich, Minoshroom and Hydra.",
        "&eTip:&r a quick visit counts; you don't need to stay."]),
    Q("tf_biomes_cold", 2, 9.5, [biome(TF + "snowy_forest"), biome(TF + "glacier")], "The Frozen Regions", deps=["w_snow_queen"], xp=75,
      optional=True, tokens=1, subtitle="Optional: snowy forest and glacier", desc=[
        "&eWhat:&r the cold half of the forest: the snowy forest and the glacier beyond it.",
        "&eChemistry:&r glacier ice is blue because water absorbs red light weakly; thick, bubble-free ice lets mostly blue through.",
        "&eHow:&r visit both. Warm armour stops the blizzard's chill."]),
    Q("tf_trophy_wall", 10, 7, [item(TF + "naga_trophy"), item(TF + "lich_trophy"), item(TF + "minoshroom_trophy"), item(TF + "hydra_trophy"),
                                 item(TF + "knight_phantom_trophy"), item(TF + "ur_ghast_trophy"), item(TF + "alpha_yeti_trophy"), item(TF + "snow_queen_trophy")],
      "Trophy Wall", deps=["tf_highlands"], xp=300, optional=True, tokens=2, loot="boss",
      subtitle="Optional: all eight trophies at once", desc=[
        "&eWhat:&r a trophy from every boss of the forest, in your inventory at the same time.",
        "&eHow:&r keep the trophies you already have. Bosses can be fought again in other structures of the same kind.",
        "&eTip:&r trophies make a fine wall in your base; place them with a right-click."]),
    Q("tf_highlands", 10, 5, [biome(TF + "highlands"), biome(TF + "thornlands")], "The Highlands", deps=["w_urghast", "w_snow_queen"], xp=300,
      size=1.5, shape="hexagon", subtitle="The plateau beyond every barrier", desc=[
        "&6Both branches beaten, the last barrier thins. You remember standing up here and looking down on all of it.&r",
        "&eWhat:&r the highlands and the thornlands ring the forest's centre. Trolls and giants live up here.",
        "&eHow:&r with the Ur-Ghast and the Snow Queen beaten, climb into the highlands, then cross the thornlands (watch the thorns).",
        "&eTip:&r giants are huge and hit hard; fight them from range."]),
    Q("tf_troll_cave", 12, 5, [structure(TF + "troll_cave"), item(TF + "lamp_of_cinders")], "Troll Caves", deps=["tf_highlands"], xp=200,
      optional=True, tokens=2, subtitle="Optional: the trolls' vaults", desc=[
        "&eWhat:&r caves under the highlands, full of trolls guarding vaults. The Lamp of Cinders hides in one.",
        "&eHow:&r find a troll cave in the highlands and loot its vaults. The lamp burns away thorns.",
        "&eTip:&r trolls throw rocks; fight them in the open, not in narrow tunnels."]),
    Q("tf_final_castle", 12, 7, [structure(TF + "final_castle")], "The Unfinished Castle", deps=["tf_highlands"], xp=150,
      secret=True, loot="secret", subtitle="Secret: the castle at the top of the world", desc=[
        "&6A castle on the final plateau, waiting for a ruler. You remember planning to come back for it.&r",
        "&eWhat:&r the Final Castle stands on the final plateau. Its last boss was never finished by the mod's authors.",
        "&eTip:&r the castle is still worth exploring for its architecture and its force-field doors."]),
    Q("tf_quest_grove", 2, -5, [structure(TF + "quest_grove")], "The Questing Ram", deps=["t5_twilight"], xp=100,
      secret=True, loot="secret", subtitle="Secret: a ram that wants every colour", desc=[
        "&eWhat:&r a hidden grove where the Questing Ram lives. Feed it one wool of every colour and it rewards you.",
        "&eChemistry:&r wool dyes are real chemistry too: indigo, cochineal and lapis-blue (lazurite, a sulfur-bearing silicate) all coloured cloth in history.",
        "&eTip:&r the grove's ring of stones looks like a fairy ring in the enchanted forest."]),
], links=[("t5_twilight", -2, 0)])
