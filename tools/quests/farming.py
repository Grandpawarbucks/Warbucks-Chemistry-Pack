"""Quest chapter: farming (Farmer's Delight, Botany Pots, animals, fertiliser). See tools/quests/STYLE.md."""
from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("farming", "Farming and Food", "farmersdelight:cooking_pot",
        ["Grow what you need, cook it well, feed it back to the soil."], SIDE, [
    # --- Farmer's Delight: kitchen (y=0, -1.5, -3) ---------------------------------------------
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
    Q("fd_pasta", 6, 0, [item("farmersdelight:pasta_with_meatballs", 2)], "Pasta with Meatballs", deps=["f_meal", "fd_crops"], xp=40,
      optional=True, tokens=1, subtitle="Optional: four ingredients, three of them cooked first", desc=[
        "&eWhat:&r a hearty meal that chains every kitchen tool: knife (minced beef), board (raw pasta from dough) and pot (tomato sauce).",
        "&eChemistry:&r dough is starch and gluten proteins; water lets gluten chains cross-link into the stretchy network that holds pasta together.",
        "&eHow:&r follow the tree in JEI: wheat dough → raw pasta, beef → minced beef, tomatoes → tomato sauce, then the pot.",
        "&eTip:&r press U on any ingredient in JEI to see every meal that uses it."]),
    Q("fd_meals", 8, 0, [anytag("farmersdelight:meals", 6)], "A Varied Diet", deps=["fd_pasta"], xp=50,
      optional=True, tokens=1, subtitle="Optional: any six Farmer's Delight meals", desc=[
        "&eWhat:&r collect six bowls or plates of any Farmer's Delight meal: stews, soups, rice dishes, ratatouille, you choose.",
        "&eHow:&r anything in the 'meals' tag counts. Mix and match, they don't have to be different.",
        "&eTip:&r meals stack to 16; keep a stack in the backpack for long mining trips."]),
    Q("f_compost", 1, -1.5, [item("farmersdelight:organic_compost"), item("farmersdelight:rich_soil", 4)], "Rich Soil", deps=["f_knife"], xp=30,
      optional=True, tokens=1, subtitle="Optional: compost into the best dirt", desc=[
        "&eWhat:&r organic compost slowly turns into Rich Soil, which grows crops faster and mushrooms into colonies.",
        "&eChemistry:&r composting is microbes breaking down organic matter with oxygen. They release CO₂ and heat, and leave humus rich in nitrogen.",
        "&eHow:&r craft compost from dirt, straw and bone meal plus rotten flesh or tree bark (check JEI), place it and wait.",
        "&eTip:&r till Rich Soil with a hoe to get rich farmland for crops."]),
    Q("fd_stove", 3, -1.5, [item("farmersdelight:stove")], "The Stove", deps=["f_cooking_pot"], xp=25,
      optional=True, tokens=1, subtitle="Optional: a heat source that never burns out", desc=[
        "&eWhat:&r the Stove heats a Cooking Pot or Skillet on top and can grill up to six items on its own surface.",
        "&eHow:&r iron ingots, bricks and a campfire (check JEI). Light it with flint and steel.",
        "&eTip:&r unlike a campfire it doesn't need logs, and it looks right in a kitchen."]),
    Q("f_feast", 5, -1.5, [item("farmersdelight:honey_glazed_ham_block")], "A Feast", deps=["f_meal"], xp=50,
      optional=True, tokens=1, subtitle="Optional: one block feeds the whole team", desc=[
        "&eWhat:&r feasts are placed as blocks and served with a bowl, several portions each.",
        "&eHow:&r cook a Honey Glazed Ham (check JEI). Place it on a table and right-click with bowls.",
        "&eTip:&r a feast is the easiest way to feed a whole team before a boss fight."]),
    Q("fd_feasts", 7, -1.5, [item("farmersdelight:roast_chicken_block"), item("farmersdelight:shepherds_pie_block")], "Banquet", deps=["f_feast"], xp=75,
      optional=True, tokens=2, subtitle="Optional: roast chicken and shepherd's pie", desc=[
        "&eWhat:&r two more feasts for the table: a whole Roast Chicken and a Shepherd's Pie.",
        "&eHow:&r both come from the Cooking Pot (check JEI). Each needs a container, often a bowl, to serve.",
        "&eTip:&r place feasts where everyone passes, like next to the team's waystone."]),
    Q("fd_colony", 1, -3, [anytag("farmersdelight:mushroom_colonies", 2)], "Mushroom Colonies", deps=["f_compost"], xp=30,
      optional=True, tokens=1, subtitle="Optional: mushrooms that keep growing", desc=[
        "&eWhat:&r a mushroom on Rich Soil grows into a colony that you can harvest again and again.",
        "&eChemistry:&r fungi don't photosynthesise. They digest organic matter with enzymes, which is why rich, dark soil suits them.",
        "&eHow:&r plant a brown or red mushroom on Rich Soil in low light, wait, then harvest it with shears; the colony stays and regrows.",
        "&eTip:&r mushroom colonies are the steady source of mushrooms for stews and rice dishes."]),
    Q("fd_skillet", 3, -3, [item("farmersdelight:skillet")], "Skillet", deps=["fd_stove"], xp=25,
      optional=True, tokens=1, subtitle="Optional: fry it, or hit something with it", desc=[
        "&eWhat:&r a frying pan that cooks one item at a time over heat, and doubles as a surprisingly good weapon.",
        "&eHow:&r iron ingots and a brick (check JEI). Place it on the Stove or a campfire, or check its tooltip for cooking in hand.",
        "&eTip:&r Fire Aspect on a skillet sounds silly; it works."]),
    Q("fd_fried", 5, -3, [item("farmersdelight:fried_egg", 4), item("farmersdelight:cooked_bacon", 4)], "Breakfast", deps=["fd_skillet"], xp=30,
      optional=True, tokens=1, subtitle="Optional: eggs and bacon from the skillet", desc=[
        "&eWhat:&r the start of most Farmer's Delight breakfasts: fried eggs and cooked bacon.",
        "&eChemistry:&r egg white turns opaque as heat unfolds its proteins (denaturation) and they tangle together; it can't go back.",
        "&eHow:&r cut raw porkchop into bacon on the Cutting Board, then fry it and the eggs on the Skillet or Stove.",
        "&eTip:&r combine them into Bacon and Eggs in the Cooking Pot (check JEI)."]),

    # --- Crops (y=1.5) -------------------------------------------------------------------------
    Q("fd_crops", 1, 1.5, [item("farmersdelight:tomato", 4), item("farmersdelight:onion", 4), item("farmersdelight:cabbage", 4), item("farmersdelight:rice", 4)], "The New Crops",
      deps=["f_knife"], xp=30, subtitle="Tomatoes, onions, cabbage and rice", desc=[
        "&eWhat:&r Farmer's Delight crops are the base of nearly every meal.",
        "&eHow:&r find wild tomatoes, onions, cabbages and rice in the world (rice grows in shallow water). Break them for seeds and replant.",
        "&eTip:&r rice must be planted in water one block deep, like in a real paddy."]),
    Q("fd_rope", 3, 1.5, [item("farmersdelight:rope", 16)], "Tomatoes on a Rope", deps=["fd_crops"], xp=20,
      optional=True, tokens=1, subtitle="Optional: grow upward", desc=[
        "&eWhat:&r tomato vines climb rope, so a single plant grows several blocks tall and fruits all the way up.",
        "&eHow:&r craft rope from straw (check JEI), hang it above a tomato plant, and let the vine climb.",
        "&eTip:&r rope also lets you climb down mineshafts; right-click a placed rope to extend it downward."]),
    Q("fd_harvest", 5, 1.5, [anytag("c:crops", 128)], "Harvest Festival", deps=["fd_crops"], xp=60,
      optional=True, tokens=2, subtitle="Optional: 128 crops of any kind", desc=[
        "&eWhat:&r a full harvest: any 128 items from the shared crops tag (wheat, carrots, potatoes, tomatoes, rice and more).",
        "&eHow:&r a large field, Hopper Botany Pots, or an MI Farmer all count. Carry them in one go.",
        "&eTip:&r crop storage blocks (crates and bags) pack 9 crops each; you need the loose crops here."]),

    # --- Botany Pots (y=3) ---------------------------------------------------------------------
    Q("f_pot", 0, 3, [item("botanypots:terracotta_hopper_botany_pot")], "Hopper Botany Pots", deps=["f_knife"], xp=25,
      subtitle="A farm in one block", desc=[
        "&eWhat:&r Hopper Botany Pots grow crops and push the harvest into the container below.",
        "&eHow:&r place one on a chest, add soil (dirt) and a seed.",
        "&eTip:&r Rich Soil or farmland grows faster than dirt, and Mystical Agriculture seeds work in pots too."]),

    # --- Animals (y=4.5) -----------------------------------------------------------------------
    Q("fd_breed", 2, 4.5, [item("minecraft:lead", 2), item("minecraft:wheat", 16)], "Animal Husbandry", deps=["f_knife"], xp=20,
      optional=True, tokens=1, subtitle="Optional: breeding, explained by Just Enough Breeding", desc=[
        "&eWhat:&r cows, sheep, pigs and chickens give food, leather, wool and eggs. Two adults fed their favourite food make a baby.",
        "&eHow:&r lead two animals into a pen and feed them. Just Enough Breeding adds a JEI page per animal: look up any mob egg or food to see what it eats and what it drops.",
        "&eTip:&r babies take about 20 minutes to grow; feeding them their breeding food speeds that up."]),
    Q("fd_feed", 4, 4.5, [item("farmersdelight:horse_feed"), item("farmersdelight:dog_food")], "Pet Food", deps=["fd_breed", "f_knife"], xp=30,
      optional=True, tokens=1, subtitle="Optional: feed for horses and wolves", desc=[
        "&eWhat:&r Horse Feed heals and speeds up horses; Dog Food heals tamed wolves and gives them buffs.",
        "&eHow:&r both are Farmer's Delight crafting recipes (check JEI).",
        "&eTip:&r a well-fed wolf is a decent bodyguard in the early Twilight Forest."]),

    # --- Fertiliser chemistry (y=6) ------------------------------------------------------------
    Q("fd_npk_salts", 0, 6, [item("chemlib:urea"), item("chemlib:diammonium_phosphate"), item("chemlib:potassium_nitrate")], "N, P and K", deps=["t1_combiner"], xp=60,
      subtitle="The three numbers on every fertiliser bag", desc=[
        "&eWhat:&r plants need nitrogen (N), phosphorus (P) and potassium (K) more than anything else from the soil. These three compounds deliver them.",
        "&eChemistry:&r urea CO(NH₂)₂ is 46% nitrogen; diammonium phosphate (NH₄)₂HPO₄ carries N and P; potassium nitrate KNO₃ carries K and N.",
        "&eHow:&r make all three in the Alchemistry Combiner (check JEI for the element recipe of each).",
        "{@pagebreak}",
        "&eDeep dive: why nitrogen is the hard one.&r",
        "Air is 78% nitrogen, but N₂ has a triple bond that plants can't break. Only some soil bacteria (and lightning) can 'fix' it.",
        "In 1909 Fritz Haber found how to force N₂ + 3H₂ → 2NH₃ with a metal catalyst, high pressure and heat; Carl Bosch scaled it up.",
        "Today about half the nitrogen in your body passed through a Haber-Bosch plant. Ammonia is turned into urea, ammonium nitrate and phosphates.",
        "You'll build that same reaction in the main quests (Haber-Bosch, HV tier). Phosphorus comes from mined phosphate rock, and potassium from potash salts like KCl."]),
    Q("fd_npk", 2, 6, [item("extended_industrialization:npk_fertilizer_bucket")], "NPK Fertilizer", deps=["fd_npk_salts", "t4_reactor", "t4_acid"], xp=100,
      subtitle="Liquid fertiliser from the Chemical Reactor", desc=[
        "&eWhat:&r Extended Industrialization's NPK Fertilizer is a fluid the MI Farmer can spread to grow crops faster.",
        "&eChemistry:&r bone meal is calcium phosphate; sulfuric acid frees phosphoric acid, H₃PO₄, just like the real 'wet process' for phosphate rock.",
        "&eHow:&r Chemical Reactor, three steps (check JEI): bone meal + H₂SO₄ → phosphoric acid; potato/carrot/beetroot + water + HCl → potassium chloride, then KCl + H₂ + O₂ → potassium hydroxide; finally nitrogen + phosphoric acid + KOH → NPK Fertilizer.",
        "&eTip:&r real NPK plants start from ammonia, not raw nitrogen. Here the recipe takes the shortcut."]),
    Q("fd_farmer", 4, 6, [item("extended_industrialization:steam_farmer")], "The Steam Farmer", deps=["t3_analog", "t3_motor"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a multiblock that plants and harvests", desc=[
        "&eWhat:&r Extended Industrialization's Farmer is a multiblock that tills, plants, harvests and (with fertiliser) speeds up a whole field.",
        "&eHow:&r analog circuits, a motor, bronze plated bricks, a steel combine and a bronze pipe casing (check JEI). Its layout is in JEI and the MI guidebook.",
        "&eTip:&r the Electric Farmer is the upgrade. JEI has a fertiliser page that shows which fluids speed up a Farmer."]),

    # --- Secret ---------------------------------------------------------------------------------
    Q("fd_rotten", 7, 3, [item("farmersdelight:rotten_tomato", 8)], "Food Fight", deps=["fd_crops"], xp=25,
      secret=True, loot="secret", subtitle="Secret: ammunition, not dinner", desc=[
        "&eWhat:&r you found a use for spoiled tomatoes: rotten tomatoes can be thrown.",
        "&eChemistry:&r rotting is bacteria and fungi breaking sugars into acids, alcohols and gases. Don't eat it.",
        "&eTip:&r they're also good compost material. Probably better than throwing them at the team."]),
], links=[("gs_food", -3, 0), ("t1_combiner", -3, 6), ("t4_reactor", -3, 7.5), ("t6_haber", -1.5, 7.5)])
