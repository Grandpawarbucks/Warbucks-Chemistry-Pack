"""Quest chapter: shop_materials (shop group). See tools/quests/STYLE.md and docs/research/shop_brief.md.

The Materials stall of the Demigod's Market: repeatable buy-quests for ingots, dusts, plates, gears, rods, wires,
circuit components, chemicals and fuels. Rule: you can only buy what you've already made yourself. Every entry
depends on the quest where the player first makes that item and stays invisible (locked_hidden) until then.
Pay by handing in tokens (consume=True); the quest resets after claiming (repeat=True).

Layout is manual: one block of rows per tier (Steam -> LV -> MV -> HV -> EV), each starting with a counter quest.
Prices follow the brief's table: Steam 1-3 tokens, LV 2-6 tokens, MV 1-2 Greater, HV 2-3 Greater, EV 3-4 Greater.
"""
from questlib import Q, Chapter, item, tick, SIDE  # noqa: F401

T = "kubejs:demigod_token"
G = "kubejs:greater_demigod_token"

PER_LINE = 10     # entries per line before wrapping
STEP_X = 1.5
STEP_Y = 1.5
_rows = []


def _price(n, greater):
    if greater:
        return f"{n} Greater" if n > 1 else "1 Greater"
    return f"{n} tokens" if n > 1 else "1 token"


def counter(key, y, title, dep, sub, desc):
    """Row header: a short optional checkmark that opens this tier's stall."""
    _rows.append([y, 0])
    return Q(key, 0, y, [tick()], title, deps=[dep], tokens=0, xp=0, optional=True, size=1.5,
             subtitle=sub, desc=desc)


