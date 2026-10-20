"""Quest chapter: powah (side page). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Powah" chapter (user decision 2026-10-20: quest for quest where we have the mod; same items,
order, clusters and sizes; the text is ours). All 108 of its item quests are here: the start, the Energizing Orb, the
seven tier quests (tiny and basic capacitors, energized steel and the four crystals) and the 14 x 7 grid of blocks,
one quest per block per tier, wired the way ATM10 wires them. ATM10's credits checkmark is skipped. Its first quest
asks for raw uraninite, which this pack doesn't generate (Powah ore is off), so ours is a checkmark.
Pack gates (STYLE.md "Pack facts"): the Energizing Orb needs an MI electronic circuit (MV), uraninite is made in MI's
Chemical Reactor (Powah's shortcut is removed). Starter reactor blocks therefore also depend on t4_uraninite, and the
starter ender cell and gate (their Ender Core is made in the Orb) on pw_orb.
The grid's quests live in GRID: (key, item, count, ATM10 quest id, deps, optional). Existing keys are kept for the
blocks they already asked for; the Powah quests that used to sit in power.py moved here with their keys.
Our own Powah quests ATM10 doesn't have (manual, wrench, rods, casing, pearl, panes, cards, snowball, hardened
capacitors, ender core, dry ice, the nitro block) stay as optional side quests.
"""
from questlib import Q, Chapter, item, tick, anyof, MAIN, SIDE  # noqa: F401

P = "powah:"
OPT = dict(optional=True, tokens=1)
TIERS = ["starter", "basic", "hardened", "blazing", "niotic", "spirited", "nitro"]
SECTION = {t: f"{t.title()} Tier" for t in TIERS}
S_START, S_SIDE = "Getting Started", "Side Projects"

# Block family -> (item prefix, display name, what it does)
COLS = {
    "discharger": ("energy_discharger", "Energy Discharger", "pulls FE back out of items placed in it and sends it on to the grid."),
    "hopper": ("energy_hopper", "Energy Hopper", "charges the FE items in the container it faces."),
    "transmitter": ("player_transmitter", "Player Transmitter", "charges the FE items carried by the player bound to it, wirelessly."),
    "battery": ("battery", "Battery", "is an item that holds FE you can carry and use to charge gear."),
    "rod": ("energizing_rod", "Energizing Rod", "pours FE into the Energizing Orb; more and better rods charge it faster."),
    "ender_cell": ("ender_cell", "Ender Cell", "shares one energy pool with every ender block on the same channel, wherever it is."),
    "cell": ("energy_cell", "Energy Cell", "stores FE and passes it on to cells next to it."),
    "cable": ("energy_cable", "Energy Cable", "carries FE; each tier carries more per tick."),
    "gate": ("ender_gate", "Ender Gate", "taps the ender network wherever you place it, without storing much itself."),
    "magmator": ("magmator", "Magmator", "burns lava and other hot fluids for FE."),
    "furnator": ("furnator", "Furnator", "burns furnace fuel for FE."),
    "thermo": ("thermo_generator", "Thermo Generator", "makes FE from a hot block underneath and a coolant fed in."),
    "reactor": ("reactor", "Reactor", "blocks stack into one multiblock reactor that burns uraninite."),
    "solar": ("solar_panel", "Solar Panel", "makes FE from daylight."),
}
PREFIX = {v[0]: k for k, v in COLS.items()}
MAT = {"starter": "tiny capacitors and a dielectric casing", "basic": "basic capacitors",
       "hardened": "energized steel and hardened capacitors", "blazing": "blazing crystals and blazing capacitors",
       "niotic": "niotic crystals and niotic capacitors", "spirited": "spirited crystals and spirited capacitors",
       "nitro": "nitro crystals and nitro capacitors"}
TIP = {"starter": "starter blocks need no Energizing Orb, so they work from your first day of power.",
       "basic": "basic blocks still need no Orb: basic capacitors are iron, paste and a redstone block.",
       "hardened": "hardened parts start from energized steel, made in the Energizing Orb.",
       "blazing": "blazing crystals are energized blaze rods; see the Blazing quest at the start of this row.",
       "niotic": "niotic crystals are energized diamonds; see the Niotic quest at the start of this row.",
       "spirited": "spirited crystals are energized emeralds; see the Spirited quest at the start of this row.",
       "nitro": "nitro crystals take a Nether Star and twenty million FE; see the Nitro quest at the start of this row."}
XP = {"starter": 30, "basic": 40, "hardened": 60, "blazing": 80, "niotic": 100, "spirited": 125, "nitro": 150}
# Pack gates on top of ATM10's deps (see the module docstring).
EXTRA_DEPS = {"pw_reactor_starter": ["t4_uraninite"], "pw_ender_cell_starter": ["pw_orb"], "pw_ender_gate": ["pw_orb"]}

