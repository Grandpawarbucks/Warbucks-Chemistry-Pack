"""Wardaddy Market price list for Warbucks Chemistry: writes pack/config/wdmarket/prices.json and the tier fields of
pack/config/wdmarket/settings.json. Re-runnable; run it after mod or KubeJS changes (it reads the server dumps).

    .venv\\Scripts\\python.exe tools\\build_market_prices.py

Inputs: test/ids.tsv (item registry and names), test/dump/recipe_dump.json + registry_dump.json (recipes and tags
after KubeJS, from test/audit_dump.ps1), the quest book (tools/quest_data.py) and tools/market_price_overrides.json
(optional, {"items": {"<id>": <buy coins>}}: fixed buy prices, applied last).

Coin scale (user decision 2026-10-20, "Coins replace tokens"): 1 old Demigod Token = 100 coins, so a Chapter I
quest pays 100 coins and the whole book about 600,000. Prices follow the old token shop: 16 iron ingots cost 2 tokens
there, so an iron ingot is worth about 24 coins here.

How a price is made:
  1. value: anchors (ANCHORS, raw materials) then the cheapest recipe from priced inputs (min-cost propagation over the
     recipe dump; the Alchemistry Dissolver and other "make it from nothing" recipes don't count), then type defaults.
  2. tier (Market shelf): the main-path chapter where a quest first asks for the item (Getting Started = 0, chapter I =
     1 ... VIII = 8, Seed = 9, Creation = 10; a side-page quest counts as the latest main chapter it depends on).
     Items no quest asks for take the lowest tier of any recipe that makes them (the highest tier among its inputs).
     Tier t opens when the team completes TIER_QUESTS[t] (a main-path quest), so stock opens as players progress.
  3. buy ("Everything, priced high"): ordinary items cost value x TIER_MULT; chemistry (ChemLib, MI circuits and hulls,
     rare and milestone metals, acids and petrochemicals, anything a KubeJS recipe gates) costs
     max(value x CHEM_MULT, CHEM_FLOOR) by tier; the Seed parts, energy cores and antimatter have their own floors and
     are also gated on the quest where the player first makes them.
  4. sell: half the value (a tenth for cheap renewables such as cobblestone), then lowered until no recipe can turn
     bought inputs into more coins than they cost (outputs x chance x sell <= inputs x buy), dissolver included.
Creative-only items (creative, debug, command blocks, spawn eggs...) and the old Demigod Tokens are left out.
"""
import collections
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
OUT = ROOT / "pack/config/wdmarket/prices.json"
SETTINGS = ROOT / "pack/config/wdmarket/settings.json"
OVERRIDES = ROOT / "tools/market_price_overrides.json"
DUMP = ROOT / "test/dump"

SELL = 0.5
# main path: chapter key -> Market tier; TIER_QUESTS[t] = the quest that opens tier t (tier 0 is always open)
MAIN = ["start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"]
TIER_QUESTS = [None, "gs_ready", "t0_pump", "t1_dissolver", "t1_steel", "t3_ebf", "t4_acid", "t5_hv", "t6_pu",
               "t7_nasa", "t7_seed"]
TIER_MULT = [1.0, 1.0, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0, 2.5, 3.0, 3.0]          # ordinary items
CHEM_MULT = [4, 4, 4, 5, 5, 6, 6, 8, 8, 10, 10]                              # chemistry: value x this ...
CHEM_FLOOR = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 102400]  # ... but never below this
# Seed of a New World parts (buy price floors, coins); these are also gated on their own first quest
SEED_FLOOR = [
    (r"^kubejs:seed_of_a_new_world$", 50_000_000),
    (r"^kubejs:antimatter_core$", 2_000_000),
    (r"^minecraft:dragon_egg$", 2_000_000),
    (r"antimatter", 500_000),
    (r"^kubejs:energy_core$", 250_000),
    (r"^kubejs:energy_core_empty$", 100_000),
]

# --- what counts as chemistry ("priced very high") --------------------------------------------------------------
RARE = ("platinum", "iridium", "osmium", "uranium", "uraninite", "tungsten", "fluorite", "plutonium", "thorium",
        "titanium", "rhodium", "ruthenium", "palladium", "polonium", "monazite", "neodymium", "chromium", "tantalum",
        "antimony", "beryllium", "lithium", "tritium", "deuterium", "yellowcake")
PETRO = (r"sulfuric|hydrochloric|nitric|hydrofluoric|aqua_regia|chloroplatinic|hexachloroplatinate|pgm_|_acid|acid_|"
         r"ammonia|benzene|toluene|ethylene|ethene|ethane|propene|propane|butane|butadiene|methane|acetylene|styrene|"
         r"polyethylene|polyvinyl|pvc|plastic|polymer|naphtha|crude_oil|diesel|gasoline|kerosene|lubricant|caprolactam|"
         r"nylon|epoxy|synthetic_oil|synthetic_rubber|heavy_fuel|light_fuel|cryofluid|alumina|bauxite_slurry|lye|"
         r"sodium_hydroxide|chlorine|fluorine|hydrogen|helium|argon|neon|xenon|krypton")