def buy(name, title, item_id, count, price, dep, dep_title, what, greater=False):
    """One shop entry: pay `price` (Greater) tokens, get `count` of `item_id`. Placed on the current row."""
    row = _rows[-1]
    i = row[1]
    row[1] += 1
    x = STEP_X * (1 + i % PER_LINE)
    y = row[0] + STEP_Y * (i // PER_LINE)
    cost = item(G if greater else T, price)
    return Q(f"sm_buy_{name}", x, y, [cost], title, deps=[dep], items=[(item_id, count)],
             tokens=0, xp=0, optional=True, repeat=True, consume=True, locked_hidden=True,
             subtitle=f"{_price(price, greater)} · unlocked by {dep_title}",
             desc=[f"&eWhat:&r {what}"])


def g(*a, **k):
    """Shorthand for an entry paid in Greater Demigod Tokens."""
    return buy(*a, greater=True, **k)


QUESTS = [
    Q("sm_intro", 0, -3, [tick()], "The Materials Stall", deps=["wel_tokens"], tokens=0, xp=10, optional=True,
      size=1.5, subtitle="Buy more of what you've already made", desc=[
          "&6You remember the offerings piling up at your temple. Now you can order them.&r",
          "&eWhat:&r this stall sells ingots, dusts, plates, gears, wires, circuit parts, chemicals and fuels.",
          "&eHow:&r an item appears here only after the quest where you first made it. Hand in the tokens and claim the bundle; the entry resets so you can buy again.",
          "&eTip:&r tokens save repetition, never a lesson. Nothing here skips a tier or a chemistry step.",
          "&eTip:&r MV and up cost Greater Demigod Tokens (1 Greater = 9 tokens; craft them in a grid)."]),

    # --- Steam (T0-T2) ------------------------------------------------------------------------------
    counter("sm_row_steam", 0, "Steam Stall", "t0_boiler", "Bronze, steel and the first chemicals", [
        "&eWhat:&r the Steam-age stall: bronze parts, steel, coke and your first Dissolver products.",
        "&eHow:&r entries show up one by one as you finish the quests that make them."]),
    buy("charcoal", "Charcoal", "minecraft:charcoal", 32, 1, "t0_charcoal", "Pyrolysis",
        "32 charcoal. Wood heated without air leaves nearly pure carbon."),
    buy("copper_ingot", "Copper Ingots", "minecraft:copper_ingot", 32, 2, "t0_copper", "Copper",
        "32 copper ingots for pipes, wires and bronze."),
    buy("tin_ingot", "Tin Ingots", "modern_industrialization:tin_ingot", 16, 2, "t0_tin", "Tin",
        "16 tin ingots, the other half of bronze."),
    buy("tin_dust", "Tin Dust", "modern_industrialization:tin_dust", 16, 2, "t0_dust", "Metal Dust",
        "16 tin dust, ready for mixing."),
    buy("bronze_ingot", "Bronze Ingots", "modern_industrialization:bronze_ingot", 16, 2, "t0_bronze", "The First Alloy",
        "16 bronze ingots (copper and tin, about 3:1)."),
    buy("bronze_plate", "Bronze Plates", "modern_industrialization:bronze_plate", 16, 2, "t0_plates", "Bronze Plates",
        "16 bronze plates for steam machines and boilers."),
    buy("bronze_curved", "Bronze Curved Plates", "modern_industrialization:bronze_curved_plate", 16, 2, "t0_curved", "Curved Plates",
        "16 curved bronze plates for tanks and pipes."),
    buy("bronze_rod", "Bronze Rods", "modern_industrialization:bronze_rod", 32, 2, "t0_parts", "Rods, Bolts and Rings",
        "32 bronze rods."),
    buy("bronze_gear", "Bronze Gears", "modern_industrialization:bronze_gear", 16, 3, "t0_gear", "Bronze Gears",
        "16 bronze gears for steam machines."),
    buy("fire_brick", "Fire Clay Bricks", "modern_industrialization:fire_clay_brick", 32, 2, "t0_fire_brick", "Fire Clay Bricks",
        "32 fire clay bricks: refractory ceramic that survives a furnace's heat."),
    buy("coke", "Coke", "modern_industrialization:coke", 32, 3, "t1_coke", "Coke",
        "32 coke: coal baked free of its volatiles, a hotter and cleaner fuel."),
    buy("creosote", "Creosote", "modern_industrialization:creosote_bucket", 4, 1, "t1_creosote", "Byproduct: Creosote",
        "4 buckets of creosote, the tar the coke oven drives out. A boiler fuel."),
    buy("lubricant", "Lubricant", "modern_industrialization:lubricant_bucket", 4, 2, "t1_lubricant", "Lubricant",
        "4 buckets of lubricant for cutting machines."),
    buy("steel_ingot", "Steel Ingots", "modern_industrialization:steel_ingot", 16, 3, "t1_steel", "Steel",
        "16 steel ingots: iron with a little carbon, far stronger than either."),
    buy("steel_plate", "Steel Plates", "modern_industrialization:steel_plate", 16, 3, "t1_steel_plate", "Steel Plates",
        "16 steel plates."),
    buy("steel_gear", "Steel Gears", "modern_industrialization:steel_gear", 8, 3, "t1_steel_gear", "Steel Gears",
        "8 steel gears."),
    buy("graphite", "Graphite", "chemlib:graphite", 16, 2, "t1_graphite", "Graphite",
        "16 graphite: carbon in flat sheets of hexagons."),
    buy("carbon", "Carbon", "chemlib:carbon", 32, 1, "t1_elements", "First Entries in the Periodic Table",
        "32 carbon (C), element 6."),
    buy("oxygen", "Oxygen", "chemlib:oxygen", 16, 1, "t1_elements", "First Entries in the Periodic Table",
        "16 oxygen (O), element 8."),
    buy("nacl", "Sodium Chloride", "chemlib:sodium_chloride", 32, 1, "pt_salt", "Ionic Bonds: Salt",
        "32 sodium chloride (NaCl), table salt."),
    buy("caco3", "Calcium Carbonate", "chemlib:calcium_carbonate", 16, 1, "pt_limestone", "Limestone",
        "16 calcium carbonate (CaCO₃), limestone and chalk."),
    buy("kno3", "Potassium Nitrate", "chemlib:potassium_nitrate", 16, 2, "pt_saltpeter", "Saltpeter",
        "16 potassium nitrate (KNO₃), saltpeter."),
    buy("naoh_chemlib", "Sodium Hydroxide", "chemlib:sodium_hydroxide", 16, 2, "pt_lye", "Lye",
        "16 sodium hydroxide (NaOH), lye: a strong base."),

    # --- LV (T3) ------------------------------------------------------------------------------------
    counter("sm_row_lv", 6, "LV Stall", "t3_analog", "Wires, rubber and circuit parts", [
        "&eWhat:&r the LV stall: wires, rubber, battery alloy and analog circuit parts.",
        "&eHow:&r finished circuits aren't sold; you still assemble those. The parts are here."]),
    buy("synth_oil", "Synthetic Oil", "modern_industrialization:synthetic_oil_bucket", 4, 3, "t3_synth_oil", "Synthetic Oil",
        "4 buckets of synthetic oil, the feedstock for rubber."),
    buy("rubber", "Rubber Sheets", "modern_industrialization:rubber_sheet", 16, 2, "t3_rubber", "Rubber",
        "16 rubber sheets for cable insulation."),
    buy("copper_wire", "Copper Wire", "modern_industrialization:copper_wire", 16, 2, "t3_wire", "Wires and Cables",
        "16 copper wires."),
    buy("tin_cable", "Tin Cable", "modern_industrialization:tin_cable", 16, 3, "t3_wire", "Wires and Cables",
        "16 insulated tin cables for LV power."),
    buy("fine_wire", "Fine Copper Wire", "modern_industrialization:copper_fine_wire", 32, 3, "t3_fine_wire", "Fine Copper Wire",
        "32 fine copper wires for inductors and boards."),
    buy("battery_alloy", "Battery Alloy", "modern_industrialization:battery_alloy_ingot", 16, 4, "t3_alloy", "Battery Alloy",
        "16 battery alloy ingots (lead hardened with antimony)."),
    buy("analog_board", "Analog Circuit Boards", "modern_industrialization:analog_circuit_board", 8, 4, "t3_board", "Analog Circuit Board",
        "8 analog circuit boards, ready for components."),
    buy("capacitor", "Capacitors", "modern_industrialization:capacitor", 16, 4, "t3_capacitor", "Capacitor",
        "16 capacitors: they store charge between two plates."),
    buy("resistor", "Resistors", "modern_industrialization:resistor", 16, 3, "t3_components", "Resistor",
        "16 resistors."),
    buy("inductor", "Inductors", "modern_industrialization:inductor", 16, 4, "t3_inductor", "Inductor",
        "16 inductors: coils that resist changes in current."),
    buy("acid_chemlib", "Sulfuric Acid", "chemlib:sulfuric_acid", 16, 4, "t3_acid", "Battery Acid",
        "16 sulfuric acid (H₂SO₄)."),
    buy("redstone_battery", "Redstone Batteries", "modern_industrialization:redstone_battery", 4, 4, "t3_battery", "Redstone Battery",
        "4 redstone batteries."),
    buy("magrod", "Magnetic Steel Rods", "modern_industrialization:steel_rod_magnetic", 16, 4, "t3_magrod", "Magnetic Steel Rod",
        "16 magnetic steel rods for motors."),
    buy("motor", "Electric Motors", "modern_industrialization:motor", 4, 6, "t3_motor", "Electric Motor",
        "4 electric motors."),
    buy("piston", "MI Pistons", "modern_industrialization:piston", 4, 6, "t3_piston", "Piston",
        "4 MI pistons."),
    buy("cupronickel_wire", "Magnetic Cupronickel Wire", "modern_industrialization:cupronickel_wire_magnetic", 16, 5, "t3_cupronickel", "Magnetic Cupronickel Wire",
        "16 magnetic cupronickel wires for heating coils."),
    buy("infused", "Infused Alloy", "mekanism:alloy_infused", 16, 4, "t3_infused", "Infused Alloy",
        "16 infused alloy (copper infused with redstone)."),

    # --- MV (T4) ------------------------------------------------------------------------------------
    counter("sm_row_mv", 12, "MV Stall", "t4_mv", "Aluminum, silicon and the first acids", [
        "&eWhat:&r the MV stall, priced in Greater Demigod Tokens: aluminum, silicon, electronics parts and acids.",
        "&eTip:&r 9 tokens in a crafting grid make 1 Greater Token."]),
    g("sulfur", "Sulfur Dust", "modern_industrialization:sulfur_dust", 32, 1, "t4_sulfur", "A Source of Sulfur",
      "32 sulfur dust (S), the start of the contact process."),
    g("alumina", "Alumina", "chemlib:aluminum_oxide_dust", 16, 1, "t4_alumina", "Alumina",
      "16 alumina (Al₂O₃) from the Bayer process. Smelting it is still the Hall-Héroult cell's job."),
    g("aluminum", "Aluminum Ingots", "modern_industrialization:aluminum_ingot", 16, 2, "t4_aluminum", "Aluminum",
      "16 aluminum ingots: light, strong and the metal of MV."),
    g("electrum", "Electrum Ingots", "modern_industrialization:electrum_ingot", 16, 1, "t4_electrum", "Electrum",
      "16 electrum ingots (gold and silver)."),
    g("silicon", "Silicon Ingots", "modern_industrialization:silicon_ingot", 16, 1, "t4_silicon", "Silicon",
      "16 silicon ingots (Si), the semiconductor."),
    g("ec_board", "Electronic Circuit Boards", "modern_industrialization:electronic_circuit_board", 8, 1, "t4_ecboard", "Electronic Circuit Board",
      "8 electronic circuit boards."),
    g("transistor", "Transistors", "modern_industrialization:transistor", 16, 1, "t4_transistor", "Transistors and Diodes",
      "16 transistors: silicon switches."),
    g("diode", "Diodes", "modern_industrialization:diode", 16, 1, "t4_transistor", "Transistors and Diodes",
      "16 diodes: current flows one way only."),
    g("sodium", "Sodium Dust", "modern_industrialization:sodium_dust", 16, 1, "t4_sodium", "Sodium",
      "16 sodium dust (Na), electrolysed from salt."),
    g("acid_bucket", "Sulfuric Acid Buckets", "modern_industrialization:sulfuric_acid_bucket", 4, 1, "t4_acid", "Sulfuric Acid",
      "4 buckets of sulfuric acid (H₂SO₄)."),
    g("naoh_bucket", "Sodium Hydroxide Buckets", "modern_industrialization:sodium_hydroxide_bucket", 4, 1, "t4_lye_bayer", "Lye for the Digester",
      "4 buckets of sodium hydroxide solution (NaOH)."),
    g("hcl_bucket", "Hydrochloric Acid Buckets", "modern_industrialization:hydrochloric_acid_bucket", 4, 1, "t4_mi_hcl", "Hydrochloric Acid, MI Style",
      "4 buckets of hydrochloric acid (HCl)."),
    g("si_battery", "Silicon Batteries", "modern_industrialization:silicon_battery", 4, 2, "t4_sibattery", "Silicon Battery",
      "4 silicon batteries."),

    # --- HV (T5) ------------------------------------------------------------------------------------
    counter("sm_row_hv", 18, "HV Stall", "t5_hv", "Oil products, polymers and stainless steel", [
        "&eWhat:&r the HV stall: refinery products, polymers, stainless steel and digital circuit parts.",
        "&eHow:&r fuels and feedstocks come as buckets, plastics as pellets or buckets."]),
    g("crude_oil", "Crude Oil", "modern_industrialization:crude_oil_bucket", 8, 1, "t5_oil", "Black Gold",
      "8 buckets of crude oil for your distillation tower."),
    g("diesel", "Diesel", "modern_industrialization:diesel_bucket", 8, 2, "t5_diesel", "Diesel Power",
      "8 buckets of diesel for generators and drills."),
    g("light_fuel", "Light Fuel", "modern_industrialization:light_fuel_bucket", 8, 1, "t5_hydrotreat", "Sweetening the Oil",
      "8 buckets of sweetened light fuel."),
    g("heavy_fuel", "Heavy Fuel", "modern_industrialization:heavy_fuel_bucket", 8, 1, "t5_hydrotreat", "Sweetening the Oil",
      "8 buckets of sweetened heavy fuel."),
    g("ethylene", "Ethylene", "modern_industrialization:ethylene_bucket", 4, 1, "t5_ethylene", "Ethylene",
      "4 buckets of ethylene (C₂H₄), the simplest alkene."),
    g("polyethylene", "Polyethylene", "modern_industrialization:polyethylene_bucket", 4, 2, "t5_pe", "Polymerisation",
      "4 buckets of polyethylene: ethylene chained thousands long."),
    g("hdpe", "HDPE Pellets", "mekanism:hdpe_pellet", 16, 2, "t5_hdpe", "HDPE",
      "16 HDPE pellets for Mekanism plastics."),
    g("chromium", "Chromium Dust", "modern_industrialization:chromium_dust", 16, 2, "t5_chromium", "Chromium and Manganese",
      "16 chromium dust (Cr), what makes stainless steel stainless."),
    g("manganese", "Manganese Dust", "modern_industrialization:manganese_dust", 16, 2, "t5_chromium", "Chromium and Manganese",
      "16 manganese dust (Mn)."),
    g("stainless", "Stainless Steel Ingots", "modern_industrialization:stainless_steel_ingot", 16, 3, "t5_ebf", "Stainless Steel",
      "16 stainless steel ingots, already cooled in the vacuum freezer."),
    g("dc_board", "Digital Circuit Boards", "modern_industrialization:digital_circuit_board", 8, 2, "t5_dcb", "Digital Circuit Board",
      "8 digital circuit boards."),
    g("op_amp", "Op Amps", "modern_industrialization:op_amp", 8, 2, "t5_gates", "Logic Gates",
      "8 operational amplifiers."),
    g("na_battery", "Sodium Batteries", "modern_industrialization:sodium_battery", 4, 3, "t5_sodium", "Sodium Battery",
      "4 sodium batteries."),
    g("fluix", "Fluix Crystals", "ae2:fluix_crystal", 16, 2, "t5_fluix", "Fluix",
      "16 fluix crystals for your ME network."),

    # --- EV (T6) ------------------------------------------------------------------------------------
    counter("sm_row_ev", 24, "EV Stall", "t6_pu", "Refractory metals, chips and industrial chemicals", [
        "&eWhat:&r the EV stall: titanium, tungsten, platinum, chips and the big industrial chemicals.",
        "&eHow:&r nuclear fuel, antimatter and the Seed's parts are never sold. You make those."]),
    g("titanium", "Titanium Ingots", "modern_industrialization:titanium_ingot", 16, 4, "t6_titanium", "Titanium",
      "16 titanium ingots, already cooled."),
    g("tungsten", "Tungsten Ingots", "modern_industrialization:tungsten_ingot", 8, 4, "t6_tungsten", "Tungsten",
      "8 tungsten ingots (W), the metal with the highest melting point."),
    g("kanthal", "Kanthal Ingots", "modern_industrialization:kanthal_ingot", 16, 3, "t6_kanthal", "Kanthal",
      "16 kanthal ingots (iron, chromium and aluminium) for hot coils."),
    g("annealed", "Annealed Copper", "modern_industrialization:annealed_copper_ingot", 16, 3, "t6_annealed", "Annealed Copper",
      "16 annealed copper ingots for EV cables."),
    g("platinum", "Platinum Dust", "modern_industrialization:platinum_dust", 8, 4, "t6_pgm", "The Platinum Line",
      "8 platinum dust (Pt) from the aqua regia line."),
    g("neodymium", "Neodymium Dust", "modern_industrialization:neodymium_dust", 8, 4, "t6_monazite", "Rare Earths and Helium",
      "8 neodymium dust (Nd), the rare earth in strong magnets."),
    g("beryllium", "Beryllium Plates", "modern_industrialization:beryllium_plate", 8, 3, "t6_beryllium", "Beryllium",
      "8 beryllium plates."),
    g("solder", "Soldering Alloy", "modern_industrialization:soldering_alloy_dust", 16, 3, "t6_solder", "Soldering Alloy",
      "16 soldering alloy dust (tin and lead)."),
    g("blastproof", "Blastproof Alloy Plates", "modern_industrialization:blastproof_alloy_plate", 8, 4, "t6_blastproof", "Blastproof Alloy",
      "8 blastproof alloy plates."),
    g("nuclear_alloy", "Nuclear Alloy Plates", "modern_industrialization:nuclear_alloy_plate", 8, 4, "t6_nuclear_alloy", "Nuclear Alloy",
      "8 nuclear alloy plates for reactor casings."),
    g("wafer", "Silicon Wafers", "modern_industrialization:silicon_wafer", 8, 3, "t6_silicon", "Semiconductor Silicon",
      "8 silicon wafers cut from a single crystal."),
    g("ram", "RAM Chips", "modern_industrialization:random_access_memory", 8, 4, "t6_chips", "Chips",
      "8 RAM chips."),
    g("alu", "ALU Chips", "modern_industrialization:arithmetic_logic_unit", 8, 4, "t6_chips", "Chips",
      "8 arithmetic logic units."),
    g("mmu", "MMU Chips", "modern_industrialization:memory_management_unit", 8, 4, "t6_chips", "Chips",
      "8 memory management units."),
    g("pu_board", "Processing Unit Boards", "modern_industrialization:processing_unit_board", 8, 3, "t6_board", "Processing Unit Board",
      "8 processing unit boards."),
    g("cd_battery", "Cadmium Batteries", "modern_industrialization:cadmium_battery", 4, 4, "t6_cadmium", "Cadmium Battery",
      "4 cadmium batteries."),
    g("pvc", "PVC", "modern_industrialization:polyvinyl_chloride_bucket", 4, 3, "t6_pvc", "PVC",
      "4 buckets of polyvinyl chloride."),
    g("argon", "Argon", "modern_industrialization:argon_bucket", 8, 3, "t6_argon", "Argon from Air",
      "8 buckets of argon (Ar), the inert gas for crystal growing."),
    g("helium", "Helium", "modern_industrialization:helium_bucket", 4, 3, "t6_monazite", "Rare Earths and Helium",
      "4 buckets of helium (He), trapped in monazite by alpha decay."),
    g("ammonia", "Ammonia", "chemlib:ammonia_bucket", 4, 3, "t6_haber", "Haber-Bosch",
      "4 buckets of ammonia (NH₃) from N₂ + 3H₂."),
    g("nitric", "Nitric Acid", "chemlib:nitric_acid_bucket", 4, 3, "t6_ostwald", "Ostwald Process",
      "4 buckets of nitric acid (HNO₃)."),
]

CHAPTER = Chapter("shop_materials", "Market: Materials and Chemicals", "modern_industrialization:steel_ingot",
        ["Buy more of the metals, parts and chemicals you've already made."], SIDE, QUESTS,
        tokens=0, layout="manual")
