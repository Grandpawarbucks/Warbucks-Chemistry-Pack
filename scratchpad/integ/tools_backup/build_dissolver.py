#!/usr/bin/env python3
"""Generate Alchemistry Dissolver recipes for block items that have none (stdlib only).

Goal (CLAUDE.md "Disassembly"): the Dissolver should break any sensible block into ChemLib
elements/compounds. Alchemistry only covers vanilla blocks, so modded woods, stones, sands, glass,
wool, leaves, etc. get a recipe COPIED from the closest vanilla analog that Alchemistry already
dissolves. No new chemistry is invented: every output comes from an existing Alchemistry recipe,
scaled down (never up) for partial blocks like slabs.

Inputs (run test/smoke.sh and test/build_id_index.py first so these are current):
  test/server/mods/*.jar           recipes + item tags + item models of every mod
  vanilla client jar (Prism cache) vanilla tags + item models
  NeoForge universal jar           c: tags
  test/ids.tsv                     every block id in the pack (type "block")

Outputs:
  pack/kubejs/data/warbucks/recipe/dissolver/<namespace>/<path>.json  (folder wiped on each run)
  docs/dissolver-coverage.md       what was generated, and what was left out and why

Balance rules (see CLAUDE.md, ProjectE lite): no recipes for ores, raw-ore blocks, storage blocks,
machines/tech blocks, creative/technical blocks or ProjectE. Metals only come out of a generated
recipe when the vanilla analog (e.g. stone, deepslate) already gives them in Alchemistry.
The loader script skips any item that no longer exists, so a block without an item is skipped
silently instead of breaking recipe loading.

Run: python3 tools/build_dissolver.py   (then test/smoke.sh)
"""
import collections
import glob
import json
import pathlib
import re
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODS = ROOT / "test/server/mods"
IDS = ROOT / "test/ids.tsv"
VANILLA = pathlib.Path.home() / "Library/Application Support/PrismLauncher/libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
OUT = ROOT / "pack/kubejs/data/warbucks/recipe/dissolver"   # old per-file output (removed on each run)
TABLE = ROOT / "pack/kubejs/config/dissolver_recipes.json"   # one file, loaded by server_scripts/dissolver_generated.js
DOC = ROOT / "docs/dissolver-coverage.md"
KUBEJS = ROOT / "pack/kubejs"


def jars():
    out = sorted(MODS.glob("*.jar"))
    out += sorted((ROOT / "test/server/libraries/net/neoforged/neoforge").glob("*/neoforge-*-universal.jar"))
    if VANILLA.exists():
        out.append(VANILLA)
    else:
        sys.exit(f"vanilla jar not found: {VANILLA}")
    return out


def load_json(z, name):
    try:
        return json.loads(z.read(name).decode("utf-8", "replace"))
    except (ValueError, KeyError):
        return None


# ----------------------------------------------------------------------------- scanning
TAG_RX = re.compile(r"data/([^/]+)/tags/(item|block)/(.+)\.json$")
MODEL_RX = re.compile(r"assets/([^/]+)/models/item/(.+)\.json$")
RECIPE_RX = re.compile(r"data/([^/]+)/recipe/(.+)\.json$")


def scan():
    tags = collections.defaultdict(set)      # (kind, tag) -> raw entries (ids or #tags)
    models = set()                           # item ids that have an item model
    recipes = []                             # (source, recipe json)
    for jar in jars():
        try:
            z = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            continue
        for name in z.namelist():
            if not name.endswith(".json"):
                continue
            m = TAG_RX.match(name)
            if m:
                d = load_json(z, name)
                if isinstance(d, dict):
                    for v in d.get("values", []):
                        if isinstance(v, dict):
                            v = v.get("id")
                        if isinstance(v, str):
                            tags[(m.group(2), f"{m.group(1)}:{m.group(3)}")].add(v)
                continue
            m = MODEL_RX.match(name)
            if m:
                models.add(f"{m.group(1)}:{m.group(2)}")
                continue
            m = RECIPE_RX.match(name)
            if m:
                raw = z.read(name)
                if b"alchemistry:dissolver" not in raw:
                    continue
                d = load_json(z, name)
                if isinstance(d, dict) and d.get("type") == "alchemistry:dissolver":
                    recipes.append((f"{jar.name}:{name}", d))
    # pack/kubejs/data recipes that are not ours
    for p in (KUBEJS / "data").glob("*/recipe/**/*.json"):
        if OUT in p.parents:
            continue
        d = json.loads(p.read_text())
        if d.get("type") == "alchemistry:dissolver":
            recipes.append((str(p.relative_to(ROOT)), d))
    return tags, models, recipes


