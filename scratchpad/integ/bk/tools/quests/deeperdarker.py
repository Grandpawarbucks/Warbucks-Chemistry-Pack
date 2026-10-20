"""Quest chapter: deeperdarker (Deeper and Darker: the Deep Dark and the Otherside). See tools/quests/STYLE.md.
Build: python3 tools/build_quests.py

Mirrors ATM10's Deeper and Darker chapter quest for quest (its list, order, sections and requirements only; ATM10's
book is All Rights Reserved, so every word here is our own). Each mirrored quest carries mirror="<ATM10 quest id>".
The Deep Dark quests that used to sit on the Other Worlds page (w_ancient, wd_warden, w_otherside, w_echo, wd_temple,
wd_otherside_biomes, w_soul_elytra, w_warden_armor) live here now, keys unchanged. Sculk/shattered/stalker hunts stay
on the Bounty Board (hunting.py); the four-biome tour is in completionist.py. New quests use the prefix dd_.
Skipped ATM10 quests (FTB "observation" tasks with no natural item to hold): the gloomy geyser, the sculk jaw and the
temple's reinforced deepslate. Our own quests that ATM10 doesn't have (the resonarium line and more) are optional.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

DD = "deeperdarker:"
DEEP, BLOOM, ECHO, OVER = "dd_bi_deeplands", "dd_bi_blooming", "wd_otherside_biomes", "dd_bi_overcast"

# --- the Otherside's creatures (ATM10's right-hand block: one kill each) ------------------------------------------
_KILLS = [
    # key, entity, ATM10 id, deps, title, subtitle, what, how, tip
    ("dd_k_shattered", "shattered", "5E287410EE969244", [DEEP, ECHO], "Shattered", "A skeleton held together by sculk",
     "the Shattered are sculk-bound husks that hunt by sound. They drop sculk bones.",
     "find them in the deeplands and the echoing forest.",
     "sneak: like the Warden, they listen more than they look."),
    ("dd_k_centipede", "sculk_centipede", "60721C9B94B36C24", [DEEP, ECHO], "Sculk Centipede", "Too many legs",
     "a long sculk creature that skitters through the Otherside's caves.",
     "find one in the deeplands or the echoing forest and bring it down.",
     "the Bounty Board has a bigger hunt for centipedes and snappers."),
    ("dd_k_snapper", "sculk_snapper", "736F4A43EEBDD7B3", [DEEP, BLOOM], "Sculk Snapper", "Jaws in the sculk",
     "sculk snappers are biting sculk beasts. They drop soul dust.",
     "find them in the deeplands and the blooming caverns.",
     "soul dust makes soundproof glass; keep what they drop."),
    ("dd_k_shriek_worm", "shriek_worm", "774D61FEFABEFD9A", [DEEP], "Shriek Worm", "It bursts out of the ground",
     "the shriek worm erupts from the Otherside's ground without warning.",
     "it lives under the deeplands. Keep moving, and hit it when it surfaces.",
     "don't fight it where you can't see the floor."),
]

# --- single blocks and plants (ATM10's top and bottom rows) --------------------------------------------------------
_PLANTS = [
    # key, item, ATM10 id, deps, title, what, how
    ("dd_gloomslate", "cobbled_gloomslate", "716FF64ACF896D50", [OVER], "Gloomslate",
     "the Otherside's second stone, the rock of the overcast columns.",
     "mine gloomslate; it breaks into cobbled gloomslate. Smelt it back into smooth gloomslate."),
    ("dd_bloom_berries", "bloom_berries", "21398F45428CD1D1", [BLOOM], "Bloom Berries",
     "edible berries from the blooming caverns, the easiest food to find down here.",
     "pick them from the blooming plants in the caverns."),
    ("dd_sculk_vines", "sculk_vines", "72EC845C19645AFC", [BLOOM, DEEP], "Sculk Vines",
     "vines of sculk that hang from the Otherside's ceilings.",
     "cut them down in the deeplands or the blooming caverns."),
    ("dd_ice_lily", "ice_lily", "36149E69A8C264E4", [BLOOM], "Ice Lily",
     "a pale flower of the blooming caverns.",
     "pick one where it grows in the caverns."),
    ("dd_moss", "blooming_moss_block", "44F9B8F285546B2C", [BLOOM], "Blooming Moss",
     "the moss that carpets the blooming caverns.",
     "dig up a block of it."),
    ("dd_cactus", "gloomy_cactus", "201E3E41018F9521", [OVER], "Gloomy Cactus",
     "a cactus that grows among the gloomy sculk of the overcast columns.",
     "break one off where it grows."),
    ("dd_tendrils", "sculk_tendrils", "0850F88E2205623F", [DEEP], "Sculk Tendrils",
     "sculk tendrils grow up from the deeplands' floor.",
     "cut a few where they grow."),
]

_BIOMES = [
    # key, biome, ATM10 id, title, what
    ("dd_bi_blooming", "blooming_caverns", "68446510A1B0D9B8", "The Blooming Caverns",
     "caverns lit by blooming plants: stems, berries, ice lilies and glowing roots."),
    ("dd_bi_deeplands", "deeplands", "0450060852F290CA", "The Deeplands",
     "the Otherside's dark heartland of sculk, and the way to the Ancient Temple."),
    ("dd_bi_overcast", "overcast_columns", "3CF2DFB7F0CE065B", "The Overcast Columns",
     "towering columns of gloomslate, the Otherside's second stone."),
]


def _kill_quests():
    return [Q(key, 0, 0, [kill(DD + ent)], title, deps=deps, xp=100, loot="hunt", mirror=mir, section="Creatures of the Otherside",
              subtitle=sub, desc=["&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip])
            for key, ent, mir, deps, title, sub, what, how, tip in _KILLS]


def _plant_quests():
    return [Q(key, 0, 0, [item(DD + it)], title, deps=deps, xp=40, mirror=mir, section="Stone and Growth",
              subtitle="One " + title.lower(), desc=["&eWhat:&r " + what, "&eHow:&r " + how])
            for key, it, mir, deps, title, what, how in _PLANTS]


def _biome_quests():
    return [Q(key, 0, 0, [biome(DD + b)], title, deps=["w_otherside"], xp=100, size=1.5, mirror=mir, section="Regions of the Otherside",
              subtitle="Walk into " + title[0].lower() + title[1:], desc=["&eWhat:&r " + what,
                                                                          "&eHow:&r Nature's Compass works in the Otherside. Walk in."])
            for key, b, mir, title, what in _BIOMES]


CHAPTER = Chapter("deeperdarker", "Deeper and Darker", "deeperdarker:warden_carapace",
        ["The Deep Dark and the Otherside: a silent world of sculk beneath the Ancient City."], SIDE, [
    # ============================ the way in (ATM10: city, Warden, heart, portal) ============================
    Q("dd_guide", 0, 0, [tick()], "Quiet, Please", deps=[], xp=10, optional=True, tokens=0, mirror="01ECFBB5F0574C24",
      icon="minecraft:sculk_sensor", subtitle="How sound works down here", desc=[
        "&eWhat:&r everything in the Deep Dark and the Otherside hears you. Sculk sensors pick up footsteps, and shriekers call the Warden.",
        "&eHow:&r sneak everywhere. Sneaking never triggers sculk sensors, and walking on wool doesn't either.",
        "&eTip:&r click the checkmark once you've read this."]),
    Q("w_ancient", 0, 3.5, [structure("minecraft:ancient_city")], "An Ancient City", deps=["t2_nether"], xp=150,
      mirror="0B11EAB8D76529E0", section="The Way Down", subtitle="Find the city beneath the deep dark", desc=[
        "&6You remember a silence older than the world. You can hear it again.&r",
        "&eWhat:&r Ancient Cities sit deep below the Overworld in the deep dark. Each one's centre holds the frame of a portal to the Otherside.",
        "&eHow:&r the Explorer's Compass can find one. Sneak in and stand inside the city.",
        "&eTip:&r shriekers summon the Warden; break them quietly or go around."]),
    Q("wd_warden", 2, 3.5, [kill("minecraft:warden")], "The Warden", deps=["w_ancient"], xp=300,
      loot="boss", mirror="3D579A1F7EFEDD5C", subtitle="Kill the blind guardian of the deep", desc=[
        "&eWhat:&r the Warden is the strongest regular mob in the game, and the key to the Otherside: with Deeper and Darker it drops the Heart of the Deep.",
        "&eHow:&r trigger shriekers three times to summon one (or let it find you). Fight from range; it's blind and tracks you by sound and smell.",
        "&eTip:&r its sonic boom goes through shields and armour. Break line of sight when it starts charging."]),
    Q("dd_heart", 0, 0, [item(DD + "heart_of_the_deep")], "Heart of the Deep", deps=["wd_warden"], xp=200, mirror="6E38CF6E7360E9CA",
      subtitle="The Warden's heart, still beating", desc=[
        "&eWhat:&r the Heart of the Deep drops from the Warden. It lights the portal in an Ancient City's centre.",
        "&eHow:&r beat a Warden and pick up the heart.",
        "&eTip:&r it's also the core of the Sonorous Staff, so a second heart is worth having."]),
    Q("w_otherside", 4, 3.5, [dim(DD + "otherside")], "The Otherside", deps=["dd_heart"], xp=300, size=2.0,
      mirror="76F14C2B866B4EAD", subtitle="Light the portal and step through", desc=[
        "&6Every footstep here used to be yours. You remember walking these halls without a sound.&r",
        "&eWhat:&r beyond the Ancient City lies the Otherside, a dark dimension of sculk, echo trees and gloomslate.",
        "&eHow:&r use the Heart of the Deep on the portal frame in the city's centre, then step through.",
        "&eTip:&r the Otherside is as quiet as the city. Keep sneaking."]),

    # ============================ the four regions ============================
    Q("wd_otherside_biomes", 6, 5.5, [biome(DD + "echoing_forest")], "The Echoing Forest", deps=["w_otherside"], xp=100, size=1.5,
      mirror="59AF80E8EE17C769", section="Regions of the Otherside", subtitle="Walk into the echoing forest", desc=[
        "&eWhat:&r a forest of pale echo trees growing on echo soil.",
        "&eChemistry:&r there's no sunlight down here; real cave and deep-sea ecosystems run on chemosynthesis, where microbes get energy by oxidising H₂S or CH₄ instead of from light.",
        "&eHow:&r Nature's Compass works in the Otherside. Walk in."]),
    *_biome_quests(),

    # ============================ Warden gear (ATM10's left-hand block) ============================
    Q("dd_warden_template", 4, 2, [item(DD + "warden_upgrade_smithing_template")], "Warden Template", deps=["w_otherside", "w_ancient"], xp=150,
      mirror="196003E1486ABB31", section="Warden Gear", subtitle="The smithing pattern beyond netherite", desc=[
        "&eWhat:&r the template that upgrades netherite gear to Warden gear.",
        "&eHow:&r loot it from Ancient City chests (often) or the Ancient Temple's secret chest.",
        "&eTip:&r copy it with 7 diamonds and a sculk block (makes 2). Never use your last one."]),
    Q("w_echo", 6, 3.5, [item(DD + "reinforced_echo_shard")], "Echoes of the Deep", deps=["w_otherside", "wd_warden"], xp=200,
      mirror="45C9D975E3731DFE", section="Warden Gear", subtitle="The Otherside's strongest material", desc=[
        "&eWhat:&r reinforced echo shards make Warden gear that rivals netherite.",
        "&eHow:&r four Warden carapace, four phantom membranes and an echo shard (check JEI). Echo shards come from Ancient City chests and Otherside loot.",
        "&eTip:&r every piece of Warden gear takes one shard, so plan your Warden fights."]),
    Q("dd_warden_tools", 6, 2, [anyof([DD + "warden_sword", DD + "warden_axe"])], "A Warden Blade", deps=["dd_warden_template", "w_echo"], xp=300,
      mirror="7CBAA67204CC258C", subtitle="A sword or an axe beyond netherite", desc=[
        "&eWhat:&r a Warden sword or axe: the Otherside's best weapons.",
        "&eHow:&r smithing table: Warden template + netherite sword or axe + reinforced echo shard.",
        "&eTip:&r echo shards also come from the Demigod Token shop (check JEI) if Ancient City chests run dry."]),
    Q("dd_warden_digging", 0, 0, [anyof([DD + "warden_pickaxe", DD + "warden_shovel", DD + "warden_hoe"])], "A Warden Tool",
      deps=["dd_warden_template", "w_echo"], xp=300, mirror="726A627BD7654E0C", subtitle="A pickaxe, shovel or hoe beyond netherite", desc=[
        "&eWhat:&r a Warden pickaxe, shovel or hoe.",
        "&eHow:&r smithing table: Warden template + netherite tool + reinforced echo shard."]),
    Q("w_warden_armor", 8, 3.5, [item(DD + "warden_helmet"), item(DD + "warden_chestplate"), item(DD + "warden_leggings"), item(DD + "warden_boots")],
      "Warden Armour", deps=["dd_warden_template", "w_echo"], xp=400, mirror="6E901EF1CB411088",
      subtitle="Beyond netherite, head to toe", desc=[
        "&6The guardian's shell, worn by the one it guarded against. You remember that joke.&r",
        "&eWhat:&r the full set of Warden armour, tougher than netherite.",
        "&eHow:&r smithing table: Warden template + netherite armour piece + reinforced echo shard, once per piece.",
        "&eTip:&r that's four shards: four Wardens' worth of carapace, at least."]),
    Q("w_soul_elytra", 8, 1.5, [item(DD + "soul_elytra")], "Soul Elytra", deps=["dd_pot", "dd_k_shattered", "dd_k_snapper"], xp=250,
      mirror="4A01C5F5DCF32C19", subtitle="An elytra with its own boost", desc=[
        "&eWhat:&r an upgraded elytra that boosts itself, no rockets needed.",
        "&eHow:&r an elytra (End Cities), sculk bones (from Shattered), a soul crystal (from Stalkers) and soul dust (check JEI).",
        "&eTip:&r Stalkers and Shattered roam the Otherside; fight them at range."]),
    Q("dd_staff", 4, -2, [item(DD + "sonorous_staff")], "Sonorous Staff", deps=["dd_pot", "dd_k_shattered", "dd_k_snapper"], xp=250,
      mirror="13B338F377951032", subtitle="Borrow the Warden's voice", desc=[
        "&eWhat:&r a staff that charges and releases a sonic boom, the Warden's own attack.",
        "&eChemistry:&r sound is a pressure wave: molecules bunch up and spread apart. A shock wave is a pressure jump so steep it travels faster than sound itself.",
        "&eHow:&r a Heart of the Deep, two soul crystals and two sculk bones (check JEI). Repair it with soul crystals.",
        "&eTip:&r the Volume and Reverberation enchantments raise its damage and range."]),

    # ============================ the Ancient Temple ============================
    Q("wd_temple", 4, 5.5, [structure(DD + "ancient_temple")], "The Ancient Temple", deps=[DEEP], xp=250,
      mirror="35629CB10DBDE340", section="The Ancient Temple", subtitle="A temple deep in the Otherside", desc=[
        "&eWhat:&r the Otherside's great structure: a sculk-choked temple with traps and the best loot in the dimension.",
        "&eHow:&r it stands in the deeplands; the Ancient Compass or the Explorer's Compass points the way. Step inside.",
        "&eTip:&r the temple is full of sculk; sneak, as you did in the Ancient City."]),
    Q("dd_transmitter", 0, -2, [item(DD + "sculk_transmitter")], "Sculk Transmitter", deps=["wd_temple"], xp=150,
      mirror="7FF3EA602FE7A546", subtitle="Open a chest from far away", desc=[
        "&eWhat:&r a handheld sculk link. Link it to a container, and it opens that container from a distance.",
        "&eHow:&r found in the Ancient Temple's secret chest. Use it on a chest to link it, then use it anywhere to open that chest.",
        "&eTip:&r dye it to tell several apart; each colour is its own item."]),
    Q("dd_pot", 6, 4, [kill(DD + "anger_pot")], "That Pot Moved", deps=["wd_temple"], xp=150, loot="hunt",
      mirror="4D57A07592AED307", subtitle="Not every pot is a pot", desc=[
        "&eWhat:&r some of the Otherside's pots are alive: anger, sorrow and fear pots. Break one that fights back.",
        "&eHow:&r the temple's halls are lined with pots. Smash them until one turns on you, then finish it.",
        "&eTip:&r living pots drop gloomsherds, so they're worth chasing."]),
    Q("dd_leech", 2, 4, [kill(DD + "sculk_leech")], "Sculk Leech", deps=["wd_temple"], xp=100, loot="hunt",
      mirror="5866438E5D19AB69", subtitle="Small, and never alone", desc=[
        "&eWhat:&r sculk leeches latch on in swarms and drop soul dust.",
        "&eHow:&r leeches hide in crystallized amber and in the temple's halls.",
        "&eTip:&r a sweeping sword handles a leech swarm best."]),

    # ============================ creatures ============================
    Q("dd_sludge", 2, 0, [kill(DD + "sludge"), item(DD + "resonarium", 8)], "Sludge", deps=[BLOOM], xp=150,
      loot="hunt", mirror="10E025288BB00657", section="Creatures of the Otherside", subtitle="An ooze with a ringing metal inside", desc=[
        "&eWhat:&r sludges are oozing creatures of the blooming caverns. They drop resonarium, a vibration-tuned material.",
        "&eHow:&r hunt sludges and collect 8 resonarium from them.",
        "&eTip:&r a Looting sword raises the drop count."]),
    Q("dd_angler", 0, 4, [kill(DD + "angler_fish"), item(DD + "cooked_angler_fish", 3)], "Angler Fish", deps=[BLOOM], xp=100,
      loot="hunt", mirror="16A2CC83C99B1F86", subtitle="A fish with its own lamp", desc=[
        "&eWhat:&r the Otherside's waters hide angler fish, a good food once cooked.",
        "&eChemistry:&r a real anglerfish's lure glows because of symbiotic bacteria living in it, which produce light by bioluminescence.",
        "&eHow:&r catch or kill them in the blooming caverns' water, then smelt or campfire-cook three."]),
    *_kill_quests(),
    Q("dd_soundproof", 6, -2, [item(DD + "soundproof_glass")], "Soundproof Glass", deps=["dd_k_snapper"], xp=100,
      mirror="78BCED8699ADEDF4", subtitle="Glass the sculk can't hear through", desc=[
        "&eWhat:&r glass that blocks vibrations, so sculk sensors (and Wardens) can't hear you through it.",
        "&eChemistry:&r sound needs a medium. Damping materials turn the wave's energy into heat; a vacuum stops it completely.",
        "&eHow:&r four soul dust (snappers drop it) around one glass makes two."]),

    # ============================ stone and growth ============================
    Q("dd_blooming", 2, -4, [item(DD + "blooming_stem"), item(DD + "bloom_berries")], "Blooming Stems", deps=[BLOOM], xp=50,
      mirror="183F6A790EC006B8", section="Stone and Growth", subtitle="The caverns' second wood", desc=[
        "&eWhat:&r the blooming caverns grow tall blooming stems (a second Otherside wood) hung with bloom berries.",
        "&eHow:&r cut a stem and pick a berry in the blooming caverns."]),
    Q("dd_echo_wood", 0, -4, [item(DD + "echo_log"), item(DD + "echo_sapling")], "Echo Trees", deps=[ECHO], xp=50,
      mirror="0B718FC37699B822", subtitle="Wood from the echoing forest", desc=[
        "&eWhat:&r pale echo trees grow on echo soil in the echoing forest. Their wood is found nowhere else.",
        "&eChemistry:&r all wood is the same chemistry: cellulose fibres glued by lignin, an aromatic polymer that makes trees rigid.",
        "&eHow:&r cut a tree; its leaves drop saplings."]),
    Q("dd_stones", 0, 0, [item(DD + "cobbled_sculk_stone")], "Sculk Stone", deps=[DEEP, ECHO, BLOOM], xp=50,
      mirror="6BB948F44B0950E8", subtitle="The bedrock of the Otherside", desc=[
        "&eWhat:&r the Otherside's main stone. It carries its own versions of the usual ores: coal, iron, copper, gold, redstone, lapis, emerald and diamond.",
        "&eHow:&r mine sculk stone; it breaks into cobbled sculk stone. Smelt it back into smooth stone.",
        "&eTip:&r these ores go through the Create crusher too, with the same pack caps as Overworld ore."]),
    Q("dd_flora", 0, 0, [item(DD + "glowing_roots")], "Glowing Roots", deps=[BLOOM], xp=40, mirror="5CCF573B67317591",
      subtitle="Light that grows downward", desc=[
        "&eWhat:&r glowing roots hang in the blooming caverns.",
        "&eChemistry:&r real woods have a glow like this: foxfire, the faint green light of fungi in rotting wood, is bioluminescence from an enzyme oxidising a luciferin.",
        "&eHow:&r cut a root where it hangs."]),
    Q("dd_living_ground", 0, 0, [item(DD + "echo_soil")], "Echo Soil", deps=[ECHO], xp=40, mirror="1A2EA742FDED54FF",
      subtitle="The soil of the echoing forest", desc=[
        "&eWhat:&r echo soil lies under the echoing forest's trees, and echo trees only grow on it.",
        "&eChemistry:&r real soil is about half mineral grains, a quarter water and a quarter air, plus a few percent organic matter that holds most of its nutrients.",
        "&eHow:&r dig some up in the echoing forest.",
        "&eTip:&r bring some home with your saplings."]),
    Q("dd_sculk_gleam", 0, 0, [item(DD + "sculk_gleam")], "Sculk Gleam", deps=[ECHO], xp=40, mirror="1BFE6745F49B4AB0",
      subtitle="The Otherside's own lamps", desc=[
        "&eWhat:&r glowing sculk growths that light the deeplands and the echoing forest.",
        "&eChemistry:&r a glow can be fluorescence (light given back at once, like a highlighter under UV) or phosphorescence (stored and released slowly, like glow-in-the-dark paint, often strontium aluminate).",
        "&eHow:&r mine sculk gleam where it grows.",
        "&eTip:&r it's the core of the gloomslate light."]),
    Q("dd_amber", 6, -4, [item(DD + "crystallized_amber")], "Crystallized Amber", deps=[OVER], xp=100, mirror="56D41A4605C42EB5",
      subtitle="Something is trapped inside", desc=[
        "&eWhat:&r amber blocks in the Otherside hold an item, or a live sculk leech. Break one to find out which.",
        "&eChemistry:&r real amber is fossilised tree resin: terpenes that slowly polymerised over millions of years, sometimes around an insect.",
        "&eHow:&r look in the Otherside's caves; the tooltip shows what's inside.",
        "&eTip:&r a leech pops out when you break the block. Be ready."]),
    Q("dd_grime_ball", 0, 0, [item(DD + "grime_ball")], "Grime Ball", deps=[DEEP], xp=50, mirror="39BED5DD9D24F98E",
      subtitle="Mud from the sculk patches", desc=[
        "&eWhat:&r sculk grime is a muddy block that forms in the Otherside's sculk patches. Mined without Silk Touch, it breaks into 2 to 4 grime balls.",
        "&eChemistry:&r mud is mostly clay minerals: sheets of aluminium silicate so thin they slide over each other when wet, which is why clay can be shaped.",
        "&eHow:&r mine sculk grime where sculk spreads; Ancient Temple chests hold grime balls too.",
        "&eTip:&r grime balls smelt into grime bricks."]),
    *_plant_quests(),

    # ============================ side quests (ours; ATM10 has no match) ============================
    Q("dd_plate", 4, 0, [item(DD + "resonarium_plate", 2)], "Resonarium Plate", deps=["dd_sludge"], xp=150, optional=True, tokens=1,
      subtitle="Optional: resonarium bound with scutes", desc=[
        "&eWhat:&r the plate that upgrades diamond gear to resonarium.",
        "&eChemistry:&r turtle and armadillo scutes are built on keratin, the tough protein of hair, horn and hooves; its sulfur bridges (cysteine disulfides) make it hard.",
        "&eHow:&r four resonarium and four scutes (turtle or armadillo, any mix), shapeless."]),
    Q("dd_res_template", 6, 0, [item(DD + "resonarium_upgrade_smithing_template")], "Resonarium Template", deps=["dd_plate"], xp=150,
      optional=True, tokens=1, subtitle="Optional: the smithing pattern for resonarium", desc=[
        "&eWhat:&r the smithing template that turns diamond gear into resonarium gear.",
        "&eHow:&r loot it from Ancient City chests, Trial Chamber reward chests, stronghold corridors or the Ancient Temple's top chest.",
        "&eTip:&r copy it with 7 diamonds and a resonarium (makes 2). Never use your last one."]),
    Q("dd_res_gear", 8, 0, [item(DD + "resonarium_pickaxe"), item(DD + "resonarium_chestplate")], "Resonarium Gear", deps=["dd_res_template"], xp=250,
      optional=True, tokens=2, subtitle="Optional: diamond gear, retuned", desc=[
        "&6Stone that sings when struck. You remember tuning it to your own voice.&r",
        "&eWhat:&r resonarium tools and armour: an upgrade over diamond that doesn't need netherite.",
        "&eHow:&r smithing table: resonarium template + diamond tool or armour piece + resonarium plate.",
        "&eTip:&r the rest of the set (axe, shovel, hoe, sword, helmet, leggings, boots) uses the same recipe."]),
    Q("dd_carapace", 0, 2, [item(DD + "warden_carapace", 6)], "Warden Carapace", deps=["wd_warden"], xp=150, optional=True, tokens=1,
      subtitle="Optional: the shell of the blind guardian", desc=[
        "&eWhat:&r every Warden drops one to three carapace pieces (and its heart). The carapace is the core of reinforced echo shards.",
        "&eHow:&r kill Wardens, or loot Ancient City chests and the Ancient Temple.",
        "&eTip:&r one reinforced echo shard takes four carapace, four phantom membranes and an echo shard. Plan your Warden fights."]),
    Q("dd_compass", 2, 3, [item(DD + "ancient_compass")], "Ancient Compass", deps=["dd_carapace"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a needle that seeks the temple", desc=[
        "&eWhat:&r a compass wrapped in Warden carapace. In the Otherside it points toward the nearest Ancient Temple.",
        "&eChemistry:&r an ordinary compass needle is magnetised iron or steel lining up with Earth's magnetic field.",
        "&eHow:&r a compass with four Warden carapace around it."]),
    Q("dd_warden_set", 8, 2, [item(DD + "warden_sword"), item(DD + "warden_axe"), item(DD + "warden_pickaxe"), item(DD + "warden_shovel"),
                              item(DD + "warden_hoe")], "Cover Me with Sculk",
      deps=["dd_warden_tools", "dd_warden_digging"], xp=400, optional=True, tokens=2, loot="boss",
      subtitle="Optional: every Warden tool and weapon", desc=[
        "&eWhat:&r all five Warden tools and weapons at once.",
        "&eHow:&r the same smithing recipe on each netherite tool: one template and one reinforced echo shard per piece.",
        "&eTip:&r that's five more Wardens' worth of carapace, at least."]),
    Q("dd_soul", 2, -2, [item(DD + "soul_dust", 8), item(DD + "soul_crystal", 2), item(DD + "sculk_bone", 4)], "Soul Materials", deps=["w_otherside"], xp=150,
      optional=True, tokens=1, subtitle="Optional: dust, crystal and bone", desc=[
        "&eWhat:&r the Otherside's crafting drops: soul dust (snappers, leeches), soul crystals (stalkers) and sculk bones (shattered).",
        "&eHow:&r hunt in the Otherside; the Ancient Temple's chests hold some of each too.",
        "&eTip:&r the Bounty Board has quests for these mobs, so do both at once."]),
    Q("dd_gleam", 4, -4, [item(DD + "gloomslate_light", 4)], "Light in the Dark", deps=["dd_sculk_gleam"], xp=75,
      optional=True, tokens=1, subtitle="Optional: gloomslate lights", desc=[
        "&eWhat:&r sculk gleam set in gloomslate makes a tidy lamp.",
        "&eChemistry:&r a glow stick makes cold light by chemiluminescence: hydrogen peroxide oxidises an oxalate ester, and the energy excites a dye that emits light.",
        "&eHow:&r one sculk gleam with four gloomslate around it."]),
    Q("dd_sherds", 4, 4, [anyof([DD + "gloomsherd", DD + "brittle_gloomsherd", DD + "dark_heart_gloomsherd", DD + "listener_gloomsherd",
                                  DD + "snapper_gloomsherd", DD + "temple_gloomsherd", DD + "transmission_gloomsherd", DD + "ward_gloomsherd",
                                  DD + "wayfinder_gloomsherd"], 3)], "Gloomsherds", deps=["dd_pot"], xp=100,
      optional=True, tokens=1, subtitle="Optional: pottery of the old city", desc=[
        "&eWhat:&r pottery sherds from the Otherside's makers. They decorate gloomslate pots, like vanilla sherds on decorated pots.",
        "&eChemistry:&r firing clay drives out water and partly melts its silicates into glass, which is why fired pottery survives for millennia.",
        "&eHow:&r collect any three. Amber blocks and the living pots of the Otherside carry them."]),
    Q("dd_grime", 8, 4, [item(DD + "grime_brick", 8)], "Grime Bricks", deps=["dd_grime_ball"], xp=75,
      optional=True, tokens=1, subtitle="Optional: bricks fired from sculk grime", desc=[
        "&eWhat:&r grime balls fire into grime bricks, a building block made from the Otherside's mud.",
        "&eChemistry:&r brick-making is old chemistry: heating clay above about 900 °C sinters its particles together into a hard ceramic.",
        "&eHow:&r smelt grime balls. Four grime balls also make a block of sculk grime."]),
], links=[("t2_nether", -2, 0)], mirror="deeper_and_darker")
