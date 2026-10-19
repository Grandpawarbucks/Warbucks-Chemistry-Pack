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

    # ===== ATM10-aligned round (2026-10-19): the vanilla farm, bees, the sea and the Nether =====
    Q("fd_garden", 0, 0, [item("minecraft:wheat_seeds", 16), item("minecraft:potato", 8), item("minecraft:carrot", 8), item("minecraft:melon_slice", 8), item("minecraft:sweet_berries", 8)],
      "Kitchen Garden", deps=["gs_farm"], xp=25, optional=True, tokens=1, subtitle="Optional: seeds, roots, melons and berries", desc=[
        "&eWhat:&r the vanilla crops beyond wheat: potatoes and carrots from village farms, melons from jungles, sweet berries from taiga.",
        "&eChemistry:&r a potato is mostly starch, long chains of glucose packed into grains. Cooking swells and bursts the grains (gelatinisation), which is why a baked potato is soft.",
        "&eHow:&r break grass for seeds, raid a village farm for potatoes and carrots, and replant everything.",
        "&eTip:&r sweet berry bushes hurt to walk through. Plant a row as a mob fence."]),
    Q("fd_barnyard", 0, 0, [anyof(["minecraft:beef", "minecraft:porkchop", "minecraft:mutton", "minecraft:chicken", "minecraft:rabbit"], 16),
                            item("minecraft:leather", 4), item("minecraft:feather", 4), item("minecraft:egg", 4)],
      "Barnyard Goods", deps=["fd_breed"], xp=30, optional=True, tokens=1, subtitle="Optional: everything a pen of animals gives", desc=[
        "&eWhat:&r 16 raw meat of any kind, plus leather, feathers and eggs: the steady output of a few animal pens.",
        "&eChemistry:&r an eggshell is about 95% calcium carbonate, CaCO₃: the same compound as chalk and limestone. Drop one in vinegar and it fizzes away as CO₂.",
        "&eHow:&r breed cows, pigs, sheep, chickens or rabbits and harvest the adults. Chickens lay eggs on their own.",
        "&eTip:&r cook meat before eating; raw chicken can give you Hunger."]),
    Q("fd_milk", 0, 0, [item("minecraft:milk_bucket")], "Milk", deps=["fd_breed", "gs_bucket"], xp=15,
      optional=True, tokens=1, subtitle="Optional: the cure for most status effects", desc=[
        "&eWhat:&r drinking milk clears every potion effect, good and bad. It's also a baking ingredient.",
        "&eChemistry:&r milk is an emulsion: fat droplets held in water by proteins (casein). Add acid and the casein clumps into curds, which is the first step of every cheese.",
        "&eHow:&r use an empty bucket on a cow (or a goat).",
        "&eTip:&r carry one into the Deep Dark or the Wither fight to wipe Darkness or Wither in one gulp."]),
    Q("fd_sugar", 0, 0, [item("minecraft:sugar", 16)], "Sugar", deps=["gs_opt_canes"], xp=15,
      optional=True, tokens=1, subtitle="Optional: crystallised sucrose", desc=[
        "&eWhat:&r sugar goes into cakes, pies, fermented spider eyes and speed potions.",
        "&eChemistry:&r table sugar is sucrose, C₁₂H₂₂O₁₁: a glucose and a fructose joined together. Heat it past about 160 °C and it breaks down into hundreds of brown, bitter-sweet compounds: caramel.",
        "&eHow:&r one sugar cane makes one sugar. A row of cane on Snad (Quality of Life page) grows fast.",
        "&eTip:&r the Alchemistry Dissolver splits sucrose into carbon, hydrogen and oxygen if you need the elements."]),
    Q("fd_baking", 0, 0, [item("minecraft:cake"), item("minecraft:pumpkin_pie", 2)], "Bake Sale", deps=["fd_sugar", "fd_milk", "fd_barnyard"], xp=30,
      optional=True, tokens=1, subtitle="Optional: a cake and two pies", desc=[
        "&eWhat:&r a cake (placed and eaten a slice at a time) and pumpkin pie, the best vanilla snack per bite.",
        "&eChemistry:&r baking is chemistry you can eat: egg proteins set the structure, sugar caramelises, and the Maillard reaction between sugars and proteins browns the crust.",
        "&eHow:&r cake: 3 milk buckets, 2 sugar, an egg and 3 wheat (you keep the buckets). Pie: a pumpkin, sugar and an egg.",
        "&eTip:&r a cake on the table in your base means nobody ever starves between trips."]),
    Q("fd_bees", 0, 0, [item("minecraft:honeycomb", 6), item("minecraft:honey_bottle", 4)], "Honey and Wax", deps=["gs_opt_campfire"], xp=30,
      optional=True, tokens=1, subtitle="Optional: rob a hive without being stung", desc=[
        "&eWhat:&r shears on a full bee nest give honeycomb; a glass bottle gives honey. Honeycomb waxes copper so it never tarnishes.",
        "&eChemistry:&r beeswax is mostly long esters (fatty acids joined to long alcohols). Wax on copper keeps out the air and water that would turn it green.",
        "&eHow:&r put a campfire under the nest first: the smoke keeps the bees calm. Then shear it or bottle it when it's dripping.",
        "&eTip:&r honey bottles cure poison and can be crafted into sugar."]),
    Q("fd_hive", 0, 0, [item("minecraft:beehive"), item("minecraft:honey_block", 2), item("minecraft:honeycomb_block", 2)], "An Apiary", deps=["fd_bees"], xp=40,
      optional=True, tokens=1, subtitle="Optional: your own hive and its blocks", desc=[
        "&eWhat:&r a beehive you can place where you like, plus the two honey blocks: sticky honey blocks and decorative honeycomb blocks.",
        "&eChemistry:&r honey is a supersaturated sugar solution, about 80% sugar in 17% water. That's why it slowly crystallises, and why bacteria can't live in it: the sugar pulls the water out of them.",
        "&eHow:&r a beehive is planks and honeycomb. A honey block is 4 honey bottles; a honeycomb block is 4 honeycomb. Lead bees home with flowers.",
        "&eTip:&r honey blocks slow anything on them and stop pistons pulling other blocks; great for flying machines."]),
    Q("fd_flowers", 0, 0, [anyof(["minecraft:dandelion", "minecraft:poppy", "minecraft:cornflower", "minecraft:blue_orchid", "minecraft:allium",
                                  "minecraft:azure_bluet", "minecraft:oxeye_daisy", "minecraft:lily_of_the_valley", "minecraft:red_tulip",
                                  "minecraft:orange_tulip", "minecraft:white_tulip", "minecraft:pink_tulip", "minecraft:torchflower"], 16)],
      "Wildflowers", deps=["f_knife"], xp=15, optional=True, tokens=1, subtitle="Optional: 16 flowers of any kind", desc=[
        "&eWhat:&r flowers make dyes, feed bees and decorate. Any 16 count.",
        "&eChemistry:&r many flower colours are anthocyanins, pigments that change colour with pH: the same molecule is red in acid and blue in alkali, like red cabbage indicator.",
        "&eHow:&r pick them in meadows and flower forests, or bone meal grass to grow more.",
        "&eTip:&r cornflower gives blue dye without lapis."]),
    Q("fd_bonemeal", 0, 0, [item("minecraft:bone_meal", 32)], "Bone Meal", deps=["f_compost"], xp=15,
      optional=True, tokens=1, subtitle="Optional: phosphate for your crops", desc=[
        "&eWhat:&r bone meal makes crops, saplings and flowers grow instantly.",
        "&eChemistry:&r bone is mostly hydroxyapatite, Ca₅(PO₄)₃(OH). Ground bone was one of the first phosphate fertilisers, before mined phosphate rock took over.",
        "&eHow:&r one bone makes 3 bone meal; a composter also turns plant scraps into it.",
        "&eTip:&r the NPK quests further along this page start from bone meal."]),
    Q("fd_hay", 0, 0, [item("minecraft:hay_block", 4)], "Hay Bales", deps=["fd_breed"], xp=10,
      optional=True, tokens=1, subtitle="Optional: wheat in bulk", desc=[
        "&eWhat:&r a hay bale is 9 wheat. Horses and llamas eat it, and landing on one cuts fall damage by 80%.",
        "&eHow:&r 9 wheat in the crafting grid.",
        "&eTip:&r a hay bale under a campfire makes the smoke rise much higher: a signal for friends."]),
    Q("fd_crates", 0, 0, [anyof(["farmersdelight:cabbage_crate", "farmersdelight:onion_crate", "farmersdelight:tomato_crate", "farmersdelight:carrot_crate",
                                 "farmersdelight:potato_crate", "farmersdelight:beetroot_crate", "farmersdelight:rice_bag"], 4)],
      "Crates and Bags", deps=["fd_crops"], xp=20, optional=True, tokens=1, subtitle="Optional: store a harvest in a block", desc=[
        "&eWhat:&r Farmer's Delight crates and bags hold 9 crops each and look good in a pantry. Any four.",
        "&eHow:&r 9 of the crop in the crafting grid (check JEI). Break one back into crops any time.",
        "&eTip:&r a wall of crates is a kitchen store that doubles as decoration."]),
    Q("fd_sea", 0, 0, [item("minecraft:kelp", 16), item("minecraft:dried_kelp", 16), item("minecraft:tropical_fish")], "From the Sea", deps=["gs_fish"], xp=25,
      optional=True, tokens=1, subtitle="Optional: kelp, and a bright fish", desc=[
        "&eWhat:&r kelp grows fast underwater; dried, it's a snack and (as a block) a good furnace fuel. Tropical fish come from fishing or warm oceans.",
        "&eChemistry:&r burnt kelp ash was the world's first source of iodine: Bernard Courtois found it in 1811 when sulfuric acid on seaweed ash gave off violet I₂ vapour. The ash was also a source of soda for glass.",
        "&eHow:&r harvest kelp, smelt it into dried kelp, and catch or bucket a tropical fish.",
        "&eTip:&r 9 dried kelp make a block that burns for 20 items in a furnace."]),
    Q("fd_nether_fungi", 0, 0, [item("minecraft:crimson_fungus", 4), item("minecraft:warped_fungus", 4)], "Nether Fungi", deps=["t2_nether", "fd_bonemeal"], xp=25,
      optional=True, tokens=1, subtitle="Optional: farm the Nether's forests", desc=[
        "&eWhat:&r crimson and warped fungi grow into huge Nether trees when bone-mealed on matching nylium. Warped fungus on a stick steers a strider.",
        "&eChemistry:&r real fungi aren't plants: their cell walls are chitin, the same polymer as insect shells, not cellulose.",
        "&eHow:&r pick them in the crimson and warped forests. Bone meal on nylium grows more.",
        "&eTip:&r hoglins run from warped fungus. Plant some around your Nether base."]),
    Q("fd_chorus", 0, 0, [item("minecraft:chorus_fruit", 16), item("minecraft:popped_chorus_fruit", 8)], "Chorus Orchard", deps=["w_end"], xp=30,
      optional=True, tokens=1, subtitle="Optional: the End's only crop", desc=[
        "&eWhat:&r chorus fruit teleports you a short way when eaten. Smelted, it becomes popped chorus fruit for purpur blocks, end rods and Silent Gear's glittery dust.",
        "&eHow:&r break chorus plants on the outer End islands, or plant a chorus flower on end stone and grow your own.",
        "&eTip:&r in this pack the Potion of Flying uses hydrogen, not chorus, so this crop is for building and Silent Gear."]),
    Q("fd_flax", 0, 0, [item("silentgear:flax_seeds", 4), item("silentgear:flax_string", 8)], "Flax", deps=["fd_crops"], xp=20,
      optional=True, tokens=1, subtitle="Optional: string without spiders", desc=[
        "&eWhat:&r Silent Gear's flax gives fibre for string, so bows and bindings don't depend on spider hunts.",
        "&eChemistry:&r flax fibre is nearly pure cellulose. Linen, made from it, is one of the oldest textiles, woven for over 30,000 years.",
        "&eHow:&r find flax seeds (check JEI for where they drop), grow them, and craft 2 flax fibre into a flax string.",
        "&eTip:&r flax flowers make blue dye too."]),
    Q("fd_netherite_hoe", 0, 0, [item("minecraft:netherite_hoe")], "Overqualified", deps=["hv_netherite"], xp=50,
      secret=True, loot="secret", subtitle="Secret: the most expensive way to till dirt", desc=[
        "&6You remember making forests grow with a word. Now you're upgrading a hoe with netherite. Priorities.&r",
        "&eWhat:&r a netherite hoe. It tills, it harvests leaves and sculk fast, and it cost you a netherite ingot.",
        "&eTip:&r hoes are the fastest tool for leaves, hay, moss and sculk. So it isn't entirely a joke."]),
], links=[("gs_food", -3, 0), ("t1_combiner", -3, 6), ("t4_reactor", -3, 7.5), ("t6_haber", -1.5, 7.5)])
