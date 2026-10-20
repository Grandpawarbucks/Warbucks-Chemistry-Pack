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
@@ROWS@@
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
        tip = "36 blocks of one tier make a full 3x3x4 stack. " + tip
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
