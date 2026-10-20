"""Quest chapter: shop_world (shop group). See tools/quests/STYLE.md and docs/research/shop_brief.md.

The World stall of the Demigod's Market: repeatable buy-quests for building blocks and decoration, food and crops,
saplings and seeds, mob drops and dimension materials (Nether, End, Deeper and Darker, Undergarden, Twilight Forest,
space). Rule: you can only buy what you've already obtained yourself. Every entry depends on the quest where the player
first gets that item and stays invisible (locked_hidden) until then. Pay by handing in tokens (consume=True); the quest
resets after claiming (repeat=True).

Layout is manual (like shop_materials): one block per stall, each starting with a counter quest, entries 10 per line.
Blocks stack downwards automatically, so a long stall never overlaps the next one.
Prices (brief's "World goods" column): Steam 1-2 tokens (rare drops up to 3), Nether 1-3, LV 2-3 (shulker shells 8),
MV 2-4, HV 4-8, EV 1 Greater.
Not sold here: metals and ingots (shop_materials), boss trophies, Nether Stars, wither skulls, Dragon Egg, Elytra and
anything for flight (soul crystals), warden carapace, reinforced echo shards, echo shards, raw ores, ancient debris.
"""
from questlib import Q, Chapter, item, tick, SIDE  # noqa: F401

T = "kubejs:demigod_token"
G = "kubejs:greater_demigod_token"

PER_LINE = 10     # entries per line before wrapping
STEP_X = 1.5
STEP_Y = 1.5
GAP = 3.0         # space between one stall's last line and the next counter
_rows = []        # [counter y, entry count]

# Titles of the unlock quests (other chapters), shown in each entry's subtitle.
TITLES = {
    "gs_stone": "Stone Age", "bd_rocks": "Know Your Rocks", "gs_logs": "Punch a Tree", "gs_opt_glass": "Glass",
    "bd_masonry": "Masonry", "t1_bricks": "A Kiln's Worth of Bricks", "bd_concrete": "Terracotta and Concrete",
    "bd_ice": "Building with Ice", "bd_dripstone": "Dripstone", "bd_ru_stones": "Rocks of Other Biomes",
    "bd_lab": "Laboratory Blocks", "bd_framed": "Framed Blocks", "gs_opt_shears": "Shearing Season",
    "bd_froglights": "Froglights", "hn_guardian": "Guardian Hunter", "ex_monument": "An Ocean Monument",
    "gs_food": "Something to Eat", "gs_meat": "Cooked Meat", "gs_fish": "Gone Fishing", "fd_breed": "Animal Husbandry",
    "fd_garden": "Kitchen Garden", "gs_opt_canes": "Sugar Cane", "fd_sugar": "Sugar", "fd_barnyard": "Barnyard Goods",
    "fd_milk": "Milk", "fd_crops": "The New Crops", "f_meal": "A Proper Meal", "fd_pasta": "Pasta with Meatballs",
    "f_feast": "A Feast", "fd_bees": "Honey and Wax", "fd_baking": "Bake Sale", "fd_sea": "From the Sea",
    "fd_hay": "Hay Bales", "f_compost": "Rich Soil", "fd_bonemeal": "Bone Meal", "fd_flax": "Flax",
    "cp_saplings": "Every Vanilla Tree", "ars_saplings": "Four Archwoods", "hn_spoil_flesh": "Spoils: Rotten Flesh",
    "hn_spoil_bone": "Spoils: Bones", "hn_spoil_spider": "Spoils: Silk and Eyes", "gs_leather": "Leather Armour",
    "hn_creeper_1": "Creeper Hunter", "hn_slime": "Slime Time", "hv_wolf_armor": "Armour for a Friend",
    "hn_trials": "The Trials", "t2_nether": "Into the Fire", "t2_blackstone": "Blackstone",
    "t2_fortress": "Fortress Found", "t2_quartz": "Nether Quartz", "t2_wart": "Nether Wart",
    "bd_lights": "Lighting Without Torches", "fd_nether_fungi": "Nether Fungi", "t2_blaze": "Blaze Rods",
    "t2_fireres": "Fire Resistance", "t2_ghast": "Ghast Tears", "t2_slowfall": "Slow Falling",
    "t2_opt_ender": "Eyes of Ender", "t2_obsidian": "A Door of Fire", "bd_end_stone": "End Stone",
    "fd_chorus": "Chorus Orchard", "w_dragon": "The Dragon's Breath", "w_elytra": "End City Loot",
    "dd_stones": "Sculk Stone and Gloomslate", "dd_sludge": "Resonarium", "dd_echo_wood": "Echo Trees",
    "dd_blooming": "Blooming Caverns", "dd_soul": "Soul Materials", "dd_grime": "Grime Bricks",
    "dd_gleam": "Light in the Dark", "dd_sculk_gleam": "Sculk Gleam", "dd_living_ground": "Living Ground",
    "dd_angler": "Angler Fish", "ug_arrival": "Depthrock", "ug_woods": "Woods Without Sun",
    "ug_saplings": "Saplings of the Dark", "ug_beans": "Underbeans", "ug_underbeans": "Roasted Underbeans",
    "ug_gloomgourd": "Gloomgourds", "ug_meat": "Hunter's Supper", "ug_berries": "Blisterberries",
    "ug_glow_food": "Droopfruit and Glitterkelp", "ug_mogmoss": "Mogmoss", "ug_goo": "Scintling Goo",
    "ug_shard_torch": "Shard Torches", "ug_mushrooms": "Four Mushrooms", "ug_rogdorium": "Rogdorium",
    "ug_rotbelcher": "The Rotbelcher", "ug_brute": "Brutes", "ug_gwibling": "Weird Fish", "tf_oak": "Wood of Dusk",
    "tf_focus_parts": "Feather and Berries", "tf_ironwood": "Ironwood", "tf_venison": "Venison", "tf_meef": "Meef",
    "tf_maze_wafer": "Maze Wafers", "tf_arctic": "Arctic Fur", "tf_armor_shards": "Armour Shards",
    "tf_carminite": "Carminite", "w_naga": "The Naga", "tf_thorn_rose": "Thorn Roses", "tf_uberous": "Uberous Soil",
    "tf_castle_bricks": "Castle Stone", "tf_alpha_fur": "Alpha Yeti Fur", "t7_rocket": "One Small Step",
    "w_mars": "Mars", "w_venus": "Venus", "w_mercury": "Mercury", "w_glacio": "Glacio",
    "w_cheese": "The Moon Is Cheese", "sp_mars_poles": "The Polar Caps",
}


