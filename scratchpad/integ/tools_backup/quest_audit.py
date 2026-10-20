#!/usr/bin/env python3
"""Quest audit: find quests a player can never finish.

Cheap checks (no game data needed beyond test/ids.tsv; build_quests.py --check runs them every time):
  1  dependency cycles, and quests that can't be reached from a root (a quest with no dependencies)
  2  required quests that hang on optional quests (soft warning: still doable, but the book says it's optional)
  3  item / reward ids that don't exist, or that aren't items (an entity or biome id in an item task)
  6  kill / dimension / structure / biome ids that don't exist in the matching registry
  +  quests with no tasks (FTB Quests can never complete them)

Full checks (python tools/quest_audit.py --full), which need a recipe dump from a real server
(test/audit_dump.ps1 -> test/dump/*.json) plus the mod jars in test/server/mods:
  4  item tasks asking for an item nobody can obtain: not a recipe output (after KubeJS changes), not a loot
     drop (blocks, mobs, chests, fishing, archaeology...), not a naturally generated block, not a quest reward
     (outside the token shop), not in ALLOW below
  5  tier sanity (soft warnings): an item task in t0..t7 whose every recipe needs (directly, or via the
     machine named like the recipe type) an item first asked for in a LATER tier chapter
  +  anytag() tags that don't exist; the dump's registries confirm item/entity/biome/structure/dimension ids

Usage: python tools/quest_audit.py           cheap checks (exit 1 on errors)
       python tools/quest_audit.py --full    cheap + full checks
       QUEST_ONLY=a,b ... (as for build_quests.py) narrows the chapters; cross-chapter deps are then not judged
"""
import gzip
import io
import json
import os
import pathlib
import re
import struct
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
DUMP = ROOT / "test/dump"
SERVER = ROOT / "test/server"
TIERS = ["start", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "seed", "creation"]  # main path order
SHOP_GROUP = "shop"

