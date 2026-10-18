"""Quest chapter: farming. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("farming", "Farming", "botanypots:terracotta_hopper_botany_pot",
        ["Grow what you need, within the rules of chemistry."], SIDE, [
    # --- Farmer's Delight (y=0) ----------------------------------------------------------------
    Q("f_knife", 0, 0, [item("farmersdelight:flint_knife"), item("farmersdelight:cutting_board")], "Knife and Board", deps=["gs_food"], xp=15,
      subtitle="Farmer's Delight starts with a cut", desc=[
        "&6You remember feasts that lasted a week. Start with something smaller.&r",
        "&eWhat:&r Farmer's Delight adds crops, meals and kitchen blocks. The knife harvests straw and cuts ingredients.",
        "&eHow:&r craft a Flint Knife and a Cutting Board. Place items on the board and use the knife on them.",
        "&eTip:&r a knife on tall grass gives straw; wild crops (tomatoes, onions, cabbage, rice) grow in the wild."]),
    Q("f_cooking_pot", 2, 0, [item("farmersdelight:cooking_pot")], "Cooking Pot", deps=["f_knife"], xp=25,
      subtitle="Heat, ingredients, and a meal", desc=[
        "&eWhat:&r the Cooking Pot turns several ingredients into one meal. It needs heat underneath.",
        "&eChemistry:&r browning meat is the Maillard reaction: amino acids and sugars react above about 140 °C, making hundreds of flavour compounds.",
        "&eHow:&r iron, bricks, a wooden shovel and a water bucket (check JEI). Place it over a fire, campfire or Stove."]),
    Q("f_meal", 4, 0, [item("farmersdelight:vegetable_soup", 2)], "A Proper Meal", deps=["f_cooking_pot"], xp=30,
      subtitle="Food that keeps you full", desc=[
        "&eWhat:&r Farmer's Delight meals restore a lot of hunger and give long effects like Nourishment (hunger stops dropping) and Comfort.",
        "&eHow:&r cook vegetable soup in the Cooking Pot (check JEI), then bowl it.",
        "&eTip:&r a Feeding Upgrade in your backpack eats these for you."]),
    Q("f_compost", 1, -1.5, [item("farmersdelight:organic_compost"), item("farmersdelight:rich_soil", 4)], "Rich Soil", deps=["f_knife"], xp=30,
      optional=True, tokens=1, subtitle="Optional: compost into the best dirt", desc=[
        "&eWhat:&r organic compost slowly turns into Rich Soil, which grows crops faster and mushrooms into colonies.",
        "&eChemistry:&r composting is microbes breaking down organic matter with oxygen. They release CO₂ and heat, and leave humus rich in nitrogen.",
        "&eHow:&r craft compost from dirt, straw and bone meal plus rotten flesh or tree bark (check JEI), place it and wait."]),
    Q("f_feast", 5, -1.5, [item("farmersdelight:honey_glazed_ham_block")], "A Feast", deps=["f_meal"], xp=50,
      optional=True, tokens=1, subtitle="Optional: one block feeds the whole team", desc=[
        "&eWhat:&r feasts are placed as blocks and served with a bowl, several portions each.",
        "&eHow:&r cook a Honey Glazed Ham (check JEI). Place it on a table and right-click with bowls.",
        "&eTip:&r a feast is the easiest way to feed a whole team before a boss fight."]),

    # --- Botany Pots (y=2) ---------------------------------------------------------------------
    Q("f_pot", 0, 2, [item("botanypots:terracotta_hopper_botany_pot")], "Hopper Botany Pots", deps=["gs_food"], xp=25,
      subtitle="A farm in one block", desc=[
        "&eWhat:&r Hopper Botany Pots grow crops and push the harvest into the container below.",
        "&eHow:&r place one on a chest, add soil (dirt) and a seed.",
        "&eTip:&r Rich Soil or farmland grows faster than dirt, and Mystical Agriculture seeds work in pots too."]),

    # --- Mystical Agriculture (y=4) ------------------------------------------------------------
    Q("f_altar", 0, 4, [item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:inferium_essence", 16)], "Mystical Agriculture", deps=["f_pot"], xp=50,
      subtitle="Resource crops, made on an altar", desc=[
        "&eWhat:&r resource crops grow essence that crafts into real materials. Seeds are made on the Infusion Altar with Infusion Pedestals around it.",
        "&eHow:&r inferium ore gives inferium essence. Craft the altar and pedestals (check JEI).",
        "&eTip:&r &eTier 3/4/5 seeds need MI LV/MV/HV circuits&r, and crops for chemistry milestones (uranium, osmium, fluorite, silicon, steel, aluminum and others) can't be grown. Farming is a convenience here, not a shortcut."]),
    Q("f_prosperity", 2, 4, [item("mysticalagriculture:prosperity_shard", 8), item("mysticalagriculture:prosperity_seed_base")], "Prosperity", deps=["f_altar"], xp=40,
      subtitle="Shards for seed bases and crystals", desc=[
        "&eWhat:&r prosperity shards come from prosperity ore. They make seed bases (the core of every resource seed) and infusion crystals.",
        "&eHow:&r mine prosperity ore; 4 shards around wheat seeds make a Prosperity Seed Base.",
        "&eTip:&r Ultimine the veins; you'll want a lot of shards."]),
    Q("f_crystal", 4, 4, [item("mysticalagriculture:infusion_crystal")], "Infusion Crystal", deps=["f_prosperity"], xp=40,
      subtitle="The tool that upgrades essence", desc=[
        "&eWhat:&r a reusable crystal that combines lower essence into higher tiers.",
        "&eHow:&r a diamond, prosperity shards and inferium essence.",
        "&eTip:&r the Master Infusion Crystal never wears out; worth it once you have spare diamonds."]),
    Q("f_prudentium", 6, 4, [item("mysticalagriculture:prudentium_essence", 8)], "Prudentium", deps=["f_crystal"], xp=40,
      subtitle="Tier 2 essence", desc=[
        "&eWhat:&r the second essence tier, for tier 2 seeds (JEI lists every crop and its tier).",
        "&eHow:&r 4 inferium essence around an infusion crystal make 1 prudentium (check JEI).",
        "&eTip:&r it uncrafts back to inferium if you overshoot (check JEI)."]),
    Q("f_tertium", 8, 4, [item("mysticalagriculture:tertium_essence", 8)], "Tertium: LV Seeds", deps=["f_prudentium", "t3_analog"], xp=75,
      subtitle="Tier 3 seeds need an analog circuit", desc=[
        "&eWhat:&r tier 3 seeds (iron, copper, redstone, nether quartz, tin, lead and more) need Tertium essence and an &eMI analog circuit&r.",
        "&eChemistry:&r the analog circuit stands on steel, and steel stands on coke: coal baked without air until only carbon is left.",
        "&eHow:&r 4 prudentium around an infusion crystal make 1 tertium. Each seed type costs its circuit once; planted seeds multiply."]),
    Q("f_imperium", 10, 4, [item("mysticalagriculture:imperium_essence", 8)], "Imperium: MV Seeds", deps=["f_tertium", "t4_mv"], xp=100,
      subtitle="Tier 4 seeds need an electronic circuit", desc=[
        "&eWhat:&r tier 4 seeds (gold, lapis, nickel, blaze, enderman and more) need Imperium essence and an &eMI electronic circuit&r.",
        "&eChemistry:&r the electronic circuit needs aluminum, which only electrolysis can free from its oxide: 2Al₂O₃ → 4Al + 3O₂.",
        "&eHow:&r 4 tertium around an infusion crystal make 1 imperium."]),
    Q("f_supremium", 12, 4, [item("mysticalagriculture:supremium_essence", 8)], "Supremium: HV Seeds", deps=["f_imperium", "t5_hv"], xp=200,
      size=1.5, shape="hexagon", subtitle="Tier 5 seeds need a digital circuit", desc=[
        "&6You remember gardens that grew gold. These come close, and they still answer to chemistry.&r",
        "&eWhat:&r tier 5 seeds (diamond, emerald, netherite and more) need Supremium essence and an &eMI digital circuit&r.",
        "&eChemistry:&r the digital circuit needs polyethylene: thousands of ethylene units, C₂H₄, linked into one chain.",
        "&eHow:&r 4 imperium around an infusion crystal make 1 supremium."]),
    Q("f_accelerator", 1, 5.5, [item("mysticalagriculture:inferium_growth_accelerator", 4)], "Growth Accelerators", deps=["f_altar"], xp=40,
      optional=True, tokens=1, subtitle="Optional: crops grow faster above them", desc=[
        "&eWhat:&r growth accelerators placed below farmland speed up the crops above them. Stack several for more effect.",
        "&eHow:&r check JEI for each tier's recipe.",
        "&eTip:&r put them under the floor of your crop room so they're out of the way."]),
    Q("f_awakening", 13, 5.5, [item("mysticalagriculture:awakening_altar"), item("mysticalagriculture:awakened_supremium_essence", 4)], "Awakening", deps=["f_supremium"], xp=300,
      optional=True, tokens=2, subtitle="Optional: beyond supremium", desc=[
        "&eWhat:&r the Awakening Altar turns supremium into awakened supremium for the strongest Mystical Agriculture gear.",
        "&eHow:&r soulstone, gold and orange wool for the altar; JEI shows the awakening recipe and its essence vessels.",
        "&eTip:&r awakened supremium makes the best Mystical Agriculture tools and armour."]),
])
