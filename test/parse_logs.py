#!/usr/bin/env python3
"""Read a collected log folder and print a pass/fail summary.

Checks: missing dependencies, mixin errors, KubeJS script errors, recipe
errors, conflicting registrations, crash reports, and startup time.
Exits 0 on pass, 1 on fail.
"""
import argparse
import pathlib
import re
import sys

# (label, regex, fails the test?)
CHECKS = [
    ("Missing dependencies", r"(Missing or unsupported mandatory dependencies|requires .* which is missing|Mod .* requires)", True),
    ("Mixin errors", r"(Mixin apply.*failed|MixinApplyError|InvalidMixinException|Mixin transformation of .* failed|Critical injection failure)", True),
    ("KubeJS script errors", r"(\[ERR \]|Error loading KubeJS script|ScriptRuntimeError|EcmaError)", True),
    ("Recipe errors", r"(Parsing error loading recipe|Couldn't parse data file .*recipe|Failed to load recipe|Unknown recipe serializer)", True),
    ("Conflicting registrations", r"(Duplicate registration|already registered|Registry .* contains duplicate|Duplicate (?:mod|key))", True),
    ("Worldgen errors", r"(Feature placement failed|Failed to (?:parse|load) .*worldgen|Unknown registry key in .*worldgen|Error placing feature)", True),
    ("Loot table errors", r"Couldn't parse element .*loot_table", True),
    ("Exceptions (info)", r"^\s*(?:Caused by: )?[a-zA-Z0-9_.$]+(?:Exception|Error): ", False),
]


KNOWN_FILE = pathlib.Path(__file__).with_name("known_issues.txt")
KNOWN = [re.compile(l.strip()) for l in KNOWN_FILE.read_text().splitlines()
         if l.strip() and not l.startswith("#")] if KNOWN_FILE.exists() else []
known_hits = set()


def is_known(line):
    if any(k.search(line) for k in KNOWN):
        known_hits.add(line.strip()[:200])
        return True
    return False


def scan(text, pattern):
    rx = re.compile(pattern, re.MULTILINE)
    return [line for line in text.splitlines() if rx.search(line) and not is_known(line)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logdir")
    ap.add_argument("--started", type=int, default=0)
    ap.add_argument("--elapsed", type=int, default=0)
    ap.add_argument("--client", action="store_true", help="client log: skip the Done check")
    args = ap.parse_args()
    d = pathlib.Path(args.logdir)

    texts = {}
    for name in ("latest.log", "console.out"):
        p = d / name
        if p.exists():
            texts[name] = p.read_text(errors="replace")
    main_log = texts.get("latest.log") or texts.get("console.out", "")
    kubejs = "\n".join(p.read_text(errors="replace") for p in (d / "kubejs").glob("*.log")) if (d / "kubejs").exists() else ""
    crashes = sorted((d / "crash-reports").glob("*.txt")) if (d / "crash-reports").exists() else []

    failed = False
    print("\n================ SMOKE TEST SUMMARY ================")
    done = re.search(r"Done \(([0-9.]+)s\)!", main_log)
    if args.client:
        joined = re.search(r"joined the game", main_log)
        print(f"[{'PASS' if joined else 'INFO'}] Client log{' (world joined)' if joined else ' (no world joined)'}")
    elif args.started and done:
        print(f"[PASS] Server reached Done in {done.group(1)}s (wall clock {args.elapsed}s)")
    else:
        print(f"[FAIL] Server did not reach Done (waited {args.elapsed}s)")
        failed = True

    if crashes:
        failed = True
        print(f"[FAIL] Crash reports: {len(crashes)}")
        for c in crashes:
            print(f"       {c.name}")

    for label, pattern, fatal in CHECKS:
        source = main_log + ("\n" + kubejs if "KubeJS" in label else "")
        hits = scan(source, pattern)
        if not hits:
            print(f"[ OK ] {label}: none")
            continue
        tag = "FAIL" if fatal else "INFO"
        failed |= fatal
        print(f"[{tag}] {label}: {len(hits)}")
        for h in hits[:8]:
            print(f"       {h.strip()[:200]}")
        if len(hits) > 8:
            print(f"       ... {len(hits) - 8} more")

    # Anything logged at ERROR that no check above covered, so nothing slips through.
    covered = re.compile("|".join(p for _, p, _ in CHECKS))
    other = [l for l in main_log.splitlines()
             if "/ERROR]" in l and not covered.search(l) and not is_known(l)]
    if other:
        print(f"[INFO] Other ERROR lines: {len(other)}")
        for h in other[:8]:
            print(f"       {h.strip()[:200]}")
    if known_hits:
        print(f"[ OK ] Known harmless issues (test/known_issues.txt): {len(known_hits)}")

    print("RESULT:", "FAIL" if failed else "PASS")
    print("====================================================")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
