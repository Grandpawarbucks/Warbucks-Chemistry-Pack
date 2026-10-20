"""Quest chapter: mystical (Mystical Agriculture). See tools/quests/STYLE.md."""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

# Any hopper botany pot (every material and colour) counts.
HOPPER_POTS = ["botanypots:black_concrete_hopper_botany_pot", "botanypots:black_glazed_terracotta_hopper_botany_pot", "botanypots:black_terracotta_hopper_botany_pot", "botanypots:blue_concrete_hopper_botany_pot", "botanypots:blue_glazed_terracotta_hopper_botany_pot", "botanypots:blue_terracotta_hopper_botany_pot", "botanypots:bricks_hopper_botany_pot", "botanypots:brown_concrete_hopper_botany_pot", "botanypots:brown_glazed_terracotta_hopper_botany_pot", "botanypots:brown_terracotta_hopper_botany_pot", "botanypots:cyan_concrete_hopper_botany_pot", "botanypots:cyan_glazed_terracotta_hopper_botany_pot", "botanypots:cyan_terracotta_hopper_botany_pot", "botanypots:deepslate_bricks_hopper_botany_pot", "botanypots:end_stone_bricks_hopper_botany_pot", "botanypots:gray_concrete_hopper_botany_pot", "botanypots:gray_glazed_terracotta_hopper_botany_pot", "botanypots:gray_terracotta_hopper_botany_pot", "botanypots:green_concrete_hopper_botany_pot", "botanypots:green_glazed_terracotta_hopper_botany_pot", "botanypots:green_terracotta_hopper_botany_pot", "botanypots:light_blue_concrete_hopper_botany_pot", "botanypots:light_blue_glazed_terracotta_hopper_botany_pot", "botanypots:light_blue_terracotta_hopper_botany_pot", "botanypots:light_gray_concrete_hopper_botany_pot", "botanypots:light_gray_glazed_terracotta_hopper_botany_pot", "botanypots:light_gray_terracotta_hopper_botany_pot", "botanypots:lime_concrete_hopper_botany_pot", "botanypots:lime_glazed_terracotta_hopper_botany_pot", "botanypots:lime_terracotta_hopper_botany_pot", "botanypots:magenta_concrete_hopper_botany_pot", "botanypots:magenta_glazed_terracotta_hopper_botany_pot", "botanypots:magenta_terracotta_hopper_botany_pot", "botanypots:mossy_stone_bricks_hopper_botany_pot", "botanypots:mud_bricks_hopper_botany_pot", "botanypots:nether_bricks_hopper_botany_pot", "botanypots:orange_concrete_hopper_botany_pot", "botanypots:orange_glazed_terracotta_hopper_botany_pot", "botanypots:orange_terracotta_hopper_botany_pot", "botanypots:pink_concrete_hopper_botany_pot", "botanypots:pink_glazed_terracotta_hopper_botany_pot", "botanypots:pink_terracotta_hopper_botany_pot", "botanypots:polished_blackstone_bricks_hopper_botany_pot", "botanypots:prismarine_bricks_hopper_botany_pot", "botanypots:purple_concrete_hopper_botany_pot", "botanypots:purple_glazed_terracotta_hopper_botany_pot", "botanypots:purple_terracotta_hopper_botany_pot", "botanypots:quartz_bricks_hopper_botany_pot", "botanypots:red_concrete_hopper_botany_pot", "botanypots:red_glazed_terracotta_hopper_botany_pot", "botanypots:red_nether_bricks_hopper_botany_pot", "botanypots:red_terracotta_hopper_botany_pot", "botanypots:stone_bricks_hopper_botany_pot", "botanypots:terracotta_hopper_botany_pot", "botanypots:tuff_bricks_hopper_botany_pot", "botanypots:white_concrete_hopper_botany_pot", "botanypots:white_glazed_terracotta_hopper_botany_pot", "botanypots:white_terracotta_hopper_botany_pot", "botanypots:yellow_concrete_hopper_botany_pot", "botanypots:yellow_glazed_terracotta_hopper_botany_pot", "botanypots:yellow_terracotta_hopper_botany_pot"]

MA = "mysticalagriculture:"
TIERS = ["inferium", "prudentium", "tertium", "imperium", "supremium"]
ARMOR = [MA + t + "_" + p for t in TIERS + ["awakened_supremium"] for p in ("helmet", "chestplate", "leggings", "boots")]
WEAPONS = [MA + t + "_" + w for t in TIERS + ["awakened_supremium"] for w in ("sword", "bow", "crossbow", "fishing_rod")]
FARMLAND_UP = [MA + t + "_farmland" for t in TIERS[1:]]
ACCEL_UP = [MA + t + "_growth_accelerator" for t in TIERS[1:] + ["awakened_supremium"]]

# ATM10 mirror (2026-10-20, user decision): this page follows ATM10's Mystical Agriculture chapter
# ("elmystical_agriculturerr") quest for quest where the crop exists here: hub, prosperity, the altar, one essence
# milestone per tier with its farmland, accelerator, armour and tools, then one quest per resource seed in ATM10's
# tier clusters. Its item list, order and shape only; all text is ours. Seeds this pack blocks (uranium, osmium,
# fluorite, aluminum, silicon, steel, graphite, platinum, iridium, refined obsidian/glowstone and the rest) and seeds
# for mods we don't have are left out. Tier 3/4/5 seeds need MI LV/MV/HV circuits (phase4_mysticalagriculture.js),
# so each seed hangs off its essence tier, which hangs off the circuit quest.
from questlib import IDS  # noqa: E402

SPINE, MACH = "Essence Tiers", "Machines and Tools"
ESS = {1: "inferium", 2: "prudentium", 3: "tertium", 4: "imperium", 5: "supremium"}
CIRCUIT = {3: "an MI analog circuit (LV)", 4: "an MI electronic circuit (MV)", 5: "an MI digital circuit (HV)"}
FARMLAND = {1: "ma_farmland", 2: "ma_farmland_up", 3: "ma_farmland_t3", 4: "ma_farmland_t4", 5: "ma_farmland_t5"}
ESSENCE_Q = {1: "ma_inferium", 2: "f_prudentium", 3: "f_tertium", 4: "f_imperium", 5: "f_supremium"}
TOOLS = ["sword", "pickaxe", "axe", "shovel", "hoe", "watering_can", "bow", "crossbow", "shears", "sickle", "scythe", "fishing_rod"]


def tier_tools(t):
    """Every essence tool of a tier that exists in this pack."""
    return [MA + f"{t}_{n}" for n in TOOLS if MA + f"{t}_{n}" in IDS]


