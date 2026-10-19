"""Quest chapter: welcome. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The "How to Read This Book" quests (wel_legend, wel_lg_*) explain the book's visual language. Shapes and sizes
everywhere else are set by role in tools/quest_style.py; the legend's shape examples are marked keep_style so
they show their own shape instead of being restyled.
"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401


def _example(q):
    """A legend example: tools/quest_style.py leaves its shape and size as written."""
    q.keep_style = True
    return q


# --- How to Read This Book (all optional; every quest is a checkmark) -------------------------------------------
LEGEND = [
    Q("wel_legend", 0, 0, [tick()], "How to Read This Book", subtitle="Shapes, lines and links, in one minute",
      deps=["wel_progress"], optional=True, tokens=1, desc=[
        "&eWhat:&r Every quest's shape tells you its job before you open it. The quests branching off this one each show one shape, with a line on what it means.",
        "&eHow:&r Click through them in any order. They're optional, so skip them if you'd rather learn by playing.",
        "&eTip:&r In short: gear = chapter finish, hexagon = section milestone, rounded square = main path, square = side step, octagon = pick one route, pentagon = tip or story, circle = optional, diamond = secret."]),
    _example(Q("wel_lg_capstone", 0, 0, [tick()], "Gear: The Chapter's Finish", subtitle="The biggest icon on the page",
      deps=["wel_legend"], optional=True, tokens=0, size=2.0, shape="gear", desc=[
        "&eWhat:&r A large gear marks the goal of a whole chapter. Reach it and that chapter's story is told.",
        "&eTip:&r Milestones pay double tokens, and in the main tiers they roll that tier's loot table too."])),
    _example(Q("wel_lg_section", 0, 0, [tick()], "Hexagon: A Section Milestone", subtitle="A smaller goal inside a chapter",
      deps=["wel_legend"], optional=True, tokens=0, size=1.5, shape="hexagon", desc=[
        "&eWhat:&r A large hexagon closes one part of a chapter: a new machine line, a new material, a new place.",
        "&eTip:&r If you only have time for one thing tonight, aim for the next hexagon."])),
    _example(Q("wel_lg_main", 0, 0, [tick()], "Rounded Square: The Main Path", subtitle="The road through the chapter",
      deps=["wel_legend"], optional=True, tokens=0, size=1.0, shape="rsquare", desc=[
        "&eWhat:&r Rounded squares are the chapter's longest line of required steps. They run along the middle row, left to right.",
        "&eHow:&r Lost? Find the rounded square nearest the left that isn't done yet, and do that one."])),
    _example(Q("wel_lg_side", 0, 0, [tick()], "Square: A Side Step", subtitle="Required, but off the middle row",
      deps=["wel_legend"], optional=True, tokens=0, size=1.0, shape="square", desc=[
        "&eWhat:&r Plain squares are required too. They sit on rows above or below the main path and feed back into it.",
        "&eTip:&r A square usually makes a part or material that a later rounded square or milestone asks for."])),
    _example(Q("wel_lg_choice", 0, 0, [tick()], "Octagon: Pick One Route", subtitle="Any one of its lines will do",
      deps=["wel_lg_main", "wel_lg_side"], any_dep=True, optional=True, tokens=0, size=1.0, shape="octagon", desc=[
        "&eWhat:&r An octagon opens as soon as ANY ONE of the quests leading into it is done. It marks a choice: for example, any one kind of generator.",
        "&eHow:&r This one opens after either the rounded square or the square example. Try it."])),
    _example(Q("wel_lg_tip", 0, 0, [tick()], "Pentagon: A Tip or a Memory", subtitle="Read it, then click the checkmark",
      deps=["wel_legend"], optional=True, tokens=0, size=0.9, shape="pentagon", desc=[
        "&eWhat:&r A pentagon has nothing to gather. It holds advice or a piece of the story, and its only task is a checkmark.",
        "&eTip:&r Pentagons on a required line still need their click before the line goes on."])),
    _example(Q("wel_lg_optional", 0, 0, [tick()], "Circle: Optional", subtitle="Bonus content that never blocks you",
      deps=["wel_legend"], optional=True, tokens=0, size=0.85, shape="circle", desc=[
        "&eWhat:&r Small circles are extras: collections, challenges, fun facts and other ways to do things. Nothing required ever waits on one.",
        "&eTip:&r They still pay tokens, so they're a good way to stock up for the Market."])),
    _example(Q("wel_lg_secret", 0, 0, [tick()], "Diamond: A Secret", subtitle="You won't see these until you find them",
      deps=["wel_legend"], optional=True, tokens=0, size=0.75, shape="diamond", desc=[
        "&eWhat:&r Real secret quests are invisible until you complete them by accident: a rare place, a strange creature, an odd discovery. When one pops up, it's a small diamond.",
        "&eTip:&r No hints here. Explore, and keep an eye on the toasts in the corner of your screen."])),
    Q("wel_lg_lines", 0, 0, [tick()], "Lines and Hidden Lines", subtitle="What the lines between quests mean",
      deps=["wel_legend"], optional=True, tokens=0, desc=[
        "&eWhat:&r A line joins a quest to the one it needs. Lines run left to right, so the quest on the left comes first.",
        "&eHow:&r Some busy pages hide part of their lines to stay readable. If a quest looks locked and you can't see why, open it: its window lists every quest it still needs.",
        "&eTip:&r A locked quest shows a padlock until everything it needs is done."]),
    Q("wel_lg_links", 0, 0, [tick()], "Quest Links", subtitle="A shortcut to a quest in another chapter",
      deps=["wel_legend"], optional=True, tokens=0, desc=[
        "&eWhat:&r Many chapters start with a quest that really lives somewhere else, usually on the main path. That is a &equest link&r: it shows where this page joins the rest of the book.",
        "&eHow:&r Click a link to open the original quest. A link isn't a copy: it's the same quest, so it shows as done in both places."]),
    Q("wel_lg_sections", 0, 0, [tick()], "Banners and Section Headers", subtitle="How a page is divided",
      deps=["wel_legend"], optional=True, tokens=0, desc=[
        "&eWhat:&r The banner at the top of a page names the chapter. Below it, each row of quests is one topic. A section header names the topic, and a hexagon marks its end.",
        "&eHow:&r Chapters are grouped in the tabs on the left. The Demigod's Path is the story; the other tabs hold mod pages you can visit whenever they open up."]),
]

CHAPTER = Chapter("welcome", "Welcome", "minecraft:nether_star",
        ["Read this first: who you are, how this world works, and how to use this book."], MAIN, [
    Q("wel_hello", 0, 0, [tick()], "Welcome, Demigod", subtitle="Your first page of the Demigod's Codex",
      size=2.0, shape="gear", tokens=3, items=[("comforts:sleeping_bag_white", 1)], desc=[
        "&6You remember light pouring from your hands. Now there is only dirt under your nails.&r",
        "&eWhat:&r Welcome to Warbucks Chemistry. You're a demigod who has lost your power, and you'll win it back by mastering chemistry: taking matter apart into its elements and building it back up.",
        "&eHow:&r Follow the lines from quest to quest. Each one tells you what to do and how to do it. Click the checkmark to collect your first reward.",
        "&eTip:&r The sleeping bag skips the night without moving your spawn point."]),
    Q("wel_story", 2, 0, [tick()], "Who You Were", subtitle="A god's memory, and a chemist's method", deps=["wel_hello"], desc=[
        "&6Some things you still know without being taught: that water is two parts hydrogen to one of oxygen, that fire is a reaction, not a spirit.&r",
        "&eWhat:&r Your power returns as you rebuild your understanding of matter. Every chapter of this book is one more piece of what you once were.",
        "&eChemistry:&r All matter is made of about 90 naturally occurring elements. Rearrange their atoms and you change what a thing is. That's the whole game.",
        "&eHow:&r Click the checkmark to continue."]),
    Q("wel_progress", 4, -1, [tick()], "How Progression Works", subtitle="Eight tiers, and how to read this book", deps=["wel_story"], desc=[
        "&eWhat:&r The pack has 8 tiers. Each one is unlocked by a chemistry milestone, not just more metal: fire and bronze → coke and steel → hydrogen and flight → electricity → acids → oil and plastics → silicon, PVC and the atom → antimatter.",
        "Modern Industrialization's voltage tiers (LV, MV, HV, EV) are the spine. Other mods (Mekanism, AE2, Powah and more) unlock alongside them.",
        "&eHow:&r Every quest reads the same way: &eWhat&r says what the thing is, &eChemistry&r gives the real science, &eHow&r gives the steps and &eTip&r saves you time. Gold lines are your memories returning.",
        "&eTip:&r Quests marked &eoptional&r sit off the main line and never block progress. If a recipe looks different from what you remember, it's been gated on purpose: JEI always shows the real recipe."]),
    Q("wel_keys", 4, 1, [tick()], "Your Toolkit", subtitle="Keys, teams and memory", deps=["wel_story"], desc=[
        "&eWhat:&r A few mods make everything easier. Learn their keys now.",
        "&eHow:&r &eR&r / &eU&r over an item: recipes / uses (JEI). &eM&r: map and chunk claiming (FTB Chunks). Hold &e`&r while mining to vein mine (FTB Ultimine). Jade shows what you're looking at.",
        "On a server, share quests and land with a team: &e/ftbteams party create <name>&r, then &e/ftbteams party invite <player>&r.",
        "&eTip:&r Give the game about 8-10 GB of memory in Prism's instance settings (docs/README.md has the Java arguments). If it hitches every few seconds, check the memory bar in F3 first."]),
    Q("wel_tokens", 8, -1, [tick()], "Demigod Tokens", subtitle="Quest rewards you can spend", deps=["wel_progress"], tokens=5, desc=[
        "&eWhat:&r Most quests give &eDemigod Tokens&r. Spend them on convenience items by crafting: torches, food, XP, iron, coke, rubber, osmium, backpack upgrades and a Warp Stone.",
        "&eHow:&r Search &eDemigod Token&r in JEI and press U to see the whole shop.",
        "&eTip:&r Bigger milestones pay more tokens, and later tiers pay more than early ones. Optional quests pay too."]),
    Q("wel_ready", 10, 0, [tick()], "Begin", subtitle="Open Getting Started", deps=["wel_tokens", "wel_keys"], size=1.5, shape="hexagon", desc=[
        "&6The world is waiting to be taken apart and put back together.&r",
        "&eHow:&r That's everything. Open &eGetting Started&r and take your first step.",
        "&eTip:&r You can come back to this chapter any time from the chapter list."]),

    # --- optional side quests -------------------------------------------------------------
    Q("wel_opt_table", 4, -3, [tick()], "The Periodic Table", subtitle="Fun fact: 118 known elements", deps=["wel_story"],
      optional=True, tokens=1, desc=[
        "&eWhat:&r Chemists know 118 elements. Each one is defined by its number of protons, its &eatomic number&r.",
        "&eChemistry:&r Dmitri Mendeleev arranged the table in 1869 by repeating properties, and left gaps for elements nobody had found yet. Gallium and germanium later filled them almost exactly as he predicted.",
        "&eTip:&r The Periodic Table chapter tracks every element you collect."]),
    Q("wel_opt_mass", 6, 3, [tick()], "Nothing Is Lost", subtitle="Fun fact: conservation of mass", deps=["wel_keys"],
      optional=True, tokens=1, desc=[
        "&eWhat:&r Antoine Lavoisier showed in the 1780s that in a closed system, mass before a reaction equals mass after it.",
        "&eChemistry:&r Atoms are rearranged, never created or destroyed in a chemical reaction. That's why every equation balances.",
        "&eTip:&r The Dissolver and Combiner follow the same rule: what you take apart, you can build back."]),

    # --- How to Read This Book (defined above) ---
    *LEGEND,
])
