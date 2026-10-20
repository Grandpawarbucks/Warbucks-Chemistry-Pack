"""Quest chapter: generators. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Generators" chapter (Iron Furnaces and Generator Galore; user decision 2026-10-20: quest for quest
where we have the mod; the text is ours). Split out of power.py on 2026-10-20 (keys unchanged); every quest carries
its ATM10 id through GEN_MIRROR below.

ATM10 Generators quests skipped: the credits checkmark and "Rainbow Furnace" (a renamed vanilla item, not a real item).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
IF, GG = "ironfurnaces:", "generatorgalore:"
S_FURN, S_IF, S_RAINBOW, S_AUG, S_GG = "The Furnace", "Iron Furnaces", "The Rainbow Generator", "Furnace Augments", "Generator Galore"


# ATM10 "generators" quest id of each quest (set on the quests after the list is built).
GEN_MIRROR = {
    "pw_furnace": "47750F3CB020104C", "pw_if_iron": "2748ACEAB96A5F60", "pw_if_gold": "420FE84DEE12CCE0",
    "pw_if_diamond": "21EA29A8C7F950CE", "pw_if_emerald": "711DDD55CEC439E5", "pw_if_obsidian": "32C7D8AE859BF89E",
    "pw_if_crystal": "2354BC5330350DF6", "pw_if_copper": "661C072E48F8D41F", "pw_if_silver": "61847F47CCA225D9",
    "pw_gg_copper": "618F1434757C8E69", "pw_gg_iron": "61F265D9A5713A4D", "pw_gold_gen": "25A3E30F722B38B6",
    "pw_gg_culinary": "1C73E60FC70408D4", "pw_gg_collection": "28FEB4C11AD1AE7C", "pw_gg_netherite": "07BEB974DF1E5AD3",
    "pw_gg_gems": "076A648E3E3245C9", "pw_gg_obsidian": "311F43D48B9C26FF", "pw_gg_sweet": "68972BA647FDCF8F",
    "pw_gg_potion": "7297391D026EE9A6", "pw_gg_enchant": "6A1145678E80FB8E", "pw_gg_magmatic": "552CA2ABE659A507",
    "pw_gg_ender": "69201157ECFBB426", "pw_gg_star": "1843C79133DFB024", "pw_gg_halitosis": "40DB6E3DE87F16EF",
    "pw_if_netherite": "79C4CF8D7312FC28", "pw_if_augments": "78D1C97A542133D8", "pw_if_aug_blasting": "73FF01D830A669AA",
    "pw_if_aug_smoking": "33436ED0D9F128BD", "pw_if_aug_factory": "49F08DE190AAD0D8", "pw_if_aug_generator": "07753C5D94312A50",
    "pw_if_aug_speed": "7F67849DE9F700D8", "pw_if_aug_fuel": "538821E23E39BE97", "pw_if_spooky": "686B25F2E9D8CC97",
    "pw_if_xmas": "553220A2CD7CAFE4", "pw_if_heater": "20EC8001A05CE2C8", "pw_if_core": "7A615E2A152917AD",
    "pw_if_plating": "0AD2B11565B484E7", "pw_if_rainbow_coal": "062AA943A1629A86", "pw_if_copy": "757B14D08A9A03C4",
    "pw_if_rainbow": "0ADBE90B33ACC9FB", "pw_gg_8x": "7CE86300AF8E9BCA", "pw_gg_64x": "72A287DCAEEFE49F",
    "pw_if_atm": "3A4C17878FC8315B", "pw_if_vibranium": "2E85D6E2CFCC356E", "pw_if_unobtainium": "25080E3295B1DF01",
}

GG_8X = [GG + g + "_generator_8x" for g in ("copper", "diamond", "emerald", "enchantment", "ender", "gold", "halitosis", "honey",
                                            "iron", "magmatic", "netherite", "netherstar", "obsidian", "potion", "culinary")]
GG_64X = [GG + g + "_generator_64x" for g in ("culinary", "enchantment", "ender", "halitosis", "honey", "magmatic", "netherite",
                                              "netherstar", "potion")]
FURNACES = ["copper", "iron", "silver", "gold", "diamond", "emerald", "crystal", "obsidian", "netherite"]


def if_furnace(key, metal, deps, xp, what, how, tip, extra=None, **kw):
    """One Iron Furnaces tier: its own quest, in the Iron Furnaces section."""
    return Q(key, 0, 0, [item(f"{IF}{metal}_furnace")], f"{metal.title()} Furnace", section=S_IF, deps=deps, xp=xp,
             subtitle=kw.pop("subtitle", f"The {metal} tier of furnace"),
             desc=[f"&eWhat:&r {what}", *([f"&eChemistry:&r {extra}"] if extra else []), f"&eHow:&r {how}", f"&eTip:&r {tip}"], **kw)


def gg(key, name, deps, xp, sub, what, how, tip, chem=None, **kw):
    """One Generator Galore generator."""
    return Q(key, 0, 0, [item(f"{GG}{name}_generator")], f"{name.title()} Generator", section=S_GG, deps=deps, xp=xp, subtitle=sub,
             desc=[f"&eWhat:&r {what}", *([f"&eChemistry:&r {chem}"] if chem else []), f"&eHow:&r {how}", f"&eTip:&r {tip}"], **kw)


def augment(key, kind, title, sub, what, tip):
    return Q(key, 0, 0, [item(f"{IF}augment_{kind}")], title, section=S_AUG, deps=["pw_if_augments"], xp=30, subtitle=sub, desc=[
        f"&eWhat:&r {what}",
        "&eHow:&r check JEI for its recipe, then put it in one of the furnace's augment slots.",
        f"&eTip:&r {tip}"])


CHAPTER = Chapter("generators", "Generators", "ironfurnaces:diamond_furnace",
        ["Faster furnaces and a burner for every fuel."], SIDE, mirror="generators", quests=[
    # ===== The Furnace (ATM10 Generators centre) ============================================
    Q("pw_furnace", 0, 0, [item("minecraft:furnace")], "Furnaces and Generators", section=S_FURN, deps=["gs_furnace", "pw_iron_gen"], xp=30,
      size=1.5, subtitle="Two mods that make heat work harder", desc=[
        "&6Fire was the first thing you ever gave anyone. You remember that much.&r",
        "&eWhat:&r Iron Furnaces makes faster furnaces, tier by tier; Generator Galore makes burners for every odd fuel. Both start from the humble furnace.",
        "&eChemistry:&r a furnace is a controlled oxidation: fuel + O₂ → CO₂ + H₂O + heat. Better furnaces just waste less of that heat.",
        "&eHow:&r any vanilla furnace opens the section."]),

    # ===== Iron Furnaces =====================================================================
    if_furnace("pw_if_copper", "copper", ["pw_furnace"], 30, "a faster furnace from copper, and the start of the silver branch.",
               "copper ingots around a vanilla furnace (check JEI).", "every furnace tier can upgrade in place with an upgrade kit, keeping its contents."),
    if_furnace("pw_if_iron", "iron", ["pw_furnace"], 30, "the first real step up: smelts noticeably faster than vanilla.",
               "iron ingots around a vanilla furnace (check JEI).", "4x vanilla cooking is on in this pack, so even this one is quick."),
    if_furnace("pw_if_silver", "silver", ["pw_if_copper", "pw_if_iron"], 40, "the silver tier, between iron and gold.",
               "silver ingots and glass around an iron furnace (check JEI).", "silver comes from MI ore processing and the Mining dimension's veins.",
               extra="silver has the highest electrical and thermal conductivity of any metal (about 6% better than copper)."),
    if_furnace("pw_if_gold", "gold", ["pw_if_iron", "pw_if_silver"], 40, "the gold tier: faster again.",
               "gold ingots and a block of gold around an iron furnace (check JEI).", "a gold furnace on your ore line pays for itself quickly."),
    if_furnace("pw_if_diamond", "diamond", ["pw_if_gold"], 50, "the diamond tier.",
               "diamonds and glass around a gold furnace (check JEI).", "from here the tree splits into emerald and crystal."),
    if_furnace("pw_if_emerald", "emerald", ["pw_if_diamond"], 50, "the emerald tier.",
               "emeralds around a diamond furnace (check JEI).", "a villager trading hall makes emeralds cheap.",
               extra="emerald is the mineral beryl, Be₃Al₂Si₆O₁₈, coloured green by a trace of chromium."),
    if_furnace("pw_if_crystal", "crystal", ["pw_if_diamond"], 50, "the crystal tier, built with Nether quartz and glass.",
               "glass and an eye of ender around a diamond furnace (check JEI).", "obsidian next needs both the emerald and the crystal furnace.",
               extra="window glass is mostly SiO₂ with soda and lime. Unlike quartz, its atoms have no regular lattice: it is a frozen liquid, not a crystal."),
    if_furnace("pw_if_obsidian", "obsidian", ["pw_if_crystal", "pw_if_emerald"], 60, "the obsidian tier: very fast, and blast-proof.",
               "obsidian and blaze rods around an emerald furnace (check JEI).", "it's the base for the netherite tier.",
               extra="obsidian is volcanic glass: lava that cooled too fast to form crystals."),
    if_furnace("pw_if_netherite", "netherite", ["pw_if_obsidian", "t2_nether"], 80, "the top standard tier.",
               "netherite ingots, magma cream and a soul sand or soul soil block around an obsidian furnace (check JEI).", "the Rainbow Core needs one of these."),
    if_furnace("pw_if_atm", "allthemodium", ["pw_if_netherite"], 80, "a furnace from Allthemodium, beyond netherite.",
               "Allthemodium ingots and blocks around a netherite furnace (check JEI).",
               "the Allthemodium page covers where the metal comes from.", subtitle="Optional: past netherite", **OPT),
    if_furnace("pw_if_vibranium", "vibranium", ["pw_if_atm"], 100, "the vibranium tier.",
               "vibranium around an Allthemodium furnace (check JEI).", "vibranium comes from the Other dimension.",
               subtitle="Optional: faster still", **OPT),
    if_furnace("pw_if_unobtainium", "unobtainium", ["pw_if_vibranium"], 120, "the fastest furnace in the mod.",
               "unobtainium around a vibranium furnace (check JEI).", "worth it only if you smelt by the hundred thousand.",
               subtitle="Optional: the last furnace", optional=True, tokens=2),

    # ===== The Rainbow Generator ============================================================
    Q("pw_if_core", 0, 0, [item(IF + "rainbow_core")], "Rainbow Core", section=S_RAINBOW, deps=["pw_if_netherite"], xp=80,
      subtitle="Seven colours around netherite", desc=[
        "&eWhat:&r the core of the Rainbow Generator.",
        "&eChemistry:&r stained glass gets its colour from metal ions in the glass: cobalt for blue, chromium for green, gold for ruby red.",
        "&eHow:&r red, orange, yellow, green, blue, purple and magenta stained glass around two netherite furnaces (check JEI)."]),
    Q("pw_if_plating", 0, 0, [item(IF + "rainbow_plating", 8)], "Rainbow Plating", section=S_RAINBOW,
      deps=["pw_if_iron", "pw_if_gold", "pw_if_diamond", "pw_if_emerald", "pw_if_obsidian", "pw_if_crystal", "pw_if_copper", "pw_if_silver"],
      xp=80, subtitle="One furnace of every tier, melted down", desc=[
        "&eWhat:&r eight plating, from one each of the copper, iron, silver, gold, diamond, emerald, crystal and obsidian furnaces.",
        "&eHow:&r shapeless, all eight furnaces together (check JEI).",
        "&eTip:&r upgrade kits make the furnaces cheaper than building each from scratch."]),
    Q("pw_if_rainbow", 0, 0, [item(IF + "million_furnace")] + [item(f"{IF}{m}_furnace") for m in FURNACES], "The Rainbow Generator",
      section=S_RAINBOW, deps=["pw_if_plating", "pw_if_core", "pw_if_netherite"], xp=200, size=1.5,
      subtitle="Every furnace working together", desc=[
        "&eWhat:&r the Rainbow Furnace, plus one furnace of every other tier. When every tier runs as a generator, it makes a great deal of FE.",
        "&eHow:&r 8 rainbow plating around a rainbow core. Put a Generator augment in one furnace of each tier and keep them all burning; the tooltip explains the rest.",
        "&eTip:&r you can only have one Rainbow Generator, so pick its spot with care."]),
    Q("pw_if_rainbow_coal", 0, 0, [item(IF + "rainbow_coal")], "Rainbow Coal", section=S_RAINBOW, deps=["pw_if_rainbow"], xp=100,
      **OPT, subtitle="Optional: a fuel with no recipe", desc=[
        "&eWhat:&r a fuel that burns for a very long time. It has no crafting recipe.",
        "&eHow:&r read the Rainbow Furnace's tooltip carefully. It hints at what to do.",
        "&eTip:&r try it far from anything you love."]),

    # ===== Furnace Augments ==================================================================
    Q("pw_if_augments", 0, 0, [item("minecraft:paper")], "Augments", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=20,
      subtitle="Cards that change what a furnace does", desc=[
        "&eWhat:&r augments go in a furnace's side slots and change how it works: blasting, smoking, more slots, speed, efficiency or power.",
        "&eHow:&r every augment starts with paper (check JEI). A furnace takes one of each type.",
        "&eTip:&r speed and fuel efficiency pull in opposite directions; pick one per furnace."]),
    augment("pw_if_aug_blasting", "blasting", "Blasting Augment", "A blast furnace in disguise",
            "makes the furnace act as a blast furnace: faster on ores and metal, no food.",
            "put it on the furnace your ore line feeds."),
    augment("pw_if_aug_smoking", "smoking", "Smoking Augment", "A smoker in disguise",
            "makes the furnace act as a smoker: fast on food only.",
            "one smoking furnace next to the kitchen is plenty."),
    augment("pw_if_aug_factory", "factory", "Factory Augment", "Several slots at once",
            "turns the furnace into a factory with several input and output slots that smelt side by side.",
            "a factory furnace plus a pipe to storage is a whole smelting room in one block."),
    augment("pw_if_aug_generator", "generator", "Generator Augment", "A furnace that makes FE",
            "turns the furnace into a generator that burns fuel for FE instead of smelting.",
            "the Rainbow Generator needs one of these in a furnace of every tier."),
    augment("pw_if_aug_speed", "speed", "Speed Augment", "Faster, hungrier",
            "makes the furnace smelt faster at the cost of more fuel.",
            "good on furnaces fed by a steady fuel line."),
    augment("pw_if_aug_fuel", "fuel", "Efficiency Augment", "Slower, thriftier",
            "makes fuel last longer at the cost of speed.",
            "good on furnaces you fill by hand."),
    Q("pw_if_heater", 0, 0, [item(IF + "heater"), item(IF + "item_heater")], "Wireless Heating", section=S_AUG,
      deps=["pw_if_copper", "pw_if_iron"], xp=40, subtitle="Fuel furnaces with FE from afar", desc=[
        "&eWhat:&r the Heater stores FE; a Heater card links a furnace to it, so the furnace burns electricity instead of fuel.",
        "&eHow:&r check JEI for both. Right-click the heater with the card, then put the card in a furnace.",
        "&eTip:&r one heater can feed a whole row of furnaces."]),
    Q("pw_if_copy", 0, 0, [item(IF + "item_copy")], "Configuration Copier", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=20,
      subtitle="Set one furnace, paste to the rest", desc=[
        "&eWhat:&r copies a furnace's side settings and pastes them onto another.",
        "&eHow:&r check JEI. Sneak-click to copy, click to paste.",
        "&eTip:&r set one furnace's input, output and fuel faces, then paste it down the row."]),
    Q("pw_if_spooky", 0, 0, [item(IF + "item_spooky")], "Furnace Spooka-lator", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=10,
      subtitle="A seasonal disguise", desc=[
        "&eWhat:&r a purely cosmetic trick: right-click a furnace and it takes on a spooky look.",
        "&eHow:&r a carved pumpkin and a furnace, shapeless.",
        "&eTip:&r sneak-right-click the furnace to undo it."]),
    Q("pw_if_xmas", 0, 0, [item(IF + "item_xmas")], "Furnace Wrapping Paper", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=10,
      subtitle="Wrap a furnace as a gift", desc=[
        "&eWhat:&r another cosmetic: right-click a furnace to wrap it like a present.",
        "&eHow:&r check JEI for the recipe.",
        "&eTip:&r sneak-right-click to unwrap it again."]),

    # ===== Generator Galore ==================================================================
    gg("pw_gg_copper", "copper", ["pw_furnace"], 30, "The cheapest burner", "Generator Galore's first generator: slow, but very cheap.",
       "copper ingots around a furnace, with a redstone block (check JEI).", "the iron generator from your T1 power quest is the next step up."),
    gg("pw_gg_iron", "iron", ["pw_gg_copper"], 30, "The workhorse burner", "a steady fuel burner and the root of the Generator Galore tree.",
       "iron ingots around a copper generator, with a redstone block (check JEI).", "every later generator is built from this one or its children."),
    gg("pw_gold_gen", "gold", ["pw_gg_iron"], 60, "Same fuel, more FE per tick", "it burns fuel faster and makes more FE per tick.",
       "upgrade from the iron generator (check JEI), or use the iron-to-gold upgrade kit on a placed one.",
       "a faster burn needs a steadier fuel supply. Pipe in charcoal from a tree farm."),
    gg("pw_gg_culinary", "culinary", ["pw_gold_gen"], 50, "Spare food into power", "burns food; better food burns longer.",
       "crops, a cake and eggs around a gold generator, with a redstone block (check JEI).", "hook it to a farm's overflow.",
       chem="food energy is chemical energy: a kilocalorie is about 4.2 kJ, whether your body or a generator releases it."),
    gg("pw_gg_collection", "diamond", ["pw_gold_gen"], 60, "A gem-tier burner", "a much stronger fuel burner, and the start of the gem branch.",
       "a gold generator in diamonds with a redstone block (check JEI).", "feed it coal blocks; loose coal won't keep up."),
    gg("pw_gg_netherite", "netherite", ["pw_gg_collection", "t2_nether"], 100, "The strongest solid-fuel burner",
       "the netherite generator burns ordinary fuel at a very high rate.",
       "smithing table: template, diamond generator and a netherite ingot (check JEI).", "it leads to the Nether Star generator."),
    gg("pw_gg_gems", "emerald", ["pw_gg_collection"], 80, "Emeralds for a hotter burn", "a step past diamond on the same fuel.",
       "a diamond generator in emeralds with a redstone block (check JEI).", "villagers are the cheapest emerald source.",
       chem="emerald is beryl, Be₃Al₂Si₆O₁₈. The beryllium in it is one of the lightest metals there is."),
    gg("pw_gg_obsidian", "obsidian", ["pw_gg_collection", "t2_obsidian"], 60, "The hub of the late tree",
       "a stronger burner, and the base for the ender, enchantment and magmatic generators.",
       "a diamond generator in obsidian with a redstone block (or the diamond-to-obsidian upgrade kit).", "JEI shows the whole tree."),
    gg("pw_gg_sweet", "honey", ["pw_gg_culinary"], 60, "Bees into power", "burns honey.",
       "a culinary generator in honey blocks with buckets and a redstone block (check JEI).",
       "a few beehives with campfires underneath keep it running.",
       chem="honey is about 80% sugars (fructose and glucose). Sugar burns well: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O."),
    gg("pw_gg_potion", "potion", ["pw_gg_culinary"], 60, "Leftover potions into power", "burns potions; stronger potions burn longer.",
       "pink dye around a culinary generator, with brewing stands and a redstone block (check JEI).", "every failed brew finally has a use."),
    gg("pw_gg_enchant", "enchantment", ["pw_gg_obsidian"], 70, "Junk books into power", "burns enchanted books and items.",
       "an obsidian generator in enchanted books with an enchanting table (check JEI).", "fishing junk books finally have a use."),
    gg("pw_gg_magmatic", "magmatic", ["pw_gg_obsidian"], 70, "Lava into power", "burns lava, a bucket at a time or by pipe.",
       "gold ingots around an obsidian generator, with a lava bucket (check JEI).", "a Nether lava lake and a pump give endless fuel.",
       chem="lava is molten silicate rock at roughly 700 to 1,200 °C."),
    gg("pw_gg_ender", "ender", ["pw_gg_obsidian"], 70, "Pearls into power", "burns ender pearls.",
       "an obsidian generator in ender pearls with a redstone block (check JEI).", "an enderman farm feeds it for ever."),
    gg("pw_gg_star", "netherstar", ["pw_gg_netherite"], 150, "Fuel fit for a god", "the Nether Star Generator burns Nether Stars for an enormous amount of FE.",
       "wither skeleton skulls around a netherite generator, with a redstone block (check JEI).", "save most stars for Powah's nitro crystals.",
       chem="real stars run on fusion: four hydrogen nuclei become one helium nucleus, and a little mass becomes a lot of energy, E = mc²."),
    gg("pw_gg_halitosis", "halitosis", ["pw_gg_ender"], 100, "Dragon's breath into power", "burns dragon's breath, bottled from the dragon's attacks in the End.",
       "amethyst around an ender generator, with an end rod (check JEI).", "plan an End trip and bring empty bottles."),
    Q("pw_gg_8x", 0, 0, [anyof(GG_8X)], "Eight Times the Burn", section=S_GG, deps=["pw_gg_copper", "w_ancient"], xp=80,
      subtitle="Compressed generators", desc=[
        "&eWhat:&r 8x generators burn fuel eight times as fast and make eight times the FE in one block. Any 8x generator counts.",
        "&eHow:&r eight generators of a tier around an echo shard (check JEI). Echo shards come from Ancient City chests.",
        "&eTip:&r make sure the fuel line can keep up first."]),
    Q("pw_gg_64x", 0, 0, [anyof(GG_64X)], "Sixty-Four Times", section=S_GG, deps=["pw_gg_8x"], xp=120, subtitle="Compressed again", desc=[
        "&eWhat:&r 64x generators: eight 8x generators in one block. Any one counts.",
        "&eHow:&r eight 8x generators around a conduit (check JEI).",
        "&eTip:&r a 64x generator eats fuel 64 times as fast. Feed it from storage, not a chest."]),
    Q("pw_gg_upgrade", 0, 0, [item(GG + "iron_to_gold_upgrade")], "Upgrade in Place", section=S_GG, deps=["pw_gold_gen"], xp=30, **OPT,
      subtitle="Optional: upgrade a generator without breaking it", desc=[
        "&eWhat:&r Generator Galore upgrade kits turn a placed generator into the next tier, keeping its fuel and connections.",
        "&eHow:&r gold ingots, an item frame and a redstone block for iron → gold (check JEI for the others). Right-click the placed generator.",
        "&eTip:&r the tree branches: gold leads to diamond or to the food-burning Culinary Generator."]),
    # ===== Upgrade kits (moved from storage.py 2026-10-20; keys unchanged) ==================
    Q("sto_if_kits", 0, 0, [item("ironfurnaces:upgrade_gold"), item("ironfurnaces:upgrade_diamond")], "Upgrade Kits", section=S_IF, deps=["pw_if_gold"], xp=30,
      **OPT, subtitle="Optional: upgrade a furnace without breaking it", desc=[
        "&eWhat:&r upgrade kits turn a placed furnace into the next tier and keep its contents, augment and settings.",
        "&eHow:&r each kit is the next tier's materials around a block (check JEI). Right-click the placed furnace with it.",
        "&eTip:&r kits are cheaper than crafting a new furnace when you have a whole row to upgrade."]),
    Q("sto_if_more_kits", 0, 0, [anyof(["ironfurnaces:upgrade_copper", "ironfurnaces:upgrade_iron", "ironfurnaces:upgrade_iron2", "ironfurnaces:upgrade_gold2",
                                       "ironfurnaces:upgrade_silver", "ironfurnaces:upgrade_silver2", "ironfurnaces:upgrade_emerald", "ironfurnaces:upgrade_crystal",
                                       "ironfurnaces:upgrade_obsidian", "ironfurnaces:upgrade_obsidian2", "ironfurnaces:upgrade_netherite"], 2)],
      "Every Kit", section=S_IF, deps=["sto_if_kits"], xp=30, **OPT, subtitle="Optional: any two more upgrade kits", desc=[
        "&eWhat:&r there's a kit for every step: vanilla to copper or iron, copper to iron, iron to gold or silver, diamond to emerald or crystal, up to netherite. Any two.",
        "&eHow:&r each is the next tier's material around a stone tool material or gem (check JEI).",
        "&eTip:&r kits keep the furnace's augment, so upgrade a generator furnace without losing its setup."]),
], links=[("gs_furnace", 0, 0), ("pw_iron_gen", 0, 0)])
for _q in CHAPTER.quests:
    if _q.key in GEN_MIRROR:
        _q.mirror = GEN_MIRROR[_q.key]
