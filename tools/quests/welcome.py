"""Quest chapter: welcome. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("welcome", "Welcome", "minecraft:nether_star",
        ["Read this first: who you are, how this world works, and how to use this book."], MAIN, [
    Q("wel_hello", 0, 0, [tick()], "Welcome, Demigod", size=2.0, shape="gear", tokens=3, items=[("comforts:sleeping_bag_white", 1)], desc=[
        "&6Welcome to Warbucks Chemistry.&r",
        "You're a demigod who has lost your power. You'll win it back by mastering chemistry: taking matter apart into its elements and building it back up.",
        "This book is your guide. Follow the lines from quest to quest; each one tells you &ewhat&r to do and &ehow&r to do it.",
        "How: click the checkmark to collect your first reward."]),
    Q("wel_progress", 2, -1, [tick()], "How Progression Works", deps=["wel_hello"], desc=[
        "The pack has 8 tiers. Each one is unlocked by a &echemistry milestone&r, not just more metal:",
        "Fire and bronze → coke and steel → hydrogen and flight → electricity → acids → oil and plastics → silicon, PVC and the atom → antimatter.",
        "Modern Industrialization's voltage tiers (LV, MV, HV, EV) are the spine. Other mods (Mekanism, AE2, Powah and more) unlock alongside them.",
        "If a recipe looks different from what you remember, it's been gated on purpose. JEI always shows the real recipe."]),
    Q("wel_keys", 2, 1, [tick()], "Your Toolkit", deps=["wel_hello"], desc=[
        "&eR&r / &eU&r over an item: recipes / uses (JEI). &eM&r: map and chunk claiming (FTB Chunks).",
        "&e`&r (hold) while mining: vein mine (FTB Ultimine). Look at a block: Jade shows what it is and what it's doing.",
        "Inventory sorting, crafting-grid tweaks and the trash slot are in your inventory screen; check Controls for their keys."]),
    Q("wel_tokens", 4, -1, [tick()], "Demigod Tokens", deps=["wel_progress"], tokens=5, desc=[
        "Most quests give &eDemigod Tokens&r. Spend them on convenience items by crafting: torches, food, XP, iron, coke, rubber, osmium, backpack upgrades and a Warp Stone.",
        "How: search &eDemigod Token&r in JEI and press U to see the whole shop.",
        "Bigger milestones pay more tokens, and later tiers pay more than early ones."]),
    Q("wel_team", 4, 1, [tick()], "Playing Together", deps=["wel_keys"], desc=[
        "On a server, make a team so you share quest progress and claimed land.",
        "How: &e/ftbteams party create <name>&r, then invite friends with &e/ftbteams party invite <player>&r."]),
    Q("wel_ready", 6, 0, [tick()], "Begin", deps=["wel_tokens", "wel_team"], size=1.5, shape="hexagon", desc=[
        "That's everything. Open &eGetting Started&r and take your first step."]),
])
