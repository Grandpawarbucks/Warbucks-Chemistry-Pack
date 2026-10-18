#!/usr/bin/env python3
"""Build test/ids.tsv: every item/block id (from lang files) and dimension id in the pack.

Sources: the vanilla 1.21.1 client jar (from Prism's library cache) and every jar in
test/server/mods (run test/smoke.sh first so the mods folder is current).
Used by tools/build_quests.py to refuse unknown ids.
"""
import glob
import json
import pathlib
import re
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
VANILLA = pathlib.Path.home() / "Library/Application Support/PrismLauncher/libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
VANILLA_DIMS = ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"]


def scan(jar, out):
    try:
        z = zipfile.ZipFile(jar)
    except zipfile.BadZipFile:
        return
    for name in z.namelist():
        m = re.match(r"assets/([^/]+)/lang/en_us\.json$", name)
        if m:
            try:
                data = json.loads(z.read(name).decode("utf-8", "replace"))
            except ValueError:
                continue
            for key, value in data.items():
                k = re.match(r"^(item|block|fluid)\.([a-z0-9_]+)\.([a-z0-9_/]+)$", key)
                if k:
                    out.add((f"{k.group(2)}:{k.group(3)}", k.group(1), value))
        d = re.match(r"data/([^/]+)/dimension/([a-z0-9_/]+)\.json$", name)
        if d:
            out.add((f"{d.group(1)}:{d.group(2)}", "dimension", ""))


def main():
    rows = set((dim, "dimension", "") for dim in VANILLA_DIMS)
    if not VANILLA.exists():
        raise SystemExit(f"Vanilla client jar not found: {VANILLA} (launch the Prism instance once)")
    scan(VANILLA, rows)
    for jar in glob.glob(str(ROOT / "test/server/mods/*.jar")):
        scan(jar, rows)
    out = ROOT / "test/ids.tsv"
    out.write_text("".join(f"{i}\t{t}\t{n}\n" for i, t, n in sorted(rows)))
    print(f"Wrote {out} ({len(rows)} ids)")


if __name__ == "__main__":
    main()