MI_PARTS = re.compile(r"^modern_industrialization:(.*circuit.*|.*processing_unit.*|.*_machine_hull|.*_hull|"
                      r"quantum_.*|.*_singularity|.*_upgrade)$")
CHEM_MISC = re.compile(r"(^chemlib:|^alchemistry:|^kubejs:|control_circuit|^mekanism:(pellet_|alloy_)|"
                       r"^extended_industrialization:.*circuit|^warbuckscore:)")
RARE_RE = re.compile(r"(^|[:_/])(" + "|".join(RARE) + r")($|[_/])")
PETRO_RE = re.compile(PETRO)

# --- never listed / never bought --------------------------------------------------------------------------------
NEVER = re.compile(r"(creative|debug|command_block|barrier|structure_block|structure_void|jigsaw|knowledge_book|"
                   r"^minecraft:light$|bedrock|admin|test_|_test$|dev_tool|infinity_cell|spawn_egg$|^minecraft:air$|"
                   r"^ftbquests:|^ftbfiltersystem:|^ftblibrary:|demigod_token$|^minecraft:petrified_oak_slab$|"
                   r"^minecraft:(reinforced_deepslate|end_portal_frame|budding_amethyst|spawner|trial_spawner|vault|"
                   r"farmland|dirt_path|frogspawn|chorus_plant)$|_tab_icon$|^modonomicon:|^patchouli:)")

# --- anchors (coins per item; old token shop x 100, rounded) -----------------------------------------------------
ANCHORS = {
    "minecraft:dirt": 1, "minecraft:cobblestone": 1, "minecraft:cobbled_deepslate": 1, "minecraft:stone": 1.5,
    "minecraft:deepslate": 1.5, "minecraft:netherrack": 1, "minecraft:sand": 1.5, "minecraft:red_sand": 1.5,
    "minecraft:gravel": 1.5, "minecraft:end_stone": 3, "minecraft:basalt": 1.5, "minecraft:blackstone": 1.5,
    "minecraft:tuff": 1.5, "minecraft:calcite": 2, "minecraft:granite": 1, "minecraft:diorite": 1,
    "minecraft:andesite": 1, "minecraft:soul_sand": 2, "minecraft:soul_soil": 2, "minecraft:clay_ball": 3,
    "minecraft:ice": 2, "minecraft:snowball": 1, "minecraft:obsidian": 16, "minecraft:mud": 1.5,
    "minecraft:coal": 6, "minecraft:raw_iron": 24, "minecraft:iron_ingot": 24, "minecraft:raw_copper": 8,
    "minecraft:copper_ingot": 8, "minecraft:raw_gold": 48, "minecraft:gold_ingot": 48, "minecraft:diamond": 225,
    "minecraft:emerald": 60, "minecraft:lapis_lazuli": 20, "minecraft:redstone": 10, "minecraft:quartz": 12,
    "minecraft:amethyst_shard": 30, "minecraft:glowstone_dust": 12, "minecraft:netherite_scrap": 1800,
    "minecraft:ancient_debris": 1800, "minecraft:flint": 2, "minecraft:ender_pearl": 60, "minecraft:blaze_rod": 75,
    "minecraft:ghast_tear": 150, "minecraft:slime_ball": 20, "minecraft:gunpowder": 20, "minecraft:string": 12,
    "minecraft:leather": 12, "minecraft:bone": 6, "minecraft:rotten_flesh": 2, "minecraft:spider_eye": 8,
    "minecraft:feather": 4, "minecraft:egg": 4, "minecraft:phantom_membrane": 125, "minecraft:shulker_shell": 900,
    "minecraft:nether_star": 25000, "minecraft:heart_of_the_sea": 1800, "minecraft:totem_of_undying": 2700,
    "minecraft:echo_shard": 675, "minecraft:prismarine_shard": 10, "minecraft:prismarine_crystals": 12,
    "minecraft:name_tag": 350, "minecraft:saddle": 900, "minecraft:elytra": 50000, "minecraft:dragon_breath": 2000,
    "minecraft:wither_skeleton_skull": 3000, "minecraft:golden_apple": 225, "minecraft:enchanted_golden_apple": 3600,
    "minecraft:experience_bottle": 12, "minecraft:bread": 6, "minecraft:wheat": 2, "minecraft:sugar_cane": 2,
    "minecraft:torch": 3, "minecraft:bone_meal": 3, "minecraft:ink_sac": 4, "minecraft:cocoa_beans": 3,
    "minecraft:magma_cream": 30, "minecraft:nautilus_shell": 300, "minecraft:turtle_scute": 200,
    "minecraft:armadillo_scute": 30, "minecraft:breeze_rod": 150, "minecraft:honeycomb": 8, "minecraft:rabbit_hide": 4,
    "modern_industrialization:raw_tin": 25, "modern_industrialization:tin_ingot": 25,
    "modern_industrialization:raw_lead": 25, "modern_industrialization:lead_ingot": 25,
    "modern_industrialization:raw_nickel": 30, "modern_industrialization:nickel_ingot": 30,
    "modern_industrialization:raw_silver": 40, "modern_industrialization:silver_ingot": 40,
    "modern_industrialization:bauxite_dust": 25, "modern_industrialization:salt_dust": 6,
    "modern_industrialization:raw_titanium": 90, "modern_industrialization:raw_tungsten": 100,
    "modern_industrialization:raw_antimony": 60, "modern_industrialization:raw_platinum": 400,
    "modern_industrialization:raw_iridium": 800, "modern_industrialization:raw_uranium": 150,
    "modern_industrialization:lignite_coal": 4, "modern_industrialization:coke": 12,
    "modern_industrialization:rubber_sheet": 12, "modern_industrialization:fire_clay_dust": 12,
    "mekanism:raw_osmium": 40, "mekanism:ingot_osmium": 40, "mekanism:raw_uranium": 150, "mekanism:raw_lead": 25,
    "mekanism:raw_tin": 25, "mekanism:fluorite_gem": 60, "ae2:certus_quartz_crystal": 40,
    "ars_nouveau:source_gem": 75, "waystones:warp_stone": 400,
}
# natural things by tag (an explicit ANCHORS entry wins; the first matching tag counts)
TAG_ANCHORS = [("minecraft:logs", 4), ("minecraft:saplings", 3), ("minecraft:leaves", 1), ("minecraft:small_flowers", 2),
               ("minecraft:flowers", 2), ("c:obsidians", 16), ("c:end_stones", 3), ("c:netherracks", 1),
               ("c:cobblestones", 1), ("c:stones", 1.5), ("c:sands", 1.5), ("c:gravels", 1.5), ("minecraft:dirt", 1),
               ("c:mushrooms", 3), ("minecraft:wool", 6), ("c:seeds", 2), ("c:crops", 2)]