# Items the obtainability check can't prove but that a player CAN get. Keep the reason honest.
ALLOW = {
    # --- vanilla mechanics with no recipe or loot table ---
    "minecraft:water_bucket": "bucket on water",
    "minecraft:lava_bucket": "bucket on lava",
    "minecraft:milk_bucket": "bucket on a cow",
    "minecraft:powder_snow_bucket": "bucket on powder snow",
    "minecraft:dragon_egg": "spawns on the exit portal when the dragon dies",
    "minecraft:dragon_head": "End ship item frame",
    "minecraft:elytra": "End ship item frame",
    "minecraft:experience_bottle": "villager trade (cleric) and quest rewards",
    "minecraft:end_portal_frame": "can't be picked up; quests only show it",
    "minecraft:bee_nest": "silk touch on a natural bee nest (block is placed by tree decorators)",
    "minecraft:budding_amethyst": "can't be mined; quest uses it as a marker",
    "minecraft:honey_bottle": "bottle on a full beehive",
    "minecraft:honeycomb": "shears on a full beehive",
    "minecraft:axolotl_bucket": "bucket on an axolotl",
    "minecraft:tadpole_bucket": "bucket on a tadpole",
    "minecraft:cod_bucket": "bucket on a cod",
    "minecraft:salmon_bucket": "bucket on a salmon",
    "minecraft:tropical_fish_bucket": "bucket on a tropical fish",
    "minecraft:pufferfish_bucket": "bucket on a pufferfish",
    "minecraft:wither_skeleton_skull": "wither skeleton drop (looting condition)",
    "minecraft:nether_star": "Wither drop (entity loot via a special rule)",
    "minecraft:trial_key": "trial spawner reward",
    "minecraft:ominous_trial_key": "ominous trial spawner reward",
    "minecraft:heavy_core": "ominous vault reward",
    "minecraft:goat_horn": "goats ram into logs/stone",
    "minecraft:turtle_scute": "baby turtles drop it when they grow up",
    "minecraft:armadillo_scute": "armadillos shed it, or brush them",
    "minecraft:sniffer_egg": "suspicious sand (archaeology) in warm ocean ruins",
    "minecraft:filled_map": "cartography table / villager trade",
    "minecraft:enchanted_book": "enchanting table on a book",
    "minecraft:potion": "brewing stand",
    "minecraft:splash_potion": "brewing stand",
    "minecraft:lingering_potion": "brewing stand",
    "minecraft:tipped_arrow": "crafting with lingering potions (special recipe)",
    "minecraft:firework_rocket": "special crafting recipe",
    "minecraft:written_book": "book and quill, signed",
    "minecraft:player_head": "player kill / trade",
    # --- modded mechanics the dump can't see (checked 2026-10-19) ---
    "occultism:book_of_binding_bound_afrit": "occultism:crafting_special_book_binding (book + Dictionary of Spirits, in code)",
    "occultism:book_of_binding_bound_marid": "occultism:crafting_special_book_binding (book + Dictionary of Spirits, in code)",
    "powah:player_aerial_pearl": "use an Aerial Pearl on a Zombie or Husk (Powah's JEI info)",
    "undergarden:cloggrum_battleaxe": "dropped as equipment by Forgotten mobs (no recipe by design)",
    "undergarden:ancient_helmet": "dropped as equipment by Forgotten mobs",
    "undergarden:ancient_chestplate": "dropped as equipment by Forgotten mobs",
    "undergarden:ancient_leggings": "dropped as equipment by Forgotten mobs",
    "extendedcrafting:singularity": "Quantum Compressor recipes are generated in code from the singularity definitions",
    "extendedcrafting:ultimate_singularity": "special recipe type (extendedcrafting:ultimate_singularity), built in code",
    "hostilenetworks:data_model": "right-click a mob with a Blank Data Model (and HNN's code-built model recipes)",
    "hostilenetworks:overworld_prediction": "Simulation Chamber output (computed from the data model in code)",
    "hostilenetworks:twilight_prediction": "Simulation Chamber output (computed from the data model in code)",
    "ironjetpacks:jetpack": "Iron Jetpacks builds the jetpack recipes in code from its jetpack definitions",
    "modern_industrialization:uranium_fuel_rod_depleted": "MI nuclear reactor: a fuel rod depletes in the reactor",
    "modern_industrialization:le_uranium_fuel_rod_depleted": "MI nuclear reactor: a fuel rod depletes in the reactor",
    "modern_industrialization:he_uranium_fuel_rod_depleted": "MI nuclear reactor: a fuel rod depletes in the reactor",
    "modern_industrialization:le_mox_fuel_rod_depleted": "MI nuclear reactor: a fuel rod depletes in the reactor",
    "modern_industrialization:he_mox_fuel_rod_depleted": "MI nuclear reactor: a fuel rod depletes in the reactor",
    "compactmachines:machine": "Compact Machines builds its machine recipes in code (one per room template)",
    "twilightforest:filled_magic_map": "use an empty magic map (map mechanic)",
    "twilightforest:filled_maze_map": "use an empty maze map (map mechanic)",
    "twilightforest:filled_ore_map": "use an empty ore map (map mechanic)",
    "undergarden:gwibling_bucket": "bucket on a gwibling",
    "utilitarian:slime_bucket": "bucket on a small slime (Utilitarian)",
    "ae2:matter_ball": "AE2 Matter Condenser output (built in code)",
    "ae2:name_press": "AE2 meteorite chests (filled in code)",
    "ae2:fe_p2p_tunnel": "attune an ME P2P tunnel by right-clicking it with an energy item",
    "ae2:fluid_p2p_tunnel": "attune an ME P2P tunnel by right-clicking it with a bucket",
    "ae2wtlib:wireless_universal_terminal": "ae2wtlib:combine special recipe (output built in code)",
    "apotheosis:potion_charm": "apotheosis:potion_charm_crafting special recipe (output built in code)",
    "apothic_enchanting:warden_tendril": "Warden drop from Apothic Enchanting's coded loot modifier",
    "ars_elemental:firenando_familiar": "Ars Ritual of Binding on the mob",
    "ars_elemental:flashjack_familiar": "Ars Ritual of Binding on the mob",
    "ars_elemental:siren_familiar": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_amethyst_golem": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_bookwyrm": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_drygmy": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_starbuncle": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_whirlisprig": "Ars Ritual of Binding on the mob",
    "ars_nouveau:familiar_wixie": "Ars Ritual of Binding on the mob",
    "justdirethings:xp_fluid_bucket": "JDT Experience Holder turns stored XP into fluid",
    "mysticalagriculture:fertilized_essence": "chance drop from MA crops grown with fertilizer (in code)",
    "mekanism:heavy_water_bucket": "Mekanism Electric Pump with a Filter Upgrade on water",
    "powah:binding_card_dim": "use a Binding Card on an Enderman or Endermite (Powah's JEI info)",
    "fluxnetworks:flux_dust": "in-world: redstone dropped on obsidian above bedrock, hit by an explosion (Flux Networks)",
    "mysticalagriculture:cognizant_dust": "boss kill with an enchanted essence sword (per the quest text; coded drop, not verified here)",
    "undergarden:gronglet": "break a wild gronglet (per the quest text; placed by coded worldgen, not verified here)",
    "undergarden:music_disc_gloomper_secret": "Gloomper secret (per the quest text; coded drop, not verified here)",
    "twilightforest:thorn_rose": "grows on thorns in the Thornlands (Twilight worldgen in code)",
}
ALLOW_NS = {
    # Whole namespaces whose items come from non-recipe mechanics the dump can't see.
    "relics": "Relics adds its items to chest loot from code (never crafted, by design)",
}


