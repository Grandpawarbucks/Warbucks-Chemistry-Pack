#!/usr/bin/env python3
"""Count ore blocks in a generated world by reading its region (.mca) files.

Usage: test/ore_scan.py [world_dir] [--dim overworld|nether|end]
Prints counts of every block whose id contains "ore", grouped by mod, so we can
confirm modded ores generate and spot duplicates (e.g. two kinds of tin ore).
No dependencies: minimal NBT reader + 1.18+ paletted block-state unpacking.
"""
import argparse
import collections
import gzip
import math
import pathlib
import struct
import sys
import zlib


# --- minimal NBT reader -------------------------------------------------------
class Reader:
    def __init__(self, data):
        self.d, self.i = data, 0

    def take(self, n):
        b = self.d[self.i:self.i + n]
        self.i += n
        return b

    def u(self, fmt):
        size = struct.calcsize(fmt)
        return struct.unpack(">" + fmt, self.take(size))[0]

    def string(self):
        return self.take(self.u("H")).decode("utf-8", "replace")

    def payload(self, tag):
        if tag == 1: return self.u("b")
        if tag == 2: return self.u("h")
        if tag == 3: return self.u("i")
        if tag == 4: return self.u("q")
        if tag == 5: return self.u("f")
        if tag == 6: return self.u("d")
        if tag == 7: return self.take(self.u("i"))
        if tag == 8: return self.string()
        if tag == 9:
            t, n = self.u("b"), self.u("i")
            return [self.payload(t) for _ in range(n)]
        if tag == 10:
            out = {}
            while True:
                t = self.u("b")
                if t == 0:
                    return out
                name = self.string()
                out[name] = self.payload(t)
        if tag == 11:
            n = self.u("i")
            return struct.unpack(f">{n}i", self.take(4 * n))
        if tag == 12:
            n = self.u("i")
            return struct.unpack(f">{n}q", self.take(8 * n))
        raise ValueError(f"bad NBT tag {tag}")


def read_nbt(data):
    r = Reader(data)
    tag = r.u("b")
    r.string()
    return r.payload(tag)


# --- region / chunk parsing ---------------------------------------------------
def chunks(region_path):
    data = region_path.read_bytes()
    for idx in range(1024):
        off = int.from_bytes(data[idx * 4:idx * 4 + 3], "big")
        if off == 0:
            continue
        pos = off * 4096
        length = int.from_bytes(data[pos:pos + 4], "big")
        comp = data[pos + 4]
        raw = data[pos + 5:pos + 4 + length]
        if comp == 1:
            raw = gzip.decompress(raw)
        elif comp == 2:
            raw = zlib.decompress(raw)
        elif comp != 3:
            continue
        yield read_nbt(raw)


def count_section(section, counts):
    bs = section.get("block_states")
    if not bs:
        return
    palette = [p.get("Name", "?") for p in bs.get("palette", [])]
    ores = {i for i, n in enumerate(palette) if "ore" in n.split(":")[-1]}
    if not ores:
        return
    if len(palette) == 1 or "data" not in bs:
        counts[palette[0]] += 4096
        return
    bits = max(4, math.ceil(math.log2(len(palette))))
    per_long = 64 // bits
    mask = (1 << bits) - 1
    seen = 0
    for value in bs["data"]:
        value &= (1 << 64) - 1  # signed → unsigned
        for _ in range(per_long):
            if seen == 4096:
                break
            i = value & mask
            if i in ores:
                counts[palette[i]] += 1
            value >>= bits
            seen += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("world", nargs="?", default=str(pathlib.Path(__file__).parent / "server/world"))
    ap.add_argument("--dim", default="overworld", choices=["overworld", "nether", "end"])
    args = ap.parse_args()
    sub = {"overworld": "region", "nether": "DIM-1/region", "end": "DIM1/region"}[args.dim]
    regions = sorted(pathlib.Path(args.world, sub).glob("*.mca"))
    if not regions:
        sys.exit(f"No region files in {args.world}/{sub}")

    counts, nchunks = collections.Counter(), 0
    for rp in regions:
        for chunk in chunks(rp):
            if chunk.get("Status", "").split(":")[-1] != "full":
                continue
            nchunks += 1
            for s in chunk.get("sections", []):
                count_section(s, counts)

    print(f"Scanned {nchunks} full chunks in {len(regions)} region file(s) ({args.dim})")
    by_mod = collections.defaultdict(list)
    for name, n in counts.items():
        by_mod[name.split(":")[0]].append((name, n))
    for mod in sorted(by_mod):
        total = sum(n for _, n in by_mod[mod])
        print(f"\n{mod}  ({total} ore blocks)")
        for name, n in sorted(by_mod[mod], key=lambda x: -x[1]):
            print(f"  {n:8}  {name}")


if __name__ == "__main__":
    main()