INF = 10 ** 12
FREE_FLUIDS = {"minecraft:water", "minecraft:lava", "modern_industrialization:steam", "minecraft:flowing_water"}
FLUID_COST = 16.0  # coins per 1000 mB for any other fluid
SKIP_TYPES = re.compile(r"^(alchemistry:dissolver|botanypots:|occultism:miner|justenoughbreeding:|mekmm:planting|"
                        r"almostunified:|mekanism:mek_data|ae2:storage_cell_disassembly|silentgear:salvaging|"
                        r"justdirethings:ability|ars_nouveau:glyph|mysticalagriculture:reprocessor)")
OUT_KEY = re.compile(r"^(result|results|output|outputs|item_outputs|item_output|product|products|byproducts?|"
                     r"secondary_output|main_output)$", re.I)
CATS = ["Chemistry", "Ores & Metals", "Building Blocks", "Wood & Plants", "Farming & Food", "Mob Drops",
        "Machines & Tech", "Tools & Armor", "Magic", "Misc"]
TECH = re.compile(r"^(modern_industrialization|extended_industrialization|industrialization_overdrive|mekanism\w*|mekmm|"
                  r"appmek|appflux|ae2\w*|extendedae|advanced_ae|megacells|merequester|aeinfinitybooster|create\w*|"
                  r"copycats|powah|ironfurnaces|generatorgalore|justdirethings|integrated\w+|sophisticated\w+|pipez|"
                  r"laserio|logisticsnetworks|sfm|toms_storage|functionalstorage|fluxnetworks|computercraft|"
                  r"advancedperipherals|ad_astra\w*|compactmachines|packaged\w+|extendedcrafting|hostilenetworks|"
                  r"mininggadgets|buildinggadgets2|constructionstick|entangled|cable_facades|pylons|ironjetpacks|"
                  r"angelring|torchmaster|wdmarket|utilitarian|laboratoryblocks|alchemistry):")
MAGIC = re.compile(r"^(ars_\w+|occultism|neovitae|reliquary|relics|artifacts|apotheosis|apothic_\w+|"
                   r"mysticalagriculture|projecte|akashictome|telepastries|gateways):")


WHY = {}  # item -> id of the recipe that set its value (for --why <item>)
CUT = {}  # item -> id of the recipe that last lowered its sell price


