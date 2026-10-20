"""Quest book content: the Demigod's Codex. Edit this file, then run python3 tools/build_quests.py.

Conventions:
- Each quest teaches one step and says HOW to do it ("How:" line), so a new player is never lost.
- Story beats are gold (&6), key terms yellow (&e). FTB Quests renders & colour codes.
- Main chapters follow the tiers in docs/PROGRESSION.md; side chapters hang off main quests.
"""
import importlib
import os
import pathlib

from questlib import MAIN, SIDE  # noqa: F401
from layout import normalize_milestones, prune_transitive
from quests._tables import REWARD_TABLES  # noqa: F401  (loot / choice reward tables)

BOOK_TITLE = "Warbucks Chemistry: The Demigod's Codex"

# Chapter groups (the left-hand tabs in the book), in display order: ONE chapter per mod, grouped by category like
# All the Mods 10's book (user decision 2026-10-19, "I really like the breakdown of ATM10"; structure only, ATM10's
# text is All Rights Reserved). A mod's layout sections are section headers on its page. Each chapter's group is set
# here by key, so moving a chapter never touches quest keys (player progress is safe).
# "top" is the ungrouped area above the first tab (title None): FTB Quests shows chapters whose group is "" there,
# as ATM10 does with Welcome, its market, bounty board and tips pages. A group's id comes from its key; titles can
# change freely. Groups with no chapter (e.g. while a QUEST_ONLY check runs) are not written.
GROUPS = {
    "top": None,
    "main": "The Demigod's Path (Main Questline)",
    "gear": "Tools and Gear",
    "storage": "Storage",
    "logistics": "Logistics",
    "resources": "Resources",
    "tech": "Tech",
    "chem": "Chemistry",          # our own identity, where ATM10 has its Modern Industrialization group
    "energy": "Energy",
    "magic": "Magic",
    "world": "Exploration",
}
LAYOUT = {
    # ATM10's top: Welcome, Market, Market Tiers, Bounty Board, Building Tips, Tips and Tricks.
    "top": ["welcome", "tips", "building", "hunting", "lab_notes", "completionist"],
    "main": ["start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"],
    "gear": ["tools", "harvest", "apotheosis", "relics", "artifacts", "silentgear", "qol"],
    "storage": ["storage", "ae2", "eae"],
    "logistics": ["logic", "integrated", "pylons"],
    "resources": ["farming", "mystical", "factory"],   # factory = mob data (HNN) + big crafting, as ATM10 files HNN
    "tech": ["create", "mekanism", "mekanism_power", "justdirethings"],
    "chem": ["periodic"],
    "energy": ["power", "generators", "powah"],
    "magic": ["ars", "occultism", "neovitae", "apothic_enchanting", "projecte"],
    "world": ["worlds", "explore", "undergarden", "twilight", "deeperdarker", "allthemodium", "space"],
}
# Sidebar titles that differ from the chapter file's own title (ATM10-style names for the top pages).
TITLES = {"building": "Building Tips", "hunting": "Bounty Board", "tips": "Tips and Tricks",
          "mekanism_power": "Mekanism: Power", "worlds": "The End"}  # worlds.py holds only the End now
# Which ATM10 chapter each of our pages mirrors (user decision 2026-10-20: quest-for-quest where we have the mod,
# the same page shapes, pictures in ATM10's image spots). Our chapter key -> ATM10 chapter file stem (its
# config/ftbquests/quests/chapters/<stem>.snbt; the folder is ATM10_BOOK in tools/layout.py). Geometry and
# requirements only: ATM10's text and image files are All Rights Reserved and never copied. A writer can set
# Chapter(mirror="...") in the chapter file instead; that wins over this map. The "mirror" layout motif (tools/
# layout.py) is the default wherever a target exists; Q(mirror="<16 hex id>") names the exact ATM10 quest.
MIRROR = {
    "storage": "storage", "ae2": "applied_energistics_2", "logic": "basic_logistics", "power": "basic_power",
    "powah": "powah", "create": "create", "justdirethings": "justdirethings", "mekanism": "mekanism",
    "mekanism_power": "mekanism_reactors", "ars": "ars_nouveau", "occultism": "occultism", "neovitae": "neo_vitae",
    "apotheosis": "apotheosis_gear", "relics": "relics", "tools": "basic_tools", "harvest": "basic_armor",
    "farming": "food_and_farming", "mystical": "elmystical_agriculturerr", "factory": "hostile_neural_networks",
    "twilight": "twilight_forest", "undergarden": "undergarden", "deeperdarker": "deeper_and_darker",
    "allthemodium": "allthemodium", "building": "building_tips", "hunting": "bounty_board",
    "tips": "tips_and_tricks", "welcome": "welcome", "start": "mainquestline_part_1",
    # chapters added in the v14 round (their files also set Chapter(mirror=...), which wins)
    "eae": "extended__advanced_ae", "artifacts": "artifacts", "silentgear": "silent_gear", "pylons": "pylons",
    "apothic_enchanting": "apothic_enchanting",
    # split out of logic and power on 2026-10-20 (keys unchanged; the files also set Chapter(mirror=...))
    "integrated": "integrated_dynamics", "generators": "generators",
}
# Chapter files that don't exist yet are skipped quietly, so new chapters can be added one at a time.
_QDIR = pathlib.Path(__file__).resolve().parent / "quests"
ORDER = [k for g in LAYOUT.values() for k in g if (_QDIR / f"{k}.py").exists()]
# A chapter file that isn't in LAYOUT is not built: say so (its quests would silently vanish otherwise).
# Retired chapter files, kept on disk but never built (2026-10-20, user: "Coins replace tokens"): the Demigod Token
# shop pages. The Wardaddy Market (Market key, coins) is the only shop now; see tools/quests/STYLE.md.
RETIRED = {"market", "shop_materials", "shop_gear", "shop_world"}
UNLISTED = sorted(f.stem for f in _QDIR.glob("*.py")
                  if not f.stem.startswith("_") and f.stem not in ORDER and f.stem not in RETIRED)
