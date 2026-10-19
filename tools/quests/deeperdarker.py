"""Quest chapter: deeperdarker (Deeper and Darker: the Otherside). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The Ancient City, the Warden, the portal (w_otherside), reinforced echo shards (w_echo), the Ancient Temple (wd_temple),
three biomes, the soul elytra and the Warden chestplate are in worlds.py; sculk/shattered/stalker hunts are in
hunting.py; the four-biome tour is in completionist.py. This page adds the rest. Prefix dd_.
Layout: y=0 the resonarium line; y=2 the Warden line; y=-2 soul materials and the temple's prizes;
y=-4 plants and light (optional); y=4 creatures and curiosities (optional).
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

DD = "deeperdarker:"

CHAPTER = Chapter("deeperdarker", "Deeper and Darker", "deeperdarker:warden_carapace",
        ["The Otherside: a silent world of sculk beneath the Ancient City."], SIDE, [
    # --- the resonarium line (y=0) -------------------------------------------------------------
    Q("dd_stones", 0, 0, [item(DD + "sculk_stone", 32), item(DD + "gloomslate", 32)], "Sculk Stone and Gloomslate", deps=["w_otherside"], xp=100,
      subtitle="The bedrock of the Otherside", desc=[
        "&6You remember this silence. Every footstep here used to be yours.&r",
        "&eWhat:&r the Otherside's two stones. Both carry their own versions of the usual ores: coal, iron, copper, gold, redstone, lapis, emerald and diamond.",
        "&eChemistry:&r real slate is a metamorphic rock: shale (mostly clay minerals) squeezed and heated until its grains line up, so it splits into flat sheets.",
        "&eHow:&r mine it and smelt the cobbled forms back into smooth stone.",
        "&eTip:&r these ores go through the Create crusher too, with the same pack caps as Overworld ore."]),
    Q("dd_sludge", 2, 0, [kill(DD + "sludge", 5), item(DD + "resonarium", 8)], "Resonarium", deps=["dd_stones"], xp=150,
      loot="hunt", subtitle="Sludges carry a ringing metal", desc=[
        "&eWhat:&r resonarium is a vibration-tuned material that drops from sludges, oozing creatures of the Otherside.",
        "&eHow:&r hunt sludges in the Otherside's caves and collect the resonarium they drop.",
        "&eTip:&r a Looting sword raises the drop count."]),
    Q("dd_plate", 4, 0, [item(DD + "resonarium_plate", 2)], "Resonarium Plate", deps=["dd_sludge"], xp=150,
      subtitle="Resonarium bound with scutes", desc=[
        "&eWhat:&r the plate that upgrades diamond gear to resonarium.",
        "&eChemistry:&r turtle and armadillo scutes are built on keratin, the tough protein of hair, horn and hooves; its sulfur bridges (cysteine disulfides) make it hard.",
        "&eHow:&r four resonarium and four scutes (turtle or armadillo, any mix), shapeless."]),
    Q("dd_res_template", 6, 0, [item(DD + "resonarium_upgrade_smithing_template")], "Resonarium Template", deps=["dd_plate"], xp=150,
      subtitle="The smithing pattern for resonarium", desc=[
        "&eWhat:&r the smithing template that turns diamond gear into resonarium gear.",
        "&eHow:&r loot it from Ancient City chests, Trial Chamber reward chests, stronghold corridors or the Ancient Temple's top chest.",
        "&eTip:&r copy it with 7 diamonds and a resonarium (makes 2). Never use your last one."]),
    Q("dd_res_gear", 8, 0, [item(DD + "resonarium_pickaxe"), item(DD + "resonarium_chestplate")], "Resonarium Gear", deps=["dd_res_template"], xp=250,
      size=1.5, shape="hexagon", subtitle="Diamond gear, retuned", desc=[
        "&6Stone that sings when struck. You remember tuning it to your own voice.&r",
        "&eWhat:&r resonarium tools and armour: an upgrade over diamond that doesn't need netherite.",
        "&eHow:&r smithing table: resonarium template + diamond tool or armour piece + resonarium plate.",
        "&eTip:&r the rest of the set (axe, shovel, hoe, sword, helmet, leggings, boots) uses the same recipe."]),

    # --- the Warden line (y=2) -----------------------------------------------------------------
    Q("dd_carapace", 0, 2, [item(DD + "warden_carapace", 6)], "Warden Carapace", deps=["wd_warden"], xp=150,
      subtitle="The shell of the blind guardian", desc=[
        "&eWhat:&r every Warden drops one to three carapace pieces (and its heart). The carapace is the core of reinforced echo shards.",
        "&eHow:&r kill Wardens, or loot Ancient City chests and the Ancient Temple.",
        "&eTip:&r one reinforced echo shard takes four carapace, four phantom membranes and an echo shard. Plan your Warden fights."]),
    Q("dd_compass", 2, 3, [item(DD + "ancient_compass")], "Ancient Compass", deps=["dd_carapace"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a needle that seeks the temple", desc=[
        "&eWhat:&r a compass wrapped in Warden carapace. In the Otherside it points toward the nearest Ancient Temple.",
        "&eChemistry:&r an ordinary compass needle is magnetised iron or steel lining up with Earth's magnetic field.",
        "&eHow:&r a compass with four Warden carapace around it."]),
    Q("dd_warden_template", 4, 2, [item(DD + "warden_upgrade_smithing_template")], "Warden Template", deps=["dd_carapace"], xp=150,
      subtitle="The smithing pattern beyond netherite", desc=[
        "&eWhat:&r the template that upgrades netherite gear to Warden gear.",
        "&eHow:&r loot it from Ancient City chests (often) or the Ancient Temple's secret chest.",
        "&eTip:&r copy it with 7 diamonds and a sculk block (makes 2)."]),
    Q("dd_warden_tools", 6, 2, [item(DD + "warden_sword"), item(DD + "warden_pickaxe")], "Warden Tools", deps=["dd_warden_template"], xp=300,
      subtitle="Netherite, reinforced with echoes", desc=[
        "&eWhat:&r the Otherside's best tools and weapons.",
        "&eHow:&r smithing table: Warden template + netherite tool + reinforced echo shard (see Echoes of the Deep on the Other Worlds page).",
        "&eTip:&r echo shards also come from the Demigod Token shop (check JEI) if Ancient City chests run dry."]),
    Q("dd_warden_set", 8, 2, [item(DD + "warden_helmet"), item(DD + "warden_leggings"), item(DD + "warden_boots")], "Cover Me with Sculk",
      deps=["dd_warden_tools"], xp=400, optional=True, tokens=2, loot="boss", size=1.5, shape="gear",
      subtitle="Optional: the rest of the Warden armour", desc=[
        "&6The guardian's shell, worn by the one it guarded against. You remember that joke.&r",
        "&eWhat:&r helmet, leggings and boots of Warden armour, to go with the chestplate.",
        "&eHow:&r the same smithing recipe on netherite armour: one template and one reinforced echo shard per piece.",
        "&eTip:&r that's three more Wardens' worth of carapace, at least."]),

    # --- soul materials and temple prizes (y=-2) -----------------------------------------------
    Q("dd_transmitter", 0, -2, [item(DD + "sculk_transmitter")], "Sculk Transmitter", deps=["wd_temple"], xp=150,
      subtitle="Open a chest from far away", desc=[
        "&eWhat:&r a handheld sculk link. Link it to a container, and it opens that container from a distance.",
        "&eHow:&r found in the Ancient Temple's secret chest. Use it on a chest to link it, then use it anywhere to open that chest.",
        "&eTip:&r dye it to tell several apart; each colour is its own item."]),
    Q("dd_soul", 2, -2, [item(DD + "soul_dust", 8), item(DD + "soul_crystal", 2), item(DD + "sculk_bone", 4)], "Soul Materials", deps=["dd_stones"], xp=150,
      subtitle="Dust, crystal and bone", desc=[
        "&eWhat:&r the Otherside's crafting drops: soul dust (snappers, leeches), soul crystals (stalkers) and sculk bones (shattered).",
        "&eHow:&r hunt in the Otherside; the Ancient Temple's chests hold some of each too.",
        "&eTip:&r the Monster Hunting page has quests for these mobs, so do both at once."]),
    Q("dd_staff", 4, -2, [item(DD + "sonorous_staff")], "Sonorous Staff", deps=["dd_soul"], xp=250,
      subtitle="Borrow the Warden's voice", desc=[
        "&eWhat:&r a staff that charges and releases a sonic boom, the Warden's own attack.",
        "&eChemistry:&r sound is a pressure wave: molecules bunch up and spread apart. A shock wave is a pressure jump so steep it travels faster than sound itself.",
        "&eHow:&r a Heart of the Deep, two soul crystals and two sculk bones (check JEI). Repair it with soul crystals.",
        "&eTip:&r the Volume and Reverberation enchantments raise its damage and range."]),
    Q("dd_soundproof", 6, -2, [item(DD + "soundproof_glass", 8)], "Soundproof Glass", deps=["dd_soul"], xp=100,
      optional=True, tokens=1, subtitle="Optional: glass the sculk can't hear through", desc=[
        "&eWhat:&r glass that blocks vibrations, so sculk sensors (and Wardens) can't hear you through it.",
        "&eChemistry:&r sound needs a medium. Damping materials turn the wave's energy into heat; a vacuum stops it completely.",
        "&eHow:&r four soul dust around one glass makes two."]),

    # --- plants and light (y=-4, optional) -----------------------------------------------------
    Q("dd_echo_wood", 0, -4, [item(DD + "echo_log", 16), item(DD + "echo_sapling")], "Echo Trees", deps=["dd_stones"], xp=75,
      optional=True, tokens=1, subtitle="Optional: wood from the echoing forest", desc=[
        "&eWhat:&r pale echo trees grow on echo soil in the echoing forest. Their wood is found nowhere else.",
        "&eChemistry:&r all wood is the same chemistry: cellulose fibres glued by lignin, an aromatic polymer that makes trees rigid.",
        "&eHow:&r cut a few trees; leaves drop saplings."]),
    Q("dd_blooming", 2, -4, [item(DD + "blooming_stem", 16), item(DD + "bloom_berries", 8)], "Blooming Caverns", deps=["dd_stones"], xp=75,
      optional=True, tokens=1, subtitle="Optional: stems and berries from the caverns", desc=[
        "&eWhat:&r the blooming caverns grow tall blooming stems (a second Otherside wood) and edible bloom berries.",
        "&eHow:&r cut the stems and pick the berries in the blooming caverns.",
        "&eTip:&r bloom berries are the easiest food to find down here."]),
    Q("dd_gleam", 4, -4, [item(DD + "gloomslate_light", 4)], "Light in the Dark", deps=["dd_stones"], xp=75,
      optional=True, tokens=1, subtitle="Optional: gloomslate lights", desc=[
        "&eWhat:&r sculk gleam is the Otherside's glowing block; set in gloomslate it makes a tidy lamp.",
        "&eChemistry:&r a glow stick makes cold light by chemiluminescence: hydrogen peroxide oxidises an oxalate ester, and the energy excites a dye that emits light.",
        "&eHow:&r one sculk gleam with four gloomslate around it."]),
    Q("dd_amber", 6, -4, [item(DD + "crystallized_amber")], "Crystallized Amber", deps=["dd_stones"], xp=100,
      optional=True, tokens=1, subtitle="Optional: something is trapped inside", desc=[
        "&eWhat:&r amber blocks in the Otherside hold an item, or a live sculk leech. Break one to find out which.",
        "&eChemistry:&r real amber is fossilised tree resin: terpenes that slowly polymerised over millions of years, sometimes around an insect.",
        "&eHow:&r look in the Otherside's caves; the tooltip shows what's inside.",
        "&eTip:&r a leech pops out when you break the block. Be ready."]),

    # --- creatures and curiosities (y=4, optional) ---------------------------------------------
    Q("dd_angler", 0, 4, [kill(DD + "angler_fish", 3), item(DD + "cooked_angler_fish", 3)], "Angler Fish", deps=["dd_stones"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: a fish with its own lamp", desc=[
        "&eWhat:&r the Otherside's waters hide angler fish, a good food once cooked.",
        "&eChemistry:&r a real anglerfish's lure glows because of symbiotic bacteria living in it, which produce light by bioluminescence.",
        "&eHow:&r catch or kill them in Otherside water, then smelt or campfire-cook."]),
    Q("dd_leech", 2, 4, [kill(DD + "sculk_leech", 5), kill(DD + "shriek_worm")], "Leeches and Worms", deps=["dd_stones"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: the smaller horrors", desc=[
        "&eWhat:&r sculk leeches latch on in swarms; the shriek worm bursts from the ground.",
        "&eHow:&r leeches hide in crystallized amber and in caves; shriek worms burst out of the Otherside's ground.",
        "&eTip:&r a sweeping sword handles a leech swarm best."]),
    Q("dd_sherds", 4, 4, [anyof([DD + "gloomsherd", DD + "brittle_gloomsherd", DD + "dark_heart_gloomsherd", DD + "listener_gloomsherd",
                                  DD + "snapper_gloomsherd", DD + "temple_gloomsherd", DD + "transmission_gloomsherd", DD + "ward_gloomsherd",
                                  DD + "wayfinder_gloomsherd"], 3)], "Gloomsherds", deps=["dd_stones"], xp=100,
      optional=True, tokens=1, subtitle="Optional: pottery of the old city", desc=[
        "&eWhat:&r pottery sherds from the Otherside's makers. They decorate gloomslate pots, like vanilla sherds on decorated pots.",
        "&eChemistry:&r firing clay drives out water and partly melts its silicates into glass, which is why fired pottery survives for millennia.",
        "&eHow:&r collect any three. Amber blocks and the strange pots of the Otherside carry them."]),
    Q("dd_pot", 6, 4, [kill(DD + "anger_pot")], "That Pot Moved", deps=["dd_stones"], xp=100,
      secret=True, loot="secret", subtitle="Secret: not every pot is a pot", desc=[
        "&eWhat:&r some pots in the Otherside are alive: anger, sorrow and fear pots. You broke an angry one.",
        "&eTip:&r they drop gloomsherds, so a living pot is worth chasing."]),
    Q("dd_grime", 8, 4, [item(DD + "grime_brick", 8)], "Grime Bricks", deps=["dd_stones"], xp=75,
      optional=True, tokens=1, subtitle="Optional: bricks fired from sculk grime", desc=[
        "&eWhat:&r grime balls fire into grime bricks, a building block made from the Otherside's mud.",
        "&eChemistry:&r brick-making is old chemistry: heating clay above about 900 °C sinters its particles together into a hard ceramic.",
        "&eHow:&r smelt grime balls (Ancient Temple chests hold them). Four grime balls also make a block of sculk grime."]),
], links=[("w_otherside", -2, 0), ("wd_warden", -2, 2), ("wd_temple", -2, -2)])