def resolver(tags, kind):
    """Return resolve(tag) -> set of ids, following nested #tag references."""
    cache = {}

    def resolve(tag, stack=()):
        if tag in cache:
            return cache[tag]
        if tag in stack:
            return set()
        items = set()
        for v in tags.get((kind, tag), ()):
            if v.startswith("#"):
                items |= resolve(v[1:], stack + (tag,))
            else:
                items.add(v)
        cache[tag] = items
        return items
    return resolve




# ----------------------------------------------------------------------------- policy
# Whole namespaces that are machines/tech/magic-tech: their blocks contain metals, circuits or
# processed materials, so a copied "analog" would either dupe metals or misrepresent them.
TECH_NAMESPACES = {
    "modern_industrialization", "extended_industrialization", "industrialization_overdrive",
    "mekanism", "mekmm", "mekanism_extras", "mekanismgenerators", "mekanismtools",
    "ae2", "extendedae", "advanced_ae", "megacells", "appflux", "appmek", "merequester",
    "ae2importexportcard", "aeinfinitybooster", "powah", "integrateddynamics", "integratedcrafting",
    "integratedterminals", "integratedtunnels", "sfm", "toms_storage", "functionalstorage",
    "sophisticatedstorage", "sophisticatedbackpacks", "packagedauto", "packagedexcrafting",
    "extendedcrafting", "generatorgalore", "ironfurnaces", "justdirethings", "mysticalagriculture",
    "computercraft", "advancedperipherals", "create_new_age", "createaddition",
    "create_enchantment_industry", "alchemistry", "chemlib", "botanypots", "waystones",
    "compactmachines", "ftbquests", "titanium", "fluxnetworks", "laserio", "pipez",
    "logisticsnetworks", "hostilenetworks", "mininggadgets", "buildinggadgets2", "pylons",
    "ironjetpacks", "angelring", "entangled", "cable_facades", "torchmaster", "silentgear",
    "apothic_spawners", "gateways", "lootr",
    "framedblocks", "copycats",  # camouflage frames: the look comes from a separate block
}
# Magic mods: their wood sets (archwood, ...) follow the item tags, nothing else is guessed.
TAG_ONLY_NAMESPACES = {"occultism", "ars_nouveau", "ars_additions", "ars_elemental", "reliquary",
                       "relics", "artifacts", "tombstone", "telepastries"}
SKIP_NAMESPACES = {"projecte": "ProjectE (ProjectE lite: no EMC-adjacent shortcuts)"}

