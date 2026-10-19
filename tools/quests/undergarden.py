"""Quest chapter: undergarden (The Undergarden). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The portal (t4_undergarden) and the first metals/catacombs/biome quests live in t4.py and worlds.py
(w_undergarden, w_regalium, wd_catacombs, w_forgotten, wd_vestige, wd_undergarden_biomes); rotspawn, nargoyle and
muncher hunts are in hunting.py; the eight-biome tour is in completionist.py. This page adds everything else.
Prefix ug_.
Layout: y=0 the main line (arrival -> cloggrum -> forgotten tools -> the Depths -> rogdorium -> infuser -> utherium);
y=2 gear branches; y=-2 / -4 exploration and creatures; y=4 / 6 food and gourds.
Gate facts (from the mod jar): dreadrock needs a Forgotten tool, rogdorium only grows in dreadrock (the Depths), and
utheric clusters only become utherium crystals in the Infuser, which needs rogdorium.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

UG = "undergarden:"

CHAPTER = Chapter("undergarden", "The Undergarden", "undergarden:catalyst",
        ["A forgotten land under the world, opened with acid."], SIDE, [
    # --- the main line (y=0) -------------------------------------------------------------------
    Q("ug_arrival", 0, 0, [item(UG + "depthrock", 32)], "Depthrock", deps=["t4_undergarden"], xp=100,
      subtitle="The bedrock of a world below the world", desc=[
        "&6Acid opened the way, and the dark below remembers you. You were the one who sealed it.&r",
        "&eWhat:&r depthrock is the Undergarden's stone, the way deepslate is the Overworld's. Its ores (cloggrum, froststeel, utherium, regalium) all sit in it or in icy shiverstone.",
        "&eChemistry:&r dissolve depthrock in the Alchemistry Dissolver and it gives silicon dioxide (SiO₂), iron and aluminium, with rare traces of zirconium, gallium, dysprosium and tungsten.",
        "&eHow:&r the catalyst is copper ingots, stone, an ender pearl and a bucket of MI sulfuric acid (this pack's recipe). Light the stone-brick frame and step through, then mine.",
        "&eTip:&r the Undergarden has no sun. Bring a stack of torches and mark your portal."]),
    Q("ug_cloggrum_tools", 2, 0, [item(UG + "cloggrum_pickaxe"), item(UG + "cloggrum_sword")], "Cloggrum Tools", deps=["ug_arrival"], xp=100,
      subtitle="The Undergarden's everyday metal", desc=[
        "&eWhat:&r cloggrum is the first Undergarden metal: about as good as iron, and the base for every Forgotten tool later.",
        "&eHow:&r mine cloggrum ore (stone pickaxe or better), smelt the raw cloggrum, and craft tools as you would iron ones.",
        "&eTip:&r keep the cloggrum sword and pickaxe once you replace them: they're what the Forgotten template upgrades."]),
    Q("ug_cloggrum_armor", 4, 0, [item(UG + "cloggrum_helmet"), item(UG + "cloggrum_chestplate"), item(UG + "cloggrum_leggings"), item(UG + "cloggrum_boots")],
      "Cloggrum Armour", deps=["ug_cloggrum_tools"], xp=150, subtitle="A full suit for the dark", desc=[
        "&eWhat:&r a full set of cloggrum armour. The boots have a perk: scintling goo no longer slows you.",
        "&eHow:&r 24 cloggrum ingots for the set. Raw cloggrum also turns up in depleted mines.",
        "&eTip:&r scintlings leave sticky goo trails across whole caverns; the boots pay for themselves fast."]),
    Q("ug_forgotten_tools", 6, 0, [item(UG + "forgotten_pickaxe"), item(UG + "forgotten_sword")], "Forgotten Tools", deps=["ug_cloggrum_armor"], xp=250,
      subtitle="Upgrade cloggrum with the guardian's metal", desc=[
        "&eWhat:&r Forgotten tools mine Undergarden blocks 1.5x as fast, Forgotten weapons hit non-boss Undergarden mobs 1.5x as hard. Only a Forgotten pickaxe can break dreadrock.",
        "&eHow:&r smithing table: Forgotten upgrade template + cloggrum tool + Forgotten Ingot. Ingots come from the Forgotten Guardian in the catacombs (see the Other Worlds page); templates from catacomb chests.",
        "&eTip:&r copy a template with 7 diamonds and a block of depthrock (makes 2). Do it before you use your last one."]),
    Q("ug_depths", 8, 0, [biome(UG + "depths")], "The Depths", deps=["ug_forgotten_tools"], xp=300, size=1.5, shape="hexagon",
      subtitle="Break the dreadrock floor", desc=[
        "&6Under the forgotten land there is an older one. You remember the floor you laid over it.&r",
        "&eWhat:&r a layer of dreadrock seals the bottom of the Undergarden. Below it lie the Depths: infected caverns, puff mushroom forests and rogdorium groves.",
        "&eHow:&r dig down until you hit dreadrock, then break through it with a Forgotten pickaxe. Nothing else can mine it.",
        "&eTip:&r the Depths carry the Utheric Infection. Read the rogdorium quest before you stay long."]),
    Q("ug_rogdorium", 10, 0, [item(UG + "rogdorium", 8)], "Rogdorium", deps=["ug_depths"], xp=200,
      subtitle="The antidote grows in dreadrock", desc=[
        "&eWhat:&r rogdorium is a crystal found only in dreadrock. It's the key to the Infuser, and eating it holds back the Utheric Infection.",
        "&eChemistry:&r real poisoning by heavy metals is treated much the same way: a chelating agent such as EDTA binds the toxic metal ions so the body can flush them out.",
        "&eHow:&r mine dreadrock rogdorium ore with a Forgotten pickaxe (it drops rogdorium) or smelt the ore block.",
        "&eTip:&r carry a few rogdorium nuggets on every trip down; eat one when the infection meter climbs."]),
    Q("ug_infuser", 12, 0, [item(UG + "infuser")], "The Infuser", deps=["ug_rogdorium"], xp=200,
      subtitle="Purify or corrupt what you put in", desc=[
        "&eWhat:&r the Undergarden's own processing block. With rogdorium fuel it purifies; with utherium it corrupts.",
        "&eChemistry:&r the idea is old: purification is often just a reaction that removes one impurity, the way a blast furnace strips oxygen from iron ore.",
        "&eHow:&r an utheric cluster, rogdorium and five dreadrock (check JEI). It also gives armour a Rogdorium Infusion.",
        "&eTip:&r JEI's Infusing category lists every conversion, including which fuel slot it needs."]),
    Q("ug_utherium", 14, 0, [item(UG + "utherium_crystal", 4)], "Purified Utherium", deps=["ug_infuser"], xp=200,
      subtitle="Turn utheric clusters into crystal", desc=[
        "&eWhat:&r utherium crystal is the Undergarden's weapon against rotspawn. Mined utherium ore only gives raw utheric clusters.",
        "&eHow:&r mine or smelt utherium ore for clusters (9 utheric shards also make one), then purify each cluster in the Infuser with rogdorium.",
        "&eTip:&r rotbeasts and rotbelchers drop utheric shards, so hunting them feeds the line."]),
    Q("ug_utherium_gear", 16, 0, [item(UG + "utherium_sword"), item(UG + "utherium_chestplate")], "Utherium Gear", deps=["ug_utherium"], xp=300,
      size=1.5, shape="gear", subtitle="Bane of the rotspawn", desc=[
        "&6Rot fears what is pure. You remember forging blades for exactly this.&r",
        "&eWhat:&r utherium weapons deal 1.5x damage to rotspawn; the armour is the Undergarden's best plain set.",
        "&eHow:&r craft them from utherium crystals like diamond gear (check JEI).",
        "&eTip:&r a worn-out utherium tool smelts back into a crystal, so nothing is wasted."]),

    # --- gear branches (y=2) -------------------------------------------------------------------
    Q("ug_slingshot", 2, 2, [item(UG + "slingshot"), item(UG + "depthrock_pebble", 16)], "Slingshot", deps=["ug_arrival"], xp=75,
      subtitle="Wigglewood, pebbles and patience", desc=[
        "&eWhat:&r a ranged weapon that fires pebbles, goo balls, gronglets or rotten blisterberries.",
        "&eHow:&r twistytwigs (two wigglewood planks make four) and sticks. Pebbles drop from mogs and stoneborn, or stonecut depthrock.",
        "&eTip:&r it takes its own enchantments: Ricochet bounces shots off walls, Self Sling launches you instead."]),
    Q("ug_froststeel", 4, 2, [item(UG + "froststeel_sword"), item(UG + "froststeel_chestplate")], "Froststeel", deps=["ug_cloggrum_tools"], xp=150,
      subtitle="A metal that bites with cold", desc=[
        "&eWhat:&r froststeel weapons give targets the Chilly effect, which slows them.",
        "&eChemistry:&r real steel gets brittle in deep cold: below its ductile-to-brittle transition temperature it cracks instead of bending, which is why ships' hulls once split in icy seas.",
        "&eHow:&r froststeel ore only forms in shiverstone, in the frozen biomes. It needs an iron pickaxe; smelt the raw froststeel.",
        "&eTip:&r a froststeel sword is great against fast rotspawn; slowed foes can't close the gap."]),
    Q("ug_battleaxe", 6, 2, [kill(UG + "forgotten", 5), item(UG + "cloggrum_battleaxe")], "The Forgotten", deps=["ug_cloggrum_armor"], xp=200,
      subtitle="Take a battleaxe from cold dead hands", desc=[
        "&eWhat:&r the Forgotten are armoured undead that guard the catacombs and vestiges. Some carry a cloggrum battleaxe.",
        "&eHow:&r kill five Forgotten. The battleaxe can't be crafted: it only drops from a Forgotten carrying one.",
        "&eTip:&r they hit hard but slowly. Shield up, then strike."]),
    Q("ug_forgotten_battleaxe", 8, 2, [item(UG + "forgotten_battleaxe")], "Forgotten Battleaxe", deps=["ug_battleaxe", "ug_forgotten_tools"], xp=200,
      optional=True, tokens=2, subtitle="Optional: the heaviest weapon below", desc=[
        "&eWhat:&r the cloggrum battleaxe, upgraded with Forgotten metal.",
        "&eHow:&r smithing table: Forgotten upgrade template + cloggrum battleaxe + Forgotten Ingot.",
        "&eTip:&r make all six Forgotten tools if you want the mod's own completion advancement."]),
    Q("ug_spear", 10, 2, [item(UG + "spear")], "Rogdorium Spear", deps=["ug_rogdorium"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a throwable point of antidote", desc=[
        "&eWhat:&r a spear you can stab with or throw, like a trident without the water.",
        "&eHow:&r one rogdorium on top of two sticks.",
        "&eTip:&r retrieve it after every throw; it doesn't come back on its own."]),
    Q("ug_gronglets", 12, 2, [item(UG + "rogdoric_gronglet"), item(UG + "utheric_gronglet")], "Two Kinds of Gronglet", deps=["ug_infuser"], xp=100,
      optional=True, tokens=1, subtitle="Optional: purify one, corrupt one", desc=[
        "&eWhat:&r gronglets are little glowing growths. The Infuser can purify one with rogdorium or corrupt one with utherium.",
        "&eHow:&r collect two wild gronglets, then run one through each Infuser mode (JEI shows both).",
        "&eTip:&r gronglets also work as slingshot ammo. The mod asks if that is okay."]),
    Q("ug_collector", 16, 2, [item(UG + "cloggrum_block"), item(UG + "froststeel_block"), item(UG + "utherium_block"), item(UG + "regalium_block"),
                               item(UG + "rogdorium_block"), item(UG + "forgotten_block")],
      "Collector's Shelf", deps=["ug_utherium_gear"], xp=300, optional=True, tokens=2, loot="boss",
      subtitle="Optional: a block of every Undergarden metal", desc=[
        "&eWhat:&r one storage block each of cloggrum, froststeel, utherium, regalium, rogdorium and Forgotten metal.",
        "&eChemistry:&r feed spares to the Dissolver: the Undergarden's metals are fiction, but what they break down into tells you what the pack thinks they are made of.",
        "&eHow:&r nine of each ingot or crystal in a crafting grid.",
        "&eTip:&r a Forgotten block and a carved gloomgourd summon a Forgotten Minion."]),

    # --- exploration (y=-2) --------------------------------------------------------------------
    Q("ug_woods", 0, -2, [item(UG + "smogstem_log", 8), item(UG + "wigglewood_log", 8), item(UG + "grongle_log", 8)], "Woods Without Sun",
      deps=["ug_arrival"], xp=75, optional=True, tokens=1, subtitle="Optional: smogstem, wigglewood, grongle", desc=[
        "&eWhat:&r three kinds of tree that grow with no daylight at all.",
        "&eChemistry:&r real plants can't do that: photosynthesis (6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂) needs light. Underground life runs on chemosynthesis or on food that falls from above.",
        "&eHow:&r smogstem forests, wigglewood forests and the gronglegrowth each have their own tree.",
        "&eTip:&r wigglewood planks make the twistytwigs for the slingshot."]),
    Q("ug_shard_torch", 2, -2, [item(UG + "shard_torch", 8)], "Shard Torches", deps=["ug_arrival"], xp=75,
      subtitle="Light that burns rotspawn", desc=[
        "&eWhat:&r a torch tipped with an utheric shard. It lights the dark and hurts rotspawn that come close.",
        "&eHow:&r one utheric shard on a stick. Shards drop from rotbeasts and rotbelchers and sit in catacomb chests.",
        "&eTip:&r ring your portal and your base with them."]),
    Q("ug_depleted_mine", 4, -2, [structure(UG + "depleted_mine")], "A Depleted Mine", deps=["ug_arrival"], xp=100,
      optional=True, tokens=1, subtitle="Optional: someone mined here before you", desc=[
        "&eWhat:&r old mines left by the Undergarden's builders. The chests still hold raw cloggrum, raw froststeel and cloggrum tools.",
        "&eHow:&r explore depthrock caverns until you find timber supports and rails; step inside.",
        "&eTip:&r a quick way to an early cloggrum pickaxe."]),
    Q("ug_bogs", 6, -2, [biome(UG + "blood_mushroom_bog"), biome(UG + "ink_mushroom_bog"), biome(UG + "veil_mushroom_bog")], "Mushroom Bogs",
      deps=["ug_arrival"], xp=100, optional=True, tokens=1, subtitle="Optional: blood, ink and veil", desc=[
        "&eWhat:&r three bogs named after the giant mushrooms that grow in them. Each mushroom makes its own stew and dye.",
        "&eChemistry:&r a fungus is closer to an animal than a plant: its cell walls are chitin, (C₈H₁₃O₅N)ₙ, the same polymer as insect shells.",
        "&eHow:&r Nature's Compass works down here. Visit all three."]),
    Q("ug_depths_biomes", 8, -2, [biome(UG + "infected_depths"), biome(UG + "puff_mushroom_forest"), biome(UG + "rogdorium_grove")], "Into the Depths",
      deps=["ug_depths"], xp=150, optional=True, tokens=1, subtitle="Optional: three regions under the dreadrock", desc=[
        "&eWhat:&r the rest of the Depths: the infected depths, the puff mushroom forest and the rogdorium grove.",
        "&eHow:&r with a Forgotten pickaxe, tunnel through dreadrock to each one.",
        "&eTip:&r the rogdorium grove is the richest place for rogdorium; carry plenty out."]),

    # --- creatures (y=-4) ----------------------------------------------------------------------
    Q("ug_rotbelcher", 0, -4, [kill(UG + "rotbelcher", 3), item(UG + "utheric_shard", 8)], "The Rotbelcher", deps=["ug_arrival"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: the rotspawn that spits", desc=[
        "&eWhat:&r a bloated rotspawn that hurls rot from a distance. Like rotbeasts, it drops utheric shards.",
        "&eHow:&r close the distance fast, or fight it with a bow or slingshot from cover.",
        "&eTip:&r a shard torch nearby softens it up while you fight."]),
    Q("ug_brute", 2, -4, [kill(UG + "brute", 3), item(UG + "brute_tusk", 2)], "Brutes", deps=["ug_arrival"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: tusks for bone meal", desc=[
        "&eWhat:&r brutes are tusked beasts that leave you alone until you hit them. Their tusks grind into bone meal.",
        "&eChemistry:&r tusks, teeth and bone are mostly hydroxyapatite, Ca₅(PO₄)₃OH, which is why bone meal feeds plants phosphorus.",
        "&eHow:&r one brute tusk crafts into four bone meal."]),
    Q("ug_denizen", 4, -4, [kill(UG + "denizen", 5), item(UG + "denizen_mask")], "The Denizens", deps=["ug_arrival"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: the Undergarden's current tenants", desc=[
        "&eWhat:&r Denizens live in camps around campfires. They drop mysterious masks, and their camp chests hold more.",
        "&eHow:&r find a denizen camp (see the Other Worlds page) and fight. Breaking their campfire angers the whole camp.",
        "&eTip:&r draw them out one at a time."]),
    Q("ug_scintling", 6, -4, [kill(UG + "scintling")], "You Monster", deps=["ug_arrival"], xp=50,
      secret=True, loot="secret", subtitle="Secret: it was just a snail", desc=[
        "&eWhat:&r you killed a scintling, a harmless glowing snail. It dropped a goo ball.",
        "&eChemistry:&r real snail slime is a mix of glycoproteins and water that thickens under stress, letting the snail glue itself to walls.",
        "&eTip:&r goo balls make sticky pistons, so at least it wasn't for nothing."]),
    Q("ug_minion", 8, -4, [kill(UG + "forgotten_guardian"), item(UG + "forgotten_block")], "A Minion of Your Own", deps=["ug_forgotten_tools"], xp=200,
      optional=True, tokens=1, subtitle="Optional: build what the guardian was", desc=[
        "&eWhat:&r stack a carved gloomgourd on a block of Forgotten metal and it wakes as a Forgotten Minion that fights for you.",
        "&eHow:&r a block of Forgotten metal is nine Forgotten Ingots, so beat the guardian until you have enough nuggets.",
        "&eTip:&r the mod has an advancement for building one; the minion fires at your enemies."]),
    Q("ug_secret_disc", 10, -4, [item(UG + "music_disc_gloomper_secret")], "The Gloomper's Secret", deps=["ug_arrival"], xp=150,
      secret=True, loot="secret", subtitle="Secret: a disc the gloompers kept quiet", desc=[
        "&6Even down here someone wrote music. You remember humming it.&r",
        "&eWhat:&r a hidden music disc from the Undergarden. The mod counts finding it as a challenge.",
        "&eTip:&r the Undergarden has four more discs; play them on a jukebox."]),

    # --- food and gourds (y=4, y=6) ------------------------------------------------------------
    Q("ug_underbeans", 0, 4, [item(UG + "roasted_underbeans", 8)], "Roasted Underbeans", deps=["ug_arrival"], xp=50,
      subtitle="The first meal below", desc=[
        "&eWhat:&r underbean bushes grow in the forests. The beans are edible raw, much better roasted.",
        "&eChemistry:&r roasting browns food by the Maillard reaction: amino acids and sugars combine into hundreds of new flavour molecules above about 140 °C.",
        "&eHow:&r pick a bush, then smelt or campfire-cook the beans.",
        "&eTip:&r underbeans on a stick steer a dweller you're riding."]),
    Q("ug_blisterbomb", 2, 4, [item(UG + "blisterbomb", 4)], "Blisterbombs", deps=["ug_slingshot"], xp=75,
      optional=True, tokens=1, subtitle="Optional: rotten berries, thrown hard", desc=[
        "&eWhat:&r a throwable bomb of rotten blisterberries that bursts into a harmful cloud.",
        "&eChemistry:&r real rotting fruit ferments: yeast turns its sugar into ethanol and carbon dioxide (C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂), and sealed fruit can split from the gas.",
        "&eHow:&r a twistytwig over six rotten blisterberries (blisterberry bushes drop both kinds).",
        "&eTip:&r eight around a gloomgourd make a boomgourd: an explosive block."]),
    Q("ug_meat", 4, 4, [item(UG + "dweller_steak", 4), item(UG + "gloomper_leg", 4)], "Hunter's Supper", deps=["ug_arrival"], xp=75,
      subtitle="Dweller steak and gloomper leg", desc=[
        "&eWhat:&r the best meats below: dwellers (big rideable grazers) and gloompers (hopping toads) both drop meat and leather.",
        "&eChemistry:&r heat denatures meat proteins: the coiled chains unfold and bond to each other, which is why meat firms up as it cooks.",
        "&eHow:&r cook the raw meat in a furnace, smoker or campfire."]),
    Q("ug_gloomgourd", 6, 4, [item(UG + "gloomgourd", 8), item(UG + "gloomgourd_seeds", 4)], "Gloomgourds", deps=["ug_arrival"], xp=75,
      subtitle="The Undergarden's pumpkin", desc=[
        "&eWhat:&r a dark gourd that grows like a pumpkin. Carve it for lanterns and minions, or bake it into pie.",
        "&eHow:&r find wild gloomgourds; one gourd crafts into four seeds. Plant them on deepsoil farmland.",
        "&eTip:&r a carved gloomgourd over a torch makes a gloom-o-lantern; over a shard torch, a shard-o-lantern."]),
    Q("ug_stews", 2, 6, [item(UG + "bloody_stew"), item(UG + "indigo_stew"), item(UG + "inky_stew"), item(UG + "veiled_stew")], "Four Stews",
      deps=["ug_underbeans"], xp=100, optional=True, tokens=1, subtitle="Optional: a stew from every giant mushroom", desc=[
        "&eWhat:&r each giant mushroom (blood, indigo, ink and veil) cooks into its own stew.",
        "&eChemistry:&r the Dissolver breaks Undergarden mushrooms into chitin and phosphoric acid (H₃PO₄); phosphate is how cells store energy, as ATP.",
        "&eHow:&r a bowl and the mushrooms (check JEI); the mushroom bogs have all four kinds nearby."]),
    Q("ug_gwibling", 4, 6, [item(UG + "gwibling_bucket"), item(UG + "cooked_gwibling", 4)], "Weird Fish", deps=["ug_meat"], xp=75,
      optional=True, tokens=1, subtitle="Optional: catch a gwibling, cook a few more", desc=[
        "&eWhat:&r gwiblings are the small fish of the Undergarden seas. Catch one live, or cook them.",
        "&eHow:&r use a water bucket on a gwibling to catch it; kill others for raw gwibling and smelt it.",
        "&eTip:&r the full-grown gwib is not a friendly fish. Watch the water."]),
    Q("ug_pie", 6, 6, [item(UG + "gloomgourd_pie", 2)], "Gloomgourd Pie", deps=["ug_gloomgourd"], xp=75,
      optional=True, tokens=1, subtitle="Optional: gourd, mushroom and glitterkelp", desc=[
        "&eWhat:&r the Undergarden's best plain food.",
        "&eHow:&r a gloomgourd, any Undergarden mushroom and a glitterkelp from the seas, shapeless.",
        "&eTip:&r glitterkelp also smelts into ordinary dried kelp."]),
], links=[("t4_undergarden", -2, 0), ("w_undergarden", -2, -2)])
