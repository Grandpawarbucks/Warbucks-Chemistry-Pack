#!/usr/bin/env python3
"""Apotheosis loot tuning, modelled on ATM10's (user decision 2026-10-20: "Apply ATM10's Apotheosis tuning ... rebuild it
from the mods' own default files with the same changes (no ATM10 files copied)").

Reads each mod's own default data file from its jar in test/server/mods, applies the numbers below, and writes the
result into pack/kubejs/data. Nothing is copied from ATM10: its choices are written down here as plain numbers.
What it does:
  - more and better loot: affix gear and gem drops in chests x2 / x1.5, Apotheosis chest rolls x2, unstable spawner x2,
    monsters spawn with affix items 30% of the time (default 12%);
  - rarities and gem purity shift up a world tier (epic from Frontier, mythic from Ascent);
  - vanilla gear weights doubled in the tiers below, gold gear off as affix loot;
  - Twilight Forest gear only drops as affix loot inside the Twilight Forest (armour weights doubled there);
  - mob gear sets that use gold or Twilight Forest items switched off; Miner's Fervor never rolls (weight 0);
  - Silent Gear axes and maces count as melee weapons and the Allthemodium alloy paxel as a breaker for affixes.
Run: python tools/build_apoth_tuning.py   (re-run after updating Apotheosis, Apothic Enchanting or Apothic Spawners)
"""
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pack/kubejs/data"
MODS = ROOT / "test/server/mods"
OFF = [{"type": "neoforge:false"}]

# Affix loot entries: world tiers whose base weight is doubled ("*" = the entry's single weight).
DOUBLE = {
    **{f"chainmail_{p}": ["frontier", "haven"] for p in ("boots", "chestplate", "helmet", "leggings")},
    **{f"diamond_{p}": ["ascent", "pinnacle", "summit"] for p in ("boots", "chestplate", "helmet", "leggings")},
    **{f"iron_{p}": ["ascent", "frontier", "summit"] for p in ("boots", "chestplate", "helmet", "leggings")},
    **{f"leather_{p}": ["haven"] for p in ("boots", "chestplate", "helmet", "leggings")},
    **{f"netherite_{p}": ["pinnacle", "summit"] for p in ("boots", "chestplate", "helmet", "leggings")},
    "turtle_helmet": ["*"],
}
_ARMOUR = ("boots", "chestplate", "helmet", "leggings")
# Twilight Forest gear: every entry only drops in the Twilight Forest; armour weights doubled like their vanilla peers.
TWILIGHT_DIM = {"dimensions": ["twilightforest:twilight_forest"]}
TWILIGHT_DOUBLE = {
    **{f"{m}_{p}": ["ascent", "pinnacle", "summit"] for m in ("arctic", "fiery", "knightmetal") for p in _ARMOUR},
    **{f"{m}_{p}": ["ascent", "frontier", "summit"] for m in ("ironwood", "steeleaf") for p in _ARMOUR},
    **{f"yeti_{p}": ["pinnacle", "summit"] for p in _ARMOUR},
}
GOLD_OFF = [f"golden_{p}" for p in ("axe", "boots", "chestplate", "helmet", "leggings", "pickaxe", "shovel", "sword")]
GEAR_SETS_OFF = [
    "ascent/enchanted_gold", "ascent/ranged/enchanted_gold",
    "ascent/ranged/twilight/arctic", "ascent/ranged/twilight/fiery",
    "ascent/twilight/arctic", "ascent/twilight/fiery", "ascent/twilight/knightmetal",
    "frontier/ranged/twilight/ironwood", "frontier/ranged/twilight/steeleaf",
    "frontier/twilight/ironwood", "frontier/twilight/knightmetal", "frontier/twilight/steeleaf",
    "pinnacle/enchanted_yeti",
    "summit/ranged/twilight/enchanted_arctic", "summit/ranged/twilight/enchanted_fiery",
    "summit/twilight/enchanted_arctic", "summit/twilight/enchanted_fiery",
]
LOOT_CHANCES = {  # loot modifier -> new chance per entry index
    "affix_conversion": {1: 0.6},
    "affix_loot_injection": {0: 0.7, 1: 0.6, 2: 0.6},
    "gem_loot_injection": {0: 0.375, 1: 0.3, 2: 0.3},
}
ROLLS_X2 = ["apotheosis:loot_table/chests/chest_valuable", "apotheosis:loot_table/chests/spawner_brutal",
            "apotheosis:loot_table/chests/spawner_swarm", "apotheosis:loot_table/chests/tome_tower",
            "apothic_spawners:loot_table/gameplay/unstable_spawner"]
RARITIES = {
    "common": {"haven": {"weight": 290}, "frontier": {"weight": 100}, "ascent": {"weight": 0}, "summit": {"weight": 0},
               "pinnacle": {"weight": 0}},
    "uncommon": {"haven": {"weight": 600}, "frontier": {"weight": 300}, "ascent": {"weight": 120},
                 "summit": {"weight": 0}, "pinnacle": {"weight": 0}},
    "rare": {"haven": {"quality": 5.0, "weight": 100}, "frontier": {"quality": 2.5, "weight": 500},
             "ascent": {"quality": 2.5, "weight": 290}, "summit": {"weight": 100}, "pinnacle": {"weight": 100}},
    "epic": {"haven": {"weight": 10}, "frontier": {"quality": 5.0, "weight": 100},
             "ascent": {"quality": 5.0, "weight": 540}, "summit": {"quality": 2.5, "weight": 650},
             "pinnacle": {"quality": 2.5, "weight": 650}},
    "mythic": {"haven": {"weight": 0}, "frontier": {"weight": 0}, "ascent": {"quality": 5.0, "weight": 50},
               "summit": {"quality": 10.0, "weight": 250}, "pinnacle": {"quality": 10.0, "weight": 250}},
}
_LATE = {"cracked": {"weight": 0}, "chipped": {"weight": 0}, "flawed": {"weight": 100}, "normal": {"weight": 330},
         "flawless": {"weight": 470}, "perfect": {"quality": 5.0, "weight": 100}}
