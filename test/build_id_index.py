#!/usr/bin/env python3
"""Build test/ids.tsv: every item/block id (from lang files) and dimension id in the pack.

Sources: the vanilla 1.21.1 client jar (from Prism's library cache) and every jar in
test/server/mods (run test/smoke.sh first so the mods folder is current).
Used by tools/build_quests.py to refuse unknown ids.
"""
import glob
import json
import pathlib
import sys
import re
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
_PRISM = {"darwin": "Library/Application Support/PrismLauncher", "win32": "AppData/Roaming/PrismLauncher"}.get(
    sys.platform, ".local/share/PrismLauncher")
VANILLA = pathlib.Path.home() / _PRISM / "libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
VANILLA_DIMS = ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"]


def scan_lang(text, out):
    try:
        data = json.loads(text)
    except ValueError:
        return
    for key, value in data.items():
        k = re.match(r"^(item|block|fluid|entity)\.([a-z0-9_]+)\.([a-z0-9_/]+)$", key)
        if k:
            out.add((f"{k.group(2)}:{k.group(3)}", k.group(1), value))


def scan(jar, out):
    try:
        z = zipfile.ZipFile(jar)
    except zipfile.BadZipFile:
        return
    for name in z.namelist():
        if re.match(r"assets/([^/]+)/lang/en_us\.json$", name):
            scan_lang(z.read(name).decode("utf-8", "replace"), out)
        d = re.match(r"data/([^/]+)/dimension/([a-z0-9_/]+)\.json$", name)
        if d:
            out.add((f"{d.group(1)}:{d.group(2)}", "dimension", ""))
        w = re.match(r"data/([^/]+)/worldgen/(structure|biome)/([a-z0-9_/]+)\.json$", name)
        if w:
            out.add((f"{w.group(1)}:{w.group(3)}", w.group(2), ""))


def main():
    rows = set((dim, "dimension", "") for dim in VANILLA_DIMS)
    if not VANILLA.exists():
        raise SystemExit(f"Vanilla client jar not found: {VANILLA} (launch the Prism instance once)")
    scan(VANILLA, rows)
    for jar in glob.glob(str(ROOT / "test/server/mods/*.jar")):
        scan(jar, rows)
    # Items registered by the pack's own KubeJS startup scripts: event.create('name')
    for js in glob.glob(str(ROOT / "pack/kubejs/startup_scripts/*.js")):
        for name in re.findall(r"event\.create\('([a-z0-9_]+)'\)", pathlib.Path(js).read_text(encoding="utf-8")):
            rows.add((f"kubejs:{name}", "item", "(KubeJS)"))
    # Blocks, fluids and buckets other mods register from KubeJS (e.g. MI machines in
    # startup_scripts/aluminum_line.js) only have names in the pack's own lang files.
    for lang in glob.glob(str(ROOT / "pack/kubejs/assets/*/lang/en_us.json")):
        scan_lang(pathlib.Path(lang).read_text(encoding="utf-8"), rows)
    out = ROOT / "test/ids.tsv"
    out.write_text("".join(f"{i}\t{t}\t{n}\n" for i, t, n in sorted(rows)), encoding="utf-8", newline="\n")
    print(f"Wrote {out} ({len(rows)} ids)")


if __name__ == "__main__":
    main()