# --- loading ------------------------------------------------------------------------------------
def load_quests():
    from quest_data import CHAPTERS, REWARD_TABLES
    return CHAPTERS, REWARD_TABLES


def load_ids():
    """ids.tsv as {id: set(types)}."""
    ids = defaultdict(set)
    for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            ids[parts[0]].add(parts[1])
    return ids


FILTER_ITEM = re.compile(r"item\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)")
FILTER_TAG = re.compile(r"item_tag\(([a-z0-9_.\-]+:[a-z0-9_./\-]+)\)")


def task_items(t):
    """Item ids a task asks for: [(id, is_alternative)]."""
    if t[0] == "item":
        return [t[1]]
    if t[0] == "filter":
        return FILTER_ITEM.findall(t[1])
    return []


# --- cheap checks -------------------------------------------------------------------------------
def cheap_checks(chapters, reward_tables=None, ids=None, partial=False):
    """Returns (errors, warnings): lists of (chapter, quest key, reason)."""
    ids = load_ids() if ids is None else ids
    errors, warnings = [], []
    quests = {}
    chapter_of = {}
    for c in chapters:
        for q in c.quests:
            quests[q.key] = q
            chapter_of[q.key] = c.key

    # 3 + 6: ids and their kinds
    # With registry rows in ids.tsv (build_id_index.py after test/audit_dump.ps1) an item task must name a real item;
    # without them, lang files list many block items only as "block".
    item_kinds = {"item"} if "#registry" in ids else {"item", "block"}
    kinds = {"item": item_kinds, "kill": {"entity"}, "dimension": {"dimension"},
             "structure": {"structure"}, "biome": {"biome"}}
    for c in chapters:
        for q in c.quests:
            if not q.tasks:
                errors.append((c.key, q.key, "quest has no tasks (it can never complete)"))
            for t in q.tasks:
                if t[0] in kinds:
                    want = kinds[t[0]]
                    have = ids.get(t[1], set())
                    if not have:
                        errors.append((c.key, q.key, f"{t[0]} task: unknown id {t[1]}"))
                    elif not have & want:
                        errors.append((c.key, q.key, f"{t[0]} task: {t[1]} is a {'/'.join(sorted(have))}, not a {'/'.join(sorted(want))}"))
                elif t[0] == "filter":
                    for i in FILTER_ITEM.findall(t[1]):
                        have = ids.get(i, set())
                        if not have & kinds["item"]:
                            errors.append((c.key, q.key, f"filter: unknown item {i}"))
                if t[0] in ("item", "kill", "filter") and len(t) > 2 and t[2] < 1:
                    errors.append((c.key, q.key, f"{t[0]} task: count {t[2]} < 1"))
            for rid, _ in q.items:
                if not ids.get(rid, set()) & kinds["item"]:
                    errors.append((c.key, q.key, f"reward: unknown item {rid}"))
    for tkey, t in (reward_tables or {}).items():
        for rid, _, _ in t["entries"]:
            if not ids.get(rid, set()) & kinds["item"]:
                errors.append(("(reward table)", tkey, f"unknown item {rid}"))

    # 1: cycles (Tarjan SCC over dep edges inside the loaded chapters)
    graph = {k: [d for d in q.deps if d in quests] for k, q in quests.items()}
    in_cycle = set()
    index, low, stack, on, counter = {}, {}, [], set(), [0]

    def strong(v):
        work = [(v, iter(graph[v]))]
        index[v] = low[v] = counter[0]; counter[0] += 1; stack.append(v); on.add(v)
        while work:
            node, it = work[-1]
            nxt = next(it, None)
            if nxt is not None:
                if nxt not in index:
                    index[nxt] = low[nxt] = counter[0]; counter[0] += 1; stack.append(nxt); on.add(nxt)
                    work.append((nxt, iter(graph[nxt])))
                elif nxt in on:
                    low[node] = min(low[node], index[nxt])
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
            if low[node] == index[node]:
                comp = []
                while True:
                    w = stack.pop(); on.discard(w); comp.append(w)
                    if w == node:
                        break
                if len(comp) > 1 or node in graph[node]:
                    in_cycle.update(comp)
                    errors.append((chapter_of[node], node, "dependency cycle: " + " -> ".join(sorted(comp))))

    for v in graph:
        if v not in index:
            strong(v)

    # 1: reachability (fixpoint). any_dep needs one completable dep, otherwise all of them.
    # Deps outside the loaded chapters (QUEST_ONLY) count as completable.
    def ok_dep(d, done):
        return d in done or (d not in quests and partial)

    done = set()
    changed = True
    while changed:
        changed = False
        for k, q in quests.items():
            if k in done:
                continue
            deps = q.deps
            if not deps or (q.any_dep and any(ok_dep(d, done) for d in deps)) or (not q.any_dep and all(ok_dep(d, done) for d in deps)):
                done.add(k)
                changed = True
    for k, q in quests.items():
        if k in done or k in in_cycle:
            continue
        bad = [d for d in q.deps if not ok_dep(d, done)]
        root = [d for d in bad if d in in_cycle or d not in quests]
        why = ("waits on a cycle: " + ", ".join(root)) if root else ("waits on unreachable " + ", ".join(bad[:4]))
        errors.append((chapter_of[k], k, "unreachable: " + why))

    # 2: required quests behind optional ones. A path through only required quests must exist.
    req_done = set()
    changed = True
    while changed:
        changed = False
        for k, q in quests.items():
            if k in req_done or k not in done:
                continue
            good = lambda d: (d in req_done and not quests[d].optional) or (d not in quests and partial)
            if not q.deps or (q.any_dep and any(good(d) for d in q.deps)) or (not q.any_dep and all(good(d) for d in q.deps)):
                req_done.add(k)
                changed = True
    for k, q in quests.items():
        if q.optional or k not in done or k in req_done:
            continue
        opt = [d for d in q.deps if d in quests and quests[d].optional]
        behind = [d for d in q.deps if d in quests and not quests[d].optional and d not in req_done]
        if opt:
            why = ("its only unlocks are optional: " if q.any_dep else "depends on optional ") + ", ".join(opt)
        else:
            why = "depends on required quests that are themselves behind optional ones: " + ", ".join(behind[:4])
        warnings.append((chapter_of[k], k, "required quest behind optional: " + why))
    return errors, warnings