GRID = [
    ('pw_thermo', 'thermo_generator_starter', 1, '52E59FCB39D66BCF', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_furnator', 'furnator_starter', 1, '3D5F87F8E6B89C1B', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_solar_starter', 'solar_panel_starter', 1, '7678B5DD1339833E', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_magmator', 'magmator_starter', 1, '0FD62827710F0AC6', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_reactor_starter', 'reactor_starter', 36, '1B0087400B0B8B49', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_ender_gate', 'ender_gate_starter', 1, '3CB6DC5B09C62CFE', ['pw_cable', 'pw_cap_tiny'], 0),
    ('pw_cable', 'energy_cable_starter', 1, '7D52DD751DDADA1B', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_transmitter', 'player_transmitter_starter', 1, '677365A816994C8B', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_hopper', 'energy_hopper_starter', 1, '5BCA3F716348ECCD', ['pw_paste', 'pw_cap_tiny'], 1),
    ('pw_discharger_starter', 'energy_discharger_starter', 1, '33816AF0E699F19F', ['pw_paste', 'pw_cap_tiny'], 1),
    ('pw_cell_starter', 'energy_cell_starter', 1, '78202A1CF5D86B94', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_ender_cell_starter', 'ender_cell_starter', 1, '700F3FF7C23D0C0F', ['pw_cell_starter', 'pw_battery', 'pw_cap_tiny'], 0),
    ('pw_battery', 'battery_starter', 1, '61A8FAEC4FF18449', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_discharger_basic', 'energy_discharger_basic', 1, '5A07C7A54D40FBE2', ['pw_capacitor'], 1),
    ('pw_hopper_up', 'energy_hopper_basic', 1, '35F885A046EAE246', ['pw_hopper', 'pw_capacitor'], 1),
    ('pw_transmitter_basic', 'player_transmitter_basic', 1, '740F314EE6242C13', ['pw_transmitter', 'pw_capacitor'], 0),
    ('pw_battery_up', 'battery_basic', 1, '04F11E192A334E3F', ['pw_battery', 'pw_capacitor'], 0),
    ('pw_ender', 'ender_cell_basic', 1, '0C481BA4C1CC0237', ['pw_orb', 'pw_capacitor'], 0),
    ('pw_powah_cell', 'energy_cell_basic', 1, '66FA15A92DC655DE', ['pw_cell_starter', 'pw_paste', 'pw_capacitor'], 0),
    ('pw_cable_basic', 'energy_cable_basic', 1, '5A708BF4F5091959', ['pw_cable', 'pw_capacitor'], 0),
    ('pw_gate_basic', 'ender_gate_basic', 1, '69D82C33347D360D', ['pw_cable_basic', 'pw_capacitor'], 0),
    ('pw_magmator_basic', 'magmator_basic', 1, '0E3A9D5E1E8AAF89', ['pw_magmator', 'pw_capacitor'], 0),
    ('pw_gen_basic', 'furnator_basic', 1, '67DE5F982629BB34', ['pw_furnator', 'pw_capacitor'], 0),
    ('pw_thermo_basic', 'thermo_generator_basic', 1, '60F5DC851FCFF1B2', ['pw_thermo', 'pw_capacitor'], 0),
    ('pw_powah', 'reactor_basic', 36, '5F6152CF085D75D6', ['pw_reactor_starter', 'pw_capacitor'], 0),
    ('pw_solar_basic', 'solar_panel_basic', 1, '7890A1478121D2CD', ['pw_solar_starter', 'pw_capacitor'], 0),
    ('pw_discharger_hardened', 'energy_discharger_hardened', 1, '534485E8185B71C3', ['pw_energized'], 1),
    ('pw_hopper_hardened', 'energy_hopper_hardened', 1, '04930767C52C7CC2', ['pw_hopper_up', 'pw_energized'], 1),
    ('pw_transmitter_up', 'player_transmitter_hardened', 1, '7444B85503DE2C53', ['pw_transmitter_basic', 'pw_energized'], 0),
    ('pw_battery_hardened', 'battery_hardened', 1, '604AB95A7600B150', ['pw_battery_up', 'pw_energized'], 0),
    ('pw_cell_hardened', 'energy_cell_hardened', 1, '7FEE780F37A1322E', ['pw_powah_cell', 'pw_energized'], 0),
    ('pw_ender_up', 'ender_cell_hardened', 1, '331498A68D110F81', ['pw_energized'], 0),
    ('pw_cable_hardened', 'energy_cable_hardened', 1, '029922AB09F8C76A', ['pw_cable_basic', 'pw_energized'], 0),
    ('pw_gate_hardened', 'ender_gate_hardened', 1, '5D594154819DD145', ['pw_cable_hardened', 'pw_energized'], 0),
    ('pw_magmator_hardened', 'magmator_hardened', 1, '6ED2F8A8DEED417D', ['pw_magmator_basic', 'pw_energized'], 0),
    ('pw_gen_hardened', 'furnator_hardened', 1, '2AE17A935862BCBF', ['pw_gen_basic', 'pw_energized'], 0),
    ('pw_thermo_hardened', 'thermo_generator_hardened', 1, '6230C6884B800689', ['pw_thermo_basic', 'pw_energized'], 0),
    ('pw_reactor_hardened', 'reactor_hardened', 36, '05B0A7D0B991050F', ['pw_powah', 'pw_energized'], 0),
    ('pw_solar_hardened', 'solar_panel_hardened', 1, '6C8148B3AE0A2222', ['pw_solar_basic', 'pw_energized'], 0),
    ('pw_battery_blazing', 'battery_blazing', 1, '79421463F01ED2D7', ['pw_battery_hardened', 'pw_blazing'], 0),
    ('pw_discharger_blazing', 'energy_discharger_blazing', 1, '13FDBA4BC4514F58', ['pw_blazing'], 1),
    ('pw_hopper_blazing', 'energy_hopper_blazing', 1, '04811BA420B80046', ['pw_hopper_hardened', 'pw_blazing'], 1),
    ('pw_transmitter_blazing', 'player_transmitter_blazing', 1, '1D80E6C3327AB376', ['pw_transmitter_up', 'pw_blazing'], 0),
    ('pw_ender_cell_blazing', 'ender_cell_blazing', 1, '564F731F0F3E5AEC', ['pw_blazing'], 0),
    ('pw_cell_blazing', 'energy_cell_blazing', 1, '25088F06228F8561', ['pw_cell_hardened', 'pw_blazing'], 0),
    ('pw_cable_crystal', 'energy_cable_blazing', 1, '0C5936697C9B3716', ['pw_cable_hardened', 'pw_blazing'], 0),
    ('pw_gate_blazing', 'ender_gate_blazing', 1, '1F55B2FA187F63DD', ['pw_cable_crystal', 'pw_blazing'], 0),
    ('pw_magmator_blazing', 'magmator_blazing', 1, '0C7D0AB254DF8CF1', ['pw_magmator_hardened', 'pw_blazing'], 0),
    ('pw_gen_blazing', 'furnator_blazing', 1, '323F7A0C4FAC28D0', ['pw_gen_hardened', 'pw_blazing'], 0),
    ('pw_thermo_blazing', 'thermo_generator_blazing', 1, '44C1315098B9CF3F', ['pw_thermo_hardened', 'pw_blazing'], 0),
    ('pw_reactor_crystal', 'reactor_blazing', 36, '6754612E9AD4B9C0', ['pw_reactor_hardened', 'pw_blazing'], 0),
    ('pw_solar_blazing', 'solar_panel_blazing', 1, '7C34EED27A9737D4', ['pw_solar_hardened', 'pw_blazing'], 0),
    ('pw_discharger_niotic', 'energy_discharger_niotic', 1, '555566F1148F5229', ['pw_niotic'], 1),
    ('pw_hopper_niotic', 'energy_hopper_niotic', 1, '5A8DE0C7D4F28E05', ['pw_hopper_blazing'], 1),
    ('pw_transmitter_niotic', 'player_transmitter_niotic', 1, '2DD9994665799747', ['pw_transmitter_blazing'], 0),
    ('pw_battery_niotic', 'battery_niotic', 1, '03798EF7AB47BB3D', ['pw_battery_blazing'], 0),
    ('pw_ender_cell_niotic', 'ender_cell_niotic', 1, '1CCCA214865526F3', ['pw_niotic'], 0),
    ('pw_cell_niotic', 'energy_cell_niotic', 1, '6EFB4BF8110F2712', ['pw_cell_blazing'], 0),
    ('pw_cable_niotic', 'energy_cable_niotic', 1, '68B604EF40198B8D', ['pw_cable_crystal', 'pw_niotic'], 0),
    ('pw_gate_niotic', 'ender_gate_niotic', 1, '584BD9A6F7594867', ['pw_cable_niotic'], 0),
    ('pw_magmator_niotic', 'magmator_niotic', 1, '03442045ED56068F', ['pw_magmator_blazing'], 0),
    ('pw_gen_niotic', 'furnator_niotic', 1, '24EE138780C43447', ['pw_gen_blazing'], 0),
    ('pw_thermo_niotic', 'thermo_generator_niotic', 1, '28EE8C172F9DF5C1', ['pw_thermo_blazing'], 0),
    ('pw_reactor_niotic', 'reactor_niotic', 36, '0FFF2BEE5D8EBE12', ['pw_reactor_crystal'], 0),
    ('pw_solar_niotic', 'solar_panel_niotic', 1, '39386F88CB38CF36', ['pw_solar_blazing'], 0),
    ('pw_battery_spirited', 'battery_spirited', 1, '63E57D2745D24761', ['pw_battery_niotic'], 0),
    ('pw_transmitter_spirited', 'player_transmitter_spirited', 1, '11F0D662FF4DC335', ['pw_transmitter_niotic'], 0),
    ('pw_hopper_spirited', 'energy_hopper_spirited', 1, '18B20F4F27F37197', ['pw_hopper_niotic'], 1),
    ('pw_discharger_spirited', 'energy_discharger_spirited', 1, '0536D7B41964FE38', ['pw_spirited'], 1),
    ('pw_ender_cell_spirited', 'ender_cell_spirited', 1, '486356E189081ADC', ['pw_spirited'], 0),
    ('pw_cell_spirited', 'energy_cell_spirited', 1, '4449AD53BCE797E1', ['pw_cell_niotic'], 0),
    ('pw_cable_spirited', 'energy_cable_spirited', 1, '379EBE12E3F61679', ['pw_cable_niotic', 'pw_spirited'], 0),
    ('pw_gate_spirited', 'ender_gate_spirited', 1, '335927C2D234451A', ['pw_cable_spirited'], 0),
    ('pw_magmator_spirited', 'magmator_spirited', 1, '36B14701D95C3C21', ['pw_magmator_niotic'], 0),
    ('pw_gen_top', 'furnator_spirited', 1, '5A7C92F05AF39FDB', ['pw_gen_niotic'], 0),
    ('pw_thermo_spirited', 'thermo_generator_spirited', 1, '637A8E4BBF108417', ['pw_thermo_niotic'], 0),
    ('pw_reactor_spirited', 'reactor_spirited', 36, '341486C9F277FEB7', ['pw_reactor_niotic'], 0),
    ('pw_solar_spirited', 'solar_panel_spirited', 1, '760F80E1C273C0AD', ['pw_solar_niotic'], 0),
    ('pw_transmitter_nitro', 'player_transmitter_nitro', 1, '348FEC9A50C2E62E', ['pw_transmitter_spirited', 'pw_nitro'], 0),
    ('pw_discharger_nitro', 'energy_discharger_nitro', 1, '24510A5C98703C84', ['pw_nitro'], 1),
    ('pw_hopper_nitro', 'energy_hopper_nitro', 1, '41DC771674A6C387', ['pw_hopper_spirited', 'pw_nitro'], 1),
    ('pw_battery_nitro', 'battery_nitro', 1, '7EBA36EF1858F428', ['pw_battery_spirited', 'pw_nitro'], 0),
    ('pw_ender_cell_nitro', 'ender_cell_nitro', 1, '3B28A8BA318D438F', ['pw_nitro'], 0),
    ('pw_cell_nitro', 'energy_cell_nitro', 1, '503CD7E104C8BA5D', ['pw_cell_spirited', 'pw_nitro'], 0),
    ('pw_cable_nitro', 'energy_cable_nitro', 1, '3CD1F9E00E33C6C9', ['pw_cable_spirited', 'pw_nitro'], 0),
    ('pw_gate_nitro', 'ender_gate_nitro', 1, '44F016F465082C55', ['pw_cable_nitro', 'pw_nitro'], 0),
    ('pw_magmator_nitro', 'magmator_nitro', 1, '4E67DE071FC9D80D', ['pw_magmator_spirited', 'pw_nitro'], 0),
    ('pw_furnator_nitro', 'furnator_nitro', 1, '129F6987E144B048', ['pw_gen_top', 'pw_nitro'], 0),
    ('pw_thermo_nitro', 'thermo_generator_nitro', 1, '71D08D1C8EA4C631', ['pw_thermo_spirited', 'pw_nitro'], 0),
    ('pw_reactor_nitro', 'reactor_nitro', 36, '61DCECE1FC38E151', ['pw_reactor_spirited', 'pw_nitro'], 0),
    ('pw_solar_nitro', 'solar_panel_nitro', 1, '393050BEA59F1570', ['pw_solar_spirited', 'pw_nitro'], 0),
    ('pw_rod_starter', 'energizing_rod_starter', 1, '1C273D9E046FD18A', ['pw_paste', 'pw_cap_tiny'], 0),
    ('pw_rod_up', 'energizing_rod_basic', 1, '4EA69350A20B0B5B', ['pw_rod_starter', 'pw_capacitor'], 0),
    ('pw_rod_hardened', 'energizing_rod_hardened', 1, '09DECE4E7977D852', ['pw_rod_up', 'pw_energized'], 0),
    ('pw_blazing_gear', 'energizing_rod_blazing', 1, '172B0296F87D6725', ['pw_rod_hardened', 'pw_blazing'], 0),
    ('pw_niotic_gear', 'energizing_rod_niotic', 1, '270B5EA3E710A209', ['pw_blazing_gear', 'pw_niotic'], 0),
    ('pw_spirited_gear', 'energizing_rod_spirited', 1, '69E572EA56B3B31D', ['pw_niotic_gear', 'pw_spirited'], 0),
    ('pw_nitro_gear', 'energizing_rod_nitro', 1, '2C9EE7BE03767976', ['pw_spirited_gear', 'pw_nitro'], 0),
]

# Our own wording for some grid quests (title, subtitle, desc); the rest use the templates in grid_quest().
CUSTOM = {
    "pw_furnator": ("Furnator", "Burn fuel, make FE", [
        "&eWhat:&r a Powah generator that burns furnace fuel for FE. It's an early way to run the Dissolver.",
        "&eChemistry:&r burning oxidises carbon. Coke burns cleaner and longer than coal because its volatile tars were already driven off.",
        "&eHow:&r paste, 2 tiny capacitors, a dielectric casing and a furnace.",
        "&eTip:&r feed it coke from your coke ovens for long runs."]),
    "pw_magmator": ("Magmator", "Power from molten rock", [
        "&eWhat:&r a generator that burns lava (and other hot fluids) instead of solid fuel.",
        "&eChemistry:&r lava is molten silicate rock at roughly 700 to 1,200 °C. The Magmator draws that stored heat off as FE.",
        "&eHow:&r like the Furnator, but with a bucket in place of the furnace. JEI's Magmatic Fluids list shows what it accepts.",
        "&eTip:&r a Nether lava lake and a pump give endless fuel."]),
    "pw_thermo": ("Thermo Generator", "Power from a temperature difference", [
        "&eWhat:&r a generator that needs a hot block underneath and a coolant fed in.",
        "&eChemistry:&r thermoelectric plates make current from a temperature difference (the Seebeck effect). Hotter below and colder inside means more power.",
        "&eHow:&r thermo plates, tiny capacitors and a casing (check JEI). Place it on lava or magma and pipe water in."]),
    "pw_solar_starter": ("Starter Solar Panel", "Light straight into electricity", [
        "&eWhat:&r Powah's solar panel. It makes FE from daylight with no fuel at all.",
        "&eChemistry:&r light can knock electrons out of a material (the photoelectric effect, explained by Einstein in 1905). Solar cells collect them as current.",
        "&eHow:&r photoelectric panes, tiny capacitors and a casing (check JEI). Place it under open sky.",
        "&eTip:&r it stops at night; pair it with a cell."]),
    "pw_cable": ("Energy Cables", "Wires that know their tier", [
        "&eWhat:&r Powah's cables. Each tier carries more FE per tick.",
        "&eHow:&r 6 horizontal rods, 2 iron nuggets and a tiny capacitor make 12 starter cables.",
        "&eTip:&r cables connect to any FE block, not just Powah ones. Use the Powah wrench to configure sides."]),
    "pw_cell_starter": ("Starter Energy Cell", "A first Powah battery block", [
        "&eWhat:&r the smallest Powah cell. Enough to smooth out a Furnator's output.",
        "&eHow:&r iron ingots in the corners, tiny capacitors on the sides, a dielectric casing in the middle.",
        "&eTip:&r the basic cell is the same recipe with basic capacitors."]),
    "pw_reactor_starter": ("Starter Reactor", "Where every reactor block begins", [
        "&eWhat:&r 36 starter reactor blocks: enough for a full, if weak, reactor. Every better reactor block is crafted from these.",
        "&eChemistry:&r uranium dioxide is a ceramic: it melts near 2,865 °C, which is why real fuel pellets are UO₂ and not uranium metal.",
        "&eHow:&r 4 uraninite, 4 tiny capacitors and a dielectric casing make 4. Uraninite comes from MI's Chemical Reactor (uranium dust + oxygen).",
        "&eTip:&r all blocks in one stack must be the same tier, or they won't form one reactor."]),
    "pw_powah": ("Basic Reactor", "Uraninite-fuelled multiblock", [
        "&eWhat:&r 36 basic reactor blocks: a real Powah reactor, fuelled by the uraninite you oxidised yourself.",
        "&eChemistry:&r uraninite is UO₂. Its U-235 splits when it absorbs a neutron, releasing heat and more neutrons; the reactor turns that heat into FE.",
        "&eHow:&r 4 starter reactor blocks, 4 large capacitors and a uraninite make 4 (check JEI). Stack them and they form one reactor.",
        "&eTip:&r fuel, temperature and coolant all show in its GUI. Watch the temperature as you scale up."]),
    "pw_reactor_hardened": ("Hardened Reactor", "Rebuild the reactor a tier up", [
        "&eWhat:&r a hardened reactor, much stronger than the basic one.",
        "&eHow:&r 4 basic reactor blocks, 4 hardened capacitors and 1 uraninite make 4 hardened blocks.",
        "&eTip:&r blazing, niotic, spirited and nitro reactors follow the same recipe with that tier's capacitor."]),
    "pw_transmitter": ("Player Transmitter", "Charge your gear wirelessly", [
        "&eWhat:&r a block that charges the FE items carried by the player bound to it.",
        "&eHow:&r Player Aerial Pearl on top, tiny capacitors and a casing in the middle, an upright rod below. The Binding Card is a blank card with redstone and rotten flesh; right-click to bind it to yourself.",
        "&eTip:&r either Binding Card counts here: the plain one or the dimensional one."]),
    "pw_rod_starter": ("Starter Energizing Rod", "The rod that feeds the Orb", [
        "&eWhat:&r Energizing Rods aim FE at the Energizing Orb. Several rods stack.",
        "&eHow:&r quartz, tiny capacitors, a casing and an upright dielectric rod (check JEI).",
        "&eTip:&r rods need no Orb to make, so build a few before the Orb is ready."]),
    "pw_rod_up": ("Basic Energizing Rod", "Quartz focuses the charge", [
        "&eWhat:&r higher-tier rods pour FE into the Orb faster.",
        "&eChemistry:&r quartz is crystalline SiO₂ and is piezoelectric: squeeze it and it makes a voltage. Every quartz watch keeps time with a vibrating crystal.",
        "&eHow:&r a block of quartz on top, basic capacitors and a casing in the middle, a starter rod below.",
        "&eTip:&r crystals cost hundreds of thousands of FE. More and better rods matter more than anything else here."]),
}


def grid_quest(key, name, count, mid, deps, opt):
    pre, tier = next((p, name[len(p) + 1:]) for p in PREFIX if name.startswith(p + "_") and name[len(p) + 1:] in TIERS)
    col = PREFIX[pre]
    _, label, what = COLS[col]
    title = f"{tier.title()} {label}" + (" (36)" if col == "reactor" else "")
    sub = f"{tier.title()} tier: {label.lower()}" + (", a full stack" if col == "reactor" else "")
    prev = TIERS[TIERS.index(tier) - 1] if tier != "starter" else None
    how = (f"{MAT[tier]}, plus the block's own parts (check JEI)." if not prev else
           f"usually the {prev} {label.lower()} with {MAT[tier]}; JEI has the exact recipe.")
    tip = TIP[tier]
    if col == "reactor":
        tip = "36 blocks of one tier make a full reactor. " + tip
    if col in ("ender_cell", "gate") and tier == "starter":
        tip = "its Ender Core is made in the Energizing Orb, so this one waits for the Orb."
    desc = [f"&eWhat:&r the {label} {what}", f"&eHow:&r {how}", f"&eTip:&r {tip}"]
    if key in CUSTOM:
        title, sub, desc = CUSTOM[key]
    tasks = [item(P + name, count)]
    if key == "pw_transmitter":
        tasks.append(anyof([P + "binding_card", P + "binding_card_dim"]))
    return Q(key, 0, 0, tasks, title, section=SECTION[tier], deps=deps + EXTRA_DEPS.get(key, []), xp=XP[tier],
             subtitle=sub, desc=desc, mirror=mid, **(OPT if opt else {}))


CHAPTER = Chapter("powah", "Powah!", P + "energizing_orb",
        ["Powah: dielectric parts, the Energizing Orb, crystal tiers, generators, cells and wireless power. "
         "The starter and basic tiers are open early; the Orb needs an MI electronic circuit (MV)."], SIDE, mirror="powah", quests=[
    # ===== Getting Started (ATM10 top) =======================================================
    Q("pw_intro", 0, 0, [tick()], "Powah!", section=S_START, deps=["t1_power"], xp=30, size=2.0, shape="gear", icon=P + "uraninite",
      mirror="6B2027DA7AA6FF34", subtitle="A whole power mod, tier by tier", desc=[
        "&6Insulators and conductors. You remember that power is mostly about where it is not allowed to go.&r",
        "&eWhat:&r Powah builds every block in seven tiers: starter, basic, hardened, blazing, niotic, spirited and nitro. Each row of this page is one tier; each column is one kind of block.",
        "&eHow:&r the starter and basic rows need only dielectric parts and capacitors. Everything from hardened up goes through the Energizing Orb, which needs an MI electronic circuit (MV) in this pack.",
        "&eTip:&r click the checkmark to start. You don't need every block: pick the columns you'll use."]),
    Q("pw_paste", 0, 0, [item(P + "dielectric_paste", 16), item(P + "dielectric_casing")], "Dielectric Parts", section=S_START,
      deps=["pw_intro"], xp=40, mirror="7E92ED270C67FDE5", subtitle="Paste and a casing: the base of every block", desc=[
        "&eWhat:&r dielectric paste goes into rods, casings, capacitors and cables; the casing is the frame inside almost every Powah block.",
        "&eChemistry:&r a dielectric is an insulator that polarises in an electric field. Fired clay (aluminosilicates such as kaolinite, Al₂Si₂O₅(OH)₄) is the porcelain on real power-line insulators.",
        "&eHow:&r paste, shapeless: 3 coal or charcoal + 2 clay balls + a lava bucket makes 24. Casing: 4 iron ingots in the corners, horizontal rods top and bottom, upright rods in the middle row (check JEI).",
        "&eTip:&r the lava recipe gives more per craft and keeps the bucket. Make a stack."]),
    Q("pw_orb", 0, 0, [item(P + "energizing_orb"), anyof([P + "energy_cable_starter", P + "energy_cable_basic"]),
                       anyof([P + "energizing_rod_starter", P + "energizing_rod_basic"])], "The Energizing Orb", section=S_START,
      deps=["pw_paste", "t4_circuit"], xp=150, size=1.5, mirror="3DDF87A1E5F5D009", subtitle="Pack gate: needs an MV electronic circuit", desc=[
        "&6A glass sphere that fills with light. You remember charging things just by holding them.&r",
        "&eWhat:&r the Orb turns FE into new materials: energized steel, crystals, ender cores. Every Powah tier above basic needs it.",
        "&eHow:&r in this pack: glass on top and sides, an MI &eelectronic circuit&r on each side of a dielectric casing in the middle, and 3 horizontal rods on the bottom. Bring a rod and a cable too.",
        "&eHow:&r place the orb, aim Energizing Rods at it from nearby, feed the rods FE through cables and put the ingredients in the orb. JEI's Energizing tab shows each recipe and its FE cost.",
        "&eTip:&r the first jobs are energized steel and the Ender Core."]),

    # ===== Tier quests (ATM10's left column) ==================================================
    Q("pw_cap_tiny", 0, 0, [item(P + "capacitor_basic_tiny")], "Tiny Capacitor", section=SECTION["starter"], deps=["pw_paste"], xp=30,
      mirror="6D88C19F47D0D469", subtitle="The heart of every starter block", desc=[
        "&eWhat:&r tiny capacitors set a block's tier to starter.",
        "&eChemistry:&r a capacitor is two conductors separated by a dielectric. It stores E = ½CV², and a better dielectric raises the capacitance C.",
        "&eHow:&r one basic capacitor splits into 2 tiny ones (check JEI)."]),
    Q("pw_capacitor", 0, 0, [item(P + "capacitor_basic")], "Basic Capacitor", section=SECTION["basic"], deps=["pw_paste"], xp=40,
      mirror="66ECC26BC81D0093", subtitle="Two plates and an insulator", desc=[
        "&eWhat:&r basic capacitors set a block's tier to basic, and split into tiny ones.",
        "&eHow:&r iron ingots, paste and a redstone block make 4 basic capacitors.",
        "&eTip:&r two basic capacitors combine into a large one, which the hardened and crystal tiers need later."]),
    Q("pw_energized", 0, 0, [item(P + "steel_energized")], "Energized Steel", section=SECTION["hardened"], deps=["pw_orb"], xp=100,
      mirror="5E090C9BB4DAA5D4", subtitle="Iron and gold, charged together", desc=[
        "&eWhat:&r Powah's basic alloy, made by the Energizing Orb. It opens the hardened tier.",
        "&eHow:&r put 1 iron + 1 gold in the Orb for 2 Energized Steel (check JEI for the FE cost).",
        "&eTip:&r hardened capacitors are a large capacitor in energized steel and paste."]),
    Q("pw_blazing", 0, 0, [item(P + "crystal_blazing")], "Blazing Crystal", section=SECTION["blazing"], deps=["pw_orb", "t2_blaze"], xp=100,
      mirror="562BD37539EE318E", subtitle="Energized blaze", desc=[
        "&eWhat:&r every Powah tier past hardened is built from a crystal made in the Orb. Blazing crystals open the blazing tier.",
        "&eHow:&r energize a blaze rod (or four blaze powder) with 120,000 FE (check JEI).",
        "&eTip:&r a blaze farm (or a Hostile Neural Networks blaze model) keeps the crystals coming."]),
    Q("pw_niotic", 0, 0, [item(P + "crystal_niotic")], "Niotic Crystal", section=SECTION["niotic"], deps=["pw_orb"], xp=125,
      mirror="7D7983F39E6E818D", subtitle="Energized diamond", desc=[
        "&eWhat:&r the niotic tier. Reactors and generators get much stronger.",
        "&eChemistry:&r diamond is pure carbon in a rigid lattice where every atom bonds to four others. It insulates electricity but carries heat better than any metal.",
        "&eHow:&r energize a diamond with 300,000 FE (check JEI)."]),
    Q("pw_spirited", 0, 0, [item(P + "crystal_spirited")], "Spirited Crystal", section=SECTION["spirited"], deps=["pw_orb"], xp=150,
      mirror="25EFC21A3C48E0B6", subtitle="Energized emerald", desc=[
        "&eWhat:&r the spirited tier, one step below the top.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈. A trace of chromium (Cr³⁺) replacing some aluminium gives it its green colour.",
        "&eHow:&r energize an emerald with 1,000,000 FE (check JEI). A villager trading hall pays off here."]),
    Q("pw_nitro", 0, 0, [item(P + "crystal_nitro")], "Nitro Crystal", section=SECTION["nitro"], deps=["pw_orb"], xp=250,
      mirror="4F1FFC02F4EAA2E6", subtitle="Powah's top tier", desc=[
        "&6Twenty million FE poured into a star. You remember power like this; it used to be yours.&r",
        "&eWhat:&r nitro crystals build the strongest Powah blocks.",
        "&eHow:&r energize a Nether Star, two redstone blocks and a blazing crystal block with 20,000,000 FE. One craft makes sixteen.",
        "&eTip:&r save your Nether Stars for this; the Wither is the only reliable source."]),

    # ===== The grid: one quest per block per tier ==============================================
    *[grid_quest(*row) for row in GRID],

    # ===== Side Projects (ours) ================================================================
    Q("pw_book", 0, 0, [item(P + "book")], "Powah's Manual", section=S_SIDE, subtitle="Optional: the mod's own guidebook", deps=["pw_paste"],
      xp=15, **OPT, desc=[
        "&eWhat:&r Powah's in-game book, with a page and a picture for every block on this chapter.",
        "&eHow:&r a book and a dielectric paste, shapeless.",
        "&eTip:&r add it to your Akashic Tome (Quality of Life page) so it doesn't take a slot."]),
    Q("pw_rods", 0, 0, [item(P + "dielectric_rod", 8), item(P + "dielectric_rod_horizontal", 8)], "Dielectric Rods", section=S_SIDE,
      subtitle="Optional: paste set around iron bars", deps=["pw_paste"], xp=30, **OPT, desc=[
        "&eWhat:&r insulated rods, upright and horizontal. Both go into casings, the Orb, cables and cards.",
        "&eHow:&r 6 paste around 3 iron bars: a vertical line of bars for the upright rod, a horizontal line for the horizontal one. 8 per craft.",
        "&eTip:&r you'll need far more horizontal rods than upright ones; every cable craft eats six."]),
    Q("pw_casing", 0, 0, [item(P + "dielectric_casing", 2)], "Spare Casings", section=S_SIDE, subtitle="Optional: you will need dozens",
      deps=["pw_rods"], xp=20, **OPT, desc=[
        "&eWhat:&r the frame inside almost every Powah machine, cell and generator.",
        "&eHow:&r 4 iron ingots in the corners, horizontal rods top and bottom, upright rods in the middle row (check JEI).",
        "&eTip:&r craft a stack of casings before a big upgrade session."]),
    Q("pw_wrench", 0, 0, [item(P + "wrench")], "Powah Wrench", section=S_SIDE, subtitle="Optional: rotate, configure, link", deps=["pw_paste"],
      xp=30, **OPT, desc=[
        "&eWhat:&r Powah's wrench. It has Rotate, Config and Link modes; the mode shows on the item.",
        "&eHow:&r iron ingots and dielectric paste (check JEI).",
        "&eTip:&r Config mode sets which sides of a cell or generator push or take power."]),
    Q("pw_pearl", 0, 0, [item(P + "player_aerial_pearl")], "Player Aerial Pearl", section=S_SIDE, subtitle="Optional: a pearl that remembers someone",
      deps=["pw_paste"], xp=40, **OPT, desc=[
        "&eWhat:&r the core of the Player Transmitter.",
        "&eHow:&r craft an Aerial Pearl (an ender pearl in iron bars and paste), then use it on a Zombie or a Husk.",
        "&eTip:&r trap a zombie near your base so you can make more later."]),
    Q("pw_photo", 0, 0, [item(P + "photoelectric_pane", 3), item(P + "thermoelectric_plate", 3)], "Panes and Plates", section=S_SIDE,
      subtitle="Optional: the parts of solar and thermo generators", deps=["pw_cap_tiny"], xp=50, **OPT, desc=[
        "&eWhat:&r photoelectric panes go into solar panels; thermo plates go into thermo generators.",
        "&eChemistry:&r lapis gets its blue from trisulfur radical ions (S₃⁻) trapped in the mineral lazurite.",
        "&eHow:&r pane: a glass pane in lapis and paste. Plate: a tiny capacitor in redstone and blaze powder.",
        "&eTip:&r blaze powder means a trip to the Nether first."]),
    Q("pw_dim_card", 0, 0, [item(P + "binding_card_dim")], "Dimensional Binding Card", section=S_SIDE, subtitle="Optional: a card touched by the End",
      deps=["pw_transmitter"], xp=60, **OPT, desc=[
        "&eWhat:&r the dimensional version of the Binding Card, for transmitters and other Powah blocks that take a card.",
        "&eHow:&r use a Binding Card on an Enderman or an Endermite.",
        "&eTip:&r read its tooltip to see what it does differently from the plain card."]),
    Q("pw_snowball", 0, 0, [item(P + "charged_snowball", 4)], "Charged Snowball", section=S_SIDE, subtitle="Optional: a pocket thunderstorm",
      deps=["pw_orb"], xp=50, **OPT, desc=[
        "&eWhat:&r a snowball charged with 500,000 FE. Throw it and lightning strikes where it lands.",
        "&eChemistry:&r a lightning channel heats air to around 30,000 K, hotter than the Sun's surface. It splits N₂ and O₂, and the nitrogen oxides it makes fertilise the soil.",
        "&eHow:&r one snowball in the Energizing Orb.",
        "&eTip:&r lightning turns a pig into a zombified piglin and a villager into a witch. Aim carefully."]),
    Q("pw_cap_hardened", 0, 0, [item(P + "capacitor_basic_large", 2), item(P + "capacitor_hardened", 2)], "Large and Hardened Capacitors",
      section=S_SIDE, subtitle="Optional: the first capacitor that needs the Orb", deps=["pw_energized"], xp=75, **OPT, desc=[
        "&eWhat:&r hardened capacitors unlock the hardened tier of everything.",
        "&eHow:&r 2 basic capacitors make a large one. A large capacitor in energized steel and paste makes 2 hardened capacitors.",
        "&eTip:&r large capacitors go into every crystal capacitor too. Craft spares."]),
    Q("pw_ender_core", 0, 0, [item(P + "ender_core", 2)], "Ender Core", section=S_SIDE, subtitle="Optional: an eye of ender, energized",
      deps=["pw_orb"], xp=75, **OPT, desc=[
        "&eWhat:&r the heart of Ender Cells and Ender Gates.",
        "&eHow:&r Energizing Orb: an eye of ender, a dielectric casing and a tiny capacitor, 50,000 FE.",
        "&eTip:&r one core per ender block, at every tier."]),
    Q("pw_coolant", 0, 0, [item(P + "dry_ice", 4)], "Dry Ice", section=S_SIDE, subtitle="Optional: a solid coolant for the reactor",
      deps=["pw_powah"], xp=75, **OPT, desc=[
        "&eWhat:&r a strong solid coolant for the Powah reactor. Cooler reactors waste less fuel.",
        "&eChemistry:&r real dry ice is solid CO₂, which sublimes straight to gas at -78.5 °C. Powah's is made from energized blue ice, which is H₂O, so take the name loosely.",
        "&eHow:&r Energizing Orb: 2 blue ice, 10,000 FE. JEI's Coolants and Solid Coolants tabs list every option and its strength.",
        "&eTip:&r the reactor also takes carbon and redstone to boost it. Check its GUI slots."]),
    Q("pw_nitro_block", 0, 0, [item(P + "nitro_crystal_block")], "A Block of Nitro", section=S_SIDE, subtitle="Secret: twenty million FE, nine times over",
      deps=["pw_nitro"], xp=100, secret=True, loot="secret", desc=[
        "&6Nine crystals, each a star's worth of charge, pressed into one block. You remember holding that much. You used to call it Tuesday.&r",
        "&eWhat:&r a storage block of nitro crystals. It does nothing; it's just very, very expensive.",
        "&eTip:&r you can always break it back into crystals."]),
], links=[("t1_power", 0, 0), ("t4_circuit", 0, 0), ("t4_uraninite", 0, 0), ("pw_more_powah", 0, 0)])
