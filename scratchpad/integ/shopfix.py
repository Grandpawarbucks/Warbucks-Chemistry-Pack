import ast, pathlib, json, sys, io, contextlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    import quest_data as qd
QS = {q.key: q for c in qd.CHAPTERS for q in c.quests}
FIX = {
 "shop_gear.py": {
  "iron_tools": ["gs_irontools", "gs_ironpick"], "create_goggles": ["cr_goggles", "cr_wrench"],
  "ferricore_tools": ["jdt_tools_t1", "jdt_fc_axe", "jdt_fc_shovel"], "ferricore_armor": "hv_ferricore_set",
  "blazegold_tools": ["jdt_tools_t2", "jdt_bg_axe", "jdt_bg_shovel", "jdt_blazegold_kit"], "blazegold_armor": "hv_blazegold_set",
  "celestigem_tools": ["jdt_tools_t3", "jdt_cg_paxel"], "celestigem_armor": ["jdt_celestigem_armor", "jdt_cg_leggings", "jdt_cg_boots"],
  "bp_smelting": ["sto_bp_smelting", "sto_bp_auto_smelting"], "bp_deposit": ["sto_bp_deposit", "sto_bp_restock"],
  "bp_pump": ["sto_bp_pump", "sto_bp_xp_pump"], "bp_compacting": ["sto_bp_compacting", "sto_bp_filter"],
  "bp_advanced": ["sto_bp_advanced", "sto_bp_adv_magnet", "sto_bp_adv_filter"],
  "barrels": ["sto_vanilla", "sto_barrel"], "drawer_tiers": ["sto_fs_tiers", "sto_fs_gold"],
  "greater_discount": "ars_discount", "cloggrum_tools": "ug_cloggrum_tools",
  "forgotten_tools": ["ug_forgotten_kit", "ug_forgotten_tools"], "ae_tools": ["ae_tools", "ae_memory_card"],
  "eclipse_tools": ["jdt_ec_pickaxe", "jdt_ec_axe", "jdt_ec_shovel", "jdt_eclipse_kit"],
  "mekasuit": ["mkp_meka_helmet", "mkp_meka_body", "mk2_mekasuit_full", "mkp_meka_boots"],
  "space_suit": ["t7_suit_full", "t7_suit"]},
 "market.py": {"osmium_compressor": "mk2_compressor", "centrifuge": "t4_centrifuge", "neutron_activator": "t6_sna"},
 "shop_world.py": {"wheat": "fd_wheat", "flax_seeds": "fd_flax_seeds", "wigglewood_sapling": "ug_wigglewood_sapling",
  "grongle_sapling": "ug_grongle_sapling", "droopvine": "ug_droopvine", "indigo_mushroom": "ug_indigo_mushroom",
  "ink_mushroom": "ug_ink_mushroom", "veil_mushroom": "ug_veil_mushroom"},
}
DEPIDX = {"shop_gear.py": 4, "market.py": 3, "shop_world.py": 5}
for fn, fixes in FIX.items():
    p = ROOT / "tools/quests" / fn
    src = p.read_text(encoding="utf-8")
    lines = src.split("\n")
    starts = [0]
    for l in lines: starts.append(starts[-1] + len(l) + 1)
    off = lambda ln, col: starts[ln - 1] + len(lines[ln - 1].encode()[:col].decode())
    eds = []
    seen = set()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("buy", "g", "shop_entry") \
                and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value in fixes:
            name = n.args[0].value
            a = n.args[DEPIDX[fn]]
            assert isinstance(a, ast.Constant) and a.value in QS, (fn, name, ast.dump(a))
            new = fixes[name]
            for d in ([new] if isinstance(new, str) else new):
                assert d in QS, d
            lit = f'"{new}"' if isinstance(new, str) else "(" + ", ".join(f'"{d}"' for d in new) + ")"
            eds.append((off(a.lineno, a.col_offset), off(a.end_lineno, a.end_col_offset), lit))
            seen.add(name)
            # dep title (shop_gear/market): the next positional arg
            if fn != "shop_world.py" and isinstance(new, str):
                t = n.args[DEPIDX[fn] + 1]
                if isinstance(t, ast.Constant) and isinstance(t.value, str):
                    eds.append((off(t.lineno, t.col_offset), off(t.end_lineno, t.end_col_offset), json.dumps(QS[new].title, ensure_ascii=False)))
    assert seen == set(fixes), set(fixes) - seen
    for a, b, t in sorted(eds, reverse=True):
        src = src[:a] + t + src[b:]
    if fn == "shop_world.py":
        add = ", ".join(f'"{d}": {json.dumps(QS[d].title, ensure_ascii=False)}' for d in fixes.values())
        src = src.replace("TITLES = {\n", "TITLES = {\n    " + add + ",\n", 1)
    if fn == "shop_gear.py":
        src = src.replace("return Q(f\"sg_buy_{name}\", x, y, [cost], title, deps=[dep], items=items,",
                          "deps = list(dep) if isinstance(dep, (list, tuple)) else [dep]  # a kit unlocks once every piece is made\n"
                          "    return Q(f\"sg_buy_{name}\", x, y, [cost], title, deps=deps, items=items,")
        src = src.replace("def buy(name, title, items, price, dep, dep_title, what, greater=False):\n    \"\"\"One shop entry: pay `price` (Greater) tokens, get `items` [(id, count), ...]. Placed on the current block.\"\"\"",
                          "def buy(name, title, items, price, dep, dep_title, what, greater=False):\n    \"\"\"One shop entry: pay `price` (Greater) tokens, get `items` [(id, count), ...]. Placed on the current block.\n    `dep` is a quest key, or a tuple of keys for a kit whose pieces are made in separate quests.\"\"\"")
    p.write_text(src, encoding="utf-8", newline="\n")
    print(fn, len(eds))