def hexid(key):  # same as tools/build_quests.py
    n = int(hashlib.sha1(key.encode()).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF
    return f"{n:016X}"


# ------------------------------------------------------------------------------------------------ inputs
def load_registry():
    items, names = set(), {}
    for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
        p = line.split("\t")
        if len(p) >= 2 and p[1] in ("item", "block") and not line.startswith("#"):
            if p[1] == "item":
                items.add(p[0])
            if len(p) > 2 and p[2]:
                names.setdefault(p[0], p[2])
    reg = json.loads((DUMP / "registry_dump.json").read_text(encoding="utf-8"))
    tags = {t: set(v) for t, v in reg.get("item_tags", {}).items()}
    item_tags = collections.defaultdict(set)
    for t, v in tags.items():
        for i in v:
            item_tags[i].add(t)
    return items, names, tags, item_tags, set(reg.get("block", ()))


def num(v, d=1.0):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else d


class Parser:
    """Recipe JSON -> (inputs [(options, count)], fluid cost, outputs [(id, count x chance)])."""

    def __init__(self, items, tags):
        self.items, self.tags = items, tags

    def opts(self, n):
        if isinstance(n, str):
            if n.startswith("#"):
                return set(self.tags.get(n[1:], ())) & self.items
            return {n} & self.items
        if isinstance(n, list):
            out = set()
            for v in n:
                out |= self.opts(v) or set()
            return out
        if not isinstance(n, dict):
            return set()
        if "ingredient" in n:
            return self.opts(n["ingredient"])
        if isinstance(n.get("tag"), str):
            return set(self.tags.get(n["tag"], ())) & self.items
        for k in ("item", "id"):
            if isinstance(n.get(k), str):
                return {n[k]} & self.items
            if isinstance(n.get(k), dict):
                return self.opts(n[k])
        for k in ("items", "children", "values"):
            if isinstance(n.get(k), list):
                return self.opts(n[k])
        return set()

    @staticmethod
    def is_fluid(n):
        return isinstance(n, dict) and ("fluid" in n or "fluid_tag" in n or "fluidTag" in n or "chemical" in n)

    @staticmethod
    def is_ing(n):
        return isinstance(n, dict) and (isinstance(n.get("item"), (str, dict)) or isinstance(n.get("tag"), str)
                                        or "ingredient" in n or isinstance(n.get("items"), list)
                                        or isinstance(n.get("children"), list))

    def parse(self, j):
        ins, fluid = [], 0.0
        if isinstance(j.get("pattern"), list) and isinstance(j.get("key"), dict):
            counts = collections.Counter("".join(j["pattern"]))
            for ch, v in j["key"].items():
                o = self.opts(v)
                if counts.get(ch):
                    if not o:
                        return None
                    ins.append((o, counts[ch]))
        else:
            def walk(n):
                nonlocal fluid
                if isinstance(n, dict):
                    if self.is_fluid(n):
                        if "chemical" in n:  # Mekanism slurry/gas: its real inputs aren't in this recipe
                            fluid += INF
                            return
                        f = n.get("fluid") or ""
                        if not isinstance(f, str) or f not in FREE_FLUIDS:
                            fluid += num(n.get("amount"), 1000) / 1000 * FLUID_COST
                        return
                    if self.is_ing(n):
                        if num(n.get("probability"), 1) == 0:  # MI: not consumed
                            return
                        o = self.opts(n)
                        ins.append((o, num(n.get("count"), num(n.get("amount"), 1))))
                        return
                    for k, v in n.items():
                        if OUT_KEY.match(k) or k in ("type", "group", "category", "neoforge:conditions", "conditions",
                                                     "tool", "keep_held_item", "pattern"):
                            continue
                        walk(v)
                elif isinstance(n, list):
                    for v in n:
                        walk(v)
                elif isinstance(n, str) and n in self.items:
                    ins.append(({n}, 1))
            walk(j)
            if any(not o for o, _ in ins):
                return None
        outs = []

        def grab(n, chance=1.0):
            if isinstance(n, str):
                if n in self.items:
                    outs.append((n, chance))
            elif isinstance(n, list):
                for v in n:
                    grab(v, chance)
            elif isinstance(n, dict):
                ch = chance * num(n.get("chance"), num(n.get("probability"), 1))
                if "probability" in n and num(n["probability"], 1) > 1:  # alchemistry groups: percent
                    ch = chance * num(n["probability"], 100) / 100
                cnt = num(n.get("count"), num(n.get("amount"), 1)) if not self.is_fluid(n) else 0
                for k in ("id", "item"):
                    if isinstance(n.get(k), str):
                        if n[k] in self.items and cnt:
                            outs.append((n[k], cnt * ch))
                        return
                    if isinstance(n.get(k), dict):
                        inner = n[k]
                        c2 = num(inner.get("count"), cnt)
                        iid = inner.get("id") or inner.get("item")
                        if iid in self.items:
                            outs.append((iid, c2 * ch))
                        return
                for k in ("results", "groups", "output", "result"):
                    if k in n:
                        grab(n[k], ch)

        def find(n):
            if isinstance(n, dict):
                for k, v in n.items():
                    if OUT_KEY.match(k):
                        grab(v)
                    elif k not in ("type",):
                        find(v)
            elif isinstance(n, list):
                for v in n:
                    find(v)
        find(j)
        if not outs:
            return None
        return ins, fluid, outs


def load_recipes(items, tags):
    p = Parser(items, tags)
    out = []  # (rid, type, ins, fluid, outs)
    for r in json.loads((DUMP / "recipe_dump.json").read_text(encoding="utf-8"))["recipes"]:
        rid = r["id"]
        if rid.startswith("kubejs:shop/"):
            continue
        try:
            j = json.loads(r["json"])
        except ValueError:
            continue
        if not isinstance(j, dict):
            continue
        t = str(j.get("type", ""))
        parsed = p.parse(j)
        if parsed:
            out.append((rid, t, *parsed))
    return out


def carve_groups(valid):
    """Rechiseled chiseling families from the server's mod jars: [[(item, worth), ...], ...]. The chisel turns any
    member into any other for free, so they all cost what the base block costs (slabs half)."""
    import zipfile
    groups = []
    for jar in sorted((ROOT / "test/server/mods").glob("*.jar")):
        try:
            z = zipfile.ZipFile(jar)
        except (OSError, zipfile.BadZipFile):
            continue
        for n in z.namelist():
            if "/chiseling_recipes/" not in n or not n.endswith(".json"):
                continue
            try:
                d = json.loads(z.read(n))
            except ValueError:
                continue
            g = []
            for e in d.get("entries", []):
                if isinstance(e, str):
                    e = {"block": e}
                if not isinstance(e, dict):
                    continue
                sw, tw = num(e.get("slab_worth"), 0.5), num(e.get("stairs_worth"), 1.0)
                for k, v in e.items():
                    if isinstance(v, str) and v in valid:
                        g.append((v, sw if "slab" in k else tw if "stairs" in k else 1.0))
            if len(g) > 1:
                groups.append(g)
    return groups


# ------------------------------------------------------------------------------------------------ quests
def quest_info(tags):
    import quest_data as qd
    by = {c.key: c for c in qd.CHAPTERS}
    quests = {q.key: (c, q) for c in qd.CHAPTERS for q in c.quests}
    memo = {}

    def qtier(k, stack=()):
        if k in memo:
            return memo[k]
        c, q = quests[k]
        if c.key in MAIN:
            t = MAIN.index(c.key)
        elif k in stack:
            return 0
        else:
            t = max([qtier(d, stack + (k,)) for d in q.deps if d in quests] or [0])
        memo[k] = t
        return t
    first = {}  # item -> (tier, chapter order, quest key)
    order = {c.key: i for i, c in enumerate(qd.CHAPTERS)}
    for k, (c, q) in quests.items():
        for t in q.tasks:
            ids = []
            if t[0] == "item":
                ids = [t[1]]
            elif t[0] == "filter":
                ids = re.findall(r"item\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)", t[1])
                for tg in re.findall(r"item_tag\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)", t[1]):
                    ids += sorted(tags.get(tg, ()))
            for i in ids:
                key = (qtier(k), order[c.key], k)
                if i not in first or key < first[i]:
                    first[i] = key
    titles = {k: q.title for k, (c, q) in quests.items()}
    tier_names = []
    for t, ck in enumerate(MAIN):
        name = by[ck].title if ck in by else ck
        if TIER_QUESTS[t]:
            name += f" (after {titles[TIER_QUESTS[t]]})"
        tier_names.append(name)
    for k in TIER_QUESTS[1:]:
        if k not in quests or quests[k][1].optional:
            sys.exit(f"tier quest {k} is missing or optional")
    return first, titles, tier_names


# ------------------------------------------------------------------------------------------------ pricing
def main():
    items, names, tags, item_tags, blocks = load_registry()
    valid = {i for i in items if not NEVER.search(i)}
    recipes = load_recipes(items, tags)
    first, titles, tier_names = quest_info(tags)
    overrides = {}
    if OVERRIDES.exists():
        overrides = {k: float(v) for k, v in json.loads(OVERRIDES.read_text(encoding="utf-8")).get("items", {}).items()
                     if not k.startswith("_")}
    # Alchemistry's Combiner/Compactor/Fusion rebuild blocks from elements: they price ChemLib items, never the
    # blocks themselves (an oak log is worth a log, not its cellulose)
    value_recipes = [r for r in recipes if not SKIP_TYPES.match(r[1]) and r[3] < INF
                     and not (r[1].startswith("alchemistry:") and not r[4][0][0].startswith(("chemlib:", "alchemistry:")))]
    produced = {r[4][0][0] for r in value_recipes}

    def default(i):
        ts = item_tags.get(i, set())
        path = i.split(":", 1)[1]
        if any(t.startswith("c:ores") for t in ts):
            return 40.0
        if any(t.startswith(("c:ingots", "c:raw_materials")) for t in ts):
            return 32.0
        if any(t.startswith("c:gems") for t in ts):
            return 60.0
        if any(t.startswith("c:dusts") for t in ts):
            return 16.0
        if any(t in ts for t in ("c:tools", "c:armors", "minecraft:swords", "minecraft:pickaxes")):
            return 300.0
        if path.endswith("_bucket"):
            return 40.0
        if any(t in ts for t in ("minecraft:logs",)):
            return 4.0
        if any(t in ts for t in ("minecraft:saplings", "minecraft:flowers", "minecraft:leaves", "c:seeds", "c:crops")):
            return 2.0
        if "c:foods" in ts:
            return 8.0
        if i.startswith("chemlib:"):
            return 32.0
        if i in blocks:
            return 2.0
        return 16.0

    FAMILY = {"ingots": 1, "gems": 1, "dusts": 1, "raw_materials": 1, "plates": 1, "nuggets": 1 / 9,
              "storage_blocks": 9, "gears": 4, "rods": 0.5}

    def values(base, rset=None, floors=None):
        """Min-cost propagation from `base` (fixed prices) over `rset` (default: every value recipe).
        Returns (val, soft, fixed)."""
        rset = value_recipes if rset is None else rset
        val = dict(base)
        fixed = set(base)
        floor = {i: v * 0.5 for i, v in (floors or {}).items()}
        # natural things (nothing in this pack makes them) get a type default. Defaults are "soft": a recipe input
        # slot uses them only when no option in it has a real price (a unified-away mekanism:block_steel must not
        # make steel cost 2/9 of a coin), and a value built on a guess stays a guess that a real price replaces.
        soft = set()
        for i in valid:
            if i not in val and i not in produced:
                val[i] = default(i)
                soft.add(i)

        def slot(o):
            hard = [val[x] for x in o if x in val and x not in soft]
            if hard:
                return min(hard)
            vs = [val[x] for x in o if x in val]
            return min(vs) if vs else None

        def propagate(passes=40):
            for _ in range(passes):
                changed = 0
                for rid, t, ins, fluid, outs in rset:
                    oid, n = outs[0]
                    if oid in fixed or oid not in valid or n <= 0:
                        continue
                    cost = fluid + (0 if t in ("minecraft:crafting_shaped", "minecraft:crafting_shapeless") else 0.25)
                    guess = False
                    for o, c in ins:
                        v = slot(o)
                        if v is None:
                            break
                        guess |= all(x in soft for x in o if x in val)
                        cost += v * c
                    else:
                        v = cost / n
                        if v <= 0:
                            continue
                        # dupe loops (4 sand -> 4 sandstone -> 8 sand; chests sawn back into more planks) would
                        # shrink a value forever: nothing drops below half of the first price it got
                        v = max(v, floor.setdefault(oid, v * 0.5))
                        if oid not in val:
                            take = True
                        elif oid in soft:  # a real price replaces a guess; a guess only lowers a guess
                            take = not guess or v < val[oid] * 0.9999
                        else:  # never lower a real price with a guess
                            take = not guess and v < val[oid] * 0.9999
                        if take and v != val.get(oid):
                            val[oid] = v
                            (soft.add if guess else soft.discard)(oid)
                            WHY[oid] = rid
                            changed += 1
                if not changed:
                    break
        propagate()
        for i in valid:  # loops nothing reached: type default, then propagate again (cheaper recipes win)
            if i not in val:
                val[i] = default(i)
                soft.add(i)
        propagate()
        return val, soft, fixed

    anchors = {i: float(v) for i, v in ANCHORS.items() if i in valid}
    for tg, v in TAG_ANCHORS:
        for i in sorted(tags.get(tg, ())):
            if i in valid and i not in anchors:
                anchors[i] = float(v)
    val, soft, fixed = values(anchors)
    # metal and gem families (as ATM10's market does): dust, raw, plate = the ingot or gem, nugget 1/9, block 9x,
    # gear 4x, rod 1/2. Then everything else is priced again from the fixed families.
    fam = collections.defaultdict(dict)
    for i in valid:
        for t in item_tags.get(i, ()):
            m = re.match(r"c:(\w+)/([a-z0-9_]+)$", t)
            if m and m.group(1) in FAMILY and not t.startswith("c:raw_materials/dyes"):
                fam[m.group(2)][i] = m.group(1)
    carve = carve_groups(valid)
    # round 1 fixes the families of anchored metals (iron, copper, tin...); round 2 also those of alloys and other
    # metals (bronze, steel...), priced in round 1 from their cheapest recipe with round 1's families fixed.
    for _round in (1, 2):
        base = dict(anchors)
        for name, members in fam.items():
            heads = [i for i, k in members.items() if k in ("ingots", "gems")]
            anch = [anchors[i] for i in heads if i in anchors]
            if not heads or (_round == 1 and not anch):
                continue
            v = anch[0] if anch else min(val[i] for i in heads)
            for i, k in members.items():
                if i not in anchors:
                    base[i] = v * FAMILY[k]
        if _round == 2:  # chiseled variants cost what their base block costs (a priced vanilla member first)
            for g in carve:
                priced = sorted((0 if it.startswith("minecraft:") else 1, val[it] / w, it) for it, w in g
                                if w > 0 and it in val and it not in soft)
                if priced:
                    unit = priced[0][1]
                    for it, w in g:
                        if it not in anchors:
                            base[it] = unit * w
        WHY.clear()
        # first the plain vanilla-style recipes (crafting, smelting, stonecutting, smithing): their prices are the
        # floors (half) for the full pass, so machine dupe loops (MI assembler: 8 planks -> 2 chests, sawn back into
        # 16 planks) can't drive a price to nothing
        plain, _s, _f = values(base, [r for r in value_recipes if r[1].startswith("minecraft:")])
        WHY.clear()
        val, soft, fixed = values(base, floors={i: v for i, v in plain.items() if i not in _s})
    # tiers
    tier = {}
    for i in valid:
        if i in first:
            tier[i] = first[i][0]
    seeded = set(tier)
    for i in valid:
        if i not in tier:
            tier[i] = 0 if i not in produced else 99
    for _ in range(40):
        changed = 0
        for rid, t, ins, fluid, outs in recipes:
            for oid, _n in outs[:1]:
                if oid not in tier or oid in seeded:
                    continue
                mt = 0
                for o, c in ins:
                    ts = [tier.get(x, 0) for x in o]
                    mt = max(mt, min(ts) if ts else 99)
                if mt < tier[oid]:
                    tier[oid] = mt
                    changed += 1
        if not changed:
            break
    for i in tier:
        if tier[i] >= 99:
            tier[i] = 0

    # chemistry classes
    kubejs_gated = {o for rid, t, ins, fluid, outs in recipes if rid.startswith("kubejs:")
                    and not rid.startswith(("kubejs:dissolver", "kubejs:shop")) for o, _ in outs[:1]}

    def chem_kind(i):
        for rx, floor in SEED_FLOOR:
            if re.search(rx, i):
                return "seed", floor
        path = i.split(":", 1)[1]
        if CHEM_MISC.search(i) or MI_PARTS.match(i) or RARE_RE.search(path) or PETRO_RE.search(path):
            return "chem", 0
        if i in kubejs_gated:
            return "chem", 0
        return None, 0

    def category(i, kind):
        if kind:
            return "Chemistry"
        ts = item_tags.get(i, set())
        if any(re.match(r"c:(ingots|gems|dusts|nuggets|raw_materials|ores|storage_blocks|plates|gears|rods)(/|$)", t)
               and not t.startswith("c:raw_materials/dyes") for t in ts):
            return "Ores & Metals"
        if any(t in ts for t in ("c:tools", "c:armors", "minecraft:swords", "minecraft:axes", "minecraft:pickaxes",
                                 "minecraft:shovels", "minecraft:hoes")):
            return "Tools & Armor"
        if any(t in ts for t in ("c:foods", "c:crops", "c:seeds")):
            return "Farming & Food"
        if any(t in ts for t in ("minecraft:logs", "minecraft:planks", "minecraft:saplings", "minecraft:leaves",
                                 "minecraft:flowers", "c:mushrooms")):
            return "Wood & Plants"
        if any(t in ts for t in ("c:bones", "c:strings", "c:gunpowders", "c:slime_balls", "c:leathers", "c:feathers",
                                 "c:ender_pearls", "c:rods/blaze", "c:eggs")):
            return "Mob Drops"
        if MAGIC.match(i):
            return "Magic"
        if TECH.match(i):
            return "Machines & Tech"
        if i in blocks:
            return "Building Blocks"
        return "Misc"

    # chemistry no quest asks for directly takes the tier of its family: the same element or rare metal asked for
    # elsewhere (chemlib:iridium_dust follows modern_industrialization:iridium_ingot), and never below the Dissolver
    def family(i):
        path = i.split(":", 1)[1]
        m = RARE_RE.search(path)
        if m:
            return m.group(2)
        if i.startswith("chemlib:"):
            return re.sub(r"_(dust|ingot|nugget|plate|metal_block|bucket|lamp_block)$", "", path)
        return None
    fam_tier = {"iridium": 7, "palladium": 7, "rhodium": 7, "ruthenium": 7}  # the PGM line (chapter VII), if unasked
    fam_seen = set()
    for i in sorted(seeded):
        if i.startswith(("mysticalagriculture:", "botanypots:")) or any(t.startswith("c:ores") for t in item_tags.get(i, ())):
            continue  # an ore hoard or a (blocked) resource seed says nothing about when the metal itself arrives
        f = family(i)
        if f:
            fam_tier[f] = min(fam_tier.get(f, 99) if f in fam_seen else 99, tier[i])
            fam_seen.add(f)
    for i in valid:
        if i in seeded or not chem_kind(i)[0]:
            continue
        f = family(i)
        if f in fam_tier:
            tier[i] = max(tier[i], fam_tier[f])
        if i.startswith("chemlib:"):
            tier[i] = max(tier[i], TIER_QUESTS.index("t1_dissolver"))  # elements begin with the Dissolver

    buy, sell, kinds, gates = {}, {}, {}, {}
    for i in valid:
        v, t = val[i], tier[i]
        kind, floor = chem_kind(i)
        kinds[i] = kind
        if kind == "seed":
            b = max(v * CHEM_MULT[t], floor)
            if i in first:
                gates[i] = first[i][2]
        elif kind == "chem":
            b = max(v * CHEM_MULT[t], CHEM_FLOOR[t])
        else:
            b = v * TIER_MULT[t]
        if i in overrides:
            b = overrides[i]
        buy[i] = b
        sell[i] = v * (SELL if v > 2 else 0.1)
        sell[i] = min(sell[i], b * 0.9)

    # ore blocks are priced by what they process into: their buy price is a guess the anti-arbitrage pass raises
    soft |= {i for i in valid if any(t.startswith("c:ores") for t in item_tags.get(i, ())) and i not in overrides}
    # anti-arbitrage: no recipe turns bought inputs into more sale coins than they cost. When the cheapest input is
    # only a guessed price (loot-only gear such as diamond horse armour salvaged into diamonds), that input's buy price
    # goes up; otherwise the outputs' sell prices come down. Weighted outputs (sequenced assembly) are averaged.
    arb = []
    for rid, t, ins, fluid, outs in recipes:
        if t.startswith(("create:sequenced_assembly", "reliquary:alkahestry")):
            continue
        given = set().union(*[o for o, c in ins]) if ins else set()
        outs = [(o, n) for o, n in outs if o not in given]  # tools and catalysts handed back
        if outs:
            arb.append((rid, t, ins, fluid, outs))
    for _ in range(30):
        hit = 0
        for rid, t, ins, fluid, outs in arb:
            cost, cheap = fluid, []
            for o, c in ins:
                bs = [(buy[x], x) for x in o if x in buy]
                if not bs:
                    cost = INF
                    break
                b, x = min(bs)
                cost += b * c
                cheap.append((x, c, b))
            if cost >= INF:
                continue
            got = sum(n * sell.get(o, 0) for o, n in outs)
            if got > cost * 1.0001 and got > 0:
                guessed = [(x, c, b) for x, c, b in cheap if x in soft and x not in overrides]
                if guessed:
                    extra = (got - cost) * 1.001
                    share = sum(c * b for x, c, b in guessed) or 1
                    for x, c, b in guessed:
                        buy[x] = b + extra * (c * b / share) / c
                        CUT[x] = "buy raised by " + rid
                else:
                    f = cost / got * 0.999
                    for o, n in outs:
                        if o in sell:
                            sell[o] *= f
                            CUT[o] = rid
                hit += 1
        if not hit:
            break

    rows = []
    for i in sorted(valid):
        b, s = buy[i], sell[i]
        fmt = lambda x: round(x, 2) if x < 100 else round(x)
        g = gates.get(i)
        rows.append([i, names.get(i) or i.split(":", 1)[1].replace("_", " ").title(), fmt(b), fmt(s), tier[i],
                     CATS.index(category(i, kinds[i])), 1, hexid("quest:" + g) if g else "", titles[g] if g else ""])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = {"sell": SELL, "fields": ["id", "name", "buy", "sell", "tier", "category", "buyable", "gate", "gate_title"],
            "categories": CATS, "items": rows}
    OUT.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    # settings.json: tier names and the quests that open them (everything else is hand-tuned in that file)
    s = json.loads(SETTINGS.read_text(encoding="utf-8")) if SETTINGS.exists() else {}
    s["_tiers"] = ("Market tiers = the Demigod's Path chapters: tier_names[0] is always open; tier t opens when the "
                   "team completes the main-path quest tier_quests[t-1] (written by tools/build_market_prices.py)")
    s["tier_names"] = tier_names
    s["tier_quests"] = [hexid("quest:" + k) for k in TIER_QUESTS[1:]]
    SETTINGS.write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    if "--why" in sys.argv:  # explain a value: the chain of recipes behind it
        for i in sys.argv[sys.argv.index("--why") + 1:]:
            seen = set()
            while i and i not in seen:
                seen.add(i)
                rid = WHY.get(i)
                print(f"  {i} = {val.get(i, 0):.3f}  via {rid or ('anchor' if i in fixed else 'default')}"
                      f"  (buy {buy.get(i, 0):.2f}, sell {sell.get(i, 0):.2f}, sell cut by {CUT.get(i)})")
                r = next((r for r in value_recipes if r[0] == rid), None)
                if not r:
                    break
                for o, c in r[2]:
                    x = min((x for x in o if x in val), key=lambda x: val[x], default=None)
                    print(f"      {c} x {x} = {val.get(x, 0):.3f}{' (guess)' if x in soft else ''}")
                i = max((min((x for x in o if x in val), key=lambda x: val[x]) for o, c in r[2] if o & set(val)),
                        key=lambda x: val[x] * 0 - 0, default=None) if False else min(
                    (min((x for x in o if x in val), key=lambda x: val[x]) for o, c in r[2] if o & set(val)),
                    key=lambda x: val[x], default=None)
        return
    c = collections.Counter
    print(f"prices.json: {len(rows)} items, {len(recipes)} recipes read, {sum(1 for r in rows if r[7])} quest-gated")
    print("by tier:", dict(sorted(c(r[4] for r in rows).items())))
    print("by category:", {CATS[k]: n for k, n in sorted(c(r[5] for r in rows).items())})
    print("chemistry:", sum(1 for k in kinds.values() if k), " skipped (creative/never):", len(items - valid))
    for i in ["minecraft:cobblestone", "minecraft:iron_ingot", "minecraft:diamond", "modern_industrialization:bronze_ingot",
              "modern_industrialization:steel_ingot", "modern_industrialization:analog_circuit",
              "modern_industrialization:electronic_circuit", "modern_industrialization:digital_circuit",
              "modern_industrialization:processing_unit", "modern_industrialization:sulfuric_acid_bucket",
              "modern_industrialization:platinum_ingot", "modern_industrialization:iridium_ingot", "chemlib:hydrogen",
              "chemlib:oganesson", "kubejs:energy_core", "kubejs:antimatter_core", "kubejs:seed_of_a_new_world",
              "mekanism:ultimate_control_circuit", "minecraft:nether_star"]:
        r = next((x for x in rows if x[0] == i), None)
        if r:
            print(f"  {i:48s} buy {r[2]:>11,} sell {r[3]:>9,}  tier {r[4]:>2}  {CATS[r[5]]}"
                  + (f"  gate: {r[8]}" if r[7] else ""))


if __name__ == "__main__":
    main()
