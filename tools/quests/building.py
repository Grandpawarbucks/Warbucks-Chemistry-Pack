"""Quest chapter: building (sidebar title "Building Tips"). See tools/quests/STYLE.md.

Restructured 2026-10-19 to the shape of ATM10's building page: one hub in the middle (bd_start) and themed
clusters around it, each with its own hub (a 1.5 hexagon) and a handful of tips: Building Tools, Chisels and
Frames, Stone and Masonry, Stone of Other Worlds, Wood, Glass, Light, Colour, Furniture, House Parts, Outdoors,
Supplementaries, Metal and Industry, The Laboratory. Every quest is an optional tip (tokens=1); the radial layout
draws the clusters as spokes with labelled headers. Quest keys are unchanged; some quests moved cluster (deps
changed), and Rechiseled's quest now asks for the chisel itself (its ids are in test/ids.tsv now).
q_effortless / q_gadget / q_gadget_copy / q_gadget_exchange moved here from qol.py earlier (keys unchanged).
"""
from questlib import Q, Chapter, item, dim, tick, anyof, anytag, IDS, MAIN, SIDE  # noqa: F401

WOODS = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove", "cherry", "bamboo", "crimson", "warped"]
STONES = ["stone", "cobblestone", "andesite", "brick", "sandstone"]
COLOURS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan",
           "purple", "blue", "brown", "green", "red", "black"]


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
STAIR_MATS = ["oak", "spruce", "birch", "dark_oak", "stone_brick", "cobblestone", "andesite"]
MCW_STAIRS = [f"mcwstairs:{m}_{s}" for m in STAIR_MATS for s in ("loft_stairs", "skyline_stairs", "terrace_stairs", "bulk_stairs", "compact_stairs")
              if f"mcwstairs:{m}_{s}" in IDS]
MCW_BALCONY = [f"mcwstairs:{m}_{s}" for m in STAIR_MATS for s in ("balcony", "railing", "platform") if f"mcwstairs:{m}_{s}" in IDS]
# Rechiseled's connecting variants (blocks that merge their texture with their neighbours), a readable sample.
RECHISELED_CONNECTING = sorted(i for i in IDS if i.startswith("rechiseled:") and i.endswith("_connecting")
                               and "_slab" not in i and "_stairs" not in i
                               and i.split(":")[1].startswith(("stone_bricks_", "cobblestone_", "oak_planks_", "iron_block_",
                                                               "copper_block_", "spruce_planks_")))[:40]
DECO_METALS = ["andesite", "brass", "copper", "iron", "zinc", "industrial_iron"]
DECO_LAMPS = variants("createdeco:{}_lamp", [f"{c}_{m}" for m in ("andesite", "brass", "copper", "iron", "zinc")
                                             for c in ("yellow", "red", "green", "blue")])
DYES = [f"minecraft:{c}_dye" for c in COLOURS]

