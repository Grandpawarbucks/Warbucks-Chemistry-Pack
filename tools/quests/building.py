"""Quest chapter: building (building tools and decoration). See tools/quests/STYLE.md.

q_effortless / q_gadget / q_gadget_copy / q_gadget_exchange moved here from qol.py (keys unchanged).
Layout: y=0 hand tools, y=2 Building Gadgets, y=5 FramedBlocks, y=7 furniture, y=9 Macaw's structure,
y=11 Macaw's outdoors and lights, y=13 Supplementaries, y=15 Create decor, y=17 the chemistry lab.
Almost everything here is optional, cheap and for fun.
"""
from questlib import Q, Chapter, item, dim, tick, anyof, IDS, MAIN, SIDE  # noqa: F401

WOODS = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "bamboo", "crimson", "warped"]
STONES = ["stone", "cobblestone", "andesite", "brick", "sandstone"]


def variants(fmt, names=WOODS):
    """Every real id from a pattern like 'handcrafted:{}_chair' (filtered against test/ids.tsv)."""
    ids = [fmt.format(n) for n in names if fmt.format(n) in IDS]
    assert len(ids) >= 3, f"too few variants for {fmt}: {ids}"
    return ids


LAB_SCREENS = ["laboratoryblocks:clear_laboratory_screen", "laboratoryblocks:text_laboratory_screen",
               "laboratoryblocks:wave_laboratory_screen", "laboratoryblocks:quantum_laboratory_screen",
               "laboratoryblocks:glowing_clear_laboratory_screen", "laboratoryblocks:glowing_text_laboratory_screen",
               "laboratoryblocks:glowing_wave_laboratory_screen", "laboratoryblocks:glowing_quantum_laboratory_screen"]
LAB_DOORS = ["laboratoryblocks:laboratory_door", "laboratoryblocks:glass_laboratory_door", "laboratoryblocks:mesh_laboratory_door"]
FRAMED_SHAPES = ["framedblocks:framed_slope", "framedblocks:framed_corner_slope", "framedblocks:framed_stairs",
                 "framedblocks:framed_slab", "framedblocks:framed_panel", "framedblocks:framed_pillar", "framedblocks:framed_prism"]
MCW_LIGHTS = ["mcwlights:classic_street_lamp", "mcwlights:double_street_lamp", "mcwlights:chain_lantern", "mcwlights:bell_lantern",
              "mcwlights:cross_lantern", "mcwlights:tavern_lantern", "mcwlights:garden_light", "mcwlights:wall_lamp",
              "mcwlights:iron_chandelier", "mcwlights:golden_chandelier", "mcwlights:copper_chandelier"]
MCW_BRIDGES = variants("mcwbridges:rope_{}_bridge") + ["mcwbridges:stone_brick_bridge", "mcwbridges:cobblestone_bridge",
               "mcwbridges:brick_bridge", "mcwbridges:iron_bridge", "mcwbridges:sandstone_bridge"]
MCW_PATHS = (variants("mcwpaths:{}_basket_weave_paving", STONES) + variants("mcwpaths:{}_honeycomb_paving", STONES)
             + variants("mcwpaths:{}_diamond_paving", STONES) + variants("mcwpaths:{}_flagstone", ["stone", "andesite", "brick", "sandstone"]))