def _price(n, greater):
    if greater:
        return f"{n} Greater" if n > 1 else "1 Greater"
    return f"{n} tokens" if n > 1 else "1 token"


def counter(key, title, dep, sub, desc):
    """Stall header: a short optional checkmark, placed below the previous stall's last line."""
    if _rows:
        y0, n = _rows[-1]
        y = y0 + STEP_Y * ((max(n, 1) - 1) // PER_LINE) + GAP
    else:
        y = 0
    _rows.append([y, 0])
    return Q(key, 0, y, [tick()], title, deps=[dep], tokens=0, xp=0, optional=True, size=1.5,
             subtitle=sub, desc=desc)


def buy(name, title, item_id, count, price, dep, what, greater=False):
    """One shop entry: pay `price` (Greater) tokens, get `count` of `item_id`. Placed on the current stall."""
    row = _rows[-1]
    i = row[1]
    row[1] += 1
    x = STEP_X * (1 + i % PER_LINE)
    y = row[0] + STEP_Y * (i // PER_LINE)
    cost = item(G if greater else T, price)
    return Q(f"sw_buy_{name}", x, y, [cost], title, deps=[dep], items=[(item_id, count)],
             tokens=0, xp=0, optional=True, repeat=True, consume=True, locked_hidden=True,
             subtitle=f"{_price(price, greater)} · unlocked by {TITLES[dep]}",
             desc=[f"&eWhat:&r {what}"])


def g(*a, **k):
    """Shorthand for an entry paid in Greater Demigod Tokens."""
    return buy(*a, greater=True, **k)


QUESTS = [
    Q("sw_intro", 0, -3, [tick()], "The World Stall", deps=["wel_tokens"], tokens=0, xp=10, optional=True,
      size=1.5, subtitle="Buy more of what you've already gathered", desc=[
          "&6You remember the harvest festivals held in your name. The world still sends its gifts.&r",
          "&eWhat:&r this stall sells building blocks, food, crops, saplings, mob drops and the stone and plants of other worlds.",
          "&eHow:&r an item appears here only after the quest where you first got it. Hand in the tokens and claim the bundle; the entry resets so you can buy again.",
          "&eTip:&r tokens save gathering, never exploring. Each world's goods only appear once you've been there.",
          "&eTip:&r the space stall costs Greater Demigod Tokens (1 Greater = 9 tokens; craft them in a grid)."]),

    # --- Steam: the Overworld ------------------------------------------------------------------------
    counter("sw_row_steam", "Overworld Stall", "t0_boiler", "Stone, wood, food and farm goods", [
        "&eWhat:&r the Steam-age stall: Overworld blocks, crops, saplings and common mob drops.",
        "&eHow:&r entries show up one by one as you finish the quests where you first gathered them."]),
    # building
    buy("cobblestone", "Cobblestone", "minecraft:cobblestone", 64, 1, "gs_stone", "64 cobblestone."),
    buy("stone", "Stone", "minecraft:stone", 64, 1, "bd_rocks", "64 smooth stone blocks, already smelted."),
    buy("oak_log", "Oak Logs", "minecraft:oak_log", 32, 1, "gs_logs", "32 oak logs."),
    buy("glass", "Glass", "minecraft:glass", 32, 1, "gs_opt_glass", "32 glass blocks (sand melted into SiO₂ glass)."),
    buy("clay_ball", "Clay", "minecraft:clay_ball", 32, 1, "bd_masonry", "32 clay balls for bricks and fire clay."),
    buy("bricks", "Bricks", "minecraft:bricks", 32, 2, "t1_bricks", "32 brick blocks."),
    buy("terracotta", "Terracotta", "minecraft:terracotta", 32, 1, "bd_concrete", "32 plain terracotta, ready to dye."),
    buy("concrete_powder", "White Concrete Powder", "minecraft:white_concrete_powder", 32, 1, "bd_concrete",
        "32 white concrete powder. Touch it to water to set it."),
    buy("packed_ice", "Packed Ice", "minecraft:packed_ice", 16, 2, "bd_ice", "16 packed ice."),
    buy("dripstone", "Dripstone Blocks", "minecraft:dripstone_block", 32, 1, "bd_dripstone",
        "32 dripstone blocks (calcium carbonate, CaCO₃)."),
    buy("chalk", "Chalk", "regions_unexplored:chalk", 32, 1, "bd_ru_stones", "32 chalk blocks, soft white CaCO₃ stone."),
    buy("lab_block", "Laboratory Blocks", "laboratoryblocks:laboratory_block", 16, 1, "bd_lab",
        "16 clean white laboratory blocks."),
    buy("framed_cube", "Framed Cubes", "framedblocks:framed_cube", 32, 1, "bd_framed", "32 framed cubes to disguise."),
    buy("wool", "White Wool", "minecraft:white_wool", 32, 1, "gs_opt_shears", "32 white wool."),
    buy("ochre_froglight", "Ochre Froglights", "minecraft:ochre_froglight", 8, 2, "bd_froglights", "8 ochre froglights."),
    buy("verdant_froglight", "Verdant Froglights", "minecraft:verdant_froglight", 8, 2, "bd_froglights",
        "8 verdant froglights."),
    buy("pearl_froglight", "Pearlescent Froglights", "minecraft:pearlescent_froglight", 8, 2, "bd_froglights",
        "8 pearlescent froglights."),
    buy("prismarine_shard", "Prismarine Shards", "minecraft:prismarine_shard", 16, 2, "hn_guardian",
        "16 prismarine shards from guardians."),
    buy("wet_sponge", "Wet Sponges", "minecraft:wet_sponge", 2, 2, "ex_monument", "2 wet sponges. Dry them in a furnace."),
    # food and crops
    buy("bread", "Bread", "minecraft:bread", 16, 1, "gs_food", "16 bread."),
    buy("cooked_beef", "Steak", "minecraft:cooked_beef", 16, 1, "gs_meat", "16 steaks."),
    buy("cooked_cod", "Cooked Cod", "minecraft:cooked_cod", 16, 1, "gs_fish", "16 cooked cod."),
    buy("wheat", "Wheat", "minecraft:wheat", 64, 1, "fd_breed", "64 wheat."),
    buy("potato", "Potatoes", "minecraft:potato", 32, 1, "fd_garden", "32 potatoes."),
    buy("carrot", "Carrots", "minecraft:carrot", 32, 1, "fd_garden", "32 carrots."),
    buy("melon_slice", "Melon Slices", "minecraft:melon_slice", 32, 1, "fd_garden", "32 melon slices."),
    buy("sweet_berries", "Sweet Berries", "minecraft:sweet_berries", 32, 1, "fd_garden", "32 sweet berries."),
    buy("sugar_cane", "Sugar Cane", "minecraft:sugar_cane", 32, 1, "gs_opt_canes", "32 sugar cane."),
    buy("sugar", "Sugar", "minecraft:sugar", 32, 1, "fd_sugar", "32 sugar (sucrose, C₁₂H₂₂O₁₁)."),
    buy("egg", "Eggs", "minecraft:egg", 16, 1, "fd_barnyard", "16 eggs."),
    buy("milk", "Milk", "minecraft:milk_bucket", 1, 1, "fd_milk", "A bucket of milk (bucket included)."),
    buy("tomato", "Tomatoes", "farmersdelight:tomato", 32, 1, "fd_crops", "32 tomatoes."),
    buy("onion", "Onions", "farmersdelight:onion", 32, 1, "fd_crops", "32 onions."),
    buy("cabbage", "Cabbages", "farmersdelight:cabbage", 32, 1, "fd_crops", "32 cabbages."),
    buy("rice", "Rice", "farmersdelight:rice", 32, 1, "fd_crops", "32 rice."),
    buy("vegetable_soup", "Vegetable Soup", "farmersdelight:vegetable_soup", 4, 1, "f_meal", "4 bowls of vegetable soup."),
    buy("pasta", "Pasta with Meatballs", "farmersdelight:pasta_with_meatballs", 4, 2, "fd_pasta",
        "4 plates of pasta with meatballs."),
    buy("ham", "Honey Glazed Ham", "farmersdelight:honey_glazed_ham_block", 1, 2, "f_feast",
        "A whole honey glazed ham feast. Place it and serve slices."),
    buy("honeycomb", "Honeycomb", "minecraft:honeycomb", 16, 2, "fd_bees", "16 honeycomb."),
    buy("honey_bottle", "Honey Bottles", "minecraft:honey_bottle", 8, 1, "fd_bees", "8 honey bottles."),
    buy("cake", "Cake", "minecraft:cake", 1, 1, "fd_baking", "One cake."),
    buy("kelp", "Kelp", "minecraft:kelp", 32, 1, "fd_sea", "32 kelp."),
    buy("hay", "Hay Bales", "minecraft:hay_block", 8, 1, "fd_hay", "8 hay bales."),
    buy("rich_soil", "Rich Soil", "farmersdelight:rich_soil", 16, 2, "f_compost", "16 rich soil."),
    buy("bone_meal", "Bone Meal", "minecraft:bone_meal", 32, 1, "fd_bonemeal", "32 bone meal (mostly calcium phosphate)."),
    # saplings and seeds
    buy("wheat_seeds", "Wheat Seeds", "minecraft:wheat_seeds", 32, 1, "fd_garden", "32 wheat seeds."),
    buy("tomato_seeds", "Tomato Seeds", "farmersdelight:tomato_seeds", 16, 1, "fd_crops", "16 tomato seeds."),
    buy("cabbage_seeds", "Cabbage Seeds", "farmersdelight:cabbage_seeds", 16, 1, "fd_crops", "16 cabbage seeds."),
    buy("flax_seeds", "Flax Seeds", "silentgear:flax_seeds", 16, 1, "fd_flax", "16 flax seeds."),
    buy("oak_sapling", "Oak Saplings", "minecraft:oak_sapling", 8, 1, "cp_saplings", "8 oak saplings."),
    buy("spruce_sapling", "Spruce Saplings", "minecraft:spruce_sapling", 8, 1, "cp_saplings", "8 spruce saplings."),
    buy("birch_sapling", "Birch Saplings", "minecraft:birch_sapling", 8, 1, "cp_saplings", "8 birch saplings."),
    buy("jungle_sapling", "Jungle Saplings", "minecraft:jungle_sapling", 8, 1, "cp_saplings", "8 jungle saplings."),
    buy("acacia_sapling", "Acacia Saplings", "minecraft:acacia_sapling", 8, 1, "cp_saplings", "8 acacia saplings."),
    buy("dark_oak_sapling", "Dark Oak Saplings", "minecraft:dark_oak_sapling", 8, 1, "cp_saplings",
        "8 dark oak saplings (plant them 2x2)."),
    buy("cherry_sapling", "Cherry Saplings", "minecraft:cherry_sapling", 8, 1, "cp_saplings", "8 cherry saplings."),
    buy("mangrove", "Mangrove Propagules", "minecraft:mangrove_propagule", 8, 1, "cp_saplings", "8 mangrove propagules."),
    buy("red_archwood", "Red Archwood Saplings", "ars_nouveau:red_archwood_sapling", 4, 2, "ars_saplings",
        "4 red archwood saplings."),
    buy("blue_archwood", "Blue Archwood Saplings", "ars_nouveau:blue_archwood_sapling", 4, 2, "ars_saplings",
        "4 blue archwood saplings."),
    buy("green_archwood", "Green Archwood Saplings", "ars_nouveau:green_archwood_sapling", 4, 2, "ars_saplings",
        "4 green archwood saplings."),
    buy("purple_archwood", "Purple Archwood Saplings", "ars_nouveau:purple_archwood_sapling", 4, 2, "ars_saplings",
        "4 purple archwood saplings."),
    # mob drops
    buy("rotten_flesh", "Rotten Flesh", "minecraft:rotten_flesh", 32, 1, "hn_spoil_flesh", "32 rotten flesh."),
    buy("bone", "Bones", "minecraft:bone", 32, 1, "hn_spoil_bone", "32 bones."),
    buy("string", "String", "minecraft:string", 32, 1, "hn_spoil_spider", "32 string."),
    buy("spider_eye", "Spider Eyes", "minecraft:spider_eye", 16, 1, "hn_spoil_spider", "16 spider eyes."),
    buy("leather", "Leather", "minecraft:leather", 16, 2, "gs_leather", "16 leather."),
    buy("feather", "Feathers", "minecraft:feather", 32, 1, "fd_barnyard", "32 feathers."),
    buy("gunpowder", "Gunpowder", "minecraft:gunpowder", 16, 2, "hn_creeper_1",
        "16 gunpowder (in real life: saltpetre, charcoal and sulfur)."),
    buy("slime_ball", "Slimeballs", "minecraft:slime_ball", 16, 2, "hn_slime", "16 slimeballs."),
    buy("scute", "Armadillo Scutes", "minecraft:armadillo_scute", 4, 2, "hv_wolf_armor", "4 armadillo scutes."),
    buy("breeze_rod", "Breeze Rods", "minecraft:breeze_rod", 2, 2, "hn_trials", "2 breeze rods from the Trial Chambers."),

    # --- Steam: the Nether --------------------------------------------------------------------------
    counter("sw_row_nether", "Nether Stall", "t2_nether", "Blocks and drops from the fire", [
        "&eWhat:&r Nether blocks, fungi and the drops of its mobs.",
        "&eHow:&r opens once you've been through the portal; each entry follows its own quest."]),
    buy("netherrack", "Netherrack", "minecraft:netherrack", 64, 1, "t2_nether", "64 netherrack."),
    buy("soul_sand", "Soul Sand", "minecraft:soul_sand", 32, 1, "t2_nether", "32 soul sand."),
    buy("blackstone", "Blackstone", "minecraft:blackstone", 64, 1, "t2_blackstone", "64 blackstone."),
    buy("nether_brick", "Nether Bricks", "minecraft:nether_brick", 32, 1, "t2_fortress", "32 nether brick items."),
    buy("obsidian", "Obsidian", "minecraft:obsidian", 16, 2, "t2_obsidian", "16 obsidian (volcanic glass)."),
    buy("quartz", "Nether Quartz", "minecraft:quartz", 32, 2, "t2_quartz", "32 nether quartz (SiO₂)."),
    buy("glowstone_dust", "Glowstone Dust", "minecraft:glowstone_dust", 32, 2, "bd_lights", "32 glowstone dust."),
    buy("nether_wart", "Nether Wart", "minecraft:nether_wart", 16, 1, "t2_wart", "16 nether wart for brewing."),
    buy("crimson_fungus", "Crimson Fungus", "minecraft:crimson_fungus", 8, 1, "fd_nether_fungi", "8 crimson fungi."),
    buy("warped_fungus", "Warped Fungus", "minecraft:warped_fungus", 8, 1, "fd_nether_fungi", "8 warped fungi."),
    buy("blaze_rod", "Blaze Rods", "minecraft:blaze_rod", 4, 3, "t2_blaze", "4 blaze rods."),
    buy("magma_cream", "Magma Cream", "minecraft:magma_cream", 8, 2, "t2_fireres", "8 magma cream."),
    buy("ghast_tear", "Ghast Tears", "minecraft:ghast_tear", 2, 3, "t2_ghast", "2 ghast tears."),
    buy("phantom_membrane", "Phantom Membranes", "minecraft:phantom_membrane", 4, 2, "t2_slowfall",
        "4 phantom membranes."),
    buy("ender_pearl", "Ender Pearls", "minecraft:ender_pearl", 4, 2, "t2_opt_ender", "4 ender pearls."),

    # --- LV: the End and the Otherside -----------------------------------------------------------------
    counter("sw_row_lv", "End and Otherside Stall", "t3_hull", "The End's stone and the deep dark", [
        "&eWhat:&r End stone, chorus, End drops and the blocks and plants of the Otherside (Deeper and Darker).",
        "&eHow:&r each entry appears after you've brought that thing home yourself."]),
    buy("end_stone", "End Stone", "minecraft:end_stone", 64, 2, "bd_end_stone", "64 end stone."),
    buy("end_stone_bricks", "End Stone Bricks", "minecraft:end_stone_bricks", 32, 2, "bd_end_stone", "32 end stone bricks."),
    buy("chorus_fruit", "Chorus Fruit", "minecraft:chorus_fruit", 16, 2, "fd_chorus", "16 chorus fruit."),
    buy("popped_chorus", "Popped Chorus Fruit", "minecraft:popped_chorus_fruit", 16, 2, "fd_chorus",
        "16 popped chorus fruit for purpur."),
    buy("dragon_breath", "Dragon's Breath", "minecraft:dragon_breath", 4, 3, "w_dragon", "4 bottles of dragon's breath."),
    buy("shulker_shell", "Shulker Shells", "minecraft:shulker_shell", 2, 8, "w_elytra", "2 shulker shells (one shulker box)."),
    buy("sculk_stone", "Sculk Stone", "deeperdarker:sculk_stone", 64, 2, "dd_stones", "64 sculk stone."),
    buy("gloomslate", "Gloomslate", "deeperdarker:gloomslate", 64, 2, "dd_stones", "64 gloomslate."),
    buy("resonarium", "Resonarium", "deeperdarker:resonarium", 8, 3, "dd_sludge", "8 resonarium."),
    buy("echo_log", "Echo Logs", "deeperdarker:echo_log", 32, 2, "dd_echo_wood", "32 echo logs."),
    buy("echo_sapling", "Echo Saplings", "deeperdarker:echo_sapling", 4, 2, "dd_echo_wood", "4 echo saplings."),
    buy("blooming_stem", "Blooming Stems", "deeperdarker:blooming_stem", 32, 2, "dd_blooming", "32 blooming stems."),
    buy("bloom_berries", "Bloom Berries", "deeperdarker:bloom_berries", 16, 2, "dd_blooming", "16 bloom berries."),
    buy("soul_dust", "Soul Dust", "deeperdarker:soul_dust", 16, 3, "dd_soul", "16 soul dust."),
    buy("sculk_bone", "Sculk Bones", "deeperdarker:sculk_bone", 8, 3, "dd_soul", "8 sculk bones."),
    buy("grime_brick", "Grime Bricks", "deeperdarker:grime_brick", 32, 2, "dd_grime", "32 grime bricks."),
    buy("gloomslate_light", "Gloomslate Lights", "deeperdarker:gloomslate_light", 8, 2, "dd_gleam", "8 gloomslate lights."),
    buy("sculk_gleam", "Sculk Gleam", "deeperdarker:sculk_gleam", 8, 2, "dd_sculk_gleam", "8 sculk gleam."),
    buy("echo_soil", "Echo Soil", "deeperdarker:echo_soil", 16, 2, "dd_living_ground", "16 echo soil."),
    buy("angler_fish", "Cooked Angler Fish", "deeperdarker:cooked_angler_fish", 8, 2, "dd_angler", "8 cooked angler fish."),

    # --- MV: the Undergarden ---------------------------------------------------------------------------
    counter("sw_row_mv", "Undergarden Stall", "t4_mv", "Stone, wood and food from below", [
        "&eWhat:&r Undergarden stone, sunless wood, strange food and its creatures' drops.",
        "&eHow:&r each entry appears after the Undergarden quest where you first found it."]),
    buy("depthrock", "Depthrock", "undergarden:depthrock", 64, 2, "ug_arrival", "64 depthrock."),
    buy("smogstem_log", "Smogstem Logs", "undergarden:smogstem_log", 32, 2, "ug_woods", "32 smogstem logs."),
    buy("wigglewood_log", "Wigglewood Logs", "undergarden:wigglewood_log", 32, 2, "ug_woods", "32 wigglewood logs."),
    buy("grongle_log", "Grongle Logs", "undergarden:grongle_log", 32, 2, "ug_woods", "32 grongle logs."),
    buy("smogstem_sapling", "Smogstem Saplings", "undergarden:smogstem_sapling", 4, 2, "ug_saplings", "4 smogstem saplings."),
    buy("wigglewood_sapling", "Wigglewood Saplings", "undergarden:wigglewood_sapling", 4, 2, "ug_saplings",
        "4 wigglewood saplings."),
    buy("grongle_sapling", "Grongle Saplings", "undergarden:grongle_sapling", 4, 2, "ug_saplings", "4 grongle saplings."),
    buy("underbeans", "Underbeans", "undergarden:underbeans", 16, 2, "ug_beans", "16 underbeans."),
    buy("roasted_underbeans", "Roasted Underbeans", "undergarden:roasted_underbeans", 16, 2, "ug_underbeans",
        "16 roasted underbeans."),
    buy("gloomgourd", "Gloomgourds", "undergarden:gloomgourd", 16, 2, "ug_gloomgourd", "16 gloomgourds."),
    buy("gloomgourd_seeds", "Gloomgourd Seeds", "undergarden:gloomgourd_seeds", 8, 2, "ug_gloomgourd", "8 gloomgourd seeds."),
    buy("dweller_steak", "Dweller Steaks", "undergarden:dweller_steak", 8, 2, "ug_meat", "8 cooked dweller steaks."),
    buy("gloomper_leg", "Gloomper Legs", "undergarden:gloomper_leg", 8, 2, "ug_meat", "8 cooked gloomper legs."),
    buy("gwibling", "Cooked Gwibling", "undergarden:cooked_gwibling", 8, 2, "ug_gwibling", "8 cooked gwibling."),
    buy("blisterberry", "Blisterberries", "undergarden:blisterberry", 16, 2, "ug_berries", "16 blisterberries."),
    buy("droopvine", "Droopvines", "undergarden:droopvine_item", 16, 2, "ug_glow_food", "16 droopvines."),
    buy("glitterkelp", "Glitterkelp", "undergarden:glitterkelp", 16, 2, "ug_glow_food", "16 glitterkelp."),
    buy("mogmoss", "Mogmoss", "undergarden:mogmoss", 16, 2, "ug_mogmoss", "16 mogmoss."),
    buy("blood_mushroom", "Blood Mushrooms", "undergarden:blood_mushroom", 8, 2, "ug_mushrooms", "8 blood mushrooms."),
    buy("indigo_mushroom", "Indigo Mushrooms", "undergarden:indigo_mushroom", 8, 2, "ug_mushrooms", "8 indigo mushrooms."),
    buy("ink_mushroom", "Ink Mushrooms", "undergarden:ink_mushroom", 8, 2, "ug_mushrooms", "8 ink mushrooms."),
    buy("veil_mushroom", "Veil Mushrooms", "undergarden:veil_mushroom", 8, 2, "ug_mushrooms", "8 veil mushrooms."),
    buy("shard_torch", "Shard Torches", "undergarden:shard_torch", 32, 2, "ug_shard_torch", "32 shard torches."),
    buy("goo_ball", "Scintling Goo", "undergarden:goo_ball", 16, 3, "ug_goo", "16 balls of scintling goo."),
    buy("brute_tusk", "Brute Tusks", "undergarden:brute_tusk", 4, 3, "ug_brute", "4 brute tusks."),
    buy("rogdorium", "Rogdorium", "undergarden:rogdorium", 16, 4, "ug_rogdorium", "16 rogdorium."),
    buy("utheric_shard", "Utheric Shards", "undergarden:utheric_shard", 16, 4, "ug_rotbelcher",
        "16 utheric shards. You still purify them yourself."),

    # --- HV: the Twilight Forest -----------------------------------------------------------------------
    counter("sw_row_hv", "Twilight Stall", "t5_hv", "Wood, food and drops from the dusk", [
        "&eWhat:&r Twilight Forest wood, food, plants and creature drops. Never boss trophies.",
        "&eHow:&r each entry appears after the Twilight quest where you first got it."]),
    buy("twilight_oak_log", "Twilight Oak Logs", "twilightforest:twilight_oak_log", 64, 4, "tf_oak", "64 twilight oak logs."),
    buy("twilight_sapling", "Twilight Oak Saplings", "twilightforest:twilight_oak_sapling", 8, 4, "tf_oak",
        "8 twilight oak saplings."),
    buy("torchberries", "Torchberries", "twilightforest:torchberries", 16, 4, "tf_focus_parts", "16 glowing torchberries."),
    buy("raven_feather", "Raven Feathers", "twilightforest:raven_feather", 4, 4, "tf_focus_parts", "4 raven feathers."),
    buy("liveroot", "Liveroot", "twilightforest:liveroot", 16, 5, "tf_ironwood", "16 liveroot for ironwood."),
    buy("venison", "Raw Venison", "twilightforest:raw_venison", 16, 4, "tf_venison", "16 raw venison."),
    buy("meef", "Raw Meef", "twilightforest:raw_meef", 16, 4, "tf_meef", "16 raw meef."),
    buy("maze_wafer", "Maze Wafers", "twilightforest:maze_wafer", 16, 4, "tf_maze_wafer", "16 maze wafers."),
    buy("thorn_rose", "Thorn Roses", "twilightforest:thorn_rose", 4, 4, "tf_thorn_rose", "4 thorn roses."),
    buy("uberous_soil", "Uberous Soil", "twilightforest:uberous_soil", 4, 6, "tf_uberous", "4 uberous soil."),
    buy("castle_brick", "Castle Bricks", "twilightforest:castle_brick", 32, 6, "tf_castle_bricks", "32 castle bricks."),
    buy("arctic_fur", "Arctic Fur", "twilightforest:arctic_fur", 8, 5, "tf_arctic", "8 arctic fur."),
    buy("armor_shard", "Armour Shards", "twilightforest:armor_shard", 9, 6, "tf_armor_shards",
        "9 armour shards (one cluster's worth)."),
    buy("carminite", "Carminite", "twilightforest:carminite", 4, 6, "tf_carminite", "4 carminite."),
    buy("naga_scale", "Naga Scales", "twilightforest:naga_scale", 4, 8, "w_naga", "4 naga scales."),
    buy("alpha_fur", "Alpha Yeti Fur", "twilightforest:alpha_yeti_fur", 4, 8, "tf_alpha_fur", "4 alpha yeti fur."),

    # --- EV: space -------------------------------------------------------------------------------------
    counter("sw_row_ev", "Space Stall", "t6_pu", "Stone and souvenirs of other planets", [
        "&eWhat:&r the stone, sand and ice of the Moon, Mars, Venus, Mercury and Glacio. Paid in Greater Tokens.",
        "&eHow:&r each planet's goods appear after you've landed there. Ores stay off the list: mine them yourself."]),
    g("moon_stone", "Moon Stone", "ad_astra:moon_stone", 64, 1, "t7_rocket", "64 moon stone."),
    g("moon_sand", "Moon Sand", "ad_astra:moon_sand", 64, 1, "t7_rocket", "64 moon sand (lunar regolith)."),
    g("cheese", "Moon Cheese", "ad_astra:cheese", 16, 1, "w_cheese", "16 wedges of moon cheese."),
    g("mars_stone", "Mars Stone", "ad_astra:mars_stone", 64, 1, "w_mars", "64 mars stone."),
    g("mars_sand", "Mars Sand", "ad_astra:mars_sand", 64, 1, "w_mars", "64 mars sand, red with iron(III) oxide."),
    g("ice_shard", "Ice Shards", "ad_astra:ice_shard", 16, 1, "sp_mars_poles", "16 ice shards from the polar caps."),
    g("venus_stone", "Venus Stone", "ad_astra:venus_stone", 64, 1, "w_venus", "64 venus stone."),
    g("venus_sand", "Venus Sand", "ad_astra:venus_sand", 64, 1, "w_venus", "64 venus sand."),
    g("mercury_stone", "Mercury Stone", "ad_astra:mercury_stone", 64, 1, "w_mercury", "64 mercury stone."),
    g("glacio_stone", "Glacio Stone", "ad_astra:glacio_stone", 64, 1, "w_glacio", "64 glacio stone."),
    g("permafrost", "Permafrost", "ad_astra:permafrost", 32, 1, "w_glacio", "32 permafrost."),
]

CHAPTER = Chapter("shop_world", "Market: Blocks, Food and Wild Goods", "minecraft:grass_block",
        ["Buy more of the blocks, food and wild goods you've already gathered."], SIDE, QUESTS,
        tokens=0, layout="manual")