def seed(crop, tier, label, mirror, mob=False, extra=(), fact=None):
    """One resource seed: craft it on the altar, plant it, and it grows essence of `label`."""
    key = "ma_s_" + crop
    deps = [ESSENCE_Q[tier] if mob else FARMLAND[tier], "f_altar"]
    if mob and tier == 2:
        deps = ["ma_dagger", "f_altar"]
    section = f"Tier {tier} {'Mobs' if mob else 'Crops'}"
    name = crop.replace("_", " ")
    how = f"&eHow:&r a prosperity seed base on the Infusion Altar, with {ESS[tier]} essence and "
    how += "a full Soul Jar of that mob on the pedestals" if mob and crop != "experience" else "the crop's materials on the pedestals"
    how += f" (check JEI). {'It also needs ' + CIRCUIT[tier] + '.' if tier >= 3 else ''}"
    desc = [f"&eWhat:&r {name} seeds grow {name} essence, which crafts back into {label}.", how.rstrip()]
    if fact:
        desc.append("&eChemistry:&r " + fact)
    desc.append("&eTip:&r one seed is enough: plant it and every harvest has a chance to drop another.")
    return Q(key, 0, 0, [item(MA + crop + "_seeds"), *extra], name.title() + " Seeds", deps=deps, xp=10 + 10 * tier,
             subtitle=f"Tier {tier} {'mob ' if mob else ''}crop", section=section, mirror=mirror, desc=desc)


def tier_kit(tier, t, farmland, accel, armor, tools, xp):
    """Farmland, accelerator, armour set and any tool of an essence tier (ATM10's ring around each milestone)."""
    eq = ESSENCE_Q.get(tier, "f_awakening")
    out = []
    nm = t.replace("_", " ").title()
    if farmland:
        out.append(Q(farmland[0], 0, 0, [item(MA + f"{t}_farmland")], nm + " Farmland", deps=[eq], xp=xp, section=SPINE,
                     mirror=farmland[1], subtitle=f"Soil for tier {tier} crops", desc=[
                         f"&eWhat:&r farmland infused with {t} essence. Inferium crops on it drop more essence, and the tier {tier} seeds on this page hang off it.",
                         f"&eHow:&r {t} essence and farmland, shapeless (check JEI).",
                         "&eTip:&r convert the soil under your inferium field first; that's where it pays."]))
    if accel:
        out.append(Q(accel[0], 0, 0, [item(MA + f"{t}_growth_accelerator")], nm + " Growth Accelerator", deps=[eq], xp=xp,
                     section=SPINE, mirror=accel[1], subtitle="Faster crops from below", desc=[
                         "&eWhat:&r a growth accelerator placed under farmland ticks the crops above it; higher tiers reach further.",
                         f"&eHow:&r {t} essence around stone and the tier's gemstone (check JEI).",
                         "&eTip:&r stack them in a column under the crop."]))
    out.append(Q(armor[0], 0, 0, [item(MA + f"{t}_{p}") for p in ("helmet", "chestplate", "leggings", "boots")], nm + " Armour",
                 deps=[eq], xp=xp * 2, section=SPINE, mirror=armor[1], subtitle="A full essence set", desc=[
                     f"&eWhat:&r the {t} armour set. Each tier adds protection and augment slots.",
                     "&eHow:&r upgrade the previous tier's pieces with this tier's ingots and gemstones (check JEI).",
                     "&eTip:&r augments go in at the Tinkering Table."]))
    out.append(Q(tools[0], 0, 0, [anyof(tier_tools(t))], nm + " Tools", deps=[eq], xp=xp, section=SPINE, mirror=tools[1],
                 subtitle="Any one essence tool of this tier", desc=[
                     f"&eWhat:&r any {t} tool: sword, pick, axe, shovel, hoe, sickle, scythe, shears, bow, crossbow, fishing rod or watering can.",
                     "&eHow:&r upgrade the previous tier's tool with this tier's ingots and gemstones (check JEI).",
                     "&eTip:&r the sickle and scythe harvest crops in an area and replant them."]))
    return out


