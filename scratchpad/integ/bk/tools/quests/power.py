"""Quest chapter: power. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Basic Power" chapter (user decision 2026-10-20: quest for quest where we have the mod; same items,
order, clusters and sizes; the text is ours). It also carries ATM10's "Generators" chapter (Iron Furnaces and
Generator Galore), quest for quest, in sections of its own. The engine takes one mirror target per chapter, so those
quests carry no mirror id; their ATM10 ids are in GEN_MIRROR below, ready if the page is ever split out.

ATM10 Basic Power quests skipped (mod not in the pack): Extreme Reactors, RFTools Power cells, Industrial Foregoing's
Mycelial Reactor, Dyson Cube, Draconic energy core, and the two Productive Bees / XyCraft flux-dust automations.
ATM10 Generators quests skipped: the credits checkmark and "Rainbow Furnace" (a renamed vanilla item, not a real item).
The Powah quests that used to live here (pw_energized, pw_powah_cell, pw_thermo, pw_powah, pw_blazing, pw_niotic,
pw_spirited, pw_nitro, pw_ender) moved to powah.py, keys unchanged. Our own quests ATM10 doesn't have (Mekanism power
plant, MI steam and diesel, extra renewables) stay as side quests; the ones other pages build on stay required.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
MEK, GEN, IF, GG, FLUX = "mekanism:", "mekanismgenerators:", "ironfurnaces:", "generatorgalore:", "fluxnetworks:"
S_HUB, S_EARLY, S_MOVE, S_FLUX, S_STORE = "Power Basics", "Early Power", "Moving Power", "Flux Networks", "Storing Power"
S_MID, S_END, S_MEKP, S_MI = "Mid-Game Power", "End-Game Power", "Mekanism Power Plant", "Steam and Diesel"
S_FURN, S_IF, S_RAINBOW, S_AUG, S_GG = "The Furnace", "Iron Furnaces", "The Rainbow Generator", "Furnace Augments", "Generator Galore"

# ATM10 "generators" quest ids for the Generators quests on this page (not used by the build: one mirror per page).
GEN_MIRROR = {
    "pw_furnace": "47750F3CB020104C", "pw_if_iron": "2748ACEAB96A5F60", "pw_if_gold": "420FE84DEE12CCE0",
    "pw_if_diamond": "21EA29A8C7F950CE", "pw_if_emerald": "711DDD55CEC439E5", "pw_if_obsidian": "32C7D8AE859BF89E",
    "pw_if_crystal": "2354BC5330350DF6", "pw_if_copper": "661C072E48F8D41F", "pw_if_silver": "61847F47CCA225D9",
    "pw_gg_copper": "618F1434757C8E69", "pw_gg_iron": "61F265D9A5713A4D", "pw_gold_gen": "25A3E30F722B38B6",
    "pw_gg_culinary": "1C73E60FC70408D4", "pw_gg_collection": "28FEB4C11AD1AE7C", "pw_gg_netherite": "07BEB974DF1E5AD3",
    "pw_gg_gems": "076A648E3E3245C9", "pw_gg_obsidian": "311F43D48B9C26FF", "pw_gg_sweet": "68972BA647FDCF8F",
    "pw_gg_potion": "7297391D026EE9A6", "pw_gg_enchant": "6A1145678E80FB8E", "pw_gg_magmatic": "552CA2ABE659A507",
    "pw_gg_ender": "69201157ECFBB426", "pw_gg_star": "1843C79133DFB024", "pw_gg_halitosis": "40DB6E3DE87F16EF",
    "pw_if_netherite": "79C4CF8D7312FC28", "pw_if_augments": "78D1C97A542133D8", "pw_if_aug_blasting": "73FF01D830A669AA",
    "pw_if_aug_smoking": "33436ED0D9F128BD", "pw_if_aug_factory": "49F08DE190AAD0D8", "pw_if_aug_generator": "07753C5D94312A50",
    "pw_if_aug_speed": "7F67849DE9F700D8", "pw_if_aug_fuel": "538821E23E39BE97", "pw_if_spooky": "686B25F2E9D8CC97",
    "pw_if_xmas": "553220A2CD7CAFE4", "pw_if_heater": "20EC8001A05CE2C8", "pw_if_core": "7A615E2A152917AD",
    "pw_if_plating": "0AD2B11565B484E7", "pw_if_rainbow_coal": "062AA943A1629A86", "pw_if_copy": "757B14D08A9A03C4",
    "pw_if_rainbow": "0ADBE90B33ACC9FB", "pw_gg_8x": "7CE86300AF8E9BCA", "pw_gg_64x": "72A287DCAEEFE49F",
    "pw_if_atm": "3A4C17878FC8315B", "pw_if_vibranium": "2E85D6E2CFCC356E", "pw_if_unobtainium": "25080E3295B1DF01",
}
GG_8X = [GG + g + "_generator_8x" for g in ("copper", "diamond", "emerald", "enchantment", "ender", "gold", "halitosis", "honey",
                                            "iron", "magmatic", "netherite", "netherstar", "obsidian", "potion", "culinary")]
GG_64X = [GG + g + "_generator_64x" for g in ("culinary", "enchantment", "ender", "halitosis", "honey", "magmatic", "netherite",
                                              "netherstar", "potion")]
FURNACES = ["copper", "iron", "silver", "gold", "diamond", "emerald", "crystal", "obsidian", "netherite"]


def if_furnace(key, metal, deps, xp, what, how, tip, extra=None, **kw):
    """One Iron Furnaces tier: its own quest, in the Iron Furnaces section."""
    return Q(key, 0, 0, [item(f"{IF}{metal}_furnace")], f"{metal.title()} Furnace", section=S_IF, deps=deps, xp=xp,
             subtitle=kw.pop("subtitle", f"The {metal} tier of furnace"),
             desc=[f"&eWhat:&r {what}", *([f"&eChemistry:&r {extra}"] if extra else []), f"&eHow:&r {how}", f"&eTip:&r {tip}"], **kw)


def gg(key, name, deps, xp, sub, what, how, tip, chem=None, **kw):
    """One Generator Galore generator."""
    return Q(key, 0, 0, [item(f"{GG}{name}_generator")], f"{name.title()} Generator", section=S_GG, deps=deps, xp=xp, subtitle=sub,
             desc=[f"&eWhat:&r {what}", *([f"&eChemistry:&r {chem}"] if chem else []), f"&eHow:&r {how}", f"&eTip:&r {tip}"], **kw)


def augment(key, kind, title, sub, what, tip):
    return Q(key, 0, 0, [item(f"{IF}augment_{kind}")], title, section=S_AUG, deps=["pw_if_augments"], xp=30, subtitle=sub, desc=[
        f"&eWhat:&r {what}",
        "&eHow:&r check JEI for its recipe, then put it in one of the furnace's augment slots.",
        f"&eTip:&r {tip}"])


CHAPTER = Chapter("power", "Power", GEN + "gas_burning_generator",
        ["Energy is chemistry too: combustion, gas burning, fission and fusion."], SIDE, mirror="basic_power", quests=[
    # ===== Power Basics (ATM10 centre) ======================================================
    Q("pw_iron_gen", 0, 0, [item("minecraft:redstone")], "Choosing Your Power", section=S_HUB, deps=["t1_power"], xp=40,
      size=2.0, shape="gear", mirror="4AB0DD227471FDBF", subtitle="A catalogue of every way to make, move and store FE", desc=[
        "&6You remember holding lightning. For now, the generator you built in T1 will do.&r",
        "&eWhat:&r this page lists the pack's power options by stage: early burners, moving power, storing it, mid-game and end-game plants, plus furnaces and Generator Galore.",
        "&eChemistry:&r every generator turns some stored energy into current: chemical bonds (C + O₂ → CO₂), sunlight, wind, heat, or the nucleus itself.",
        "&eHow:&r a little redstone opens the page. Most lines are optional; pick the ones that suit your base.",
        "&eTip:&r MI machines run on EU, Modern Industrialization's own electricity. Most other mods run on FE (Forge Energy)."]),

    # ===== Early Power ======================================================================
    Q("pw_early", 0, 0, [item("minecraft:coal")], "Early Power", section=S_EARLY, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="42D173B9FF8D16E4", subtitle="Burn something", desc=[
        "&eWhat:&r early power comes from burning fuel or catching heat and light.",
        "&eChemistry:&r coal is mostly carbon; burning it releases about 33 kJ per gram as it becomes CO₂.",
        "&eHow:&r a lump of coal starts this section. Charcoal works in every burner too."]),
    Q("pw_heat", 0, 0, [item(GEN + "heat_generator")], "Heat Generator", section=S_EARLY, deps=["pw_early", "t3_infuser"], xp=60,
      mirror="11D09E918015355C", subtitle="Mekanism's starter generator", desc=[
        "&eWhat:&r Mekanism's first generator. It burns fuel and turns heat into FE.",
        "&eHow:&r place lava next to it for a passive bonus, and feed it fuel for more.",
        "&eTip:&r lava from a pump makes this a decent passive generator early on."]),
    Q("pw_coal_gens", 0, 0, [anyof(["justdirethings:generatort1", "integrateddynamics:coal_generator", GG + "iron_generator"])],
      "Coal Generators", section=S_EARLY, deps=["pw_early"], xp=40, mirror="0BB367839D28607D", subtitle="Any simple burner counts", desc=[
        "&eWhat:&r a plain fuel-burning generator from any mod: Just Dire Things, Integrated Dynamics or Generator Galore.",
        "&eHow:&r check JEI for each. Feed it coal, charcoal or coke.",
        "&eTip:&r coke from your coke oven burns twice as long as coal in most burners."]),
    Q("pw_solar", 0, 0, [anyof([GEN + "solar_generator", GEN + "advanced_solar_generator", GEN + "wind_generator"])], "Renewables",
      section=S_EARLY, deps=["pw_early", "t4_mv"], xp=100, mirror="48DC9E8E9D21A2FA", subtitle="Light and wind, no fuel", desc=[
        "&eWhat:&r Mekanism's solar panels and wind generator: free power once built. Any one counts.",
        "&eChemistry:&r silicon solar cells use a p-n junction: a photon knocks an electron loose and the junction pushes it into a current.",
        "&eHow:&r solar under open sky; wind as high as you can build it (check JEI).",
        "&eTip:&r pair them with an energy cube to cover the night or a calm spell."]),
    Q("pw_adv_solar", 0, 0, [item(GEN + "advanced_solar_generator")], "Advanced Solar", section=S_EARLY, subtitle="Optional: a bigger array",
      deps=["pw_solar"], xp=150, **OPT, desc=[
        "&eWhat:&r Mekanism's Advanced Solar Generator, a larger array with much more output.",
        "&eHow:&r check JEI for the recipe. Give it space: it's bigger than one block.",
        "&eTip:&r like the basic panel, it only works in daylight. Buffer it with a cube."]),
    Q("pw_wind", 0, 0, [item(GEN + "wind_generator")], "Wind Power", section=S_EARLY, subtitle="Optional: build it high", deps=["pw_solar"],
      xp=150, **OPT, desc=[
        "&eWhat:&r Mekanism's Wind Generator. It works day and night.",
        "&eHow:&r it makes more power the higher it's placed. Build it on a mountain or a tall tower.",
        "&eTip:&r it needs open space around it, so leave room."]),
    Q("pw_bio", 0, 0, [item(GEN + "bio_generator")], "Bio Fuel", section=S_EARLY, subtitle="Optional: crops into power", deps=["pw_heat"],
      xp=100, **OPT, desc=[
        "&eWhat:&r Mekanism's Bio-Generator burns Bio Fuel.",
        "&eChemistry:&r plants store sunlight as sugars and cellulose. Burning them releases it, and the CO₂ is the same CO₂ the plant took in.",
        "&eHow:&r crush seeds and crops into Bio Fuel in a Mekanism Crusher."]),

    # ===== Moving Power =====================================================================
    Q("pw_transfer", 0, 0, [item("minecraft:iron_ingot")], "Moving Power", section=S_MOVE, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="1F81EA5E45424308", subtitle="From generator to machine", desc=[
        "&eWhat:&r power is useless where it's made. This section is cables, pipes and the ways to skip them.",
        "&eChemistry:&r copper and aluminium carry real grids because their electrons move freely; iron conducts about six times worse than copper.",
        "&eHow:&r an iron ingot opens the section."]),
    Q("pw_pipez", 0, 0, [item("pipez:energy_pipe"), item("pipez:wrench")], "Energy Pipes", section=S_MOVE, deps=["pw_transfer"], xp=30,
      mirror="4EEAB467C722ECE7", subtitle="The cheapest FE line", desc=[
        "&eWhat:&r Pipez energy pipes carry FE, and the Pipe Wrench sets which ends pull.",
        "&eHow:&r iron and redstone with a redstone block for the pipe (check JEI). Sneak-click the generator end to extract.",
        "&eTip:&r the Automation and Logic page has the rest of Pipez."]),
    Q("pw_pipez_up", 0, 0, [anyof([f"pipez:{t}_upgrade" for t in ("basic", "improved", "advanced", "ultimate")])], "Pipe Upgrades",
      section=S_MOVE, deps=["pw_pipez"], xp=30, mirror="1409C17773B6A131", subtitle="More FE per tick through one pipe", desc=[
        "&eWhat:&r an upgrade in the extracting end raises how much a pipe moves. Any tier counts.",
        "&eHow:&r each tier is the one before plus better materials (check JEI).",
        "&eTip:&r one upgrade at the generator end is enough for the whole line."]),
    Q("pw_cables", 0, 0, [anyof([f"{MEK}{t}_universal_cable" for t in ("basic", "advanced", "elite", "ultimate")])], "Universal Cables",
      section=S_MOVE, deps=["pw_transfer", "t3_infuser"], xp=40, mirror="5C47935A3B2877FF", subtitle="Mekanism's tiered power cable", desc=[
        "&eWhat:&r Mekanism's power cable, from basic to ultimate. Any tier counts.",
        "&eHow:&r steel and redstone for the basic cable (check JEI); higher tiers upgrade in place with alloys.",
        "&eTip:&r cables hold a little energy themselves, so a long line is a small buffer too."]),
    Q("pw_entangle", 0, 0, [item(MEK + "quantum_entangloporter")], "Quantum Entangloporter", section=S_MOVE, deps=["pw_transfer", "t6_pu"],
      xp=150, mirror="7FE969CB4B419FC6", subtitle="Power to anywhere, no line at all", desc=[
        "&eWhat:&r two Entangloporters on one frequency act as one block: power goes in one and comes out the other, across any distance or dimension.",
        "&eHow:&r refined obsidian, atomic alloy, ultimate control circuits (EV) and a teleportation core (check JEI).",
        "&eTip:&r the Mekanism page covers the frequency setup; here, it's just a very long cable."]),

    # ===== Flux Networks ====================================================================
    Q("pw_flux_dust", 0, 0, [item(FLUX + "flux_dust", 4)], "Flux Networks", section=S_FLUX, deps=["pw_transfer", "t2_nether"], xp=60,
      size=1.5, mirror="35CC898E0E49FE58", subtitle="Redstone crushed between obsidian and bedrock", desc=[
        "&eWhat:&r flux dust is the base of every Flux Networks device.",
        "&eChemistry:&r real redstone doesn't exist, but pressure really does change minerals: graphite squeezed hard enough becomes diamond, and that's the idea here.",
        "&eHow:&r its tooltip says it: redstone compressed with bedrock and obsidian. JEI's Flux Networks page shows the setup. Bedrock is easy to reach at the Nether's floor or roof.",
        "&eTip:&r make a big batch now. The Flux Core needs an MI processing unit (EV), but the dust doesn't."]),
    Q("pw_flux_core", 0, 0, [item(FLUX + "flux_core", 4), item(FLUX + "flux_block")], "Flux Cores", section=S_FLUX,
      deps=["pw_flux_dust", "t6_pu"], xp=150, mirror="1BE26A00A420DAE3", subtitle="Pack gate: an MI processing unit in each", desc=[
        "&eWhat:&r Flux Cores are the heart of every flux device; nine flux dust make a Flux Block.",
        "&eHow:&r in this pack: flux dust and obsidian around an MI &eprocessing unit&r (EV). Check JEI.",
        "&eTip:&r a plug, a point and a storage block each eat cores. Make four at once."]),
    Q("pw_flux_plug", 0, 0, [item(FLUX + "flux_plug")], "Flux Plug", section=S_FLUX, deps=["pw_flux_core"], xp=60,
      mirror="5F078A574A783B02", subtitle="Where power enters the network", desc=[
        "&eWhat:&r a Flux Plug takes power from whatever it touches and puts it on a flux network.",
        "&eHow:&r flux blocks and a flux core (check JEI). Open it and create a network.",
        "&eTip:&r put one on your biggest battery's output."]),
    Q("pw_flux_net", 0, 0, [tick()], "Set Up a Network", section=S_FLUX, deps=["pw_flux_plug"], xp=40, icon=FLUX + "flux_configurator",
      mirror="36DEA17CBB696CC7", subtitle="Name it, colour it, lock it", desc=[
        "&eWhat:&r every flux device joins one named network. The network decides who may connect.",
        "&eHow:&r open the plug, make a network, give it a colour and set its security (public, encrypted or private). Click the checkmark when it's set.",
        "&eTip:&r private networks stop a teammate's machine draining your reactor by accident."]),
    Q("pw_flux_point", 0, 0, [item(FLUX + "flux_point")], "Flux Point", section=S_FLUX, deps=["pw_flux_net"], xp=60,
      mirror="56B6ABF3D6EA0D84", subtitle="Where power leaves the network", desc=[
        "&eWhat:&r a Flux Point gives network power to whatever it touches.",
        "&eHow:&r like the plug (check JEI). Join it to the same network.",
        "&eTip:&r set a priority so the most important machines fill first."]),
    Q("pw_flux_storage", 0, 0, [item(FLUX + "basic_flux_storage")], "Flux Storage", section=S_FLUX, deps=["pw_flux_net"], xp=80,
      mirror="79AD74A863EA43CB", subtitle="A battery the whole network shares", desc=[
        "&eWhat:&r Basic Flux Storage buffers energy for the network.",
        "&eHow:&r flux blocks and glass around a flux core (check JEI).",
        "&eTip:&r flux storage keeps its energy when broken, so you can carry charged batteries to a new base."]),
    Q("pw_flux_tip", 0, 0, [tick()], "Note: Priorities", section=S_FLUX, deps=["pw_flux_net"], xp=20, **OPT, icon=FLUX + "flux_point",
      mirror="2EB7784D5296F410", subtitle="Optional: who gets fed first", desc=[
        "&eWhat:&r each plug and point has a priority and a transfer limit. High-priority points fill first; storage fills last.",
        "&eHow:&r open a point, set its priority and limit. Click the checkmark when you've set one.",
        "&eTip:&r give the reactor coolant pumps the top priority. Everything else can wait a tick."]),
    Q("pw_flux_controller", 0, 0, [item(FLUX + "flux_controller")], "Flux Controller", section=S_FLUX, deps=["pw_flux_net"], xp=100,
      mirror="27A4FA38992448A0", subtitle="Charge yourself from the network", desc=[
        "&eWhat:&r the Flux Controller sends network energy wirelessly into players' inventories.",
        "&eHow:&r flux blocks, a flux core and flux dust (check JEI).",
        "&eTip:&r turn charging off for your armour slots if it fights with other chargers. The Flux Configurator copies settings between devices."]),
    Q("pw_flux_big", 0, 0, [item(FLUX + "herculean_flux_storage")], "Herculean Storage", section=S_FLUX, deps=["pw_flux_storage"], xp=100,
      **OPT, subtitle="Optional: a much bigger flux battery", desc=[
        "&eWhat:&r Herculean (and then Gargantuan) Flux Storage holds far more energy in one block, shared with the whole network.",
        "&eHow:&r Basic Flux Storage blocks around glass panes (check JEI). Gargantuan is the same with Herculean blocks.",
        "&eTip:&r one Herculean block can carry a small base through a night with no solar."]),

    # ===== Storing Power ====================================================================
    Q("pw_storing", 0, 0, [item("minecraft:iron_ingot")], "Storing Power", section=S_STORE, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="76EA017B12E8F01B", subtitle="A buffer between making and using", desc=[
        "&eWhat:&r a battery keeps machines running when the generator stalls, and catches power you'd otherwise waste.",
        "&eChemistry:&r a lead-acid battery stores energy in a reversible reaction: Pb + PbO₂ + 2H₂SO₄ ⇌ 2PbSO₄ + 2H₂O.",
        "&eHow:&r an iron ingot opens the section."]),
    Q("pw_cube", 0, 0, [anyof([f"{MEK}{t}_energy_cube" for t in ("basic", "advanced", "elite", "ultimate")])], "Energy Cubes",
      section=S_STORE, deps=["pw_storing", "t3_infuser"], xp=60, mirror="477B411F84342EEA", subtitle="Mekanism's block battery", desc=[
        "&eWhat:&r energy cubes hold FE so short spikes don't stall your machines. Any tier counts.",
        "&eHow:&r put one between your generators and machines. Configure its sides with the Configurator.",
        "&eTip:&r cubes upgrade in place: craft the next tier around the old one."]),
    Q("pw_id_battery", 0, 0, [item("integrateddynamics:energy_battery")], "Energy Battery", section=S_STORE, deps=["pw_storing"], xp=40,
      mirror="72EA25D05C46D39A", subtitle="Integrated Dynamics' battery", desc=[
        "&eWhat:&r a small FE battery made of crystalized Menril. It stacks power with others placed next to it.",
        "&eHow:&r Menril chunks and blocks around a redstone block (check JEI). The resin line is on the Automation and Logic page.",
        "&eTip:&r it fits on a logic network, where cables can carry its power."]),
    Q("pw_induction", 0, 0, [anyof([f"{MEK}{t}_induction_provider" for t in ("basic", "advanced", "elite", "ultimate")]),
                             anyof([f"{MEK}{t}_induction_cell" for t in ("basic", "advanced", "elite", "ultimate")])],
      "Induction Matrix", section=S_STORE, deps=["pw_cube", "pw_lithium"], xp=300, size=1.5, mirror="682034C680FDEDC2",
      subtitle="One multiblock battery for the whole base", desc=[
        "&6Power stored, waiting, obedient. This feels familiar.&r",
        "&eWhat:&r a hollow multiblock battery. Cells inside set how much it stores; providers set how fast it charges and discharges.",
        "&eHow:&r casings form the shell (Structural Glass works for the walls), ports move energy in and out. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r switch one port to output with the Configurator. Start small; you can rebuild it larger later."]),

    # ===== Mid-Game Power ===================================================================
    Q("pw_mid", 0, 0, [item("minecraft:diamond")], "Mid-Game Power", section=S_MID, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="5E41363F9AE243F3", subtitle="Gases and uranium", desc=[
        "&eWhat:&r the mid game is about chemistry you've built yourself: burning hydrogen, and fission fuel.",
        "&eChemistry:&r diamond is carbon too, but burning one for power would be a terrible trade.",
        "&eHow:&r a diamond opens the section."]),
    Q("pw_gas", 0, 0, [item(GEN + "gas_burning_generator")], "Burning Hydrogen", section=S_MID, deps=["pw_mid", "t4_separator"], xp=150,
      mirror="0AEC181F5E21A299", subtitle="The cleanest combustion there is", desc=[
        "&eWhat:&r the Gas-Burning Generator turns flammable gas into FE.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O + energy. The only exhaust is water.",
        "&eHow:&r pipe hydrogen from your Electrolytic Separator in with pressurized tubes.",
        "&eTip:&r electrolysis costs more energy than burning hydrogen returns. Use it to store spare power, not to make it."]),
    Q("pw_more_powah", 0, 0, [item("powah:uraninite")], "More Powah", section=S_MID, deps=["pw_mid", "t4_uraninite"], xp=80,
      mirror="35ABB0DEE70DF7FD", subtitle="Uranium dioxide for Powah's reactors", desc=[
        "&eWhat:&r uraninite fuels Powah's reactors. The Powah! page has the whole mod, tier by tier.",
        "&eChemistry:&r uraninite is UO₂. In this pack you make it the real way: uranium dust oxidised in MI's Chemical Reactor.",
        "&eHow:&r uranium dust and oxygen in the Chemical Reactor (MV). Powah's own shortcut is removed.",
        "&eTip:&r a Powah reactor takes uraninite, coolant, and carbon or redstone to boost it."]),

    # ===== End-Game Power ===================================================================
    Q("pw_end", 0, 0, [item("minecraft:netherite_ingot")], "End-Game Power", section=S_END, deps=["pw_iron_gen", "t2_nether"], xp=40,
      size=1.5, mirror="3BDB94F17765EE77", subtitle="Fusion, and nothing less", desc=[
        "&eWhat:&r end-game power means fusion: more energy than everything else on this page together.",
        "&eHow:&r a netherite ingot opens the section.",
        "&eTip:&r the Mekanism: Power page walks through fission and fusion step by step."]),
    Q("pw_fusion", 0, 0, [item(GEN + "fusion_reactor_controller")], "Fusion", section=S_END, deps=["pw_end", "pw_dt_fuel", "t6_waste"],
      xp=1000, mirror="43D83CFA824B0A70", subtitle="The power of a star", desc=[
        "&6The power of a star, in a box you built. This is what you were.&r",
        "&eWhat:&r Mekanism's fusion reactor, the top of the power tree.",
        "&eChemistry:&r D + T → ⁴He + n + 17.6 MeV, millions of times more energy per kilogram than any chemical reaction.",
        "&eHow:&r a filled Hohlraum in the controller, then a burst from a Laser through a Laser Amplifier to ignite it. Layout: Just Enough Mekanism Multiblocks."]),

    # ===== Mekanism Power Plant (ours; the Mekanism pages build on these) ====================
    Q("pw_adv_cube", 0, 0, [item(MEK + "advanced_energy_cube")], "Bigger Cubes", section=S_MEKP,
      subtitle="Alloys and energy tablets around the cube below", deps=["pw_cube", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the Advanced Energy Cube holds and moves much more energy.",
        "&eHow:&r a basic cube with infused alloy, osmium ingots and energy tablets around it (check JEI). Upgrading in place keeps the stored energy.",
        "&eTip:&r Elite and Ultimate cubes follow the same pattern with reinforced and atomic alloys."]),
    Q("pw_brine", 0, 0, [item(MEK + "thermal_evaporation_controller"), item(MEK + "brine_bucket")], "Evaporation Ponds", section=S_MEKP,
      subtitle="Sunlight and heat concentrate brine", deps=["pw_adv_cube"], xp=150, desc=[
        "&eWhat:&r the Thermal Evaporation Plant boils water down into brine, and brine down into liquid lithium.",
        "&eChemistry:&r real lithium comes from salt flats: brine sits in ponds until the water evaporates and the salts concentrate.",
        "&eHow:&r a multiblock tower of Thermal Evaporation Blocks, Valves and one Controller. See Just Enough Mekanism Multiblocks in JEI.",
        "&eTip:&r taller towers and more heat run faster. Feed it plain water."]),
    Q("pw_lithium", 0, 0, [item(MEK + "dust_lithium", 8)], "Lithium", section=S_MEKP, subtitle="The battery metal", deps=["pw_brine"], xp=150, desc=[
        "&eWhat:&r lithium dust, for induction cells (and later, tritium).",
        "&eChemistry:&r lithium is the lightest metal and gives up its electron easily, which is why lithium-ion batteries store so much energy for their weight.",
        "&eHow:&r run brine through the plant again for liquid lithium. Turn it into gas in a Rotary Condensentrator, then crystallise it in a Chemical Crystallizer.",
        "&eTip:&r check JEI with &eR&r on Lithium Dust to confirm each step."]),
    Q("pw_fission_safety", 0, 0, [item(GEN + "fission_reactor_logic_adapter", 2)], "Reactor Safety", section=S_MEKP,
      subtitle="Build the off-switch first", deps=["pw_mid", "t6_fission"], xp=200, desc=[
        "&eWhat:&r Logic Adapters let redstone read the reactor and switch it off.",
        "&eChemistry:&r a fission reactor makes heat by splitting heavy nuclei. If heat can't escape fast enough, the reactor takes damage; at 100% it melts down.",
        "&eHow:&r set one adapter to emit a signal on damage or high temperature (pick the mode in its GUI) and wire it to another in Activation mode.",
        "&eTip:&r start at a low burn rate (0.1 mB/t), keep coolant flowing, and drain waste and heated coolant constantly."]),
    Q("pw_turbine", 0, 0, [item(GEN + "turbine_casing", 16)], "Industrial Turbine", section=S_MEKP, subtitle="Steam into enormous power",
      deps=["pw_fission_safety"], xp=300, desc=[
        "&eWhat:&r Mekanism's multiblock turbine. Feed it steam from fission or a boiler and it makes huge amounts of FE.",
        "&eHow:&r casings, valves, vents, rotors with blades, a rotational complex, a pressure disperser and electromagnetic coils. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r a Saturating Condenser turns spent steam back into water, closing the loop."]),
    Q("pw_dt_fuel", 0, 0, [item(MEK + "solar_neutron_activator"), item(GEN + "hohlraum")], "D-T Fuel", section=S_MEKP,
      subtitle="Deuterium and tritium", deps=["pw_turbine", "pw_lithium"], xp=300, desc=[
        "&eWhat:&r fusion fuel: deuterium and tritium, the two heavy isotopes of hydrogen.",
        "&eChemistry:&r deuterium comes from heavy water (D₂O). Tritium is bred from lithium by neutrons: ⁶Li + n → ³H + ⁴He.",
        "&eHow:&r electrolyse heavy water for deuterium; put lithium in the Solar Neutron Activator for tritium. Combine them into D-T fuel in the Chemical Infuser, then fill a Hohlraum with it (a chemical tank's item slot works; see its tooltip).",
        "&eTip:&r heavy water comes from a Mekanism Electric Pump with a Filter Upgrade."]),

    # ===== Steam and Diesel (ours) ===========================================================
    Q("pw_mi_storage", 0, 0, [item("modern_industrialization:lv_storage_unit")], "EU Storage", section=S_MI,
      subtitle="Optional: a battery for MI's grid", deps=["pw_storing", "t3_hull"], xp=60, **OPT, desc=[
        "&eWhat:&r MI's storage unit holds EU, Modern Industrialization's electricity.",
        "&eHow:&r built from redstone batteries, battery alloy plates and an LV hull. Put it between your turbine and your machines.",
        "&eTip:&r a buffer lets your steam turbine keep running while machines are idle."]),
    Q("pw_mv_turbine", 0, 0, [item("modern_industrialization:mv_steam_turbine")], "MV Steam Turbine", section=S_MI,
      subtitle="Optional: more steam, more EU", deps=["pw_mi_storage", "t4_mv"], xp=100, **OPT, desc=[
        "&eWhat:&r a bigger steam turbine that outputs MV power.",
        "&eChemistry:&r a turbine converts the energy of hot, expanding steam into rotation, then a generator turns rotation into current.",
        "&eHow:&r assemble it from an MV hull, aluminum rotors and large motors (check JEI)."]),
    Q("pw_transformer", 0, 0, [item("modern_industrialization:lv_mv_transformer")], "Transformers", section=S_MI,
      subtitle="Optional: step voltage between tiers", deps=["pw_mv_turbine"], xp=75, **OPT, desc=[
        "&eWhat:&r a transformer moves energy between two neighbouring voltage tiers (LV and MV here).",
        "&eHow:&r place it between an MV cable and your LV machines (or the other way round). Check which face is which in its tooltip.",
        "&eTip:&r real grids do the same: high voltage for transmission, low voltage at the socket."]),
    Q("pw_hv_turbine", 0, 0, [item("modern_industrialization:hv_steam_turbine")], "HV Steam Turbine", section=S_MI,
      subtitle="Optional: high-voltage steam", deps=["pw_transformer", "t5_hv"], xp=150, **OPT, desc=[
        "&eWhat:&r the HV steam turbine, for HV machine lines.",
        "&eHow:&r check JEI for the recipe. Feed it from a large boiler.",
        "&eTip:&r more steam than one turbine can eat? Add a second turbine on the same steam line."]),
    Q("pw_large_turbine", 0, 0, [item("modern_industrialization:large_steam_turbine")], "Large Steam Turbine", section=S_MI,
      subtitle="Optional: power-station scale", deps=["pw_hv_turbine", "t6_pu"], xp=300, **OPT, desc=[
        "&eWhat:&r MI's multiblock steam turbine. It eats steam by the thousands of mB and makes serious EU.",
        "&eHow:&r the controller needs an HV steam turbine, a processing unit (EV) and a highly advanced hull. Layout: JEI or the MI guidebook.",
        "&eTip:&r pair it with a large boiler or a reactor's steam output."]),
    Q("pw_diesel", 0, 0, [item("modern_industrialization:mv_diesel_generator")], "Diesel Generators", section=S_MI,
      subtitle="Optional: petrochemical power", deps=["pw_mid", "t5_diesel"], xp=150, **OPT, desc=[
        "&eWhat:&r MI generators that burn the fuels from your distillation tower.",
        "&eChemistry:&r diesel is a mix of hydrocarbons around C₁₂ to C₂₀. Long chains pack lots of C-H bonds, and lots of energy.",
        "&eHow:&r pipe diesel into the generator and cable it to your machines."]),
    Q("pw_large_diesel", 0, 0, [item("modern_industrialization:large_diesel_generator")], "Large Diesel Generator", section=S_MI,
      subtitle="Optional: factory-scale combustion", deps=["pw_diesel", "t5_hv"], xp=250, **OPT, desc=[
        "&eWhat:&r a multiblock diesel generator for real factories.",
        "&eHow:&r the 3D layout is in JEI and the MI guidebook. It needs fluid input and energy output hatches.",
        "&eTip:&r refined fuels (like boosted diesel) burn for more EU per bucket. Check JEI."]),

    # ===== The Furnace (ATM10 Generators centre) ============================================
    Q("pw_furnace", 0, 0, [item("minecraft:furnace")], "Furnaces and Generators", section=S_FURN, deps=["gs_furnace", "pw_iron_gen"], xp=30,
      size=1.5, subtitle="Two mods that make heat work harder", desc=[
        "&6Fire was the first thing you ever gave anyone. You remember that much.&r",
        "&eWhat:&r Iron Furnaces makes faster furnaces, tier by tier; Generator Galore makes burners for every odd fuel. Both start from the humble furnace.",
        "&eChemistry:&r a furnace is a controlled oxidation: fuel + O₂ → CO₂ + H₂O + heat. Better furnaces just waste less of that heat.",
        "&eHow:&r any vanilla furnace opens the section."]),

    # ===== Iron Furnaces =====================================================================
    if_furnace("pw_if_copper", "copper", ["pw_furnace"], 30, "a faster furnace from copper, and the start of the silver branch.",
               "copper ingots around a vanilla furnace (check JEI).", "every furnace tier can upgrade in place with an upgrade kit, keeping its contents."),
    if_furnace("pw_if_iron", "iron", ["pw_furnace"], 30, "the first real step up: smelts noticeably faster than vanilla.",
               "iron ingots around a vanilla furnace (check JEI).", "4x vanilla cooking is on in this pack, so even this one is quick."),
    if_furnace("pw_if_silver", "silver", ["pw_if_copper", "pw_if_iron"], 40, "the silver tier, between iron and gold.",
               "silver ingots and glass around an iron furnace (check JEI).", "silver comes from MI ore processing and the Mining dimension's veins.",
               extra="silver has the highest electrical and thermal conductivity of any metal (about 6% better than copper)."),
    if_furnace("pw_if_gold", "gold", ["pw_if_iron", "pw_if_silver"], 40, "the gold tier: faster again.",
               "gold ingots and a block of gold around an iron furnace (check JEI).", "a gold furnace on your ore line pays for itself quickly."),
    if_furnace("pw_if_diamond", "diamond", ["pw_if_gold"], 50, "the diamond tier.",
               "diamonds and glass around a gold furnace (check JEI).", "from here the tree splits into emerald and crystal."),
    if_furnace("pw_if_emerald", "emerald", ["pw_if_diamond"], 50, "the emerald tier.",
               "emeralds around a diamond furnace (check JEI).", "a villager trading hall makes emeralds cheap.",
               extra="emerald is the mineral beryl, Be₃Al₂Si₆O₁₈, coloured green by a trace of chromium."),
    if_furnace("pw_if_crystal", "crystal", ["pw_if_diamond"], 50, "the crystal tier, built with Nether quartz and glass.",
               "glass and an eye of ender around a diamond furnace (check JEI).", "obsidian next needs both the emerald and the crystal furnace.",
               extra="window glass is mostly SiO₂ with soda and lime. Unlike quartz, its atoms have no regular lattice: it is a frozen liquid, not a crystal."),
    if_furnace("pw_if_obsidian", "obsidian", ["pw_if_crystal", "pw_if_emerald"], 60, "the obsidian tier: very fast, and blast-proof.",
               "obsidian and blaze rods around an emerald furnace (check JEI).", "it's the base for the netherite tier.",
               extra="obsidian is volcanic glass: lava that cooled too fast to form crystals."),
    if_furnace("pw_if_netherite", "netherite", ["pw_if_obsidian", "t2_nether"], 80, "the top standard tier.",
               "netherite ingots, magma cream and a soul sand or soul soil block around an obsidian furnace (check JEI).", "the Rainbow Core needs one of these."),
    if_furnace("pw_if_atm", "allthemodium", ["pw_if_netherite"], 80, "a furnace from Allthemodium, beyond netherite.",
               "Allthemodium ingots and blocks around a netherite furnace (check JEI).",
               "the Allthemodium page covers where the metal comes from.", subtitle="Optional: past netherite", **OPT),
    if_furnace("pw_if_vibranium", "vibranium", ["pw_if_atm"], 100, "the vibranium tier.",
               "vibranium around an Allthemodium furnace (check JEI).", "vibranium comes from the Other dimension.",
               subtitle="Optional: faster still", **OPT),
    if_furnace("pw_if_unobtainium", "unobtainium", ["pw_if_vibranium"], 120, "the fastest furnace in the mod.",
               "unobtainium around a vibranium furnace (check JEI).", "worth it only if you smelt by the hundred thousand.",
               subtitle="Optional: the last furnace", optional=True, tokens=2),

    # ===== The Rainbow Generator ============================================================
    Q("pw_if_core", 0, 0, [item(IF + "rainbow_core")], "Rainbow Core", section=S_RAINBOW, deps=["pw_if_netherite"], xp=80,
      subtitle="Seven colours around netherite", desc=[
        "&eWhat:&r the core of the Rainbow Generator.",
        "&eChemistry:&r stained glass gets its colour from metal ions in the glass: cobalt for blue, chromium for green, gold for ruby red.",
        "&eHow:&r red, orange, yellow, green, blue, purple and magenta stained glass around two netherite furnaces (check JEI)."]),
    Q("pw_if_plating", 0, 0, [item(IF + "rainbow_plating", 8)], "Rainbow Plating", section=S_RAINBOW,
      deps=["pw_if_iron", "pw_if_gold", "pw_if_diamond", "pw_if_emerald", "pw_if_obsidian", "pw_if_crystal", "pw_if_copper", "pw_if_silver"],
      xp=80, subtitle="One furnace of every tier, melted down", desc=[
        "&eWhat:&r eight plating, from one each of the copper, iron, silver, gold, diamond, emerald, crystal and obsidian furnaces.",
        "&eHow:&r shapeless, all eight furnaces together (check JEI).",
        "&eTip:&r upgrade kits make the furnaces cheaper than building each from scratch."]),
    Q("pw_if_rainbow", 0, 0, [item(IF + "million_furnace")] + [item(f"{IF}{m}_furnace") for m in FURNACES], "The Rainbow Generator",
      section=S_RAINBOW, deps=["pw_if_plating", "pw_if_core", "pw_if_netherite"], xp=200, size=1.5,
      subtitle="Every furnace working together", desc=[
        "&eWhat:&r the Rainbow Furnace, plus one furnace of every other tier. When every tier runs as a generator, it makes a great deal of FE.",
        "&eHow:&r 8 rainbow plating around a rainbow core. Put a Generator augment in one furnace of each tier and keep them all burning; the tooltip explains the rest.",
        "&eTip:&r you can only have one Rainbow Generator, so pick its spot with care."]),
    Q("pw_if_rainbow_coal", 0, 0, [item(IF + "rainbow_coal")], "Rainbow Coal", section=S_RAINBOW, deps=["pw_if_rainbow"], xp=100,
      **OPT, subtitle="Optional: a fuel with no recipe", desc=[
        "&eWhat:&r a fuel that burns for a very long time. It has no crafting recipe.",
        "&eHow:&r read the Rainbow Furnace's tooltip carefully. It hints at what to do.",
        "&eTip:&r try it far from anything you love."]),

    # ===== Furnace Augments ==================================================================
    Q("pw_if_augments", 0, 0, [item("minecraft:paper")], "Augments", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=20,
      subtitle="Cards that change what a furnace does", desc=[
        "&eWhat:&r augments go in a furnace's side slots and change how it works: blasting, smoking, more slots, speed, efficiency or power.",
        "&eHow:&r every augment starts with paper (check JEI). A furnace takes one of each type.",
        "&eTip:&r speed and fuel efficiency pull in opposite directions; pick one per furnace."]),
    augment("pw_if_aug_blasting", "blasting", "Blasting Augment", "A blast furnace in disguise",
            "makes the furnace act as a blast furnace: faster on ores and metal, no food.",
            "put it on the furnace your ore line feeds."),
    augment("pw_if_aug_smoking", "smoking", "Smoking Augment", "A smoker in disguise",
            "makes the furnace act as a smoker: fast on food only.",
            "one smoking furnace next to the kitchen is plenty."),
    augment("pw_if_aug_factory", "factory", "Factory Augment", "Several slots at once",
            "turns the furnace into a factory with several input and output slots that smelt side by side.",
            "a factory furnace plus a pipe to storage is a whole smelting room in one block."),
    augment("pw_if_aug_generator", "generator", "Generator Augment", "A furnace that makes FE",
            "turns the furnace into a generator that burns fuel for FE instead of smelting.",
            "the Rainbow Generator needs one of these in a furnace of every tier."),
    augment("pw_if_aug_speed", "speed", "Speed Augment", "Faster, hungrier",
            "makes the furnace smelt faster at the cost of more fuel.",
            "good on furnaces fed by a steady fuel line."),
    augment("pw_if_aug_fuel", "fuel", "Efficiency Augment", "Slower, thriftier",
            "makes fuel last longer at the cost of speed.",
            "good on furnaces you fill by hand."),
    Q("pw_if_heater", 0, 0, [item(IF + "heater"), item(IF + "item_heater")], "Wireless Heating", section=S_AUG,
      deps=["pw_if_copper", "pw_if_iron"], xp=40, subtitle="Fuel furnaces with FE from afar", desc=[
        "&eWhat:&r the Heater stores FE; a Heater card links a furnace to it, so the furnace burns electricity instead of fuel.",
        "&eHow:&r check JEI for both. Right-click the heater with the card, then put the card in a furnace.",
        "&eTip:&r one heater can feed a whole row of furnaces."]),
    Q("pw_if_copy", 0, 0, [item(IF + "item_copy")], "Configuration Copier", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=20,
      subtitle="Set one furnace, paste to the rest", desc=[
        "&eWhat:&r copies a furnace's side settings and pastes them onto another.",
        "&eHow:&r check JEI. Sneak-click to copy, click to paste.",
        "&eTip:&r set one furnace's input, output and fuel faces, then paste it down the row."]),
    Q("pw_if_spooky", 0, 0, [item(IF + "item_spooky")], "Furnace Spooka-lator", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=10,
      subtitle="A seasonal disguise", desc=[
        "&eWhat:&r a purely cosmetic trick: right-click a furnace and it takes on a spooky look.",
        "&eHow:&r a carved pumpkin and a furnace, shapeless.",
        "&eTip:&r sneak-right-click the furnace to undo it."]),
    Q("pw_if_xmas", 0, 0, [item(IF + "item_xmas")], "Furnace Wrapping Paper", section=S_AUG, deps=["pw_if_copper", "pw_if_iron"], xp=10,
      subtitle="Wrap a furnace as a gift", desc=[
        "&eWhat:&r another cosmetic: right-click a furnace to wrap it like a present.",
        "&eHow:&r check JEI for the recipe.",
        "&eTip:&r sneak-right-click to unwrap it again."]),

    # ===== Generator Galore ==================================================================
    gg("pw_gg_copper", "copper", ["pw_furnace"], 30, "The cheapest burner", "Generator Galore's first generator: slow, but very cheap.",
       "copper ingots around a furnace, with a redstone block (check JEI).", "the iron generator from your T1 power quest is the next step up."),
    gg("pw_gg_iron", "iron", ["pw_gg_copper"], 30, "The workhorse burner", "a steady fuel burner and the root of the Generator Galore tree.",
       "iron ingots around a copper generator, with a redstone block (check JEI).", "every later generator is built from this one or its children."),
    gg("pw_gold_gen", "gold", ["pw_gg_iron"], 60, "Same fuel, more FE per tick", "it burns fuel faster and makes more FE per tick.",
       "upgrade from the iron generator (check JEI), or use the iron-to-gold upgrade kit on a placed one.",
       "a faster burn needs a steadier fuel supply. Pipe in charcoal from a tree farm."),
    gg("pw_gg_culinary", "culinary", ["pw_gold_gen"], 50, "Spare food into power", "burns food; better food burns longer.",
       "crops, a cake and eggs around a gold generator, with a redstone block (check JEI).", "hook it to a farm's overflow.",
       chem="food energy is chemical energy: a kilocalorie is about 4.2 kJ, whether your body or a generator releases it."),
    gg("pw_gg_collection", "diamond", ["pw_gold_gen"], 60, "A gem-tier burner", "a much stronger fuel burner, and the start of the gem branch.",
       "a gold generator in diamonds with a redstone block (check JEI).", "feed it coal blocks; loose coal won't keep up."),
    gg("pw_gg_netherite", "netherite", ["pw_gg_collection", "t2_nether"], 100, "The strongest solid-fuel burner",
       "the netherite generator burns ordinary fuel at a very high rate.",
       "smithing table: template, diamond generator and a netherite ingot (check JEI).", "it leads to the Nether Star generator."),
    gg("pw_gg_gems", "emerald", ["pw_gg_collection"], 80, "Emeralds for a hotter burn", "a step past diamond on the same fuel.",
       "a diamond generator in emeralds with a redstone block (check JEI).", "villagers are the cheapest emerald source.",
       chem="emerald is beryl, Be₃Al₂Si₆O₁₈. The beryllium in it is one of the lightest metals there is."),
    gg("pw_gg_obsidian", "obsidian", ["pw_gg_collection", "t2_obsidian"], 60, "The hub of the late tree",
       "a stronger burner, and the base for the ender, enchantment and magmatic generators.",
       "a diamond generator in obsidian with a redstone block (or the diamond-to-obsidian upgrade kit).", "JEI shows the whole tree."),
    gg("pw_gg_sweet", "honey", ["pw_gg_culinary"], 60, "Bees into power", "burns honey.",
       "a culinary generator in honey blocks with buckets and a redstone block (check JEI).",
       "a few beehives with campfires underneath keep it running.",
       chem="honey is about 80% sugars (fructose and glucose). Sugar burns well: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O."),
    gg("pw_gg_potion", "potion", ["pw_gg_culinary"], 60, "Leftover potions into power", "burns potions; stronger potions burn longer.",
       "pink dye around a culinary generator, with brewing stands and a redstone block (check JEI).", "every failed brew finally has a use."),
    gg("pw_gg_enchant", "enchantment", ["pw_gg_obsidian"], 70, "Junk books into power", "burns enchanted books and items.",
       "an obsidian generator in enchanted books with an enchanting table (check JEI).", "fishing junk books finally have a use."),
    gg("pw_gg_magmatic", "magmatic", ["pw_gg_obsidian"], 70, "Lava into power", "burns lava, a bucket at a time or by pipe.",
       "gold ingots around an obsidian generator, with a lava bucket (check JEI).", "a Nether lava lake and a pump give endless fuel.",
       chem="lava is molten silicate rock at roughly 700 to 1,200 °C."),
    gg("pw_gg_ender", "ender", ["pw_gg_obsidian"], 70, "Pearls into power", "burns ender pearls.",
       "an obsidian generator in ender pearls with a redstone block (check JEI).", "an enderman farm feeds it for ever."),
    gg("pw_gg_star", "netherstar", ["pw_gg_netherite"], 150, "Fuel fit for a god", "the Nether Star Generator burns Nether Stars for an enormous amount of FE.",
       "wither skeleton skulls around a netherite generator, with a redstone block (check JEI).", "save most stars for Powah's nitro crystals.",
       chem="real stars run on fusion: four hydrogen nuclei become one helium nucleus, and a little mass becomes a lot of energy, E = mc²."),
    gg("pw_gg_halitosis", "halitosis", ["pw_gg_ender"], 100, "Dragon's breath into power", "burns dragon's breath, bottled from the dragon's attacks in the End.",
       "amethyst around an ender generator, with an end rod (check JEI).", "plan an End trip and bring empty bottles."),
    Q("pw_gg_8x", 0, 0, [anyof(GG_8X)], "Eight Times the Burn", section=S_GG, deps=["pw_gg_copper", "w_ancient"], xp=80,
      subtitle="Compressed generators", desc=[
        "&eWhat:&r 8x generators burn fuel eight times as fast and make eight times the FE in one block. Any 8x generator counts.",
        "&eHow:&r eight generators of a tier around an echo shard (check JEI). Echo shards come from Ancient City chests.",
        "&eTip:&r make sure the fuel line can keep up first."]),
    Q("pw_gg_64x", 0, 0, [anyof(GG_64X)], "Sixty-Four Times", section=S_GG, deps=["pw_gg_8x"], xp=120, subtitle="Compressed again", desc=[
        "&eWhat:&r 64x generators: eight 8x generators in one block. Any one counts.",
        "&eHow:&r eight 8x generators around a conduit (check JEI).",
        "&eTip:&r a 64x generator eats fuel 64 times as fast. Feed it from storage, not a chest."]),
    Q("pw_gg_upgrade", 0, 0, [item(GG + "iron_to_gold_upgrade")], "Upgrade in Place", section=S_GG, deps=["pw_gold_gen"], xp=30, **OPT,
      subtitle="Optional: upgrade a generator without breaking it", desc=[
        "&eWhat:&r Generator Galore upgrade kits turn a placed generator into the next tier, keeping its fuel and connections.",
        "&eHow:&r gold ingots, an item frame and a redstone block for iron → gold (check JEI for the others). Right-click the placed generator.",
        "&eTip:&r the tree branches: gold leads to diamond or to the food-burning Culinary Generator."]),
], links=[("t1_power", 0, 0), ("gs_furnace", 0, 0), ("t6_fission", 0, 0), ("t4_uraninite", 0, 0)])
