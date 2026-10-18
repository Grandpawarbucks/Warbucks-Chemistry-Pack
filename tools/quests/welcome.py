"""Quest chapter: welcome. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

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
    Q("wel_progress", 4, -1, [tick()], "How Progression Works", subtitle="Eight tiers, each opened by chemistry", deps=["wel_story"], desc=[
        "&eWhat:&r The pack has 8 tiers. Each one is unlocked by a chemistry milestone, not just more metal.",
        "&eHow:&r Fire and bronze → coke and steel → hydrogen and flight → electricity → acids → oil and plastics → silicon, PVC and the atom → antimatter.",
        "Modern Industrialization's voltage tiers (LV, MV, HV, EV) are the spine. Other mods (Mekanism, AE2, Powah and more) unlock alongside them.",
        "&eTip:&r If a recipe looks different from what you remember, it's been gated on purpose. JEI always shows the real recipe."]),
    Q("wel_keys", 4, 1, [tick()], "Your Toolkit", subtitle="The keys you'll press a thousand times", deps=["wel_story"], desc=[
        "&eWhat:&r A few mods make everything easier. Learn their keys now.",
        "&eHow:&r &eR&r / &eU&r over an item: recipes / uses (JEI). &eM&r: map and chunk claiming (FTB Chunks).",
        "Hold &e`&r while mining to vein mine (FTB Ultimine). Look at a block and Jade shows what it is and what it's doing.",
        "&eTip:&r Inventory sorting, crafting-grid tweaks and the trash slot are in your inventory screen; check Controls for their keys."]),
    Q("wel_book", 6, -1, [tick()], "Reading This Book", subtitle="Sections, side quests and gold lines", deps=["wel_progress"], desc=[
        "&eWhat:&r Every quest is written the same way, so you always know where to look.",
        "&eHow:&r &eWhat&r says what the thing is, &eChemistry&r gives the real science, &eHow&r gives the steps, and &eTip&r saves you time.",
        "Quests marked &eoptional&r sit above or below the main line. They give bonus tokens but never block progress.",
        "&eTip:&r Gold lines are your memories returning. They mark the start of each chapter and its big milestones."]),
    Q("wel_tokens", 8, -1, [tick()], "Demigod Tokens", subtitle="Quest rewards you can spend", deps=["wel_book"], tokens=5, desc=[
        "&eWhat:&r Most quests give &eDemigod Tokens&r. Spend them on convenience items by crafting: torches, food, XP, iron, coke, rubber, osmium, backpack upgrades and a Warp Stone.",
        "&eHow:&r Search &eDemigod Token&r in JEI and press U to see the whole shop.",
        "&eTip:&r Bigger milestones pay more tokens, and later tiers pay more than early ones. Optional quests pay too."]),
    Q("wel_team", 6, 1, [tick()], "Playing Together", subtitle="Share quests and land with friends", deps=["wel_keys"], desc=[
        "&eWhat:&r On a server, make a team so you share quest progress and claimed land.",
        "&eHow:&r &e/ftbteams party create <name>&r, then invite friends with &e/ftbteams party invite <player>&r.",
        "&eTip:&r Split the work: one player on ore processing, one on power, one exploring. Chemistry rewards a production line."]),
    Q("wel_perf", 8, 1, [tick()], "Give the Game Room", subtitle="Memory settings for a big pack", deps=["wel_team"], desc=[
        "&eWhat:&r This is a large pack. Too little memory means stutters; too much can cause long pauses.",
        "&eHow:&r In Prism, open the instance settings and allocate about 8-10 GB. The pack's docs/README.md has the recommended Java arguments.",
        "&eTip:&r If the game hitches every few seconds, check the memory bar in F3 before blaming a mod."]),
    Q("wel_ready", 10, 0, [tick()], "Begin", subtitle="Open Getting Started", deps=["wel_tokens", "wel_perf"], size=1.5, shape="hexagon", desc=[
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
])