# --- game data (full checks) -------------------------------------------------------------------
def data_jars():
    jars = sorted((SERVER / "mods").glob("*.jar"))
    jars += sorted((SERVER / "libraries/net/minecraft/server").glob("*/server-*-extra.jar"))
    jars += sorted((SERVER / "libraries/net/neoforged/neoforge").glob("*/neoforge-*-universal.jar"))
    return jars


def data_files():
    """Yield (path inside a data root, bytes) for every data/ file in the jars and pack/kubejs/data."""
    for jar in data_jars():
        try:
            z = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            continue
        for name in z.namelist():
            if name.startswith("data/") and not name.endswith("/"):
                yield name, (lambda z=z, n=name: z.read(n))
    kj = ROOT / "pack/kubejs/data"
    for f in kj.rglob("*"):
        if f.is_file():
            yield "data/" + f.relative_to(kj).as_posix(), (lambda f=f: f.read_bytes())


def nbt_names(raw):
    """Block names from a structure template's palette(s) (gzipped NBT): every string under a "Name" key."""
    try:
        buf = io.BytesIO(gzip.decompress(raw))
    except OSError:
        return set()
    out = set()

    def rd(n):
        return buf.read(n)

    def string():
        (n,) = struct.unpack(">H", rd(2))
        return rd(n).decode("utf-8", "replace")

    def payload(tag, name):
        if tag == 1: rd(1)
        elif tag == 2: rd(2)
        elif tag == 3: rd(4)
        elif tag == 4: rd(8)
        elif tag == 5: rd(4)
        elif tag == 6: rd(8)
        elif tag == 7: (n,) = struct.unpack(">i", rd(4)); rd(n)
        elif tag == 8:
            s = string()
            if name == "Name":
                out.add(s)
        elif tag == 9:
            sub = rd(1)[0]; (n,) = struct.unpack(">i", rd(4))
            for _ in range(n):
                payload(sub, None)
        elif tag == 10:
            while True:
                t = rd(1)
                if not t or t[0] == 0:
                    break
                nm = string()
                payload(t[0], nm)
        elif tag == 11: (n,) = struct.unpack(">i", rd(4)); rd(4 * n)
        elif tag == 12: (n,) = struct.unpack(">i", rd(4)); rd(8 * n)
    try:
        t = rd(1)[0]
        string()
        payload(t, None)
    except (struct.error, IndexError, RecursionError):
        pass
    return out


