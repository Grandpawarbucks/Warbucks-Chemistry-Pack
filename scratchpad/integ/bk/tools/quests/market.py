"""Quest chapter: market (the Demigod Token shop). See tools/quests/STYLE.md.
The supply shop is in pack/kubejs/server_scripts/phase4_chemistry.js, section 5 (shapeless recipes).

MACHINE SHOP (bottom of this file): repeatable quests that sell copies of machines, boilers, tanks, hulls and cables.
Rule: BUILD YOUR FIRST, BUY THE REST. Each entry depends on the quest where the player builds that machine and stays
invisible until then (locked_hidden), so tokens save the grind of copies and never skip a tier.
Prices follow docs/research/shop_brief.md: Steam 3-6 tokens, LV 8-15, MV 2-3 Greater, HV 4-6 Greater, EV 8+ Greater.

Layout is manual (like the other shop chapters): the market quests sit at the top; below them, one block of rows per
tier (Steam y=5, LV y=11, MV y=17, HV y=23, EV y=29). Each block starts with a counter quest at x=0 and its entries
follow, 10 per line, in the order they are written.

Helpers (one line per entry):
    counter(key, title, milestone, prev, y, band, price_note)
  -> the optional checkmark "shop counter" at (0, y) that opens one tier block after that tier's milestone.
    shop_entry(name, item_id, price, built_in, built_title, what, count=1, coin=T, title=None)
  -> key "mk_buy_<name>" (never rename it), deps [built_in], pays `price` x `coin` on Submit, placed on the
     block of the counter written just before it.
"""
from questlib import Q, Chapter, item, tick, SIDE  # noqa: F401

T = "kubejs:demigod_token"
G = "kubejs:greater_demigod_token"
MI = "modern_industrialization:"

PER_LINE = 10   # entries per line before wrapping
STEP_X = 1.5
STEP_Y = 1.5
_rows = []      # [y, entries placed so far] per tier block


def counter(key, title, milestone, prev, y, band, price_note):
    """Tier 'shop counter' checkmark (optional, no reward) at (0, y): opens one tier block of the Machine Shop."""
    _rows.append([y, 0])
    return Q(key, 0, y, [tick()], title, deps=[prev, milestone], tokens=0, xp=0, optional=True, size=1.5,
             subtitle=f"{band} machines · {price_note}", desc=[
                 f"&eWhat:&r the {band} counter of the Machine Shop.",
                 "&eHow:&r click to open it. Each machine in this row appears once you finish the quest where you build it yourself.",
                 f"&eTip:&r prices at this counter are {price_note}."])