# Writers can validate just their own chapters (plus the main tiers) while others are mid-edit:
#   QUEST_ONLY=ars,apotheosis python3 tools/build_quests.py --check
ONLY = [k for k in os.environ.get("QUEST_ONLY", "").split(",") if k]
if ONLY:
    ORDER = [k for k in ORDER if k in ONLY or k in ("welcome", "start", *(f"t{i}" for i in range(8)))]
PAGES = [importlib.import_module(f"quests.{k}").CHAPTER for k in ORDER]  # one per chapter file
for _c in PAGES:
    _c.group = next(g for g, ks in LAYOUT.items() if _c.key in ks)
    _c.title = TITLES.get(_c.key, _c.title)
    if _c.mirror is None:  # Chapter(mirror=) in the file wins; else the MIRROR map; else no mirror target
        _c.mirror = MIRROR.get(_c.key)
    normalize_milestones(_c)  # capstone = 2.0 gear, section milestone = 1.5 hexagon (tools/layout.py)

# Automatic layout style per chapter (tools/layout.py; manual chapters ignore it). Picked by looking at
# test/build_quest_preview.py --gallery next to ATM10's "The Beginning" and at tools/layout_lint.py (orthogonal %,
# lone quests, crossings, size). v13 (2026-10-19): "comb" everywhere it beats the older motif:
#   "comb":     ATM10-style main questline: one straight spine (wrapped into 2-3 serpentine rows past ~16 quests),
#               everything else hangs straight down or up from it as small trees on a 2-cell grid; nearly every
#               line horizontal or vertical (default);
#   "radial":   the hub sits in the middle with its own quests ringed around it; the other sections are spokes
#               (kept for building: a page of independent hubs, where the comb tangles);
#   "winding", "molecule", "tree", "grid", "spine": older motifs (v11/v12), kept for comparison and LAYOUT_STYLE.
# Per chapter on 2026-10-19 (comb vs the old motif): every auto page is comb except building (radial).
#   "mirror":   v14 (2026-10-20, user decision): the page mirrors its ATM10 chapter (MIRROR above / Chapter(mirror=)):
#               matched quests sit at the ATM10 quest's position, unmatched ones in free cells by their deps, and
#               ATM10's image spots become our pictures (tools/build_pictures.py). The default wherever a mirror
#               target exists and its ATM10 file is present; STYLES below still wins (building stays radial only if
#               that beats the mirror: checked 2026-10-20, the mirror wins, so building is a mirror page too).
#   2026-10-20 later (user: "lets make it comb shaped as we have before for the quests if it gets to cluttered just
#   make it another chapter"): every auto page is a comb again. The mirror motif and the Q(mirror=)/MIRROR data stay
#   (ATM10's quest-for-quest content is kept); set USE_MIRROR = True to draw mirror pages again.
STYLES = {"tips": "grid"}
DEFAULT_STYLE = "comb"
USE_MIRROR = False


def style_of(chapter):
    """The layout motif of a chapter: STYLES by key, else (only with USE_MIRROR) "mirror" where its ATM10 chapter
    is on disk, else comb."""
    if chapter.key in STYLES:
        return STYLES[chapter.key]
    import layout
    if USE_MIRROR and getattr(chapter, "mirror", None) and layout.load_mirror(chapter.mirror):
        return "mirror"
    return DEFAULT_STYLE
# Section shapes on a page whose motif otherwise draws plain trees: "molecule" rings (where a section fits a ring).
# Only the winding/radial/molecule motifs use it (none at the moment).
BLOCKS = {}
# Trying a motif without editing this file: LAYOUT_STYLE=t6=radial,t3=tree (style or style+molecule) for a build/check.
for _kv in filter(None, os.environ.get("LAYOUT_STYLE", "").split(",")):
    _k, _, _v = _kv.partition("=")
    STYLES[_k], _, _b = _v.partition("+")
    BLOCKS[_k] = _b or None