CHAPTER = Chapter("building", "Building and Decoration", "framedblocks:framed_hammer",
        ["A god's house should look like one."], SIDE, [
    Q("bd_start", -1, 1, [tick()], "Building Basics", deps=["gs_table"], xp=10, size=1.5, shape="hexagon",
      subtitle="Tools and blocks for a base worth living in", desc=[
        "&6You remember raising cities with a gesture. For now, a few clever tools will do.&r",
        "&eWhat:&r this page is a catalogue: building tools, gadgets, framed blocks, furniture, Macaw's blocks, Supplementaries, Create decor and a proper chemistry lab, one row each.",
        "&eHow:&r everything here is optional and cheap; pick what you like. Click the checkmark to open the page.",
        "&eTip:&r the lab row at the bottom opens once you have Nether quartz."]),

    # --- Hand tools (y=0) ----------------------------------------------------------------------
    Q("q_effortless", 0, 0, [item("effortlessbuilding:randomizer_tool")], "Effortless Building", deps=["bd_start"], xp=20,
      optional=True, tokens=1, subtitle="Optional: mirror, array and line building", desc=[
        "&eWhat:&r Effortless Building adds mirror, array and line modes for big builds.",
        "&eHow:&r open its menu (check Controls) and pick a mode. The randomizer places a random mix of the blocks you load into it.",
        "&eTip:&r the randomizer with stone, andesite and cobblestone makes natural-looking walls."]),
    Q("bd_stick", 2, 0, [item("constructionstick:wooden_stick")], "Construction Stick", deps=["bd_start"], xp=15,
      optional=True, tokens=1, subtitle="Optional: extend a wall in one click", desc=[
        "&eWhat:&r a Construction Stick places a whole row or face of blocks matching the one you click, using blocks from your inventory.",
        "&eHow:&r three sticks in a column (check JEI). Right-click the face of a wall to grow it by one layer.",
        "&eTip:&r the tooltip lists its modes, such as only extending in a straight line."]),
    Q("bd_stick_diamond", 4, 0, [item("constructionstick:diamond_stick")], "Diamond Stick", deps=["bd_stick"], xp=30,
      optional=True, tokens=1, subtitle="Optional: bigger reach, more durability", desc=[
        "&eWhat:&r better sticks place more blocks per click and last longer: copper, iron, diamond, then netherite.",
        "&eChemistry:&r diamond is pure carbon (C) in a tight 3D lattice, which makes it the hardest natural material.",
        "&eHow:&r a diamond on two sticks (check JEI). Templates applied at a smithing table add tricks like placing in mid-air."]),
    Q("bd_chisel", 6, 0, [tick()], "Rechiseled", deps=["bd_start", "gs_iron"], xp=15,
      optional=True, tokens=1, subtitle="Optional: hundreds of block patterns", desc=[
        "&eWhat:&r Rechiseled adds a chisel that turns stone, planks, metal blocks and more into decorative patterns: bricks, tiles, pillars, gears.",
        "&eHow:&r craft the chisel from an iron ingot on a stick, right-click to open it, put blocks in and pick a pattern. Click the checkmark when you've chiseled something.",
        "&eTip:&r many patterns connect to each other when placed side by side. Try the iron and copper block patterns for a machine room."]),

    # --- Building Gadgets (y=2) ----------------------------------------------------------------
    Q("q_gadget", 0, 2, [item("buildinggadgets2:gadget_building")], "Building Gadgets", deps=["bd_start", "t3_hull"], xp=40,
      subtitle="Place whole surfaces with FE", desc=[
        "&eWhat:&r FE-powered gadgets that place, swap, copy and remove blocks in bulk.",
        "&eHow:&r iron, redstone, lapis and a diamond (check JEI). Charge it in an energy cube.",
        "&eTip:&r link the gadget to a chest or backpack so it pulls blocks from storage."]),
    Q("q_gadget_copy", 1, 3.5, [item("buildinggadgets2:gadget_copy_paste"), item("buildinggadgets2:template_manager")], "Copy and Paste", deps=["q_gadget"], xp=60,
      optional=True, tokens=1, subtitle="Optional: copy a whole build", desc=[
        "&eWhat:&r copy an area and paste it elsewhere; the Template Manager saves copies to share.",
        "&eHow:&r check JEI. Great for repeating a chemical reactor cell or a row of machines.",
        "&eTip:&r templates can be shared with friends on the server."]),
    Q("q_gadget_exchange", 3, 3.5, [item("buildinggadgets2:gadget_exchanging")], "Exchanging Gadget", deps=["q_gadget"], xp=40,
      optional=True, tokens=1, subtitle="Optional: swap blocks in place", desc=[
        "&eWhat:&r replaces blocks in an area with another block, keeping the shape.",
        "&eHow:&r check JEI. Perfect for turning a cobble shell into something pretty.",
        "&eTip:&r it uses the blocks in your inventory, so carry enough."]),
    Q("bd_gadget_destroy", 2, 2, [item("buildinggadgets2:gadget_destruction")], "Destruction Gadget", deps=["q_gadget"], xp=40,
      optional=True, tokens=1, subtitle="Optional: clear a room in seconds", desc=[
        "&eWhat:&r removes a box of blocks in front of you, sized however you like. It can undo its last action.",
        "&eHow:&r check JEI. Set the depth, width and height in its menu.",
        "&eTip:&r perfect for hollowing out a hillside for a new factory floor."]),

    # --- FramedBlocks (y=5) --------------------------------------------------------------------
    Q("bd_framed", 0, 5, [item("framedblocks:framed_cube", 8), item("framedblocks:framed_hammer")], "Framed Blocks", deps=["bd_start"], xp=20,
      subtitle="Any shape, any texture", desc=[
        "&eWhat:&r FramedBlocks are wooden frames that take the look of any block you right-click into them, in dozens of shapes.",
        "&eHow:&r framed cubes are planks and sticks (check JEI). Right-click a framed block with any full block to apply it as camouflage. The Framed Hammer takes it back off.",
        "&eTip:&r camouflage with glass, ores or even machine casings: the block keeps its shape and takes the texture."]),
    Q("bd_framed_shapes", 2, 5, [anyof(FRAMED_SHAPES, 6)], "Slopes and Panels", deps=["bd_framed"], xp=20,
      optional=True, tokens=1, subtitle="Optional: six framed shapes", desc=[
        "&eWhat:&r any six framed slopes, corner slopes, stairs, slabs, panels, pillars or prisms.",
        "&eHow:&r each shape is made from framed cubes (check JEI). Most come several at a time.",
        "&eTip:&r framed slopes camouflaged as stone make roofs and ramps that look hand-carved."]),
    Q("bd_framed_secret", 4, 5, [item("framedblocks:framed_secret_storage")], "Secret Storage", deps=["bd_framed_shapes"], xp=30,
      optional=True, tokens=1, subtitle="Optional: a chest that looks like a wall", desc=[
        "&eWhat:&r a full-block chest that wears any block's texture, so it disappears into a wall.",
        "&eHow:&r a framed chest surrounded by framed cubes (check JEI), then camouflage it.",
        "&eTip:&r hide your rarest elements in one. Nobody suspects the third stone brick from the left."]),

    # --- Furniture (y=7) -----------------------------------------------------------------------
    Q("bd_chairs", 0, 7, [anyof(variants("handcrafted:{}_chair"), 2), anyof(variants("handcrafted:{}_table"), 1)], "Somewhere to Sit", deps=["bd_start"], xp=15,
      optional=True, tokens=1, subtitle="Optional: Handcrafted chairs and a table", desc=[
        "&eWhat:&r Handcrafted adds furniture you can actually sit on: chairs, couches, benches, tables, desks.",
        "&eHow:&r any wood works (check JEI). Right-click a chair to sit.",
        "&eTip:&r the Handcrafted Hammer changes the shape of trims and some other pieces (check its tooltip)."]),
    Q("bd_couch", 2, 7, [anyof(variants("handcrafted:{}_couch"), 2), anyof(variants("handcrafted:{}_desk"), 1)], "A Proper Study", deps=["bd_chairs"], xp=20,
      optional=True, tokens=1, subtitle="Optional: couches and a desk", desc=[
        "&eWhat:&r couches connect into long sofas; desks connect into long workbenches.",
        "&eHow:&r any wood (check JEI). Cushions and sheets add colour.",
        "&eTip:&r a desk by your Alchemistry machines makes a fine place to read the quest book."]),
    Q("bd_mcw_furniture", 4, 7, [anyof(variants("mcwfurnitures:{}_wardrobe") + variants("mcwfurnitures:{}_drawer")
                                       + variants("mcwfurnitures:{}_kitchen_cabinet"), 2)], "Macaw's Furniture", deps=["bd_chairs"], xp=20,
      optional=True, tokens=1, subtitle="Optional: wardrobes, drawers and cabinets", desc=[
        "&eWhat:&r Macaw's Furniture adds kitchens, wardrobes, drawers, bookshelves and more. Many of them store items.",
        "&eHow:&r any two wardrobes, drawers or kitchen cabinets (check JEI for the full set).",
        "&eTip:&r drawers and cabinets open like chests, so a kitchen can double as food storage."]),

    # --- Macaw's structure (y=9) ---------------------------------------------------------------
    Q("bd_mcw_doors", 0, 9, [anyof(variants("mcwdoors:{}_barn_door") + variants("mcwdoors:{}_modern_door")
                                   + variants("mcwdoors:{}_glass_door") + variants("mcwdoors:{}_cottage_door"), 2)], "Doors", deps=["bd_start"], xp=15,
      optional=True, tokens=1, subtitle="Optional: Macaw's doors", desc=[
        "&eWhat:&r Macaw's Doors adds barn, cottage, glass, modern and many more doors in every wood.",
        "&eHow:&r any two barn, modern, glass or cottage doors (check JEI for recipes).",
        "&eTip:&r glass doors let you see into a machine room without opening it."]),
    Q("bd_mcw_trapdoors", 2, 9, [anyof(variants("mcwtrpdoors:{}_barn_trapdoor") + variants("mcwtrpdoors:{}_glass_trapdoor")
                                       + variants("mcwtrpdoors:{}_classic_trapdoor"), 4)], "Trapdoors", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Optional: Macaw's trapdoors", desc=[
        "&eWhat:&r decorative trapdoors that match the doors: barn, glass, classic and more.",
        "&eHow:&r any four barn, glass or classic trapdoors (check JEI).",
        "&eTip:&r trapdoors on walls make great shutters and cabinet fronts."]),
    Q("bd_mcw_windows", 4, 9, [anyof(variants("mcwwindows:{}_window") + variants("mcwwindows:{}_pane_window")
                                     + variants("mcwwindows:{}_four_window"), 4)], "Windows", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Optional: framed windows", desc=[
        "&eWhat:&r Macaw's Windows adds framed windows, shutters, curtains, blinds and parapets.",
        "&eHow:&r any four framed windows (check JEI).",
        "&eChemistry:&r glass is mostly silica (SiO₂) melted with soda (Na₂CO₃) and lime (CaO), then cooled before it can crystallise."]),
    Q("bd_mcw_roofs", 6, 9, [anyof(variants("mcwroofs:{}_roof") + variants("mcwroofs:{}_steep_roof")
                                   + variants("mcwroofs:{}_roof", ["stone", "cobblestone", "blackstone", "deepslate", "andesite"]), 16)], "Roofs", deps=["bd_mcw_doors"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a roof that isn't flat", desc=[
        "&eWhat:&r Macaw's Roofs adds sloped, steep, attic and top roof pieces that join into proper roofs.",
        "&eHow:&r any sixteen roof pieces (check JEI). Wooden roofs come from logs and sticks.",
        "&eTip:&r place the lower and upper pieces together to make a gentler slope."]),
    Q("bd_mcw_fences", 8, 9, [anyof(variants("mcwfences:{}_picket_fence") + variants("mcwfences:{}_stockade_fence")
                                    + variants("mcwfences:{}_wired_fence") + variants("mcwfences:{}_hedge"), 8)], "Fences and Hedges", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Optional: picket, stockade, wired, hedge", desc=[
        "&eWhat:&r Macaw's Fences adds picket and stockade fences, wired fences, hedges and gates.",
        "&eHow:&r any eight picket, stockade or wired fences or hedges (check JEI).",
        "&eTip:&r hedges are made from leaves, so you can keep a garden looking natural."]),

    # --- Macaw's outdoors and lights (y=11) ----------------------------------------------------
    Q("bd_mcw_paths", 0, 11, [anyof(MCW_PATHS, 16)], "Paths", deps=["bd_start", "gs_stone"], xp=15,
      optional=True, tokens=1, subtitle="Optional: paving between your buildings", desc=[
        "&eWhat:&r Macaw's Paths adds paving patterns (basket weave, honeycomb, flagstone) in stone, brick and sandstone.",
        "&eHow:&r any sixteen paving blocks (check JEI).",
        "&eTip:&r a path from your base to your waystone saves getting lost at night."]),
    Q("bd_mcw_bridges", 2, 11, [anyof(MCW_BRIDGES, 8)], "Bridges", deps=["bd_mcw_paths"], xp=15,
      optional=True, tokens=1, subtitle="Optional: rope, stone and iron bridges", desc=[
        "&eWhat:&r Macaw's Bridges adds bridge pieces that connect into rope, stone, brick and iron bridges, with piers and stairs.",
        "&eHow:&r any eight bridge pieces (check JEI).",
        "&eTip:&r an iron bridge over a lava lake makes the Nether commute much safer."]),
    Q("bd_mcw_lights", 4, 11, [anyof(MCW_LIGHTS, 4)], "Lamps and Lanterns", deps=["bd_start", "gs_torch"], xp=15,
      optional=True, tokens=1, subtitle="Optional: street lamps and chandeliers", desc=[
        "&eWhat:&r Macaw's Lights adds street lamps, lanterns, garden lights and chandeliers.",
        "&eHow:&r any four of them (check JEI).",
        "&eTip:&r street lamps along your paths keep mobs from spawning on the way home."]),
    Q("bd_lava_lamp", 6, 11, [item("mcwlights:lava_lamp")], "Lava Lamp", deps=["bd_mcw_lights", "gs_bucket"], xp=20,
      optional=True, tokens=1, subtitle="Optional: groovy chemistry", desc=[
        "&eWhat:&r a lava lamp for your desk. This one really has lava in it.",
        "&eChemistry:&r a real lava lamp holds wax in water. The bulb heats the wax, it expands, its density drops below the water's and it rises; at the top it cools, gets denser and sinks.",
        "&eHow:&r iron nuggets, a lava bucket and an iron ingot (check JEI)."]),

    # --- Supplementaries (y=13) ----------------------------------------------------------------
    Q("bd_jar", 0, 13, [item("supplementaries:jar", 2)], "Jars", deps=["bd_start"], xp=15,
      optional=True, tokens=1, subtitle="Optional: display jars for anything", desc=[
        "&eWhat:&r Supplementaries jars hold items, liquids or even small mobs, and show what's inside.",
        "&eHow:&r glass and a wooden slab (check JEI). Right-click with an item or a bucket to fill.",
        "&eTip:&r a shelf of jars, one per element, makes a lovely periodic table display."]),
    Q("bd_rope", 2, 13, [item("supplementaries:rope", 16), item("supplementaries:sack")], "Rope and Sacks", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="Optional: flax, rope and a sack", desc=[
        "&eWhat:&r rope you can climb and pull things up with, and sacks that store items and can be carried.",
        "&eHow:&r grow flax (seeds from wild flax), then craft rope and sacks from it (check JEI).",
        "&eTip:&r ropes hanging down a mineshaft are a quick way up and down (check JEI for the pulley block)."]),
    Q("bd_soap", 4, 13, [item("supplementaries:soap", 2)], "Soap", deps=["bd_jar"], xp=25,
      optional=True, tokens=1, subtitle="Optional: the oldest chemistry in the house", desc=[
        "&eWhat:&r soap washes the dye off coloured blocks and items, and it powers the Bubble Blower.",
        "&eChemistry:&r saponification. Wood ash is rich in potash (K₂CO₃); in water it makes lye. Lye splits fat into glycerol and fatty-acid salts, which is soap. People made it this way for thousands of years.",
        "&eHow:&r a water bucket, four ash and a porkchop (check JEI). Ash is left behind when fire burns blocks away; check JEI for other sources."]),
    Q("bd_bubbles", 6, 13.5, [item("supplementaries:bubble_blower")], "Bubbles!", deps=["bd_soap"], xp=20,
      secret=True, loot="secret", subtitle="Secret: a demigod at play", desc=[
        "&6You remember making nebulae. These are smaller, but they're very pretty.&r",
        "&eWhat:&r the Bubble Blower uses soap to blow bubbles; it can also make Bubble Blocks (check its tooltip).",
        "&eChemistry:&r a soap film is a thin water layer between two layers of soap molecules. The colours come from light reflecting off its front and back surfaces and interfering."]),

    # --- Create decor (y=15) -------------------------------------------------------------------
    Q("bd_deco_lamps", 0, 15, [anyof(variants("createdeco:{}_lamp", ["yellow_andesite", "red_andesite", "green_andesite", "blue_andesite",
                                                                      "yellow_brass", "red_brass", "green_brass", "blue_brass",
                                                                      "yellow_copper", "red_copper", "green_copper", "blue_copper",
                                                                      "yellow_iron", "red_iron", "green_iron", "blue_iron",
                                                                      "yellow_zinc", "red_zinc", "green_zinc", "blue_zinc"]), 4)], "Create Deco Lamps", deps=["bd_start", "cr_deco"], xp=20,
      optional=True, tokens=1, subtitle="Optional: industrial lights", desc=[
        "&eWhat:&r Create Deco lamps in four colours and five metals light up a factory floor properly.",
        "&eHow:&r a nugget, a torch and a plate of the metal (check JEI). Any four lamps.",
        "&eTip:&r lamps can be switched off with redstone: red lamps as warning lights next to a reactor are a nice touch."]),
    Q("bd_deco_hull", 2, 15, [anyof(variants("createdeco:{}_hull", ["andesite", "brass", "copper", "iron", "zinc", "industrial_iron"]), 4),
                              anyof(variants("createdeco:{}_support", ["andesite", "brass", "copper", "iron", "zinc", "industrial_iron"]), 4)], "Hulls and Supports", deps=["bd_deco_lamps"], xp=20,
      optional=True, tokens=1, subtitle="Optional: riveted walls and girders", desc=[
        "&eWhat:&r hulls are riveted metal walls; supports are girders for roofs and catwalks.",
        "&eHow:&r any four hulls and four supports (check JEI).",
        "&eTip:&r copper hulls weather like copper blocks do. Wax them with honeycomb to keep the shine."]),
    Q("bd_copycat", 4, 15, [item("copycats:copycat_block", 2), anyof(["copycats:copycat_slope", "copycats:copycat_stairs", "copycats:copycat_board",
                                                                     "copycats:copycat_beam", "copycats:copycat_slice", "copycats:copycat_vertical_slope"], 4)],
      "Copycats", deps=["bd_start", "cr_casing"], xp=25,
      optional=True, tokens=1, subtitle="Optional: Create-style shape-shifting blocks", desc=[
        "&eWhat:&r Copycats+ adds many more Create copycat shapes: slopes, boards, beams, slices. Each takes the look of the block you apply to it.",
        "&eHow:&r cut zinc ingots in a stonecutter (zinc ore is found underground; check JEI), then right-click a placed copycat with a block.",
        "&eTip:&r copycat boards cover pipes and shafts while leaving them working."]),

    # --- The chemistry lab (y=17) --------------------------------------------------------------
    Q("bd_lab", 0, 17, [item("laboratoryblocks:laboratory_block", 16)], "Laboratory Blocks", deps=["bd_start", "t2_quartz"], xp=25,
      subtitle="Clean white walls for a chemist", desc=[
        "&6You remember a laboratory of white stone and light. You can build it again.&r",
        "&eWhat:&r Artemis' Laboratory Blocks adds clean lab walls, tiles, glass, screens, vents and fans.",
        "&eChemistry:&r the recipe uses Nether quartz, which is silicon dioxide (SiO₂), the same compound as sand and glass.",
        "&eHow:&r eight stone around one Nether quartz makes eight laboratory blocks (check JEI). Stonecut them into tiles, pillars and doors."]),
    Q("bd_lab_glow", 2, 17, [item("laboratoryblocks:glowstone_particles", 8), item("laboratoryblocks:glowing_laboratory_block", 8)], "Glowing Panels", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Optional: walls that light the room", desc=[
        "&eWhat:&r glowing laboratory blocks give off light, so a lab can be bright with no torches.",
        "&eHow:&r one glowstone dust makes eight glowstone particles; one particle plus a laboratory block makes a glowing block (check JEI).",
        "&eChemistry:&r real glow-in-the-dark materials store energy from light and release it slowly (phosphorescence). Glowstone just glows; it's magic."]),
    Q("bd_lab_screens", 4, 17, [anyof(LAB_SCREENS, 4)], "Lab Screens", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Optional: monitors on every wall", desc=[
        "&eWhat:&r decorative screens: clear, text, wave and quantum patterns, plain or glowing.",
        "&eHow:&r clear screens from laboratory blocks, laboratory glass and iron screws; add a dye for the patterns (check JEI).",
        "&eTip:&r put a wave screen next to your reactor and a ComputerCraft monitor beside it for real numbers."]),
    Q("bd_lab_fan", 6, 17, [item("laboratoryblocks:laboratory_fan"), item("laboratoryblocks:laboratory_vent", 2)], "Fans and Vents", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Optional: fume extraction", desc=[
        "&eWhat:&r animated lab fans and vents. The redstone-controlled fan only spins when powered.",
        "&eChemistry:&r real labs work with HCl, NH₃ and Cl₂ under a fume hood, which pulls vapours away from your face. Breathing chlorine is a very bad idea.",
        "&eHow:&r laboratory blocks with iron nuggets and iron screws (check JEI)."]),
    Q("bd_lab_doors", 8, 17, [anyof(LAB_DOORS, 2), item("laboratoryblocks:laboratory_glass", 8)], "Lab Doors and Glass", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Optional: see in, keep fumes out", desc=[
        "&eWhat:&r lab doors (solid, glass or mesh) and laboratory glass for viewing windows.",
        "&eHow:&r doors from laboratory blocks; laboratory glass is eight glass around a laboratory block (check JEI).",
        "&eTip:&r a glass wall around your Alchemistry room lets visitors admire it without touching anything."]),
    Q("bd_lab_done", 10, 17, [tick()], "A Proper Laboratory", deps=["bd_lab_glow", "bd_lab_screens", "bd_lab_fan", "bd_lab_doors"], xp=100,
      optional=True, tokens=2, size=1.5, shape="hexagon", subtitle="Optional: build a lab worthy of you", desc=[
        "&6White walls, humming fans, glass and light. You remember this place. It was always where you were happiest.&r",
        "&eWhat:&r a challenge: build a real laboratory around your chemistry machines using these blocks.",
        "&eHow:&r include glowing panels, screens, a fume fan and a glass wall. Click the checkmark when you're proud of it.",
        "&eTip:&r share a screenshot with your server. Bragging rights are a demigod's privilege."]),

    # ===== ATM10-aligned round (2026-10-19): vanilla materials with real geology, and a few tools =====
    Q("bd_rocks", 0, 0, [anyof(["minecraft:stone", "minecraft:deepslate", "minecraft:andesite", "minecraft:diorite", "minecraft:granite",
                                "minecraft:tuff", "minecraft:calcite"], 64)], "Know Your Rocks", deps=["bd_start", "gs_stone"], xp=15,
      optional=True, tokens=1, subtitle="Optional: 64 of any natural stone", desc=[
        "&eWhat:&r stone, deepslate, andesite, diorite, granite, tuff or calcite, mixed as you like. Each has a polished and brick form for building.",
        "&eChemistry:&r granite cooled slowly deep underground, so its quartz and feldspar crystals grew big; andesite and diorite are its iron- and calcium-richer cousins. Tuff is welded volcanic ash, and calcite is CaCO₃.",
        "&eHow:&r mine them with Silk Touch for smooth stone, or smelt cobblestone back into stone.",
        "&eTip:&r the Trowel (Quality of Life page) mixes them into a natural-looking wall."]),
    Q("bd_ru_stones", 0, 0, [item("regions_unexplored:chalk", 16), item("regions_unexplored:argillite", 16), item("regions_unexplored:mossy_stone", 8)], "Rocks of Other Biomes",
      deps=["bd_rocks"], xp=20, optional=True, tokens=1, subtitle="Optional: chalk, argillite and mossy stone", desc=[
        "&eWhat:&r three building stones from Regions Unexplored biomes: white chalk, dark red argillite and mossy stone.",
        "&eChemistry:&r chalk is CaCO₃ made of the tiny plates (coccoliths) of ancient sea algae: the white cliffs of Dover are trillions of them. Argillite is clay squeezed into hard rock.",
        "&eHow:&r find the biomes with Nature's Compass (Quality of Life page) and mine the stone.",
        "&eTip:&r chalk is soft and white; it lights a room almost like the lab blocks."]),
    Q("bd_dripstone", 0, 0, [item("minecraft:pointed_dripstone", 8), item("minecraft:dripstone_block", 8)], "Dripstone", deps=["bd_rocks"], xp=15,
      optional=True, tokens=1, subtitle="Optional: stone that grows", desc=[
        "&eWhat:&r pointed dripstone grows down from the ceiling and up from the floor in dripstone caves. Hanging under a water source, it slowly fills cauldrons below.",
        "&eChemistry:&r water carrying calcium bicarbonate drips, loses CO₂ and leaves calcite behind: Ca(HCO₃)₂ → CaCO₃ + H₂O + CO₂. A real stalactite grows about a centimetre a century.",
        "&eHow:&r mine both in a dripstone cave (Nature's Compass finds one).",
        "&eTip:&r falling pointed dripstone hurts like an arrow. Mind your head."]),
    Q("bd_masonry", 0, 0, [item("minecraft:clay_ball", 16), item("minecraft:brick", 16), item("minecraft:chiseled_stone_bricks", 4), item("minecraft:cobblestone_wall", 8)],
      "Masonry", deps=["bd_start", "gs_furnace"], xp=20, optional=True, tokens=1, subtitle="Optional: clay, bricks and walls", desc=[
        "&eWhat:&r clay fires into bricks; stone bricks chisel into patterns; walls make fences that mobs can't jump.",
        "&eChemistry:&r clay is mostly kaolinite, Al₂Si₂O₅(OH)₄. Fired above about 900 °C it loses its water and the particles sinter together into hard, waterproof ceramic.",
        "&eHow:&r dig clay from riverbeds and lush caves and smelt it into bricks. Chiseled stone bricks come from the stonecutter; walls from cobblestone.",
        "&eTip:&r a stonecutter makes walls, stairs and slabs with no waste."]),
    Q("bd_concrete", 0, 0, [item("minecraft:terracotta", 16), anyof([f"minecraft:{c}_concrete_powder" for c in ("white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
                                                                                                                  "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black")], 16)],
      "Terracotta and Concrete", deps=["bd_masonry"], xp=20, optional=True, tokens=1, subtitle="Optional: colour by the stack", desc=[
        "&eWhat:&r terracotta is fired clay; concrete powder is sand, gravel and dye that sets into concrete when it touches water.",
        "&eChemistry:&r real concrete doesn't dry, it reacts: calcium silicates in cement take up water (hydration) and grow interlocking crystals. It even sets underwater.",
        "&eHow:&r smelt clay blocks into terracotta; 4 sand, 4 gravel and a dye make 8 concrete powder of any colour.",
        "&eTip:&r place powder in front of a water flow, or run it through Create's bulk washing, to harden a whole stack."]),
    Q("bd_lights", 0, 0, [item("minecraft:glowstone_dust", 16), item("minecraft:glowstone", 4), item("minecraft:redstone_lamp", 4), item("minecraft:soul_lantern", 2)],
      "Lighting Without Torches", deps=["bd_start", "t2_nether"], xp=20, optional=True, tokens=1, subtitle="Optional: glowstone, lamps and lanterns", desc=[
        "&eWhat:&r glowstone gives the brightest block light; redstone lamps switch on and off; soul lanterns burn blue and dim.",
        "&eChemistry:&r a flame is incandescence (hot soot glowing). Cold light, from LEDs to glow-sticks, is luminescence: electrons drop between energy levels and give off exactly one colour.",
        "&eHow:&r glowstone from the Nether ceiling (4 dust per block); lamp: glowstone in redstone; soul lantern: a soul torch in iron nuggets.",
        "&eTip:&r a lamp on a daylight detector lights itself at dusk."]),
    Q("bd_froglights", 0, 0, [item("minecraft:ochre_froglight"), item("minecraft:verdant_froglight"), item("minecraft:pearlescent_froglight")], "Froglights",
      deps=["bd_lights", "fd_breed"], xp=60, optional=True, tokens=2, subtitle="Optional: three frogs, three colours", desc=[
        "&eWhat:&r a frog that eats a small magma cube leaves a froglight. Its colour depends on the frog: temperate, warm or cold.",
        "&eChemistry:&r real frogs' skin colour comes from pigment cells stacked in layers: yellow pigment over a layer that scatters blue light makes green, the same trick as a blue sky.",
        "&eHow:&r scoop tadpoles from a swamp in a bucket, raise them in a temperate, a warm and a cold biome, and bring the three frogs to the Nether's magma cubes.",
        "&eTip:&r a lead is the easiest way to walk frogs through a portal."]),
    Q("bd_metal_blocks", 0, 0, [item("minecraft:copper_block", 4), item("minecraft:lapis_block", 2), item("minecraft:quartz_block", 8)], "Mineral Blocks",
      deps=["bd_start", "t2_quartz"], xp=20, optional=True, tokens=1, subtitle="Optional: copper, lapis and quartz to build with", desc=[
        "&eWhat:&r copper blocks weather from orange to green; lapis and quartz blocks are the classic blue and white trims.",
        "&eChemistry:&r copper turns green as it reacts with air, water and CO₂ into basic copper carbonate (the Statue of Liberty's patina). Honeycomb wax stops it, an axe scrapes it back.",
        "&eHow:&r 9 copper ingots or 9 lapis per block; 4 Nether quartz per quartz block. Cut copper and quartz pillars come from the stonecutter.",
        "&eTip:&r copper blocks in Create Deco and Rechiseled take the same patina."]),
    Q("bd_amethyst", 0, 0, [item("minecraft:amethyst_shard", 8), item("minecraft:amethyst_block", 2)], "Amethyst", deps=["bd_start", "gs_ironpick"], xp=20,
      optional=True, tokens=1, subtitle="Optional: purple quartz from a geode", desc=[
        "&eWhat:&r amethyst clusters grow on budding amethyst inside underground geodes. Shards make spyglasses, tinted glass and amethyst blocks that chime.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured violet by traces of iron that natural radiation has nudged into Fe⁴⁺ colour centres. Heat it and it turns yellow (citrine).",
        "&eHow:&r break fully grown clusters in a geode (calcite and smooth basalt shells), and craft 4 shards into a block.",
        "&eTip:&r never break the budding amethyst: it can't be moved and it's the only thing that grows more."]),
    Q("bd_ice", 0, 0, [item("minecraft:snow_block", 8), item("minecraft:packed_ice", 8), item("minecraft:blue_ice", 2)], "Building with Ice", deps=["bd_start"], xp=20,
      optional=True, tokens=1, subtitle="Optional: snow, packed ice and blue ice", desc=[
        "&eWhat:&r snow blocks, packed ice (doesn't melt) and blue ice, the slipperiest block in the game: boats on blue ice outrun horses.",
        "&eChemistry:&r ice floats because hydrogen bonds lock water into an open hexagonal lattice, about 9% less dense than liquid water. That's why lakes freeze from the top.",
        "&eHow:&r 4 snowballs make a snow block; 9 ice make packed ice, 9 packed ice make blue ice. Ice needs Silk Touch; icebergs have packed and blue ice.",
        "&eTip:&r a blue-ice boat road in the Nether makes long trips fast."]),
    Q("bd_nether_masonry", 0, 0, [item("minecraft:polished_blackstone", 16), item("minecraft:gilded_blackstone"), item("minecraft:chain", 4)], "Nether Masonry",
      deps=["bd_start", "t2_blackstone"], xp=20, optional=True, tokens=1, subtitle="Optional: blackstone, gold-flecked stone and chains", desc=[
        "&eWhat:&r polished blackstone and its bricks make dark, gothic builds; gilded blackstone sparkles with gold; chains hang lanterns.",
        "&eChemistry:&r gold in veins inside dark rock is how real gold is often found: hot water carries dissolved gold through cracks and drops it as it cools.",
        "&eHow:&r polish blackstone in a stonecutter. Gilded blackstone is found in bastions. Chain: an iron ingot between two iron nuggets.",
        "&eTip:&r gilded blackstone sometimes drops gold nuggets when mined without Silk Touch."]),
    Q("bd_end_stone", 0, 0, [item("minecraft:end_stone", 16), item("minecraft:end_stone_bricks", 8)], "End Stone", deps=["bd_start", "w_end"], xp=20,
      optional=True, tokens=1, subtitle="Optional: pale stone from the void", desc=[
        "&eWhat:&r end stone and its bricks: pale yellow and very blast-resistant. Chorus plants grow only on it.",
        "&eHow:&r mine end stone on any End island; 4 end stone make 4 end stone bricks.",
        "&eTip:&r end stone resists explosions far better than cobblestone, so wall in anything that might blow."]),
    Q("bd_vanilla_decor", 0, 0, [item("minecraft:painting", 2), item("minecraft:carved_pumpkin"), item("minecraft:cauldron"),
                                 anyof(["minecraft:stripped_oak_log", "minecraft:stripped_spruce_log", "minecraft:stripped_birch_log", "minecraft:stripped_jungle_log",
                                        "minecraft:stripped_acacia_log", "minecraft:stripped_dark_oak_log", "minecraft:stripped_mangrove_log",
                                        "minecraft:stripped_cherry_log"], 8)],
      "Finishing Touches", deps=["bd_start", "gs_iron"], xp=15, optional=True, tokens=1, subtitle="Optional: paintings, a pumpkin, a cauldron, clean beams", desc=[
        "&eWhat:&r the small things that make a base feel lived in: paintings, a carved pumpkin, a cauldron and stripped-log beams.",
        "&eChemistry:&r stripping a log takes off the bark, which is full of tannins: the same polyphenols that tan leather.",
        "&eHow:&r painting: sticks around wool. Carve a pumpkin with shears. Cauldron: 7 iron. Use an axe on any log to strip it.",
        "&eTip:&r a cauldron under pointed dripstone fills with water by itself."]),
    Q("bd_diamond_block", 0, 0, [item("minecraft:diamond_block")], "Showing Off", deps=["bd_metal_blocks", "hv_iron"], xp=50,
      secret=True, loot="secret", subtitle="Secret: nine diamonds you'll never use", desc=[
        "&6You remember a throne cut from a single gem. A block of diamond on the mantelpiece is a start.&r",
        "&eWhat:&r a block of diamond, placed only to be looked at.",
        "&eChemistry:&r a diamond block's worth of real diamond would be about 3.5 tonnes of pure carbon. Burn it and you'd get about 13 tonnes of CO₂."]),
    Q("bd_tool_extras", 0, 0, [item("framedblocks:framing_saw"), item("mcwwindows:hammer"), item("constructionstick:template_angel")], "Tool Extras",
      deps=["bd_framed", "bd_mcw_windows", "bd_stick_diamond"], xp=30, optional=True, tokens=1, subtitle="Optional: a saw, a hammer and an angel template", desc=[
        "&eWhat:&r the Framing Saw crafts any framed shape from plain framed cubes; the Window Hammer reshapes a placed Macaw's window; the Angel template lets a Construction Stick place blocks in mid-air.",
        "&eHow:&r check JEI for each. Apply the template to a stick at a smithing table.",
        "&eTip:&r the angel template is a building aid, not flight. Flight in this pack is a chemistry milestone."]),
    Q("bd_spikes", 0, 0, [item("supplementaries:bamboo_spikes", 4)], "Bamboo Spikes", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="Optional: a garden of sharp sticks", desc=[
        "&eWhat:&r Supplementaries bamboo spikes hurt mobs that walk on them; coated with a lingering potion they poison them too.",
        "&eHow:&r 4 bamboo over 3 wooden slabs (check JEI). Use a lingering potion on placed spikes to coat them.",
        "&eTip:&r a ring of spikes around a farm keeps zombies off the crops."]),
], links=[("gs_table", -2, 0), ("t3_hull", -2, 2), ("cr_deco", -2, 15), ("t2_quartz", -2, 17)])
