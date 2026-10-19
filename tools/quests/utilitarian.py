"""Quest chapter: utilitarian (the Utilitarian mod, added 2026-10-18). See tools/quests/STYLE.md.

Recipes checked against utilitarian-1.21.1-0.19.2.jar (data/utilitarian/recipe/).
Layout: y=0 bulk wood recipes, y=2 early tools and fuel, y=4 blocks that move things, y=6 redstone and
sound, y=8 traders, raiders and mobs. Hangs off gs_table in the start chapter.
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("utilitarian", "Utilitarian", "utilitarian:angel_block",
        ["Small blocks and shortcuts that save a lot of clicks."], SIDE, [
    # --- Bulk wood recipes (y=0) ---------------------------------------------------------------
    Q("ut_sticks", 0, 0, [item("minecraft:stick", 32)], "Sticks by the Bundle", deps=["gs_table"], xp=10,
      subtitle="Two logs, sixteen sticks", desc=[
        "&6You remember never wasting a motion. These recipes feel familiar.&r",
        "&eWhat:&r Utilitarian adds bulk recipes that skip the planks step. Two logs stacked in a column make 16 sticks.",
        "&eHow:&r put two logs of any kind one above the other in the crafting grid.",
        "&eTip:&r JEI shows every Utilitarian shortcut: press U on a log to see them all."]),
    Q("ut_chests", 2, 0, [item("minecraft:chest", 4), item("minecraft:ladder", 24)], "Chests and Ladders", deps=["ut_sticks"], xp=10,
      subtitle="Eight logs, four chests", desc=[
        "&eWhat:&r logs in a chest ring make 4 chests at once. Seven logs in a ladder shape make 24 ladders.",
        "&eHow:&r the same shapes as the plank recipes, but with logs (check JEI).",
        "&eTip:&r three logs in a V make 12 bowls, and logs between iron make a hopper without a chest."]),
    Q("ut_building", 4, 0, [anytag("minecraft:wooden_slabs", 24), anytag("minecraft:wooden_stairs", 16)], "Slabs and Stairs", deps=["ut_chests"], xp=15,
      subtitle="A row of logs, a stack of slabs", desc=[
        "&eWhat:&r three logs in a row make 24 slabs; six logs in a stair shape make 16 stairs.",
        "&eHow:&r use logs of one wood type in the usual slab or stair shape (check JEI).",
        "&eTip:&r two slabs placed diagonally in the grid turn back into a plank, so leftover slabs are never wasted."]),
    Q("ut_doors", 6, 0, [anytag("minecraft:wooden_doors", 12), anytag("minecraft:wooden_trapdoors", 12)], "Doors and Trapdoors", deps=["ut_building"], xp=15,
      subtitle="Six logs, a dozen doors", desc=[
        "&eWhat:&r six logs in a door shape make 12 doors; six logs in a trapdoor shape make 12 trapdoors.",
        "&eHow:&r one wood type per craft (check JEI). Two logs side by side also make 4 pressure plates.",
        "&eTip:&r doors placed side by side open together, so a double door needs only one click."]),
    Q("ut_redye", 8, 0, [anytag("c:concretes", 8)], "Re-Dyeing", deps=["ut_doors"], xp=15,
      optional=True, tokens=1, subtitle="Optional: wrong colour? Dye it again", desc=[
        "&eWhat:&r Utilitarian lets you re-dye concrete, concrete powder, terracotta, stained glass, glass panes and candles that already have a colour.",
        "&eChemistry:&r real pigments are chemicals too: concrete's colours come from metal oxides, like iron oxide (Fe₂O₃) for red and brown.",
        "&eHow:&r eight coloured blocks around one dye re-colours all eight, or one block plus one dye does a single block (check JEI).",
        "&eTip:&r it also mixes blue and yellow dye into green, so cactus isn't the only green."]),

    # --- Early tools and fuel (y=2) ------------------------------------------------------------
    Q("ut_tiny_coal", 0, 2, [item("utilitarian:tiny_coal", 8), item("utilitarian:tiny_charcoal", 8)], "Tiny Coal", deps=["ut_sticks", "gs_coal"], xp=15,
      subtitle="One coal split eight ways", desc=[
        "&eWhat:&r one coal or charcoal makes 8 tiny pieces. Each burns for 10 seconds, so you don't waste a whole coal on one item.",
        "&eChemistry:&r charcoal is wood heated without air (pyrolysis): water and volatile compounds are driven off, leaving mostly carbon.",
        "&eHow:&r put one coal or charcoal in the crafting grid. Eight tiny pieces craft back into one.",
        "&eTip:&r this pack's furnaces cook faster than vanilla, so one tiny coal covers more than one item."]),
    Q("ut_trowel", 2, 2, [item("utilitarian:trowel")], "The Trowel", deps=["ut_sticks", "gs_iron"], xp=15,
      subtitle="Places random blocks from your hotbar", desc=[
        "&eWhat:&r the Trowel places a random block from your hotbar each time you use it. Great for natural-looking walls and paths.",
        "&eHow:&r two iron ingots and a stick (check JEI). Sneak-use it to switch between hotbar only and your whole inventory.",
        "&eTip:&r fill the hotbar with stone, cobblestone, andesite and tuff, and a plain wall looks weathered in seconds."]),
    Q("ut_angel", 4, 2, [item("utilitarian:angel_block", 4)], "Angel Block", deps=["ut_sticks", "gs_iron"], xp=25,
      subtitle="A block you can place in mid-air", desc=[
        "&eWhat:&r the Angel Block can be placed in empty air, with nothing next to it. It's the start of any sky bridge or floating build.",
        "&eHow:&r two feathers, two gold ingots and obsidian (check JEI). Use it while looking at empty air.",
        "&eTip:&r it's a building block, not flight. Flying in this pack is a chemistry milestone (see the Nether chapter)."]),

    # --- Blocks that move things (y=4) ---------------------------------------------------------
    Q("ut_snad", 0, 4, [item("utilitarian:snad", 4)], "Snad", deps=["ut_tiny_coal"], xp=20,
      subtitle="Sand that makes plants grow taller", desc=[
        "&eWhat:&r cactus, sugar cane, kelp and bamboo grow taller and faster on Snad. Soul Snad does the same for nether wart.",
        "&eChemistry:&r sand is mostly quartz grains, SiO₂, the same compound as the Nether quartz and certus you'll meet later.",
        "&eHow:&r two sand make one Snad (red sand makes Red Snad, soul sand makes Soul Snad).",
        "&eTip:&r a column of sugar cane on Snad is the fastest paper source for Sophisticated upgrades and Iron Furnace augments."]),
    Q("ut_magnet", 2, 4, [item("utilitarian:magnet")], "Block Magnet", deps=["ut_trowel"], xp=25,
      subtitle="Powered magnet that lifts iron blocks", desc=[
        "&eWhat:&r with a redstone signal, the Block Magnet pulls iron blocks, steel blocks and anvils below it up towards it.",
        "&eChemistry:&r iron is ferromagnetic: its atoms' tiny magnetic moments line up in domains. The recipe is an electromagnet, an iron core with copper on each side.",
        "&eHow:&r copper ingot, iron block, copper ingot in a row. Place it, put an iron block somewhere below, and power the magnet.",
        "&eTip:&r a magnet and a lever make a simple lift for iron blocks: power it to pull them up, cut the power to let them fall."]),
    Q("ut_fluid_hopper", 4, 4, [item("utilitarian:fluid_hopper")], "Fluid Hopper", deps=["ut_trowel", "gs_bucket"], xp=25,
      subtitle="A hopper for liquids", desc=[
        "&eWhat:&r the Fluid Hopper moves fluids the way a hopper moves items: it collects fluid from above and passes it on, the way a hopper does with items (check its JEI page).",
        "&eHow:&r iron ingots around a bucket, with white dye on top (check JEI).",
        "&eTip:&r under an infinite water source it fills a tank for your first steam boiler without any pump."]),
    Q("ut_dropper", 6, 4, [item("utilitarian:well_behaved_dropper")], "Well Behaved Dropper", deps=["ut_trowel"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a dropper that doesn't spray", desc=[
        "&eWhat:&r a dropper that drops items neatly in front of itself instead of flinging them in random directions.",
        "&eHow:&r a dropper with a gold nugget on each side (check JEI).",
        "&eTip:&r drop items onto a pressure plate or into water streams and they land exactly where you planned."]),

    # --- Redstone and sound (y=6) --------------------------------------------------------------
    Q("ut_clock", 0, 6, [item("utilitarian:redstone_clock")], "Redstone Clock", deps=["ut_snad"], xp=20,
      subtitle="A pulse generator in one block", desc=[
        "&eWhat:&r the Redstone Clock pulses a redstone signal on its own, with no repeater loop.",
        "&eHow:&r chiseled stone bricks with redstone on four sides (check JEI). Right-click it with an empty hand to change the speed; sneak to change it faster.",
        "&eTip:&r a slow clock on a dispenser or a Well Behaved Dropper makes a simple timed feeder."]),
    Q("ut_tps", 2, 6, [item("utilitarian:tps_meter")], "TPS Meter", deps=["ut_clock"], xp=25,
      optional=True, tokens=1, subtitle="Optional: how hard is the server working?", desc=[
        "&eWhat:&r the TPS Meter gives a redstone signal based on the dimension's ticks per second. A healthy server runs at 20.",
        "&eHow:&r four comparators around obsidian (check JEI).",
        "&eTip:&r wire it to a lamp in your factory: if it dims, something you built is lagging the server."]),
    Q("ut_muffler", 4, 6, [item("utilitarian:sound_muffler")], "Sound Muffler", deps=["ut_clock"], xp=15,
      subtitle="Silence a noisy machine room", desc=[
        "&eWhat:&r the Sound Muffler mutes sounds in a radius around it. Your crushers, pumps and boilers go quiet.",
        "&eChemistry:&r real soundproofing works the same way: soft, porous fibres like wool turn sound energy into a tiny amount of heat.",
        "&eHow:&r any wool plus a note block, shapeless.",
        "&eTip:&r one in the middle of a machine row is usually enough. Its tooltip shows the radius."]),

    # --- Traders, raiders and mobs (y=8) -------------------------------------------------------
    Q("ut_carpet", 0, 8, [anyof(["utilitarian:white_soliciting_carpet", "utilitarian:orange_soliciting_carpet", "utilitarian:magenta_soliciting_carpet",
        "utilitarian:light_blue_soliciting_carpet", "utilitarian:yellow_soliciting_carpet", "utilitarian:lime_soliciting_carpet",
        "utilitarian:pink_soliciting_carpet", "utilitarian:gray_soliciting_carpet", "utilitarian:light_gray_soliciting_carpet",
        "utilitarian:cyan_soliciting_carpet", "utilitarian:purple_soliciting_carpet", "utilitarian:blue_soliciting_carpet",
        "utilitarian:brown_soliciting_carpet", "utilitarian:green_soliciting_carpet", "utilitarian:red_soliciting_carpet",
        "utilitarian:black_soliciting_carpet"])], "Trader Carpet", deps=["ut_clock"], xp=15,
      subtitle="Wandering traders land here, not on you", desc=[
        "&eWhat:&r a wandering trader arriving nearby appears on a Trader Carpet instead of right in your face.",
        "&eHow:&r any carpet plus a small flower, shapeless. Each colour has its own carpet.",
        "&eTip:&r put it in a little market stall by your base. JEI also shows a trapped version, if you're feeling unkind."]),
    Q("ut_banner", 2, 8, [item("utilitarian:no_soliciting_banner")], "No Soliciting", deps=["ut_carpet"], xp=15,
      subtitle="A banner that keeps traders away", desc=[
        "&eWhat:&r the No Soliciting Banner stops wandering traders from spawning in the chunks around it.",
        "&eHow:&r wool, a lead and a stick, in a banner shape (check JEI).",
        "&eTip:&r use either the carpet or the banner: carpet if you like the trader's goods, banner if you don't."]),
    Q("ut_raider", 4, 8, [item("utilitarian:no_raider_block")], "Outpost Claim", deps=["ut_banner"], xp=40,
      optional=True, tokens=1, subtitle="Optional: stop pillagers returning to an outpost", desc=[
        "&eWhat:&r place the Raider Outpost Claim Block inside a pillager outpost and raiders stop coming back to it.",
        "&eHow:&r the recipe uses an ominous (illager) banner, which a pillager captain drops (check JEI).",
        "&eTip:&r claim the outpost before building there; it makes a fine tower base."]),
    Q("ut_unname", 6, 8, [item("utilitarian:unname_tag")], "Un-Name Tag", deps=["ut_banner"], xp=15,
      optional=True, tokens=1, subtitle="Optional: undo a name tag", desc=[
        "&eWhat:&r the Un-Name Tag removes a mob's custom name.",
        "&eHow:&r a name tag plus white dye, shapeless. Use it on the named mob.",
        "&eTip:&r useful when a pet name typo has been bothering you for weeks."]),
    Q("ut_slime", 8, 8, [item("utilitarian:slime_bucket")], "Slime in a Bucket", deps=["ut_unname"], xp=25,
      secret=True, loot="secret", subtitle="Secret: it gets excited near its friends", desc=[
        "&6You remember finding hidden things by feel. The slime remembers too.&r",
        "&eWhat:&r you scooped a small slime into a bucket. It gets visibly excited when you carry it into a slime chunk.",
        "&eHow:&r use an empty bucket on a small slime. Place it again by using the bucket on the ground.",
        "&eTip:&r slime chunks spawn slimes underground at any light level, which makes them the best spot for a slime farm."]),
], links=[("gs_table", -2, 0)])