# A word in the id means the block is (or is made of) a metal or metal alloy.
METAL_NAMES = {
    "iron", "gold", "golden", "copper", "netherite", "zinc", "brass", "tin", "lead", "silver",
    "nickel", "aluminum", "aluminium", "steel", "bronze", "osmium", "uranium", "platinum",
    "titanium", "tungsten", "chrome", "chromium", "electrum", "invar", "cupronickel", "kanthal",
    "desh", "ostrum", "calorite", "etrium", "cloggrum", "froststeel", "utherium", "regalium",
    "forgotten", "cobalt", "knightmetal", "ironwood", "fiery", "steeleaf",
}
METAL_WORDS = METAL_NAMES | {
    "metal", "metallic", "chain", "anvil", "bell", "rail", "industrial", "plating", "plateblock", "sheet", "hull",
    "bars", "lantern", "cage", "pipe", "machine", "casing", "alloy",
}
# Words for creative/technical/structure blocks.
TECH_WORDS = {
    "creative", "spawner", "barrier", "command", "structure", "jigsaw", "debug", "test",
    "portal", "boss", "trophy", "infested", "budding", "reinforced", "void",
    "unbreakable", "force", "field", "locked", "vanishing", "miniature",
}
TECH_IDS = {"minecraft:light", "minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
# Reference recipes that hand out metals because the input IS a metal item. Never used as analog.
METAL_REF_RX = re.compile(r"(iron|gold|copper|netherite|chain|anvil|bell|debris|raw_|_ingot|_nugget|horse_armor|gilded)")

# Remainder words allowed around a base material. "vanilla" words keep the base's ratio
# (stairs/walls 1:1, slabs 1:2); "decor" words come from decoration mods whose crafting ratio is
# not standardised, so those recipes give half the base output (never more than the input cost).
VANILLA_WORDS = {
    "stairs": 1.0, "stair": 1.0, "slab": 0.5, "wall": 1.0, "polished": 1.0, "cut": 1.0,
    "chiseled": 1.0, "smooth": 1.0, "cracked": 1.0, "mossy": 1.0, "bricks": 1.0, "brick": 1.0,
    "tiles": 1.0, "tile": 1.0, "pillar": 1.0, "carved": 1.0, "cobbled": 1.0, "block": 1.0,
    "stripped": 1.0, "log": 1.0, "wood": 1.0, "stem": 1.0, "hyphae": 1.0, "planks": 1.0,
    "plank": 1.0, "button": 1.0, "pressure": 1.0, "plate": 1.0, "fence": 0.5, "gate": 0.5,
    "door": 1.0, "trapdoor": 1.0, "sign": 1.0, "hanging": 1.0, "vertical": 1.0, "small": 1.0,
    "layered": 1.0, "tiled": 1.0,
}
# Dimension-stone qualifiers (Ad Astra): "mars_cobblestone" is cobblestone from Mars.
STONE_QUALIFIERS = {"mars", "moon", "venus", "mercury", "glacio"}
STONE_REFS = {"minecraft:stone", "minecraft:cobblestone", "minecraft:sandstone", "minecraft:sand"}
DECOR_WORDS = {
    # roofs (mcwroofs), paths (mcwpaths), windows/walls (mcwwindows), stairs/fences (mcw*)
    "roof", "attic", "steep", "upper", "lower", "top", "path", "paving", "flagstone", "running",
    "bond", "honeycomb", "windmill", "weave", "crystal", "floor", "diamond", "basket", "square",
    "dumble", "clover", "strewn", "parapet", "arrow", "slit", "gothic", "railing", "balcony",
    "banister", "platform", "bulk", "skyline", "loft", "compact", "terrace", "pier", "bridge",
    "rope", "log_bridge", "middle", "end", "stair_rail", "rail_fence", "picket", "modern",
    "wired", "highley", "pyramid", "grass_topped", "horse", "curved", "railing_gate", "rails",
    "bamboo",  # mcwfences bamboo-style
    # furniture (mcwfurnitures, handcrafted)
    "chair", "table", "bench", "desk", "drawer", "wardrobe", "cabinet", "counter", "cupboard",
    "shelf", "couch", "stool", "coffee", "end_table", "dining", "kitchen", "double", "triple",
    "covered", "nightstand", "side", "corner", "trim", "pot", "pillar_trim", "crate", "board",
    "beam", "beams", "support", "column", "post", "frame", "hollow", "horizontal", "climbable",
    # rechiseled-style patterns and generic decoration words
    "pattern", "bordered", "decorated", "dotted", "wavy", "rotated", "squares", "diagonal",
    "flooring", "inlay", "mosaic", "panel", "ornate", "fancy", "shingles", "shingle", "siding",
    "lined", "framed", "engraved", "glyphed", "etched", "runic", "rune", "patterned", "checkered",
    "herringbone", "slanted", "mixed", "stacked", "detailed", "carving", "big", "bold", "tiny",
    "four", "x", "plain", "classic", "simple", "rough", "worn", "weathered", "old",
    "large", "short", "long", "tall",
}
DECOR_FACTOR = 0.5
# Words that put a second, non-trivial material into the block (glass, light, books, cloth...).
# Such blocks are left uncovered rather than guessed.
FOREIGN_WORDS = {
    "glass", "window", "window2", "lamp", "lantern", "torch", "candle", "bookshelf", "book",
    "bed", "banner", "carpet", "cushion", "chaise", "curtain", "blinds", "sink", "oven", "stove",
    "fridge", "furnace", "chest", "barrel", "jar", "cake", "flag", "sofa", "awning", "mailbox",
    "postbox", "toolbox", "lever", "redstone", "hopper", "dispenser", "dropper", "piston",
    "glowing", "glow", "neon", "screen", "indicating", "sail", "seat",
}

# Item tags whose members are reliably made of one material -> (reference recipe, factor, rule).
TAG_RULES = [
    ("minecraft:wooden_stairs", "#minecraft:planks", 1.0, "tag: wooden stairs -> planks"),
    ("minecraft:wooden_doors", "#minecraft:planks", 1.0, "tag: wooden doors -> planks"),
    ("minecraft:wooden_trapdoors", "#minecraft:planks", 1.0, "tag: wooden trapdoors -> planks"),
    ("minecraft:wooden_buttons", "#minecraft:planks", 1.0, "tag: wooden buttons -> planks"),
    ("minecraft:wooden_pressure_plates", "#minecraft:planks", 1.0, "tag: wooden pressure plates -> planks"),
    ("minecraft:signs", "#minecraft:planks", 1.0, "tag: signs -> planks"),
    ("minecraft:hanging_signs", "#minecraft:planks", 1.0, "tag: hanging signs -> planks"),
    ("minecraft:wooden_fences", "#c:fences/wooden", 1.0, "tag: wooden fences"),
    ("c:fences/wooden", "#c:fences/wooden", 1.0, "tag: wooden fences"),
    ("c:fence_gates/wooden", "#c:fence_gates/wooden", 1.0, "tag: wooden fence gates"),
    ("c:chests/wooden", "#c:chests/wooden", 1.0, "tag: wooden chests"),
    ("c:barrels/wooden", "#c:chests/wooden", 1.0, "tag: wooden barrels -> wooden chest"),
    ("minecraft:logs", "#minecraft:logs", 1.0, "tag: logs"),
    ("minecraft:planks", "#minecraft:planks", 1.0, "tag: planks"),
    ("minecraft:wooden_slabs", "#minecraft:wooden_slabs", 1.0, "tag: wooden slabs"),
    ("minecraft:leaves", "#minecraft:leaves", 1.0, "tag: leaves"),
    ("minecraft:saplings", "#minecraft:saplings", 1.0, "tag: saplings"),
    ("minecraft:wool", "#minecraft:wool", 1.0, "tag: wool"),
    ("minecraft:wool_carpets", "#minecraft:carpets", 1.0, "tag: carpets (Alchemistry's own #minecraft:carpets recipe is empty on 1.21)"),
    ("c:glass_blocks", "#c:glass", 1.0, "tag: glass blocks (Alchemistry's own #c:glass recipe is empty on 1.21)"),
    ("c:glass_panes", "#c:glass", 0.375, "tag: glass panes -> glass x3/8"),
    ("c:sandstone/slabs", "minecraft:sandstone_slab", 1.0, "tag: sandstone slabs"),
    ("c:sandstone/stairs", "minecraft:sandstone", 1.0, "tag: sandstone stairs -> sandstone"),
    ("c:sandstone/blocks", "minecraft:sandstone", 1.0, "tag: sandstone"),
    ("minecraft:sand", "minecraft:sand", 1.0, "tag: sand"),
    ("c:sands", "minecraft:sand", 1.0, "tag: sand"),
    ("c:gravels", "minecraft:gravel", 1.0, "tag: gravel"),
    ("c:cobblestones", "minecraft:cobblestone", 1.0, "tag: cobblestone"),
    ("c:obsidians", "minecraft:obsidian", 1.0, "tag: obsidian"),
    ("c:stones", "minecraft:stone", 1.0, "tag: stone"),
    ("minecraft:stone_bricks", "minecraft:stone_bricks", 1.0, "tag: stone bricks"),
    ("minecraft:terracotta", "minecraft:terracotta", 1.0, "tag: terracotta"),
    ("c:glazed_terracottas", "minecraft:black_glazed_terracotta", 1.0, "tag: glazed terracotta"),
    ("c:concretes", "minecraft:white_concrete", 1.0, "tag: concrete"),
    ("c:concrete_powders", "minecraft:white_concrete_powder", 1.0, "tag: concrete powder"),
    ("minecraft:dirt", "#minecraft:dirt", 1.0, "tag: dirt"),
    ("c:mushrooms", "minecraft:brown_mushroom", 1.0, "tag: mushrooms -> brown mushroom"),
    ("minecraft:small_flowers", "minecraft:short_grass", 1.0, "tag: flowers -> short grass (plant matter)"),
    ("minecraft:flowers", "minecraft:short_grass", 1.0, "tag: flowers -> short grass (plant matter)"),
    ("c:netherracks", "minecraft:netherrack", 1.0, "tag: netherrack"),
    ("c:end_stones", "minecraft:end_stone", 1.0, "tag: end stone"),
]
# Block tags that mark natural stone (dimension stones, Create's stones, ...).
STONE_BLOCK_TAGS = ["c:stones", "minecraft:base_stone_overworld", "minecraft:stone_ore_replaceables",
                    "minecraft:dripstone_replaceable_blocks"]
DEEPSLATE_BLOCK_TAGS = ["minecraft:deepslate_ore_replaceables"]
PLANT_BLOCK_TAGS = ["minecraft:replaceable_by_trees"]   # grasses, ferns, vines, bushes
PLANT_DENY_WORDS = {"redstone", "firefly", "hair", "webbing", "web"}  # not plant matter

# Gem/mineral storage blocks with large outputs (diamond block = 1152 graphite). Only exact
# vanilla shapes and Rechiseled's 1:1 chisel variants may copy them.
VALUABLE_REFS = {
    "minecraft:diamond_block", "minecraft:emerald_block", "minecraft:lapis_block",
    "minecraft:redstone_block", "minecraft:coal_block", "minecraft:amethyst_block",
    "minecraft:glowstone", "minecraft:quartz", "minecraft:quartz_bricks", "minecraft:smooth_quartz",
    "minecraft:quartz_pillar", "minecraft:chiseled_quartz_block", "#c:storage_blocks/quartz",
}
VALUABLE_OK_NAMESPACES = {"minecraft", "rechiseled"}
# Alchemistry's #c:storage_blocks/<x> recipes that are not metals (all others are metal/element blocks).
NONMETAL_STORAGE = {"quartz", "apple", "bamboo", "beetroot", "carrot", "charcoal", "gunpowder",
                    "potato", "sugar_cane"}
STONE_REPLACEABLES_RX = re.compile(r"^ad_astra:[a-z]+_stone_replaceables$")


# ----------------------------------------------------------------------------- recipe helpers
AIR = {"count": 0, "item": "minecraft:air"}


def is_air(group):
    return all(r.get("item") == "minecraft:air" for r in group["results"])


def rnd(x):
    return round(x, 4)


def scale_output(output, f):
    """Scale a dissolver output by f (<= 1) without changing its chemistry."""
    out = json.loads(json.dumps(output))
    if f >= 0.9999:
        return out
    groups = out["groups"]
    if out.get("weighted"):
        # One group is picked per roll, by weight. Scale the chance of a real result by adding air.
        n = sum(g["probability"] for g in groups if not is_air(g))
        w = sum(g["probability"] for g in groups)
        air = w / f - n
        rest = [g for g in groups if not is_air(g)]
        out["groups"] = [{"probability": rnd(air), "results": [dict(AIR)]}] + rest
        return out
    # Unweighted: each group fires independently with chance probability/100 (after a gate of
    # total/100). If every real group is certain and counts halve cleanly, scale the counts
    # (as Alchemistry does for brick_slab); otherwise scale chances and keep the total.
    real = [g for g in groups if not is_air(g)]
    total = sum(g["probability"] for g in groups)
    if all(g["probability"] >= 100 for g in real) and all(
            (r.get("count", 1) * f).is_integer() and r.get("count", 1) * f >= 1
            for g in real for r in g["results"]):
        for g in real:
            for r in g["results"]:
                r["count"] = int(r.get("count", 1) * f)
        return out
    new_real = []
    for g in real:
        g = dict(g)
        g["probability"] = rnd(g["probability"] * f)
        new_real.append(g)
    air = total - sum(g["probability"] for g in new_real)
    out["groups"] = new_real + ([{"probability": rnd(air), "results": [dict(AIR)]}] if air > 0.0001 else [])
    return out


def recipe_json(item, output):
    return {
        "neoforge:conditions": [{"type": "neoforge:item_exists", "item": item}],
        "type": "alchemistry:dissolver",
        "group": "alchemistry:dissolver",
        "input": {"ingredient": {"item": item}},
        "output": output,
    }


def condition_ok(cond, item_tags):
    t = cond.get("type")
    if t == "neoforge:not":
        return not condition_ok(cond["value"], item_tags)
    if t == "neoforge:tag_empty":
        return not item_tags(cond["tag"])
    if t == "neoforge:and":
        return all(condition_ok(c, item_tags) for c in cond["values"])
    if t == "neoforge:or":
        return any(condition_ok(c, item_tags) for c in cond["values"])
    return True  # mod_loaded / item_exists: everything here is loaded


# ----------------------------------------------------------------------------- main
def main():
    tags, models, recipes = scan()
    item_tags = resolver(tags, "item")
    block_tags = resolver(tags, "block")

    # Existing recipes: reference outputs and coverage.
    refs = {}                     # "ns:item" or "#tag" -> output
    covered = {}                  # item -> ref key that covers it
    dead_tags = []
    for src, d in recipes:
        if not all(condition_ok(c, item_tags) for c in d.get("neoforge:conditions", [])):
            continue
        ing = d["input"]["ingredient"]
        if isinstance(ing, list) or "item" not in ing and "tag" not in ing:
            continue
        if "item" in ing:
            key = ing["item"]
            members = {key}
        else:
            key = "#" + ing["tag"]
            members = item_tags(ing["tag"])
            if not members:
                dead_tags.append(key)
        refs[key] = d["output"]
        for m in members:
            covered.setdefault(m, key)

    blocks = [l.split("\t")[0] for l in IDS.read_text().splitlines()
              if l.count("\t") >= 2 and l.split("\t")[1] == "block" and l.split("\t")[2]]
    # (named lang rows only: build_id_index.py also adds unnamed registry rows, e.g. technical blocks like wall torches)
    missing_refs = sorted({r for _, r, _, _ in TAG_RULES if r not in refs})
    if missing_refs:
        sys.exit(f"reference recipes not found in Alchemistry: {missing_refs}")

    # Precompute tag membership for the rules.
    tag_rule_members = [(set(item_tags(t)), ref, f, rule) for t, ref, f, rule in TAG_RULES]
    storage = item_tags("c:storage_blocks")
    ores = item_tags("c:ores") | block_tags("c:ores")
    stone_blocks = set().union(*(block_tags(t) for t in STONE_BLOCK_TAGS))
    for (kind, t) in list(tags):
        if kind == "block" and STONE_REPLACEABLES_RX.match(t):
            stone_blocks |= block_tags(t)
    deepslate_blocks = set().union(*(block_tags(t) for t in DEEPSLATE_BLOCK_TAGS))
    plant_blocks = set().union(*(block_tags(t) for t in PLANT_BLOCK_TAGS))

    # Wood names: X for every X_planks in #minecraft:planks (per namespace).
    woods = collections.defaultdict(set)
    for p in item_tags("minecraft:planks"):
        ns, path = p.split(":")
        if path.endswith("_planks"):
            woods[ns].add(path[:-len("_planks")])

    def ref_is_metal(ref):
        if ref.startswith("#c:storage_blocks/"):
            return ref.split("/", 1)[1] not in NONMETAL_STORAGE
        return bool(METAL_REF_RX.search(ref)) or ref.startswith("#c:ores") or ref.startswith("#c:ingots") \
            or ref.startswith("#c:nuggets") or ref.startswith("#c:dusts") or ref.startswith("#c:plates")

    resolved = {}      # item -> (ref, factor, rule)
    skipped = collections.defaultdict(list)   # reason -> items

    candidates = []
    for item in blocks:
        if item in covered:
            continue
        if item not in models or item.split(":", 1)[1].startswith("potted_"):
            skipped["no item form (technical block state, wall/potted variant, fluid)"].append(item)
            continue
        ns, path = item.split(":", 1)
        toks = set(re.split(r"[_/]", path))
        if ns in SKIP_NAMESPACES:
            skipped[SKIP_NAMESPACES[ns]].append(item)
        elif item in ores or "ore" in toks or path.endswith("_ore") or "ores" in toks:
            skipped["ore (ores are processed, not dissolved, before acids)"].append(item)
        elif path.startswith("raw_") or "raw" in toks:
            skipped["raw ore block"].append(item)
        elif item in storage:
            skipped["storage block (c:storage_blocks)"].append(item)
        elif ns in TECH_NAMESPACES:
            skipped["machine / tech / magic-tech mod (would dupe metals or processed parts)"].append(item)
        elif toks & TECH_WORDS or item in TECH_IDS:
            skipped["creative / technical / structure block"].append(item)
        elif toks & (METAL_NAMES if ns == "rechiseled" else METAL_WORDS):
            skipped["metal or metal-containing block (metals only from metal inputs)"].append(item)
        else:
            candidates.append(item)

    decor_applied = {}   # item -> its factor already includes the decoration halving
    # Pass 1: item tags, then natural-stone block tags.
    rest = []
    for item in candidates:
        hit = None
        for members, ref, f, rule in tag_rule_members:
            if item in members:
                hit = (ref, f, rule)
                break
        if hit is None and item in deepslate_blocks:
            hit = ("minecraft:deepslate", 1.0, "block tag: deepslate ore replaceable -> deepslate")
        if hit is None and item in stone_blocks:
            hit = ("minecraft:stone", 1.0, "block tag: natural stone -> stone")
        if hit is None and item in plant_blocks and not set(item.split(":", 1)[1].split("_")) & PLANT_DENY_WORDS:
            hit = ("minecraft:short_grass", 1.0, "block tag: replaceable plants -> short grass (plant matter)")
        if hit:
            resolved[item] = hit
            decor_applied[item] = False
        elif item.split(":", 1)[0] in TAG_ONLY_NAMESPACES:
            skipped["magic mod block without a material tag (only tagged wood sets are covered)"].append(item)
        else:
            rest.append(item)

    # Pass 2+: name rules. A contiguous run of tokens names a known base (covered or already
    # resolved item, a wood type); every other token must be a known shape/decoration word.
    def base_of(cand, ns):
        # Plural first so "brick" means the bricks block, not one brick item.
        for b in (f"{ns}:{cand}s", f"minecraft:{cand}s", f"{ns}:{cand}_block", f"minecraft:{cand}_block",
                  f"{ns}:{cand}", f"minecraft:{cand}"):
            if b in covered:
                ref, f, d = covered[b], 1.0, False
            elif b in resolved:
                ref, f, _ = resolved[b]
                d = decor_applied.get(b, False)
            else:
                continue
            if ref_is_metal(ref) or (ref in VALUABLE_REFS and ns not in VALUABLE_OK_NAMESPACES):
                return None
            return (ref, f, b, d)
        if cand in woods[ns] or cand in woods["minecraft"]:
            return ("#minecraft:planks", 1.0, f"{cand} wood", False)
        return None

    def name_rule(item):
        ns, path = item.split(":", 1)
        t = path.split("_")
        n = len(t)
        if ns != "rechiseled" and set(t) & FOREIGN_WORDS:
            return None
        for size in range(n, 0, -1):
            for i in range(0, n - size + 1):
                if ns == "rechiseled" and i != 0:
                    continue
                cand = "_".join(t[i:i + size])
                if f"{ns}:{cand}" == item:
                    continue
                b = base_of(cand, ns)
                if not b:
                    continue
                remainder = t[:i] + t[i + size:]
                ref, bf, bname, bdecor = b
                f = 1.0
                decor = False
                if ns == "rechiseled":
                    # Rechiseled blocks are chiseled 1:1 from their base; only slabs halve.
                    if "slab" in remainder:
                        f = 0.5
                else:
                    ok = True
                    for w in remainder:
                        if w in VANILLA_WORDS:
                            f = min(f, VANILLA_WORDS[w])
                        elif w in DECOR_WORDS:
                            decor = True
                        elif w in STONE_QUALIFIERS and ref in STONE_REFS:
                            pass
                        else:
                            ok = False
                            break
                    if not ok:
                        continue
                    if decor and not bdecor:
                        f *= DECOR_FACTOR
                # Wood name + log/wood/stem/hyphae is a log, not planks.
                if bname.endswith(" wood") and set(remainder) & {"log", "wood", "stem", "hyphae"} and not decor:
                    ref = "#minecraft:logs"
                if ns == "rechiseled":
                    kind = "rechiseled variant (chiseled 1:1, slabs x0.5)"
                elif decor:
                    kind = "decoration-mod variant (x0.5)"
                else:
                    kind = "vanilla-style shape/variant (slabs x0.5, fences x0.5)"
                return (ref, f * bf, f"name: {kind} of base material", bname, decor or bdecor)
        return None

    bases = {}
    changed = True
    while changed and rest:
        changed = False
        nxt = []
        for item in sorted(rest, key=lambda x: (len(x.split(":", 1)[1]), x)):
            r = name_rule(item)
            if r:
                resolved[item] = (r[0], r[1], r[2])
                bases[item] = r[3]
                decor_applied[item] = r[4]
                changed = True
            else:
                nxt.append(item)
        rest = nxt

    for item in rest:
        skipped["no sensible analog (left uncovered)"].append(item)

    # Write recipes as ONE table (thousands of separate files would make every player's first
    # packwiz sync slow): {"outputs": [unique output objects], "recipes": [[item, output_index], ...]}.
    if OUT.exists():
        shutil.rmtree(OUT)
    by_rule = collections.Counter()
    examples = {}
    outputs, out_index, rows = [], {}, []
    for item, (ref, f, rule) in sorted(resolved.items()):
        if item != item.lower():
            sys.exit(f"uppercase id: {item}")
        out = scale_output(refs[ref], f)
        key = json.dumps(out, sort_keys=True)
        if key not in out_index:
            out_index[key] = len(outputs)
            outputs.append(out)
        rows.append([item, out_index[key]])
        by_rule[rule] += 1
        examples.setdefault(rule, (item, ref, f))
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    TABLE.write_text(json.dumps({"generated_by": "tools/build_dissolver.py", "outputs": outputs, "recipes": rows},
                                separators=(",", ":")) + "\n")
    print(f"Wrote {TABLE.relative_to(ROOT)}: {len(rows)} recipes, {len(outputs)} unique outputs, "
          f"{TABLE.stat().st_size // 1024} KB")

    # Summary.
    covered_blocks = sum(1 for b in blocks if b in covered)
    print(f"Block ids in pack: {len(blocks)}")
    print(f"Covered before (Alchemistry): {covered_blocks}")
    print(f"Generated now: {len(resolved)}")
    for rule, c in by_rule.most_common():
        print(f"  {c:5d}  {rule}")
    print(f"Skipped: {sum(len(v) for v in skipped.values())}")
    for reason, v in sorted(skipped.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(v):5d}  {reason}")
    if dead_tags:
        print(f"Alchemistry recipes with empty tags on 1.21.1: {', '.join(sorted(dead_tags))}")
    if "--dump" in sys.argv:  # debugging aid: every generated recipe and its analog
        dump = pathlib.Path(sys.argv[sys.argv.index("--dump") + 1])
        dump.write_text("".join(f"{i}\t{r}\t{f:g}\t{bases.get(i, '')}\t{rule}\n"
                                for i, (r, f, rule) in sorted(resolved.items())))
    write_doc(len(blocks), covered_blocks, resolved, by_rule, examples, skipped, dead_tags)


def write_doc(n_blocks, n_covered, resolved, by_rule, examples, skipped, dead_tags):
    L = ["# Dissolver coverage (generated)", "",
         "Generated by `python3 tools/build_dissolver.py`; do not edit by hand. Rerun it after the mod list",
         "changes (after `test/smoke.sh` and `python3 test/build_id_index.py`), then run the smoke test.",
         "Recipes are written to `pack/kubejs/data/warbucks/recipe/dissolver/` and copy the output of the",
         "closest vanilla block Alchemistry already dissolves (scaled down for slabs and decorations).", "",
         "## Summary", "",
         f"- Block ids in the pack: {n_blocks}",
         f"- Already dissolvable (Alchemistry): {n_covered}",
         f"- Generated recipes: {len(resolved)}",
         f"- Left uncovered: {sum(len(v) for v in skipped.values())}", ""]
    if dead_tags:
        L += ["Alchemistry ships recipes for tags that are empty on 1.21.1 (" + ", ".join(f"`{t}`" for t in sorted(dead_tags))
              + "); the generator covers those items with item recipes using the same outputs.", ""]
    L += ["## Generated, by rule", "", "| Recipes | Rule | Example (reference, factor) |", "|---:|---|---|"]
    for rule, c in by_rule.most_common():
        item, ref, f = examples[rule]
        L.append(f"| {c} | {rule} | `{item}` (`{ref}`, x{f:g}) |")
    L += ["", "## Left uncovered, by reason", ""]
    for reason, v in sorted(skipped.items(), key=lambda kv: -len(kv[1])):
        L += [f"### {reason} ({len(v)})", ""]
        byns = collections.defaultdict(list)
        for i in v:
            ns, path = i.split(":", 1)
            byns[ns].append(path)
        for ns in sorted(byns, key=lambda k: (-len(byns[k]), k)):
            L.append(f"- **{ns}** ({len(byns[ns])}): " + ", ".join(sorted(byns[ns])))
        L.append("")
    DOC.write_text("\n".join(L))


if __name__ == "__main__":
    main()