import layout as _layout  # noqa: E402
# Comb and mirror pages add a quest link for every quest whose deps are all in other chapters; those linked quests
# then never get hide flags (tools/layout.py _ext_targets), like shared_quests.
_layout.COMB_PAGES = {c.key for c in PAGES if c.layout != "manual" and style_of(c) in ("comb", "mirror")}


# --- "Mod = category" split (v12, 2026-10-19; SWITCHED OFF by the ATM10-style regroup the same day) -------------
# One chapter per mod is the current design. The old split is kept, off, in case it's wanted again: every page in a
# group listed in SPLIT_TABS becomes its own category (an FTB chapter group, titled after the page) and the layout's
# sections of that page become its chapters, in progression order. Quest keys never change: only which chapter
# shows a quest. The first chapter keeps the page's key (so links and docs still resolve); the others are
# "<page>_<slug of the chapter title>". A page that comes out as one chapter stays in its own group.
SPLIT_TABS = ()                         # e.g. ("tech", "magic") to split those groups' pages again
JOIN = {"mekanism_power": "mekanism"}   # page -> page whose category its chapters join (one category per mod)
SPLIT_MIN, SPLIT_MAX = 5, 25            # a section under SPLIT_MIN quests joins a neighbour; merges stay <= SPLIT_MAX
PAGE_TITLES = {}                        # category title when the page title doesn't read well as one
# Chapter names and subtitles, by the chapter's root quest (the quest the layout names a section after); icon is
# optional (default: the root quest's item). A chapter not listed here keeps the layout's auto title. Only used when
# SPLIT_TABS splits a group; pruned 2026-10-20 to the roots a split of the current pages would still produce.
CHAPTER_TITLES = {
    # Gear and Comfort (tools)
    "tc_sg_repair": ("Silent Gear", "Repair kits, parts, grading and jewellery"),
    "tc_scuba": ("Mekanism Gear", "Paxels, the Disassembler, scuba gear and the MekaSuit"),
    "tc_jetpack": ("Flight and Gadgets", "Iron Jetpacks, the Angel Ring and handy gadgets"),
    # Tools, Armour and Harvest Tiers (harvest)
    "hv_intro": ("Stone and Bronze", "Why ores need a better pick: the early tiers"),
    "hv_iron": ("Iron and Diamond", "Hard ores, diamond tools and the scratch test"),
    "hv_steel": ("Steel and Obsidian", "The diamond tier without diamonds, and beyond"),
    # Storage and Logistics (storage)
    "s_barrel": ("Sophisticated Storage", "Barrels, chests, tiers and upgrades"),
    # Power
    "pw_mi_storage": ("Steam and Crystals", "EU storage, steam turbines and Powah crystals"),
    # Farming and Food
    "f_knife": ("Farmer's Delight", "Knives, cutting boards and new crops"),
    "fd_bees": ("Gardens and Bees", "Bees, kitchen gardens and odd orchards"),
    # Quality of Life
    "ql_start": ("Comfort First", "Graves, backpacks, teams and other comforts"),
    "q_waystone": ("Waystones and Shortcuts", "Travel, the all-in-one manual and crafting sticks"),
    "ut_sticks": ("Utilitarian", "Shortcuts for building and moving things"),
    "ut_snad": ("Odds and Ends", "Snad, clocks, mufflers and pylons"),
    # Building and Decoration
    "bd_rocks": ("Gadgets and Stone", "Building gadgets and every kind of rock"),
    "bd_jar": ("Furniture and Fun", "Framed blocks, seats, jars and soap"),
    # The Periodic Table
    "pt_intro": ("Reading the Table", "Metalloids, non-metals and the p-block families"),
    "pt_alkali": ("The Metals", "Alkali, alkaline earth and transition metals"),
    "pt_noble": ("Collecting the Table", "Noble gases, rare earths and complete groups"),
    "pt_co2": ("Compounds", "Bonds, acids, salts and everyday chemicals"),
    # Mekanism (mekanism + mekanism_power)
    "mk2_intro": ("Factories and Upgrades", "The configurator, factories, upgrades and infusion"),
    "mk2_tablet": ("Alloys and Teleporters", "Reinforced and atomic alloys, teleporters and the miner"),
    "mkp_intro": ("Power and Big Machines", "Boilers, turbines, fusion and More Machine"),
    # Mob Data and Big Crafting (factory)
    "mf_components": ("Extended Crafting", "Black iron, bigger tables and crafting cores"),
    "mf_compact": ("Compact Machines", "Rooms inside blocks, and cake that teleports"),
    # Automation and Logic
    "lg_computer": ("Computers and Autocrafting", "CC: Tweaked, peripherals and a first chemical line"),
    # The Mechanical Age (create)
    "cr_power": ("Contraptions", "Bearings, pistons, pulleys and drills"),
    "cr_belts": ("Belts and Logistics", "Millstones, saws, depots, funnels and vaults"),
    # Applied Energistics
    "ae_certus": ("Certus Quartz", "Sky stone, charged certus and fluix"),
    "ae_condenser": ("Quantum Tech", "The condenser, quantum computer and armour cards"),
    "s_ae_cell": ("Storage Cells", "Cells, MEGA cells and flux storage"),
    # Ars Nouveau
    "m_brazier": ("Rituals", "The ritual brazier, archmage book and familiars"),
    "ars_storage": ("Storage and Charms", "Storage lectern, turrets, charms and rings"),
    "ars_fire_essence": ("Elemental Essences", "Fire, earth, water and the caster's tools"),
    # Neo Vitae
    "nv_altar": ("The Blood Altar", "Ara Vitae, the first orb, sigils and runes"),
    # Relics and Artifacts
    "m_reliquary": ("Reliquary", "Alkahestry, mob charms and odd relics"),
    # Equivalent Exchange
    "pe_stone": ("The Philosopher's Stone", "Transmutation, covalence dust and fuels"),
    "pe_dm": ("Dark Matter", "Dark and red matter tools and armour"),
    # Other Worlds
    "w_end": ("The End and the Deep Dark", "The dragon, End cities, ancient cities and the Otherside"),
    "w_undergarden": ("Undergarden Metals", "Regalium, catacombs and the forgotten ingot"),
    # Exploration
    "ex_village": ("Villages and Mansions", "Every kind of village, outposts and mansions", "minecraft:bell"),
    "ex_zombie_dungeon": ("Dungeons and Mines", "Catacombs, strongholds, mineshafts and trials", "minecraft:trial_key"),
    "ex_shipwreck": ("Temples and the Sea", "Temples, shipwrecks, ruins and monuments", "minecraft:heart_of_the_sea"),
    "ex_fortress": ("The Nether", "Fortresses, bastions and fossils", "minecraft:nether_bricks"),
    "ex_bio_chalk": ("Biomes", "Chalk cliffs, hot springs, wetlands and more", "minecraft:cherry_sapling"),
    # The Undergarden
    "ug_rogdorium": ("Utherium", "Rogdorium, the infuser and utherium gear"),
    # The Twilight Forest
    "tf_oak": ("Into the Twilight", "Magic trees, steeleaf, ironwood and the questing ram"),
    # Space
    "w_desh": ("The Moon and Mars", "Desh, ostrum, oxygen and the rover"),
    "w_suit": ("Venus and Mercury", "Heat suits, calorite and the hot planets"),
    "w_space_metals": ("Glacio", "Alien metals, launch sites and moon dungeons"),
    # Monster Hunting
    "hn_zombie_1": ("The Undead", "Zombies, skeletons and the drowned", "minecraft:rotten_flesh"),
    "hn_spider_1": ("Creepers and Crawlers", "Creepers, spiders and silverfish", "minecraft:gunpowder"),
    "hn_witch": ("Night Creatures", "Endermen, witches, slimes and phantoms", "minecraft:ender_pearl"),
    "hn_pillager": ("Raiders and Guardians", "Pillagers, ravagers and elder guardians", "minecraft:crossbow"),
    "hn_blaze_1": ("Nether Hunts", "Blazes, ghasts, magma cubes and bastions", "minecraft:blaze_rod"),
    "hn_wither_skel_1": ("Skulls and Giants", "Wither skeletons, Twilight beasts and the Wither",
                         "minecraft:wither_skeleton_skull"),
    "hn_sculk": ("Strange Creatures", "Shulkers, Undergarden beasts, sculk and aliens", "minecraft:shulker_shell"),
}


