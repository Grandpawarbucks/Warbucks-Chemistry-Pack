"""Quest chapter: undergarden (The Undergarden). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's Undergarden chapter quest for quest (its list, order, sections and requirements only; ATM10's book is
All Rights Reserved, so every word here is our own). Each mirrored quest carries mirror="<ATM10 quest id>".
The portal is opened in t4 (t4_undergarden). The Undergarden quests that used to sit on the Other Worlds page
(w_undergarden, w_regalium, wd_catacombs, w_forgotten, wd_vestige, wd_undergarden_biomes) live here now, keys unchanged.
The bigger rotspawn / nargoyle / muncher hunts stay on the Bounty Board (hunting.py); the biome tour is in completionist.py.
New quests use the prefix ug_. Our own quests that ATM10 doesn't have are optional side quests.
Gate facts (from the mod jar): dreadrock needs a Forgotten tool, rogdorium only grows in dreadrock (the Depths), and
utheric clusters only become utherium crystals in the Infuser, which needs rogdorium.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

UG = "undergarden:"

# --- the creatures (ATM10's middle row: one kill each) ---------------------------------------------------------
_KILLS = [
    # key, entity, ATM10 id, title, subtitle, what, how, tip
    ("ug_k_rotling", "rotling", "24D38DA8E86DD897", "Rotling", "The smallest rotspawn",
     "rotlings are the small, quick rotspawn: the infection's first wave.",
     "they gather in the dark caverns. Light an area and they come to you.",
     "utherium weapons deal extra damage to every rotspawn."),
    ("ug_k_rotwalker", "rotwalker", "380D3212D1CBA593", "Rotwalker", "Tall, slow and rotten",
     "rotwalkers are the tall rotspawn: slower than rotlings, much tougher.",
     "they wander the caverns in the dark. Fight in the open.",
     "a shard torch nearby softens them up."),
    ("ug_k_rotbeast", "rotbeast", "70FD8856BFCD9AEE", "Rotbeast", "The biggest of the rotspawn",
     "the rotbeast is the heaviest rotspawn, with a lot of health and a hard hit. It drops utheric shards.",
     "find one in the deeper caverns and fight it where you have room to back off.",
     "its shards make shard torches, which hurt its kin."),
    ("ug_k_muncher", "muncher", "5D229FA3A5F92954", "Muncher", "Something with teeth",
     "munchers are one of the Undergarden's hostile hunters.",
     "you'll meet them in the caverns soon enough. Check JEI for what they drop.",
     "keep your armour up when you explore new caverns."),
    ("ug_k_stoneborn", "stoneborn", "4D836B9D9E3B898F", "Stoneborn", "People made of rock",
     "stoneborn are the stony folk of the Undergarden. They drop depthrock pebbles, among other things.",
     "find one in the caverns and bring it down. Check JEI for its drops.",
     "pebbles are slingshot ammo."),
    ("ug_k_gloomper", "gloomper", "79C652E3FCB88550", "Gloomper", "A hopping toad",
     "gloompers are hopping toads, one of the Undergarden's game animals. They drop meat and leather.",
     "hunt them in the forests and fields.",
     "they hop away fast; a slingshot or bow helps."),
    ("ug_k_nargoyle", "nargoyle", "0A1D6E233C0ECC8E", "Nargoyle", "A predator in the dark",
     "nargoyles are among the Undergarden's nastier predators.",
     "they turn up as you explore. Fight with your back to a wall.",
     "the Bounty Board has a bigger hunt for nargoyles and munchers."),
    ("ug_k_sploogie", "sploogie", "67A2347534269528", "Sploogie", "A strange little creature",
     "sploogies are one of the odder creatures of the Undergarden's caverns.",
     "find one and bring it down. Check JEI for what it drops.",
     "every creature down here is worth a look in JEI's mob drops."),
    ("ug_k_gwibling", "gwibling", "53FDC6C536E50A1A", "Gwibling", "The small fish of the seas",
     "gwiblings are the little fish of the Undergarden's seas, and they cook into a decent meal.",
     "find one in an Undergarden sea and catch it with a weapon (or a bucket, for a live one).",
     "the full-grown gwib in the same waters is not friendly."),
    ("ug_k_gwib", "gwib", "71E1454990DEC451", "Gwib", "The big fish bites back",
     "the gwib is the gwibling all grown up: a hostile fish that goes after swimmers.",
     "fight it from the shore, or from a block above the water.",
     "Respiration and Depth Strider help if you must fight in the water."),
    ("ug_k_mog", "mog", "744DBE831C120B2F", "Mog", "A mossy burrower",
     "mogs are mossy burrowers. They drop mogmoss and depthrock pebbles.",
     "find them digging in the depthrock forests.",
     "mogmoss makes rugs and slop bowls."),
    ("ug_k_smog_mog", "smog_mog", "2E596B5A4EA2ABF4", "Smog Mog", "A mog of the smog spires",
     "smog mogs are the mogs of the smog spires. They drop blue mogmoss.",
     "visit the smog spires and find one.",
     "you need the smog spires for the biome quest anyway."),
    ("ug_k_dweller", "dweller", "17C2C8F64B4AE6EE", "Dweller", "A big grazer you can ride",
     "dwellers are big rideable grazers. They drop meat and leather.",
     "hunt them in the forests and fields; an underbean on a stick steers one you ride.",
     "keep one alive and saddled for long cavern trips."),
    ("ug_k_greater_dweller", "greater_dweller", "1A23BBF444D17A63", "Greater Dweller", "The dweller's bigger cousin",
     "the greater dweller is a much bigger relative of the dweller.",
     "it lives in the Undergarden's open caverns. Check JEI for what it drops.",
     "bring a bow: it has plenty of health."),
    ("ug_k_mysterious_pot", "mysterious_pot", "57545837046F552B", "A Pot That Moves", "Not every pot is a pot",
     "some of the pots in a forgotten vestige are creatures pretending to be pots.",
     "break pots in a vestige until one fights back, then finish it.",
     "keep your sword out while you loot the ruins."),
]

# --- the biomes (ATM10's top-left block: one biome each) --------------------------------------------------------
_BIOMES = [
    # key, biome, ATM10 id, title, what, chemistry line or None
    ("ug_bi_gronglegrowth", "gronglegrowth", "647A87E800C703C3", "Gronglegrowth",
     "a forest of grongle trees, hung with glowing gronglets.", None),
    ("ug_bi_ancient_sea", "ancient_sea", "353AEEC116A5DEEF", "Ancient Sea",
     "a dark sea under the world, home to gwiblings, gwibs and glitterkelp.",
     "with no sunlight nothing here can photosynthesise; real deep-sea vents feed whole ecosystems by chemosynthesis, with microbes oxidising H₂S for energy."),
    ("ug_bi_wigglewood", "wigglewood_forest", "050D8480EE9D8E62", "Wigglewood Forest",
     "a forest of twisting wigglewood, the wood your slingshot is made from.", None),
    ("ug_bi_ink_bog", "ink_mushroom_bog", "278D34BBC13356DF", "Ink Mushroom Bog",
     "a bog grown over with giant ink mushrooms.", None),
    ("ug_bi_veil_bog", "veil_mushroom_bog", "7E3DA4168D352B42", "Veil Mushroom Bog",
     "a bog grown over with giant veil mushrooms.", None),
    ("ug_bi_indigo_bog", "indigo_mushroom_bog", "0A0A991BAC99092C", "Indigo Mushroom Bog",
     "a bog grown over with giant indigo mushrooms.",
     "real indigo dye is indigotin, C₁₆H₁₀N₂O₂; it only dissolves after it's chemically reduced, then turns blue again as air oxidises it on the cloth."),
    ("ug_bi_barren_abyss", "barren_abyss", "36389696767EFB4E", "Barren Abyss",
     "a bare, open chasm with little growing in it.", None),
    ("ug_bi_dead_sea", "dead_sea", "1BAE1519E44E40CE", "Dead Sea",
     "a still, lifeless body of water.",
     "the real Dead Sea is about a third salt, rich in magnesium and sodium chlorides: dense enough to float in, too salty for fish."),
    ("ug_bi_dense_forest", "dense_forest", "15A8F04BC10E619E", "Dense Forest",
     "the thickest forest below, packed tight with trees.", None),
    ("ug_bi_frostfields", "frostfields", "1E13D7CE5A9EFF74", "Frostfields",
     "frozen fields of shiverstone, where froststeel ore forms.",
     "water expands by about 9% as it freezes, which is why ice floats and frost splits rock."),
    ("ug_bi_frosty_smogstem", "frosty_smogstem_forest", "0C98503A2F20484D", "Frosty Smogstem Forest",
     "a smogstem forest gone cold and white.", None),
    ("ug_bi_icy_sea", "icy_sea", "073BA8470EA37A00", "Icy Sea",
     "a frozen sea in the Undergarden's cold corner.", None),
    ("ug_bi_smog_spires", "smog_spires", "511144EF336BFAF5", "Smog Spires",
     "tall spires that belch smog, home of the smog mogs.",
     "real industrial smog is soot plus sulfur dioxide (SO₂), which forms sulfuric acid droplets in damp air."),
    ("ug_bi_smogstem", "smogstem_forest", "43FD4AEBB9548E57", "Smogstem Forest",
     "the Undergarden's everyday forest of smogstem trees.", None),
    ("ug_bi_rogdorium_grove", "rogdorium_grove", "6F483B77D64F4EE2", "Rogdorium Grove",
     "the richest place in the Depths for rogdorium.", None),
]

# --- single plants (ATM10's top-right block) ---------------------------------------------------------------------
_PLANTS = [
    # key, item, ATM10 id, title, what, how
    ("ug_wigglewood_sapling", "wigglewood_sapling", "51C59FDF0BD11FDF", "Wigglewood Sapling",
     "a sapling to grow wigglewood at home.", "break wigglewood leaves until one drops."),
    ("ug_grongle_sapling", "grongle_sapling", "2C5A7E4CD8B57E08", "Grongle Sapling",
     "a sapling to grow grongle trees at home.", "break grongle leaves in the gronglegrowth until one drops."),
    ("ug_veil_mushroom", "veil_mushroom", "0FA77C28A57E06F1", "Veil Mushroom",
     "a small veil mushroom, the seed of the veiled stew.", "pick one in the veil mushroom bog."),
    ("ug_ink_mushroom", "ink_mushroom", "739601B0C43B239B", "Ink Mushroom",
     "a small ink mushroom, the seed of the inky stew.", "pick one in the ink mushroom bog."),
    ("ug_indigo_mushroom", "indigo_mushroom", "4C5CFA45D9B4F6D3", "Indigo Mushroom",
     "a small indigo mushroom, the seed of the indigo stew.", "pick one in the indigo mushroom bog."),
    ("ug_droopvine", "droopvine_item", "4568C2F465EDB960", "Droopvine",
     "droopvines hang from cavern roofs and carry glowing droopfruit.", "pick the fruit off a vine; the vines are climbable, too."),
]


def _kill_quests():
    out = []
    for key, ent, mir, title, sub, what, how, tip in _KILLS:
        dep = "wd_vestige" if ent == "mysterious_pot" else "ug_enter"
        # a creature collection: optional (less grind) unless another quest builds on the kill
        out.append(Q(key, 0, 0, [kill(UG + ent)], title, deps=[dep], xp=75, loot="hunt", mirror=mir,
                     optional=key not in ("ug_k_gwibling", "ug_k_mog"),
                     section="Creatures of the Dark", subtitle=sub, desc=[
                         "&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip]))
    return out


def _biome_quests():
    out = []
    for key, b, mir, title, what, chem in _BIOMES:
        grove = b == "rogdorium_grove"
        how = ("tunnel down through the dreadrock with a Forgotten pickaxe and find it in the Depths." if grove
               else "Nature's Compass works in the Undergarden. Walk in.")
        desc = ["&eWhat:&r " + what] + (["&eChemistry:&r " + chem] if chem else []) + ["&eHow:&r " + how]
        out.append(Q(key, 0, 0, [biome(UG + b)], title, deps=["ug_depths" if grove else "ug_enter"], xp=50, mirror=mir,
                     optional=True,  # a biome collection: optional (less grind)
                     section="Biomes Below", subtitle="Visit the " + title, desc=desc))
    return out


def _plant_quests():
    return [Q(key, 0, 0, [item(UG + it)], title, deps=["ug_enter"], xp=40, mirror=mir, section="Gathering in the Dark",
              optional=True,  # a plant collection: optional (less grind)
              subtitle="One " + title.lower(), desc=["&eWhat:&r " + what, "&eHow:&r " + how])
            for key, it, mir, title, what, how in _PLANTS]


CHAPTER = Chapter("undergarden", "The Undergarden", "undergarden:catalyst",
        ["A forgotten land under the world, opened with acid."], SIDE, [
    # ============================ into the dark (ATM10: catalyst, guide, the dimension hub) ============================
    Q("ug_catalyst", 0, 0, [item(UG + "catalyst")], "The Catalyst", deps=["t4_undergarden"], xp=100, mirror="6C4B93FE64BD418D",
      section="Into the Dark", subtitle="The key that opens the world below", desc=[
        "&6Acid opened the way, and the dark below remembers you. You were the one who sealed it.&r",
        "&eWhat:&r the Catalyst lights an Undergarden portal: a stone-brick frame, like a Nether portal's.",
        "&eHow:&r copper ingots, stone, an ender pearl and a bucket of sulfuric acid (MI, Mekanism or ChemLib; this pack's recipe, check JEI).",
        "&eTip:&r keep it: the Catalyst isn't used up, so one lights every portal you build."]),
    Q("ug_guide", 0, 0, [tick()], "Before You Go Down", deps=[], xp=10, optional=True, tokens=0, mirror="4C7E006502E30C20",
      icon="undergarden:depthrock", subtitle="How this page works", desc=[
        "&eWhat:&r the Undergarden is a whole world under the Overworld: its own biomes, metals, food and rotting monsters.",
        "&eHow:&r the creatures, biomes and plants on this page are one quick task each. The metals below them build into the gear you'll want down there.",
        "&eTip:&r click the checkmark once you've read this."]),
    Q("ug_enter", 0, 0, [dim(UG + "undergarden")], "The Undergarden", deps=["ug_catalyst"], xp=300, size=2.0,
      mirror="1C232674CD04024D", subtitle="Step through into the dark", desc=[
        "&6No sun, no sky, and still the place feels like home. You remember why you hid it so well.&r",
        "&eWhat:&r a dimension beneath the world: depthrock caverns, sunless forests, seas and the rotspawn infection.",
        "&eHow:&r build the stone-brick frame, light it with the Catalyst and step through.",
        "&eTip:&r the Undergarden has no sun. Bring a stack of torches and mark your portal."]),

    # ============================ ruins (ATM10: the ends of the creature row) ============================
    Q("wd_catacombs", 4, 8, [structure(UG + "catacombs")], "The Catacombs", deps=["ug_enter"], xp=250, size=1.5,
      mirror="00CB8D60E7831A57", section="Ruins of the Builders", subtitle="A buried tomb, still guarded", desc=[
        "&eWhat:&r the catacombs are a buried tomb of the Undergarden's old builders. The Forgotten Guardian, a hulking armoured giant, still stands watch.",
        "&eHow:&r the Explorer's Compass can find one. Step inside.",
        "&eTip:&r the chests hold Forgotten upgrade templates and regalium."]),
    Q("ug_guardian", 0, 0, [kill(UG + "forgotten_guardian")], "The Forgotten Guardian", deps=["wd_catacombs"], xp=400, size=2.0,
      loot="boss", mirror="1054168AFD8520D4", subtitle="Wake the catacombs' keeper, and win", desc=[
        "&6You remember the old guardians and the oaths they swore. This one has forgotten its own.&r",
        "&eWhat:&r the Undergarden's boss. It drops Forgotten nuggets, the only source of Forgotten metal.",
        "&eHow:&r clear the catacomb halls, then fight the guardian.",
        "&eTip:&r it's slow; hit it, step back out of its swing, and repeat."]),
    Q("wd_vestige", 2, 10, [structure(UG + "forgotten_vestige")], "A Forgotten Vestige", deps=["ug_enter"], xp=150, size=1.5,
      mirror="75A66B81C1181F59", section="Ruins of the Builders", subtitle="Ruins of the old builders", desc=[
        "&eWhat:&r forgotten vestiges are ruins left by the Undergarden's builders, guarded by the Forgotten and full of pots.",
        "&eHow:&r explore until you find one (the Explorer's Compass helps) and step inside.",
        "&eTip:&r Denizen camps are the other settlement down here; they belong to the hostile Denizens who live there now."]),
    Q("ug_battleaxe", 6, 2, [kill(UG + "forgotten", 3)], "The Forgotten", deps=["ug_enter"], xp=150, loot="hunt",
      mirror="141681FE9E524FB0", section="Creatures of the Dark", subtitle="Armoured dead in the ruins", desc=[
        "&eWhat:&r the Forgotten are armoured undead that guard the catacombs and vestiges. Some carry a cloggrum battleaxe or ancient armour.",
        "&eHow:&r kill three Forgotten in a catacomb or vestige.",
        "&eTip:&r they hit hard but slowly. Shield up, then strike."]),
    Q("ug_minion", 8, -4, [kill(UG + "forgotten_guardian"), item(UG + "forgotten_block")], "A Minion of Your Own", deps=["ug_enter"], xp=200,
      mirror="5B4B5C148D63ACA1", section="Creatures of the Dark", subtitle="Build what the guardian was", desc=[
        "&eWhat:&r stack a carved gloomgourd on a block of Forgotten metal and it wakes as a Forgotten Minion that fights for you.",
        "&eHow:&r a block of Forgotten metal is nine Forgotten Ingots, so beat the guardian until you have enough nuggets.",
        "&eTip:&r the mod has an advancement for building one; the minion fires at your enemies."]),
    Q("ug_rotbelcher", 0, -4, [kill(UG + "rotbelcher"), item(UG + "utheric_shard", 8)], "The Rotbelcher", deps=["ug_enter"], xp=150,
      loot="hunt", mirror="1D2C70F1750E84D0", section="Creatures of the Dark", subtitle="The rotspawn that spits", desc=[
        "&eWhat:&r a bloated rotspawn that hurls rot from a distance. Like rotbeasts, it drops utheric shards.",
        "&eHow:&r close the distance fast, or fight it with a bow or slingshot from cover. Collect 8 shards from it and its kin.",
        "&eTip:&r a shard torch nearby softens it up while you fight."]),
    Q("ug_brute", 2, -4, [kill(UG + "brute"), item(UG + "brute_tusk", 2)], "Brutes", deps=["ug_enter"], xp=100,
      loot="hunt", mirror="119242549BD21764", section="Creatures of the Dark", subtitle="Tusks for bone meal", desc=[
        "&eWhat:&r brutes are tusked beasts that leave you alone until you hit them. Their tusks grind into bone meal.",
        "&eChemistry:&r tusks, teeth and bone are mostly hydroxyapatite, Ca₅(PO₄)₃OH, which is why bone meal feeds plants phosphorus.",
        "&eHow:&r one brute tusk crafts into four bone meal."]),
    Q("ug_denizen", 4, -4, [kill(UG + "denizen")], "The Denizens", optional=True, deps=["ug_enter"], xp=100,
      loot="hunt", mirror="2A2041098C069772", section="Creatures of the Dark", subtitle="The Undergarden's current tenants", desc=[
        "&eWhat:&r Denizens live in camps around campfires. They drop mysterious masks, and their camp chests hold more.",
        "&eHow:&r find a denizen camp and fight. Breaking their campfire angers the whole camp.",
        "&eTip:&r draw them out one at a time."]),
    Q("ug_scintling", 6, -4, [kill(UG + "scintling")], "You Monster", deps=["ug_enter"], xp=50,
      secret=True, loot="secret", mirror="4F3B4990BE6C2A4A", section="Creatures of the Dark", subtitle="Secret: it was just a snail", desc=[
        "&eWhat:&r you killed a scintling, a harmless glowing snail. It dropped a goo ball.",
        "&eChemistry:&r real snail slime is a mix of glycoproteins and water that thickens under stress, letting the snail glue itself to walls.",
        "&eTip:&r goo balls make sticky pistons, so at least it wasn't for nothing."]),
    *_kill_quests(),

    # ============================ biomes ============================
    Q("ug_bogs", 6, -2, [biome(UG + "blood_mushroom_bog")], "Blood Mushroom Bog", optional=True, deps=["ug_enter"], xp=50,
      mirror="06D13E319C26C949", section="Biomes Below", subtitle="Visit the Blood Mushroom Bog", desc=[
        "&eWhat:&r a bog grown over with giant blood mushrooms. Each bog is named after its mushroom, and each mushroom makes its own stew.",
        "&eChemistry:&r a fungus is closer to an animal than a plant: its cell walls are chitin, (C₈H₁₃O₅N)ₙ, the same polymer as insect shells.",
        "&eHow:&r Nature's Compass works down here. Walk in."]),
    Q("wd_undergarden_biomes", 4, 10, [biome(UG + "forgotten_field")], "Forgotten Field", optional=True, deps=["ug_enter"], xp=50,
      mirror="4E3D548E5D8D7D26", section="Biomes Below", subtitle="Visit the Forgotten Field", desc=[
        "&eWhat:&r open fields where the Forgotten wander and the vestiges stand.",
        "&eHow:&r Nature's Compass works here too. Walk in."]),
    Q("ug_depths", 8, 0, [biome(UG + "depths")], "The Depths", deps=["ug_forgotten_tools"], xp=300,
      mirror="6E7C8537D8A28833", section="Biomes Below", subtitle="Break the dreadrock floor", desc=[
        "&6Under the forgotten land there is an older one. You remember the floor you laid over it.&r",
        "&eWhat:&r a layer of dreadrock seals the bottom of the Undergarden. Below it lie the Depths: infected caverns, puff mushroom forests and rogdorium groves.",
        "&eHow:&r dig down until you hit dreadrock, then break through it with a Forgotten pickaxe. Nothing else can mine it.",
        "&eTip:&r the Depths carry the Utheric Infection. Read the rogdorium quest before you stay long."]),
    *_biome_quests(),

    # ============================ metals: cloggrum ============================
    Q("w_undergarden", 0, 8, [item(UG + "cloggrum_ingot")], "Cloggrum", deps=["ug_enter"], xp=150, size=1.5,
      mirror="4141EF8B8C316118", section="Cloggrum", subtitle="The Undergarden's everyday metal", desc=[
        "&eWhat:&r cloggrum is the first Undergarden metal: about as good as iron, and the base for every Forgotten tool later.",
        "&eHow:&r mine cloggrum ore in depthrock (stone pickaxe or better) and smelt the raw cloggrum.",
        "&eTip:&r run a spare through the Alchemistry Dissolver: what is this strange metal made of?"]),
    Q("ug_cloggrum_tools", 2, 0, [item(UG + "cloggrum_pickaxe"), item(UG + "cloggrum_axe"), item(UG + "cloggrum_shovel"),
                                  item(UG + "cloggrum_hoe"), item(UG + "cloggrum_sword")],
      "Cloggrum Tools", optional=True, deps=["w_undergarden"], xp=150, mirror="16A04B2FC3F0D902", subtitle="Pickaxe, axe, shovel, hoe and sword", desc=[
        "&eWhat:&r the full cloggrum toolset.",
        "&eHow:&r cloggrum ingots in the usual tool shapes (check JEI).",
        "&eTip:&r keep them once you replace them: cloggrum tools are what the Forgotten template upgrades."]),
    Q("ug_cloggrum_kit", 0, 0, [item(UG + "cloggrum_battleaxe"), item(UG + "cloggrum_shield")],
      "Battleaxe and Shield", deps=["w_undergarden"], xp=150, mirror="1E81B903137BB62A",
      subtitle="Heavy arms against the Forgotten", desc=[
        "&eWhat:&r a cloggrum battleaxe and shield. The shield holds off the Forgotten's heavy swings.",
        "&eChemistry:&r a shield spreads a blow over a large area: the same force over more area means less pressure (P = F / A) on your arm.",
        "&eHow:&r the battleaxe can't be crafted: a Forgotten carrying one drops it. The shield is cloggrum and planks (check JEI).",
        "&eTip:&r the battleaxe is what the Forgotten template turns into the Forgotten Battleaxe."]),
    Q("ug_cloggrum_armor", 4, 0, [item(UG + "cloggrum_helmet"), item(UG + "cloggrum_chestplate"), item(UG + "cloggrum_leggings"), item(UG + "cloggrum_boots")],
      "Cloggrum Armour", optional=True, deps=["w_undergarden"], xp=150, mirror="130577AD1A1A8222", subtitle="A full suit for the dark", desc=[
        "&eWhat:&r a full set of cloggrum armour. The boots have a perk: scintling goo no longer slows you.",
        "&eHow:&r 24 cloggrum ingots for the set. Raw cloggrum also turns up in depleted mines.",
        "&eTip:&r scintlings leave sticky goo trails across whole caverns; the boots pay for themselves fast."]),

    # ============================ metals: froststeel ============================
    Q("ug_froststeel", 4, 2, [item(UG + "froststeel_ingot")], "Froststeel", deps=["ug_enter"], xp=150, size=1.5,
      mirror="51E2728C5E35A152", section="Froststeel", subtitle="A metal that bites with cold", desc=[
        "&eWhat:&r froststeel weapons give targets the Chilly effect, which slows them.",
        "&eChemistry:&r real steel gets brittle in deep cold: below its ductile-to-brittle transition temperature it cracks instead of bending, which is why ships' hulls once split in icy seas.",
        "&eHow:&r froststeel ore only forms in shiverstone, in the frozen biomes. It needs an iron pickaxe; smelt the raw froststeel.",
        "&eTip:&r raw froststeel has a blast furnace recipe, so smelt it there at double speed."]),
    Q("ug_froststeel_tools", 0, 0, [item(UG + "froststeel_sword"), item(UG + "froststeel_pickaxe"), item(UG + "froststeel_axe"),
                                    item(UG + "froststeel_shovel"), item(UG + "froststeel_hoe")],
      "Froststeel Tools", optional=True, deps=["ug_froststeel"], xp=150, mirror="46DCB235D3FEDA61", subtitle="A full set of cold tools", desc=[
        "&eWhat:&r sword, pickaxe, axe, shovel and hoe of froststeel.",
        "&eChemistry:&r cold slows chemistry down: as a rule of thumb, many reactions run about half as fast for every 10 °C cooler. That's why a fridge keeps food.",
        "&eHow:&r froststeel ingots in the usual tool shapes (check JEI).",
        "&eTip:&r a froststeel sword is great against fast rotspawn; slowed foes can't close the gap."]),
    Q("ug_froststeel_armor", 0, 0, [item(UG + "froststeel_helmet"), item(UG + "froststeel_chestplate"), item(UG + "froststeel_leggings"),
                                    item(UG + "froststeel_boots")],
      "Froststeel Armour", optional=True, deps=["ug_froststeel"], xp=150, mirror="7617737FC179EA1A", subtitle="The cold suit", desc=[
        "&eWhat:&r the full froststeel armour set.",
        "&eHow:&r froststeel ingots in the usual armour shapes (check JEI).",
        "&eTip:&r compare it with cloggrum in your inventory before you commit: pick the set whose perks suit how you fight."]),

    # ============================ metals: Forgotten ============================
    Q("w_forgotten", 6, 8, [item(UG + "forgotten_ingot")], "The Forgotten Ingot", deps=["ug_enter"], xp=300, size=1.5,
      mirror="4F5A2E2A5C7F4837", section="Forgotten Metal", subtitle="Forge the guardian's metal", desc=[
        "&eWhat:&r the Forgotten Guardian drops Forgotten nuggets; nine make a Forgotten Ingot for the strongest Undergarden tools.",
        "&eHow:&r find a catacomb, beat the guardian, and craft the nuggets into an ingot. The smithing template is in catacomb chests.",
        "&eTip:&r it hits hard; armour up and keep your distance between swings."]),
    Q("ug_forgotten_tools", 6, 0, [item(UG + "forgotten_pickaxe"), item(UG + "forgotten_axe"), item(UG + "forgotten_shovel"),
                                   item(UG + "forgotten_hoe"), item(UG + "forgotten_sword")],
      "Forgotten Tools", deps=["w_forgotten"], xp=300, mirror="6124C0E9E419694B", subtitle="Upgrade cloggrum with the guardian's metal", desc=[
        "&eWhat:&r Forgotten tools mine Undergarden blocks 1.5x as fast, Forgotten weapons hit non-boss Undergarden mobs 1.5x as hard. Only a Forgotten pickaxe can break dreadrock.",
        "&eHow:&r smithing table: Forgotten upgrade template + cloggrum tool + Forgotten Ingot, once for each. Templates come from catacomb chests.",
        "&eTip:&r copy a template with 7 diamonds and a block of depthrock (makes 2). Do it before you use your last one."]),
    Q("ug_forgotten_battleaxe", 8, 2, [item(UG + "forgotten_battleaxe")], "Forgotten Battleaxe", deps=["w_forgotten"], xp=200,
      mirror="0D91A6B36BD2F526", subtitle="The heaviest weapon below", desc=[
        "&eWhat:&r the cloggrum battleaxe, upgraded with Forgotten metal.",
        "&eHow:&r smithing table: Forgotten upgrade template + cloggrum battleaxe + Forgotten Ingot.",
        "&eTip:&r with the five Forgotten tools that makes all six, which the mod has an advancement for."]),
    Q("ug_crumbling", 0, 0, [item(UG + "crumbling_catalyst")], "Crumbling Catalyst", deps=["w_forgotten"], xp=100,
      mirror="4985F82E0D300C6D", subtitle="A catalyst that's spent once used", desc=[
        "&eWhat:&r a cheaper, crumbling cousin of the Catalyst: it lights an Undergarden portal frame and is used up doing it.",
        "&eChemistry:&r the name is a joke for chemists: a true catalyst is never used up by the reaction it speeds. This one is a reagent wearing a catalyst's name.",
        "&eHow:&r four cloggrum ingots, four depthrock and one Forgotten nugget in the middle (check JEI).",
        "&eTip:&r use it for a second portal near another base, and keep the real Catalyst safe."]),

    # ============================ rogdorium and the Infuser ============================
    Q("ug_rogdorium", 10, 0, [item(UG + "rogdorium")], "Rogdorium", deps=["ug_forgotten_tools"], xp=200, size=1.5,
      mirror="257893DD23BF5017", section="Rogdorium and Utherium", subtitle="The antidote grows in dreadrock", desc=[
        "&eWhat:&r rogdorium is a crystal found only in dreadrock. It's the key to the Infuser, and eating it holds back the Utheric Infection.",
        "&eChemistry:&r real poisoning by heavy metals is treated much the same way: a chelating agent such as EDTA binds the toxic metal ions so the body can flush them out.",
        "&eHow:&r mine dreadrock rogdorium ore with a Forgotten pickaxe (it drops rogdorium) or smelt the ore block.",
        "&eTip:&r carry a few rogdorium nuggets on every trip down; eat one when the infection meter climbs."]),
    Q("ug_infuser", 12, 0, [item(UG + "infuser")], "The Infuser", deps=["ug_rogdorium"], xp=200, mirror="5AF0E903DB670D65",
      subtitle="Purify or corrupt what you put in", desc=[
        "&eWhat:&r the Undergarden's own processing block. With rogdorium fuel it purifies; with utherium it corrupts.",
        "&eChemistry:&r the idea is old: purification is often just a reaction that removes one impurity, the way a blast furnace strips oxygen from iron ore.",
        "&eHow:&r an utheric cluster, rogdorium and five dreadrock (check JEI). It also gives armour a Rogdorium Infusion.",
        "&eTip:&r JEI's Infusing category lists every conversion, including which fuel slot it needs."]),
    Q("ug_spear", 10, 2, [item(UG + "spear")], "Rogdorium Spear", deps=["ug_rogdorium"], xp=100, mirror="19862DBCE9305DE3",
      subtitle="A throwable point of antidote", desc=[
        "&eWhat:&r a spear you can stab with or throw, like a trident without the water.",
        "&eHow:&r one rogdorium on top of two sticks.",
        "&eTip:&r retrieve it after every throw; it doesn't come back on its own."]),
    Q("ug_totem", 0, 0, [item(UG + "denizen_totem")], "Mysterious Totem", deps=["ug_rogdorium"], xp=100, mirror="30ED5FF9DF7B34CF",
      subtitle="Purify an ancient root", desc=[
        "&eWhat:&r a carved totem like the ones in denizen camps.",
        "&eHow:&r purify an ancient root in the Infuser with rogdorium, or loot one from a denizen camp chest.",
        "&eTip:&r it's an axe-mined block, so break and move it with an axe."]),
    Q("ug_utherium", 14, 0, [item(UG + "utherium_crystal")], "Purified Utherium", deps=["ug_enter", "ug_infuser"], xp=250, size=1.5,
      mirror="30582B5FBED35FD1", subtitle="Turn utheric clusters into crystal", desc=[
        "&6Rot fears what is pure. You remember forging blades for exactly this.&r",
        "&eWhat:&r utherium crystal is the Undergarden's weapon against rotspawn. Mined utherium ore only gives raw utheric clusters.",
        "&eHow:&r mine or smelt utherium ore for clusters (9 utheric shards also make one), then purify each cluster in the Infuser with rogdorium.",
        "&eTip:&r rotbeasts and rotbelchers drop utheric shards, so hunting them feeds the line."]),
    Q("ug_utherium_tools", 0, 0, [item(UG + "utherium_sword"), item(UG + "utherium_pickaxe"), item(UG + "utherium_axe"),
                                  item(UG + "utherium_shovel"), item(UG + "utherium_hoe")],
      "Utherium Tools", optional=True, deps=["ug_utherium"], xp=250, mirror="1FCF946B7BE3C0BD", subtitle="The purest tools below", desc=[
        "&eWhat:&r the full utherium toolset. Utherium weapons deal 1.5x damage to rotspawn.",
        "&eHow:&r utherium crystals in the usual tool shapes (check JEI).",
        "&eTip:&r a worn-out utherium tool smelts back into a crystal, so nothing is wasted."]),
    Q("ug_utherium_armor", 0, 0, [item(UG + "utherium_helmet"), item(UG + "utherium_chestplate"), item(UG + "utherium_leggings"),
                                  item(UG + "utherium_boots")],
      "Utherium Armour", optional=True, deps=["ug_utherium"], xp=250, mirror="01B13BBB41BBB460", subtitle="The Undergarden's best plain set", desc=[
        "&eWhat:&r the full utherium armour set.",
        "&eChemistry:&r a crystal's strength comes from its lattice: every atom held by bonds in every direction, which is why diamond (carbon in a 3D lattice) is so hard.",
        "&eHow:&r utherium crystals in the usual armour shapes (check JEI).",
        "&eTip:&r the Infuser can still give this armour a Rogdorium Infusion."]),

    # ============================ regalium and the odd finds ============================
    Q("w_regalium", 2, 8, [item(UG + "regalium_crystal")], "Regalium", deps=["ug_enter"], xp=150, size=1.5,
      mirror="3AF7446592D19FA6", section="Regalium and Finds", subtitle="The Undergarden's precious crystal", desc=[
        "&eWhat:&r regalium is the Undergarden's treasure: a rare crystal in depthrock and shiverstone.",
        "&eHow:&r smelt regalium ore. It also turns up in catacomb chests.",
        "&eTip:&r catacombs are also where the Forgotten Guardian waits."]),
    Q("ug_slingshot", 2, 2, [item(UG + "slingshot")], "Slingshot", deps=["ug_enter"], xp=75, mirror="1190BB433EFA3945",
      subtitle="Wigglewood, pebbles and patience", desc=[
        "&eWhat:&r a ranged weapon that fires pebbles, goo balls, gronglets or rotten blisterberries.",
        "&eHow:&r twistytwigs (two wigglewood planks make four) and sticks. Pebbles drop from mogs and stoneborn, or stonecut depthrock.",
        "&eTip:&r it takes its own enchantments: Ricochet bounces shots off walls, Self Sling launches you instead."]),
    Q("ug_blisterbomb", 2, 4, [item(UG + "blisterbomb"), item(UG + "boomgourd")], "Things That Burst", deps=["ug_enter"], xp=100,
      mirror="5E63C78CDC44FF95", subtitle="A blisterbomb and a boomgourd", desc=[
        "&eWhat:&r a blisterbomb is a throwable of rotten blisterberries that bursts into a harmful cloud; a boomgourd is a gloomgourd packed with them, and explodes.",
        "&eChemistry:&r real rotting fruit ferments: yeast turns its sugar into ethanol and carbon dioxide (C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂), and sealed fruit can split from the gas.",
        "&eHow:&r a twistytwig over six rotten blisterberries makes blisterbombs; eight around a gloomgourd make a boomgourd (check JEI).",
        "&eTip:&r treat the boomgourd like TNT: place it, light it, step back."]),
    Q("ug_ancient_armor", 0, 0, [item(UG + "ancient_helmet"), item(UG + "ancient_chestplate"), item(UG + "ancient_leggings")], "Ancient Armour",
      deps=["ug_enter", "ug_battleaxe"], xp=250, loot="hunt", mirror="49EB9FB2133E3219", subtitle="Rare gear off the Forgotten", desc=[
        "&eWhat:&r the Forgotten wear ancient armour. It has no recipe: the only way to get a piece is from a Forgotten when it falls.",
        "&eHow:&r keep fighting Forgotten in catacombs and vestiges until you have the helmet, chestplate and leggings. Looting helps.",
        "&eTip:&r drops are rare; a vestige full of Forgotten is the best hunting ground."]),
    Q("ug_denizen_mask", 0, 0, [item(UG + "denizen_mask")], "Mysterious Mask", deps=["ug_enter"], xp=100, mirror="30D6924003C6E273",
      subtitle="A Denizen's face, to wear", desc=[
        "&eWhat:&r the carved masks the Denizens wear.",
        "&eHow:&r Denizens drop them, and their camp chests hold more.",
        "&eTip:&r wear one to the next camp and see who notices."]),

    # ============================ gathering (ATM10's plant block) ============================
    Q("ug_saplings", 0, 0, [item(UG + "smogstem_sapling")], "Smogstem Sapling", optional=True, deps=["ug_enter"], xp=40, mirror="6D4FB6291CA8D1A6",
      section="Gathering in the Dark", subtitle="Grow the Undergarden at home", desc=[
        "&eWhat:&r a smogstem sapling, so you can farm the Undergarden's everyday wood without the trip.",
        "&eChemistry:&r real trees couldn't grow here: photosynthesis (6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂) needs light. Underground life runs on chemosynthesis or on food from above.",
        "&eHow:&r break smogstem leaves until one drops a sapling."]),
    Q("ug_mushrooms", 0, 0, [item(UG + "blood_mushroom")], "Blood Mushroom", deps=["ug_enter"], xp=40, mirror="6751F2651063B3A5",
      subtitle="The first of four small mushrooms", desc=[
        "&eWhat:&r a small blood mushroom, the seed of the bloody stew.",
        "&eChemistry:&r real ink caps (Coprinus) digest their own gills into a black liquid as they ripen, and people once wrote with it. The Undergarden's ink mushroom is a nod to them.",
        "&eHow:&r they grow on the ground in the bogs and forests; the blood mushroom bog has the most."]),
    Q("ug_berries", 0, 0, [item(UG + "blisterberry")], "Blisterberries", deps=["ug_enter"], xp=40, mirror="6F416275B6F6D8F0",
      subtitle="Fresh, and sometimes rotten", desc=[
        "&eWhat:&r blisterberry bushes drop both fresh and rotten berries. The rotten ones are slingshot ammo and the base of blisterbombs.",
        "&eChemistry:&r rotting is chemistry by microbes: yeasts and bacteria break sugars into ethanol, acids and gas, which is why spoiled fruit fizzes and smells sour.",
        "&eHow:&r harvest blisterberry bushes in the forests.",
        "&eTip:&r don't eat the rotten ones."]),
    Q("ug_gloomgourd", 6, 4, [item(UG + "gloomgourd"), item(UG + "gloomgourd_seeds")], "Gloomgourds", deps=["ug_enter"], xp=50,
      mirror="22739522F0D33D7B", subtitle="The Undergarden's pumpkin", desc=[
        "&eWhat:&r a dark gourd that grows like a pumpkin. Carve it for lanterns and minions, or bake it into pie.",
        "&eHow:&r find a wild gloomgourd; one gourd crafts into four seeds. Plant them on deepsoil farmland.",
        "&eTip:&r a carved gloomgourd over a torch makes a gloom-o-lantern; over a shard torch, a shard-o-lantern."]),
    Q("ug_beans", 0, 0, [item(UG + "underbeans")], "Underbeans", deps=["ug_enter"], xp=40, mirror="08D9C809CF4062E8",
      subtitle="Pick a bush in the dark", desc=[
        "&eWhat:&r underbean bushes grow on the forest floors. Their beans are the Undergarden's first food.",
        "&eChemistry:&r beans are protein-rich because legumes host bacteria that fix nitrogen from the air: N₂ becomes ammonia (NH₃), and the plant builds amino acids from it.",
        "&eHow:&r right-click a ripe underbean bush to pick it.",
        "&eTip:&r raw beans are edible, but roasted ones are far better."]),
    Q("ug_glow_food", 0, 0, [item(UG + "glitterkelp")], "Glitterkelp", deps=["ug_enter"], xp=40, mirror="43A1BC20BB054A14",
      subtitle="Food that glows, from the seas", desc=[
        "&eWhat:&r glitterkelp grows in the Undergarden's seas. It's edible and smelts into dried kelp.",
        "&eChemistry:&r real kelp is where iodine was discovered: in 1811 Bernard Courtois added sulfuric acid to seaweed ash and saw violet I₂ vapour rise.",
        "&eHow:&r harvest it from the water.",
        "&eTip:&r the gloomgourd pie needs a glitterkelp."]),
    Q("ug_gronglet", 0, 0, [item(UG + "gronglet")], "Gronglet", deps=["ug_enter"], xp=40, mirror="5FCA6F5FE97780B7",
      subtitle="A little glowing growth", desc=[
        "&eWhat:&r small glowing growths that hang on grongle trees in the gronglegrowth. The Infuser can purify or corrupt them.",
        "&eHow:&r break a wild gronglet to pick it up.",
        "&eTip:&r keep two: a side quest later wants one of each Infuser kind."]),
    *_plant_quests(),

    # ============================ side quests (ours; ATM10 has no match) ============================
    Q("ug_arrival", 0, 0, [item(UG + "depthrock", 32)], "Depthrock", deps=["ug_enter"], xp=100, optional=True, tokens=1,
      subtitle="Optional: the bedrock of a world below the world", desc=[
        "&eWhat:&r depthrock is the Undergarden's stone, the way deepslate is the Overworld's. Its ores (cloggrum, froststeel, utherium, regalium) all sit in it or in icy shiverstone.",
        "&eChemistry:&r dissolve depthrock in the Alchemistry Dissolver and it gives silicon dioxide (SiO₂), iron and aluminium, with rare traces of zirconium, gallium, dysprosium and tungsten.",
        "&eHow:&r mine it anywhere below.",
        "&eTip:&r depthrock stonecuts into pebbles for the slingshot."]),
    Q("ug_utherium_gear", 16, 0, [item(UG + "utherium_sword"), item(UG + "utherium_chestplate")], "Bane of the Rotspawn", deps=["ug_utherium"], xp=200,
      optional=True, tokens=1, subtitle="Optional: utherium sword and chestplate", desc=[
        "&eWhat:&r utherium weapons deal 1.5x damage to rotspawn; the armour is the Undergarden's best plain set.",
        "&eHow:&r craft them from utherium crystals like diamond gear (check JEI).",
        "&eTip:&r the sword and chestplate are the two pieces to make first."]),
    Q("ug_clusters", 0, 0, [item(UG + "utheric_cluster", 4)], "Utheric Clusters", deps=["ug_depths"], xp=150, optional=True, tokens=1,
      subtitle="Optional: raw, corrupted utherium", desc=[
        "&eWhat:&r mined utherium ore gives utheric clusters: utherium still full of the infection. The Infuser needs one to be built, and purifies the rest.",
        "&eChemistry:&r most real ores come out of the ground impure too: the metal is locked in a compound with sulfur, oxygen or arsenic, and refining is the work of pulling it free.",
        "&eHow:&r utherium ore sits in depthrock, shiverstone, tremblecrust and the Depths' dreadrock. Mine or smelt it; nine utheric shards also make a cluster.",
        "&eTip:&r mine extra: every utherium crystal you will ever make starts as one of these."]),
    Q("ug_depths_biomes", 8, -2, [biome(UG + "infected_depths"), biome(UG + "puff_mushroom_forest")], "Deeper Still",
      deps=["ug_depths"], xp=150, optional=True, tokens=1, subtitle="Optional: two more regions under the dreadrock", desc=[
        "&eWhat:&r the rest of the Depths: the infected depths and the puff mushroom forest.",
        "&eHow:&r with a Forgotten pickaxe, tunnel through dreadrock to each one.",
        "&eTip:&r the infection is strongest here; eat rogdorium before the meter fills."]),
    Q("ug_gronglets", 12, 2, [item(UG + "rogdoric_gronglet"), item(UG + "utheric_gronglet")], "Two Kinds of Gronglet", deps=["ug_infuser", "ug_gronglet"], xp=100,
      optional=True, tokens=1, subtitle="Optional: purify one, corrupt one", desc=[
        "&eWhat:&r the Infuser can purify a gronglet with rogdorium or corrupt one with utherium.",
        "&eHow:&r collect two wild gronglets, then run one through each Infuser mode (JEI shows both).",
        "&eTip:&r gronglets also work as slingshot ammo. The mod asks if that is okay."]),
    Q("ug_collector", 16, 2, [item(UG + "cloggrum_block"), item(UG + "froststeel_block"), item(UG + "utherium_block"), item(UG + "regalium_block"),
                               item(UG + "rogdorium_block"), item(UG + "forgotten_block")],
      "Collector's Shelf", deps=["ug_utherium"], xp=300, optional=True, tokens=2, loot="boss",
      subtitle="Optional: a block of every Undergarden metal", desc=[
        "&eWhat:&r one storage block each of cloggrum, froststeel, utherium, regalium, rogdorium and Forgotten metal.",
        "&eChemistry:&r feed spares to the Dissolver: the Undergarden's metals are fiction, but what they break down into tells you what the pack thinks they are made of.",
        "&eHow:&r nine of each ingot or crystal in a crafting grid.",
        "&eTip:&r a Forgotten block and a carved gloomgourd summon a Forgotten Minion."]),
    Q("ug_forgotten_kit", 0, 0, [item(UG + "forgotten_axe"), item(UG + "forgotten_shovel"), item(UG + "forgotten_hoe")],
      "Forgotten Kit", deps=["ug_forgotten_tools"], xp=100, optional=True, tokens=1,
      subtitle="Optional: the working half of the set", desc=[
        "&eWhat:&r Forgotten axe, shovel and hoe: the same 1.5x speed on Undergarden blocks as the pickaxe.",
        "&eHow:&r smithing table: Forgotten upgrade template + cloggrum tool + Forgotten Ingot, once for each.",
        "&eTip:&r these three are the ones you'll reach for when building down here."]),
    Q("ug_nuggets", 0, 0, [item(UG + "cloggrum_nugget", 9), item(UG + "froststeel_nugget", 9), item(UG + "forgotten_nugget", 9)],
      "Small Change", deps=["w_forgotten"], xp=75, optional=True, tokens=1, subtitle="Optional: nuggets of three metals", desc=[
        "&eWhat:&r nuggets of cloggrum, froststeel and Forgotten metal. Forgotten nuggets are how the guardian pays out: nine make an ingot.",
        "&eChemistry:&r real nuggets only form from unreactive metals. Gold turns up native in rivers because it doesn't oxidise; iron almost never does.",
        "&eHow:&r break an ingot into nine in the crafting grid; Forgotten nuggets drop from the Forgotten Guardian.",
        "&eTip:&r a Forgotten nugget is also the heart of the Crumbling Catalyst."]),
    Q("ug_woods", 0, -2, [item(UG + "smogstem_log", 8), item(UG + "wigglewood_log", 8), item(UG + "grongle_log", 8)], "Woods Without Sun",
      deps=["ug_enter"], xp=75, optional=True, tokens=1, subtitle="Optional: smogstem, wigglewood, grongle", desc=[
        "&eWhat:&r three kinds of tree that grow with no daylight at all.",
        "&eHow:&r smogstem forests, wigglewood forests and the gronglegrowth each have their own tree.",
        "&eTip:&r wigglewood planks make the twistytwigs for the slingshot."]),
    Q("ug_shard_torch", 2, -2, [item(UG + "shard_torch", 8)], "Shard Torches", deps=["ug_enter"], xp=75,
      subtitle="Optional: light that burns rotspawn", optional=True, tokens=1, desc=[
        "&eWhat:&r a torch tipped with an utheric shard. It lights the dark and hurts rotspawn that come close.",
        "&eHow:&r one utheric shard on a stick. Shards drop from rotbeasts and rotbelchers and sit in catacomb chests.",
        "&eTip:&r ring your portal and your base with them."]),
    Q("ug_depleted_mine", 4, -2, [structure(UG + "depleted_mine")], "A Depleted Mine", deps=["ug_enter"], xp=100,
      optional=True, tokens=1, subtitle="Optional: someone mined here before you", desc=[
        "&eWhat:&r old mines left by the Undergarden's builders. The chests still hold raw cloggrum, raw froststeel and cloggrum tools.",
        "&eHow:&r explore depthrock caverns until you find timber supports and rails; step inside.",
        "&eTip:&r a quick way to an early cloggrum pickaxe."]),
    Q("ug_mogmoss", 0, 0, [item(UG + "mogmoss", 4), item(UG + "blue_mogmoss", 4)], "Mogmoss", deps=["ug_k_mog"], xp=75,
      optional=True, tokens=1, subtitle="Optional: moss from two kinds of mog", desc=[
        "&eWhat:&r mogs drop mogmoss; the smog mogs of the smog spires drop the blue kind.",
        "&eHow:&r hunt mogs in the depthrock forests and smog mogs in the smog spires. Mogmoss makes rugs and slop bowls.",
        "&eTip:&r mogs also drop depthrock pebbles for the slingshot."]),
    Q("ug_goo", 0, 0, [item(UG + "goo_ball", 8)], "Scintling Goo", deps=["ug_enter"], xp=50,
      optional=True, tokens=1, subtitle="Optional: harvest the snail trail", desc=[
        "&eWhat:&r goo balls, the sticky stuff scintlings leave behind. They work like slime balls: sticky pistons, leads and goo blocks.",
        "&eChemistry:&r slime is a hydrogel: long, tangled polymer chains (glycoproteins, in a real snail) holding many times their weight in water.",
        "&eHow:&r break the goo trail blocks scintlings leave across the caverns; each drops goo balls. No need to hurt the snail.",
        "&eTip:&r cloggrum boots stop goo from slowing you down."]),
    Q("ug_secret_disc", 10, -4, [item(UG + "music_disc_gloomper_secret")], "The Gloomper's Secret", deps=["ug_enter"], xp=150,
      secret=True, loot="secret", subtitle="Secret: a disc the gloompers kept quiet", desc=[
        "&6Even down here someone wrote music. You remember humming it.&r",
        "&eWhat:&r a hidden music disc from the Undergarden. The mod counts finding it as a challenge.",
        "&eTip:&r the Undergarden has four more discs; play them on a jukebox."]),
    Q("ug_raw_meat", 0, 0, [item(UG + "raw_dweller_meat", 4), item(UG + "raw_gloomper_leg", 4)], "Hunting Below", deps=["ug_enter"], xp=50,
      optional=True, tokens=1, subtitle="Optional: dwellers and gloompers", desc=[
        "&eWhat:&r dwellers (big rideable grazers) and gloompers (hopping toads) are the Undergarden's game animals. Both drop meat and leather.",
        "&eHow:&r hunt them in the forests and fields. Cook the meat in the next quest.",
        "&eTip:&r gloompers hop away fast; a slingshot or bow helps."]),
    Q("ug_meat", 4, 4, [item(UG + "dweller_steak", 4), item(UG + "gloomper_leg", 4)], "Hunter's Supper", deps=["ug_raw_meat"], xp=75,
      optional=True, tokens=1, subtitle="Optional: dweller steak and gloomper leg", desc=[
        "&eWhat:&r the best meats below, cooked.",
        "&eChemistry:&r heat denatures meat proteins: the coiled chains unfold and bond to each other, which is why meat firms up as it cooks.",
        "&eHow:&r cook the raw meat in a furnace, smoker or campfire."]),
    Q("ug_gwibling", 4, 6, [item(UG + "gwibling_bucket"), item(UG + "cooked_gwibling", 4)], "Weird Fish", deps=["ug_k_gwibling"], xp=75,
      optional=True, tokens=1, subtitle="Optional: catch a gwibling, cook a few more", desc=[
        "&eWhat:&r gwiblings are the small fish of the Undergarden seas. Catch one live, or cook them.",
        "&eHow:&r use a water bucket on a gwibling to catch it; kill others for raw gwibling and smelt it.",
        "&eTip:&r the full-grown gwib is not a friendly fish. Watch the water."]),
    Q("ug_underbeans", 0, 4, [item(UG + "roasted_underbeans", 8)], "Roasted Underbeans", deps=["ug_beans"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the first meal below", desc=[
        "&eWhat:&r the beans are edible raw, much better roasted.",
        "&eChemistry:&r roasting browns food by the Maillard reaction: amino acids and sugars combine into hundreds of new flavour molecules above about 140 °C.",
        "&eHow:&r smelt or campfire-cook underbeans.",
        "&eTip:&r underbeans on a stick steer a dweller you're riding."]),
    Q("ug_bean_stick", 0, 0, [item(UG + "underbean_on_a_stick")], "Underbean on a Stick", deps=["ug_underbeans"], xp=75,
      optional=True, tokens=1, subtitle="Optional: steer a dweller", desc=[
        "&eWhat:&r the Undergarden's carrot on a stick. Hold it while riding a dweller to steer it.",
        "&eHow:&r a stick and underbeans, shapeless.",
        "&eTip:&r a ridden dweller carries you over long cavern floors without tiring your hunger bar as fast as sprinting."]),
    Q("ug_stews", 2, 6, [item(UG + "bloody_stew"), item(UG + "indigo_stew"), item(UG + "inky_stew"), item(UG + "veiled_stew")], "Four Stews",
      deps=["ug_mushrooms"], xp=100, optional=True, tokens=1, subtitle="Optional: a stew from every mushroom", desc=[
        "&eWhat:&r each mushroom (blood, indigo, ink and veil) cooks into its own stew.",
        "&eChemistry:&r the Dissolver breaks Undergarden mushrooms into chitin and phosphoric acid (H₃PO₄); phosphate is how cells store energy, as ATP.",
        "&eHow:&r a bowl and the mushrooms (check JEI); the mushroom bogs have all four kinds nearby."]),
    Q("ug_pie", 6, 6, [item(UG + "gloomgourd_pie", 2)], "Gloomgourd Pie", deps=["ug_gloomgourd"], xp=75,
      optional=True, tokens=1, subtitle="Optional: gourd, mushroom and glitterkelp", desc=[
        "&eWhat:&r the Undergarden's best plain food.",
        "&eHow:&r a gloomgourd, any Undergarden mushroom and a glitterkelp from the seas, shapeless.",
        "&eTip:&r glitterkelp also smelts into ordinary dried kelp."]),
    Q("ug_boomgourd", 0, 0, [item(UG + "boomgourd", 4)], "Demolition Gourds", deps=["ug_blisterbomb"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a stack of explosive gourds", desc=[
        "&eWhat:&r four boomgourds, for clearing caverns the loud way.",
        "&eHow:&r eight blisterbombs around a gloomgourd, four times over (check JEI).",
        "&eTip:&r keep them well away from your base."]),
], links=[("t4_undergarden", -2, 0)], mirror="undergarden")
