#!/usr/bin/env python3
"""Generate ore-deposit worldgen (GregTech-vein feel, vanilla datapack format) into pack/kubejs/data.

For each main MI metal:
  1. Scattered ore: MI's placed features are overridden with ~35% of their original count, so
     random strip-mining finds less.
  2. Deposits: in about 1 of every N chunks, K large ore blobs (size 32, ~95 ores each) cluster in a narrow depth
     band, forming one rich deposit worth prospecting for (Nature's Compass, Ultimine, Jade).
Everything uses vanilla feature types (minecraft:ore, rarity_filter, height_range), no extra mod.
Run: python3 tools/build_deposits.py, then smoke + worldgen + test/ore_scan.py to measure.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "pack/kubejs/data"
MI = "modern_industrialization"
SCATTER = 0.35  # fraction of MI's original scattered-ore count that remains

BLOB_SIZE = 32  # measured: a size-32 ore blob places ~95 blocks (size 64 placed ~465, far too many)

# Calibrated with test/ore_scan.py (radius 384, seed 20261018). Baseline ore per chunk: tin 82,
# lead 139, bauxite 99, nickel 43, antimony 48, uranium 20, tungsten 15. Blobs are chosen so deposits
# add ~40% of the baseline, and scattered ore keeps 35%: ~75% of the original total, but concentrated.
# metal: (original MI count per chunk-feature, deposit 1-in-N chunks, blobs per deposit, (min Y, max Y))
DEPOSITS = {
    "tin":      (16, 18, 6, (-8, 24)),
    "lead":     (32, 16, 9, (-24, 16)),
    "bauxite":  (24, 18, 7, (-16, 24)),
    "nickel":   (14, 22, 4, (-32, 8)),
    "antimony": (20, 24, 5, (-24, 16)),
    "uranium":  (8,  30, 3, (-56, -24)),
    "tungsten": (6,  30, 2, (-56, -32)),
}


# Allthemodium's Mining dimension (user decision 2026-10-19): rich veins of the common, non-milestone metals so the
# mining world is worth the trip. Milestone metals (platinum, iridium, uranium, osmium, tungsten, fluorite...) stay out:
# they come from chemistry. The dimension is flat: deepslate Y 65-128, stone Y 129-247, so veins sit in Y 65-240.
# metal: (stone ore block, deepslate ore block, veins per chunk, vein size, (min Y, max Y))
MINING_BIOMES = "#allthemodium:mining_features/mining_biomes"
MINING = {
    "tin":     (f"{MI}:tin_ore", f"{MI}:deepslate_tin_ore", 30, 9, (65, 200)),
    "lead":    (f"{MI}:lead_ore", f"{MI}:deepslate_lead_ore", 30, 9, (65, 160)),
    "nickel":  (f"{MI}:nickel_ore", f"{MI}:deepslate_nickel_ore", 20, 9, (65, 140)),
    "silver":  ("mekanism:silver_ore", "mekanism:deepslate_silver_ore", 16, 8, (65, 140)),  # MI has no silver ore
    "bauxite": (f"{MI}:bauxite_ore", f"{MI}:deepslate_bauxite_ore", 30, 9, (120, 240)),
}


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")


def height(lo, hi):
    return {"type": "minecraft:height_range",
            "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": lo}, "max_inclusive": {"absolute": hi}}}


def main():
    for metal, (orig, n, blobs, (lo, hi)) in DEPOSITS.items():
        # 1. Reduce MI's scattered ore: recreate MI's placed features (same height ranges as MI's
        #    originals, checked in its jar) with a lower count.
        mi_range = {"tin": 64, "lead": 64, "bauxite": 32, "nickel": 64, "antimony": 64, "uranium": 16, "tungsten": 20}[metal]
        for prefix in ("", "deepslate_"):
            write(DATA / MI / "worldgen/placed_feature" / f"{prefix}ore_generator_{metal}.json", {
                "feature": f"{MI}:{prefix}ore_generator_{metal}",
                "placement": [
                    {"type": "minecraft:count", "count": max(1, round(orig * SCATTER))},
                    {"type": "minecraft:in_square"},
                    {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                        "max_inclusive": {"absolute": mi_range}, "min_inclusive": {"above_bottom": 0}}},
                    {"type": "minecraft:biome"}]})

        # 2. Deposit: one big ore feature replacing stone and deepslate with the right ore variant.
        write(DATA / "warbucks/worldgen/configured_feature" / f"deposit_{metal}.json", {
            "type": "minecraft:ore",
            "config": {"size": BLOB_SIZE, "discard_chance_on_air_exposure": 0.0, "targets": [
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
                 "state": {"Name": f"{MI}:{metal}_ore"}},
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                 "state": {"Name": f"{MI}:deepslate_{metal}_ore"}}]}})
        write(DATA / "warbucks/worldgen/placed_feature" / f"deposit_{metal}.json", {
            "feature": f"warbucks:deposit_{metal}",
            "placement": [
                {"type": "minecraft:rarity_filter", "chance": n},   # only 1 in n chunks has a deposit
                {"type": "minecraft:count", "count": blobs},        # many blobs in that chunk...
                {"type": "minecraft:in_square"},
                height(lo, hi),                                     # ...packed into a narrow depth band
                {"type": "minecraft:biome"}]})
        write(DATA / "warbucks/neoforge/biome_modifier" / f"deposit_{metal}.json", {
            "type": "neoforge:add_features", "biomes": "#minecraft:is_overworld",
            "features": f"warbucks:deposit_{metal}", "step": "underground_ores"})
    for metal, (stone, deep, count, size, (lo, hi)) in MINING.items():
        write(DATA / "warbucks/worldgen/configured_feature" / f"mining_{metal}.json", {
            "type": "minecraft:ore",
            "config": {"size": size, "discard_chance_on_air_exposure": 0.0, "targets": [
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
                 "state": {"Name": stone}},
                {"target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                 "state": {"Name": deep}}]}})
        write(DATA / "warbucks/worldgen/placed_feature" / f"mining_{metal}.json", {
            "feature": f"warbucks:mining_{metal}",
            "placement": [{"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
                          height(lo, hi), {"type": "minecraft:biome"}]})
    write(DATA / "warbucks/neoforge/biome_modifier/mining_ores.json", {
        "type": "neoforge:add_features", "biomes": MINING_BIOMES,
        "features": [f"warbucks:mining_{m}" for m in MINING], "step": "underground_ores"})
    print(f"Wrote deposits for {len(DEPOSITS)} metals and Mining-dimension veins for {len(MINING)} into "
          f"{DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