def _icon_of(q):
    """The item a quest shows: its icon, else its first item task (or the first item of an anyof filter)."""
    import re
    if getattr(q, "icon", None):
        return q.icon
    for t in q.tasks:
        if t[0] == "item":
            return t[1]
        if t[0] == "filter":
            m = re.search(r"item\(([^()]+)\)", t[1])
            if m:
                return m.group(1)
    return None


def _split_page(page):
    """The page's sections merged into chapter-sized parts: [{"members": [keys], "root": key}] in progression
    order (a part comes after the parts it depends on; ties keep reading order)."""
    import layout
    secs = layout.page_sections(page, "grid" if page.style == "grid" else "tree")
    parts = [{"members": list(s["members"]), "root": s["root"], "title": s["title"]} for s in secs]
    byk = {q.key: q for q in page.quests}
    idx = {q.key: i for i, q in enumerate(page.quests)}

    def links(a, b):
        sa, sb = set(a["members"]), set(b["members"])
        return sum(1 for k in sa for d in byk[k].deps if d in sb) + sum(1 for k in sb for d in byk[k].deps if d in sa)

    while len(parts) > 1:
        small = [i for i, p in enumerate(parts) if len(p["members"]) < SPLIT_MIN]
        if not small:
            break
        i = min(small, key=lambda i: (len(parts[i]["members"]), i))
        cand = [j for j in range(len(parts)) if j != i and (abs(j - i) == 1 or links(parts[i], parts[j]))]
        j = min(cand, key=lambda j: (len(parts[i]["members"]) + len(parts[j]["members"]) > SPLIT_MAX,
                                     -links(parts[i], parts[j]), abs(j - i), len(parts[j]["members"])))
        keep, gone = (parts[j], parts[i])
        keep["members"] = sorted(keep["members"] + gone["members"], key=idx.get)
        parts.pop(i)
    # Progression order: Kahn's algorithm over the deps between parts, ties by the earliest quest.
    part_of = {k: n for n, p in enumerate(parts) for k in p["members"]}
    need = {n: {part_of[d] for k in p["members"] for d in byk[k].deps if d in part_of and part_of[d] != n}
            for n, p in enumerate(parts)}
    depth = {}  # longest chain of in-page deps above a quest: early parts (shallow roots) come first among equals
    for q in page.quests:
        depth.setdefault(q.key, 0)
    for _ in range(len(page.quests)):
        moved = False
        for q in page.quests:
            dd = max((depth[d] + 1 for d in q.deps if d in depth), default=0)
            if dd > depth[q.key] and dd <= len(page.quests):
                depth[q.key], moved = dd, True
        if not moved:
            break
    first = {n: (depth[p["root"]], min(idx[k] for k in p["members"])) for n, p in enumerate(parts)}
    entry = part_of.get(page.quests[0].key, 0)  # the page's first quest (its way in) opens the first chapter
    out, done = [], set()
    while len(out) < len(parts):
        todo = [n for n in range(len(parts)) if n not in done]
        ready = [entry] if not out else [n for n in todo if need[n] <= done]
        if not ready:  # parts that need each other: the one with the fewest unmet needs first
            least = min(len(need[n] - done) for n in todo)
            ready = [n for n in todo if len(need[n] - done) == least]
        n = min(ready, key=first.get)
        out.append(parts[n])
        done.add(n)
    return out


