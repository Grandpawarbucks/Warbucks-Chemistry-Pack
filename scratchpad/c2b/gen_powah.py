import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scratchpad/c3"))
import atm_parse
rows = atm_parse.parse("powah")
PRE = {"energy_discharger": "discharger", "energy_hopper": "hopper", "player_transmitter": "transmitter", "battery": "battery",
       "energizing_rod": "rod", "ender_cell": "ender_cell", "energy_cell": "cell", "energy_cable": "cable", "ender_gate": "gate",
       "magmator": "magmator", "furnator": "furnator", "thermo_generator": "thermo", "reactor": "reactor", "solar_panel": "solar"}
TIERS = ["starter", "basic", "hardened", "blazing", "niotic", "spirited", "nitro"]
FIXED = {"powah:thermo_generator_starter": "pw_thermo", "powah:furnator_starter": "pw_furnator", "powah:magmator_starter": "pw_magmator",
 "powah:reactor_starter": "pw_reactor_starter", "powah:ender_gate_starter": "pw_ender_gate", "powah:energy_cable_starter": "pw_cable",
 "powah:player_transmitter_starter": "pw_transmitter", "powah:energy_hopper_starter": "pw_hopper", "powah:energy_cell_starter": "pw_cell_starter",
 "powah:ender_cell_starter": "pw_ender_cell_starter", "powah:battery_starter": "pw_battery", "powah:energy_hopper_basic": "pw_hopper_up",
 "powah:ender_cell_basic": "pw_ender", "powah:battery_basic": "pw_battery_up", "powah:energy_cell_basic": "pw_powah_cell",
 "powah:furnator_basic": "pw_gen_basic", "powah:reactor_basic": "pw_powah", "powah:energizing_rod_basic": "pw_rod_up",
 "powah:player_transmitter_hardened": "pw_transmitter_up", "powah:energy_cell_hardened": "pw_cell_hardened", "powah:ender_cell_hardened": "pw_ender_up",
 "powah:energy_cable_hardened": "pw_cable_hardened", "powah:furnator_hardened": "pw_gen_hardened", "powah:reactor_hardened": "pw_reactor_hardened",
 "powah:energizing_rod_hardened": "pw_rod_hardened", "powah:energy_cable_blazing": "pw_cable_crystal", "powah:furnator_blazing": "pw_gen_blazing",
 "powah:reactor_blazing": "pw_reactor_crystal", "powah:energizing_rod_blazing": "pw_blazing_gear", "powah:furnator_niotic": "pw_gen_niotic",
 "powah:energizing_rod_niotic": "pw_niotic_gear", "powah:furnator_spirited": "pw_gen_top", "powah:energizing_rod_spirited": "pw_spirited_gear",
 "powah:energizing_rod_nitro": "pw_nitro_gear",
 "powah:steel_energized": "pw_energized", "powah:crystal_blazing": "pw_blazing", "powah:crystal_niotic": "pw_niotic",
 "powah:crystal_spirited": "pw_spirited", "powah:crystal_nitro": "pw_nitro", "powah:capacitor_basic_tiny": "pw_cap_tiny",
 "powah:capacitor_basic": "pw_capacitor"}
key_of = {}
grid = []
for i, r in enumerate(rows):
    its = [it for t in r["tasks"] for it in t[1]]
    if i == 0: key_of[r["id"]] = "pw_intro"; continue
    if i == 1: key_of[r["id"]] = "pw_paste"; continue
    if i == 2: key_of[r["id"]] = "pw_orb"; continue
    if not its: continue
    it = its[0]
    if it in FIXED and i not in (101,):
        key_of[r["id"]] = FIXED[it]
    else:
        name = it.split(":")[1]
        for pre, col in PRE.items():
            if name.startswith(pre + "_"):
                tier = name[len(pre) + 1:]
                key_of[r["id"]] = FIXED.get(it, f"pw_{col}_{tier}")
                break
    if i == 101: key_of[r["id"]] = "pw_rod_starter"
for i, r in enumerate(rows):
    if r["id"] not in key_of or i < 3: continue
    its = [it for t in r["tasks"] for it in t[1]]; cnt = r["tasks"][0][2]
    k = key_of[r["id"]]
    deps = [key_of[d] for d in r["deps"]]
    name = its[0].split(":")[1]
    col = tier = None
    for pre, c in PRE.items():
        if name.startswith(pre + "_") and name[len(pre)+1:] in TIERS:
            col, tier = c, name[len(pre)+1:]
    print(f"    ({k!r}, {name!r}, {cnt}, {r['id']!r}, {deps!r}, {int(r['opt'])}),  # {col} {tier}")