def shop_entry(name, item_id, price, built_in, built_title, what, count=1, coin=T, title=None):
    """One Machine Shop quest: hand in `price` x `coin` (taken on Submit), receive `count` x `item_id`. Repeatable.

    name: key suffix (key = "mk_buy_<name>"). built_in: key of the quest where the player builds this machine.
    built_title: that quest's title (shown in the subtitle). what: one sentence on what the machine does.
    Placed on the block of the last counter() written above it.
    """
    row = _rows[-1]
    i = row[1]
    row[1] += 1
    x = STEP_X * (1 + i % PER_LINE)
    y = row[0] + STEP_Y * (i // PER_LINE)
    unit = "Greater Token" if coin == G else "token"
    cost = f"{price} {unit}{'s' if price != 1 else ''}"
    label = title or name.replace("_", " ").title()
    got = f"{count} {label}s" if count > 1 else f"one {label}"
    return Q(f"mk_buy_{name}", x, y, [item(coin, price)], label + (f" x{count}" if count > 1 else ""),
             deps=[built_in], items=[(item_id, count)], tokens=0, xp=0, optional=True,
             repeat=True, consume=True, locked_hidden=True,
             subtitle=f"{cost} · unlocked by {built_title}", desc=[
                 f"&eWhat:&r {what} This is a copy of something you already built yourself.",
                 f"&eHow:&r hold {cost} and click &eSubmit&r. The tokens are taken and you get {got}.",
                 "&eTip:&r repeatable: buy as many as you need."])


CHAPTER = Chapter("market", "The Demigod's Market", T,
        ["Spend your Demigod Tokens: supplies and comforts, never shortcuts."], SIDE, [
    Q("mk_intro", 0, 0, [tick()], "The Market", deps=["wel_tokens"], xp=20, tokens=1,
      subtitle="What Demigod Tokens are for", desc=[
        "&6You remember offerings left at your altar. Now the world pays you in coins instead.&r",
        "&eWhat:&r Demigod Tokens are the reward currency of this book. You trade them for supplies by crafting, with no shopkeeper and no server plugin.",
        "&eHow:&r every shop trade is a shapeless crafting recipe: put tokens in a crafting grid and the item appears.",
        "&eHow:&r the price list is JEI: search &eDemigod Token&r and press &eU&r (uses). Every trade shows as a crafting recipe. Do the same for the Greater Demigod Token.",
        "&eTip:&r the crafting shop sells raw supplies and comforts, never anything that skips a tier. Copies of machines you have already built are in the Machine Shop quests.",
        "{@pagebreak}",
        "&eWhat tokens never buy:&r the shop skips boring gathering (sand, gravel, string, torches), never learning. If a trade seems missing, it was left out on purpose.",
        "&eChemistry:&r a bag of raw ore is not a refinery. Raw tin still needs your crusher, raw titanium still needs your blast furnace."]),
    Q("mk_earn", 2, 0, [item(T)], "Where Tokens Come From", deps=["mk_intro"], xp=20, tokens=1,
      subtitle="Every quest pays", desc=[
        "&eWhat:&r almost every quest pays tokens, scaled by tier: 1 per quest at the start, 2 in the steam and Nether chapters, 3 at LV and MV, 4 at HV, 5 at EV, 8 in space.",
        "&eHow:&r milestone quests (the big ones) pay double and also roll that tier's reward table. Optional side quests pay 1 or 2.",
        "&eTip:&r on a team, rewards go to each player who claims them, so everyone builds their own purse."]),
    Q("mk_small", 4, 0, [tick()], "The Price Bands", deps=["mk_earn"], xp=60, tokens=1,
      subtitle="Small, medium and large trades", desc=[
        "&eWhat:&r the shop has three price bands. Small (1 to 3 tokens): cheap stacks of things you'd otherwise spend an afternoon gathering. Medium and large are on the next pages.",
        "&eHow:&r 1 token: 32 torches, 16 bread, 8 bottles o' enchanting, 32 bone meal, 64 sand, 64 gravel or 32 clay balls.",
        "&eHow:&r 2 tokens: 16 iron ingots, 16 coke, 16 rubber sheets, 16 fire clay dust, 32 salt dust, 16 string, 16 leather or a sleeping bag.",
        "&eHow:&r 3 tokens: 8 osmium ingots, 2 backpack upgrade bases, 16 gunpowder, 16 slime balls, 32 redstone or 16 lapis.",
        "&eTip:&r sand and gravel are the best early value: concrete, glass and silicon all start there.",
        "{@pagebreak}",
        "&eMedium band (4 to 8 tokens):&r raw ores (you still process them yourself) and drops you would otherwise farm.",
        "&eHow:&r 4 tokens: a Warp Stone, 32 raw copper, 16 raw tin, 16 raw lead, 16 bauxite dust, 32 quartz or 32 glowstone dust.",
        "&eHow:&r 5: 16 raw nickel, 8 ender pearls, 4 phantom membranes, 16 amethyst. 6: 8 blaze rods, 4 ghast tears, 16 certus quartz, 8 source gems.",
        "&eHow:&r 7: 8 raw titanium or 2 name tags. 8: 8 raw tungsten or 32 prismarine shards.",
        "&eTip:&r raw ore bought here is worth up to 5x once your Mekanism line is running. Buy late, process well.",
        "{@pagebreak}",
        "&eLarge band (Greater Tokens):&r the big trades cost Greater Demigod Tokens, not regular ones.",
        "&eHow:&r 1 Greater: 4 golden apples, 4 diamonds, 16 emeralds or a saddle. 2: 2 shulker shells, a heart of the sea or a netherite scrap.",
        "&eHow:&r 3 Greater: a totem of undying or 4 echo shards. 4 Greater: an enchanted golden apple.",
        "&eTip:&r shulker shells mean shulker boxes. Many players find that the best trade in the shop."]),
    Q("mk_exchange", 6, 0, [item(G)], "The Exchange", deps=["mk_small"], xp=50, tokens=1,
      subtitle="Nine tokens make one Greater Token", desc=[
        "&eWhat:&r a Greater Demigod Token is worth 9 Demigod Tokens, and the trade works both ways.",
        "&eHow:&r 9 tokens in a crafting grid make 1 Greater Token. 1 Greater Token alone in the grid gives the 9 back.",
        "&eTip:&r late-tier milestones and boss loot sometimes pay Greater Tokens directly."]),

    # --- Market days (y=2): hold tokens, pick a reward -----------------------------------------
    Q("mk_day_early", 4, 2, [item(T, 10)], "Market Day: Early", deps=["mk_small", "gs_iron"], xp=50, tokens=1,
      choice="pick_early", subtitle="Hold 10 tokens; pick a comfort", desc=[
        "&eWhat:&r a reward for saving. Hold 10 Demigod Tokens at once and choose one comfort: a sleeping bag, a Warp Stone, backpack upgrade bases or a saddle.",
        "&eHow:&r the tokens are only checked, not taken. Spend them afterwards if you like.",
        "&eTip:&r the Warp Stone is the pick if you explore a lot."]),
    Q("mk_day_mid", 6, 2, [item(T, 30)], "Market Day: Industrial", deps=["mk_day_early", "t3_analog"], xp=100, tokens=1,
      choice="pick_mid", subtitle="Hold 30 tokens; pick a feedstock", desc=[
        "&eWhat:&r hold 30 tokens and choose a stack of raw feedstock: tin, lead, nickel, bauxite or salt.",
        "&eHow:&r tokens are checked, not taken.",
        "&eTip:&r bauxite is the slow one to find, and aluminium is the gate to MV."]),
    Q("mk_day_late", 8, 2, [item(T, 64)], "Market Day: Divine", deps=["mk_day_mid", "t6_pu"], xp=200, tokens=2, size=2.0, shape="gear",
      choice="pick_late", subtitle="Hold 64 tokens; pick a treasure", desc=[
        "&6You remember when worshippers brought you treasures. Now you just keep a full stack.&r",
        "&eWhat:&r hold a full stack of 64 tokens and choose a treasure: a totem, shulker shells, a heart of the sea, an enchanted golden apple or 3 Greater Tokens.",
        "&eHow:&r tokens are checked, not taken. Exchange Greater Tokens back if you need 64 loose ones.",
        "&eTip:&r picking the Greater Tokens is the same as taking 27 regular tokens home."]),

    # --- Secret -----------------------------------------------------------------------------------
    Q("mk_sec_hoard", 8, 0, [item(G, 9)], "A Dragon's Hoard", deps=["mk_exchange"], secret=True, optional=True, tokens=1,
      loot="secret", subtitle="81 tokens' worth, unspent", desc=[
        "&eWhat:&r hold nine Greater Demigod Tokens at once. That's 81 tokens you chose not to spend.",
        "&eTip:&r the demigod approves of patience. The demigod also notes that totems exist."]),
    # --- The Machine Shop: build your first, buy the rest ---------------------------------------
    Q("mk_shop", 0, 2, [tick()], "The Machine Shop", deps=["mk_intro"], tokens=0, xp=20, optional=True,
      subtitle="Build your first, buy the rest", desc=[
        "&6You remember forges that worked while you slept. Once you know how a thing is made, its copies come cheap.&r",
        "&eWhat:&r repeatable shop quests that sell copies of machines, boilers, tanks, hulls and cables.",
        "&eHow:&r a machine goes on sale only after you finish the quest where you build it yourself. Until then its entry is invisible.",
        "&eHow:&r hold the price and click &eSubmit&r: the tokens are taken and the machine is yours. Buy again whenever you like.",
        "&eTip:&r counters run Steam, LV, MV, HV, EV. From MV up, prices are in Greater Demigod Tokens (9 tokens each). Multiblock controllers are never sold."]),

    # Steam (T0-T1): bronze and steel steam machines, boilers, tanks (tokens)
    counter("mk_shop_steam", "Counter: Steam", "t0_boiler", "mk_shop", 5, "Steam", "3 to 6 tokens"),
    shop_entry("bronze_tank", MI + "bronze_tank", 3, "t0_tank", "Bronze Tank", "Holds water, steam or any other fluid.", title="Bronze Tank"),
    shop_entry("bronze_casing", MI + "bronze_machine_casing", 3, "t0_casing", "Bronze Machine Casing", "The frame of every bronze machine.", title="Bronze Machine Casing"),
    shop_entry("fluid_pipe", MI + "fluid_pipe", 3, "t0_pipes", "Fluid Pipes", "Pipes that carry water and steam.", count=16, title="Fluid Pipe"),
    shop_entry("bronze_furnace", MI + "bronze_furnace", 3, "t0_furnace", "Steam Furnace", "Smelts with steam instead of fuel.", title="Steam Furnace"),
    shop_entry("bronze_boiler", MI + "bronze_boiler", 4, "t0_boiler", "Steam Power", "Burns fuel to boil water into steam.", title="Bronze Boiler"),
    shop_entry("bronze_compressor", MI + "bronze_compressor", 4, "t0_compressor", "Steam Compressor", "Presses ingots into plates.", title="Steam Compressor"),
    shop_entry("bronze_mixer", MI + "bronze_mixer", 4, "t0_mixer", "Steam Mixer", "Mixes dusts into alloys and compounds.", title="Steam Mixer"),
    shop_entry("bronze_cutter", MI + "bronze_cutting_machine", 4, "t0_cutter", "Steam Cutting Machine", "Cuts rods into bolts and more.", title="Steam Cutting Machine"),
    shop_entry("bronze_macerator", MI + "bronze_macerator", 5, "t0_macerator", "Steam Macerator", "Grinds ore into dust.", title="Steam Macerator"),
    shop_entry("bronze_water_pump", MI + "bronze_water_pump", 5, "t0_pump", "Endless Water", "Pumps endless water for your boilers.", title="Bronze Water Pump"),
    shop_entry("steel_upgrade", MI + "steel_upgrade", 4, "t1_opt_steel_machines", "Steel Upgrades", "Packs into a bronze steam machine to make its faster steel version.", title="Steel Upgrade"),
    shop_entry("steel_wiremill", MI + "steel_wiremill", 5, "t3_wiremill", "Steel Wiremill", "Draws plates into wire.", title="Steel Wiremill"),
    shop_entry("steel_packer", MI + "steel_packer", 5, "t1_opt_packer", "Packer and Unpacker", "Packs items into blocks and upgrades into machines.", title="Steel Packer"),
    shop_entry("steel_unpacker", MI + "steel_unpacker", 5, "t1_opt_packer", "Packer and Unpacker", "Unpacks blocks back into items.", title="Steel Unpacker"),
    shop_entry("steel_boiler", MI + "steel_boiler", 6, "t1_steel_boiler", "Steel Boiler", "A boiler with more steam output.", title="Steel Boiler"),
    shop_entry("steel_macerator", MI + "steel_macerator", 6, "t1_opt_steel_machines", "Steel Upgrades", "A faster steam macerator.", title="Steel Macerator"),

    # LV (T3): MI electric machines, hull, cable; Mekanism machines on basic control circuits (tokens)
    counter("mk_shop_lv", "Counter: LV", "t3_hull", "mk_shop_steam", 11, "LV", "8 to 15 tokens"),
    shop_entry("tin_cable", MI + "tin_cable", 8, "t3_wire", "Wires and Cables", "LV power cable.", count=16, title="Tin Cable"),
    shop_entry("lv_hull", MI + "basic_machine_hull", 10, "t3_hull", "LV Machine Hull", "The core of every LV machine.", title="LV Machine Hull"),
    shop_entry("polarizer", MI + "polarizer", 11, "t3_polarizer", "Polarizer", "Magnetises rods and wires.", title="Polarizer"),
    shop_entry("lv_steam_turbine", MI + "lv_steam_turbine", 12, "t3_turbine", "Steam to Electricity", "Turns steam into LV power.", title="LV Steam Turbine"),
    shop_entry("electric_mixer", MI + "electric_mixer", 12, "t3_mixer", "Electric Mixer", "Mixes dusts and fluids on power.", title="Electric Mixer"),
    shop_entry("electric_furnace", MI + "electric_furnace", 12, "t3_efurnace", "Electric Furnace", "Smelts on power.", title="Electric Furnace"),
    shop_entry("lv_storage", MI + "lv_storage_unit", 12, "t3_storage", "LV Storage Unit", "Stores LV energy.", title="LV Storage Unit"),
    shop_entry("electric_water_pump", MI + "electric_water_pump", 13, "t3_waterpump", "Electric Water Pump", "Pumps water on power.", title="Electric Water Pump"),
    shop_entry("electric_unpacker", MI + "electric_unpacker", 13, "t4_lv_machines", "Electric Helpers", "Unpacks blocks on power.", title="Electric Unpacker"),
    shop_entry("electric_wiremill", MI + "electric_wiremill", 14, "t3_ewiremill", "Electric Wiremill", "Draws wire on power.", title="Electric Wiremill"),
    shop_entry("electric_cutter", MI + "electric_cutting_machine", 14, "t3_cutting", "Cutting Machine", "Cuts rods, bolts and wafers on power.", title="Electric Cutting Machine"),
    shop_entry("electric_macerator", MI + "electric_macerator", 15, "t3_emacerator", "Electric Macerator", "Grinds ore into dust on power.", title="Electric Macerator"),
    shop_entry("electric_compressor", MI + "electric_compressor", 15, "t3_ecompressor", "Electric Compressor", "Presses plates on power.", title="Electric Compressor"),
    shop_entry("electric_packer", MI + "electric_packer", 15, "t3_packer", "Packer", "Packs items and parts on power.", title="Electric Packer"),
    shop_entry("assembler", MI + "assembler", 15, "t3_assembler", "Assembler", "Builds machines and components from parts.", title="Assembler"),
    shop_entry("metallurgic_infuser", "mekanism:metallurgic_infuser", 8, "t3_infuser", "Mekanism: Metallurgic Infuser", "Infuses carbon, redstone and more into metals.", title="Metallurgic Infuser"),
    shop_entry("chemical_tank", "mekanism:basic_chemical_tank", 8, "t4_tanks", "Bottled Gases", "Stores Mekanism gases.", title="Basic Chemical Tank"),
    shop_entry("energy_cube", "mekanism:basic_energy_cube", 10, "pw_cube", "Store It", "Stores Mekanism energy.", title="Basic Energy Cube"),
    shop_entry("enrichment_chamber", "mekanism:enrichment_chamber", 10, "t3_enrich", "Enrichment Chamber", "Doubles ore into dust.", title="Enrichment Chamber"),
    shop_entry("crusher", "mekanism:crusher", 10, "t3_crusher", "Crusher", "Crushes ingots back into dust.", title="Crusher"),
    shop_entry("energized_smelter", "mekanism:energized_smelter", 10, "mk2_smelter", "Energized Smelter", "Smelts on power.", title="Energized Smelter"),
    shop_entry("precision_sawmill", "mekanism:precision_sawmill", 10, "mk2_sawmill", "Precision Sawmill", "Saws logs into planks and sawdust.", title="Precision Sawmill"),
    shop_entry("electrolytic_separator", "mekanism:electrolytic_separator", 12, "t4_separator", "Mekanism Gases", "Splits fluids into gases, like water into H₂ and O₂.", title="Electrolytic Separator"),
    shop_entry("rotary_condensentrator", "mekanism:rotary_condensentrator", 12, "t4_vapor", "Water Vapor", "Turns gases into fluids and back.", title="Rotary Condensentrator"),
    shop_entry("chemical_oxidizer", "mekanism:chemical_oxidizer", 13, "t4_oxidizer", "Contact Process 1: SO₂", "Burns solids into gases, like sulfur into SO₂.", title="Chemical Oxidizer"),
    shop_entry("chemical_infuser", "mekanism:chemical_infuser", 13, "t4_so3", "Contact Process 2: SO₃", "Combines two gases, like SO₂ and O₂ into SO₃.", title="Chemical Infuser"),
    shop_entry("prc", "mekanism:pressurized_reaction_chamber", 15, "mk2_prc", "Pressurized Reaction Chamber", "Reacts a solid, a fluid and a gas together.", title="Pressurized Reaction Chamber"),

    # MV (T4): Greater Tokens
    counter("mk_shop_mv", "Counter: MV", "t4_mv", "mk_shop_lv", 17, "MV", "2 to 3 Greater Tokens"),
    shop_entry("mv_hull", MI + "advanced_machine_hull", 2, "t4_mv", "MV: Aluminum", "The core of every MV machine.", coin=G, title="MV Machine Hull"),
    shop_entry("lv_mv_transformer", MI + "lv_mv_transformer", 2, "pw_transformer", "Transformers", "Steps power between LV and MV.", coin=G, title="LV/MV Transformer"),
    shop_entry("purification_chamber", "mekanism:purification_chamber", 2, "t4_ore3", "3x Ore: Oxygen", "Triples ore with oxygen.", coin=G, title="Purification Chamber"),
    shop_entry("osmium_compressor", "mekanism:osmium_compressor", 2, "mk2_refined_obsidian", "Refined Obsidian", "Compresses dusts with liquid osmium.", coin=G, title="Osmium Compressor"),
    shop_entry("advanced_energy_cube", "mekanism:advanced_energy_cube", 2, "pw_adv_cube", "Bigger Cubes", "Stores more Mekanism energy.", coin=G, title="Advanced Energy Cube"),
    shop_entry("electrolyzer", MI + "electrolyzer", 3, "t4_electrolyzer", "Electrolysis", "Splits compounds with electric current.", coin=G, title="Electrolyzer"),
    shop_entry("chemical_reactor", MI + "chemical_reactor", 3, "t4_reactor", "The Chemical Reactor", "Runs MI's chemical reactions.", coin=G, title="Chemical Reactor"),
    shop_entry("centrifuge", MI + "centrifuge", 3, "t4_byproduct", "Ore Byproducts", "Separates mixtures by density.", coin=G, title="Centrifuge"),
    shop_entry("distillery", MI + "distillery", 3, "t5_opt_distillery", "The Distillery", "A one-output distillation column in a single block.", coin=G, title="Distillery"),
    shop_entry("mv_steam_turbine", MI + "mv_steam_turbine", 3, "pw_mv_turbine", "MV Steam Turbine", "Turns steam into MV power.", coin=G, title="MV Steam Turbine"),
    shop_entry("mv_diesel", MI + "mv_diesel_generator", 3, "pw_diesel", "Diesel Generators", "Burns liquid fuel for MV power.", coin=G, title="MV Diesel Generator"),
    shop_entry("injection_chamber", "mekanism:chemical_injection_chamber", 3, "t4_ore4", "4x Ore: Hydrogen Chloride", "Quadruples ore with hydrogen chloride.", coin=G, title="Chemical Injection Chamber"),
    shop_entry("dissolution_chamber", "mekanism:chemical_dissolution_chamber", 3, "t4_dissolution", "Dissolving Ore", "Dissolves ore in sulfuric acid.", coin=G, title="Chemical Dissolution Chamber"),
    shop_entry("chemical_washer", "mekanism:chemical_washer", 3, "t4_washer", "Washing Slurry", "Washes dirty slurry clean.", coin=G, title="Chemical Washer"),
    shop_entry("chemical_crystallizer", "mekanism:chemical_crystallizer", 3, "t4_ore5", "5x Ore: Dissolution", "Crystallizes clean slurry.", coin=G, title="Chemical Crystallizer"),

    # HV (T5): Greater Tokens
    counter("mk_shop_hv", "Counter: HV", "t5_hv", "mk_shop_mv", 23, "HV", "4 to 6 Greater Tokens"),
    shop_entry("hv_hull", MI + "turbo_machine_hull", 4, "t5_hv", "HV: Digital Circuits", "The core of every HV machine.", coin=G, title="HV Machine Hull"),
    shop_entry("combiner", "mekanism:combiner", 4, "mk2_combiner", "Combiner", "Combines dust and cobblestone back into ore.", coin=G, title="Combiner"),
    shop_entry("hv_steam_turbine", MI + "hv_steam_turbine", 5, "pw_hv_turbine", "HV Steam Turbine", "Turns steam into HV power.", coin=G, title="HV Steam Turbine"),
    shop_entry("neutron_activator", "mekanism:solar_neutron_activator", 6, "t6_polonium", "Polonium", "Uses sunlight to drive neutron activation.", coin=G, title="Solar Neutron Activator"),

    # EV (T6): Greater Tokens
    counter("mk_shop_ev", "Counter: EV", "t6_pu", "mk_shop_hv", 29, "EV", "8 or more Greater Tokens"),
    shop_entry("ev_hull", MI + "highly_advanced_machine_hull", 8, "t6_pu", "EV: Processing Units", "The core of every EV machine.", coin=G, title="EV Machine Hull"),
    shop_entry("isotopic_centrifuge", "mekanism:isotopic_centrifuge", 9, "t6_centrifuge", "Isotope Separation", "Separates uranium isotopes.", coin=G, title="Isotopic Centrifuge"),
], links=[("wel_tokens", -2, 0)], layout="manual")