def _split(pages):
    """Pages -> (chapters, groups): the "Mod = category" sidebar. Returns the chapter list in sidebar order and
    the GROUPS dict (group key -> title) in display order."""
    import layout
    from questlib import Chapter
    if not SPLIT_TABS:  # one chapter per mod (current design): pages are the chapters, in LAYOUT order
        return list(pages), dict(GROUPS)
    groups = {g: GROUPS[g] for g in GROUPS if g not in SPLIT_TABS}
    chapters = [c for c in pages if c.group in groups]
    taken = {c.key for c in pages}
    for tab in SPLIT_TABS:
        for page in [c for c in pages if c.group == tab]:
            page.style = style_of(page)
            parts = _split_page(page)
            if len(parts) < 2:
                groups.setdefault(tab, GROUPS[tab])
                page.page = None
                chapters.append(page)
                continue
            gkey = "p_" + JOIN.get(page.key, page.key)
            if gkey not in groups:
                owner = next((c for c in pages if c.key == gkey[2:]), page)
                groups[gkey] = PAGE_TITLES.get(owner.key, owner.title.split(". ", 1)[-1])
            home = {k: n for n, p in enumerate(parts) for k in p["members"]}
            byk = {q.key: q for q in page.quests}
            used_icons = {c2.icon for c2 in chapters if c2.group == gkey}
            subs = []
            for n, p in enumerate(parts):
                root = byk[p["root"]]
                title, sub, icon = (tuple(CHAPTER_TITLES[p["root"]]) + (None, None))[:3] \
                    if p["root"] in CHAPTER_TITLES else (p["title"], None, None)
                if n == 0:
                    key = page.key
                else:
                    key = f"{page.key}_{layout.slug(title)}"
                    while key in taken:
                        key += "_2"
                taken.add(key)
                if icon is None:  # the root quest's item; another member's if a sibling chapter already shows it
                    for k in [p["root"]] + p["members"]:
                        icon = _icon_of(byk[k])
                        if icon and icon not in used_icons:
                            break
                    icon = icon or page.icon
                used_icons.add(icon)
                quests = [q for q in page.quests if home.get(q.key) == n]
                # Quest links: the page's own links go to the chapters whose quests depend on them (the first
                # chapter keeps those nothing depends on); every quest a chapter needs from a sibling is linked.
                lks = [l for l in page.links if any(l[0] in q.deps for q in quests)]
                if n == 0:
                    lks += [l for l in page.links if not any(l[0] in q.deps for q in page.quests)]
                ch = Chapter(key, title, icon, [sub or title], SIDE, quests, links=lks, layout=page.layout)
                ch.group, ch.page, ch.page_title, ch.headers = gkey, page.key, groups[gkey], False
                ch.style = style_of(page)
                if ch.style == "winding":
                    ch.style = "tree"   # a winding page's chapters are short: plain trees
                elif ch.style == "radial" and n:
                    ch.style = "tree"   # only the hub's chapter is a radial hub page
                subs.append(ch)
            chapters += subs
    # Every quest a chapter needs from another chapter of its category is shown there as a quest link.
    home = {q.key: c for c in chapters for q in c.quests}
    for c in chapters:
        if not getattr(c, "page", None):
            continue
        for q in c.quests:
            for d in q.deps:
                h = home.get(d)
                if h is not None and h is not c and h.group == c.group and all(d != l[0] for l in c.links):
                    c.links.append((d, 0, 0))
    return chapters, groups