CHAPTER = Chapter("mystical", "Mystical Agriculture", "mysticalagriculture:infusion_altar",
        ["Resource crops, within the rules of chemistry."], SIDE, [
    # --- Essence tiers: the spine (y=0) --------------------------------------------------------
    Q("f_altar", 0, 0, [item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:infusion_pedestal", 8)], "Mystical Agriculture", deps=["ma_seed_base", "gs_iron"], size=2.0, shape="gear", section=SPINE, mirror="0B37355262121DD5", xp=50,
      subtitle="Resource crops, made on an altar", desc=[
        "&6You remember coaxing metal out of the ground like wheat. Some of that still works.&r",
        "&eWhat:&r resource crops grow essence that crafts into real materials. Seeds are made on the Infusion Altar with Infusion Pedestals around it.",
        "&eHow:&r the altar is gold, stone and red wool; 8 Infusion Pedestals stand around it (check JEI for both and the layout).",
        "&eTip:&r &eTier 3/4/5 seeds need MI LV/MV/HV circuits&r, and crops for chemistry milestones can't be grown at all. Farming is a convenience here, not a shortcut."]),
    Q("f_prosperity", 2, 0, [item("mysticalagriculture:prosperity_shard", 4)], "Prosperity", deps=["ma_hub"], size=1.5, section=SPINE, mirror="2DDA04088C8220D2", xp=40,
      subtitle="Shards for seed bases and crystals", desc=[
        "&eWhat:&r prosperity shards come from prosperity ore. They make seed bases (the core of every resource seed) and infusion crystals.",
        "&eHow:&r mine prosperity ore (an iron pick is enough).",
        "&eTip:&r Ultimine the veins; you'll want a lot of shards."]),
    Q("f_crystal", 4, 0, [item("mysticalagriculture:infusion_crystal")], "Infusion Crystal", deps=["ma_inferium"], size=1.25, section=SPINE, mirror="217DB12EA32E1724", xp=40,
      subtitle="The tool that upgrades essence", desc=[
        "&eWhat:&r a crystal that combines lower essence into higher tiers. It wears out with use.",
        "&eHow:&r a diamond, prosperity shards and inferium essence (check JEI).",
        "&eTip:&r the Master Infusion Crystal never wears out; it comes much later, from supremium."]),
    Q("f_prudentium", 6, 0, [item("mysticalagriculture:prudentium_essence")], "Prudentium", deps=["f_crystal"], size=1.5, section=SPINE, mirror="73350AD668200E99", xp=40,
      subtitle="Tier 2 essence", desc=[
        "&eWhat:&r the second essence tier, for tier 2 seeds (JEI lists every crop and its tier).",
        "&eHow:&r 4 inferium essence around an infusion crystal make 1 prudentium (check JEI).",
        "&eTip:&r it uncrafts back to inferium if you overshoot (check JEI)."]),
    Q("f_tertium", 8, 0, [item("mysticalagriculture:tertium_essence")], "Tertium: LV Seeds", deps=["f_prudentium", "t3_analog"], size=1.5, section=SPINE, mirror="2C9C9CB71941DC01", xp=75,
      subtitle="Tier 3 seeds need an analog circuit", desc=[
        "&eWhat:&r tier 3 seeds (iron, copper, redstone, nether quartz, tin, lead and more) need Tertium essence and an &eMI analog circuit&r.",
        "&eChemistry:&r the analog circuit stands on steel, and steel stands on coke: coal baked without air until only carbon is left.",
        "&eHow:&r 4 prudentium around an infusion crystal make 1 tertium. Each seed type costs its circuit once; planted seeds multiply."]),
    Q("f_imperium", 10, 0, [item("mysticalagriculture:imperium_essence")], "Imperium: MV Seeds", deps=["f_tertium", "t4_mv"], size=1.5, section=SPINE, mirror="66C52B137A4FF869", xp=100,
      subtitle="Tier 4 seeds need an electronic circuit", desc=[
        "&eWhat:&r tier 4 seeds (gold, lapis, nickel, blaze, enderman and more) need Imperium essence and an &eMI electronic circuit&r.",
        "&eChemistry:&r the electronic circuit needs aluminum, which only electrolysis can free from its oxide: 2Al₂O₃ → 4Al + 3O₂.",
        "&eHow:&r 4 tertium around an infusion crystal make 1 imperium."]),
    Q("f_supremium", 12, 0, [item("mysticalagriculture:supremium_essence")], "Supremium: HV Seeds", deps=["f_imperium", "t5_hv"], section=SPINE, mirror="67DBE6C59C0D9D1B", xp=200,
      size=1.5, shape="hexagon", subtitle="Tier 5 seeds need a digital circuit", desc=[
        "&6You remember gardens that grew gold. These come close, and they still answer to chemistry.&r",
        "&eWhat:&r tier 5 seeds (diamond, emerald, netherite and more) need Supremium essence and an &eMI digital circuit&r.",
        "&eChemistry:&r the digital circuit needs polyethylene: thousands of ethylene units, C₂H₄, linked into one chain.",
        "&eHow:&r 4 imperium around an infusion crystal make 1 supremium."]),
    Q("f_accelerator", 1, 1.5, [item("mysticalagriculture:inferium_growth_accelerator")], "Growth Accelerators", deps=["ma_inferium"], section=SPINE, mirror="4821419D44F8083F", xp=40, subtitle="Crops grow faster above them", desc=[
        "&eWhat:&r growth accelerators placed below farmland speed up the crops above them. Stack several for more effect.",
        "&eHow:&r check JEI for each tier's recipe.",
        "&eTip:&r put them under the floor of your crop room so they're out of the way."]),
    Q("f_awakening", 14, 1.5, [item("mysticalagriculture:awakened_supremium_essence")], "Awakening", deps=["ma_awaken_parts", "ma_cognizant"], size=2.0, shape="gear", section=SPINE, mirror="7A103577EAE7B3F1", xp=300, subtitle="Beyond supremium", desc=[
        "&eWhat:&r the Awakening Altar turns supremium into awakened supremium for the strongest Mystical Agriculture gear.",
        "&eHow:&r JEI shows the altar, its Awakening Pedestals, the Essence Vessels and the awakening recipe.",
        "&eTip:&r awakened supremium makes the best Mystical Agriculture tools and armour."]),
    Q("ma_master", 12, -2, [item("mysticalagriculture:master_infusion_crystal")], "Master Infusion Crystal", deps=["f_supremium"], size=1.25, section=SPINE, mirror="219A5BDA5A01A420", xp=150, subtitle="A crystal that never breaks", desc=[
        "&eWhat:&r an infusion crystal with no durability, so essence upgrades stop costing crystals.",
        "&eHow:&r a supremium gemstone, supremium essence and prosperity shards (check JEI).",
        "&eTip:&r worth it once you are mass-producing tertium and imperium for seeds."]),

    # --- First crops and farmland (y=-2) -------------------------------------------------------
    Q("ma_seeds", 0, -2, [anytag("mysticalagriculture:seeds", 4)], "Inferium Seeds", deps=["f_altar"], xp=30,
      subtitle="The crop that grows more essence", desc=[
        "&eWhat:&r Inferium Seeds grow inferium essence, the fuel for every higher tier. Any 4 Mystical Agriculture seeds complete this.",
        "&eHow:&r 8 inferium essence around wheat seeds in a crafting grid (no altar needed). Plant them on farmland and replant the extra seeds.",
        "&eTip:&r every other resource seed starts from a seed base on the altar, so build a big inferium field first."]),
    Q("ma_farmland", 2, -2, [item("mysticalagriculture:inferium_farmland"), item("mysticalagriculture:inferium_seeds")], "Essence Farmland", deps=["ma_inferium"], section=SPINE, mirror="7DFF18CFEB0B8DBE", xp=30,
      subtitle="Better soil, and the first seeds", desc=[
        "&eWhat:&r farmland infused with essence. Inferium crops drop more essence on higher-tier farmland.",
        "&eHow:&r one inferium essence plus one farmland, shapeless (check JEI). Higher tiers use their own essence.",
        "&eTip:&r upgrade the farmland under your inferium field as each new essence tier arrives."]),
    Q("ma_fertilizer", 4, -2, [item("mysticalagriculture:mystical_fertilizer")], "Mystical Fertilizer", deps=["ma_hub"], section=MACH, mirror="6501A410F1543C70", xp=30,
      optional=True, tokens=1, subtitle="Optional: grow a crop instantly", desc=[
        "&eWhat:&r instantly grows a crop or sapling, including resource crops that bone meal can't push.",
        "&eHow:&r bone meal, inferium essence and a diamond make 4 (check JEI).",
        "&eTip:&r save it for slow, expensive crops rather than wheat."]),
    Q("ma_agglo", 6, -2, [item("mysticalagriculture:nature_agglomeratio"), item("mysticalagriculture:earth_agglomeratio")], "Agglomeratio", deps=["f_prosperity"], xp=30,
      optional=True, tokens=1, subtitle="Optional: materials for crops with no single item", desc=[
        "&eWhat:&r some crops (nature, the four elements, dye, nether, coral and others) don't map to one item. Their seed recipes use an agglomeratio instead.",
        "&eHow:&r Nature Agglomeratio is pumpkin, potato, cactus and sugar cane; JEI shows the rest.",
        "&eTip:&r the elemental crops (air, earth, water, fire) feed many other recipes, so they're good early picks."]),
    Q("ma_why", 8, -2, [tick()], "Why Chemistry Won't Grow", deps=["f_tertium"], xp=40,
      subtitle="Some seeds were removed on purpose", optional=True, tokens=1, desc=[
        "&eWhat:&r seeds for uranium, uraninite, osmium, fluorite, silicon, steel, aluminum, graphite, platinum, iridium, refined obsidian and refined glowstone don't exist in this pack. Click the checkmark when you've read why.",
        "&eHow:&r if JEI shows no altar recipe for a crop, it's one of these. Get them from ore processing and the reactors in the main quests.",
        "&eTip:&r iron, copper, tin, lead, gold and other everyday metals are still farmable, behind their circuit gates.",
        "{@pagebreak}",
        "&eDeep dive: why these metals?&r",
        "Each blocked resource is the reason a tier exists. Steel needs carbon from coke and an oxygen-controlled furnace; aluminum needs electrolysis of molten alumina (Hall-Héroult, 2Al₂O₃ → 4Al + 3O₂).",
        "Silicon is reduced from quartz with carbon at about 2000 °C (SiO₂ + 2C → Si + 2CO). Fluorite is the fluorine source for uranium enrichment; uranium and uraninite are the nuclear chain.",
        "Platinum and iridium come from the PGM line: anode sludge, aqua regia, ammonium hexachloroplatinate, calcining. Graphite and osmium gate Mekanism and MI steps.",
        "Growing them on a plant would skip the chemistry those tiers teach. Everything else stays farmable, so farming saves time without replacing a single reaction."]),

    # --- Watering cans and gear (y=-4) ---------------------------------------------------------
    Q("ma_can", 0, -4, [item("mysticalagriculture:watering_can")], "Watering Can", deps=["ma_hub"], section=MACH, mirror="1636F3F12E92CAEA", xp=25,
      subtitle="Water speeds up growth", desc=[
        "&eWhat:&r right-click to water crops in an area, which makes them grow faster while you hold it.",
        "&eHow:&r iron ingots, a bowl and bone meal (check JEI). Fill it from any water source.",
        "&eTip:&r stand in the middle of the field and hold right-click."]),
    Q("ma_ingot", 2, -4, [item("mysticalagriculture:inferium_ingot", 4)], "Inferium Ingots", deps=["f_prosperity"], xp=30,
      subtitle="The metal for Mystical Agriculture gear", desc=[
        "&eWhat:&r essence-infused ingots for tools, armour and the better watering cans.",
        "&eHow:&r a prosperity ingot plus 2 inferium essence (check JEI for the prosperity ingot).",
        "&eTip:&r each essence tier has its own ingot; JEI shows the upgrade path."]),
    Q("ma_can2", 4, -4, [item("mysticalagriculture:inferium_watering_can")], "Inferium Watering Can", deps=["ma_can", "ma_ingot", "ma_fertilizer"], xp=40,
      optional=True, tokens=1, subtitle="Optional: a bigger watering area", desc=[
        "&eWhat:&r a tiered watering can covers a larger area and works faster.",
        "&eHow:&r your watering can, inferium ingots and mystical fertilizer (check JEI). The higher tiers repeat the pattern.",
        "&eTip:&r the can keeps its contents when upgraded."]),
    Q("ma_lucky", 6, -4, [item("mysticalagriculture:fertilized_essence")], "A Lucky Harvest", deps=["ma_seeds"], xp=25,
      secret=True, loot="secret", subtitle="Secret: a rare drop from the field", desc=[
        "&eWhat:&r crops sometimes drop Fertilized Essence. You found one.",
        "&eHow:&r it crafts into mystical fertilizer (check JEI).",
        "&eTip:&r more crops means more chances; a big inferium field pays for itself."]),

    # --- Souls and mob crops (y=3.5) ------------------------------------------------------------
    Q("ma_soulium", 0, 3.5, [item("mysticalagriculture:soulium_dust", 4), item("mysticalagriculture:soulstone", 8)], "Soulstone", deps=["f_altar", "t2_nether"], xp=40,
      subtitle="A Nether stone with something inside", desc=[
        "&eWhat:&r soulstone clusters generate in the Nether. A few of their blocks are soulium ore, the source of soulium dust.",
        "&eHow:&r mine soulstone in the Nether and watch for soulium ore (check JEI for its drops).",
        "&eTip:&r a soulium ingot is a prosperity ingot plus 2 soulium dust; soul dust (for soul glass) comes from smelting smooth soulstone."]),
    Q("ma_dagger", 2, 3.5, [item("mysticalagriculture:soulium_dagger"), item("mysticalagriculture:soul_jar", 4), item("mysticalagriculture:soul_extractor")], "Soulium Dagger", deps=["f_prudentium", "ma_soulium"], section="Tier 2 Mobs", mirror="75560045ED084900", xp=40,
      subtitle="A blade that collects souls", desc=[
        "&eWhat:&r kills with this dagger capture the mob's soul into a Soul Jar in your inventory.",
        "&eHow:&r a golden sword, soulium ingots and soulium dust (check JEI).",
        "&eTip:&r carry 4 Soul Jars for four mob types; the Soul Extractor fills jars from drops instead of kills."]),
    Q("ma_jar", 4, 3.5, [item("mysticalagriculture:soul_jar", 2)], "Soul Jars", deps=["ma_dagger"], xp=30,
      subtitle="Glass that holds a mob's essence", desc=[
        "&eWhat:&r each jar stores souls of one mob type. Full jars are the material for mob seeds.",
        "&eHow:&r soul glass (soul dust around glass) and a soulium ingot (check JEI).",
        "&eTip:&r carry one empty jar per mob type you're hunting."]),
    Q("ma_souls", 6, 3.5, [kill("minecraft:zombie", 20)], "Fill a Jar", deps=["ma_jar"], xp=50,
      loot="hunt", subtitle="Kill 20 zombies with the dagger", desc=[
        "&eWhat:&r fill a Soul Jar with zombie souls for zombie seeds (rotten flesh).",
        "&eHow:&r keep an empty Soul Jar in your inventory and kill zombies with the Soulium Dagger.",
        "&eTip:&r the Soul Extractor can also pull souls out of mob drops like rotten flesh (check JEI)."]),
    Q("ma_mobseed", 8, 3.5, [item("mysticalagriculture:soulium_seed_base")], "Mob Seeds", deps=["ma_souls", "f_tertium"], xp=60,
      subtitle="Grow mob drops without the mobs", optional=True, tokens=1, desc=[
        "&eWhat:&r mob seeds start from a Soulium Seed Base and grow drops like rotten flesh, bones and string.",
        "&eHow:&r a prosperity seed base plus 2 soulium dust. On the altar, put it in the middle and the full jars and essence on the pedestals (check JEI).",
        "&eTip:&r zombie, skeleton, spider and creeper are tier 3, so they also need an analog circuit."]),

    # --- Machines and automation (y=5.5) -------------------------------------------------------
    Q("ma_frame", 0, 5.5, [item("mysticalagriculture:machine_frame")], "Machine Frame", deps=["ma_soulium"], xp=25,
      subtitle="The base of Mystical Agriculture machines", desc=[
        "&eWhat:&r the shared frame for the Harvester, Soul Extractor, Seed Reprocessor and other MA machines.",
        "&eHow:&r iron, redstone and stone (check JEI).",
        "&eTip:&r MA machines run on Forge Energy, so they plug into any FE cable."]),
    Q("ma_harvester", 2, 5.5, [item("mysticalagriculture:harvester")], "Harvester", deps=["ma_scythe"], section=MACH, mirror="0EFEDB0DD90DFC81", xp=50,
      subtitle="Harvests and replants a field", desc=[
        "&eWhat:&r the Harvester picks mature crops in an area in front of it and replants them, pushing drops into its inventory.",
        "&eHow:&r machine frame, soulium ingots, iron and two diamond scythes (check JEI). Power it with FE.",
        "&eTip:&r pipe its output into storage and the field runs itself."]),
    Q("ma_extractor", 4, 5.5, [item("mysticalagriculture:soul_extractor")], "Soul Extractor", deps=["ma_hub"], section=MACH, mirror="3EA2578C3A56FAE8", xp=50, subtitle="Souls from mob drops", desc=[
        "&eWhat:&r fills Soul Jars from mob drops (rotten flesh, bones, string and more) instead of kills.",
        "&eHow:&r machine frame, soulium ingots, iron and a soulium dagger (check JEI). Power it with FE.",
        "&eTip:&r feed it drops from an HNN Simulation Chamber for a fully passive soul supply."]),
    Q("ma_pots", 6, 5.5, [anyof(HOPPER_POTS, 8), anytag("mysticalagriculture:seeds", 8)], "A Pot Farm", deps=["f_pot", "ma_seeds"], xp=60,
      subtitle="Eight hopper pots of resource crops", optional=True, tokens=1, desc=[
        "&eWhat:&r Mystical Agriculture seeds grow in Hopper Botany Pots, which harvest by themselves into a chest below.",
        "&eHow:&r put each pot on a hopper, pipe or chest, add dirt or farmland and a seed. Hold any MA seed in JEI to see its pot growth time.",
        "&eTip:&r a column of pots over one shared item pipe is a compact essence farm for every tier."]),

    # --- ATM10-aligned additions (2026-10-19): altar parts, upgrades, gear, machines --------------
    Q("ma_pedestals", 0, 0, [item(MA + "infusion_pedestal", 8)], "Infusion Pedestals", deps=["f_altar"], xp=30,
      optional=True, tokens=1, subtitle="Optional: a full ring around the altar", desc=[
        "&eWhat:&r the altar takes its eight side ingredients from the pedestals around it. Every seed recipe uses all eight.",
        "&eHow:&r each pedestal is gold, red wool and stone (check JEI). Place them as JEI shows around the altar.",
        "&eTip:&r a hopper or pipe into the altar's centre makes repeat seeds easier."]),
    Q("ma_farmland_up", 0, 0, [item(MA + "prudentium_farmland")], "Better Farmland", deps=["f_prudentium"], section=SPINE, mirror="576ABF43FCF886B7", xp=40, subtitle="Upgrade the soil under your inferium", desc=[
        "&eWhat:&r higher-tier farmland makes inferium crops drop more essence: prudentium, tertium, imperium or supremium.",
        "&eHow:&r one essence of the tier plus farmland (shapeless), or till dirt with a hoe and the essence.",
        "&eTip:&r it only boosts inferium crops; resource crops grow the same on any farmland."]),
    Q("ma_accel_up", 0, 0, [item(MA + "prudentium_growth_accelerator")], "Stronger Accelerators", deps=["f_prudentium"], section=SPINE, mirror="7655E1C6C5E5469F", xp=40, subtitle="Faster growth from below", desc=[
        "&eWhat:&r higher-tier growth accelerators reach further and tick crops more often.",
        "&eHow:&r essence of the tier around stone and that tier's gemstone (makes 3; check JEI).",
        "&eTip:&r stack them in a column under the crop; each tier adds range."]),
    Q("ma_gear", 0, 0, [item(MA + "inferium_" + p) for p in ("helmet", "chestplate", "leggings", "boots")], "Inferium Armour", deps=["ma_inferium"], section=SPINE, mirror="2A7E3F2CD335EAD0", xp=60, subtitle="Armor grown from a field", desc=[
        "&eWhat:&r Mystical Agriculture armor in six tiers, from inferium to awakened supremium. Higher tiers hold augments.",
        "&eHow:&r a diamond armor piece with two ingots and two gemstones of the tier (it keeps the item's enchantments). Each tier upgrades the last.",
        "&eTip:&r higher tiers also take augments; see the Augments quest."]),
    Q("ma_weapons", 0, 0, [anyof(tier_tools("inferium"))], "Inferium Tools", deps=["ma_inferium"], section=SPINE, mirror="4EF5DE3FBA2A7AE3", xp=60, subtitle="Swords, bows and a fishing rod", desc=[
        "&eWhat:&r essence swords, bows, crossbows and fishing rods, upgraded tier by tier like the armor.",
        "&eHow:&r the diamond (or plain) item with two ingots and two gemstones of the tier (check JEI).",
        "&eTip:&r a sword with the Mystical Enlightenment enchantment can collect Cognizant Dust from bosses."]),
    Q("ma_augments", 0, 0, [item(MA + "unattuned_augment")], "Augments", deps=["ma_weapons", "ma_gear"], any_dep=True, section=MACH, mirror="37B297640F537383", xp=60, subtitle="Add powers to essence gear", desc=[
        "&eWhat:&r augments add effects to essence tools and armor (speed, night vision, mining area and more). The Tinkering Table fits them.",
        "&eHow:&r an Unattuned Augment is prosperity shards and iron; attune it on the altar (check JEI). The Tinkering Table fits it.",
        "&eTip:&r higher gear tiers have more augment slots."]),
    Q("ma_reprocessor", 0, 0, [item(MA + "seed_reprocessor")], "Seed Reprocessor", deps=["ma_hub"], section=MACH, mirror="5C590DB2F3D935E5", xp=40, subtitle="Spare seeds back into essence", desc=[
        "&eWhat:&r grinds surplus resource seeds back into the essence they're made of, powered by FE.",
        "&eHow:&r a machine frame with soulium ingots, iron and 2 iron hoes.",
        "&eTip:&r feed it the extra seeds from a pot farm and nothing goes to waste."]),
    Q("ma_furnace", 0, 0, [item(MA + "furnace")], "Essence Furnace", deps=["f_prosperity"], section=MACH, mirror="21A90474590FCDB8", xp=30, subtitle="An electric furnace", desc=[
        "&eWhat:&r a powered furnace that smelts with FE instead of burning fuel.",
        "&eChemistry:&r an electric furnace heats by resistance: current through a wire, P = I²R. No combustion, no CO₂ at the furnace.",
        "&eHow:&r a machine frame with iron, prosperity ingots and 2 furnaces."]),
    Q("ma_enchanter", 0, 0, [item(MA + "enchanter")], "Essence Enchanter", deps=["ma_hub"], section=MACH, mirror="6235B9923BE0AAEB", xp=50,
      optional=True, tokens=1, subtitle="Optional: enchant with essence, not luck", desc=[
        "&eWhat:&r applies the enchantment you pick, paid for with experience essence plus an item for each enchantment (check JEI for the costs).",
        "&eHow:&r an enchanting table on a soulium ingot over 3 soulstone.",
        "&eTip:&r it's the easy way to put Mystical Enlightenment on a sword."]),
    Q("ma_capsule", 0, 0, [item(MA + "experience_capsule")], "Experience Capsule", deps=["ma_jar"], xp=30,
      optional=True, tokens=1, subtitle="Optional: bottle your levels", desc=[
        "&eWhat:&r stores experience points picked up while it's in your inventory, to spend later.",
        "&eHow:&r 2 soulium ingots and 2 soul glass."]),
    Q("ma_spawner", 0, 0, [item(MA + "soulium_spawner")], "Soulium Spawner", deps=["ma_hub"], section=MACH, mirror="16E3031D800B40D5", xp=75, subtitle="Mobs from essence", desc=[
        "&eWhat:&r a powered spawner that turns mob essence into living mobs (JEI's Soulium Spawner page lists what each costs).",
        "&eHow:&r a machine frame with iron, soulium ingots and 2 wither skeleton skulls.",
        "&eTip:&r pair it with a mob grinder for drops crops can't grow, like XP."]),
    Q("ma_awaken_parts", 0, 0, [item(MA + "awakening_altar"), item(MA + "awakening_pedestal", 4), item(MA + "essence_vessel", 4)], "Awakening Rig", deps=["f_supremium"], section=SPINE, mirror="33D23C65E7274A8F", xp=100, subtitle="Pedestals and vessels for the altar", desc=[
        "&eWhat:&r the Awakening Altar is fed by 4 Awakening Pedestals and 4 Essence Vessels holding air, earth, water and fire essence.",
        "&eHow:&r both are gold and soulstone, with orange wool (pedestal) or glass (vessel). JEI shows the layout.",
        "&eTip:&r fill the vessels before you start; awakening drains a lot of elemental essence."]),
    Q("ma_witherproof", 0, 0, [anyof([MA + "witherproof_block", MA + "witherproof_bricks", MA + "witherproof_glass"])], "Witherproof Bricks", deps=["ma_s_wither_skeleton"], section="Tier 5 Mobs", mirror="408D8B1CFBA22BAF", xp=60,
      optional=True, tokens=1, subtitle="Optional: an arena the Wither can't break", desc=[
        "&eWhat:&r bricks the Wither's skulls can't destroy: build a box and fight it on your terms.",
        "&eHow:&r a witherproof block is soulstone in wither skeleton essence (a tier 5 crop); 4 blocks make 4 bricks.",
        "&eTip:&r the Seed of a New World needs Nether Stars, so a safe Wither arena pays for itself."]),
    Q("ma_cognizant", 0, 0, [item(MA + "cognizant_dust", 4)], "Cognizant Dust", deps=["f_supremium"], section=SPINE, mirror="1CF8263756EE8F2A", xp=200, subtitle="Knowledge from a boss", desc=[
        "&6You remember learning from the strongest things you fought. Some of it is still on the floor.&r",
        "&eWhat:&r Cognizant Dust drops from the Wither and the Ender Dragon when they die to an essence weapon with Mystical Enlightenment.",
        "&eHow:&r enchant an essence sword in the Essence Enchanter, then land the last hit on a boss with it.",
        "&eTip:&r it goes into awakened supremium: JEI shows the awakening recipe."]),

    # ===== ATM10 mirror: Mystical Agriculture (2026-10-20) ==================================================
    Q("ma_hub", 0, 0, [anytag("c:seeds")], "Seeds of Something", deps=[], xp=10, size=2.0, shape="gear", section=SPINE,
      mirror="54735C5FCD2077B3", icon="mysticalagriculture:inferium_seeds", subtitle="Any seed: the start of every crop", desc=[
        "&6You remember coaxing metal out of the ground like wheat. Some of that still works.&r",
        "&eWhat:&r Mystical Agriculture grows resources as crops. This page climbs its five essence tiers and lists every seed this pack allows.",
        "&eChemistry:&r a real plant only builds itself from CO₂, water and a few soil minerals. Growing iron from a seed is the magic part; the circuit gates are the chemistry part.",
        "&eHow:&r pick up any seed. Wheat seeds from grass are fine.",
        "&eTip:&r seeds for uranium, osmium, fluorite and the other chemistry milestones don't exist here, by design."]),
    Q("ma_seed_base", 0, 0, [item(MA + "prosperity_seed_base")], "Prosperity Seed Base", deps=["f_prosperity"], xp=25, size=1.25,
      section=SPINE, mirror="1E0F92F07FDD162E", subtitle="The core of every resource seed", desc=[
        "&eWhat:&r every resource seed is crafted around a seed base on the Infusion Altar.",
        "&eHow:&r 4 prosperity shards around wheat seeds.",
        "&eTip:&r make a stack; each new seed type costs one."]),
    Q("ma_inferium", 0, 0, [item(MA + "inferium_essence")], "Inferium Essence", deps=["ma_hub"], xp=20, size=1.5, section=SPINE,
      mirror="1CC4F8570A7A99EB", subtitle="Tier 1 essence", desc=[
        "&eWhat:&r the first essence. Everything on this page is built from it, and every higher essence is made from four of the tier below.",
        "&eHow:&r mine inferium ore (or kill mobs, which drop a little). 8 essence around wheat seeds make Inferium Seeds.",
        "&eTip:&r a big inferium field is the engine of the whole page."]),
    Q("ma_wand", 0, 0, [item(MA + "wand")], "The Wand", deps=["ma_inferium"], xp=10, size=0.75, optional=True, section=MACH,
      mirror="224CE21E56703F6E", subtitle="Optional: start the altar's crafting", desc=[
        "&eWhat:&r the wand activates the Infusion and Awakening Altars when the ingredients are in place.",
        "&eHow:&r check JEI; it's cheap.",
        "&eTip:&r a redstone signal on the altar also starts it, which is handy for automation."]),
    Q("ma_sickle", 0, 0, [anytag("cucumber:sickles")], "A Sickle", deps=["ma_hub"], xp=15, section=MACH, mirror="04A7AA70C23830FF",
      icon="mysticalagriculture:diamond_sickle", subtitle="Harvest crops and leaves in an area", desc=[
        "&eWhat:&r a sickle breaks plants, leaves and grass in a radius around the block you hit.",
        "&eHow:&r any sickle counts: wood up to diamond, or the essence ones (check JEI).",
        "&eTip:&r great for clearing a jungle canopy."]),
    Q("ma_scythe", 0, 0, [anytag("cucumber:scythes")], "A Scythe", deps=["ma_hub"], xp=15, section=MACH, mirror="45549E52B3CE2D23",
      icon="mysticalagriculture:diamond_scythe", subtitle="Harvest and replant a field", desc=[
        "&eWhat:&r a scythe harvests mature crops in an area and replants them in one swing.",
        "&eHow:&r any scythe counts (check JEI). Two diamond scythes also go into the Harvester.",
        "&eTip:&r right-click a mature crop to harvest just that one and replant it."]),
    Q("ma_upgrade", 0, 0, [anyof([MA + t + "_upgrade" for t in TIERS + ["awakened_supremium"]])], "Machine Upgrades", deps=["f_prosperity", "ma_inferium"],
      xp=40, size=2.0, section=MACH, mirror="77C6667B4C37589C", icon="mysticalagriculture:inferium_upgrade", subtitle="Faster machines, one tier at a time", desc=[
        "&eWhat:&r machine upgrades make the MA machines (furnace, harvester, reprocessor, spawner, extractor) faster and wider-reaching.",
        "&eHow:&r essence of the tier around a prosperity ingot or the previous upgrade (check JEI). Any tier counts.",
        "&eTip:&r one upgrade slot per machine: put your best one where the bottleneck is."]),
    Q("ma_tinkering", 0, 0, [item(MA + "tinkering_table")], "Tinkering Table", deps=["ma_augments"], xp=40, size=1.5, section=MACH,
      mirror="41DBE44D7AA0B623", subtitle="Fit augments to essence gear", desc=[
        "&eWhat:&r the Tinkering Table puts augments into essence tools and armour.",
        "&eHow:&r stone and soulium dust (check JEI).",
        "&eTip:&r higher gear tiers have more augment slots."]),
    Q("ma_awakened_block", 0, 0, [item(MA + "awakened_supremium_ingot_block")], "A Block of Awakened Supremium", deps=["f_awakening"], xp=150,
      section=SPINE, mirror="3C9F5EB59D72AC90", subtitle="Nine of the best ingots", desc=[
        "&6The garden answers you fully now. You remember this: patience, then plenty.&r",
        "&eWhat:&r a storage block of awakened supremium ingots: proof you've run the whole essence ladder.",
        "&eHow:&r 9 awakened supremium ingots.",
        "&eTip:&r the ingots also upgrade gear to the awakened tier, so only block your spares."]),

    # --- the kit around each essence tier (farmland, accelerator, armour, tools) ----------------------------------
    *tier_kit(2, "prudentium", None, None, ("ma_armor_t2", "4F137DB561F45306"), ("ma_tools_t2", "3339445194568D77"), 20),
    *tier_kit(3, "tertium", ("ma_farmland_t3", "76071C22A73A2026"), ("ma_accel_t3", "077B2D62FA7650FB"),
              ("ma_armor_t3", "15D764CAF047EA7A"), ("ma_tools_t3", "1E414D285E7A5FE2"), 30),
    *tier_kit(4, "imperium", ("ma_farmland_t4", "5BC4250E4C9F803C"), ("ma_accel_t4", "06EAA74E0A10CBB6"),
              ("ma_armor_t4", "7D43016926E77150"), ("ma_tools_t4", "67DDFA6FB1F9EECA"), 40),
    *tier_kit(5, "supremium", ("ma_farmland_t5", "48BF71269DEA1AB1"), ("ma_accel_t5", "3E555B364FD88B43"),
              ("ma_armor_t5", "5B1E0E3E876339E7"), ("ma_tools_t5", "30E9255DEC69C061"), 50),
    *tier_kit(6, "awakened_supremium", None, ("ma_accel_aw", "52BB58D470560219"),
              ("ma_armor_aw", "685C4A646E092A82"), ("ma_tools_aw", "5A58D4B25C9CB757"), 80),

    # --- tier 1 crops (inferium farmland) ---------------------------------------------------------------------
    seed("ice", 1, "ice and snow", "54D72C234EA76054", fact="ice is water whose molecules have locked into a hexagonal lattice held by hydrogen bonds; that open lattice is why ice floats."),
    seed("earth", 1, "earth-element ingredients", "1E7DC8E0493BE99E"),
    seed("water", 1, "water-element ingredients", "712EB19B26D405DD"),
    seed("dirt", 1, "dirt", "409A92D40F539485"),
    seed("stone", 1, "stone", "1609BF52108238B0"),
    seed("deepslate", 1, "deepslate", "4526E151BAE88310"),
    seed("fire", 1, "fire-element ingredients", "13124A7E22999850"),
    seed("wood", 1, "logs", "27A0BCE75F198A82"),
    seed("air", 1, "air-element ingredients", "62D572BAB055F56F"),
    # --- tier 2 crops (prudentium farmland) ---------------------------------------------------------------------
    seed("coral", 2, "coral", "31BAC57972148E1F", fact="real coral skeletons are calcium carbonate, CaCO₃, laid down by tiny animals."),
    seed("coal", 2, "coal", "573885D6EF32B7BC", fact="coal is mostly carbon: fuel, and the reducing agent that pulled iron out of its ore."),
    seed("dye", 2, "dyes", "2777FEB022346947"),
    seed("honey", 2, "honey and honeycomb", "594F6ED00D1619EE"),
    seed("nature", 2, "plants such as cactus, sugar cane and melons", "40B13424FA523E11"),
    seed("nether", 2, "Nether blocks", "3DDB7C8E61BA048F"),
    seed("amethyst", 2, "amethyst shards", "7AD9DF3FFCB03495", fact="amethyst is quartz, SiO₂, turned purple by iron impurities and natural radiation."),
    seed("sulfur", 2, "sulfur", "51592B271E56C6B2", fact="burning sulfur gives SO₂ (S + O₂ → SO₂), the first step to sulfuric acid. The acid still needs your contact process."),
    seed("menril", 2, "menril (check JEI)", "2D0BA4183DCA2751"),
    seed("limestone", 2, "limestone", "600388EAB96609E4", fact="limestone is CaCO₃. Heat it and it splits into quicklime and carbon dioxide: CaCO₃ → CaO + CO₂."),
    # --- tier 2 mobs ----------------------------------------------------------------------------------------------
    seed("chicken", 2, "feathers, eggs and chicken", "3384308C78D86059", mob=True),
    seed("squid", 2, "ink sacs", "2AECDD9E2DEA708C", mob=True),
    seed("cow", 2, "leather and beef", "7580037DB8ADEB3C", mob=True),
    seed("pig", 2, "porkchops", "75D09040185B0E40", mob=True),
    seed("sheep", 2, "wool and mutton", "2C73E3C5113BF2AC", mob=True),
    seed("fish", 2, "fish", "29AE69722AB4C75C", mob=True),
    seed("turtle", 2, "turtle scutes", "092A23FDA5D50812", mob=True),
    seed("slime", 2, "slime balls", "04B6E31120663EB2", mob=True),
    seed("armadillo", 2, "armadillo scutes", "2A2CC461B9620BDC", mob=True),
    # --- tier 3 crops (tertium farmland; LV circuit) ------------------------------------------------------------
    seed("copper", 3, "copper", "5A17C762CDB680B5"),
    seed("iron", 3, "iron", "7A89560F303A8BE6"),
    seed("tin", 3, "tin", "56B58CAFCB707565"),
    seed("silver", 3, "silver", "6950FC974624C6AA", fact="silver (Ag) conducts heat and electricity better than any other metal."),
    seed("lead", 3, "lead", "7361BD20A6B95D14"),
    seed("zinc", 3, "zinc", "0A8F44B9B3C8FC0F"),
    seed("redstone", 3, "redstone", "5EE485880EA9FACF"),
    seed("glowstone", 3, "glowstone", "02D45E3FB37ED0AD"),
    seed("nether_quartz", 3, "nether quartz", "30DF8297FEEC9F22"),
    seed("certus_quartz", 3, "certus quartz", "47045A0E8E3457C2"),
    seed("obsidian", 3, "obsidian", "2581B7D8E6C6E510", fact="obsidian is volcanic glass: lava that cooled too fast to crystallise."),
    seed("prismarine", 3, "prismarine", "67AA59BD340FEC62"),
    seed("bronze", 3, "bronze", "7BC289DEF023FEAA", fact="bronze is copper with about 12% tin."),
    seed("brass", 3, "brass", "09282E3864752CEE", fact="brass is copper with zinc, usually 30 to 40%."),
    seed("sky_stone", 3, "sky stone", "7388D8168AF78B9A"),
    seed("steeleaf", 3, "steeleaf", "4D8B82FBA0FFD49E"),
    seed("ironwood", 3, "ironwood", "69F63F3B48E4344E"),
    # --- tier 3 mobs ----------------------------------------------------------------------------------------------
    seed("rabbit", 3, "rabbit hide, meat and feet", "38A77DBAD24C4B53", mob=True),
    seed("spider", 3, "string and spider eyes", "6A18B971C3DB83AE", mob=True),
    seed("skeleton", 3, "bones and arrows", "26A7746051A4A079", mob=True),
    seed("zombie", 3, "rotten flesh", "155A843A562DB7C4", mob=True),
    seed("creeper", 3, "gunpowder", "7ADE214373DE135F", mob=True, fact="gunpowder is the old black powder: about 75% potassium nitrate, 15% charcoal and 10% sulfur."),
    seed("phantom", 3, "phantom membranes", "7B7F7626FB6813FA", mob=True),
    # --- tier 4 crops (imperium farmland; MV circuit) ------------------------------------------------------------
    seed("gold", 4, "gold", "0AF5FB1B5AA5AA11"),
    seed("nickel", 4, "nickel", "25D84D82DBADA0DB"),
    seed("lapis_lazuli", 4, "lapis lazuli", "64B04D1CBC923789"),
    seed("end", 4, "End blocks", "248AEF5537E48B1A"),
    seed("electrum", 4, "electrum", "521C9B00B1D87DEB", fact="electrum is a natural gold-silver alloy; the first coins were struck from it."),
    seed("invar", 4, "invar", "70E4EBA7C9901007", fact="invar is iron with about 36% nickel, and barely expands when heated."),
    seed("soulium", 4, "soulium", "21F4CFF171246537"),
    seed("fluix", 4, "fluix", "3AD4367855B3E595"),
    seed("energized_steel", 4, "energized steel", "31EC6244E4A3CBD6"),
    seed("blazing_crystal", 4, "blazing crystal", "4A4C14AF947D93EF"),
    seed("fiery_ingot", 4, "fiery ingots", "4DF23FC932F5EB7D"),
    seed("knightmetal", 4, "knightmetal", "07751E1BE48C6024"),
    # --- tier 4 mobs ----------------------------------------------------------------------------------------------
    seed("blaze", 4, "blaze rods", "260F9C98DC2E485B", mob=True),
    seed("ghast", 4, "ghast tears", "4F0DD86CF6E5F1B5", mob=True),
    seed("enderman", 4, "ender pearls", "27E8ED4B5F8127F9", mob=True),
    seed("experience", 4, "experience", "07564DBB023EE2A6", mob=True, extra=[item(MA + "experience_capsule", 4)]),
    seed("breeze", 4, "breeze rods", "4530C14828C3D153", mob=True),
    # --- tier 5 crops (supremium farmland; HV circuit) -------------------------------------------------------------
    seed("diamond", 5, "diamonds", "6A2AD67569F91F1F"),
    seed("emerald", 5, "emeralds", "4E09BBC0BAED3440"),
    seed("netherite", 5, "netherite scrap", "06A7A3FC8634D2DA"),
    seed("niotic_crystal", 5, "niotic crystals", "15279CAC2FFE6B35"),
    seed("spirited_crystal", 5, "spirited crystals", "5F72C0C82F3C0310"),
    # --- tier 5 mobs ----------------------------------------------------------------------------------------------
    seed("wither_skeleton", 5, "wither skeleton skulls", "7CFA92CC48D1E7E3", mob=True),
], links=[("gs_iron", -3, 0), ("t3_analog", 8, 1.5), ("t4_mv", 10, 1.5), ("t5_hv", 12, 1.5), ("f_pot", 6, 7.5)], mirror="elmystical_agriculturerr")