CHAPTER = Chapter("building", "Building Tips", "framedblocks:framed_hammer",
        ["A god's house should look like one."], SIDE, [
    # ===== The hub =====================================================================================
    Q("bd_start", 0, 0, [tick()], "Building Tips", deps=["gs_table"], xp=10, size=2.0, shape="gear",
      optional=True, tokens=1, icon="minecraft:grass_block", subtitle="Tools and blocks for a base worth living in", desc=[
        "&6You remember raising cities with a gesture. For now, a few clever tools will do.&r",
        "&eWhat:&r this page is a catalogue of the pack's building mods and decoration, one cluster per theme around this quest.",
        "&eHow:&r everything here is optional and cheap. Pick a cluster that suits your next build and work outward.",
        "&eTip:&r a stonecutter makes stairs, slabs, walls and patterns with no waste. Use it for every stone on this page."]),

    # ===== Building Tools ===============================================================================
    Q("bd_stick", 0, 0, [item("constructionstick:wooden_stick")], "Construction Stick", deps=["bd_start"], xp=15,
      section="Building Tools", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Extend a wall in one click", desc=[
        "&eWhat:&r a Construction Stick places a whole row or face of blocks matching the one you click, from your inventory.",
        "&eHow:&r three sticks in a column (check JEI). Right-click the face of a wall to grow it by one layer.",
        "&eTip:&r the tooltip lists its modes, such as only extending in a straight line."]),
    Q("bd_stick_diamond", 0, 0, [item("constructionstick:diamond_stick")], "Diamond Stick", deps=["bd_stick"], xp=30,
      optional=True, tokens=1, subtitle="Bigger reach, more durability", desc=[
        "&eWhat:&r better sticks place more blocks per click and last longer: copper, iron, diamond, then netherite.",
        "&eChemistry:&r diamond is pure carbon in a tight 3D lattice, which makes it the hardest natural material.",
        "&eHow:&r a diamond on two sticks (check JEI). Templates at a smithing table add tricks such as replacing blocks."]),
    Q("bd_tool_extras", 0, 0, [item("framedblocks:framing_saw"), item("mcwwindows:hammer"), item("constructionstick:template_angel")], "Tool Extras",
      deps=["bd_stick_diamond"], xp=30, optional=True, tokens=1, subtitle="A saw, a hammer and an angel template", desc=[
        "&eWhat:&r the Framing Saw crafts any framed shape from framed cubes; the Window Hammer reshapes a placed Macaw's window; the Angel template lets a stick place blocks in mid-air.",
        "&eHow:&r check JEI for each. Apply the template to a stick at a smithing table.",
        "&eTip:&r the angel template is a building aid, not flight. Flight in this pack is a chemistry milestone."]),
    Q("q_effortless", 0, 0, [item("effortlessbuilding:randomizer_tool")], "Effortless Building", deps=["bd_stick"], xp=20,
      optional=True, tokens=1, subtitle="Mirror, array and line building", desc=[
        "&eWhat:&r Effortless Building adds mirror, array and line modes for big symmetric builds.",
        "&eHow:&r open its menu (check Controls) and pick a mode. The randomizer places a random mix of the blocks you load into it.",
        "&eTip:&r load the randomizer with stone, andesite and cobblestone for natural-looking walls."]),
    Q("bd_scaffolding", 0, 0, [item("minecraft:scaffolding", 16)], "Scaffolding", deps=["bd_stick"], xp=15,
      optional=True, tokens=1, subtitle="Climb up, sneak down, break the base", desc=[
        "&eWhat:&r scaffolding stacks upward and outward, you climb it like a ladder, and breaking the bottom brings the whole tower down.",
        "&eChemistry:&r bamboo is a grass whose stems are stiffened with lignin and silica, which is why real scaffolds have used it for centuries.",
        "&eHow:&r six bamboo and a string make six scaffolding (check JEI). Sneak to climb down."]),
    Q("q_gadget", 0, 0, [item("buildinggadgets2:gadget_building")], "Building Gadgets", deps=["bd_stick", "t3_hull"], xp=40,
      optional=True, tokens=1, subtitle="Place whole surfaces with FE", desc=[
        "&eWhat:&r FE-powered gadgets that place, swap, copy and remove blocks in bulk.",
        "&eHow:&r iron, redstone, lapis and a diamond (check JEI). Charge it in any energy storage block.",
        "&eTip:&r link the gadget to a chest or backpack so it pulls blocks from storage."]),
    Q("q_gadget_copy", 0, 0, [item("buildinggadgets2:gadget_copy_paste"), item("buildinggadgets2:template_manager")], "Copy and Paste", deps=["q_gadget"], xp=60,
      optional=True, tokens=1, subtitle="Copy a whole build", desc=[
        "&eWhat:&r copy an area and paste it elsewhere; the Template Manager saves copies to share.",
        "&eHow:&r check JEI. Great for repeating a row of furnaces or a decorated wall.",
        "&eTip:&r templates can be shared with friends on the server."]),
    Q("q_gadget_exchange", 0, 0, [item("buildinggadgets2:gadget_exchanging")], "Exchanging Gadget", deps=["q_gadget"], xp=40,
      optional=True, tokens=1, subtitle="Swap blocks in place", desc=[
        "&eWhat:&r replaces blocks in an area with another block, keeping the shape.",
        "&eHow:&r check JEI. Perfect for turning a cobblestone shell into something pretty.",
        "&eTip:&r it uses the blocks in your inventory, so carry enough."]),
    Q("bd_gadget_destroy", 0, 0, [item("buildinggadgets2:gadget_destruction")], "Destruction Gadget", deps=["q_gadget"], xp=40,
      optional=True, tokens=1, subtitle="Clear a room in seconds", desc=[
        "&eWhat:&r removes a box of blocks in front of you, sized however you like. It can undo its last action.",
        "&eHow:&r check JEI. Set the depth, width and height in its menu.",
        "&eTip:&r perfect for hollowing out a hillside for a new factory floor."]),

    # ===== Chisels and Frames ===========================================================================
    Q("bd_chisel", 0, 0, [item("rechiseled:chisel")], "Rechiseled", deps=["bd_start", "gs_iron"], xp=15,
      section="Chisels and Frames", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Hundreds of block patterns", desc=[
        "&eWhat:&r Rechiseled's chisel turns stone, planks, metal blocks and more into patterns: bricks, tiles, pillars, gears.",
        "&eHow:&r an iron ingot on a stick (check JEI). Right-click to open it, put blocks in and pick a pattern.",
        "&eTip:&r iron and copper block patterns make a machine room look deliberate."]),
    Q("bd_chisel_connect", 0, 0, [anyof(RECHISELED_CONNECTING, 16)], "Connected Textures", deps=["bd_chisel"], xp=20,
      optional=True, tokens=1, subtitle="Patterns that merge with their neighbours", desc=[
        "&eWhat:&r every Rechiseled pattern has a connecting version whose texture joins up with the same block next to it, so a wall reads as one panel.",
        "&eHow:&r chisel any sixteen connecting blocks of stone bricks, cobblestone, planks, iron or copper (the chisel shows the connecting versions next to the plain ones).",
        "&eTip:&r mix plain and connecting versions to frame a window or a doorway."]),
    Q("bd_framed", 0, 0, [item("framedblocks:framed_cube", 8), item("framedblocks:framed_hammer")], "Framed Blocks", deps=["bd_chisel"], xp=20,
      optional=True, tokens=1, subtitle="Any shape, any texture", desc=[
        "&eWhat:&r FramedBlocks are wooden frames that take the look of any block you right-click into them, in dozens of shapes.",
        "&eHow:&r framed cubes are planks and sticks (check JEI). Right-click one with a full block to apply it; the Framed Hammer takes it off.",
        "&eTip:&r camouflage with glass, ores or machine casings: the block keeps its shape and takes the texture."]),
    Q("bd_framed_shapes", 0, 0, [anyof(FRAMED_SHAPES, 6)], "Slopes and Panels", deps=["bd_framed"], xp=20,
      optional=True, tokens=1, subtitle="Six framed shapes", desc=[
        "&eWhat:&r any six framed slopes, corner slopes, stairs, slabs, panels, pillars or prisms.",
        "&eHow:&r each shape is made from framed cubes (check JEI). Most come several at a time.",
        "&eTip:&r framed slopes camouflaged as stone make roofs and ramps that look hand-carved."]),
    Q("bd_framed_secret", 0, 0, [item("framedblocks:framed_secret_storage")], "Secret Storage", deps=["bd_framed_shapes"], xp=30,
      optional=True, tokens=1, subtitle="A chest that looks like a wall", desc=[
        "&eWhat:&r a full-block chest that wears any block's texture, so it disappears into a wall.",
        "&eHow:&r a framed chest surrounded by framed cubes (check JEI), then camouflage it.",
        "&eTip:&r hide your rarest elements in one. Nobody suspects the third stone brick from the left."]),
    Q("bd_copycat", 0, 0, [item("copycats:copycat_block", 2), anyof(["copycats:copycat_slope", "copycats:copycat_stairs", "copycats:copycat_board",
                                                                     "copycats:copycat_beam", "copycats:copycat_slice", "copycats:copycat_vertical_slope"], 4)],
      "Copycats", deps=["bd_chisel", "cr_casing"], xp=25,
      optional=True, tokens=1, subtitle="Create-style shape-shifting blocks", desc=[
        "&eWhat:&r Copycats+ adds many more Create copycat shapes: slopes, boards, beams, slices. Each takes the look of the block you apply.",
        "&eHow:&r cut zinc ingots in a stonecutter (check JEI), then right-click a placed copycat with a block.",
        "&eTip:&r copycat boards cover pipes and shafts while leaving them working."]),

    # ===== Stone and Masonry ============================================================================
    Q("bd_rocks", 0, 0, [anyof(["minecraft:stone", "minecraft:deepslate", "minecraft:andesite", "minecraft:diorite", "minecraft:granite",
                                "minecraft:tuff", "minecraft:calcite"], 64)], "Know Your Rocks", deps=["bd_start", "gs_stone"], xp=15,
      section="Stone and Masonry", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="64 of any natural stone", desc=[
        "&eWhat:&r stone, deepslate, andesite, diorite, granite, tuff or calcite, mixed as you like. Each has polished and brick forms.",
        "&eChemistry:&r granite cooled slowly deep underground, so its quartz and feldspar crystals grew large. Tuff is welded volcanic ash, and calcite is CaCO₃.",
        "&eTip:&r the Trowel (Quality of Life page) mixes them into a natural-looking wall."]),
    Q("bd_masonry", 0, 0, [item("minecraft:clay_ball", 16), item("minecraft:brick", 16), item("minecraft:chiseled_stone_bricks", 4), item("minecraft:cobblestone_wall", 8)],
      "Masonry", deps=["bd_rocks", "gs_furnace"], xp=20, optional=True, tokens=1, subtitle="Clay, bricks and walls", desc=[
        "&eWhat:&r clay fires into bricks; stone bricks chisel into patterns; walls make fences mobs can't jump.",
        "&eChemistry:&r clay is mostly kaolinite, Al₂Si₂O₅(OH)₄. Fired above about 900 °C it loses its water and sinters into hard, waterproof ceramic.",
        "&eHow:&r dig clay from riverbeds and lush caves and smelt it. Chiseled stone bricks and walls come from the stonecutter."]),
    Q("bd_mud", 0, 0, [item("minecraft:packed_mud", 8), item("minecraft:mud_bricks", 8)], "Mud Bricks", deps=["bd_masonry"], xp=15,
      optional=True, tokens=1, subtitle="The oldest building block there is", desc=[
        "&eWhat:&r mud packs with wheat into packed mud, which cuts into warm brown mud bricks.",
        "&eChemistry:&r sun-dried mud brick (adobe) binds clay particles with straw fibres; it hardens by drying, not by firing, so it needs a roof to stay dry.",
        "&eHow:&r use a water bottle on dirt to make mud, craft it with wheat into packed mud, then four packed mud make mud bricks."]),
    Q("bd_deepslate", 0, 0, [anyof(["minecraft:deepslate_tiles", "minecraft:deepslate_bricks", "minecraft:polished_deepslate",
                                    "minecraft:tuff_bricks", "minecraft:polished_tuff", "minecraft:chiseled_tuff"], 32)], "Deep Stone", deps=["bd_rocks"], xp=15,
      optional=True, tokens=1, subtitle="Deepslate and tuff, cut and polished", desc=[
        "&eWhat:&r deepslate tiles and bricks, and tuff bricks from the trial chambers' palette: dark, heavy-looking stone for foundations.",
        "&eChemistry:&r deepslate is a metamorphic rock: older stone squeezed and heated far underground until its minerals lined up in layers.",
        "&eHow:&r any 32 of them, cut from cobbled deepslate or tuff in a stonecutter."]),
    Q("bd_sandstone", 0, 0, [anyof(["biomesoplenty:white_sandstone", "biomesoplenty:orange_sandstone", "biomesoplenty:black_sandstone",
                                    "biomesoplenty:smooth_white_sandstone", "biomesoplenty:smooth_orange_sandstone", "biomesoplenty:smooth_black_sandstone",
                                    "minecraft:sandstone", "minecraft:red_sandstone"], 32)], "Coloured Sandstone", deps=["bd_rocks"], xp=15,
      optional=True, tokens=1, subtitle="White, orange, red and black sand", desc=[
        "&eWhat:&r Biomes O' Plenty adds white, orange and black sands; each makes its own sandstone.",
        "&eChemistry:&r white sand is nearly pure quartz (SiO₂), orange and red sand are stained by iron oxides, and black sand is ground volcanic rock rich in magnetite.",
        "&eHow:&r any 32 sandstone blocks of any colour. Four sand make one sandstone."]),
    Q("bd_ru_stones", 0, 0, [item("regions_unexplored:chalk", 16), item("regions_unexplored:argillite", 16), item("regions_unexplored:mossy_stone", 8)], "Rocks of Other Biomes",
      deps=["bd_rocks"], xp=20, optional=True, tokens=1, subtitle="Chalk, argillite and mossy stone", desc=[
        "&eWhat:&r three building stones from Regions Unexplored biomes: white chalk, dark red argillite and mossy stone.",
        "&eChemistry:&r chalk is CaCO₃ made of the tiny plates of ancient sea algae. Argillite is clay squeezed into hard rock.",
        "&eHow:&r find the biomes with Nature's Compass (Quality of Life page) and mine the stone."]),
    Q("bd_dripstone", 0, 0, [item("minecraft:pointed_dripstone", 8), item("minecraft:dripstone_block", 8)], "Dripstone", deps=["bd_rocks"], xp=15,
      optional=True, tokens=1, subtitle="Stone that grows", desc=[
        "&eWhat:&r pointed dripstone grows in dripstone caves; hanging under a water source, it slowly fills a cauldron below.",
        "&eChemistry:&r dripping water loses CO₂ and leaves calcite behind: Ca(HCO₃)₂ → CaCO₃ + H₂O + CO₂. A real stalactite grows about a centimetre a century.",
        "&eHow:&r mine both in a dripstone cave (Nature's Compass finds one)."]),
    Q("bd_amethyst", 0, 0, [item("minecraft:amethyst_shard", 8), item("minecraft:amethyst_block", 2)], "Amethyst", deps=["bd_rocks", "gs_ironpick"], xp=20,
      optional=True, tokens=1, subtitle="Purple quartz from a geode", desc=[
        "&eWhat:&r amethyst grows on budding amethyst inside underground geodes. Shards make spyglasses, tinted glass and blocks that chime.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured violet by traces of iron that natural radiation has turned into colour centres.",
        "&eTip:&r never break the budding amethyst: it can't be moved and it's the only thing that grows more."]),
    Q("bd_ice", 0, 0, [item("minecraft:snow_block", 8), item("minecraft:packed_ice", 8), item("minecraft:blue_ice", 2)], "Building with Ice", deps=["bd_rocks"], xp=20,
      optional=True, tokens=1, subtitle="Snow, packed ice and blue ice", desc=[
        "&eWhat:&r snow blocks, packed ice (it doesn't melt) and blue ice, the slipperiest block in the game.",
        "&eChemistry:&r ice floats because hydrogen bonds lock water into an open hexagonal lattice, about 9% less dense than liquid water.",
        "&eHow:&r 4 snowballs make a snow block; 9 ice make packed ice, 9 packed ice make blue ice. Icebergs have both."]),

    # ===== Stone of Other Worlds ========================================================================
    Q("bd_nether_masonry", 0, 0, [item("minecraft:polished_blackstone", 16), item("minecraft:gilded_blackstone"), item("minecraft:chain", 4)], "Nether Masonry",
      deps=["bd_start", "t2_blackstone"], xp=20, section="Stone of Other Worlds", size=1.5, shape="hexagon",
      optional=True, tokens=1, subtitle="Blackstone, gold-flecked stone and chains", desc=[
        "&eWhat:&r polished blackstone makes dark, gothic builds; gilded blackstone sparkles with gold; chains hang lanterns.",
        "&eChemistry:&r gold in dark rock is how real gold is often found: hot water carries dissolved gold through cracks and drops it as it cools.",
        "&eHow:&r polish blackstone in a stonecutter. Gilded blackstone is found in bastions. Chain: an iron ingot between two iron nuggets."]),
    Q("bd_brimstone", 0, 0, [item("biomesoplenty:brimstone", 16), item("biomesoplenty:brimstone_bricks", 8)], "Brimstone", deps=["bd_nether_masonry"], xp=20,
      optional=True, tokens=1, subtitle="Yellow stone from the Nether's vents", desc=[
        "&eWhat:&r Biomes O' Plenty's brimstone covers volcanic Nether biomes, around fumaroles that puff smoke.",
        "&eChemistry:&r \"brimstone\" is the old name for sulfur. Real volcanic vents deposit yellow sulfur crystals as hot H₂S and SO₂ gases cool and react.",
        "&eHow:&r mine brimstone in the Nether (Nature's Compass finds the biome) and craft or cut it into bricks."]),
    Q("bd_end_stone", 0, 0, [item("minecraft:end_stone", 16), item("minecraft:end_stone_bricks", 8)], "End Stone", deps=["bd_nether_masonry", "w_end"], xp=20,
      optional=True, tokens=1, subtitle="Pale stone from the void", desc=[
        "&eWhat:&r end stone and its bricks: pale yellow and very blast-resistant. Chorus plants grow only on it.",
        "&eHow:&r mine end stone on any End island; 4 end stone make 4 end stone bricks.",
        "&eTip:&r end stone resists explosions far better than cobblestone, so wall in anything that might blow."]),
    Q("bd_purpur", 0, 0, [item("minecraft:purpur_block", 8), item("minecraft:purpur_pillar", 4)], "Purpur", deps=["bd_end_stone"], xp=20,
      optional=True, tokens=1, subtitle="The End cities' purple stone", desc=[
        "&eWhat:&r purpur blocks and pillars are what End cities are built from.",
        "&eHow:&r pop chorus fruit in a furnace, then four popped fruit make four purpur blocks; pillars come from the stonecutter.",
        "&eTip:&r chorus plants regrow from their flowers on end stone, so you can farm purpur at home."]),
    Q("bd_prismarine", 0, 0, [item("minecraft:prismarine_bricks", 8), item("minecraft:dark_prismarine", 8)], "Prismarine", deps=["bd_nether_masonry", "hn_guardian"], xp=25,
      optional=True, tokens=1, subtitle="Sea-green stone from the monuments", desc=[
        "&eWhat:&r prismarine bricks and dark prismarine, the stone of ocean monuments, made from guardians' shards.",
        "&eChemistry:&r real sea creatures build shells from calcium carbonate and silica drawn out of seawater, which is where reef stone comes from.",
        "&eHow:&r 9 prismarine shards make prismarine bricks; 8 shards around a black dye make dark prismarine."]),
    Q("bd_ug_stone", 0, 0, [anyof(["undergarden:depthrock_bricks", "undergarden:shiverstone_bricks", "undergarden:tremblecrust_bricks",
                                   "undergarden:depthrock_tiles", "undergarden:chiseled_depthrock_bricks", "undergarden:dreadrock_bricks"], 16)],
      "Undergarden Bricks", deps=["bd_nether_masonry", "t4_undergarden"], xp=25, optional=True, tokens=1, subtitle="Depthrock, shiverstone and tremblecrust", desc=[
        "&eWhat:&r the Undergarden's stones cut into bricks and tiles: grey depthrock, icy shiverstone and cracked tremblecrust.",
        "&eHow:&r mine the stone in the Undergarden and use a stonecutter or crafting grid (check JEI). Any 16.",
        "&eTip:&r depthrock bricks make a fine floor for a room that should feel underground."]),
    Q("bd_tf_stone", 0, 0, [anyof(["twilightforest:castle_brick", "twilightforest:mazestone_brick", "twilightforest:underbrick",
                                   "twilightforest:nagastone", "twilightforest:etched_nagastone", "twilightforest:mossy_castle_brick"], 16)],
      "Twilight Stonework", deps=["bd_nether_masonry", "t5_twilight"], xp=25, optional=True, tokens=1, subtitle="Castle brick, mazestone and nagastone", desc=[
        "&eWhat:&r the Twilight Forest's ruins are built from stone you can take home: castle brick, mazestone, underbrick and the Naga's scaled stone.",
        "&eHow:&r mine them in the Naga courtyard, the labyrinth and the castle (or craft them, check JEI). Any 16.",
        "&eTip:&r castle brick is very hard to break, which makes it a sturdy outer wall."]),

    # ===== Wood =========================================================================================
    Q("bd_logs", 0, 0, [anytag("minecraft:logs", 64)], "A Stack of Logs", deps=["bd_start", "gs_logs"], xp=15,
      section="Wood", size=1.5, shape="hexagon", optional=True, tokens=1, icon="minecraft:oak_log", subtitle="64 logs of any tree", desc=[
        "&eWhat:&r every wood in the pack has its own colour and grain. A full stack lets you try them side by side.",
        "&eChemistry:&r wood is cellulose fibres glued with lignin. Lignin's aromatic rings are what turn wood brown when it ages in sunlight.",
        "&eTip:&r Ultimine fells a whole tree at once, and saplings from each wood are worth keeping."]),
    Q("bd_vanilla_decor", 0, 0, [item("minecraft:painting", 2), item("minecraft:carved_pumpkin"), item("minecraft:cauldron"),
                                 anyof(["minecraft:stripped_oak_log", "minecraft:stripped_spruce_log", "minecraft:stripped_birch_log", "minecraft:stripped_jungle_log",
                                        "minecraft:stripped_acacia_log", "minecraft:stripped_dark_oak_log", "minecraft:stripped_mangrove_log",
                                        "minecraft:stripped_cherry_log"], 8)],
      "Finishing Touches", deps=["bd_logs", "gs_iron"], xp=15, optional=True, tokens=1, subtitle="Paintings, a pumpkin, a cauldron, clean beams", desc=[
        "&eWhat:&r the small things that make a base feel lived in: paintings, a carved pumpkin, a cauldron and stripped-log beams.",
        "&eChemistry:&r stripping a log takes off the bark, which is full of tannins: the same polyphenols that tan leather.",
        "&eHow:&r painting: sticks around wool. Carve a pumpkin with shears. Cauldron: 7 iron. Use an axe on any log to strip it."]),
    Q("bd_timber", 0, 0, [item("supplementaries:timber_frame", 8), anyof(["supplementaries:timber_brace", "supplementaries:timber_cross_brace"], 4)],
      "Timber Framing", deps=["bd_logs"], xp=15, optional=True, tokens=1, subtitle="Tudor walls, one frame at a time", desc=[
        "&eWhat:&r Supplementaries' timber frames, braces and cross braces sit over a wall to make half-timbered houses.",
        "&eHow:&r craft them from sticks (check JEI), then right-click a frame with a block to fill it, like daub or plaster.",
        "&eTip:&r white-filled frames over a stone ground floor read as a proper village house."]),
    Q("bd_bop_wood", 0, 0, [anyof(variants("biomesoplenty:{}_planks", ["fir", "pine", "maple", "redwood", "mahogany", "jacaranda", "palm",
                                                                         "willow", "dead", "magic", "umbran", "hellbark", "empyreal"]), 32)],
      "Biomes O' Plenty Woods", deps=["bd_logs"], xp=20, optional=True, tokens=1, subtitle="Pink jacaranda, blue magic, red maple", desc=[
        "&eWhat:&r Biomes O' Plenty grows a dozen new trees, from pale fir to bright pink jacaranda and blue magic wood.",
        "&eHow:&r any 32 planks from its woods. Nature's Compass finds the biomes.",
        "&eTip:&r maple and jacaranda leaves make colourful hedges with Macaw's Fences."]),
    Q("bd_ru_wood", 0, 0, [anyof(variants("regions_unexplored:{}_planks", ["baobab", "blackwood", "cypress", "eucalyptus", "joshua", "kapok", "larch",
                                                                             "magnolia", "maple", "palm", "pine", "redwood", "socotra", "willow", "brimwood",
                                                                             "cobalt"]), 32)],
      "Regions Unexplored Woods", deps=["bd_logs"], xp=20, optional=True, tokens=1, subtitle="Baobab, eucalyptus, blackwood and more", desc=[
        "&eWhat:&r Regions Unexplored adds its own trees, including baobab, eucalyptus, larch, blackwood and the Nether's brimwood.",
        "&eHow:&r any 32 planks from its woods.",
        "&eChemistry:&r eucalyptus leaves are rich in eucalyptol (C₁₀H₁₈O), the oil that gives cough drops their smell."]),
    Q("bd_tf_wood", 0, 0, [anyof(["twilightforest:twilight_oak_planks", "twilightforest:canopy_planks", "twilightforest:mangrove_planks",
                                  "twilightforest:dark_planks", "twilightforest:time_planks", "twilightforest:transformation_planks",
                                  "twilightforest:mining_planks", "twilightforest:sorting_planks"], 32)],
      "Twilight Woods", deps=["bd_logs", "t5_twilight"], xp=20, optional=True, tokens=1, subtitle="Canopy, darkwood and the magic trees", desc=[
        "&eWhat:&r the Twilight Forest's woods: twilight oak, canopy, mangrove, darkwood, and the planks of its four magic trees.",
        "&eHow:&r any 32 planks. The magic trees' cores are worth more as machines than as planks, so cut their trunks instead.",
        "&eTip:&r darkwood is nearly black; it pairs well with lab blocks."]),
    Q("bd_ug_wood", 0, 0, [anyof(["undergarden:smogstem_planks", "undergarden:wigglewood_planks", "undergarden:grongle_planks"], 32)],
      "Undergarden Woods", deps=["bd_logs", "t4_undergarden"], xp=20, optional=True, tokens=1, subtitle="Smogstem, wigglewood and grongle", desc=[
        "&eWhat:&r three woods from trees that grow without sunlight in the Undergarden.",
        "&eHow:&r any 32 smogstem, wigglewood or grongle planks.",
        "&eChemistry:&r real plants can't grow without light; deep-sea and cave life lives on chemosynthesis instead, oxidising H₂S or methane for energy."]),

    # ===== Glass ========================================================================================
    Q("bd_glass", 0, 0, [item("minecraft:glass", 32)], "Glass", deps=["bd_start", "gs_furnace"], xp=15,
      section="Glass", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Sand, heat and a lot of light", desc=[
        "&eWhat:&r a stack and a half of glass for windows, roofs and greenhouses.",
        "&eChemistry:&r glass is mostly silica (SiO₂) melted with soda (Na₂CO₃) and lime (CaO), then cooled before it can crystallise.",
        "&eHow:&r smelt sand. The pack's furnaces cook four times faster, so a stack is quick."]),
    Q("bd_mcw_windows", 0, 0, [anyof(variants("mcwwindows:{}_window") + variants("mcwwindows:{}_pane_window")
                                     + variants("mcwwindows:{}_four_window"), 4)], "Windows", deps=["bd_glass"], xp=15,
      optional=True, tokens=1, subtitle="Framed windows, shutters and curtains", desc=[
        "&eWhat:&r Macaw's Windows adds framed windows, shutters, curtains, blinds and parapets.",
        "&eHow:&r any four framed windows (check JEI).",
        "&eTip:&r the Window Hammer reshapes a placed window without breaking it."]),
    Q("bd_stained_glass", 0, 0, [anyof([f"minecraft:{c}_stained_glass" for c in COLOURS], 16)], "Stained Glass", deps=["bd_glass"], xp=15,
      optional=True, tokens=1, subtitle="Colour in the light", desc=[
        "&eWhat:&r 8 glass around a dye make 8 stained glass. Beacon beams take the colour of glass above them.",
        "&eChemistry:&r medieval stained glass got its colour from metal oxides: cobalt for blue, copper for green, and tiny gold particles for ruby red.",
        "&eHow:&r any 16 stained glass of any colour."]),
    Q("bd_tinted_glass", 0, 0, [item("minecraft:tinted_glass", 4)], "Tinted Glass", deps=["bd_glass"], xp=20,
      optional=True, tokens=1, subtitle="A window that blocks light", desc=[
        "&eWhat:&r tinted glass looks dark and lets no light through, so mobs can spawn behind it but you can still see in.",
        "&eHow:&r one glass surrounded by four amethyst shards makes two (check JEI).",
        "&eTip:&r a tinted roof over a farm or a mob trap keeps it dark without hiding it."]),
    Q("bd_create_glass", 0, 0, [anyof(["create:framed_glass", "create:tiled_glass"], 8), anyof(variants("create:{}_window"), 4)],
      "Create Glass", deps=["bd_glass"], xp=20, optional=True, tokens=1, subtitle="Framed glass and wooden windows", desc=[
        "&eWhat:&r Create's framed and tiled glass connect into large clean panes, and its windows come in every wood.",
        "&eHow:&r eight framed or tiled glass and four windows of any wood (check JEI for the recipes).",
        "&eTip:&r framed glass over a row of machines lets you watch them work."]),

    # ===== Light ========================================================================================
    Q("bd_lanterns", 0, 0, [item("minecraft:lantern", 4)], "Lanterns", deps=["bd_start", "gs_iron"], xp=15,
      section="Light", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Light that hangs", desc=[
        "&eWhat:&r lanterns sit on floors or hang from ceilings and chains, and give a little more light than a torch.",
        "&eHow:&r a torch surrounded by iron nuggets (check JEI).",
        "&eTip:&r light keeps mobs from spawning: every dark corner of your base is a spawn point."]),
    Q("bd_lights", 0, 0, [item("minecraft:glowstone_dust", 16), item("minecraft:glowstone", 4), item("minecraft:redstone_lamp", 4), item("minecraft:soul_lantern", 2)],
      "Lighting Without Torches", deps=["bd_lanterns", "t2_nether"], xp=20, optional=True, tokens=1, subtitle="Glowstone, lamps and soul lanterns", desc=[
        "&eWhat:&r glowstone gives the brightest block light; redstone lamps switch on and off; soul lanterns burn blue and dim.",
        "&eChemistry:&r a flame glows because hot soot glows (incandescence). LEDs and glow-sticks give cold light (luminescence): electrons dropping between energy levels.",
        "&eHow:&r glowstone from the Nether ceiling (4 dust per block); lamp: glowstone in redstone; soul lantern: a soul torch in iron nuggets."]),
    Q("bd_froglights", 0, 0, [item("minecraft:ochre_froglight"), item("minecraft:verdant_froglight"), item("minecraft:pearlescent_froglight")], "Froglights",
      deps=["bd_lights", "fd_breed"], xp=60, optional=True, tokens=2, subtitle="Three frogs, three colours", desc=[
        "&eWhat:&r a frog that eats a small magma cube leaves a froglight. Its colour depends on the frog: temperate, warm or cold.",
        "&eHow:&r raise tadpoles from a swamp in a temperate, a warm and a cold biome, then bring the three frogs to the Nether's magma cubes.",
        "&eTip:&r a lead is the easiest way to walk frogs through a portal."]),
    Q("bd_mcw_lights", 0, 0, [anyof(MCW_LIGHTS, 4)], "Lamps and Lanterns", deps=["bd_lanterns", "gs_torch"], xp=15,
      optional=True, tokens=1, subtitle="Street lamps and chandeliers", desc=[
        "&eWhat:&r Macaw's Lights adds street lamps, lanterns, garden lights and chandeliers.",
        "&eHow:&r any four of them (check JEI).",
        "&eTip:&r street lamps along your paths keep mobs from spawning on the way home."]),
    Q("bd_lava_lamp", 0, 0, [item("mcwlights:lava_lamp")], "Lava Lamp", deps=["bd_mcw_lights", "gs_bucket"], xp=20,
      optional=True, tokens=1, subtitle="Groovy chemistry", desc=[
        "&eWhat:&r a lava lamp for your desk. This one really has lava in it.",
        "&eChemistry:&r a real lava lamp holds wax in water. Heated wax expands, its density drops below the water's and it rises; at the top it cools and sinks.",
        "&eHow:&r iron nuggets, a lava bucket and an iron ingot (check JEI)."]),
    Q("bd_deco_lamps", 0, 0, [anyof(DECO_LAMPS, 4)], "Create Deco Lamps", deps=["bd_lanterns", "cr_deco"], xp=20,
      optional=True, tokens=1, subtitle="Industrial lights", desc=[
        "&eWhat:&r Create Deco lamps in four colours and five metals light up a factory floor properly.",
        "&eHow:&r a nugget, a torch and a plate of the metal (check JEI). Any four lamps.",
        "&eTip:&r lamps can be switched off with redstone: red ones make good warning lights by a reactor."]),
    Q("bd_sea_lantern", 0, 0, [item("minecraft:sea_lantern", 4), item("minecraft:end_rod", 4)], "Sea Lanterns and End Rods", deps=["bd_lanterns"], xp=25,
      optional=True, tokens=1, subtitle="Cool white light", desc=[
        "&eWhat:&r sea lanterns are bright, cold-looking light blocks; end rods are thin white light sticks.",
        "&eHow:&r a sea lantern is prismarine shards and crystals from guardians; an end rod is a blaze rod on popped chorus fruit (check JEI).",
        "&eTip:&r sea lanterns under a glass floor light a room with no visible source."]),
    Q("bd_candles", 0, 0, [anyof(["minecraft:candle"] + [f"minecraft:{c}_candle" for c in COLOURS], 8), item("supplementaries:candle_holder")],
      "Candles", deps=["bd_lanterns"], xp=15, optional=True, tokens=1, subtitle="Wax, wick and a holder", desc=[
        "&eWhat:&r candles stack up to four per block and come in every colour; Supplementaries adds holders for walls.",
        "&eChemistry:&r a candle burns its own vapour: heat melts the wax, the wick draws it up, and the hot gas burns into CO₂ and water.",
        "&eHow:&r honeycomb on string makes a candle; dye it any colour. Any 8 candles and a candle holder (check JEI)."]),

    # ===== Colour =======================================================================================
    Q("bd_dyes", 0, 0, [anyof(DYES, 16)], "Dyes", deps=["bd_start"], xp=15,
      section="Colour", size=1.5, shape="hexagon", optional=True, tokens=1, icon="minecraft:red_dye", subtitle="Sixteen colours from flowers and more", desc=[
        "&eWhat:&r dyes colour wool, glass, concrete, terracotta, beds, candles and banners.",
        "&eChemistry:&r flower colours come from pigments like anthocyanins, which shift from red to blue with acidity: a natural pH indicator.",
        "&eHow:&r any 16 dyes. Most come from flowers; check JEI for the odd ones (cocoa, ink, lapis, bone meal)."]),
    Q("bd_wool", 0, 0, [anytag("minecraft:wool", 16)], "Wool", deps=["bd_dyes"], xp=15,
      optional=True, tokens=1, icon="minecraft:white_wool", subtitle="Soft blocks in every colour", desc=[
        "&eWhat:&r wool blocks for carpets, beds, banners and colourful walls.",
        "&eChemistry:&r wool is keratin, the same protein as hair and feathers; its sulfur bridges are why it smells when singed.",
        "&eHow:&r shear sheep, or craft four string into a block. Any 16 wool of any colour."]),
    Q("bd_concrete", 0, 0, [item("minecraft:terracotta", 16), anyof([f"minecraft:{c}_concrete_powder" for c in COLOURS], 16)],
      "Terracotta and Concrete", deps=["bd_dyes"], xp=20, optional=True, tokens=1, subtitle="Colour by the stack", desc=[
        "&eWhat:&r terracotta is fired clay; concrete powder is sand, gravel and dye that sets into concrete when it touches water.",
        "&eChemistry:&r real concrete doesn't dry, it reacts: calcium silicates in cement take up water and grow interlocking crystals. It even sets underwater.",
        "&eHow:&r smelt clay blocks into terracotta; 4 sand, 4 gravel and a dye make 8 concrete powder."]),
    Q("bd_glazed", 0, 0, [anyof([f"minecraft:{c}_glazed_terracotta" for c in COLOURS], 8)], "Glazed Terracotta", deps=["bd_concrete"], xp=20,
      optional=True, tokens=1, subtitle="Tiles with a pattern", desc=[
        "&eWhat:&r smelting dyed terracotta gives glazed tiles whose pattern changes with the way you face when placing them.",
        "&eChemistry:&r a real glaze is a thin glassy coat of silica and metal oxides fused onto fired clay, which is why tiles are waterproof.",
        "&eHow:&r dye terracotta, then smelt it. Any 8 glazed terracotta."]),
    Q("bd_painted", 0, 0, [anyof(variants("regions_unexplored:{}_painted_planks", COLOURS), 16)], "Painted Planks", deps=["bd_dyes"], xp=15,
      optional=True, tokens=1, subtitle="Wood in bright colours", desc=[
        "&eWhat:&r Regions Unexplored's painted planks come in all sixteen colours, for beach huts and toy-box rooms.",
        "&eHow:&r planks with a dye (check JEI). Any 16.",
        "&eTip:&r painted planks with white trim make a cheerful kitchen."]),
    Q("bd_banners", 0, 0, [item("minecraft:loom"), anyof([f"minecraft:{c}_banner" for c in COLOURS], 2)], "Banners", deps=["bd_wool"], xp=20,
      optional=True, tokens=1, icon="minecraft:red_banner", subtitle="A flag for your house", desc=[
        "&eWhat:&r banners take patterns from a loom; put one on a shield to carry your colours.",
        "&eHow:&r six wool and a stick make a banner; the loom adds dye patterns (check JEI).",
        "&eTip:&r design your team's banner once and copy it in a crafting grid."]),

    # ===== Furniture ====================================================================================
    Q("bd_chairs", 0, 0, [anyof(variants("handcrafted:{}_chair"), 2), anyof(variants("handcrafted:{}_table"), 1)], "Somewhere to Sit", deps=["bd_start"], xp=15,
      section="Furniture", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Handcrafted chairs and a table", desc=[
        "&eWhat:&r Handcrafted adds furniture you can sit on: chairs, couches, benches, tables and desks.",
        "&eHow:&r any wood works (check JEI). Right-click a chair to sit.",
        "&eTip:&r the Handcrafted Hammer changes the shape of trims and some other pieces."]),
    Q("bd_couch", 0, 0, [anyof(variants("handcrafted:{}_couch"), 2), anyof(variants("handcrafted:{}_desk"), 1)], "A Proper Study", deps=["bd_chairs"], xp=20,
      optional=True, tokens=1, subtitle="Couches and a desk", desc=[
        "&eWhat:&r couches connect into long sofas; desks connect into long workbenches.",
        "&eHow:&r any wood (check JEI). Cushions and sheets add colour.",
        "&eTip:&r a desk by your Alchemistry machines makes a fine place to read the quest book."]),
    Q("bd_mcw_furniture", 0, 0, [anyof(variants("mcwfurnitures:{}_wardrobe") + variants("mcwfurnitures:{}_drawer")
                                       + variants("mcwfurnitures:{}_kitchen_cabinet"), 2)], "Macaw's Furniture", deps=["bd_chairs"], xp=20,
      optional=True, tokens=1, subtitle="Wardrobes, drawers and cabinets", desc=[
        "&eWhat:&r Macaw's Furniture adds kitchens, wardrobes, drawers, bookshelves and more. Many of them store items.",
        "&eHow:&r any two wardrobes, drawers or kitchen cabinets (check JEI for the full set).",
        "&eTip:&r drawers and cabinets open like chests, so a kitchen can double as food storage."]),
    Q("bd_kitchen", 0, 0, [anyof(variants("handcrafted:{}_counter"), 2), anyof(variants("handcrafted:{}_cupboard"), 1), item("handcrafted:kitchen_hood")],
      "A Real Kitchen", deps=["bd_chairs"], xp=20, optional=True, tokens=1, subtitle="Counters, a cupboard and a hood", desc=[
        "&eWhat:&r Handcrafted counters, cupboards and a kitchen hood to go over your Farmer's Delight stove.",
        "&eChemistry:&r a kitchen hood is a small fume hood: it pulls away smoke and the acrolein that hot fat gives off.",
        "&eHow:&r any wood (check JEI). Two counters, a cupboard and a hood."]),
    Q("bd_bedroom", 0, 0, [anyof(variants("handcrafted:{}_fancy_bed"), 1), anyof(variants("handcrafted:{}_nightstand"), 1)],
      "A Bedroom", deps=["bd_chairs"], xp=20, optional=True, tokens=1, subtitle="A fancy bed and a nightstand", desc=[
        "&eWhat:&r a four-poster fancy bed and a nightstand; sheets and cushions change their colours.",
        "&eHow:&r any wood (check JEI). The fancy bed works like a normal bed.",
        "&eTip:&r a sleeping bag for trips and a real bed at home: your spawn stays here."]),
    Q("bd_tableware", 0, 0, [anyof(["handcrafted:wood_plate", "handcrafted:white_plate", "handcrafted:blue_plate", "handcrafted:yellow_plate",
                                    "handcrafted:terracotta_plate", "handcrafted:wood_cup", "handcrafted:white_cup", "handcrafted:blue_cup",
                                    "handcrafted:wood_bowl", "handcrafted:white_bowl", "handcrafted:terracotta_bowl"], 4)],
      "Plates and Cups", deps=["bd_kitchen"], xp=15, optional=True, tokens=1, subtitle="Set the table", desc=[
        "&eWhat:&r plates, cups and bowls to put on tables. A plate can hold a piece of food for display.",
        "&eChemistry:&r white porcelain is kaolin clay fired so hot (about 1,300 °C) that part of it turns to glass, sealing the pores.",
        "&eHow:&r any four (check JEI for the wood, terracotta and coloured sets)."]),

    # ===== House Parts ==================================================================================
    Q("bd_mcw_doors", 0, 0, [anyof(variants("mcwdoors:{}_barn_door") + variants("mcwdoors:{}_modern_door")
                                   + variants("mcwdoors:{}_glass_door") + variants("mcwdoors:{}_cottage_door"), 2)], "Doors", deps=["bd_start"], xp=15,
      section="House Parts", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Macaw's doors in every wood", desc=[
        "&eWhat:&r Macaw's Doors adds barn, cottage, glass, modern and many more doors in every wood.",
        "&eHow:&r any two barn, modern, glass or cottage doors (check JEI for recipes).",
        "&eTip:&r glass doors let you see into a machine room without opening it."]),
    Q("bd_mcw_trapdoors", 0, 0, [anyof(variants("mcwtrpdoors:{}_barn_trapdoor") + variants("mcwtrpdoors:{}_glass_trapdoor")
                                       + variants("mcwtrpdoors:{}_classic_trapdoor"), 4)], "Trapdoors", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Shutters and cabinet fronts", desc=[
        "&eWhat:&r decorative trapdoors that match the doors: barn, glass, classic and more.",
        "&eHow:&r any four barn, glass or classic trapdoors (check JEI).",
        "&eTip:&r trapdoors on walls make great shutters and cabinet fronts."]),
    Q("bd_mcw_roofs", 0, 0, [anyof(variants("mcwroofs:{}_roof") + variants("mcwroofs:{}_steep_roof")
                                   + variants("mcwroofs:{}_roof", ["stone", "cobblestone", "blackstone", "deepslate", "andesite"]), 16)], "Roofs", deps=["bd_mcw_doors"], xp=20,
      optional=True, tokens=1, subtitle="A roof that isn't flat", desc=[
        "&eWhat:&r Macaw's Roofs adds sloped, steep, attic and top roof pieces that join into proper roofs.",
        "&eHow:&r any sixteen roof pieces (check JEI). Wooden roofs come from logs and sticks.",
        "&eTip:&r place the lower and upper pieces together to make a gentler slope."]),
    Q("bd_mcw_fences", 0, 0, [anyof(variants("mcwfences:{}_picket_fence") + variants("mcwfences:{}_stockade_fence")
                                    + variants("mcwfences:{}_wired_fence") + variants("mcwfences:{}_hedge"), 8)], "Fences and Hedges", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Picket, stockade, wired, hedge", desc=[
        "&eWhat:&r Macaw's Fences adds picket and stockade fences, wired fences, hedges and gates.",
        "&eHow:&r any eight picket, stockade or wired fences or hedges (check JEI).",
        "&eTip:&r hedges are made from leaves, so a garden can stay looking natural."]),
    Q("bd_mcw_stairs", 0, 0, [anyof(MCW_STAIRS, 8)], "Better Stairs", deps=["bd_mcw_doors"], xp=15,
      optional=True, tokens=1, subtitle="Loft, skyline and terrace stairs", desc=[
        "&eWhat:&r Macaw's Stairs adds loft, skyline, terrace, bulk and compact stairs that turn corners and climb steeply.",
        "&eHow:&r any eight, in wood or stone (check JEI).",
        "&eTip:&r compact stairs fit a tight tower where vanilla stairs won't."]),
    Q("bd_mcw_balcony", 0, 0, [anyof(MCW_BALCONY, 6)], "Balconies and Railings", deps=["bd_mcw_stairs"], xp=15,
      optional=True, tokens=1, subtitle="A place to look out from", desc=[
        "&eWhat:&r balconies, railings and platforms from Macaw's Stairs, matching the stairs' woods and stones.",
        "&eHow:&r any six (check JEI).",
        "&eTip:&r a railing around the top of a tank or a vat keeps you from falling in."]),

    # ===== Outdoors =====================================================================================
    Q("bd_mcw_paths", 0, 0, [anyof(MCW_PATHS, 16)], "Paths", deps=["bd_start", "gs_stone"], xp=15,
      section="Outdoors", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Paving between your buildings", desc=[
        "&eWhat:&r Macaw's Paths adds paving patterns (basket weave, honeycomb, flagstone) in stone, brick and sandstone.",
        "&eHow:&r any sixteen paving blocks (check JEI).",
        "&eTip:&r a path from your base to your waystone saves getting lost at night."]),
    Q("bd_mcw_bridges", 0, 0, [anyof(MCW_BRIDGES, 8)], "Bridges", deps=["bd_mcw_paths"], xp=15,
      optional=True, tokens=1, subtitle="Rope, stone and iron bridges", desc=[
        "&eWhat:&r Macaw's Bridges adds pieces that connect into rope, stone, brick and iron bridges, with piers and stairs.",
        "&eHow:&r any eight bridge pieces (check JEI).",
        "&eTip:&r an iron bridge over a lava lake makes the Nether commute much safer."]),
    Q("bd_garden", 0, 0, [item("minecraft:flower_pot", 4), anyof(["supplementaries:planter", "supplementaries:flower_box"], 2)], "A Garden", deps=["bd_mcw_paths"], xp=15,
      optional=True, tokens=1, subtitle="Pots, planters and flower boxes", desc=[
        "&eWhat:&r flower pots, Supplementaries planters (crops grow in them) and flower boxes for under windows.",
        "&eChemistry:&r terracotta pots breathe: their open pores let water and air through, which keeps roots from rotting.",
        "&eHow:&r a flower pot is three bricks; check JEI for the planter and flower box."]),
    Q("bd_zen", 0, 0, [item("supplementaries:raked_gravel", 16)], "A Raked Garden", deps=["bd_garden"], xp=15,
      optional=True, tokens=1, subtitle="Calm lines in the gravel", desc=[
        "&eWhat:&r Supplementaries' raked gravel: gravel with lines combed into it, for a quiet stone garden.",
        "&eHow:&r use a hoe on gravel. The lines follow the direction you face.",
        "&eTip:&r a few stones, a pond and a cherry tree finish the look."]),

    # ===== Supplementaries ==============================================================================
    Q("bd_jar", 0, 0, [item("supplementaries:jar", 2)], "Jars", deps=["bd_start"], xp=15,
      section="Supplementaries", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Display jars for anything", desc=[
        "&eWhat:&r Supplementaries jars hold items, liquids or small mobs, and show what's inside.",
        "&eHow:&r glass and a wooden slab (check JEI). Right-click with an item or a bucket to fill.",
        "&eTip:&r a shelf of jars, one per element, makes a lovely periodic table display."]),
    Q("bd_rope", 0, 0, [item("supplementaries:rope", 16), item("supplementaries:sack")], "Rope and Sacks", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="Flax, rope and a sack", desc=[
        "&eWhat:&r rope you can climb and pull things up with, and sacks that store items and can be carried.",
        "&eHow:&r grow flax (seeds from wild flax), then craft rope and sacks from it (check JEI).",
        "&eTip:&r rope down a mineshaft is a quick way up and down (check JEI for the pulley block)."]),
    Q("bd_soap", 0, 0, [item("supplementaries:soap", 2)], "Soap", deps=["bd_jar"], xp=25,
      optional=True, tokens=1, subtitle="The oldest chemistry in the house", desc=[
        "&eWhat:&r soap washes dye off coloured blocks and items, and it powers the Bubble Blower.",
        "&eChemistry:&r saponification: wood ash is rich in potash (K₂CO₃), which makes lye in water; lye splits fat into glycerol and fatty-acid salts, which is soap.",
        "&eHow:&r a water bucket, four ash and a porkchop (check JEI). Ash is left when fire burns blocks away."]),
    Q("bd_bubbles", 0, 0, [item("supplementaries:bubble_blower")], "Bubbles!", deps=["bd_soap"], xp=20,
      secret=True, loot="secret", subtitle="Secret: a demigod at play", desc=[
        "&6You remember making nebulae. These are smaller, but they're very pretty.&r",
        "&eWhat:&r the Bubble Blower uses soap to blow bubbles; it can also make Bubble Blocks (check its tooltip).",
        "&eChemistry:&r a soap film is a thin water layer between two layers of soap molecules. Its colours come from light reflecting off both surfaces and interfering."]),
    Q("bd_spikes", 0, 0, [item("supplementaries:bamboo_spikes", 4)], "Bamboo Spikes", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="A garden of sharp sticks", desc=[
        "&eWhat:&r bamboo spikes hurt mobs that walk on them; coated with a lingering potion they poison them too.",
        "&eHow:&r 4 bamboo over 3 wooden slabs (check JEI). Use a lingering potion on placed spikes to coat them.",
        "&eTip:&r a ring of spikes around a farm keeps zombies off the crops."]),
    Q("bd_globe", 0, 0, [item("supplementaries:globe")], "A Globe", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="Spin the world on your desk", desc=[
        "&eWhat:&r a desk globe that spins when you click it, showing a map of a made-up world.",
        "&eHow:&r check JEI for the recipe.",
        "&eTip:&r it belongs on the desk in your study, next to the quest book."]),
    Q("bd_notice", 0, 0, [item("supplementaries:notice_board"), item("supplementaries:blackboard")], "Boards to Write On", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="A notice board and a blackboard", desc=[
        "&eWhat:&r the notice board shows a written book's page on a wall; the blackboard is a slate you can draw on pixel by pixel.",
        "&eHow:&r check JEI for both; the blackboard's tooltip shows how to draw.",
        "&eTip:&r write your reactor's recipe on a blackboard next to it, the way chemists do."]),
    Q("bd_clock", 0, 0, [item("supplementaries:clock_block"), item("supplementaries:hourglass")], "Clocks and Hourglasses", deps=["bd_jar"], xp=15,
      optional=True, tokens=1, subtitle="Know the time without a clock in hand", desc=[
        "&eWhat:&r the clock block shows the time on a wall; the hourglass is a timer you fill with sand or other powders.",
        "&eChemistry:&r a real hourglass works because dry sand flows at a steady rate no matter how full the glass is, unlike water.",
        "&eHow:&r check JEI for both. Days here are twice as long, so the clock moves slowly in daylight."]),
    Q("bd_flags", 0, 0, [anyof([f"supplementaries:flag_{c}" for c in COLOURS], 1), anyof([f"supplementaries:bunting_{c}" for c in COLOURS], 4)],
      "Flags and Bunting", deps=["bd_jar"], xp=15, optional=True, tokens=1, icon="supplementaries:flag_red", subtitle="Wave your colours", desc=[
        "&eWhat:&r flags that flutter in the wind and strings of bunting for a festival look.",
        "&eHow:&r any flag and four bunting (check JEI). Flags take banner patterns too.",
        "&eTip:&r a flag on top of each waystone makes it easy to spot from far away."]),

    # ===== Metal and Industry ===========================================================================
    Q("bd_metal_blocks", 0, 0, [item("minecraft:copper_block", 4), item("minecraft:lapis_block", 2), item("minecraft:quartz_block", 8)], "Mineral Blocks",
      deps=["bd_start", "t2_quartz"], xp=20, section="Metal and Industry", size=1.5, shape="hexagon",
      optional=True, tokens=1, subtitle="Copper, lapis and quartz to build with", desc=[
        "&eWhat:&r copper blocks weather from orange to green; lapis and quartz blocks are the classic blue and white trims.",
        "&eChemistry:&r copper turns green as it reacts with air, water and CO₂ into basic copper carbonate. Honeycomb wax stops it; an axe scrapes it back.",
        "&eHow:&r 9 copper ingots or 9 lapis per block; 4 Nether quartz per quartz block."]),
    Q("bd_copper_age", 0, 0, [item("minecraft:copper_grate", 4), item("minecraft:copper_bulb", 2), item("minecraft:chiseled_copper", 4)], "Copper Craft",
      deps=["bd_metal_blocks"], xp=20, optional=True, tokens=1, subtitle="Grates, bulbs and chiseled copper", desc=[
        "&eWhat:&r copper grates you can see through, copper bulbs that toggle with each redstone pulse, and chiseled copper.",
        "&eChemistry:&r in game a bulb dims as it weathers. Real patina (basic copper carbonate) is a far poorer conductor than the bright metal under it, which is why electrical contacts are kept clean.",
        "&eHow:&r cut copper blocks in a stonecutter; a bulb is copper blocks, a blaze rod and redstone (check JEI)."]),
    Q("bd_iron_bars", 0, 0, [item("minecraft:iron_bars", 16), item("supplementaries:iron_gate", 2)], "Bars and Gates", deps=["bd_metal_blocks"], xp=15,
      optional=True, tokens=1, subtitle="Railings that let air through", desc=[
        "&eWhat:&r iron bars make cages, windows and railings; Supplementaries iron gates open like fence gates.",
        "&eChemistry:&r iron rusts into hydrated iron(III) oxide, Fe₂O₃·nH₂O; in game it never does, which is the only unrealistic thing about it.",
        "&eHow:&r six iron ingots make 16 bars (check JEI for the gate)."]),
    Q("bd_deco_hull", 0, 0, [anyof(variants("createdeco:{}_hull", DECO_METALS), 4), anyof(variants("createdeco:{}_support", DECO_METALS), 4)],
      "Hulls and Supports", deps=["bd_metal_blocks", "cr_deco"], xp=20, optional=True, tokens=1, subtitle="Riveted walls and girders", desc=[
        "&eWhat:&r hulls are riveted metal walls; supports are girders for roofs and catwalks.",
        "&eHow:&r any four hulls and four supports (check JEI).",
        "&eTip:&r copper hulls weather like copper blocks do. Wax them with honeycomb to keep the shine."]),
    Q("bd_catwalks", 0, 0, [anyof(variants("createdeco:{}_catwalk", DECO_METALS), 8), anyof(variants("createdeco:{}_catwalk_railing", DECO_METALS), 4)],
      "Catwalks", deps=["bd_deco_hull"], xp=20, optional=True, tokens=1, subtitle="Walk above your machines", desc=[
        "&eWhat:&r Create Deco catwalks and railings: see-through metal floors for walking over a factory.",
        "&eHow:&r any eight catwalks and four railings (check JEI).",
        "&eTip:&r catwalks over your pipes and belts keep everything reachable for repairs."]),
    Q("bd_diamond_block", 0, 0, [item("minecraft:diamond_block")], "Showing Off", deps=["bd_metal_blocks", "hv_iron"], xp=50,
      secret=True, loot="secret", subtitle="Secret: nine diamonds you'll never use", desc=[
        "&6You remember a throne cut from a single gem. A block of diamond on the mantelpiece is a start.&r",
        "&eWhat:&r a block of diamond, placed only to be looked at.",
        "&eChemistry:&r a block's worth of real diamond would be about 3.5 tonnes of pure carbon. Burn it and you'd get about 13 tonnes of CO₂."]),

    # ===== The Laboratory ===============================================================================
    Q("bd_lab", 0, 0, [item("laboratoryblocks:laboratory_block", 16)], "Laboratory Blocks", deps=["bd_start", "t2_quartz"], xp=25,
      section="The Laboratory", size=1.5, shape="hexagon", optional=True, tokens=1, subtitle="Clean white walls for a chemist", desc=[
        "&6You remember a laboratory of white stone and light. You can build it again.&r",
        "&eWhat:&r Artemis' Laboratory Blocks adds clean lab walls, tiles, glass, screens, vents and fans.",
        "&eChemistry:&r the recipe uses Nether quartz, which is silicon dioxide (SiO₂), the same compound as sand and glass.",
        "&eHow:&r eight stone around one Nether quartz makes eight laboratory blocks (check JEI)."]),
    Q("bd_lab_glow", 0, 0, [item("laboratoryblocks:glowstone_particles", 8), item("laboratoryblocks:glowing_laboratory_block", 8)], "Glowing Panels", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Walls that light the room", desc=[
        "&eWhat:&r glowing laboratory blocks give off light, so a lab can be bright with no torches.",
        "&eHow:&r one glowstone dust makes eight glowstone particles; a particle plus a laboratory block makes a glowing block (check JEI).",
        "&eChemistry:&r real glow-in-the-dark materials store energy from light and release it slowly (phosphorescence)."]),
    Q("bd_lab_screens", 0, 0, [anyof(LAB_SCREENS, 4)], "Lab Screens", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Monitors on every wall", desc=[
        "&eWhat:&r decorative screens: clear, text, wave and quantum patterns, plain or glowing.",
        "&eHow:&r clear screens from laboratory blocks, laboratory glass and iron screws; add a dye for the patterns (check JEI).",
        "&eTip:&r put a wave screen beside your reactor and a ComputerCraft monitor next to it for real numbers."]),
    Q("bd_lab_fan", 0, 0, [item("laboratoryblocks:laboratory_fan"), item("laboratoryblocks:laboratory_vent", 2)], "Fans and Vents", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="Fume extraction", desc=[
        "&eWhat:&r animated lab fans and vents. The redstone-controlled fan only spins when powered.",
        "&eChemistry:&r real labs handle HCl, NH₃ and Cl₂ under a fume hood, which pulls vapours away from your face.",
        "&eHow:&r laboratory blocks with iron nuggets and iron screws (check JEI)."]),
    Q("bd_lab_doors", 0, 0, [anyof(LAB_DOORS, 2), item("laboratoryblocks:laboratory_glass", 8)], "Lab Doors and Glass", deps=["bd_lab"], xp=20,
      optional=True, tokens=1, subtitle="See in, keep fumes out", desc=[
        "&eWhat:&r lab doors (solid, glass or mesh) and laboratory glass for viewing windows.",
        "&eHow:&r doors from laboratory blocks; laboratory glass is eight glass around a laboratory block (check JEI).",
        "&eTip:&r a glass wall around your Alchemistry room lets visitors admire it without touching anything."]),
    Q("bd_lab_hazard", 0, 0, [anyof(["createdeco:decal_radioactive", "createdeco:decal_fire_diamond", "createdeco:decal_fire", "createdeco:decal_warning",
                                     "createdeco:decal_electrical", "createdeco:decal_skull"], 3)], "Hazard Signs", deps=["bd_lab", "cr_deco"], xp=20,
      optional=True, tokens=1, subtitle="Label what can hurt you", desc=[
        "&eWhat:&r Create Deco decals: radiation, fire, electrical and warning signs to stick on walls and doors.",
        "&eChemistry:&r real labs label chemicals with hazard pictograms and the four-coloured fire diamond: blue for health, red for fire, yellow for reactivity, white for special hazards.",
        "&eHow:&r any three hazard decals (check JEI)."]),
    Q("bd_lab_done", 0, 0, [tick()], "A Proper Laboratory", deps=["bd_lab_glow", "bd_lab_screens", "bd_lab_fan", "bd_lab_doors"], xp=100,
      optional=True, tokens=2, size=1.5, shape="hexagon", subtitle="Build a lab worthy of you", desc=[
        "&6White walls, humming fans, glass and light. You remember this place. It was always where you were happiest.&r",
        "&eWhat:&r a challenge: build a real laboratory around your chemistry machines with these blocks.",
        "&eHow:&r include glowing panels, screens, a fume fan and a glass wall. Click the checkmark when you're proud of it."]),
], links=[("gs_table", 0, 0)])
