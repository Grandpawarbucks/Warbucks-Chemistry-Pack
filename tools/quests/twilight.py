"""Quest chapter: twilight (the Twilight Forest). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Moved here from worlds.py (keys unchanged): w_naga, w_lich, w_minoshroom, w_hydra, w_tf_metals, w_knight, w_urghast,
w_yeti, w_snow_queen, w_uncrafting. New quests use the tf_ prefix.

Layout (grid cells):
- The forest (left, x=-4..-12): tf_oak is the hub; each row is one short chain of things you can do from day one.
- The boss line (x=0..20): lairs at y=0, spoils at y=2. Things that drop in the fight sit above the lair (y<0);
  things made from the spoils sit below (y=4..8). Bosses are 4 columns apart.
- The snowy branch (x=2..10, y=10..14) hangs off the Lich (snowy forest opens after the Lich).
- The highlands and the end (x=24..33, y=8..10.5): Hydra + Ur-Ghast + Snow Queen open the highlands.
Facts are from the Twilight Forest 4.8 jar: biome locks (data/twilightforest/twilight/restrictions), progression
advancements, loot tables and recipes. The pack does not change Twilight Forest except the Twilight Cake (KubeJS).
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

TF = "twilightforest:"


def tf(*names):
    return [TF + n for n in names]


CHAPTER = Chapter("twilight", "The Twilight Forest", "twilightforest:naga_trophy",
        ["A realm of permanent dusk, ruled by bosses in order."], SIDE, [
    # ============================ the forest: things you can do from day one (x=-4..-12) ============================
    Q("tf_oak", -4, 0, [item(TF + "twilight_oak_log", 16)], "Wood of Dusk", deps=["t5_twilight"], xp=75,
      subtitle="Your first logs in the forest", desc=[
        "&6The trees here are older than your forgetting. Their bark still knows your hand.&r",
        "&eWhat:&r twilight oak is the forest's common wood. It makes mason jars, drying racks and tannin for leather.",
        "&eHow:&r chop any twilight oak. Canopy trees, mangroves and darkwood grow nearby too.",
        "&eTip:&r every side quest on this page branches from here; the boss line starts at the Naga's courtyard."]),
    Q("tf_cake", -2, -2, [item("telepastries:twilight_cake")], "Twilight Cake", deps=["t5_twilight"], xp=75,
      optional=True, tokens=1, subtitle="Optional: a portal you can eat", desc=[
        "&eWhat:&r a TelePastries cake: eat a slice and you're taken to the Twilight Forest. A tidy alternative to the flower pool.",
        "&eHow:&r cake, poppies and dandelions, with an MI digital circuit (HV) in the bottom centre (this pack's recipe; check JEI).",
        "&eTip:&r keep the cake at your base and the portal pool stays optional."]),

    # --- magic trees (y=-8 / -10) ---
    Q("tf_hollow_tree", -6, -8, [structure(TF + "hollow_tree")], "A Hollow Giant", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: climb inside a giant hollow tree", desc=[
        "&eWhat:&r huge hollow trees tower over the forest. Their branches hide leafy caches with rare magic saplings.",
        "&eHow:&r find one (taller than everything around it) and climb inside. Search the leaf clusters for a chest.",
        "&eTip:&r bring ladders or scaffolding; the fall from the canopy is long."]),
    Q("tf_magic_saplings", -8, -8, [anyof(tf("time_sapling", "transformation_sapling", "mining_sapling", "sorting_sapling"))],
      "Magic Saplings", deps=["tf_hollow_tree"], xp=100, optional=True, tokens=1, subtitle="Optional: a sapling with a heart", desc=[
        "&eWhat:&r four magic trees: Time, Transformation, Mining and Sorting. Each grows with a working core inside its trunk.",
        "&eHow:&r loot one from a hollow tree's cache. Plant it where you want the tree; it can't be moved later.",
        "&eTip:&r breaking a core only drops a plain log, so choose the spot first."]),
    Q("tf_tree_time", -6, -10, [item(TF + "time_log", 4)], "Tree of Time", deps=["tf_magic_saplings"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Timewood Clock", desc=[
        "&eWhat:&r the Timewood Clock in the trunk makes blocks around the tree tick faster: crops, saplings and machines that tick.",
        "&eHow:&r grow a Tree of Time from its sapling and collect some of its logs (any log of the tree counts).",
        "&eTip:&r plant it in the middle of a farm. Check its tooltip in JEI for the range."]),
    Q("tf_tree_transform", -8, -10, [item(TF + "transformation_log", 4)], "Tree of Transformation", deps=["tf_magic_saplings"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Heart of Transformation", desc=[
        "&eWhat:&r the Heart of Transformation slowly rewrites the biome around the tree into a Twilight one.",
        "&eHow:&r grow a Tree of Transformation from its sapling and collect some of its logs.",
        "&eTip:&r don't plant it next to a base that needs a particular biome; the change spreads."]),
    Q("tf_tree_mining", -10, -10, [item(TF + "mining_log", 4)], "Miner's Tree", deps=["tf_magic_saplings"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Minewood Core", desc=[
        "&eWhat:&r the Minewood Core gathers ore from the ground around the tree (its tooltip in JEI explains the details).",
        "&eChemistry:&r real ore is just rock rich in a mineral, like haematite (Fe₂O₃) or chalcopyrite (CuFeS₂). The tree simply finds it for you.",
        "&eHow:&r grow a Miner's Tree from its sapling and collect some of its logs."]),
    Q("tf_tree_sorting", -12, -10, [item(TF + "sorting_log", 4)], "Sorting Tree", deps=["tf_magic_saplings"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Sortingwood Engine", desc=[
        "&eWhat:&r the Sortingwood Engine moves items from a chest by the tree into nearby chests that already hold the same item.",
        "&eHow:&r grow a Sorting Tree from its sapling and collect some of its logs.",
        "&eTip:&r a cheap sorting room for a forest outpost; at home your storage network does it better."]),

    # --- maps (y=-6) ---
    Q("tf_map_focus", -6, -6, [item(TF + "magic_map_focus")], "Magic Map Focus", deps=["tf_oak"], xp=75,
      subtitle="Feather, berry and glowstone", desc=[
        "&eWhat:&r the focus that turns paper into a Magic Map of the Twilight Forest.",
        "&eHow:&r a raven feather, torchberries and glowstone dust, shapeless. Ravens hop about the forest floor; torchberries hang from cave roofs (skeleton druids drop them too).",
        "&eTip:&r torchberries also make berry torches, which never need fuel."]),
    Q("tf_map", -8, -6, [item(TF + "filled_magic_map")], "A Map of Dusk", deps=["tf_map_focus"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the forest draws its own map", desc=[
        "&eWhat:&r the Magic Map shows Twilight biomes and marks every boss structure with an icon.",
        "&eHow:&r eight paper around the focus makes a blank Magic Map. Use it inside the Twilight Forest to fill it in.",
        "&eTip:&r the Maze Map does the same job inside the Minoshroom's labyrinth; Nature's Compass finds biomes, Explorer's Compass finds structures."]),

    # --- hollow hills (y=-4) ---
    Q("tf_hollow_hill", -6, -4, [structure(TF + "small_hollow_hill")], "Hollow Hills", deps=["tf_oak"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a hill full of ore and spiders", desc=[
        "&eWhat:&r hollow hills are mounds with a cave inside, lined with ore blocks, spawners and a treasure chest.",
        "&eHow:&r find a small hollow hill (the mounds in the plain forest) and step inside.",
        "&eTip:&r break the spawners first. The ore inside is free feedstock for your ore lines."]),
    Q("tf_ore_magnet", -8, -4, [item(TF + "ore_magnet")], "Ore Magnet", deps=["tf_hollow_hill"], xp=100,
      optional=True, tokens=1, subtitle="Optional: pull the vein to you", desc=[
        "&eWhat:&r a hollow hill treasure that drags a vein of ore out of the rock towards you.",
        "&eChemistry:&r real mines do a version of this: magnetic separation pulls magnetite (Fe₃O₄) out of crushed rock, because it is strongly ferromagnetic.",
        "&eHow:&r loot it from a hollow hill chest (any size). Aim at stone and use it."]),
    Q("tf_big_hill", -10, -4, [structure(TF + "large_hollow_hill")], "The Great Hollow Hill", deps=["tf_ore_magnet"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the biggest hill, the best chest", desc=[
        "&eWhat:&r large hollow hills hold the most ore, the most spawners and the richest chest of the three sizes.",
        "&eHow:&r look for the biggest mounds in the forest and step inside.",
        "&eTip:&r light the cave up as you go; the spawners inside are what makes it dangerous."]),
    Q("tf_hill_curios", -12, -4, [anyof(tf("peacock_feather_fan", "moonworm_queen", "transformation_powder"))], "Hill Curios",
      deps=["tf_big_hill"], xp=100, optional=True, tokens=1, subtitle="Optional: a fan, a worm queen or a powder", desc=[
        "&eWhat:&r odd treasures from hills and the Lich Tower: the Peacock Feather Fan blows a gust of wind, the Moonworm Queen fires glowing moonworms, and Transformation Powder turns some mobs into their Twilight cousins.",
        "&eHow:&r loot any one of them from hollow hill or tower chests.",
        "&eTip:&r the Moonworm Queen is a lighting tool that never runs out for good; its repair recipe is in JEI."]),

    # --- steeleaf and ironwood (y=-2 / 0) ---
    Q("tf_steeleaf", -6, -2, [item(TF + "steeleaf_ingot", 4)], "Steeleaf", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: leaves as hard as metal", desc=[
        "&eWhat:&r steeleaf is a metal-hard leaf found only as treasure: hollow hill, labyrinth, stronghold and Dark Tower chests.",
        "&eChemistry:&r a leaf of steel is fantasy. Real steel is iron with roughly 0.2 to 2% carbon dissolved in it, which is what makes it hard.",
        "&eHow:&r loot chests as you explore. Nine make a steeleaf block for storage."]),
    Q("tf_steeleaf_gear", -8, -2, [anyof(tf("steeleaf_pickaxe", "steeleaf_sword", "steeleaf_axe", "steeleaf_helmet",
                                            "steeleaf_chestplate", "steeleaf_leggings", "steeleaf_boots"))],
      "Steeleaf Gear", deps=["tf_steeleaf"], xp=100, optional=True, tokens=1, subtitle="Optional: a pickaxe with built-in Fortune", desc=[
        "&eWhat:&r steeleaf tools and armour come pre-enchanted. The pickaxe is crafted with Fortune II already on it.",
        "&eHow:&r craft any steeleaf piece (vanilla shapes with steeleaf; check JEI).",
        "&eTip:&r a Fortune II pickaxe this early doubles ore from your best veins."]),
    Q("tf_ironwood", -6, 0, [item(TF + "liveroot", 2), item(TF + "ironwood_ingot", 4)], "Ironwood", deps=["tf_oak"], xp=100,
      subtitle="Living root, iron and gold", desc=[
        "&eWhat:&r ironwood is the forest's first metal: tougher than iron, and needed for the Twilight Metals milestone.",
        "&eChemistry:&r smelting raw iron is a reduction: carbon monoxide strips the oxygen, Fe₂O₃ + 3CO → 2Fe + 3CO₂. The liveroot and gold just make it Twilight.",
        "&eHow:&r liveroot + raw iron + a gold nugget makes 2 raw ironwood (shapeless). Smelt or blast it. Liveroot grows in the root tangles underground.",
        "&eTip:&r bring a stack of raw iron from home; liveroot is the only forest part."]),
    Q("tf_ironwood_gear", -8, 0, [anyof(tf("ironwood_pickaxe", "ironwood_sword", "ironwood_axe", "ironwood_helmet",
                                           "ironwood_chestplate", "ironwood_leggings", "ironwood_boots"))],
      "Ironwood Gear", deps=["tf_ironwood"], xp=100, optional=True, tokens=1, subtitle="Optional: tools that come enchanted", desc=[
        "&eWhat:&r ironwood tools and armour come with enchantments built in (the pickaxe has Efficiency I).",
        "&eHow:&r craft any ironwood piece in the usual shapes (check JEI).",
        "&eTip:&r a full ironwood set is a solid start for the Naga and the Lich."]),
    Q("tf_oreberries", -6, 2, [anyof(tf("iron_berry", "copper_berry", "gold_berry"), 8)], "Oreberries", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: bushes that grow metal", desc=[
        "&eWhat:&r oreberry bushes grow underground in the forest and fruit iron, copper or gold berries. Smelt a berry for a nugget.",
        "&eChemistry:&r real plants can do this: hyperaccumulators such as Alyssum store nickel in their leaves, and phytomining burns them for metal-rich ash.",
        "&eHow:&r dig down a little under the forest floor to find the bushes (the enchanted forest grows them too). Collect 8 berries of any metal.",
        "&eTip:&r the bushes are thorny and hurt you when you walk through them. Harvest them, don't push past."]),

    # --- leather and food (y=4 / 6) ---
    Q("tf_drying_rack", -6, 4, [item(TF + "twilight_oak_drying_rack")], "Drying Rack", deps=["tf_oak"], xp=75,
      optional=True, tokens=1, subtitle="Optional: let the air do the work", desc=[
        "&eWhat:&r a rack that slowly dries what you hang on it: meat into jerky, mud into clay, treated leather into tanned leather.",
        "&eHow:&r three twilight oak slabs in a row. Every wood has its own rack; right-click items onto it.",
        "&eTip:&r drying takes minutes, not seconds. Build a row of racks."]),
    Q("tf_tanning", -8, 4, [item(TF + "tannin"), item(TF + "tanned_leather", 4)], "Tanning", deps=["tf_drying_rack"], xp=100,
      optional=True, tokens=1, subtitle="Optional: bark chemistry for leather", desc=[
        "&eWhat:&r tanned leather is the material for the new traveller's gear.",
        "&eChemistry:&r real vegetable tanning works the same way: tannins (polyphenols from bark and leaves) bind to the collagen in hide and cross-link it, so it stops rotting and stays supple.",
        "&eHow:&r tannin = water bottle + twilight oak sapling + root strand + twilight oak leaves. Tannin + leather = treated leather; dry that on a rack to get tanned leather.",
        "&eTip:&r root strands come from the root blocks underground, near the liveroot."]),
    Q("tf_travellers", -10, 4, [anyof(tf("travellers_vest", "travellers_belt", "travellers_goggles", "travellers_boots",
                                         "travellers_gloves", "travellers_wings"))],
      "Traveller's Gear", deps=["tf_tanning"], xp=150, optional=True, tokens=1, subtitle="Optional: gear you can upgrade", desc=[
        "&eWhat:&r vest, belt, goggles, boots, gloves and wings made from tanned leather. Each piece takes modifiers (double jump, gliding, auto-repair and more).",
        "&eHow:&r craft any piece (check JEI). The modifier recipes are in JEI too; many use Twilight drops such as raven feathers and borer essence.",
        "&eTip:&r the wings need carminite, so they wait until the Dark Tower."]),
    Q("tf_jerky", -8, 6, [anyof(tf("meef_jerky", "venison_jerky", "beef_jerky", "pork_jerky", "chicken_jerky", "mutton_jerky"), 8)],
      "Jerky", deps=["tf_drying_rack"], xp=75, optional=True, tokens=1, subtitle="Optional: food that keeps", desc=[
        "&eWhat:&r dried meat from the drying rack: light, filling travel food.",
        "&eChemistry:&r drying lowers the water activity of meat below about 0.85, and most bacteria can't grow without free water. It's one of the oldest preservation methods there is.",
        "&eHow:&r hang raw meat (venison from forest deer works well) on a drying rack and wait. Collect 8 jerky."]),

    # --- charms (y=8) ---
    Q("tf_charm_life", -6, 8, [item(TF + "charm_of_life_1")], "Charm of Life", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: one death, refused", desc=[
        "&eWhat:&r carried in your inventory, the Charm of Life is used up to save you from a killing blow.",
        "&eHow:&r a chest find: fallen trunks, hollow hills, the Lich Tower, the stronghold and the Aurora Palace all have them.",
        "&eTip:&r carry one into every boss fight."]),
    Q("tf_charm_keeping", -8, 8, [item(TF + "charm_of_keeping_1")], "Charm of Keeping", deps=["tf_charm_life"], xp=100,
      optional=True, tokens=1, subtitle="Optional: keep your things when you fall", desc=[
        "&eWhat:&r the Charm of Keeping is used up when you die and keeps some of your items with you. Higher tiers keep more.",
        "&eHow:&r found in many forest chests; maze slimes drop them too.",
        "&eTip:&r the forest's death caskets also hold what you drop, so you can come back for it."]),
    Q("tf_charm_upgrade", -10, 8, [anyof(tf("charm_of_life_2", "charm_of_keeping_2", "charm_of_keeping_3"))], "Stronger Charms",
      deps=["tf_charm_keeping"], xp=150, optional=True, tokens=2, subtitle="Optional: four charms make one better", desc=[
        "&eWhat:&r combine charms into a higher tier: Charm of Life II, or Charm of Keeping II and III.",
        "&eHow:&r four of a tier, shapeless, make one of the next tier (check JEI).",
        "&eTip:&r a Charm of Keeping III keeps your whole inventory, so it's worth saving sixteen of the first tier."]),

    # --- open biomes, hedge maze and the questing ram (y=10) ---
    Q("tf_biomes_green", -6, 10, [biome(TF + "enchanted_forest"), biome(TF + "firefly_forest"), biome(TF + "mushroom_forest")], "The Green Twilight",
      deps=["tf_oak"], xp=75, optional=True, tokens=1, subtitle="Optional: three of the open biomes", desc=[
        "&eWhat:&r the outer Twilight biomes are open from the start: a glowing enchanted forest, a firefly forest and giant mushrooms.",
        "&eChemistry:&r fireflies (and their real cousins) glow by bioluminescence: the enzyme luciferase oxidises luciferin with O₂ and ATP, releasing light instead of heat.",
        "&eHow:&r Nature's Compass can point you to each biome. Just walk in."]),
    Q("tf_hedge_maze", -8, 10, [structure(TF + "hedge_maze")], "The Hedge Maze", deps=["tf_biomes_green"], xp=100,
      optional=True, tokens=1, subtitle="Optional: thorny walls and hedge spiders", desc=[
        "&eWhat:&r a maze of hedges in the forest, with hedge spiders and chests at the dead ends.",
        "&eHow:&r find one in the forest and walk in.",
        "&eTip:&r bring shears or an axe and cut your own path when you're lost."]),
    Q("tf_quest_grove", -10, 10, [structure(TF + "quest_grove")], "The Questing Ram", deps=["tf_hedge_maze"], xp=100,
      secret=True, loot="secret", subtitle="Secret: a ram that wants every colour", desc=[
        "&eWhat:&r a hidden grove where the Questing Ram lives. Feed it one wool of every colour and it rewards you.",
        "&eChemistry:&r wool dyes are real chemistry too: indigo, cochineal and lapis-blue (lazurite, a sulfur-bearing silicate) all coloured cloth in history.",
        "&eTip:&r the grove's ring of stones looks like a fairy ring in the enchanted forest."]),
    Q("tf_crumble_horn", -12, 10, [item(TF + "crumble_horn")], "The Crumble Horn", deps=["tf_quest_grove"], xp=150,
      secret=True, loot="secret", subtitle="Secret: the ram's reward", desc=[
        "&eWhat:&r feed the Questing Ram all sixteen colours of wool and it pays out blocks of metal and gems, its trophy, and the Crumble Horn.",
        "&eHow:&r blow the horn at stone and it crumbles the blocks in front of you (check JEI for what turns into what).",
        "&eTip:&r it's a handy tunnelling tool for the labyrinth."]),

    # ============================ the boss line (lairs y=0, spoils y=2) ============================
    # --- the Naga (x=0) ---
    Q("tf_courtyard", 0, 0, [structure(TF + "naga_courtyard"), kill(TF + "naga")], "The Naga's Courtyard", deps=["t5_twilight"], xp=150,
      loot="boss", subtitle="Find the serpent's courtyard and win", desc=[
        "&6You remember this twilight. You walked here once, when the forest was young.&r",
        "&eWhat:&r the first boss. Each boss lifts the curse on the next region (hunger, fire, darkness, frost or acid rain), so the order matters.",
        "&eHow:&r the courtyard is a walled stone garden in the plain forest (the Magic Map marks it). Fight inside it.",
        "&eTip:&r the Naga charges in straight lines; sidestep, then hit it while it turns."]),
    Q("tf_naga_armor", 0, -2, [item(TF + "naga_chestplate"), item(TF + "naga_leggings")], "Naga Scale Armour", deps=["tf_courtyard"], xp=150,
      optional=True, tokens=1, subtitle="Optional: armour from the serpent", desc=[
        "&eWhat:&r a tunic and leggings of naga scales. Both come pre-enchanted: Fire Protection III on the tunic, Protection III on the leggings.",
        "&eHow:&r eight scales for the tunic, seven for the leggings, in the usual armour shapes (check JEI).",
        "&eTip:&r the fire protection pays off later in the Hydra's fire swamp."]),
    Q("w_naga", 0, 2, [item("twilightforest:naga_scale", 4)], "The Naga", deps=["tf_courtyard"], xp=200,
      subtitle="Scales from the forest's first boss", desc=[
        "&eWhat:&r a great serpent coiled in a stone courtyard. Its scales unlock the path forward and make naga armour.",
        "&eHow:&r the Naga drops scales and its trophy when it dies. Hit it when it stops charging; stay out of its coils.",
        "&eTip:&r the Lich Tower is next. Its door won't open until the Naga is dead."]),

    # --- the Lich (x=4) ---
    Q("tf_lich_tower", 4, 0, [structure(TF + "lich_tower"), kill(TF + "lich")], "The Lich Tower", deps=["w_naga"], xp=200,
      loot="boss", subtitle="Climb the tower and break the sorcerer", desc=[
        "&eWhat:&r the Lich waits at the top of a tall stone tower. Beating it opens the swamp, the dark forest and the snowy forest.",
        "&eHow:&r climb through the tower's rooms to the top. Break the shields orbiting it before you can hurt it.",
        "&eTip:&r the Lich's shadow clones are distractions; watch for the one that casts."]),
    Q("tf_scepters", 4, -2, [item(TF + "twilight_scepter"), item(TF + "zombie_scepter"), item(TF + "lifedrain_scepter"), item(TF + "fortification_scepter")],
      "Four Scepters", deps=["tf_lich_tower"], xp=300, optional=True, tokens=2, subtitle="Optional: every scepter the Lich carries", desc=[
        "&eWhat:&r the Lich drops one scepter per kill: Twilight (fires bolts), Zombie (raises loyal zombies), Lifedrain (heals you as it hurts) and Fortification (a shield).",
        "&eHow:&r other Lich Towers have their own Lich. Beat it again to collect the set.",
        "&eTip:&r scepters recharge on a crafting grid with their own item (check JEI). The Renewal enchantment recharges them automatically."]),
    Q("w_lich", 4, 2, [item("twilightforest:lich_trophy")], "The Lich", deps=["tf_lich_tower"], xp=300,
      subtitle="A sorcerer's trophy and scepters", desc=[
        "&eWhat:&r the Lich drops its trophy, one of its scepters and golden gear.",
        "&eHow:&r pick up the trophy from the top of the tower once it falls.",
        "&eTip:&r three ways open now: the labyrinth in the swamp, the stronghold in the dark forest, and the snowy forest below."]),

    # --- the Minoshroom (x=8) ---
    Q("tf_labyrinth", 8, 0, [structure(TF + "labyrinth"), kill(TF + "minoshroom")], "The Labyrinth", deps=["w_lich"], xp=200,
      loot="boss", subtitle="A maze under the swamp", desc=[
        "&eWhat:&r beneath the swamp lies a maze of mossy stone. The Minoshroom waits in a room at its heart.",
        "&eHow:&r enter through the stairs in the swamp. A Maze Map (made with a Maze Map Focus) shows the corridors.",
        "&eTip:&r mosquito swarms bite in the swamp; bring plenty of food."]),
    Q("tf_mazebreaker", 6, -2, [item(TF + "mazebreaker_pickaxe")], "Mazebreaker", deps=["tf_labyrinth"], xp=250,
      optional=True, tokens=2, subtitle="Optional: the labyrinth's jackpot", desc=[
        "&eWhat:&r a diamond pickaxe that chews through maze stone, found only in the labyrinth's best vault.",
        "&eHow:&r labyrinth vaults are sealed rooms off the corridors. The jackpot vault is rare; check every one.",
        "&eTip:&r a Maze Map shows unexplored rooms as gaps in the corridors."]),
    Q("tf_maze_focus", 8, -2, [item(TF + "maze_map_focus")], "Maze Map Focus", deps=["tf_labyrinth"], xp=150,
      subtitle="A minotaur's map lens", desc=[
        "&eWhat:&r the focus for Maze Maps, and the heart of the Uncrafting Table.",
        "&eHow:&r minotaurs in the labyrinth drop it. Kill them as you search for the Minoshroom.",
        "&eTip:&r keep a spare; the Uncrafting Table eats one."]),
    Q("tf_minotaur_axe", 10, -2, [item(TF + "diamond_minotaur_axe")], "Minotaur Axe", deps=["tf_labyrinth"], xp=150,
      optional=True, tokens=1, subtitle="Optional: the Minoshroom's weapon", desc=[
        "&eWhat:&r a heavy diamond axe dropped by the Minoshroom.",
        "&eHow:&r beat the Minoshroom; the axe drops with its stroganoff.",
        "&eTip:&r it's an axe, so it still chops wood; keep it for both jobs."]),
    Q("tf_maze_map", 8, -4, [item(TF + "filled_maze_map")], "Maze Map", deps=["tf_maze_focus"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a map of corridors", desc=[
        "&eWhat:&r a map that draws the tunnels around you at your own depth.",
        "&eHow:&r eight paper around a Maze Map Focus makes a blank Maze Map. Use it in the labyrinth to fill it in.",
        "&eTip:&r one map covers one level; make another for each floor."]),
    Q("tf_ore_map", 8, -6, [item(TF + "filled_ore_map")], "Ore Map", deps=["tf_maze_map"], xp=200,
      optional=True, tokens=2, subtitle="Optional: a map that shows ore", desc=[
        "&eWhat:&r a Maze Map upgraded to also mark the ore around you.",
        "&eHow:&r a blank Maze Map + a diamond block + a gold block + an iron block, shapeless. Use it to fill it in.",
        "&eTip:&r expensive, but it finds rich pockets for your ore lines fast."]),
    Q("w_uncrafting", 10, -4, [item("twilightforest:uncrafting_table")], "Uncrafting Table", deps=["tf_maze_focus"], xp=75,
      optional=True, tokens=1, subtitle="Optional: undo a crafting recipe", desc=[
        "&eWhat:&r the Twilight Forest's table that turns crafted items back into their ingredients, for XP.",
        "&eChemistry:&r the Alchemistry Dissolver goes further: it uncrafts all the way down to elements.",
        "&eHow:&r eight crafting tables around a Maze Map Focus (this pack leaves the recipe and the table unchanged).",
        "&eTip:&r the XP cost rises with the item's value, and some recipes can't be reversed; the table tells you."]),
    Q("w_minoshroom", 8, 2, [item("twilightforest:minoshroom_trophy")], "The Minoshroom", deps=["tf_labyrinth"], xp=300,
      subtitle="The boss at the labyrinth's heart", desc=[
        "&eWhat:&r a mushroom minotaur in the swamp labyrinth. It drops its trophy, meef stroganoff and a mighty axe.",
        "&eHow:&r the Maze Map helps you find it in the maze. Sidestep its charges.",
        "&eTip:&r don't eat all the stroganoff at once; the next quest needs one."]),
    Q("tf_stroganoff", 10, 2, [item(TF + "meef_stroganoff")], "Mighty Stroganoff", deps=["w_minoshroom"], xp=150,
      subtitle="Eat it to bear the fire swamp", desc=[
        "&eWhat:&r the fire swamp sets you alight until your body is used to its heat. Eating meef stroganoff does that.",
        "&eHow:&r eat one meef stroganoff from the Minoshroom, and keep another in your inventory for this quest.",
        "&eTip:&r it's also one of the best foods in the forest: a full bowl of hunger."]),

    # --- the Hydra (x=12) ---
    Q("tf_hydra_lair", 12, 0, [structure(TF + "hydra_lair"), kill(TF + "hydra")], "The Hydra's Lair", deps=["tf_stroganoff"], xp=250,
      loot="boss", subtitle="A cave in the fire swamp", desc=[
        "&eWhat:&r the Hydra lives in a hill cave in the fire swamp, the hottest place in the forest.",
        "&eChemistry:&r swamps really do burn: rotting plants release methane (CH₄), which can ignite as marsh fire.",
        "&eHow:&r eat the stroganoff first or the swamp burns you. Strike the heads when they lunge.",
        "&eTip:&r the heads regrow if you're slow; pressure one at a time."]),
    Q("tf_biomes_wild", 12, -2, [biome(TF + "swamp"), biome(TF + "fire_swamp"), biome(TF + "dark_forest")], "The Wild Regions",
      deps=["tf_hydra_lair"], xp=100, optional=True, tokens=1, subtitle="Optional: swamp, fire swamp and dark forest", desc=[
        "&eWhat:&r the regions you fought through on the main line. Walk through each once you've earned it.",
        "&eHow:&r Nature's Compass points to each biome. The Lich lifts the swamp's hunger and the dark forest's darkness; the stroganoff lifts the fire swamp's burning.",
        "&eTip:&r a quick visit counts; you don't need to stay."]),
    Q("w_hydra", 12, 2, [item("twilightforest:hydra_trophy"), item("twilightforest:fiery_blood", 2)], "The Hydra", deps=["tf_hydra_lair"], xp=400,
      subtitle="Three heads in the fire swamp", desc=[
        "&eWhat:&r the Hydra breathes fire from three heads. It drops its trophy, fiery blood and hydra chops.",
        "&eHow:&r fire resistance potions help. Hit the heads when they lunge at you; they regrow, so keep up the pressure.",
        "&eTip:&r a hydra chop is a huge meal that also heals; save them for boss fights."]),
    Q("tf_fiery", 12, 4, [item(TF + "fiery_ingot", 4)], "Fiery Metal", deps=["w_hydra"], xp=200,
      subtitle="Iron quenched in burning blood", desc=[
        "&eWhat:&r fiery ingots: the hottest metal of the forest, for fire-proof tools and armour.",
        "&eChemistry:&r real blood is red because of the iron in haem, the part of haemoglobin that carries O₂. The Hydra's blood just burns as well.",
        "&eHow:&r a vial of fiery blood (Hydra) or fiery tears (Ur-Ghast) + an iron ingot, shapeless."]),
    Q("tf_fiery_gear", 10, 6, [anyof(tf("fiery_pickaxe", "fiery_sword", "fiery_helmet", "fiery_chestplate", "fiery_leggings", "fiery_boots"))],
      "Fiery Gear", deps=["tf_fiery"], xp=200, optional=True, tokens=1, subtitle="Optional: a pickaxe that smelts as it digs", desc=[
        "&eWhat:&r the Fiery Pickaxe smelts the ore it mines on the spot; the sword sets targets alight.",
        "&eChemistry:&r smelting is reduction: heat plus carbon pulls the oxygen off a metal oxide. The pickaxe does the furnace's job at the moment you mine.",
        "&eHow:&r fiery ingots with blaze rods for the tools, or alone for the armour (check JEI).",
        "&eTip:&r auto-smelting skips your ore doubling. Use it on things you'd only smelt anyway."]),

    # --- metals milestone and knightmetal (x=13..18, y=4..8) ---
    Q("tf_armor_shards", 14, 4, [item(TF + "armor_shard", 9)], "Armour Shards", deps=["w_hydra"], xp=150,
      subtitle="Knock the plates off goblins", desc=[
        "&eWhat:&r shards of knightmetal, the stronghold's metal. Nine make a shard cluster.",
        "&eHow:&r goblin knights and block-and-chain goblins in the Goblin Knight Stronghold drop them; helmet crabs on the shore drop them too.",
        "&eTip:&r the dark forest has been safe to walk since the Lich; only its centre stays dark."]),
    Q("tf_knightmetal", 14, 6, [item(TF + "armor_shard_cluster"), item(TF + "knightmetal_ingot", 4)], "Knightmetal", deps=["tf_armor_shards"], xp=200,
      subtitle="Melt the shards back together", desc=[
        "&eWhat:&r knightmetal ingots, for the heaviest armour and weapons in the forest.",
        "&eChemistry:&r remelting scrap is how most real steel is made today: an electric arc furnace melts recycled metal back into new ingots.",
        "&eHow:&r nine armour shards make a cluster (shapeless). Smelt or blast the cluster for one ingot."]),
    Q("w_tf_metals", 13, 8, [item("twilightforest:ironwood_ingot", 4), item("twilightforest:knightmetal_ingot", 4), item("twilightforest:fiery_ingot", 2)], "Twilight Metals",
      deps=["tf_fiery", "tf_knightmetal"], xp=250, subtitle="Ironwood, knightmetal and fiery metal", desc=[
        "&eWhat:&r the three alloys found nowhere else, for strong tools and armour.",
        "&eHow:&r ironwood from liveroot (see the forest), knightmetal from armour shards, fiery metal from iron and fiery blood or tears.",
        "&eTip:&r knightmetal armour and tools are great against the Knight Phantoms."]),
    Q("tf_knight_gear", 16, 6, [anyof(tf("knightmetal_pickaxe", "knightmetal_sword", "knightmetal_axe", "knightmetal_helmet",
                                         "knightmetal_chestplate", "knightmetal_leggings", "knightmetal_boots",
                                         "phantom_helmet", "phantom_chestplate"))],
      "Knight's Arms", deps=["tf_knightmetal"], xp=200, optional=True, tokens=1, subtitle="Optional: knightmetal or phantom gear", desc=[
        "&eWhat:&r knightmetal tools and armour, or the phantom helmet and chestplate the Knight Phantoms sometimes drop.",
        "&eHow:&r craft any knightmetal piece (check JEI), or take phantom armour from the phantoms' drops.",
        "&eTip:&r the phantoms also drop knightmetal weapons, so the fight can pay for itself."]),
    Q("tf_block_chain", 18, 6, [anyof(tf("block_and_chain", "knightmetal_shield"))], "Block and Chain", deps=["tf_knight_gear"], xp=200,
      optional=True, tokens=1, subtitle="Optional: a ball and chain, or a shield", desc=[
        "&eWhat:&r the Block and Chain is a thrown flail that smashes blocks and mobs; the Knightmetal Shield blocks like a wall.",
        "&eHow:&r both start with a knightmetal ring (four ingots in a ring). Block and Chain: block + 3 ingots + ring. Shield: ingots, ring and towerwood (check JEI).",
        "&eTip:&r the shield needs towerwood from the Dark Tower."]),

    # --- the Knight Phantoms (x=16) ---
    Q("tf_stronghold", 16, 0, [structure(TF + "knight_stronghold"), kill(TF + "knight_phantom", 6)], "The Goblin Stronghold", deps=["w_hydra"], xp=300,
      loot="boss", subtitle="Six phantoms under the dark forest", desc=[
        "&eWhat:&r the Knight Phantoms haunt the deepest room of the Goblin Knight Stronghold, buried under the dark forest.",
        "&eHow:&r find the entrance in the dark forest (the Magic Map marks it). Inside, place a boss trophy on the Trophy Pedestal to wake the phantoms, then kill all six.",
        "&eTip:&r the stronghold opens after the Lich; this page sends you after the Hydra so you arrive with fiery and knightmetal gear."]),
    Q("w_knight", 16, 2, [item("twilightforest:knight_phantom_trophy")], "The Knight Phantoms", deps=["tf_stronghold"], xp=400,
      subtitle="Six ghosts in the goblin stronghold", desc=[
        "&eWhat:&r six phantom knights guard the Goblin Stronghold in the dark forest. Their trophy drops with the last one.",
        "&eHow:&r they wait deep inside the stronghold. Knightmetal armour helps.",
        "&eTip:&r beating them lifts the darkness on the dark forest's centre, where the Dark Tower stands."]),

    # --- the Ur-Ghast (x=20) ---
    Q("tf_dark_tower", 20, 0, [structure(TF + "dark_tower"), kill(TF + "ur_ghast")], "The Dark Tower", deps=["w_knight"], xp=350,
      loot="boss", subtitle="Climb to the Ur-Ghast", desc=[
        "&eWhat:&r a huge tower of towerwood in the centre of the dark forest, with the Ur-Ghast at the top.",
        "&eHow:&r climb through the tower's floors using its carminite contraptions; redstone opens the way in many rooms. A tower key from a chest opens the locked doors.",
        "&eTip:&r towerwood borers eat through the walls; kill them before they swarm."]),
    Q("tf_carminite", 20, -2, [item(TF + "carminite", 4)], "Carminite", deps=["tf_dark_tower"], xp=200,
      subtitle="The red gem that runs the tower", desc=[
        "&eWhat:&r carminite powers the Dark Tower's devices and the traveller's wings.",
        "&eChemistry:&r its name echoes carmine, a real red dye: carminic acid (C₂₂H₂₀O₁₃), made by cochineal insects.",
        "&eHow:&r the Ur-Ghast drops some. Or craft it: 4 borer essence + 4 redstone + a ghast tear. Borer essence drops from towerwood borers."]),
    Q("tf_tower_devices", 20, -4, [anyof(tf("carminite_reactor", "carminite_builder", "reappearing_block", "vanishing_block"))],
      "Tower Contraptions", deps=["tf_carminite"], xp=150, optional=True, tokens=1, subtitle="Optional: build the tower's tricks", desc=[
        "&eWhat:&r the redstone gadgets of the Dark Tower: blocks that vanish and reappear, a builder that lays bridges, and the carminite reactor.",
        "&eHow:&r encased towerwood + carminite, with redstone, a dispenser or redstone ore depending on the device (check JEI).",
        "&eTip:&r vanishing blocks make secret doors for your base; a redstone pulse opens them."]),
    Q("tf_experiment_115", 22, -2, [item(TF + "experiment_115")], "Experiment 115", deps=["tf_dark_tower"], xp=100,
      secret=True, loot="secret", subtitle="Secret: someone baked in the tower", desc=[
        "&eWhat:&r a strange cake left in the Dark Tower's chests. Nobody knows who baked it.",
        "&eHow:&r found in Dark Tower chests. Place it and take a bite.",
        "&eTip:&r there's a rumour it can be refilled. Experiment."]),
    Q("w_urghast", 20, 2, [item("twilightforest:ur_ghast_trophy")], "The Ur-Ghast", deps=["tf_dark_tower"], xp=500,
      size=1.5, shape="hexagon", subtitle="The ghast queen of the Dark Tower", desc=[
        "&6You remember the last tower of the twilight. Its keeper remembers you too.&r",
        "&eWhat:&r the great ghast at the top of the Dark Tower. Its fiery tears make more fiery metal.",
        "&eHow:&r climb the tower. Kill ghastlings near the ghast traps to charge them; charged traps pull the Ur-Ghast down so you can strike.",
        "&eTip:&r carminite from the tower makes redstone gadgets of the twilight."]),

    # ============================ the snowy branch (off the Lich; x=2..10, y=10..14) ============================
    Q("tf_yeti_cave", 4, 10, [structure(TF + "yeti_cave"), kill(TF + "alpha_yeti")], "The Yeti Cave", deps=["w_lich"], xp=200,
      loot="boss", subtitle="A cave in the snowy forest", desc=[
        "&eWhat:&r the Alpha Yeti rules a cave in the snowy forest, surrounded by its smaller yetis.",
        "&eChemistry:&r cold kills by pulling heat out of you; still air is a poor conductor of heat, which is why fur and down keep you warm.",
        "&eHow:&r the snowy forest's frost lifts after the Lich. Find the cave and fight inside.",
        "&eTip:&r when it roars, icicles fall from the roof; keep moving."]),
    Q("tf_arctic", 2, 12, [item(TF + "arctic_fur", 4), anyof(tf("arctic_helmet", "arctic_chestplate", "arctic_leggings", "arctic_boots"))],
      "Arctic Fur", deps=["tf_yeti_cave"], xp=150, optional=True, tokens=1, subtitle="Optional: dyeable armour from yeti fur", desc=[
        "&eWhat:&r ordinary yetis drop arctic fur, which makes light, warm armour you can dye.",
        "&eChemistry:&r fur traps a layer of still air, and air conducts heat about a thousand times worse than ice-cold water does.",
        "&eHow:&r kill yetis in the snowy forest. Arctic armour uses the usual shapes (check JEI)."]),
    Q("w_yeti", 4, 12, [item("twilightforest:alpha_yeti_trophy")], "The Alpha Yeti", deps=["tf_yeti_cave"], xp=300,
      subtitle="The snowy forest's boss", desc=[
        "&eWhat:&r the Alpha Yeti lives in a cave in the snowy forest. It drops its trophy, alpha yeti fur and ice bombs.",
        "&eHow:&r dodge the ice it throws and the icicles that fall from the cave roof.",
        "&eTip:&r carrying alpha yeti fur is what lets you bear the glacier's cold."]),
    Q("tf_yeti_armor", 4, 14, [anyof(tf("yeti_helmet", "yeti_chestplate", "yeti_leggings", "yeti_boots"))], "Yeti Armour", deps=["w_yeti"], xp=200,
      optional=True, tokens=1, subtitle="Optional: the Alpha Yeti's coat", desc=[
        "&eWhat:&r armour of alpha yeti fur; every piece is crafted with Protection II already on it.",
        "&eHow:&r alpha yeti fur in the usual armour shapes (check JEI).",
        "&eTip:&r the Alpha Yeti's ice bombs freeze the ground where they land; throw them at a crowd."]),
    Q("tf_aurora", 8, 10, [structure(TF + "aurora_palace"), kill(TF + "snow_queen")], "The Aurora Palace", deps=["w_yeti"], xp=300,
      loot="boss", subtitle="An ice palace on the glacier", desc=[
        "&eWhat:&r the Snow Queen's palace of packed ice and aurora blocks stands on the glacier.",
        "&eChemistry:&r real auroras are light from oxygen (green, red) and nitrogen (blue, purple) atoms excited by charged particles from the Sun.",
        "&eHow:&r the glacier opens after the Alpha Yeti. Climb the palace to the Queen's throne room.",
        "&eTip:&r break her ice shields first; she falls on you from above, so look up."]),
    Q("tf_ice_weapons", 10, 10, [anyof(tf("ice_sword", "ice_bow", "ender_bow"))], "Palace Armoury", deps=["tf_aurora"], xp=150,
      optional=True, tokens=1, subtitle="Optional: weapons from the palace caches", desc=[
        "&eWhat:&r the Aurora Palace's chests hold the Ice Sword and Ice Bow, which slow what they hit, and the Ender Bow, which swaps you with your target.",
        "&eHow:&r loot the palace's rooms and caches on your way up.",
        "&eTip:&r the Ender Bow is a fine escape tool: shoot a mob far away and trade places."]),
    Q("w_snow_queen", 8, 12, [item("twilightforest:snow_queen_trophy")], "The Snow Queen", deps=["tf_aurora"], xp=400,
      subtitle="The glacier's ice palace", desc=[
        "&eWhat:&r the Snow Queen rules the Aurora Palace on the glacier.",
        "&eHow:&r climb the palace, then break her ice shields and avoid her drop attacks.",
        "&eTip:&r beating her finishes the snowy branch of the twilight."]),
    Q("tf_queen_bows", 8, 14, [anyof(tf("triple_bow", "seeker_bow"))], "The Queen's Bows", deps=["w_snow_queen"], xp=200,
      optional=True, tokens=1, subtitle="Optional: three arrows, or arrows that seek", desc=[
        "&eWhat:&r the Snow Queen drops one of two bows: the Tri-Bow fires three arrows at once, the Seeker Bow's arrows home in on targets.",
        "&eHow:&r beat the Snow Queen; one bow drops with her trophy.",
        "&eTip:&r the Seeker Bow is perfect against the flying Ur-Ghast's ghastlings."]),
    Q("tf_biomes_cold", 6, 14, [biome(TF + "snowy_forest"), biome(TF + "glacier")], "The Frozen Regions", deps=["w_snow_queen"], xp=75,
      optional=True, tokens=1, subtitle="Optional: snowy forest and glacier", desc=[
        "&eWhat:&r the cold half of the forest: the snowy forest and the glacier beyond it.",
        "&eChemistry:&r glacier ice is blue because water absorbs red light weakly; thick, bubble-free ice lets mostly blue through.",
        "&eHow:&r visit both. Warm armour stops the blizzard's chill."]),

    # ============================ the highlands and the end (x=24..33, y=8..10.5) ============================
    Q("tf_highlands", 24, 8, [biome(TF + "highlands"), biome(TF + "thornlands")], "The Highlands", deps=["w_urghast", "w_snow_queen"], xp=300,
      size=1.5, shape="hexagon", subtitle="The plateau beyond every barrier", desc=[
        "&6Both branches beaten, the last barrier thins. You remember standing up here and looking down on all of it.&r",
        "&eWhat:&r the highlands and the thornlands ring the forest's centre. Trolls and giants live up here.",
        "&eHow:&r with the Hydra, the Ur-Ghast and the Snow Queen beaten, the acid rain over the highlands stops. Step into the thornlands' edge too; their rain only stops once you hold the Lamp of Cinders.",
        "&eTip:&r giants are huge and hit hard; fight them from range."]),
    Q("tf_trophy_wall", 24, 10.5, [item(TF + "naga_trophy"), item(TF + "lich_trophy"), item(TF + "minoshroom_trophy"), item(TF + "hydra_trophy"),
                                   item(TF + "knight_phantom_trophy"), item(TF + "ur_ghast_trophy"), item(TF + "alpha_yeti_trophy"), item(TF + "snow_queen_trophy")],
      "Trophy Wall", deps=["tf_highlands"], xp=300, optional=True, tokens=2, loot="boss",
      subtitle="Optional: all eight trophies at once", desc=[
        "&eWhat:&r a trophy from every boss of the forest, in your inventory at the same time.",
        "&eHow:&r keep the trophies you already have. Bosses can be fought again in other structures of the same kind.",
        "&eTip:&r trophies make a fine wall in your base; place them with a right-click."]),
    Q("tf_troll_cave", 27, 8, [structure(TF + "troll_cave"), item(TF + "lamp_of_cinders")], "Troll Caves", deps=["tf_highlands"], xp=250,
      subtitle="The trolls' vaults and the Lamp of Cinders", desc=[
        "&eWhat:&r caves under the highlands, full of trolls guarding vaults. The Lamp of Cinders hides in one.",
        "&eHow:&r find a troll cave in the highlands and loot its vaults. The lamp burns away the thorns that wall off the final plateau.",
        "&eTip:&r trolls throw rocks; fight them in the open, not in narrow tunnels."]),
    Q("tf_magic_beans", 27, 10.5, [item(TF + "magic_beans")], "Magic Beans", deps=["tf_troll_cave"], xp=150,
      optional=True, tokens=1, subtitle="Optional: a beanstalk to the clouds", desc=[
        "&eWhat:&r trolls drop magic beans. Planted on the glowing uberous soil beneath the clouds, they grow a beanstalk straight up.",
        "&eChemistry:&r real beans are legumes: bacteria in their root nodules fix N₂ from the air into ammonia (NH₃), the same job Haber-Bosch does with iron and heat.",
        "&eHow:&r kill trolls or loot their gardens (the gardens also hold uberous soil). Plant a bean on the glowing soil under the clouds."]),
    Q("tf_giants", 30, 10.5, [anyof(tf("giant_pickaxe", "giant_sword"))], "Giant's Tools", deps=["tf_magic_beans"], xp=250,
      optional=True, tokens=2, subtitle="Optional: a pickaxe the size of a house", desc=[
        "&eWhat:&r giant miners drop the Giant's Pickaxe, which breaks the oversized blocks of the cloud world; armoured giants drop the Giant's Sword.",
        "&eHow:&r climb the beanstalk to the clouds and beat a giant. Both can also be crafted from giant cobblestone and giant logs (check JEI).",
        "&eTip:&r giant blocks break down into normal ones: one giant log crafts into 64 oak logs."]),
    Q("tf_final_plateau", 30, 8, [biome(TF + "final_plateau")], "The Final Plateau", deps=["tf_troll_cave"], xp=300,
      subtitle="Burn through the thorns", desc=[
        "&eWhat:&r the highest ground in the forest, walled in by thorns and acid rain.",
        "&eHow:&r carry the Lamp of Cinders. Use it on the thorns to burn a path through the thornlands, then climb onto the plateau.",
        "&eTip:&r burnt thorns crumble away; don't stand in living ones, they hurt."]),
    Q("tf_final_castle", 33, 8, [structure(TF + "final_castle")], "The Unfinished Castle", deps=["tf_final_plateau"], xp=300,
      size=2.0, shape="gear", choice="pick_late", subtitle="The castle at the top of the world", desc=[
        "&6A castle on the final plateau, waiting for a ruler. You remember planning to come back for it.&r",
        "&eWhat:&r the Final Castle stands on the final plateau. Its last boss was never finished by the mod's authors, so this is the end of the road.",
        "&eHow:&r cross the plateau and step inside the castle.",
        "&eTip:&r the castle is still worth exploring for its architecture and its force-field doors."]),
    Q("tf_castle_bricks", 36, 8, [item(TF + "castle_brick", 16)], "Castle Stone", deps=["tf_final_castle"], xp=100,
      optional=True, tokens=1, subtitle="Optional: bricks from the last castle", desc=[
        "&eWhat:&r the Final Castle's pale brick, for building your own keep.",
        "&eHow:&r mine castle brick from the castle walls. Its cracked, mossy, worn and pillar variants are in JEI.",
        "&eTip:&r a stonecutter makes the stairs and pillars without waste."]),
], links=[("t5_twilight", -2, 0)])