PURITY = {
    "haven": {"cracked": {"weight": 230}, "chipped": {"weight": 540}, "flawed": {"quality": 2.5, "weight": 180},
              "normal": {"quality": 1.0, "weight": 50}, "flawless": {"weight": 0}, "perfect": {"weight": 0}},
    "frontier": {"cracked": {"weight": 20}, "chipped": {"weight": 250}, "flawed": {"quality": 2.5, "weight": 560},
                 "normal": {"quality": 5.0, "weight": 160}, "flawless": {"quality": 1.0, "weight": 10},
                 "perfect": {"weight": 0}},
    "ascent": {"cracked": {"weight": 0}, "chipped": {"weight": 80}, "flawed": {"quality": 2.5, "weight": 310},
               "normal": {"quality": 5.0, "weight": 580}, "flawless": {"quality": 5.0, "weight": 20},
               "perfect": {"weight": 10}},
    "summit": _LATE, "pinnacle": _LATE,
}
CATEGORY_EXTRA = {"silentgear:axe": "apotheosis:melee_weapon", "silentgear:mace": "apotheosis:melee_weapon",
                  "allthemodium:alloy_paxel": "apotheosis:breaker"}


def load_defaults():
    data = {}
    for jar in MODS.glob("*.jar"):
        with zipfile.ZipFile(jar) as z:
            for name in z.namelist():
                if name.startswith("data/apo") and name.endswith(".json"):
                    data[name[len("data/"):]] = json.loads(z.read(name))
    return data


def main():
    d = load_defaults()
    written = []

    def put(rel, obj):
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")
        written.append(rel)

    def get(rel):
        if rel not in d:
            raise SystemExit(f"missing default {rel}: did a mod update rename it?")
        return json.loads(json.dumps(d[rel]))

    for item, tiers in DOUBLE.items():
        rel = f"apotheosis/affix_loot_entries/{item}.json"
        obj = get(rel)
        w = obj["weights"]
        if tiers == ["*"]:
            w["weight"] *= 2
        else:
            for t in tiers:
                w[t]["weight"] *= 2
        put(rel, obj)
    twilight = sorted(r for r in d if r.startswith("apotheosis/affix_loot_entries/twilight/"))
    for rel in twilight:
        obj = get(rel)
        obj["constraints"] = TWILIGHT_DIM
        for t in TWILIGHT_DOUBLE.get(rel.rsplit("/", 1)[1][:-5], []):
            obj["weights"][t]["weight"] *= 2
        put(rel, obj)
    for item in GOLD_OFF:
        rel = f"apotheosis/affix_loot_entries/{item}.json"
        obj = get(rel)
        obj["neoforge:conditions"] = OFF
        put(rel, obj)
    for gs in GEAR_SETS_OFF:
        rel = f"apotheosis/gear_sets/{gs}.json"
        obj = get(rel)
        obj["neoforge:conditions"] = OFF
        put(rel, obj)
    for mod, chances in LOOT_CHANCES.items():
        rel = f"apotheosis/loot_modifiers/{mod}.json"
        obj = get(rel)
        for i, c in chances.items():
            obj["entries"][i]["chance"] = c
        put(rel, obj)
    for loc in ROLLS_X2:
        ns, path = loc.split(":", 1)
        rel = f"{ns}/{path}.json"
        obj = get(rel)
        r = obj["pools"][0]["rolls"]
        r["min"], r["max"] = r["min"] * 2, r["max"] * 2
        if rel.endswith("chest_valuable.json"):
            r2 = obj["pools"][1]["rolls"]
            r2["min"], r2["max"] = r2["min"] * 2, r2["max"] * 2
        put(rel, obj)
    for rarity, weights in RARITIES.items():
        rel = f"apotheosis/rarities/{rarity}.json"
        obj = get(rel)
        obj["weights"] = weights
        put(rel, obj)
    rel = "apotheosis/purity_weights/weights.json"
    obj = get(rel)
    obj["weights"] = PURITY
    put(rel, obj)
    rel = "apotheosis/apothic_augments/random_affix_items.json"
    obj = get(rel)
    obj["application_chance"] = 0.3
    put(rel, obj)
    # Miner's Fervor can't simply be removed: Apothic Enchanting puts it in #minecraft:non_treasure, and a missing entry
    # makes that tag (and the enchanting-table, trade, random-loot and Create enchanter tags built on it) fail to load.
    # So it stays registered (weight 1 is the game's minimum; 0 fails to parse) with a cost no table reaches, and
    # server_scripts/phase5_apotheosis.js takes it out of #minecraft:non_treasure, which every table/trade/loot tag uses.
    rel = "apothic_enchanting/enchantment/miners_fervor.json"
    obj = get(rel)
    obj["weight"] = 1
    obj["min_cost"]["base"] = 1000
    obj["max_cost"]["base"] = 1001
    put(rel, obj)
    # This path also exists in Neo Vitae's jar; ours replaces it, so keep its entry and add ours.
    rel = "apotheosis/data_maps/item/loot_category_overrides.json"
    obj = get(rel)
    obj["values"].update(CATEGORY_EXTRA)
    put(rel, obj)
    print(f"wrote {len(written)} Apotheosis tuning files into {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