for _c in PAGES:  # the layout finds sections on pruned deps (as apply() does), and names loose groups by page
    _c.pruned_deps = prune_transitive(_c.quests)
    _c.home_of = {q.key: c.key for c in PAGES for q in c.quests}
    _c.chapter_titles = {c.key: c.title.split(". ", 1)[-1] for c in PAGES}
# --- Page splits (2026-10-20, user: "if it gets to cluttered just make it another chapter no big deal") ---------
# A mod page too big or tangled for one comb (over about 35 x 22 cells, more than ~3 crossings, many lone quests,
# a low tools/layout_lint.py score) becomes 2 or more chapters in the same group, right after it, cut along its
# layout sections in progression order. Quest keys never change (only which chapter shows a quest); the first
# chapter keeps the page's key, the others are "<page>_<slug of their title>". Each gets its own banner (the build
# writes one per chapter), a distinct icon, the page's token rate, and quest links to whatever it needs from its
# siblings (so its first quest links back to the parent). Only mod pages: the main path, shop and top pages stay.
# Page key -> the chapters after the first: (key suffix, sidebar title, subtitle), named after the sections they
# hold (checked against the build, 2026-10-20); their number sets the split. The cut is chosen by the build (see
# _split_pages): if a page's sections change a lot, check the names still fit (the sections are listed in the
# gallery: test/build_quest_preview.py --gallery).
SPLIT_PAGES = {
    "mekanism": [("machines", "Mekanism: Ore Lines and Big Builds", "Machines, the 2x to 5x ore lines and multiblocks"),
                 ("logistics", "Mekanism: Logistics and Gadgets", "Pipes, storage, upgrades, chemical machines, gadgets")],
    "mekanism_power": [("fusion", "Mekanism: Fusion and the MekaSuit", "Fusion, antimatter, modules and the MekaSuit")],
    "create": [("contraptions", "Create: Contraptions and Trains", "Kinetics, contraptions and trains")],
    "storage": [("backpacks", "Storage: Backpacks and Furnaces", "Sophisticated Backpacks and Iron Furnaces")],
    "harvest": [("armour_sets", "Armour Sets and Refined Obsidian", "Every armour set, and refined obsidian")],
    "mystical": [("crops", "Mystical Agriculture: Crops and Mob Seeds", "Tier 1 to 4 crops and the mob seeds")],
    "justdirethings": [("gadgets", "Just Dire Things: Armour and Gadgets", "Armour, tool and armour upgrades, gadgets")],
    "powah": [("higher_tiers", "Powah: Niotic to Nitro", "The niotic, spirited and nitro tiers")],
    "ae2": [("autocrafting", "AE2: Autocrafting and Cells", "Autocrafting, storage cells, wireless and the condenser")],
    "ars": [("rituals", "Ars Nouveau: Rituals and Glyphs", "Rituals and the tier 2 and 3 glyphs"),
            ("elemental", "Ars Nouveau: Elemental and Helpers", "Ars Elemental, essences, the Wilden and helpers")],
    "undergarden": [("biomes", "Undergarden: Biomes and Utherium", "The biomes below, gathering and utherium tools")],
    "twilight": [("progression", "Twilight Forest: The Labyrinth and Beyond",
                  "The labyrinth, hydra, dark tower, highlands and the final plateau")],
}


