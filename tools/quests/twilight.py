"""Quest chapter: twilight (the Twilight Forest). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's Twilight Forest chapter quest for quest (list, order, sections and requirements only; its text is ARR,
all words here are ours); mirrored quests carry mirror="<ATM10 id>". Moved here from worlds.py (keys unchanged): w_naga, w_lich, w_minoshroom, w_hydra, w_tf_metals, w_knight, w_urghast,
w_yeti, w_snow_queen, w_uncrafting. New quests use the tf_ prefix.

Facts are from the Twilight Forest 4.8 jar: biome locks (data/twilightforest/twilight/restrictions), progression
advancements, loot tables and recipes. The pack does not change Twilight Forest except the Twilight Cake (KubeJS).
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

TF = "twilightforest:"


def tf(*names):
    return [TF + n for n in names]


CHAPTER = Chapter("twilight", "The Twilight Forest", "twilightforest:naga_trophy",
        ["A realm of permanent dusk, ruled by bosses in order."], SIDE, [
    # ============================ first steps (ATM10's start: arrival, first hunt, the raven and the map) ============================
    Q("tf_arrive", 0, 0, [dim(TF + "twilight_forest")], "Into the Dusk", deps=["t5_twilight"], xp=100, size=1.5,
      mirror="4193303999597249", section="First Steps", subtitle="Step through the flower ring", desc=[
        "&6The trees here are older than your forgetting. Their bark still knows your hand.&r",
        "&eWhat:&r the Twilight Forest: a dimension of endless dusk where every region is locked until you beat the boss before it.",
        "&eHow:&r ring a 2x2 pool of water with flowers (or grass and ferns) and drop a diamond in. The portal sends you through.",
        "&eTip:&r note the coordinates of your return portal. The forest is easy to get lost in."]),
    Q("tf_hunter", 0, 0, [kill(TF + "raven")], "First Hunt", deps=["tf_arrive"], xp=50, mirror="575E405B270BBCBC",
      subtitle="Bring down one of the forest's ravens", desc=[
        "&eWhat:&r ravens hop across the forest floor and fly off when you get close. Catching one is your first lesson in how this place moves.",
        "&eHow:&r sneak up on a raven and strike before it takes off. Any weapon will do.",
        "&eTip:&r a bow helps. Ravens drop the feathers the Magic Map Focus needs."]),
    Q("tf_dinner", 0, 0, [item(TF + "raw_venison"), item(TF + "cooked_venison"), item(TF + "maze_wafer"), item(TF + "raw_meef"),
                          item(TF + "meef_stroganoff"), item(TF + "hydra_chop"), item(TF + "experiment_115")],
      "A Twilight Feast", deps=["tf_arrive"], xp=200, optional=True, tokens=2, mirror="604F2B68B27885BF",
      subtitle="Optional: one of every dish the forest serves", desc=[
        "&eWhat:&r a full menu of the forest: venison raw and cooked, a maze wafer, raw meef, meef stroganoff, a hydra chop and a slice of Experiment 115.",
        "&eChemistry:&r cooking meat denatures its proteins: heat unravels their folded chains, which is why a steak firms up and turns opaque.",
        "&eHow:&r gather them as the boss trail takes you through the forest. Deer, minotaurs, the Minoshroom, the Hydra and the Dark Tower's chests cover the list.",
        "&eTip:&r hold one of each at the same time; it finishes the moment the last dish lands in your bag."]),

    # ============================ the forest: our own side trails (things you can do from day one) ============================
    Q("tf_oak", -4, 0, [item(TF + "twilight_oak_log", 16)], "Wood of Dusk", deps=["tf_arrive"], xp=75, optional=True, tokens=1,
      section="The Living Forest", subtitle="Optional: your first logs in the forest", desc=[
        "&eWhat:&r twilight oak is the forest's common wood. It makes mason jars, drying racks and tannin for leather.",
        "&eHow:&r chop any twilight oak. Canopy trees, mangroves and darkwood grow nearby too.",
        "&eTip:&r the forest's crafting side trails branch from here; the boss trail starts with the Naga."]),
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
    Q("tf_magic_saplings", -8, -8, [item(TF + "time_sapling"), item(TF + "sorting_sapling"), item(TF + "mining_sapling"),
                                    item(TF + "transformation_sapling")],
      "Four Hearts of the Forest", optional=True, deps=["tf_castle_doors"], xp=500, size=2.0, mirror="0ED7B25DC1AA767B", choice="pick_late",
      section="Beyond the Thorns", subtitle="All four magic saplings at once", desc=[
        "&6Four trees with a heart each. You remember planting the first of them, long before there was a forest to hold it.&r",
        "&eWhat:&r the four magic trees: Time, Sorting, Mining and Transformation. Each grows with a working core inside its trunk.",
        "&eHow:&r hollow trees hide them in the leafy caches up in their branches. Climb more than one tree to find all four, then hold one of each.",
        "&eTip:&r plant them where you want the trees for good: breaking a core only drops a plain log."]),
    Q("tf_tree_time", -6, -10, [item(TF + "time_log", 4)], "Tree of Time", deps=["tf_hollow_tree"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Timewood Clock", desc=[
        "&eWhat:&r the Timewood Clock in the trunk makes blocks around the tree tick faster: crops, saplings and machines that tick.",
        "&eHow:&r grow a Tree of Time from its sapling and collect some of its logs (any log of the tree counts).",
        "&eTip:&r plant it in the middle of a farm. Check its tooltip in JEI for the range."]),
    Q("tf_tree_transform", -8, -10, [item(TF + "transformation_log", 4)], "Tree of Transformation", deps=["tf_hollow_tree"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Heart of Transformation", desc=[
        "&eWhat:&r the Heart of Transformation slowly rewrites the biome around the tree into a Twilight one.",
        "&eHow:&r grow a Tree of Transformation from its sapling and collect some of its logs.",
        "&eTip:&r don't plant it next to a base that needs a particular biome; the change spreads."]),
    Q("tf_tree_mining", -10, -10, [item(TF + "mining_log", 4)], "Miner's Tree", deps=["tf_hollow_tree"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Minewood Core", desc=[
        "&eWhat:&r the Minewood Core gathers ore from the ground around the tree (its tooltip in JEI explains the details).",
        "&eChemistry:&r real ore is just rock rich in a mineral, like haematite (Fe₂O₃) or chalcopyrite (CuFeS₂). The tree simply finds it for you.",
        "&eHow:&r grow a Miner's Tree from its sapling and collect some of its logs."]),
    Q("tf_tree_sorting", -12, -10, [item(TF + "sorting_log", 4)], "Sorting Tree", deps=["tf_hollow_tree"], xp=100,
      optional=True, tokens=1, subtitle="Optional: grow the Sortingwood Engine", desc=[
        "&eWhat:&r the Sortingwood Engine moves items from a chest by the tree into nearby chests that already hold the same item.",
        "&eHow:&r grow a Sorting Tree from its sapling and collect some of its logs.",
        "&eTip:&r a cheap sorting room for a forest outpost; at home your storage network does it better."]),

    # --- maps (y=-6) ---
    Q("tf_focus_parts", 0, 0, [item(TF + "raven_feather"), item(TF + "torchberries", 4)], "Feather and Berries", deps=["tf_hunter"], xp=50,
      mirror="57940981E8DE55D4", subtitle="A raven's feather and a glowing berry", desc=[
        "&eWhat:&r the two forest ingredients of the Magic Map Focus.",
        "&eChemistry:&r glowing berries are a nod to real bioluminescence: an enzyme, luciferase, oxidises a molecule called luciferin, and the energy leaves as light instead of heat.",
        "&eHow:&r ravens hop about the forest floor and drop feathers; Dark Tower chests hold them too. Torchberries hang from cave and hollow-hill roofs, and skeleton druids drop them.",
        "&eTip:&r the Moonworm Queen eats torchberries: each one restores 64 of its durability."]),
    Q("tf_map_focus", -6, -6, [item(TF + "magic_map_focus")], "Magic Map Focus", deps=["tf_focus_parts"], xp=75, mirror="4F66DF6B494BEFF3",
      subtitle="Feather, berry and glowstone", desc=[
        "&eWhat:&r the focus that turns paper into a Magic Map of the Twilight Forest.",
        "&eHow:&r a raven feather, torchberries and glowstone dust, shapeless. Ravens hop about the forest floor; torchberries hang from cave roofs (skeleton druids drop them too).",
        "&eTip:&r torchberries also make berry torches, which never need fuel."]),
    Q("tf_map", -8, -6, [anyof(tf("magic_map", "filled_magic_map"))], "A Map of Dusk", deps=["tf_map_focus"], xp=50,
      optional=True, tokens=1, mirror="0990D6CEE042F44E", subtitle="Optional: the forest draws its own map", desc=[
        "&eWhat:&r the Magic Map shows Twilight biomes and marks every boss structure with an icon.",
        "&eHow:&r eight paper around the focus makes a blank Magic Map. A blank or a filled one counts; use it inside the forest to fill it in.",
        "&eTip:&r the Maze Map does the same job inside the Minoshroom's labyrinth; Nature's Compass finds biomes, Explorer's Compass finds structures."]),

    # --- hollow hills (y=-4) ---
    Q("tf_hollow_hill", -6, -4, [structure(TF + "small_hollow_hill")], "Hollow Hills", deps=["tf_oak"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a hill full of ore and spiders", desc=[
        "&eWhat:&r hollow hills are mounds with a cave inside, lined with ore blocks, spawners and a treasure chest.",
        "&eHow:&r find a small hollow hill (the mounds in the plain forest) and step inside.",
        "&eTip:&r break the spawners first. The ore inside is free feedstock for your ore lines."]),
    Q("tf_ore_magnet", -8, -4, [item(TF + "ore_magnet")], "Ore Magnet", deps=["tf_arrive"], xp=100,
      mirror="5FE4DAE8F41B1437", section="Forest Treasures", subtitle="Pull the vein to you", desc=[
        "&eWhat:&r a hollow hill treasure that drags a vein of ore out of the rock towards you.",
        "&eChemistry:&r real mines do a version of this: magnetic separation pulls magnetite (Fe₃O₄) out of crushed rock, because it is strongly ferromagnetic.",
        "&eHow:&r loot it from a hollow hill chest (any size). Aim at stone and use it."]),
    Q("tf_big_hill", -10, -4, [structure(TF + "large_hollow_hill")], "The Great Hollow Hill", deps=["tf_hollow_hill"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the biggest hill, the best chest", desc=[
        "&eWhat:&r large hollow hills hold the most ore, the most spawners and the richest chest of the three sizes.",
        "&eHow:&r look for the biggest mounds in the forest and step inside.",
        "&eTip:&r light the cave up as you go; the spawners inside are what makes it dangerous."]),
    Q("tf_hill_curios", -12, -4, [item(TF + "peacock_feather_fan")], "Peacock Feather Fan",
      deps=["tf_arrive"], xp=100, mirror="1464D45C474464DB", section="Forest Treasures", subtitle="A fan that blows a gale", desc=[
        "&eWhat:&r a fan of peacock feathers. Swing it and a gust of wind shoves mobs, items and you yourself.",
        "&eHow:&r loot it from hollow hill chests and the Lich Tower's rooms.",
        "&eTip:&r fan yourself upward mid-jump to clear a gap you couldn't otherwise reach."]),
    Q("tf_moonworm", 0, 0, [item(TF + "moonworm_queen")], "Moonworm Queen", deps=["tf_arrive"], xp=100, mirror="60FC2DAEA954A849",
      section="Forest Treasures", subtitle="A light source that fires glowing worms", desc=[
        "&eWhat:&r a staff that shoots moonworms: each one sticks to the block it hits and glows there for good.",
        "&eChemistry:&r a cold light like this is chemiluminescence: a reaction leaves a molecule in an excited state, and it sheds the energy as a photon instead of heat.",
        "&eHow:&r a treasure from hollow hill and tower chests.",
        "&eTip:&r it wears down with use; torchberries repair it (check JEI)."]),
    Q("tf_transform_powder", 0, 0, [item(TF + "transformation_powder")], "Transformation Powder", deps=["tf_arrive"], xp=100,
      mirror="0E9DE6293DF611E1", section="Forest Treasures", subtitle="Turn a mob into its Twilight cousin", desc=[
        "&eWhat:&r a dust that changes some mobs into their Twilight relatives, and back again (JEI lists the pairs).",
        "&eHow:&r found in forest chests (the Lich Tower and hollow hills are good bets). Use it on a mob to see what it turns into.",
        "&eTip:&r it's a cheap way to bring Twilight animals home without a lead and a long walk."]),

    # --- steeleaf and ironwood (y=-2 / 0) ---
    Q("tf_steeleaf", -6, -2, [tick()], "Steeleaf", deps=['tf_oak'], optional=True, tokens=0, xp=0, icon="twilightforest:steeleaf_ingot", subtitle="Moved: see Steeleaf Ingot", desc=["&eMoved:&r this step is now \"Steeleaf Ingot\" on the Armour and Harvest Tiers page. Click to dismiss."]),
    Q("tf_steeleaf_gear", -8, -2, [item(TF + "steeleaf_helmet"), item(TF + "steeleaf_chestplate"), item(TF + "steeleaf_leggings"),
                                    item(TF + "steeleaf_boots")],
      "Steeleaf Armour", optional=True, deps=["tf_arrive"], xp=150, mirror="2BEBF66D7EA594FA", section="Forest Treasures",
      subtitle="A full suit of metal-hard leaves", desc=[
        "&eWhat:&r steeleaf armour and tools come pre-enchanted; the pickaxe even has Fortune II built in.",
        "&eHow:&r helmet, chestplate, leggings and boots in the usual armour shapes, from steeleaf ingots (check JEI).",
        "&eTip:&r a Fortune II pickaxe this early doubles ore from your best veins."]),
    Q("tf_ironwood", -6, 0, [item(TF + "liveroot", 2), item(TF + "ironwood_ingot", 4)], "Ironwood", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: living root, iron and gold", desc=[
        "&eWhat:&r ironwood is the forest's first metal: tougher than iron, and needed for the Twilight Metals milestone.",
        "&eChemistry:&r smelting raw iron is a reduction: carbon monoxide strips the oxygen, Fe₂O₃ + 3CO → 2Fe + 3CO₂. The liveroot and gold just make it Twilight.",
        "&eHow:&r liveroot + raw iron + a gold nugget makes 2 raw ironwood (shapeless). Smelt or blast it. Liveroot grows in the root tangles underground.",
        "&eTip:&r bring a stack of raw iron from home; liveroot is the only forest part."]),
    Q("tf_ironwood_gear", -8, 0, [item(TF + "ironwood_helmet"), item(TF + "ironwood_chestplate"), item(TF + "ironwood_leggings"),
                                   item(TF + "ironwood_boots")],
      "Ironwood Armour", optional=True, deps=["tf_arrive"], xp=150, mirror="40258842B0359A2D", section="Forest Treasures",
      subtitle="A full suit that comes enchanted", desc=[
        "&eWhat:&r ironwood armour comes with enchantments built in, and so do its tools (the pickaxe has Efficiency I).",
        "&eHow:&r helmet, chestplate, leggings and boots in the usual shapes from ironwood ingots (the Ironwood side quest shows how to make them).",
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
    Q("tf_venison", 0, 0, [item(TF + "raw_venison", 4), item(TF + "cooked_venison", 4)], "Venison", deps=["tf_oak"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the forest's everyday meat", desc=[
        "&eWhat:&r Twilight deer drop raw venison and leather. Cooked, it's a steady food for long trips.",
        "&eChemistry:&r red meat is red because of myoglobin, an iron protein that holds oxygen. Cooking unfolds it and oxidises its iron from Fe²⁺ to Fe³⁺, which turns the meat brown.",
        "&eHow:&r hunt deer in the forest, then cook the venison in a furnace, smoker or on a campfire.",
        "&eTip:&r save a few raw pieces for the drying rack: venison jerky keeps forever."]),

    # --- charms (y=8) ---
    Q("tf_charm_life", -6, 8, [item(TF + "charm_of_life_1")], "Charm of Life", deps=["tf_arrive"], xp=100,
      mirror="6F67079A453DAABE", section="Forest Treasures", subtitle="One death, refused", desc=[
        "&eWhat:&r carried in your inventory, the Charm of Life is used up to save you from a killing blow.",
        "&eHow:&r a chest find: fallen trunks, hollow hills, the Lich Tower, the stronghold and the Aurora Palace all have them.",
        "&eTip:&r carry one into every boss fight."]),
    Q("tf_charm_life2", 0, 0, [item(TF + "charm_of_life_2")], "Greater Charm of Life", deps=["tf_charm_life"], xp=200, size=1.5,
      mirror="15006CF73F8CAB7C", subtitle="Four charms make a stronger one", desc=[
        "&6One death refused was never enough for you. You remember carrying a better promise.&r",
        "&eWhat:&r the second Charm of Life saves you from a killing blow and leaves you in far better shape than the first one does.",
        "&eHow:&r four Charms of Life I, shapeless, make one Charm of Life II (check JEI). Forest chests fill the stack.",
        "&eTip:&r it's used up like the first one, so carry it into the hardest fights only."]),
    Q("tf_charm_keeping", -8, 8, [item(TF + "charm_of_keeping_1")], "Charm of Keeping", deps=["tf_maze_map"], xp=100,
      mirror="610F9E9D0B5131C7", subtitle="Keep your things when you fall", desc=[
        "&eWhat:&r the Charm of Keeping is used up when you die and keeps some of your items with you. Higher tiers keep more.",
        "&eHow:&r found in many forest chests; maze slimes drop them too.",
        "&eTip:&r the forest's death caskets also hold what you drop, so you can come back for it."]),
    Q("tf_charm_upgrade", -10, 8, [item(TF + "charm_of_keeping_2")], "Charm of Keeping II",
      deps=["tf_charm_keeping"], xp=150, mirror="4665E6FD0AAED164", subtitle="Four charms make one better", desc=[
        "&eWhat:&r the second Charm of Keeping saves more of your inventory when you die than the first.",
        "&eHow:&r four Charms of Keeping I, shapeless, make one Charm of Keeping II (check JEI).",
        "&eTip:&r don't stop here: the third tier is the one worth carrying."]),
    Q("tf_charm_keeping3", 0, 0, [item(TF + "charm_of_keeping_3")], "Charm of Keeping III", deps=["tf_charm_upgrade"], xp=250, size=1.5,
      mirror="3A3ED88027331A6C", subtitle="Die, and keep everything", desc=[
        "&6Even death used to hand your things back. You remember why.&r",
        "&eWhat:&r the top Charm of Keeping: when it's used up, you keep your whole inventory.",
        "&eHow:&r four Charms of Keeping II make one (check JEI). That's sixteen of the first tier in all.",
        "&eTip:&r one in your pocket turns a lost boss fight into a long walk back."]),

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
    Q("tf_ram_trophy", 0, 0, [item(TF + "quest_ram_trophy")], "The Ram's Own Trophy", deps=["tf_arrive"], xp=100,
      optional=True, tokens=2, loot="secret", mirror="4DA0725E089D7C91", section="Forest Treasures",
      subtitle="Optional: a bundle with a head in it", desc=[
        "&eWhat:&r the Questing Ram's reward comes in a bundle: its own trophy plus a pile of metal and gem blocks.",
        "&eHow:&r open the bundle the ram gave you and keep the trophy. Place it on a wall next to your boss trophies.",
        "&eTip:&r it's the only trophy in the forest you earn without a fight."]),

    # ============================ the boss line (lairs y=0, spoils y=2) ============================
    # --- the Naga (x=0) ---
    Q("tf_courtyard", 0, 0, [structure(TF + "naga_courtyard"), kill(TF + "naga")], "The Naga's Courtyard", deps=["tf_arrive"], xp=150,
      optional=True, tokens=1, loot="boss", subtitle="Optional: find the serpent's courtyard and win", desc=[
        "&eWhat:&r the first boss. Each boss lifts the curse on the next region (hunger, fire, darkness, frost or acid rain), so the order matters.",
        "&eHow:&r the courtyard is a walled stone garden in the plain forest (the Magic Map marks it). Fight inside it.",
        "&eTip:&r the Naga charges in straight lines; sidestep, then hit it while it turns."]),
    Q("tf_naga_armor", 0, -2, [item(TF + "naga_chestplate"), item(TF + "naga_leggings")], "Naga Scale Armour", deps=["w_naga"], xp=150,
      mirror="4D4AB60B3B1CD437", subtitle="Armour from the serpent", desc=[
        "&eWhat:&r a tunic and leggings of naga scales. Both come pre-enchanted: Fire Protection III on the tunic, Protection III on the leggings.",
        "&eHow:&r eight scales for the tunic, seven for the leggings, in the usual armour shapes (check JEI).",
        "&eTip:&r the fire protection pays off later in the Hydra's fire swamp."]),
    Q("w_naga", 0, 2, [item(TF + "naga_trophy"), item(TF + "naga_scale", 4)], "The Naga", deps=["tf_arrive"], xp=200,
      mirror="3531B28F14CF72A2", section="The Boss Trail", subtitle="Trophy and scales from the forest's first boss", desc=[
        "&eWhat:&r a great serpent coiled in a stone courtyard. Its scales unlock the path forward and make naga armour.",
        "&eHow:&r its courtyard is a walled stone garden in the plain forest (the Magic Map marks it). The Naga drops its trophy and scales; hit it when it stops charging.",
        "&eTip:&r the Lich Tower is next. Its door won't open until the Naga is dead."]),

    # --- the Lich (x=4) ---
    Q("tf_lich_tower", 4, 0, [structure(TF + "lich_tower"), kill(TF + "lich")], "The Lich Tower", deps=["w_naga"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: climb the tower and break the sorcerer", desc=[
        "&eWhat:&r the Lich waits at the top of a tall stone tower. Beating it opens the swamp, the dark forest and the snowy forest.",
        "&eHow:&r climb through the tower's rooms to the top. Break the shields orbiting it before you can hurt it.",
        "&eTip:&r the Lich's shadow clones are distractions; watch for the one that casts."]),
    Q("tf_scepters", 4, -2, [item(TF + "twilight_scepter")], "Scepter of Twilight", deps=["w_lich"], xp=150,
      mirror="212EC1F41227184D", section="Scepters of the Lich", subtitle="Bolts of pure dusk", desc=[
        "&eWhat:&r the Lich drops one of four scepters per kill. This one fires bolts of twilight energy at whatever you aim at.",
        "&eHow:&r if your Lich dropped a different scepter, other Lich Towers have their own Lich. Beat one again.",
        "&eTip:&r scepters recharge on a crafting grid with their own item (check JEI). The Renewal enchantment recharges them automatically."]),
    Q("tf_scepter_lifedrain", 0, 0, [item(TF + "lifedrain_scepter")], "Scepter of Lifedrain", deps=["w_lich"], xp=150,
      mirror="6CB1BFBA10DF24E4", subtitle="Hurt them, heal yourself", desc=[
        "&eWhat:&r a scepter that drains a target's health in a steady beam and feeds some of it back to you.",
        "&eHow:&r one of the four scepters the Lich can drop. Fight more Liches until it turns up.",
        "&eTip:&r its charge runs down; recharge it on a crafting grid (check JEI)."]),
    Q("tf_scepter_zombie", 0, 0, [item(TF + "zombie_scepter")], "Scepter of Zombies", deps=["w_lich"], xp=150,
      mirror="3908F7C80154D9CA", subtitle="Raise a few loyal dead", desc=[
        "&eWhat:&r a scepter that summons zombies that fight for you for a while before they crumble.",
        "&eHow:&r one of the four scepters the Lich can drop.",
        "&eTip:&r summon them in a doorway: they hold a corridor while you heal."]),
    Q("tf_scepter_fort", 0, 0, [item(TF + "fortification_scepter")], "Scepter of Fortification", deps=["w_lich"], xp=150,
      mirror="3371570F189DF994", subtitle="Shields that circle you", desc=[
        "&eWhat:&r a scepter that wraps you in orbiting shields, the same trick the Lich used on you.",
        "&eHow:&r one of the four scepters the Lich can drop.",
        "&eTip:&r cast it before a boss's opening attack, not after it."]),
    Q("w_lich", 4, 2, [item("twilightforest:lich_trophy")], "The Lich", deps=["w_naga"], xp=300, mirror="0107D516E038E0DB",
      subtitle="A sorcerer's trophy and scepters", desc=[
        "&eWhat:&r the Lich drops its trophy, one of its scepters and golden gear.",
        "&eHow:&r pick up the trophy from the top of the tower once it falls.",
        "&eTip:&r three ways open now: the labyrinth in the swamp, the stronghold in the dark forest, and the snowy forest below."]),

    # --- the Minoshroom (x=8) ---
    Q("tf_labyrinth", 8, 0, [structure(TF + "labyrinth"), kill(TF + "minoshroom")], "The Labyrinth", deps=["tf_maze_map"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: the maze under the swamp", desc=[
        "&eWhat:&r beneath the swamp lies a maze of mossy stone. The Minoshroom waits in a room at its heart.",
        "&eHow:&r enter through the stairs in the swamp. A Maze Map (made with a Maze Map Focus) shows the corridors.",
        "&eTip:&r mosquito swarms bite in the swamp; bring plenty of food."]),
    Q("tf_mazebreaker", 6, -2, [item(TF + "mazebreaker_pickaxe")], "Mazebreaker", deps=["tf_maze_map"], xp=250,
      mirror="51BC981AB4CFAD95", subtitle="The labyrinth's jackpot", desc=[
        "&eWhat:&r a diamond pickaxe that chews through maze stone, found only in the labyrinth's best vault.",
        "&eHow:&r labyrinth vaults are sealed rooms off the corridors. The jackpot vault is rare; check every one.",
        "&eTip:&r a Maze Map shows unexplored rooms as gaps in the corridors."]),
    Q("tf_maze_focus", 8, -2, [item(TF + "maze_map_focus")], "Maze Map Focus", deps=["w_lich"], xp=150,
      optional=True, tokens=1, subtitle="Optional: a minotaur's map lens", desc=[
        "&eWhat:&r the focus for Maze Maps, and the heart of the Uncrafting Table.",
        "&eHow:&r minotaurs in the labyrinth drop it. Kill them as you search for the Minoshroom.",
        "&eTip:&r keep a spare; the Uncrafting Table eats one."]),
    Q("tf_minotaur_axe", 10, -2, [item(TF + "diamond_minotaur_axe")], "Minotaur Axe", deps=["w_minoshroom"], xp=150,
      mirror="730AF9210F00018E", subtitle="The Minoshroom's weapon", desc=[
        "&eWhat:&r a heavy diamond axe dropped by the Minoshroom.",
        "&eHow:&r beat the Minoshroom; the axe drops with its stroganoff.",
        "&eTip:&r it's an axe, so it still chops wood; keep it for both jobs."]),
    Q("tf_meef", 0, 0, [item(TF + "raw_meef", 4), item(TF + "cooked_meef", 4)], "Meef", deps=["tf_labyrinth"], xp=75,
      optional=True, tokens=1, subtitle="Optional: minotaur meat, a maze staple", desc=[
        "&eWhat:&r the labyrinth's minotaurs drop raw meef. Cooked meef steaks are among the best plain foods in the forest.",
        "&eChemistry:&r a seared crust is the Maillard reaction: amino acids and sugars react above about 140 °C into hundreds of browned flavour compounds.",
        "&eHow:&r kill minotaurs in the labyrinth's corridors, then cook the meef in a furnace, smoker or on a campfire.",
        "&eTip:&r raw meef also dries into meef jerky on a drying rack."]),
    Q("tf_maze_wafer", 0, 0, [item(TF + "maze_wafer", 8)], "Maze Wafers", deps=["tf_labyrinth"], xp=50,
      optional=True, tokens=1, subtitle="Optional: biscuits from the labyrinth's larder", desc=[
        "&eWhat:&r small dry wafers stashed in labyrinth rooms, dead ends and vaults. Goblin strongholds and the Aurora Palace keep some too.",
        "&eChemistry:&r dry food keeps because microbes need free water; bakers call this low water activity, the same trick as jerky and hard tack.",
        "&eHow:&r open the labyrinth's chests as you work through the maze.",
        "&eTip:&r keep a few in a pocket as emergency food for the rest of the boss line."]),
    Q("tf_maze_map", 8, -4, [anyof(tf("maze_map", "filled_maze_map")), item(TF + "raw_meef", 3)], "Into the Labyrinth", deps=["w_lich"], xp=150,
      mirror="4B95D48D7525FFAD", section="The Labyrinth", subtitle="A maze map and a few cuts of meef", desc=[
        "&eWhat:&r the swamp labyrinth under the Lich's old lands: a Maze Map to find your way and meef from the minotaurs that patrol it.",
        "&eHow:&r minotaurs drop raw meef and the Maze Map Focus; eight paper around the focus makes a blank Maze Map (blank or filled counts).",
        "&eTip:&r one map covers one level; make another for each floor."]),
    Q("tf_ore_map", 8, -6, [anyof(tf("ore_map", "filled_ore_map"))], "Ore Map", deps=["tf_maze_map"], xp=200,
      optional=True, tokens=2, mirror="6F957D07AA74F16E", subtitle="Optional: a map that shows ore", desc=[
        "&eWhat:&r a Maze Map upgraded to also mark the ore around you.",
        "&eHow:&r a blank Maze Map + a diamond block + a gold block + an iron block, shapeless. Blank or filled counts.",
        "&eTip:&r expensive, but it finds rich pockets for your ore lines fast."]),
    Q("w_uncrafting", 10, -4, [item("twilightforest:uncrafting_table")], "Uncrafting Table", deps=["tf_maze_focus"], xp=75,
      optional=True, tokens=1, subtitle="Optional: undo a crafting recipe", desc=[
        "&eWhat:&r the Twilight Forest's table that turns crafted items back into their ingredients, for XP.",
        "&eChemistry:&r the Alchemistry Dissolver goes further: it uncrafts all the way down to elements.",
        "&eHow:&r eight crafting tables around a Maze Map Focus (this pack leaves the recipe and the table unchanged).",
        "&eTip:&r the XP cost rises with the item's value, and some recipes can't be reversed; the table tells you."]),
    Q("w_minoshroom", 8, 2, [item("twilightforest:minoshroom_trophy"), item(TF + "meef_stroganoff")], "The Minoshroom", deps=["tf_maze_map"], xp=300,
      mirror="04440BB2EFFD6DD9", subtitle="Its trophy and its stroganoff", desc=[
        "&eWhat:&r a mushroom minotaur in the swamp labyrinth. It drops its trophy, meef stroganoff and a mighty axe.",
        "&eHow:&r the Maze Map helps you find it in the maze. Sidestep its charges.",
        "&eTip:&r keep one bowl of stroganoff in your bag for this quest, and eat another before the fire swamp."]),
    Q("tf_stroganoff", 10, 2, [item(TF + "meef_stroganoff")], "Mighty Stroganoff", deps=["w_minoshroom"], xp=150,
      optional=True, tokens=1, subtitle="Optional: eat it to bear the fire swamp", desc=[
        "&eWhat:&r the fire swamp sets you alight until your body is used to its heat. Eating meef stroganoff does that.",
        "&eHow:&r eat one meef stroganoff from the Minoshroom, and keep another in your inventory for this quest.",
        "&eTip:&r it's also one of the best foods in the forest: a full bowl of hunger."]),

    # --- the Hydra (x=12) ---
    Q("tf_hydra_lair", 12, 0, [structure(TF + "hydra_lair"), kill(TF + "hydra")], "The Hydra's Lair", deps=["w_minoshroom"], xp=250,
      optional=True, tokens=1, loot="boss", subtitle="Optional: a cave in the fire swamp", desc=[
        "&eWhat:&r the Hydra lives in a hill cave in the fire swamp, the hottest place in the forest.",
        "&eChemistry:&r swamps really do burn: rotting plants release methane (CH₄), which can ignite as marsh fire.",
        "&eHow:&r eat the stroganoff first or the swamp burns you. Strike the heads when they lunge.",
        "&eTip:&r the heads regrow if you're slow; pressure one at a time."]),
    Q("tf_biomes_wild", 12, -2, [biome(TF + "swamp"), biome(TF + "fire_swamp"), biome(TF + "dark_forest")], "The Wild Regions",
      deps=["tf_hydra_lair"], xp=100, optional=True, tokens=1, subtitle="Optional: swamp, fire swamp and dark forest", desc=[
        "&eWhat:&r the regions you fought through on the main line. Walk through each once you've earned it.",
        "&eHow:&r Nature's Compass points to each biome. The Lich lifts the swamp's hunger and the dark forest's darkness; the stroganoff lifts the fire swamp's burning.",
        "&eTip:&r a quick visit counts; you don't need to stay."]),
    Q("w_hydra", 12, 2, [item("twilightforest:hydra_trophy")], "The Hydra", deps=["w_minoshroom"], xp=400,
      mirror="7026E46FD8B3A81D", subtitle="Three heads in the fire swamp", desc=[
        "&eWhat:&r the Hydra breathes fire from three heads. It drops its trophy, fiery blood and hydra chops.",
        "&eHow:&r eat meef stroganoff first or the fire swamp burns you. Fire resistance helps; hit the heads when they lunge, and keep up the pressure.",
        "&eTip:&r a hydra chop is a huge meal that also heals; save them for boss fights."]),
    Q("tf_fiery", 12, 4, [tick()], "Fiery Metal", deps=['w_hydra'], optional=True, tokens=0, xp=0, icon="twilightforest:fiery_ingot", subtitle="Moved: see Fiery Ingot", desc=["&eMoved:&r this step is now \"Fiery Ingot\" on the Armour and Harvest Tiers page. Click to dismiss."]),
    Q("tf_hydra_chop", 0, 0, [item(TF + "hydra_chop")], "Hydra Chop", deps=["w_hydra"], xp=100,
      optional=True, tokens=1, subtitle="Optional: one bite fills you up", desc=[
        "&eWhat:&r a giant cut of Hydra meat. Eating one fills your whole hunger bar at once.",
        "&eChemistry:&r food energy is measured by burning food in a bomb calorimeter: the heat released (about 4 kcal per gram of protein, 9 per gram of fat) is what your body can extract by slower oxidation.",
        "&eHow:&r the Hydra drops them when it dies. Fight another Hydra in a different lair for more.",
        "&eTip:&r eat it when your hunger bar is empty; the mod has an advancement for exactly that."]),
    Q("tf_fiery_gear", 10, 6, [item(TF + "fiery_sword"), item(TF + "fiery_pickaxe")],
      "Fiery Sword and Pickaxe", deps=["w_hydra"], xp=200, mirror="111F2EE85FB0A455", subtitle="A pickaxe that smelts as it digs", desc=[
        "&eWhat:&r the Fiery Pickaxe smelts the ore it mines on the spot; the sword sets targets alight.",
        "&eChemistry:&r smelting is reduction: heat plus carbon pulls the oxygen off a metal oxide. The pickaxe does the furnace's job at the moment you mine.",
        "&eHow:&r fiery ingots with blaze rods (check JEI). The Fiery Metal side quest shows how to make the ingots.",
        "&eTip:&r auto-smelting skips your ore doubling. Use it on things you'd only smelt anyway."]),
    Q("tf_fiery_armor", 0, 0, [item(TF + "fiery_helmet"), item(TF + "fiery_chestplate"), item(TF + "fiery_leggings"), item(TF + "fiery_boots")],
      "Fiery Armour", optional=True, deps=["w_hydra"], xp=200, mirror="1FF5906DF721D091", subtitle="A suit that burns whoever hits it", desc=[
        "&eWhat:&r armour of fiery metal: tough, and it sets attackers alight when they strike you.",
        "&eChemistry:&r a metal that glows when hot is showing black-body radiation: the hotter it gets, the more its light shifts from dull red to yellow-white.",
        "&eHow:&r fiery ingots in the usual armour shapes (check JEI). Fiery blood from the Hydra or fiery tears from the Ur-Ghast make the ingots.",
        "&eTip:&r it pairs well with the fire swamp, where everything else around you is burning anyway."]),

    # --- metals milestone and knightmetal (x=13..18, y=4..8) ---
    Q("tf_armor_shards", 14, 4, [item(TF + "armor_shard", 9)], "Armour Shards", deps=["w_hydra"], xp=150,
      optional=True, tokens=1, subtitle="Optional: knock the plates off goblins", desc=[
        "&eWhat:&r shards of knightmetal, the stronghold's metal. Nine make a shard cluster.",
        "&eHow:&r goblin knights and block-and-chain goblins in the Goblin Knight Stronghold drop them; helmet crabs on the shore drop them too.",
        "&eTip:&r the dark forest has been safe to walk since the Lich; only its centre stays dark."]),
    Q("tf_knightmetal", 14, 6, [item(TF + "armor_shard_cluster"), item(TF + "knightmetal_ingot", 4)], "Knightmetal", deps=["tf_armor_shards"], xp=200,
      optional=True, tokens=1, subtitle="Optional: melt the shards back together", desc=[
        "&eWhat:&r knightmetal ingots, for the heaviest armour and weapons in the forest.",
        "&eChemistry:&r remelting scrap is how most real steel is made today: an electric arc furnace melts recycled metal back into new ingots.",
        "&eHow:&r nine armour shards make a cluster (shapeless). Smelt or blast the cluster for one ingot."]),
    Q("w_tf_metals", 13, 8, [item("twilightforest:ironwood_ingot", 4), item("twilightforest:knightmetal_ingot", 4), item("twilightforest:fiery_ingot", 2)], "Twilight Metals",
      deps=["hv_mat_fiery", "tf_knightmetal"], xp=250, subtitle="Ironwood, knightmetal and fiery metal", optional=True, tokens=1, desc=[
        "&eWhat:&r the three alloys found nowhere else, for strong tools and armour.",
        "&eHow:&r ironwood from liveroot (see the forest), knightmetal from armour shards, fiery metal from iron and fiery blood or tears.",
        "&eTip:&r knightmetal armour and tools are great against the Knight Phantoms."]),
    Q("tf_knight_gear", 16, 6, [item(TF + "knightmetal_helmet"), item(TF + "knightmetal_chestplate"), item(TF + "knightmetal_leggings"),
                                 item(TF + "knightmetal_boots")],
      "Knightmetal Armour", optional=True, deps=["w_knight"], xp=200, mirror="25906B43A198B72F", section="The Knight's Armoury",
      subtitle="Plate fit for the phantoms", desc=[
        "&eWhat:&r a full set of knightmetal armour, the heaviest plate the forest makes.",
        "&eHow:&r knightmetal ingots in the usual armour shapes (check JEI). The Knightmetal side quest shows how to make the ingots.",
        "&eTip:&r the phantoms drop knightmetal weapons too, so the fight helps pay for the set."]),
    Q("tf_phantom_armor", 0, 0, [item(TF + "phantom_helmet"), item(TF + "phantom_chestplate")], "Phantom Armour", deps=["w_knight"], xp=200,
      mirror="0A207A437AF153AA", subtitle="A ghost knight's helm and plate", desc=[
        "&eWhat:&r the phantom helmet and chestplate, worn by the Knight Phantoms and dropped when they fall. Both come enchanted.",
        "&eHow:&r beat the Knight Phantoms; their armour drops with their loot. Another stronghold has another six phantoms if you're missing a piece.",
        "&eTip:&r phantom armour can't be crafted, so repair it with knightmetal rather than letting it break."]),
    Q("tf_block_chain", 18, 6, [item(TF + "knightmetal_sword"), item(TF + "knightmetal_pickaxe"), item(TF + "knightmetal_axe"),
                                 item(TF + "block_and_chain"), item(TF + "knightmetal_shield")],
      "Knight's Arms", optional=True, deps=["w_knight"], xp=250, mirror="607D592CE102C82E", subtitle="Sword, pickaxe, axe, flail and shield", desc=[
        "&eWhat:&r the full knightmetal arsenal: sword, pickaxe and axe, the Block and Chain (a thrown flail that smashes blocks and mobs) and the Knightmetal Shield.",
        "&eHow:&r the tools use knightmetal ingots in the usual shapes. The flail and shield start with a knightmetal ring; the shield also needs towerwood (check JEI).",
        "&eTip:&r the shield needs towerwood from the Dark Tower."]),

    # --- the Knight Phantoms (x=16) ---
    Q("tf_stronghold", 16, 0, [structure(TF + "knight_stronghold"), kill(TF + "knight_phantom", 6)], "The Goblin Stronghold", deps=["w_hydra"], xp=300,
      optional=True, tokens=1, loot="boss", subtitle="Optional: six phantoms under the dark forest", desc=[
        "&eWhat:&r the Knight Phantoms haunt the deepest room of the Goblin Knight Stronghold, buried under the dark forest.",
        "&eHow:&r find the entrance in the dark forest (the Magic Map marks it). Inside, place a boss trophy on the Trophy Pedestal to wake the phantoms, then kill all six.",
        "&eTip:&r the stronghold opens after the Lich; this page sends you after the Hydra so you arrive with fiery and knightmetal gear."]),
    Q("w_knight", 16, 2, [item("twilightforest:knight_phantom_trophy")], "The Knight Phantoms", deps=["w_hydra"], xp=400,
      mirror="3DCF26B53AE1EBF6", subtitle="Six ghosts in the goblin stronghold", desc=[
        "&eWhat:&r six phantom knights guard the Goblin Stronghold in the dark forest. Their trophy drops with the last one.",
        "&eHow:&r they wait deep inside the stronghold. Knightmetal armour helps.",
        "&eTip:&r beating them lifts the darkness on the dark forest's centre, where the Dark Tower stands."]),

    # --- the Ur-Ghast (x=20) ---
    Q("tf_dark_tower", 20, 0, [structure(TF + "dark_tower"), kill(TF + "ur_ghast")], "The Dark Tower", deps=["w_knight"], xp=350,
      optional=True, tokens=1, loot="boss", subtitle="Optional: climb to the Ur-Ghast", desc=[
        "&eWhat:&r a huge tower of towerwood in the centre of the dark forest, with the Ur-Ghast at the top.",
        "&eHow:&r climb through the tower's floors using its carminite contraptions; redstone opens the way in many rooms. A tower key from a chest opens the locked doors.",
        "&eTip:&r towerwood borers eat through the walls; kill them before they swarm."]),
    Q("tf_carminite", 20, -2, [tick()], "Carminite", deps=['tf_dark_tower'], optional=True, tokens=0, xp=0, icon="twilightforest:carminite", subtitle="Moved: see Carminite", desc=["&eMoved:&r this step is now \"Carminite\" on the Armour and Harvest Tiers page. Click to dismiss."]),
    Q("tf_tower_devices", 20, -4, [item(TF + "carminite_builder"), item(TF + "carminite_reactor")],
      "Tower Machinery", deps=["w_urghast"], xp=200, mirror="7B4A687EB505C2FF", subtitle="A bridge builder and a carminite reactor", desc=[
        "&eWhat:&r two of the Dark Tower's devices: the Carminite Builder, which lays a temporary bridge in the direction you face, and the Carminite Reactor.",
        "&eHow:&r encased towerwood and carminite, with a dispenser for the builder and redstone ore for the reactor (check JEI).",
        "&eTip:&r treat the reactor with care: read its JEI page before you power one."]),
    Q("tf_vanishing", 0, 0, [item(TF + "reappearing_block"), item(TF + "vanishing_block")], "Now You See It", deps=["w_urghast"], xp=150,
      mirror="01748C2CD9C97523", subtitle="Blocks that vanish on a signal", desc=[
        "&eWhat:&r the Dark Tower's trick doors: a vanishing block disappears when powered, a reappearing block vanishes and then comes back by itself.",
        "&eHow:&r encased towerwood around carminite, with towerwood for vanishing blocks and redstone for reappearing ones (check JEI).",
        "&eTip:&r a hidden base entrance: a pressure plate and a wall of vanishing blocks."]),
    Q("tf_experiment_115", 22, -2, [item(TF + "experiment_115")], "Experiment 115", deps=["tf_dark_tower"], xp=100,
      secret=True, loot="secret", subtitle="Secret: someone baked in the tower", desc=[
        "&eWhat:&r a strange cake left in the Dark Tower's chests. Nobody knows who baked it.",
        "&eHow:&r found in Dark Tower chests. Place it and take a bite.",
        "&eTip:&r there's a rumour it can be refilled. Experiment."]),
    Q("w_urghast", 20, 2, [item("twilightforest:ur_ghast_trophy")], "The Ur-Ghast", deps=["w_knight"], xp=500,
      mirror="688C911ECFB2F134", subtitle="The ghast queen of the Dark Tower", desc=[
        "&6You remember the last tower of the twilight. Its keeper remembers you too.&r",
        "&eWhat:&r the great ghast at the top of the Dark Tower. Its fiery tears make more fiery metal.",
        "&eHow:&r climb the tower. Kill ghastlings near the ghast traps to charge them; charged traps pull the Ur-Ghast down so you can strike.",
        "&eTip:&r carminite from the tower makes redstone gadgets of the twilight."]),

    # ============================ the snowy branch (off the Lich; x=2..10, y=10..14) ============================
    Q("tf_yeti_cave", 4, 10, [structure(TF + "yeti_cave"), kill(TF + "alpha_yeti")], "The Yeti Cave", deps=["w_urghast"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: a cave in the snowy forest", desc=[
        "&eWhat:&r the Alpha Yeti rules a cave in the snowy forest, surrounded by its smaller yetis.",
        "&eChemistry:&r cold kills by pulling heat out of you; still air is a poor conductor of heat, which is why fur and down keep you warm.",
        "&eHow:&r the snowy forest's frost lifts after the Lich. Find the cave and fight inside.",
        "&eTip:&r when it roars, icicles fall from the roof; keep moving."]),
    Q("tf_arctic", 2, 12, [item(TF + "arctic_fur", 4), item(TF + "arctic_helmet"), item(TF + "arctic_chestplate"), item(TF + "arctic_leggings"),
                       item(TF + "arctic_boots")],
      "Arctic Armour", optional=True, deps=["w_yeti"], xp=200, mirror="2A0B3C91D72E8B75", subtitle="Dyeable armour from yeti fur", desc=[
        "&eWhat:&r ordinary yetis drop arctic fur, which makes light, warm armour you can dye.",
        "&eChemistry:&r fur traps a layer of still air, and air conducts heat about a thousand times worse than ice-cold water does.",
        "&eHow:&r kill yetis in the snowy forest for fur, then make all four pieces in the usual shapes (check JEI). Keep 4 spare fur."]),
    Q("w_yeti", 4, 12, [item("twilightforest:alpha_yeti_trophy")], "The Alpha Yeti", deps=["w_urghast"], xp=300,
      mirror="31BB7EB95CE73C1A", subtitle="The snowy forest's boss", desc=[
        "&eWhat:&r the Alpha Yeti lives in a cave in the snowy forest. It drops its trophy, alpha yeti fur and ice bombs.",
        "&eHow:&r dodge the ice it throws and the icicles that fall from the cave roof.",
        "&eTip:&r the snowy forest opens after the Lich, so you can fight it early; carrying alpha yeti fur lets you bear the glacier's cold."]),
    Q("tf_alpha_fur", 0, 0, [item(TF + "alpha_yeti_fur", 8)], "Alpha Yeti Fur", deps=["w_yeti"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the pelt of the snowy forest's boss", desc=[
        "&eWhat:&r the Alpha Yeti's thick white fur, the material of yeti armour.",
        "&eChemistry:&r hair and fur are keratin, a protein whose chains are cross-linked by disulfide (S–S) bonds from the amino acid cysteine; that's what makes it tough and water-shedding.",
        "&eHow:&r the Alpha Yeti drops it when it dies. Other yeti caves have other Alpha Yetis if you need more.",
        "&eTip:&r a full yeti set takes a lot of fur; keep a piece in your pack for the glacier's cold."]),
    Q("tf_yeti_armor", 4, 14, [item(TF + "yeti_helmet"), item(TF + "yeti_chestplate"), item(TF + "yeti_leggings"), item(TF + "yeti_boots")],
      "Yeti Armour", optional=True, deps=["w_yeti"], xp=250, mirror="3C8724C3A9459507", subtitle="The Alpha Yeti's coat", desc=[
        "&eWhat:&r armour of alpha yeti fur; every piece is crafted with Protection II already on it.",
        "&eHow:&r alpha yeti fur in the usual armour shapes (check JEI).",
        "&eTip:&r the Alpha Yeti's ice bombs freeze the ground where they land; throw them at a crowd."]),
    Q("tf_aurora", 8, 10, [structure(TF + "aurora_palace"), kill(TF + "snow_queen")], "The Aurora Palace", deps=["w_yeti"], xp=300,
      optional=True, tokens=1, loot="boss", subtitle="Optional: an ice palace on the glacier", desc=[
        "&eWhat:&r the Snow Queen's palace of packed ice and aurora blocks stands on the glacier.",
        "&eChemistry:&r real auroras are light from oxygen (green, red) and nitrogen (blue, purple) atoms excited by charged particles from the Sun.",
        "&eHow:&r the glacier opens after the Alpha Yeti. Climb the palace to the Queen's throne room.",
        "&eTip:&r break her ice shields first; she falls on you from above, so look up."]),
    Q("tf_ice_weapons", 10, 10, [item(TF + "ice_sword")], "Ice Sword", deps=["tf_arrive"], xp=150,
      mirror="78CE2ECEF0B651DA", section="Forest Treasures", subtitle="A blade that slows what it cuts", desc=[
        "&eWhat:&r a sword of enchanted ice that slows whatever it hits.",
        "&eHow:&r a treasure from the Aurora Palace's chests (and other forest caches); check every room on the way up.",
        "&eTip:&r slowed enemies can't chase; use it to kite anything fast."]),
    Q("tf_ice_bow", 0, 0, [item(TF + "ice_bow")], "Ice Bow", deps=["tf_arrive"], xp=150, mirror="49EE6D2A3684A510",
      section="Forest Treasures", subtitle="Arrows that chill", desc=[
        "&eWhat:&r a bow whose arrows slow whatever they hit.",
        "&eChemistry:&r cold slows everything down, chemistry included: a common rule of thumb is that many reaction rates roughly halve for every 10 °C drop.",
        "&eHow:&r a treasure from the Aurora Palace and other forest chests.",
        "&eTip:&r slow the Snow Queen's guardians before they reach you."]),
    Q("tf_ender_bow", 0, 0, [item(TF + "ender_bow")], "Ender Bow", deps=["tf_arrive"], xp=150, mirror="3D29EF7F150F5334",
      section="Forest Treasures", subtitle="Swap places with what you shoot", desc=[
        "&eWhat:&r a bow whose arrows swap you with the mob they hit.",
        "&eHow:&r a treasure from forest chests (the Aurora Palace and hollow hills among them).",
        "&eTip:&r an escape tool: shoot a mob far away and trade places with it."]),
    Q("tf_glass_sword", 0, 0, [item(TF + "glass_sword")], "One Hit Wonder", deps=["tf_arrive"], xp=150,
      mirror="38ADDF7FF4E4892D", section="Forest Treasures", subtitle="A blade that shatters on first use", desc=[
        "&eWhat:&r an enchanted Glass Sword from the Aurora Palace's room chests. It hits very hard, then breaks after a single hit.",
        "&eChemistry:&r glass is amorphous SiO₂: with no crystal grains to stop it, one crack runs straight through. Toughened glass is quenched so its surface is squeezed, and cracks have to fight that first.",
        "&eHow:&r loot the palace rooms on your way up to the Queen. It's a rare find; check every chest.",
        "&eTip:&r save it for one blow that matters, like the last hit on a boss."]),
    Q("w_snow_queen", 8, 12, [item("twilightforest:snow_queen_trophy")], "The Snow Queen", deps=["w_yeti"], xp=400,
      mirror="6FD41DF7704466A4", subtitle="The glacier's ice palace", desc=[
        "&eWhat:&r the Snow Queen rules the Aurora Palace on the glacier.",
        "&eHow:&r climb the palace, then break her ice shields and avoid her drop attacks.",
        "&eTip:&r beating her finishes the snowy branch of the twilight."]),
    Q("tf_queen_bows", 8, 14, [item(TF + "triple_bow")], "Tri-Bow", deps=["w_snow_queen"], xp=200,
      mirror="53A79338994088FD", subtitle="Three arrows at once", desc=[
        "&eWhat:&r the Tri-Bow fires three arrows in a spread with every shot.",
        "&eHow:&r the Snow Queen drops one of her two bows with her trophy; beat another Queen if you got the Seeker Bow.",
        "&eTip:&r a spread shot is made for crowds: point it at a swarm and loose."]),
    Q("tf_seeker_bow", 0, 0, [item(TF + "seeker_bow")], "Seeker Bow", deps=["w_snow_queen"], xp=200, mirror="7509E4093010EA4C",
      subtitle="Arrows that find their mark", desc=[
        "&eWhat:&r the Seeker Bow's arrows curve towards the nearest target.",
        "&eHow:&r the Snow Queen drops one of her two bows; fight another Queen if you got the Tri-Bow.",
        "&eTip:&r perfect against fliers like ghastlings that never hold still."]),
    Q("tf_biomes_cold", 6, 14, [biome(TF + "snowy_forest"), biome(TF + "glacier")], "The Frozen Regions", deps=["w_snow_queen"], xp=75,
      optional=True, tokens=1, subtitle="Optional: snowy forest and glacier", desc=[
        "&eWhat:&r the cold half of the forest: the snowy forest and the glacier beyond it.",
        "&eChemistry:&r glacier ice is blue because water absorbs red light weakly; thick, bubble-free ice lets mostly blue through.",
        "&eHow:&r visit both. Warm armour stops the blizzard's chill."]),

    # ============================ the highlands and the end (x=24..33, y=8..10.5) ============================
    Q("tf_highlands", 24, 8, [biome(TF + "highlands"), biome(TF + "thornlands")], "The Highlands", deps=["w_urghast", "w_snow_queen"], xp=300,
      optional=True, tokens=2, subtitle="Optional: the plateau beyond every barrier", desc=[
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
    Q("tf_troll_cave", 27, 8, [item(TF + "lamp_of_cinders")], "The Lamp of Cinders", deps=["tf_giants"], xp=250,
      mirror="5CBA8C89FE717B9C", subtitle="A lamp that burns away the thorns", desc=[
        "&eWhat:&r the Lamp of Cinders, the key to the forest's last region. It sits in a troll cave vault under the highlands.",
        "&eHow:&r find a troll cave in the highlands and loot its vaults. The lamp burns away the thorns that wall off the final plateau.",
        "&eTip:&r trolls throw rocks; fight them in the open, not in narrow tunnels."]),
    Q("tf_thorn_rose", 0, 0, [item(TF + "thorn_rose", 12)], "Thorn Roses", deps=["tf_troll_cave"], xp=150,
      mirror="2951B1D7080C5EF9", subtitle="A dozen flowers from among the thorns", desc=[
        "&eWhat:&r the thornlands' only flower, growing among the thorns. One rose crafts into red dye.",
        "&eChemistry:&r red petals get their colour from anthocyanins, pigments that change colour with pH: red in acid, purple to blue as it rises. Red cabbage juice is the same dye and makes a classroom pH indicator.",
        "&eHow:&r pick twelve at the thornlands' edge; living thorns hurt to touch.",
        "&eTip:&r bring the Lamp of Cinders to clear a safe path first."]),
    Q("tf_castle_doors", 0, 0, [item(TF + "pink_castle_door", 12), item(TF + "yellow_castle_door", 12), item(TF + "blue_castle_door", 12),
                                item(TF + "violet_castle_door", 12)],
      "Rune Doors", optional=True, deps=["tf_thorn_rose"], xp=300, mirror="420158B1736A1354", subtitle="Twelve of each of the castle's coloured doors", desc=[
        "&eWhat:&r the Final Castle's rune doors come in four colours, one for each wing of the castle.",
        "&eHow:&r burn through the thorns with the Lamp of Cinders, climb onto the final plateau and mine the doors out of the castle walls. Twelve of each colour.",
        "&eTip:&r the doors vanish when activated; mine them while they're solid."]),
    Q("tf_uberous", 0, 0, [item(TF + "uberous_soil", 2)], "Uberous Soil", deps=["tf_troll_cave"], xp=100,
      optional=True, tokens=1, subtitle="Optional: soil rich enough for a beanstalk", desc=[
        "&eWhat:&r a glowing, absurdly fertile soil from the trolls' gardens. Magic beans planted on it sprout a beanstalk.",
        "&eChemistry:&r real fertile soil is rich in humus and in the three big plant nutrients, nitrogen, phosphorus and potassium (N-P-K), the same numbers printed on every fertiliser bag.",
        "&eHow:&r loot troll cave gardens; the same caves hold the magic beans.",
        "&eTip:&r a beanstalk is only useful with clouds above it; plant under the cloud layer."]),
    Q("tf_magic_beans", 27, 10.5, [item(TF + "magic_beans"), item(TF + "uberous_soil")], "Magic Beans", deps=["w_snow_queen"], xp=200,
      mirror="58BD1063A19777DC", section="Beyond the Thorns", subtitle="Beans, and soil rich enough to grow them", desc=[
        "&eWhat:&r trolls drop magic beans. Planted on the glowing uberous soil beneath the clouds, they grow a beanstalk straight up.",
        "&eChemistry:&r real beans are legumes: bacteria in their root nodules fix N₂ from the air into ammonia (NH₃), the same job Haber-Bosch does with iron and heat.",
        "&eHow:&r troll caves in the highlands: kill trolls for beans and loot their gardens for uberous soil. Plant a bean on the soil under the clouds."]),
    Q("tf_giants", 30, 10.5, [item(TF + "giant_pickaxe")], "Giant's Pickaxe", deps=["tf_magic_beans"], xp=250,
      mirror="20436AFCC7E6855D", subtitle="A pickaxe the size of a house", desc=[
        "&eWhat:&r the Giant's Pickaxe breaks the oversized blocks of the cloud world in one go.",
        "&eHow:&r climb the beanstalk to the clouds and beat a giant miner, or craft one from giant cobblestone and giant logs (check JEI).",
        "&eTip:&r giant blocks break down into normal ones: one giant log crafts into 64 oak logs."]),
    Q("tf_final_plateau", 30, 8, [biome(TF + "final_plateau")], "The Final Plateau", deps=["tf_troll_cave"], xp=300,
      optional=True, tokens=1, subtitle="Optional: burn through the thorns", desc=[
        "&eWhat:&r the highest ground in the forest, walled in by thorns and acid rain.",
        "&eHow:&r carry the Lamp of Cinders. Use it on the thorns to burn a path through the thornlands, then climb onto the plateau.",
        "&eTip:&r burnt thorns crumble away; don't stand in living ones, they hurt."]),
    Q("tf_final_castle", 33, 8, [structure(TF + "final_castle")], "The Unfinished Castle", deps=["tf_final_plateau"], xp=300,
      optional=True, tokens=2, loot="boss", subtitle="Optional: the castle at the top of the world", desc=[
        "&6A castle on the final plateau, waiting for a ruler. You remember planning to come back for it.&r",
        "&eWhat:&r the Final Castle stands on the final plateau. Its last boss was never finished by the mod's authors, so this is the end of the road.",
        "&eHow:&r cross the plateau and step inside the castle.",
        "&eTip:&r the castle is still worth exploring for its architecture and its force-field doors."]),
    Q("tf_castle_bricks", 36, 8, [item(TF + "castle_brick", 16)], "Castle Stone", deps=["tf_final_castle"], xp=100,
      optional=True, tokens=1, subtitle="Optional: bricks from the last castle", desc=[
        "&eWhat:&r the Final Castle's pale brick, for building your own keep.",
        "&eHow:&r mine castle brick from the castle walls. Its cracked, mossy, worn and pillar variants are in JEI.",
        "&eTip:&r a stonecutter makes the stairs and pillars without waste."]),
], links=[("t5_twilight", -2, 0)], mirror="twilight_forest")
