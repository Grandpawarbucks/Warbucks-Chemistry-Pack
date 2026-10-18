"""Quest chapter: mystical (Mystical Agriculture). See tools/quests/STYLE.md."""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

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
      subtitle="Better soil for inferium crops", desc=[
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
      subtitle="Some seeds were removed on purpose", desc=[
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
      subtitle="Grow mob drops without the mobs", desc=[
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
      subtitle="Harvests and replants a field", desc=[
        "&eWhat:&r the Harvester picks mature crops in an area in front of it and replants them, pushing drops into its inventory.",
        "&eHow:&r machine frame, soulium ingots, iron and two diamond scythes (check JEI). Power it with FE.",
        "&eTip:&r pipe its output into storage and the field runs itself."]),
    Q("ma_extractor", 4, 5.5, [item("mysticalagriculture:soul_extractor")], "Soul Extractor", deps=["ma_frame", "ma_dagger"], xp=50,
      optional=True, tokens=1, subtitle="Optional: souls from mob drops", desc=[
        "&eWhat:&r fills Soul Jars from mob drops (rotten flesh, bones, string and more) instead of kills.",
        "&eHow:&r machine frame, soulium ingots, iron and a soulium dagger (check JEI). Power it with FE.",
        "&eTip:&r feed it drops from an HNN Simulation Chamber for a fully passive soul supply."]),
    Q("ma_pots", 6, 5.5, [item("botanypots:terracotta_hopper_botany_pot", 8), anytag("mysticalagriculture:seeds", 8)], "A Pot Farm", deps=["f_pot", "ma_seeds"], xp=60,
      subtitle="Eight hopper pots of resource crops", desc=[
        "&eWhat:&r Mystical Agriculture seeds grow in Hopper Botany Pots, which harvest by themselves into a chest below.",
        "&eHow:&r put each pot on a hopper, pipe or chest, add dirt or farmland and a seed. Hold any MA seed in JEI to see its pot growth time.",
        "&eTip:&r a column of pots over one shared item pipe is a compact essence farm for every tier."]),
], links=[("gs_iron", -3, 0), ("t3_analog", 8, 1.5), ("t4_mv", 10, 1.5), ("t5_hv", 12, 1.5), ("f_pot", 6, 7.5)])
