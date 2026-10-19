"""Quest chapter: mystical (Mystical Agriculture). See tools/quests/STYLE.md."""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

MA = "mysticalagriculture:"
TIERS = ["inferium", "prudentium", "tertium", "imperium", "supremium"]
ARMOR = [MA + t + "_" + p for t in TIERS + ["awakened_supremium"] for p in ("helmet", "chestplate", "leggings", "boots")]
WEAPONS = [MA + t + "_" + w for t in TIERS + ["awakened_supremium"] for w in ("sword", "bow", "crossbow", "fishing_rod")]
FARMLAND_UP = [MA + t + "_farmland" for t in TIERS[1:]]
ACCEL_UP = [MA + t + "_growth_accelerator" for t in TIERS[1:] + ["awakened_supremium"]]

CHAPTER = Chapter("mystical", "Mystical Agriculture", "mysticalagriculture:infusion_altar",
        ["Resource crops, within the rules of chemistry."], SIDE, [
    # --- Essence tiers: the spine (y=0) --------------------------------------------------------
    Q("f_altar", 0, 0, [item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:inferium_essence", 16)], "Mystical Agriculture", deps=["gs_iron"], xp=50,
      subtitle="Resource crops, made on an altar", desc=[
        "&6You remember coaxing metal out of the ground like wheat. Some of that still works.&r",
        "&eWhat:&r resource crops grow essence that crafts into real materials. Seeds are made on the Infusion Altar with Infusion Pedestals around it.",
        "&eHow:&r inferium ore gives inferium essence (mobs drop some too). The altar is gold, stone and red wool; pedestals are in JEI.",
        "&eTip:&r &eTier 3/4/5 seeds need MI LV/MV/HV circuits&r, and crops for chemistry milestones can't be grown at all. Farming is a convenience here, not a shortcut."]),
    Q("f_prosperity", 2, 0, [item("mysticalagriculture:prosperity_shard", 8), item("mysticalagriculture:prosperity_seed_base")], "Prosperity", deps=["f_altar"], xp=40,
      subtitle="Shards for seed bases and crystals", desc=[
        "&eWhat:&r prosperity shards come from prosperity ore. They make seed bases (the core of every resource seed) and infusion crystals.",
        "&eHow:&r mine prosperity ore; 4 shards around wheat seeds make a Prosperity Seed Base.",
        "&eTip:&r Ultimine the veins; you'll want a lot of shards."]),
    Q("f_crystal", 4, 0, [item("mysticalagriculture:infusion_crystal")], "Infusion Crystal", deps=["f_prosperity"], xp=40,
      subtitle="The tool that upgrades essence", desc=[
        "&eWhat:&r a crystal that combines lower essence into higher tiers. It wears out with use.",
        "&eHow:&r a diamond, prosperity shards and inferium essence (check JEI).",
        "&eTip:&r the Master Infusion Crystal never wears out; it comes much later, from supremium."]),
    Q("f_prudentium", 6, 0, [item("mysticalagriculture:prudentium_essence", 8)], "Prudentium", deps=["f_crystal"], xp=40,
      subtitle="Tier 2 essence", desc=[
        "&eWhat:&r the second essence tier, for tier 2 seeds (JEI lists every crop and its tier).",
        "&eHow:&r 4 inferium essence around an infusion crystal make 1 prudentium (check JEI).",
        "&eTip:&r it uncrafts back to inferium if you overshoot (check JEI)."]),
    Q("f_tertium", 8, 0, [item("mysticalagriculture:tertium_essence", 8)], "Tertium: LV Seeds", deps=["f_prudentium", "t3_analog"], xp=75,
      subtitle="Tier 3 seeds need an analog circuit", desc=[
        "&eWhat:&r tier 3 seeds (iron, copper, redstone, nether quartz, tin, lead and more) need Tertium essence and an &eMI analog circuit&r.",
        "&eChemistry:&r the analog circuit stands on steel, and steel stands on coke: coal baked without air until only carbon is left.",
        "&eHow:&r 4 prudentium around an infusion crystal make 1 tertium. Each seed type costs its circuit once; planted seeds multiply."]),
    Q("f_imperium", 10, 0, [item("mysticalagriculture:imperium_essence", 8)], "Imperium: MV Seeds", deps=["f_tertium", "t4_mv"], xp=100,
      subtitle="Tier 4 seeds need an electronic circuit", desc=[
        "&eWhat:&r tier 4 seeds (gold, lapis, nickel, blaze, enderman and more) need Imperium essence and an &eMI electronic circuit&r.",
        "&eChemistry:&r the electronic circuit needs aluminum, which only electrolysis can free from its oxide: 2Al₂O₃ → 4Al + 3O₂.",
        "&eHow:&r 4 tertium around an infusion crystal make 1 imperium."]),
    Q("f_supremium", 12, 0, [item("mysticalagriculture:supremium_essence", 8)], "Supremium: HV Seeds", deps=["f_imperium", "t5_hv"], xp=200,
      size=1.5, shape="hexagon", subtitle="Tier 5 seeds need a digital circuit", desc=[
        "&6You remember gardens that grew gold. These come close, and they still answer to chemistry.&r",
        "&eWhat:&r tier 5 seeds (diamond, emerald, netherite and more) need Supremium essence and an &eMI digital circuit&r.",
        "&eChemistry:&r the digital circuit needs polyethylene: thousands of ethylene units, C₂H₄, linked into one chain.",
        "&eHow:&r 4 imperium around an infusion crystal make 1 supremium."]),
    Q("f_accelerator", 1, 1.5, [item("mysticalagriculture:inferium_growth_accelerator", 4)], "Growth Accelerators", deps=["f_altar"], xp=40,
      optional=True, tokens=1, subtitle="Optional: crops grow faster above them", desc=[
        "&eWhat:&r growth accelerators placed below farmland speed up the crops above them. Stack several for more effect.",
        "&eHow:&r check JEI for each tier's recipe.",
        "&eTip:&r put them under the floor of your crop room so they're out of the way."]),
    Q("f_awakening", 14, 1.5, [item("mysticalagriculture:awakening_altar"), item("mysticalagriculture:awakened_supremium_essence", 4)], "Awakening", deps=["f_supremium"], xp=300,
      optional=True, tokens=2, subtitle="Optional: beyond supremium", desc=[
        "&eWhat:&r the Awakening Altar turns supremium into awakened supremium for the strongest Mystical Agriculture gear.",
        "&eHow:&r JEI shows the altar, its Awakening Pedestals, the Essence Vessels and the awakening recipe.",
        "&eTip:&r awakened supremium makes the best Mystical Agriculture tools and armour."]),
    Q("ma_master", 12, -2, [item("mysticalagriculture:master_infusion_crystal")], "Master Infusion Crystal", deps=["f_supremium"], xp=150,
      optional=True, tokens=2, subtitle="Optional: a crystal that never breaks", desc=[
        "&eWhat:&r an infusion crystal with no durability, so essence upgrades stop costing crystals.",
        "&eHow:&r a supremium gemstone, supremium essence and prosperity shards (check JEI).",
        "&eTip:&r worth it once you are mass-producing tertium and imperium for seeds."]),

    # --- First crops and farmland (y=-2) -------------------------------------------------------
    Q("ma_seeds", 0, -2, [anytag("mysticalagriculture:seeds", 4)], "Inferium Seeds", deps=["f_altar"], xp=30,
      subtitle="The crop that grows more essence", desc=[
        "&eWhat:&r Inferium Seeds grow inferium essence, the fuel for every higher tier. Any 4 Mystical Agriculture seeds complete this.",
        "&eHow:&r 8 inferium essence around wheat seeds in a crafting grid (no altar needed). Plant them on farmland and replant the extra seeds.",
        "&eTip:&r every other resource seed starts from a seed base on the altar, so build a big inferium field first."]),
    Q("ma_farmland", 2, -2, [item("mysticalagriculture:inferium_farmland", 8)], "Essence Farmland", deps=["ma_seeds"], xp=30,
      subtitle="Better soil for inferium crops", optional=True, tokens=1, desc=[
        "&eWhat:&r farmland infused with essence. Inferium crops drop more essence on higher-tier farmland.",
        "&eHow:&r one inferium essence plus one farmland, shapeless (check JEI). Higher tiers use their own essence.",
        "&eTip:&r upgrade the farmland under your inferium field as each new essence tier arrives."]),
    Q("ma_fertilizer", 4, -2, [item("mysticalagriculture:mystical_fertilizer", 4)], "Mystical Fertilizer", deps=["ma_seeds"], xp=30,
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
    Q("ma_can", 0, -4, [item("mysticalagriculture:watering_can")], "Watering Can", deps=["ma_seeds"], xp=25,
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
    Q("ma_dagger", 2, 3.5, [item("mysticalagriculture:soulium_dagger")], "Soulium Dagger", deps=["ma_soulium"], xp=40,
      subtitle="A blade that collects souls", desc=[
        "&eWhat:&r kills with this dagger capture the mob's soul into a Soul Jar in your inventory.",
        "&eHow:&r a golden sword, soulium ingots and soulium dust (check JEI).",
        "&eTip:&r JEI's soul extraction page shows how many souls each mob gives."]),
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
    Q("ma_harvester", 2, 5.5, [item("mysticalagriculture:harvester")], "Harvester", deps=["ma_frame"], xp=50,
      subtitle="Harvests and replants a field", optional=True, tokens=1, desc=[
        "&eWhat:&r the Harvester picks mature crops in an area in front of it and replants them, pushing drops into its inventory.",
        "&eHow:&r machine frame, soulium ingots, iron and two diamond scythes (check JEI). Power it with FE.",
        "&eTip:&r pipe its output into storage and the field runs itself."]),
    Q("ma_extractor", 4, 5.5, [item("mysticalagriculture:soul_extractor")], "Soul Extractor", deps=["ma_frame", "ma_dagger"], xp=50,
      optional=True, tokens=1, subtitle="Optional: souls from mob drops", desc=[
        "&eWhat:&r fills Soul Jars from mob drops (rotten flesh, bones, string and more) instead of kills.",
        "&eHow:&r machine frame, soulium ingots, iron and a soulium dagger (check JEI). Power it with FE.",
        "&eTip:&r feed it drops from an HNN Simulation Chamber for a fully passive soul supply."]),
    Q("ma_pots", 6, 5.5, [item("botanypots:terracotta_hopper_botany_pot", 8), anytag("mysticalagriculture:seeds", 8)], "A Pot Farm", deps=["f_pot", "ma_seeds"], xp=60,
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
    Q("ma_farmland_up", 0, 0, [anyof(FARMLAND_UP, 8)], "Better Farmland", deps=["ma_farmland", "f_prudentium"], xp=40,
      optional=True, tokens=1, subtitle="Optional: upgrade the soil under your inferium", desc=[
        "&eWhat:&r higher-tier farmland makes inferium crops drop more essence: prudentium, tertium, imperium or supremium.",
        "&eHow:&r one essence of the tier plus farmland (shapeless), or till dirt with a hoe and the essence.",
        "&eTip:&r it only boosts inferium crops; resource crops grow the same on any farmland."]),
    Q("ma_accel_up", 0, 0, [anyof(ACCEL_UP, 4)], "Stronger Accelerators", deps=["f_accelerator", "f_prudentium"], xp=40,
      optional=True, tokens=1, subtitle="Optional: faster growth from below", desc=[
        "&eWhat:&r higher-tier growth accelerators reach further and tick crops more often.",
        "&eHow:&r essence of the tier around stone and that tier's gemstone (makes 3; check JEI).",
        "&eTip:&r stack them in a column under the crop; each tier adds range."]),
    Q("ma_gear", 0, 0, [anyof(ARMOR)], "Essence Armor", deps=["ma_ingot"], xp=60,
      optional=True, tokens=1, subtitle="Optional: armor grown from a field", desc=[
        "&eWhat:&r Mystical Agriculture armor in six tiers, from inferium to awakened supremium. Higher tiers hold augments.",
        "&eHow:&r a diamond armor piece with two ingots and two gemstones of the tier (it keeps the item's enchantments). Each tier upgrades the last.",
        "&eTip:&r higher tiers also take augments; see the Augments quest."]),
    Q("ma_weapons", 0, 0, [anyof(WEAPONS)], "Essence Weapons", deps=["ma_ingot"], xp=60,
      optional=True, tokens=1, subtitle="Optional: swords, bows and a fishing rod", desc=[
        "&eWhat:&r essence swords, bows, crossbows and fishing rods, upgraded tier by tier like the armor.",
        "&eHow:&r the diamond (or plain) item with two ingots and two gemstones of the tier (check JEI).",
        "&eTip:&r a sword with the Mystical Enlightenment enchantment can collect Cognizant Dust from bosses."]),
    Q("ma_augments", 0, 0, [item(MA + "tinkering_table"), item(MA + "unattuned_augment")], "Augments", deps=["ma_gear", "ma_soulium"], xp=60,
      optional=True, tokens=1, subtitle="Optional: add powers to essence gear", desc=[
        "&eWhat:&r augments add effects to essence tools and armor (speed, night vision, mining area and more). The Tinkering Table fits them.",
        "&eHow:&r the table is stone and soulium dust. An Unattuned Augment is prosperity shards and iron; attune it on the altar (check JEI).",
        "&eTip:&r higher gear tiers have more augment slots."]),
    Q("ma_reprocessor", 0, 0, [item(MA + "seed_reprocessor")], "Seed Reprocessor", deps=["ma_frame"], xp=40,
      optional=True, tokens=1, subtitle="Optional: spare seeds back into essence", desc=[
        "&eWhat:&r grinds surplus resource seeds back into the essence they're made of, powered by FE.",
        "&eHow:&r a machine frame with soulium ingots, iron and 2 iron hoes.",
        "&eTip:&r feed it the extra seeds from a pot farm and nothing goes to waste."]),
    Q("ma_furnace", 0, 0, [item(MA + "furnace")], "Essence Furnace", deps=["ma_frame"], xp=30,
      optional=True, tokens=1, subtitle="Optional: an electric furnace", desc=[
        "&eWhat:&r a powered furnace that smelts with FE instead of burning fuel.",
        "&eChemistry:&r an electric furnace heats by resistance: current through a wire, P = I²R. No combustion, no CO₂ at the furnace.",
        "&eHow:&r a machine frame with iron, prosperity ingots and 2 furnaces."]),
    Q("ma_enchanter", 0, 0, [item(MA + "enchanter")], "Essence Enchanter", deps=["ma_soulium"], xp=50,
      optional=True, tokens=1, subtitle="Optional: enchant with essence, not luck", desc=[
        "&eWhat:&r applies the enchantment you pick, paid for with experience essence plus an item for each enchantment (check JEI for the costs).",
        "&eHow:&r an enchanting table on a soulium ingot over 3 soulstone.",
        "&eTip:&r it's the easy way to put Mystical Enlightenment on a sword."]),
    Q("ma_capsule", 0, 0, [item(MA + "experience_capsule")], "Experience Capsule", deps=["ma_jar"], xp=30,
      optional=True, tokens=1, subtitle="Optional: bottle your levels", desc=[
        "&eWhat:&r stores experience points picked up while it's in your inventory, to spend later.",
        "&eHow:&r 2 soulium ingots and 2 soul glass."]),
    Q("ma_spawner", 0, 0, [item(MA + "soulium_spawner")], "Soulium Spawner", deps=["ma_frame", "ma_souls"], xp=75,
      optional=True, tokens=1, subtitle="Optional: mobs from essence", desc=[
        "&eWhat:&r a powered spawner that turns mob essence into living mobs (JEI's Soulium Spawner page lists what each costs).",
        "&eHow:&r a machine frame with iron, soulium ingots and 2 wither skeleton skulls.",
        "&eTip:&r pair it with a mob grinder for drops crops can't grow, like XP."]),
    Q("ma_awaken_parts", 0, 0, [item(MA + "awakening_pedestal", 4), item(MA + "essence_vessel", 4)], "Awakening Rig", deps=["f_supremium", "ma_soulium"], xp=100,
      optional=True, tokens=1, subtitle="Optional: pedestals and vessels for the altar", desc=[
        "&eWhat:&r the Awakening Altar is fed by 4 Awakening Pedestals and 4 Essence Vessels holding air, earth, water and fire essence.",
        "&eHow:&r both are gold and soulstone, with orange wool (pedestal) or glass (vessel). JEI shows the layout.",
        "&eTip:&r fill the vessels before you start; awakening drains a lot of elemental essence."]),
    Q("ma_witherproof", 0, 0, [item(MA + "witherproof_bricks", 16)], "Witherproof Bricks", deps=["f_supremium", "ma_soulium"], xp=60,
      optional=True, tokens=1, subtitle="Optional: an arena the Wither can't break", desc=[
        "&eWhat:&r bricks the Wither's skulls can't destroy: build a box and fight it on your terms.",
        "&eHow:&r a witherproof block is soulstone in wither skeleton essence (a tier 5 crop); 4 blocks make 4 bricks.",
        "&eTip:&r the Seed of a New World needs Nether Stars, so a safe Wither arena pays for itself."]),
    Q("ma_cognizant", 0, 0, [item(MA + "cognizant_dust")], "Cognizant Dust", deps=["ma_weapons", "ma_enchanter"], xp=200,
      optional=True, tokens=2, subtitle="Optional: knowledge from a boss", desc=[
        "&6You remember learning from the strongest things you fought. Some of it is still on the floor.&r",
        "&eWhat:&r Cognizant Dust drops from the Wither and the Ender Dragon when they die to an essence weapon with Mystical Enlightenment.",
        "&eHow:&r enchant an essence sword in the Essence Enchanter, then land the last hit on a boss with it.",
        "&eTip:&r it goes into awakened supremium: JEI shows the awakening recipe."]),
], links=[("gs_iron", -3, 0), ("t3_analog", 8, 1.5), ("t4_mv", 10, 1.5), ("t5_hv", 12, 1.5), ("f_pot", 6, 7.5)])