def _split_pages(chapters):
    """Split the pages in SPLIT_PAGES (see above). Returns the new chapter list (sidebar order)."""
    from questlib import Chapter
    import layout
    global SPLIT_MIN, SPLIT_MAX
    out, taken = [], {c.key for c in chapters}
    for page in chapters:
        extra = SPLIT_PAGES.get(page.key) or []
        n = len(extra) + 1
        if n < 2 or page.layout == "manual":
            out.append(page)
            continue
        page.style = style_of(page)
        keep_min, keep_max = SPLIT_MIN, SPLIT_MAX
        SPLIT_MIN, SPLIT_MAX = 6, 10 ** 6
        try:
            parts = _split_page(page)  # sections, small ones merged, in progression order
        finally:
            SPLIT_MIN, SPLIT_MAX = keep_min, keep_max
        if len(parts) < n:
            out.append(page)
            continue
        # n chunks of consecutive parts: the biggest chunk small, and few deps between chunks (each needs a quest
        # link, and links bring lines that cross)
        import itertools
        sizes = [len(p_["members"]) for p_ in parts]
        pbyk = {q.key: q for q in page.quests}
        part_of = {k: i for i, p_ in enumerate(parts) for k in p_["members"]}
        fan = {}
        for q in page.quests:
            for d in q.deps:
                fan[d] = fan.get(d, 0) + 1
        best = None
        for cuts in itertools.combinations(range(1, len(parts)), n - 1):
            bounds = (0,) + cuts + (len(parts),)
            chunk = {i: j for j in range(n) for i in range(bounds[j], bounds[j + 1])}
            worst = max(sum(sizes[bounds[j]:bounds[j + 1]]) for j in range(n))
            # a hub that ends up linked from a sibling chapter keeps no hide flags (FTB applies them to every
            # button of a quest), so its whole fan stays drawn: cutting below a hub costs by its fan-out
            across = sum(1.0 + fan.get(d, 0) / 3 for _, d in {(chunk[part_of[k]], d) for k in part_of
                         for d in pbyk[k].deps if d in part_of and chunk[part_of[d]] != chunk[part_of[k]]})
            if min(sum(sizes[bounds[j]:bounds[j + 1]]) for j in range(n)) < 12:
                continue  # no tiny chapters
            cost = worst + 1.5 * across
            if best is None or cost < best[0]:
                best = (cost, bounds)
        if best is None:
            out.append(page)
            continue
        bounds = best[1]
        chunks = [[k for p_ in parts[bounds[j]:bounds[j + 1]] for k in p_["members"]] for j in range(n)]
        home = {k: j for j, ks in enumerate(chunks) for k in ks}
        byk = {q.key: q for q in page.quests}
        all_q, all_l = list(page.quests), list(page.links)
        used_icons = {page.icon}
        subs = []
        for j in range(n):
            quests = [q for q in all_q if home.get(q.key) == j]
            lks = [l for l in all_l if any(l[0] in q.deps for q in quests)]
            if j == 0:
                ch = page
                ch.quests = quests
                ch.links = lks + [l for l in all_l if not any(l[0] in q.deps for q in all_q)]
            else:
                suffix, title, sub = extra[j - 1]
                key = f"{page.key}_{suffix}"
                while key in taken:
                    key += "_2"
                taken.add(key)
                icon = None
                for k in chunks[j]:
                    icon = _icon_of(byk[k])
                    if icon and icon not in used_icons:
                        break
                icon = icon or page.icon
                used_icons.add(icon)
                ch = Chapter(key, title, icon, [sub], page.group, quests, links=lks, layout=page.layout,
                             mirror=page.mirror)
                ch.group = page.group
            ch.page, ch.split_of = page.key, page.key
            ch.style = style_of(page)
            subs.append(ch)
        out += subs
    # Every quest a split chapter needs from a sibling is shown there as a quest link.
    home = {q.key: c for c in out for q in c.quests}
    for c in out:
        if not getattr(c, "split_of", None):
            continue
        for q in c.quests:
            for d in q.deps:
                h = home.get(d)
                if h is not None and h is not c and getattr(h, "split_of", None) == c.split_of                         and all(d != l[0] for l in c.links):
                    c.links.append((d, 0, 0))
    return out


CHAPTERS, GROUPS = _split(PAGES)
CHAPTERS = _split_pages(CHAPTERS)
_layout.COMB_PAGES |= {c.key for c in CHAPTERS if c.layout != "manual" and c.style in ("comb", "mirror")}
_layout.SPLIT_OF = {c.key: c.split_of for c in CHAPTERS if getattr(c, "split_of", None)}
_HOME = {q.key: c.key for c in CHAPTERS for q in c.quests}
_TITLES = {c.key: c.title.split(". ", 1)[-1] for c in CHAPTERS}
_QUESTS = {q.key: q for c in CHAPTERS for q in c.quests}
for _c in CHAPTERS:
    if not getattr(_c, "page", None):  # split chapters got their style from their page in _split
        _c.style = style_of(_c)
    _c.block_kind = BLOCKS.get(getattr(_c, "page", None) or _c.key)
    _c.home_of, _c.chapter_titles = _HOME, _TITLES  # names loose groups after the chapter they follow on from
    # Every chapter's redundant deps are dropped up front (layout.prune_transitive; what players must do doesn't
    # change), so a page knows the final deps of the quests its links show: FTB draws those lines too.
    _c.pruned_deps = prune_transitive(_c.quests)
    _c.book_quests = _QUESTS
# Quests other chapters depend on (so they may be shown there as quest links): the layout never sets the hide-line
# flags on them, because FTB applies a quest's flags to every button of it, links on other pages included.
def _linked_elsewhere():
    """Quests shown as a quest link on some other page: the writers' links plus each auto chapter's entry links
    (the deps in other chapters of its first spine quest, as tools/layout.py adds them)."""
    from layout import _graph, _spine
    out = set()
    split_of = {c.key: getattr(c, "split_of", None) for c in CHAPTERS}
    for c in CHAPTERS:
        # a link to a sibling chapter of the same split page doesn't count: hiding a hub's fan there too (FTB
        # applies a quest's flags to all its buttons) is better than leaving the whole fan drawn on its own page
        out |= {lk for lk, _, _ in c.links if _HOME.get(lk) != c.key
                and not (split_of[c.key] and split_of.get(_HOME.get(lk)) == split_of[c.key])}
        if c.layout != "manual" and c.quests:
            byk, idx, parents, children, order = _graph(c.quests)
            G = {"byk": byk, "idx": idx, "parents": parents, "children": children, "order": order,
                 "opt": {k: bool(byk[k].optional) for k in byk}}
            out |= {d for d in byk[_spine(set(byk), G)[0]].deps if d in _HOME and d not in byk}
    return out


