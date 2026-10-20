"""Quest chapter: welcome. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

A small, centred showcase page (reshaped 2026-10-19): the welcome quest in the middle, four signposts around it
(the Demigod's Path, the Market, Tips and Tricks, Building Tips) and Getting Started below as the way out.
Two optional fun facts sit above the centre. Manual layout: the x/y below are used as written.
Keys are unchanged; wel_story's lore now lives in wel_hello, and wel_opt_mass is the Building Tips signpost.
"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401


CHAPTER = Chapter("welcome", "Welcome", "minecraft:nether_star",
        ["Read this first: who you are, and where to go next."], MAIN, [
    # --- the centrepiece -------------------------------------------------------------------------
    Q("wel_hello", 0, 0, [tick()], "Welcome, Demigod", subtitle="Your first page of the Demigod's Codex",
      size=2.0, shape="gear", tokens=3, items=[("comforts:sleeping_bag_white", 1)], icon="minecraft:nether_star", desc=[
        "&6You remember light pouring from your hands. Now there is only dirt under your nails.&r",
        "&eWhat:&r Welcome to Warbucks Chemistry. You're a demigod who lost your power, and you win it back by mastering chemistry: taking matter apart into elements and building it up again.",
        "&eHow:&r the four signposts around this quest point to the pages that matter most. Read them, then take the road below to Getting Started.",
        "&eTip:&r the sleeping bag skips the night without moving your spawn point."]),

    # --- four signposts around it ----------------------------------------------------------------
    Q("wel_progress", -3.5, -1.5, [tick()], "The Demigod's Path", subtitle="The main story, one tier at a time",
      deps=["wel_hello"], size=1.5, shape="hexagon", icon="modern_industrialization:bronze_ingot", desc=[
        "&eWhat:&r the Demigod's Path is the spine of the book: eight tiers, each opened by a chemistry milestone. Fire and bronze, then steel, hydrogen, electricity, acids, plastics, the atom and antimatter.",
        "&eHow:&r every other page hangs off it. Modern Industrialization's voltages (LV, MV, HV, EV) set the pace, and other mods open alongside.",
        "&eTip:&r if a recipe looks different from what you remember, it was changed on purpose. JEI always shows the real one."]),
    Q("wel_tokens", 3.5, -1.5, [tick()], "The Demigod's Market", subtitle="What your Demigod Tokens buy",
      deps=["wel_hello"], size=1.5, shape="hexagon", tokens=5, icon="kubejs:demigod_token", desc=[
        "&eWhat:&r most quests pay Demigod Tokens. The Market turns them into supplies and comforts, never into shortcuts past a tier.",
        "&eHow:&r open the Demigod's Market pages, or search &eDemigod Token&r in JEI and press &eU&r: every trade is a crafting recipe.",
        "&eTip:&r the Market sells more of what you have already made yourself, so finishing quests opens new stalls."]),
    Q("wel_keys", -3.5, 1.5, [tick()], "Tips and Tricks", subtitle="Keys, shortcuts and how this pack differs",
      deps=["wel_hello"], size=1.5, shape="hexagon", icon="minecraft:spyglass", desc=[
        "&eWhat:&r the Tips and Tricks page collects short lessons: JEI lookups, Jade, claiming land, Ultimine, waystones, perks and the pack's own changes.",
        "&eHow:&r &eR&r / &eU&r over an item for recipes and uses, &eM&r for the claim map, hold &e`&r to vein mine. The page has the rest.",
        "&eTip:&r give the game about 8 to 10 GB of memory in your launcher's instance settings."]),
    Q("wel_opt_mass", 3.5, 1.5, [tick()], "Building Tips", subtitle="Make your base look like a god lives there",
      deps=["wel_hello"], size=1.5, shape="hexagon", icon="framedblocks:framed_hammer", desc=[
        "&eWhat:&r the Building Tips pages are a catalogue of the pack's building tools and decoration: gadgets, chisels, framed blocks, stone, wood, glass, light, furniture and a proper laboratory.",
        "&eHow:&r everything there is optional. Dip in whenever your base needs a new look.",
        "&eTip:&r a construction stick and a stonecutter save more time than anything else on that page."]),

    # --- the way out -------------------------------------------------------------------------------
    Q("wel_ready", 0, 3.25, [tick()], "Getting Started", subtitle="Your first day begins here", deps=["wel_hello"],
      size=1.5, shape="hexagon", icon="minecraft:oak_sapling", desc=[
        "&6The world is waiting to be taken apart and put back together.&r",
        "&eHow:&r open &eGetting Started&r and take your first step: wood, stone, food and a safe first night.",
        "&eTip:&r you can come back to this page any time from the top of the chapter list."]),

    # --- optional fun facts above the centre (retired from the old main line) ------------------------
    Q("wel_story", -1.75, -3, [tick()], "Who You Were", subtitle="Optional: a god's memory, a chemist's method",
      deps=["wel_hello"], optional=True, tokens=1, desc=[
        "&6Some things you still know without being taught: water is two parts hydrogen to one of oxygen, and fire is a reaction, not a spirit.&r",
        "&eChemistry:&r about 90 elements occur in nature. Rearrange their atoms and you change what a thing is. That's the whole game.",
        "&eTip:&r every chapter of this book returns one more piece of what you once were."]),
    Q("wel_opt_table", 1.75, -3, [tick()], "The Periodic Table", subtitle="Optional: 118 known elements", deps=["wel_hello"],
      optional=True, tokens=1, icon="chemlib:hydrogen", desc=[
        "&eWhat:&r chemists know 118 elements. Each is defined by its number of protons, its &eatomic number&r.",
        "&eChemistry:&r Mendeleev ordered the table in 1869 by repeating properties and left gaps for elements nobody had found. Gallium and germanium later filled them almost exactly as he predicted.",
        "&eTip:&r the Periodic Table page tracks every element you collect, and whole groups grant permanent perks."]),
], layout="manual")