ID_RE = re.compile(r"^[a-z0-9_.\-]+:[a-z0-9_./\-]+$")


def walk_strings(node, keys=("Name", "name", "item", "id", "block")):
    """All id-like strings under the given keys anywhere in a JSON tree."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and k in keys and ID_RE.match(v):
                yield v
            else:
                yield from walk_strings(v, keys)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v, keys)


class GameData:
    def __init__(self, reg=None):
        reg = reg or {}
        self.server_tags = reg.get("item_tags")  # from the dump: tags after KubeJS edits (preferred)
        self.tags = defaultdict(set)      # item tag -> raw entries ("#x" or ids)
        self.block_loot = {}              # block id -> set(drops)
        self.other_loot = set()           # every item from non-block loot tables
        self.natural = set()              # blocks named in worldgen json / structure templates
        self.ore_blocks = set()
        self.crops = set()
        files = list(data_files())
        replaced = set()
        for name, get in files:
            m = re.match(r"data/([^/]+)/tags/items?/(.+)\.json$", name)
            if m:
                tag = f"{m.group(1)}:{m.group(2)}"
                try:
                    j = json.loads(get())
                except ValueError:
                    continue
                if j.get("replace") and tag not in replaced:
                    self.tags[tag].clear(); replaced.add(tag)
                for v in j.get("values", []):
                    self.tags[tag].add(v["id"] if isinstance(v, dict) else v)
                continue
            m = re.match(r"data/([^/]+)/tags/blocks?/(.+)\.json$", name)
            if m and ("ores" in m.group(2).split("/")[0]):
                try:
                    j = json.loads(get())
                except ValueError:
                    continue
                for v in j.get("values", []):
                    v = v["id"] if isinstance(v, dict) else v
                    if not v.startswith("#"):
                        self.ore_blocks.add(v)
                continue
            m = re.match(r"data/([^/]+)/loot_tables?/(.+)\.json$", name)
            if m:
                try:
                    j = json.loads(get())
                except ValueError:
                    continue
                drops = {s for s in walk_strings(j, ("name",)) if ID_RE.match(s)}
                drops |= self._tag_drops(j)
                path = m.group(2)
                if path.startswith("blocks/"):
                    b = f"{m.group(1)}:{path[7:]}"
                    self.block_loot.setdefault(b, set()).update(drops)
                    if "minecraft:block_state_property" in json.dumps(j) and '"age"' in json.dumps(j):
                        self.crops.add(b)  # a crop: placed by its seed, which is a different item
                else:
                    self.other_loot |= drops
                continue
            if re.match(r"data/[^/]+/loot_modifiers/", name) and name.endswith(".json"):
                try:
                    j = json.loads(get())
                except ValueError:
                    continue
                if isinstance(j, dict) and "entries" not in j:  # skip the global_loot_modifiers.json index
                    self.other_loot.update(walk_strings(j, ("item", "name", "id", "result")))
                continue
            if re.match(r"data/[^/]+/worldgen/", name) and name.endswith(".json"):
                try:
                    j = json.loads(get())
                except ValueError:
                    continue
                self.natural.update(walk_strings(j, ("Name",)))
                continue
            if re.match(r"data/[^/]+/(structures?)/.+\.nbt$", name):
                self.natural |= nbt_names(get())
        self._resolved = {}
        for t in ("c:ores", "minecraft:base_stone_overworld", "minecraft:base_stone_nether", "minecraft:logs",
                  "minecraft:leaves", "minecraft:flowers", "minecraft:sand", "minecraft:dirt"):
            self.natural.update((reg.get("block_tags") or {}).get(t, ()))

    def _tag_drops(self, j):
        out = set()
        if isinstance(j, dict):
            if j.get("type") == "minecraft:tag" and isinstance(j.get("name"), str):
                out.add("#" + j["name"])
            for v in j.values():
                out |= self._tag_drops(v)
        elif isinstance(j, list):
            for v in j:
                out |= self._tag_drops(v)
        return out

    def tag(self, t, seen=None):
        """Item ids in a tag (nested tags resolved)."""
        t = t.lstrip("#")
        if self.server_tags is not None:
            return set(self.server_tags.get(t, ()))
        if t in self._resolved:
            return self._resolved[t]
        seen = seen or set()
        if t in seen:
            return set()
        seen.add(t)
        out = set()
        for v in self.tags.get(t, ()):
            out |= self.tag(v, seen) if v.startswith("#") else {v}
        self._resolved[t] = out
        return out

    def expand(self, ids):
        out = set()
        for i in ids:
            out |= self.tag(i) if i.startswith("#") else {i}
        return out


OUT_KEY = re.compile(r"result|output|product|byproduct", re.I)


def recipe_outputs(j, gd):
    """Item/fluid ids under output-like keys of a recipe JSON (tags resolved)."""
    out = set()

    def grab(node):
        if isinstance(node, str):
            if ID_RE.match(node):
                out.add(node)
        elif isinstance(node, dict):
            for k, v in node.items():
                if k in ("item", "id", "fluid", "name", "Name", "block") and isinstance(v, str) and ID_RE.match(v):
                    out.add(v)
                elif k == "tag" and isinstance(v, str):
                    out.update(gd.tag(v))
                elif k not in ("type", "count", "amount", "chance", "components", "nbt"):
                    grab(v)
        elif isinstance(node, list):
            for v in node:
                grab(v)

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if OUT_KEY.search(k):
                    grab(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(j)
    return out


def recipe_input_groups(j, gd):
    """Ingredient groups (each a set of acceptable item ids) of a recipe JSON. Approximate: lists are AND,
    except values in a shaped "key" and nested lists, which are alternatives."""
    groups = []

    def options(node):
        if isinstance(node, dict):
            if "tag" in node and isinstance(node["tag"], str):
                return gd.tag(node["tag"])
            for k in ("item", "id"):
                if isinstance(node.get(k), str) and ID_RE.match(node[k]):
                    return {node[k]}
            if "ingredient" in node:
                return options(node["ingredient"])
            if "items" in node and isinstance(node["items"], list):  # neoforge compound/list ingredient
                return set().union(*[options(v) or set() for v in node["items"]]) if node["items"] else None
            if "children" in node and isinstance(node["children"], list):
                return set().union(*[options(v) or set() for v in node["children"]]) if node["children"] else None
            return None
        if isinstance(node, list):
            opts = [options(v) for v in node]
            opts = [o for o in opts if o]
            return set().union(*opts) if opts else None
        if isinstance(node, str) and ID_RE.match(node):
            return {node}
        return None

    def walk(node, key=None):
        if isinstance(node, dict):
            o = options(node) if key is not None else None
            if o:
                groups.append(o)
                return
            for k, v in node.items():
                if OUT_KEY.search(k) or k in ("type", "pattern", "group", "category", "neoforge:conditions", "conditions"):
                    continue
                if k == "key" and isinstance(v, dict):
                    for vv in v.values():
                        o = options(vv)
                        if o:
                            groups.append(o)
                    continue
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                if isinstance(v, list):
                    o = options(v)
                    if o:
                        groups.append(o)
                else:
                    walk(v, key)
    walk(j)
    return groups


def load_dump():
    rf, gf = DUMP / "recipe_dump.json", DUMP / "registry_dump.json"
    if not rf.exists() or not gf.exists():
        sys.exit("test/dump/recipe_dump.json or registry_dump.json missing: run test/audit_dump.ps1 (Terminal panel)")
    recipes = []
    for r in json.loads(rf.read_text(encoding="utf-8"))["recipes"]:
        try:
            recipes.append((r["id"], json.loads(r["json"])))
        except (ValueError, KeyError):
            pass
    reg = {k: (v if isinstance(v, dict) else set(v)) for k, v in json.loads(gf.read_text(encoding="utf-8")).items()}
    return recipes, reg


def full_checks(chapters, reward_tables):
    errors, warnings, notes = [], [], []
    recipes, reg = load_dump()
    gd = GameData(reg)
    items = reg.get("item", set())
    blocks = reg.get("block", set())
    fluids = reg.get("fluid", set())

    # registry confirmations (6 + 3, authoritative)
    regkind = {"item": "item", "kill": "entity", "dimension": "dimension", "structure": "structure", "biome": "biome"}
    for c in chapters:
        for q in c.quests:
            for t in q.tasks:
                if t[0] in regkind and reg.get(regkind[t[0]]) and t[1] not in reg[regkind[t[0]]]:
                    errors.append((c.key, q.key, f"{t[0]} task: {t[1]} is not in the server's {regkind[t[0]]} registry"))
                if t[0] == "filter":
                    for i in FILTER_ITEM.findall(t[1]):
                        if i not in items:
                            errors.append((c.key, q.key, f"filter: {i} is not in the item registry"))
                    for tg in FILTER_TAG.findall(t[1]):
                        if not gd.tag(tg):
                            errors.append((c.key, q.key, f"anytag: item tag #{tg} is empty or missing (from jar data)"))

    # 4: obtainable set
    made = set()
    produced_by = defaultdict(list)  # item -> [recipe index]
    rec_in = []
    for n, (rid, j) in enumerate(recipes):
        outs = recipe_outputs(j, gd)
        made |= outs
        for o in outs:
            produced_by[o].append(n)
        rec_in.append((rid, j.get("type", ""), recipe_input_groups(j, gd)))
    rewards = set()
    for c in chapters:
        if c.group == SHOP_GROUP:
            continue
        for q in c.quests:
            rewards.update(i for i, _ in q.items)
            for tk in (q.loot, q.choice):
                if tk and tk in reward_tables:
                    rewards.update(i for i, _, _ in reward_tables[tk]["entries"])
    natural = gd.natural | gd.ore_blocks
    loot_other = gd.expand(gd.other_loot)
    base = made | loot_other | rewards | natural | set(ALLOW)
    obtainable = set(base)
    # block loot: drops of a block you can have (placed or natural), or of a block that never drops itself
    # (crops, leaves, grass: it is placed by a different item)
    changed = True
    while changed:
        changed = False
        for b, drops in gd.block_loot.items():
            d = gd.expand(drops)
            if (b in obtainable or b not in d or b in gd.crops) and not d <= obtainable:
                obtainable |= d
                changed = True
    # buckets: obtainable when their fluid is made, natural or in a block loot
    for i in items:
        if (i.endswith("_bucket") or ":bucket_" in i) and i not in obtainable:
            ns, path = i.split(":", 1)
            stem = path[:-7]
            if path.startswith("bucket_"):  # integrateddynamics:bucket_menril_resin
                stem = path[7:]
            for f in (f"{ns}:{stem}", f"{ns}:{stem}_fluid", f"{ns}:molten_{stem}", f"{ns}:flowing_{stem}", f"{ns}:{stem}_still",
                      f"{ns}:{stem}_block", f"{ns}:{stem}_source", f"{ns}:{stem}_flowing"):
                if f in obtainable:
                    obtainable.add(i)
                    break
    asked = {}
    for c in chapters:
        if c.group == SHOP_GROUP:
            continue  # shop entries pay with tokens and only reward items
        for q in c.quests:
            for t in q.tasks:
                if t[0] == "item":
                    cand = [t[1]]
                elif t[0] == "filter":
                    cand = FILTER_ITEM.findall(t[1])
                    if not cand or any(i in obtainable for i in cand) or FILTER_TAG.search(t[1]):
                        continue
                else:
                    continue
                for i in cand:
                    asked.setdefault(i, []).append((c.key, q.key, q.optional))
    for i, where in sorted(asked.items()):
        if i in obtainable or i.split(":")[0] in ALLOW_NS or i not in items:
            continue
        for ck, qk, opt in where:
            (warnings if opt else errors).append((ck, qk, f"unobtainable item {i}: no recipe, loot, worldgen or reward makes it"
                                                 + (" (optional quest)" if opt else "")))

    # 5: tier sanity (soft): direct ingredients and machine only
    tier_of = {}
    for c in chapters:
        if c.key in TIERS[:9]:  # start..t7; seed/creation re-ask for earlier materials in bulk
            ti = TIERS.index(c.key)
            for q in c.quests:
                for t in q.tasks:
                    for i in task_items(t):
                        tier_of[i] = min(tier_of.get(i, 99), ti)
    free = loot_other | natural | rewards | set(ALLOW)  # obtainable without any recipe
    machine_cache = {}

    def machine(rtype):
        if rtype in machine_cache:
            return machine_cache[rtype]
        o = None
        if ":" in rtype and not rtype.startswith("minecraft:"):
            ns, p = rtype.split(":", 1)
            cands = {f"{ns}:{pre}{p}" for pre in ("", "bronze_", "steel_", "electric_", "steam_", "large_")} & items
            o = cands or None
        machine_cache[rtype] = o
        return o

    for c in chapters:
        if c.key not in TIERS[1:9]:  # t0..t7
            continue
        ti = TIERS.index(c.key)
        for q in c.quests:
            for t in q.tasks:
                if t[0] != "item":
                    continue
                x = t[1]
                if x in free or not produced_by.get(x):
                    continue
                blockers = []
                for n in produced_by[x]:
                    rid, rtype, groups = rec_in[n]
                    m = machine(rtype)
                    gs = groups + ([m] if m else [])
                    late = [g for g in gs if g and x not in g and all(tier_of.get(i, -1) > ti and i not in free for i in g)]
                    if not late:
                        blockers = None
                        break
                    g = late[0]
                    first = min(g, key=lambda i: tier_of.get(i, 99))
                    blockers.append(f"{rid} needs {first} ({TIERS[tier_of[first]]})")
                if blockers:
                    warnings.append((c.key, q.key, f"tier: {x} ({c.key}) can only be made with later-tier items: "
                                     + "; ".join(sorted(set(blockers))[:3])))
    notes.append(f"{len(recipes)} recipes, {len(items)} items in registry, {len(made)} recipe outputs, "
                 f"{len(obtainable)} obtainable ids, {len(gd.natural)} natural block names, {len(gd.block_loot)} block loot tables")
    return errors, warnings, notes


def fmt(rows):
    return "\n".join(f"  [{c}] {k}: {r}" for c, k, r in sorted(set(rows)))


def main():
    from quest_data import ONLY
    chapters, tables = load_quests()
    errors, warnings = cheap_checks(chapters, tables, partial=bool(ONLY))
    notes = []
    if "--full" in sys.argv:
        e2, w2, notes = full_checks(chapters, tables)
        errors += e2
        warnings += w2
    for n in notes:
        print("INFO: " + n)
    if warnings:
        print(f"WARNINGS ({len(set(warnings))}):\n" + fmt(warnings))
    if errors:
        print(f"ERRORS ({len(set(errors))}):\n" + fmt(errors))
        sys.exit(1)
    print(f"Quest audit OK ({'full' if notes else 'cheap'} checks): {sum(len(c.quests) for c in chapters)} quests, "
          f"{len(set(warnings))} warning(s)")


if __name__ == "__main__":
    main()