_SHARED = _linked_elsewhere()
for _c in CHAPTERS:
    _c.shared_quests = _SHARED

# Quest reward rate per chapter, in the old Demigod Token units (milestone quests, size >= 1.5, pay double).
# tools/build_quests.py pays it as Wardaddy Market coins: COINS_PER_TOKEN coins per unit (FTB Quests "currency"
# reward, paid into the SG-Economy wallet through FTB XMod Compat).
TOKENS = {"welcome": 1, "start": 1, "t0": 1, "t1": 2, "t2": 2, "t3": 3, "t4": 3, "t5": 4, "t6": 5, "t7": 8,
          "seed": 10, "creation": 10, "completionist": 3, "harvest": 1}
for _c in CHAPTERS:  # a split page's chapters (if the split is ever switched on) all pay the page's rate
    _c.tokens = TOKENS.get(getattr(_c, "page", None) or _c.key, 1)
    _c.linear = False  # the retired token-shop pages were the only linear chapters

# Tier milestones (size >= 1.5 in t0..t7) also roll that tier's loot table, unless set by hand.
for _c in CHAPTERS:
    if _c.key in REWARD_TABLES:
        for _q in _c.quests:
            if (_q.size or 1) >= 1.5 and not _q.loot and not _q.optional:
                _q.loot = _c.key


# --- Quest editor overrides (tools/quest_editor.py) ---------------------------------------------
# tools/quest_overrides.json maps a quest key to any of {x, y, title, subtitle, desc}, or
# "link:<chapter>:<quest>" to {x, y} for a quest link. Applied AFTER the automatic layout (so a dragged quest
# keeps its spot), they only ever change position and text: never keys, deps, tasks or rewards.
OVERRIDES_FILE = pathlib.Path(__file__).resolve().parent / "quest_overrides.json"
_OVERRIDE_FIELDS = {"x", "y", "title", "subtitle", "desc"}


def load_overrides():
    """The overrides dict ({} if the file is missing or empty). Invalid JSON raises (edits must not vanish silently)."""
    import json
    if not OVERRIDES_FILE.exists():
        return {}
    text = OVERRIDES_FILE.read_text(encoding="utf-8").strip()
    data = json.loads(text) if text else {}
    if not isinstance(data, dict):
        raise ValueError(f"{OVERRIDES_FILE.name}: top level must be a JSON object")
    return data


def apply_overrides(chapters=None, overrides=None):
    """Apply the overrides to already laid-out chapters. Returns a list of warnings (unknown keys, bad values)."""
    chapters = CHAPTERS if chapters is None else chapters
    overrides = load_overrides() if overrides is None else overrides
    quests = {q.key: q for c in chapters for q in c.quests}
    bych = {c.key: c for c in chapters}
    warnings = []
    num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
    for k, o in overrides.items():
        if not isinstance(o, dict):
            warnings.append(f"override {k}: value must be an object")
            continue
        for f in sorted(set(o) - _OVERRIDE_FIELDS):
            warnings.append(f"override {k}: unknown field {f!r} (ignored)")
        for f in ("x", "y"):
            if f in o and not num(o[f]):
                warnings.append(f"override {k}: {f} must be a number (ignored)")
        if k.startswith("link:"):
            _, ck, lk = (k.split(":", 2) + ["", ""])[:3]
            c = bych.get(ck)
            i = next((i for i, (l, _, _) in enumerate(c.links) if l == lk), None) if c else None
            if i is None:
                if not ONLY:
                    warnings.append(f"override {k}: no such quest link (ignored)")
                continue
            for f in sorted({"title", "subtitle", "desc"} & set(o)):
                warnings.append(f"override {k}: links only take x/y, not {f} (ignored)")
            l, x, y = c.links[i]
            c.links[i] = (l, o["x"] if num(o.get("x")) else x, o["y"] if num(o.get("y")) else y)
            continue
        q = quests.get(k)
        if q is None:
            if not ONLY:
                warnings.append(f"override {k}: no quest with that key (ignored)")
            continue
        if num(o.get("x")):
            q.x = o["x"]
        if num(o.get("y")):
            q.y = o["y"]
        for f in ("title", "subtitle"):
            if f in o:
                if o[f] is None or isinstance(o[f], str):
                    setattr(q, f, o[f])
                else:
                    warnings.append(f"override {k}: {f} must be a string (ignored)")
        if "desc" in o:
            if isinstance(o["desc"], list) and all(isinstance(s, str) for s in o["desc"]):
                q.desc = list(o["desc"])
            else:
                warnings.append(f"override {k}: desc must be a list of strings (ignored)")
    return warnings
