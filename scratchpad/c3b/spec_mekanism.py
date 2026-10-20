S_BASE, S_TIER, S_MACH, S_CHEM = '"Osmium and Steel"', '"Circuit Tiers"', '"Machines"', '"Chemical Machines"'
S_PIPE, S_UPG, S_BIG, S_EN, S_GAD = '"Pipes and Storage"', '"Upgrades"', '"Big Builds"', '"Energy"', '"Gadgets"'
S_O2, S_O3, S_O4, S_O5 = '"Ore Line: 2x"', '"Ore Line: 3x"', '"Ore Line: 4x"', '"Ore Line: 5x"'

EDIT = {
    "mk2_intro": {"mirror": '"58B125BD4876054C"', "section": S_BASE, "size": "2.0", "shape": '"gear"'},
    "mk2_configurator": {"mirror": '"5E116409DC7D30BB"', "section": S_PIPE, "deps": '["mk2_steel"]', "optional": "False",
                         "tokens": "None", "size": "2.0", "shape": '"gear"', "loot": '"t3"'},
    "mk2_tablet": {"mirror": '"4935209D870E25F2"', "section": S_EN, "deps": '["mk2_infused_alloy"]', "optional": "False",
                   "tokens": "None", "size": "2.0", "shape": '"gear"', "loot": '"t3"'},
    "mk2_adv_circuit": {"mirror": '"6263A27182B2CE3D"', "section": S_MACH, "tasks": '[item(MEK + "advanced_control_circuit")]',
                        "deps": '["mk2_steel_casing", "t4_mv"]'},
    "mk2_elite_circuit": {"mirror": '"71CF9E59F8F0B4A6"', "section": S_MACH, "tasks": '[item(MEK + "elite_control_circuit")]'},
    "mk2_ult_circuit": {"mirror": '"1ABD22AA58E093A6"', "section": S_MACH, "tasks": '[item(MEK + "ultimate_control_circuit")]'},
    "mk2_refined_obsidian": {"mirror": '"31B73D16C0199785"', "section": S_MACH, "tasks": '[item(MEK + "ingot_refined_obsidian")]',
                             "deps": '["mk2_compressor", "mk2_obsidian_dust"]'},
    "mk2_obsidian_dust": {"mirror": '"5B556192F060F3F1"', "section": S_MACH,
                          "tasks": '[item(MEK + "dust_refined_obsidian"), item(MEK + "dust_obsidian", 4)]',
                          "deps": '["mk2_infuser", "mk2_crusher"]', "optional": "False", "tokens": "None"},
    "mk2_teleport_core": {"deps": '["mk2_refined_obsidian", "mk2_atomic"]'},
    "mk2_teleporter": {"mirror": '"7B0DFA55B4D8B16D"', "section": S_BIG, "deps": '["mk2_infuser", "mk2_teleport_core"]',
                       "optional": "False", "tokens": "None"},
    "mk2_entangloporter": {"mirror": '"7CC49360D07086B8"', "section": S_BIG, "optional": "False", "tokens": "None"},
    "mk2_portable_tp": {"mirror": '"2EA0C74AE7366656"', "section": S_GAD, "deps": '["mk2_chargepad", "mk2_teleport_core"]',
                        "optional": "False", "tokens": "None"},
    "mk2_smelter": {"mirror": '"488DBE69595F38F8"', "section": S_MACH, "deps": '["mk2_steel_casing"]'},
    "mk2_sawmill": {"mirror": '"7ECA0633AF1AEC19"', "section": S_MACH, "deps": '["mk2_steel_casing"]'},
    "mk2_combiner": {"mirror": '"566C1DBA9829E328"', "section": S_MACH, "deps": '["mk2_elite_circuit"]', "optional": "False", "tokens": "None"},
    "mk2_upgrades": {"mirror": '"3C8D9278B81BB37A"', "section": S_UPG, "tasks": '[item(MEK + "upgrade_speed")]', "title": '"Speed Upgrade"',
                     "subtitle": '"Faster machines, bigger bills"', "deps": '["mk2_steel_casing", "mk2_glass"]'},
    "mk2_upgrade_set": {"mirror": '"763FB27929E053BE"', "section": S_UPG, "tasks": '[item(MEK + "upgrade_filter")]', "title": '"Filter Upgrade"',
                        "subtitle": '"Choose what the pump pulls up"', "deps": '["mk2_steel_casing", "mk2_glass"]', "optional": "False",
                        "tokens": "None", "desc": '''[
        "&eWhat:&r the Filter upgrade goes in an Electric Pump. With it the pump pulls heavy water out of ordinary water blocks instead of plain water.",
        "&eChemistry:&r heavy water is D₂O: water whose hydrogen atoms carry an extra neutron. About 1 molecule in 6,400 in seawater has a deuterium atom in it.",
        "&eHow:&r Infused Alloy and glass around tin dust (check JEI). One per pump.",
        "&eTip:&r heavy water is the start of deuterium, and later of fusion fuel."]'''},
    "mk2_installer": {"mirror": '"090B564935D7A8F5"', "section": S_UPG,
                      "tasks": '[anyof([MEK + t + "_tier_installer" for t in ("basic", "advanced", "elite", "ultimate")])]',
                      "deps": '["mk2_tier_basic"]', "optional": "False", "tokens": "None"},
    "mk2_cardboard": {"mirror": '"24BA664B60E49461"', "section": S_GAD},
    "mk2_heaters": {"mirror": '"21F3379C904BFD50"', "section": S_PIPE, "tasks": '[item(MEK + "resistive_heater")]', "title": '"Resistive Heater"',
                    "subtitle": '"Electricity in, heat out"', "deps": '["mk2_conductors", "pw_brine"]'},
    "mk2_dynamic_tank": {"mirror": '"1796E08BBDC09B84"', "section": S_PIPE,
                         "tasks": '[item(MEK + "dynamic_tank", 24), item(MEK + "dynamic_valve", 2)]',
                         "deps": '["mk2_chem_tanks", "mk2_fluid_tanks", "t3_mekcircuit"]'},
    "mk2_prc": {"mirror": '"71869B1D81D6A7EF"', "section": S_CHEM, "deps": '["mk2_steel_casing", "t4_separator"]'},
    "mk2_coal_gas": {"mirror": '"7276892E129A739B"', "section": S_CHEM, "tasks": '[item(MEK + "dust_sulfur")]', "title": '"Sulfur, the Key Element"',
                     "subtitle": '"Every chemical machine, one yellow dust"',
                     "deps": '["mk2_chem_infuser", "mk2_oxidizer", "mk2_dissolution", "mk2_enrich", "mk2_condensentrator", "mk2_prc"]',
                     "optional": "False", "tokens": "None", "size": "2.0", "shape": '"gear"', "loot": '"t4"', "desc": '''[
        "&6Yellow dust, and every acid you will ever need. You remember sulfur as the first gift of volcanoes.&r",
        "&eWhat:&r sulfur dust: the start of sulfur dioxide, sulfur trioxide and sulfuric acid, the gas behind Mekanism's 5x ore line.",
        "&eChemistry:&r the PRC can gasify coal (C + H₂O → CO + H₂, with a little O₂ burning to keep it hot) and leaves the coal's sulfur behind. The Oxidizer then burns S + O₂ → SO₂.",
        "&eHow:&r PRC with coal or coal dust, water and O₂ (check JEI), or crush sulfur from other sources. Every machine before this quest has a job in the acid line.",
        "&eTip:&r more sulfur is the usual bottleneck of a 5x line. Automate a source early."]'''},
    "mk2_cables": {"mirror": '"62827AA1AD29A222"', "section": S_EN,
                   "tasks": '[anyof([MEK + t + "_universal_cable" for t in ("basic", "advanced", "elite", "ultimate")])]',
                   "deps": '["mk2_tablet"]', "title": '"Universal Cable"', "subtitle": '"Energy, Mekanism style"', "desc": '''[
        "&eWhat:&r Universal Cable carries FE between generators, cubes and machines. Any tier counts here.",
        "&eChemistry:&r a cable is a conductor: electrons drift through the metal, and its resistance turns a little of the power into heat (P = I²R).",
        "&eHow:&r steel with redstone, 8 per craft. Higher tiers wrap 8 of the tier below around an alloy (check JEI).",
        "&eTip:&r cables of one type join into one network. Colour them with a Configurator to keep two networks apart."]'''},
    "mk2_transporter": {"mirror": '"60ECCCAB66AAC05D"', "section": S_PIPE,
                        "tasks": '[anyof([MEK + t + "_logistical_transporter" for t in ("basic", "advanced", "elite", "ultimate")])]',
                        "deps": '["mk2_configurator"]'},
    "mk2_security": {"mirror": '"1F8B4F648EB5A0DC"', "section": S_PIPE, "tasks": '[anyof([MEK + "personal_barrel", MEK + "personal_chest"])]',
                     "title": '"Mine, Not Yours"', "subtitle": '"Storage that only opens for you"', "optional": "False", "tokens": "None"},
    "mk2_fluid_tanks": {"mirror": '"7952DA35B4F5C598"', "section": S_PIPE,
                        "tasks": '[anyof([MEK + t + "_fluid_tank" for t in ("basic", "advanced", "elite", "ultimate")])]',
                        "deps": '["mk2_pipes"]', "optional": "False", "tokens": "None"},
    "mk2_bio_fuel": {"mirror": '"081DC030A0546549"', "section": S_MACH, "tasks": '[item(MEK + "bio_fuel")]', "deps": '["mk2_crusher"]',
                     "optional": "False", "tokens": "None"},
    "mk2_lab_tools": {"mirror": '"041365A540BF5A03"', "section": S_GAD, "tasks": '[item(MEK + "dictionary")]', "title": '"Dictionary"',
                      "subtitle": '"Read any item\'s tags"', "deps": '["mk2_chargepad"]'},
    "mk2_chargepad": {"mirror": '"4274E777FB60BA28"', "section": S_EN, "optional": "False", "tokens": "None"},
    "mk2_electric_bow": {"mirror": '"4E7823C2FCEBE4DC"', "section": S_GAD, "deps": '["mk2_chargepad"]', "optional": "False", "tokens": "None"},
    "mk2_flamethrower": {"mirror": '"109310AF19AAC482"', "section": S_GAD, "deps": '["mk2_chargepad", "t4_separator", "t4_mv"]',
                         "optional": "False", "tokens": "None"},
    "mk2_enriched": {"mirror": '"0F326EEEC2EBE4E5"', "section": S_MACH, "deps": '["mk2_enrich"]', "optional": "False", "tokens": "None",
                     "tasks": '[anytag("mekanism:enriched")]'},
    "mk2_pigment": {"mirror": '"07084582F9562740"', "section": S_BIG,
                    "tasks": '[item(MEK + "pigment_extractor"), item(MEK + "pigment_mixer"), item(MEK + "painting_machine")]',
                    "deps": '["mk2_steel_casing", "t4_mv", "t5_hv"]', "optional": "False", "tokens": "None"},
}

MOVE_OUT = ["mk2_robit", "mk2_miner", "mk2_qio", "mk2_qio_io", "mk2_qio_drives", "mk2_module_base", "mk2_mekatool", "mk2_mekasuit_full"]

INSERT = r'''
    # --- ATM10 mirror round (2026-10-20): one quest per ATM10 Mekanism quest we have the items for -------------
    # Osmium and steel
    Q("mk2_osmium", 0, 0, [item(MEK + "ingot_osmium")], "Osmium", subtitle="Mekanism's own metal", deps=["mk2_intro"], xp=30,
      mirror="6F62B5510FA881CD", section="Osmium and Steel", desc=[
        "&eWhat:&r osmium is the metal in almost every Mekanism machine, cable and upgrade.",
        "&eChemistry:&r osmium (Os, element 76) is a platinum-group metal and the densest element known, about 22.6 g/cm³.",
        "&eHow:&r mine osmium ore underground and smelt it, or run it through your ore line for more per ore.",
        "&eTip:&r you will want stacks of it. Put osmium at the top of your ore processing list."]),
    Q("mk2_tips", 0, 0, [tick()], "Reading a Machine", subtitle="Colours, sides and multiblocks", deps=["mk2_intro"], xp=10,
      optional=True, tokens=1, mirror="4A1C8125896F7F1A", section="Osmium and Steel", icon=MEK + "configurator", desc=[
        "&eWhat:&r every Mekanism machine has a side configuration tab. Each colour is a slot or tank, and each side of the block can be set to one of them.",
        "&eHow:&r open a machine and click the side tab on its GUI, or use the Configurator in the world. Multiblock layouts are in &eJust Enough Mekanism Multiblocks&r in JEI.",
        "&eTip:&r auto-eject on the output side saves you a pump or a transporter."]),
    Q("mk2_infuser", 0, 0, [item(MEK + "metallurgic_infuser")], "Metallurgic Infuser", subtitle="Soak a metal, make an alloy", deps=["mk2_osmium"],
      xp=60, size=1.5, shape="hexagon", mirror="162CE44400A63575", section="Osmium and Steel", desc=[
        "&6A furnace that adds rather than burns. Your hands remember this kind of patience.&r",
        "&eWhat:&r the Metallurgic Infuser pushes carbon, redstone, diamond or refined obsidian into a metal. It is how every Mekanism alloy and steel starts.",
        "&eChemistry:&r carburising is real: hot iron soaks up carbon from its surroundings and becomes steel. Mekanism uses the same idea for every alloy.",
        "&eHow:&r iron, osmium, redstone and a furnace (check JEI). Put the infuse material in the left slot and the metal in the middle."]),
    Q("mk2_infused_alloy", 0, 0, [item(MEK + "alloy_infused")], "Infused Alloy", subtitle="Iron and redstone, fused", deps=["mk2_infuser"],
      xp=40, mirror="166971866A9234C7", section="Osmium and Steel", desc=[
        "&eWhat:&r the first Mekanism alloy. It goes into energy tablets, advanced circuits, upgrades and the second tier of everything.",
        "&eHow:&r Metallurgic Infuser: iron ingot + redstone infusion.",
        "&eTip:&r enriched redstone from the Enrichment Chamber gives far more infuse per item."]),
    Q("mk2_basic_circuit", 0, 0, [item(MEK + "basic_control_circuit")], "Basic Control Circuit", subtitle="Mekanism's LV tier",
      deps=["mk2_infuser", "t3_mekcircuit"], xp=40, mirror="0498A578D0EC3254", section="Osmium and Steel", desc=[
        "&eWhat:&r the circuit inside every basic Mekanism machine.",
        "&eHow:&r in this pack it needs an &eMI analog circuit&r (LV) with osmium and Basic Alloy (check JEI). The infuser shortcut is removed.",
        "&eTip:&r make a stack. Almost every quest on this page eats a few."]),
    Q("mk2_steel", 0, 0, [anytag("c:ingots/steel")], "Steel", subtitle="Iron plus carbon", deps=["mk2_infuser"], xp=40,
      mirror="4B35C01F5D0AAC58", section="Osmium and Steel", desc=[
        "&eWhat:&r steel ingots: the frame of every Mekanism casing, cable and tank.",
        "&eChemistry:&r steel is iron with about 0.2-2% carbon. The carbon atoms sit between the iron atoms and stop the layers from sliding, which makes it harder.",
        "&eHow:&r infuse iron with carbon to get enriched iron, infuse that again into steel dust and smelt it. Steel from your MI line works too.",
        "&eTip:&r any steel ingot counts: the pack unifies them."]),
    Q("mk2_steel_casing", 0, 0, [item(MEK + "steel_casing")], "Steel Casing", subtitle="The shell of every machine", deps=["mk2_steel", "t3_mekcircuit"],
      xp=80, size=2.0, shape="gear", loot="t3", mirror="21D8B88155648EA6", section="Machines", desc=[
        "&6A steel shell, ready for a purpose. You remember building with intent.&r",
        "&eWhat:&r the Steel Casing is the body of every Mekanism machine on this page.",
        "&eHow:&r steel ingots, glass and an osmium ingot (check JEI).",
        "&eTip:&r every machine below starts from one casing. Make several at once."]),
    # Circuit tiers
    Q("mk2_tier_basic", 0, 0, [item("minecraft:redstone"), item(MEK + "basic_control_circuit")], "The Basic Tier", subtitle="Redstone and a basic circuit",
      deps=["mk2_basic_circuit", "mk2_infused_alloy"], xp=60, size=1.5, shape="hexagon", mirror="19341B01E048ACAB", section="Circuit Tiers", desc=[
        "&eWhat:&r every Mekanism block comes in four tiers: basic, advanced, elite and ultimate. Each tier pairs an alloy with a control circuit.",
        "&eHow:&r the basic tier runs on redstone and Basic Control Circuits.",
        "&eTip:&r the tier of a factory, cube or tank shows in its name and its colour stripe."]),
    Q("mk2_tier_adv", 0, 0, [item(MEK + "alloy_infused"), item(MEK + "advanced_control_circuit")], "The Advanced Tier", subtitle="Infused alloy, MV circuits",
      deps=["mk2_tier_basic", "t4_mv"], xp=100, size=1.5, shape="hexagon", mirror="7C687DCF71D77761", section="Circuit Tiers", desc=[
        "&eWhat:&r the advanced tier pairs Infused Alloy with the Advanced Control Circuit.",
        "&eHow:&r the circuit needs an &eMI electronic circuit&r (MV) in this pack.",
        "&eTip:&r advanced cables, tanks and factories all use this pair."]),
    Q("mk2_tier_elite", 0, 0, [item(MEK + "alloy_reinforced"), item(MEK + "elite_control_circuit")], "The Elite Tier", subtitle="Reinforced alloy, HV circuits",
      deps=["mk2_tier_adv", "t5_hv"], xp=150, size=1.5, shape="hexagon", mirror="1AEFF93A398B8BBF", section="Circuit Tiers", desc=[
        "&eWhat:&r the elite tier pairs Reinforced Alloy (diamond infusion) with the Elite Control Circuit.",
        "&eHow:&r the circuit needs an &eMI digital circuit&r (HV) in this pack.",
        "&eTip:&r diamond infuse comes from diamonds or diamond dust; enrich it first for more per diamond."]),
    Q("mk2_tier_ult", 0, 0, [item(MEK + "alloy_atomic"), item(MEK + "ultimate_control_circuit")], "The Ultimate Tier", subtitle="Atomic alloy, EV circuits",
      deps=["mk2_tier_elite", "t6_pu"], xp=250, size=1.5, shape="hexagon", loot="t5", mirror="06210B6FD0F9989B", section="Circuit Tiers", desc=[
        "&6The top of the ladder. You remember when four steps felt like a long climb.&r",
        "&eWhat:&r the ultimate tier pairs Atomic Alloy (refined obsidian infusion) with the Ultimate Control Circuit.",
        "&eHow:&r the circuit needs an &eMI processing unit&r (EV) in this pack."]),
    # Machines
    Q("mk2_enrich", 0, 0, [item(MEK + "enrichment_chamber")], "Enrichment Chamber", subtitle="Ore into two dusts", deps=["mk2_steel_casing"], xp=50,
      mirror="08DDE018A804BFE7", section="Machines", desc=[
        "&eWhat:&r the Enrichment Chamber turns one ore into two dusts, and enriches coal, redstone and diamonds for the infuser.",
        "&eHow:&r redstone, a Basic Control Circuit and a steel casing (check JEI).",
        "&eTip:&r 2x is the cap before acids in this pack. The 3x, 4x and 5x lines are below."]),
    Q("mk2_crusher", 0, 0, [item(MEK + "crusher")], "Crusher", subtitle="Ingots and blocks into dust", deps=["mk2_steel_casing"], xp=50,
      mirror="7AE502EDB73BD57A", section="Machines", desc=[
        "&eWhat:&r the Crusher grinds ingots into dust, stone into gravel and plants into bio fuel.",
        "&eHow:&r redstone, a Basic Control Circuit, lava buckets and a steel casing (check JEI).",
        "&eTip:&r it is the last step of the 3x line: clumps go in, dirty dust comes out."]),
    Q("mk2_compressor", 0, 0, [item(MEK + "osmium_compressor")], "Osmium Compressor", subtitle="Dust pressed with liquid osmium", deps=["mk2_adv_circuit"],
      xp=80, mirror="195729280394ABFB", section="Machines", desc=[
        "&eWhat:&r the Osmium Compressor presses a dust together with osmium into a refined ingot: refined obsidian or refined glowstone.",
        "&eHow:&r an Advanced Control Circuit, alloys and a steel casing (check JEI). Osmium ingots go in its fuel slot.",
        "&eTip:&r one osmium ingot feeds many operations."]),
    Q("mk2_purifier", 0, 0, [item(MEK + "purification_chamber")], "Purification Chamber", subtitle="Oxygen for 3x ore", deps=["mk2_adv_circuit", "mk2_enrich"],
      xp=80, mirror="33415CB421F7620A", section="Machines", desc=[
        "&eWhat:&r the Purification Chamber uses oxygen to turn ore into clumps, three per ore.",
        "&eChemistry:&r oxygen attacks the ore's surface and loosens the metal-bearing grains from the rock around them.",
        "&eHow:&r an Advanced Control Circuit (MV), an Enrichment Chamber and osmium (check JEI). Feed it O₂ from an Electrolytic Separator."]),
    Q("mk2_injector", 0, 0, [item(MEK + "chemical_injection_chamber")], "Chemical Injection Chamber", subtitle="Hydrogen chloride for 4x ore",
      deps=["mk2_elite_circuit", "mk2_purifier"], xp=100, mirror="27512B0434531195", section="Machines", desc=[
        "&eWhat:&r the Injection Chamber uses hydrogen chloride to turn ore into shards, four per ore.",
        "&eChemistry:&r HCl dissolves metal oxides into chlorides (for example FeO + 2HCl → FeCl₂ + H₂O), which frees more metal from each ore.",
        "&eHow:&r a Purification Chamber, gold and circuits (check JEI; MV in this pack). Feed it HCl from a Chemical Infuser."]),
    Q("mk2_washer", 0, 0, [item(MEK + "chemical_washer")], "Chemical Washer", subtitle="Rinse the ore slurry", deps=["mk2_ult_circuit"], xp=100,
      mirror="60B52705049D1BA5", section="Machines", desc=[
        "&eWhat:&r the Washer cleans dirty ore slurry into clean slurry with water.",
        "&eChemistry:&r washing removes the insoluble rock and gangue that the acid left behind.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and a bucket (check JEI). Feed it water with an Electric Pump.",
        "&eTip:&r it is part of the 5x line, together with the Dissolution Chamber and Crystallizer."]),
    Q("mk2_dissolution", 0, 0, [item(MEK + "chemical_dissolution_chamber")], "Chemical Dissolution Chamber", subtitle="Sulfuric acid eats the ore",
      deps=["mk2_ult_circuit"], xp=100, mirror="6B8040401B512E50", section="Machines", desc=[
        "&eWhat:&r the Dissolution Chamber dissolves ore in sulfuric acid into a dirty slurry, the first step of the 5x line.",
        "&eChemistry:&r H₂SO₄ turns metal oxides into soluble sulfates, so the metal leaves the rock as a solution.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and chemical tanks (check JEI)."]),
    Q("mk2_crystallizer", 0, 0, [item(MEK + "chemical_crystallizer")], "Chemical Crystallizer", subtitle="Clean slurry back into solids",
      deps=["mk2_ult_circuit"], xp=100, mirror="602A6CF9D5B66AD3", section="Machines", desc=[
        "&eWhat:&r the Crystallizer turns clean slurry into crystals, five per ore, and brine into salt.",
        "&eChemistry:&r crystallisation pulls a pure solid out of a saturated solution: as the solvent goes, the ions arrange into a lattice and leave impurities behind.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and chemical tanks (check JEI)."]),
    Q("mk2_dusts", 0, 0, [anytag("c:dusts")], "A Pile of Dust", subtitle="Anything crushed counts", deps=["mk2_crusher", "mk2_enrich"], xp=20,
      mirror="47F38E606AD3FF53", section="Machines", desc=[
        "&eWhat:&r any dust. Dust is the common middle step: ore and ingots become dust, and dust smelts into ingots.",
        "&eChemistry:&r grinding raises surface area, and reactions happen at surfaces, so powders react and melt faster than lumps.",
        "&eHow:&r put an ingot in the Crusher or an ore in the Enrichment Chamber."]),
    # Chemical machines
    Q("mk2_separator", 0, 0, [item(MEK + "electrolytic_separator")], "Electrolytic Separator", subtitle="Split water into H₂ and O₂",
      deps=["mk2_steel_casing"], xp=60, mirror="18783C62009934DB", section="Chemical Machines", desc=[
        "&eWhat:&r the Separator splits fluids with electricity: water into hydrogen and oxygen, brine into sodium and chlorine.",
        "&eChemistry:&r electrolysis of water: 2H₂O → 2H₂ + O₂. Twice as much hydrogen as oxygen comes out, by volume.",
        "&eHow:&r redstone, iron, osmium and a Basic Control Circuit (check JEI). Pump water in, take each gas out on its own side."]),
    Q("mk2_oxidizer", 0, 0, [item(MEK + "chemical_oxidizer")], "Chemical Oxidizer", subtitle="Solids into gases", deps=["mk2_steel_casing"], xp=60,
      mirror="2A793B35FE25003C", section="Chemical Machines", desc=[
        "&eWhat:&r the Oxidizer burns a solid into a gas: sulfur into sulfur dioxide, and later uranium compounds for fission fuel.",
        "&eChemistry:&r S + O₂ → SO₂. Sulfur burns with a pale blue flame.",
        "&eHow:&r a Dynamic Tank block, a chemical tank and a circuit (check JEI)."]),
    Q("mk2_chem_infuser", 0, 0, [item(MEK + "chemical_infuser")], "Chemical Infuser", subtitle="Two gases in, one out", deps=["mk2_steel_casing"], xp=60,
      mirror="376532CD98D39781", section="Chemical Machines", desc=[
        "&eWhat:&r the Chemical Infuser reacts two gases: H₂ + Cl₂ into HCl, SO₂ + O₂ into SO₃, SO₃ + water vapour into sulfuric acid.",
        "&eChemistry:&r the contact process: 2SO₂ + O₂ → 2SO₃, then SO₃ + H₂O → H₂SO₄. Sulfuric acid is the most produced chemical in the world.",
        "&eHow:&r a Basic Control Circuit, chemical tanks and a steel casing (check JEI)."]),
    Q("mk2_condensentrator", 0, 0, [item(MEK + "rotary_condensentrator")], "Rotary Condensentrator", subtitle="Gas to liquid and back",
      deps=["mk2_steel_casing"], xp=60, mirror="603BEDD49070ECAD", section="Chemical Machines", desc=[
        "&eWhat:&r turns a gas into its liquid form and back. It also boils water into vapour for the acid line.",
        "&eChemistry:&r every gas liquefies when cooled below its boiling point; water vapour is just water above 100 °C.",
        "&eHow:&r glass, a chemical tank, a fluid tank and a circuit (check JEI). Toggle the mode in its GUI."]),
    Q("mk2_hdpe_pellet", 0, 0, [item(MEK + "hdpe_pellet")], "HDPE Pellet", subtitle="Polyethylene from the PRC",
      deps=["mk2_bio_fuel", "mk2_prc", "mk2_condensentrator", "t5_hdpe"], xp=100, mirror="78DD2A3DFF6D1613", section="Chemical Machines", desc=[
        "&eWhat:&r high-density polyethylene pellets, the plastic for sheets, rods and the late Mekanism gear.",
        "&eChemistry:&r n C₂H₄ → (C₂H₄)ₙ: thousands of ethene units join into long, straight chains.",
        "&eHow:&r PRC: substrate + ethene + oxygen → HDPE pellet (check JEI). Your MI polyethylene line from the main path is the other route."]),
    # Upgrades
    Q("mk2_glass", 0, 0, [item(MEK + "structural_glass", 4)], "Structural Glass", subtitle="Windows for multiblocks", deps=["mk2_steel_casing"], xp=30,
      mirror="01A90E2541C91DB2", section="Upgrades", desc=[
        "&eWhat:&r Structural Glass is the wall block of dynamic tanks, evaporation plants, boilers, turbines and the SPS.",
        "&eChemistry:&r glass is mostly SiO₂ cooled too fast to crystallise, so it stays clear.",
        "&eHow:&r glass and steel (check JEI)."]),
    Q("mk2_upg_energy", 0, 0, [item(MEK + "upgrade_energy")], "Energy Upgrade", subtitle="Lower bills, bigger buffer", deps=["mk2_steel_casing", "mk2_glass"],
      xp=40, mirror="0ACE573560A19309", section="Upgrades", desc=[
        "&eWhat:&r cuts a machine's energy use and enlarges its internal buffer.",
        "&eHow:&r Infused Alloy and glass around gold dust (check JEI). Up to 8 per machine.",
        "&eTip:&r pair every speed upgrade with an energy upgrade."]),
    Q("mk2_upg_muffling", 0, 0, [item(MEK + "upgrade_muffling")], "Muffling Upgrade", subtitle="Quiet machines", deps=["mk2_steel_casing", "mk2_glass"],
      xp=30, mirror="001DE8028CAF0A08", section="Upgrades", desc=[
        "&eWhat:&r makes a machine quieter. Four make it silent.",
        "&eHow:&r Infused Alloy and glass around wool (check JEI).",
        "&eTip:&r your ears will thank you in a room of 20 crushers."]),
    Q("mk2_upg_chemical", 0, 0, [item(MEK + "upgrade_chemical")], "Chemical Upgrade", subtitle="Use less gas per job", deps=["mk2_steel_casing", "mk2_glass"],
      xp=40, mirror="09830BB2A23E94B4", section="Upgrades", desc=[
        "&eWhat:&r cuts the gas a machine uses per operation, in machines that take a secondary gas (purification, injection).",
        "&eHow:&r Infused Alloy and glass around a gas ingredient (check JEI).",
        "&eTip:&r on an injection line it saves a lot of HCl."]),
    Q("mk2_upg_stone", 0, 0, [item(MEK + "upgrade_stone_generator")], "Stone Generator Upgrade", subtitle="Cobble on demand",
      deps=["mk2_steel_casing", "mk2_glass"], xp=30, mirror="515A60B89ED5440D", section="Upgrades", desc=[
        "&eWhat:&r lets an Electric Pump make stone from the water and lava next to it.",
        "&eChemistry:&r lava is molten rock; water cools its surface below the melting point and it sets as stone.",
        "&eHow:&r Infused Alloy and glass around water and lava (check JEI)."]),
    Q("mk2_upg_anchor", 0, 0, [item(MEK + "upgrade_anchor")], "Anchor Upgrade", subtitle="Keep one machine's chunk loaded", deps=["mk2_upgrades"], xp=40,
      optional=True, tokens=1, section="Upgrades", desc=[
        "&eWhat:&r a machine with an Anchor upgrade keeps its own chunk loaded.",
        "&eHow:&r Infused Alloy and glass around diamond dust (check JEI).",
        "&eTip:&r cheaper than a Dimensional Stabilizer for one remote machine."]),
    # Pipes and storage
    Q("mk2_pipes", 0, 0, [anyof([MEK + t + "_mechanical_pipe" for t in ("basic", "advanced", "elite", "ultimate")])], "Mechanical Pipes",
      subtitle="Fluids, Mekanism style", deps=["mk2_configurator"], xp=40, mirror="33C69B5934BE4D64", section="Pipes and Storage", desc=[
        "&eWhat:&r Mechanical Pipes carry fluids. Any tier counts.",
        "&eHow:&r steel and a bucket, 8 per craft (check JEI).",
        "&eTip:&r pipes pull only from blocks that push; set the source's side to output."]),
    Q("mk2_tubes", 0, 0, [anyof([MEK + t + "_pressurized_tube" for t in ("basic", "advanced", "elite", "ultimate")])], "Pressurized Tubes",
      subtitle="Gases need their own pipe", deps=["mk2_configurator"], xp=40, mirror="3AF1DC02E9A0010C", section="Pipes and Storage", desc=[
        "&eWhat:&r Pressurized Tubes carry Mekanism chemicals: gases, slurries and infuse types.",
        "&eChemistry:&r gases spread to fill any space, so a gas line must be sealed. Pressure drives the flow from the full end to the empty end.",
        "&eHow:&r steel and glass, 8 per craft (check JEI)."]),
    Q("mk2_conductors", 0, 0, [anyof([MEK + t + "_thermodynamic_conductor" for t in ("basic", "advanced", "elite", "ultimate")])], "Thermodynamic Conductors",
      subtitle="Pipes for heat", deps=["mk2_configurator"], xp=40, mirror="66A450CAC07232E1", section="Pipes and Storage", desc=[
        "&eWhat:&r conductors carry heat between heaters, the evaporation plant and the boiler.",
        "&eChemistry:&r heat flows from hot to cold. Copper conducts heat about eight times better than steel.",
        "&eHow:&r steel and copper (check JEI)."]),
    Q("mk2_chem_tanks", 0, 0, [anyof([MEK + t + "_chemical_tank" for t in ("basic", "advanced", "elite", "ultimate")])], "Chemical Tanks",
      subtitle="A bottle for any gas", deps=["mk2_tubes"], xp=50, mirror="1922623A26E08078", section="Pipes and Storage", desc=[
        "&eWhat:&r Chemical Tanks store gases and keep them when broken. Any tier counts.",
        "&eHow:&r osmium and redstone (check JEI). Higher tiers ring the tank below with alloy.",
        "&eTip:&r one under each separator output keeps the line steady."]),
    Q("mk2_bins", 0, 0, [anyof([MEK + t + "_bin" for t in ("basic", "advanced", "elite", "ultimate")])], "Bins", subtitle="Lots of one item",
      deps=["mk2_transporter"], xp=40, mirror="73E6878553BA6908", section="Pipes and Storage", desc=[
        "&eWhat:&r a Bin holds a large amount of one item type and keeps it when broken.",
        "&eHow:&r a chest, Basic Alloy and a circuit (check JEI). Left-click to take a stack, right-click to put one in.",
        "&eTip:&r good for cobblestone, dusts or anything you hoard by the thousand."]),
    Q("mk2_fuelwood", 0, 0, [item(MEK + "fuelwood_heater")], "Fuelwood Heater", subtitle="Burn fuel for heat", deps=["mk2_conductors"], xp=40,
      mirror="2D1CBCEC82F1B37D", section="Pipes and Storage", desc=[
        "&eWhat:&r burns any furnace fuel and gives heat to the conductors around it.",
        "&eChemistry:&r burning is fast oxidation: C + O₂ → CO₂ releases about 394 kJ per mole of carbon.",
        "&eHow:&r a steel casing, a furnace and a circuit (check JEI)."]),
    Q("mk2_security_desk", 0, 0, [item(MEK + "security_desk")], "Security Desk", subtitle="Who may use your machines", deps=["mk2_security", "mk2_elite_circuit"],
      xp=60, optional=True, tokens=1, section="Pipes and Storage", desc=[
        "&eWhat:&r sets who may use your Mekanism blocks: you, a trusted list, or everyone.",
        "&eHow:&r steel, glass and &eElite Control Circuits&r (HV) (check JEI).",
        "&eTip:&r on a shared server, lock your reactor controls."]),
    # Big builds
    Q("mk2_evaporation", 0, 0, [item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"), item(MEK + "thermal_evaporation_valve")],
      "Thermal Evaporation Plant", subtitle="Sun and heat turn water into brine", deps=["mk2_steel_casing"], xp=120, mirror="120572510F525930", section="Big Builds", desc=[
        "&eWhat:&r a tall multiblock that boils water down into brine, and brine into lithium.",
        "&eChemistry:&r salt pans work the same way: water evaporates and the dissolved salts stay behind at higher and higher concentration.",
        "&eHow:&r a 4x4 base of evaporation blocks, up to 18 high, with a controller and valves (layout in JEI). Heat makes it faster."]),
    # Energy
    Q("mk2_solar", 0, 0, [item(GEN + "solar_generator")], "Solar Generator", subtitle="Free power by day", deps=["mk2_tablet"], xp=40,
      mirror="74200A48498DD7F8", section="Energy", desc=[
        "&eWhat:&r a small generator that makes FE in daylight under open sky.",
        "&eChemistry:&r a photovoltaic cell is a silicon junction: light knocks electrons loose and the junction pushes them one way, making a current.",
        "&eHow:&r solar panels, an Energy Tablet and osmium (check JEI)."]),
    Q("mk2_adv_solar", 0, 0, [item(GEN + "advanced_solar_generator")], "Advanced Solar Generator", subtitle="Four panels, one block",
      deps=["mk2_solar"], xp=60, mirror="4EDD96EB60EF5814", section="Energy", desc=[
        "&eWhat:&r four solar generators on a frame, with much more output.",
        "&eHow:&r solar generators, Infused Alloy and iron (check JEI).",
        "&eTip:&r it works in the rain too, just slower."]),
    Q("mk2_heat_gen", 0, 0, [item(GEN + "heat_generator")], "Heat Generator", subtitle="Lava and fuel into power", deps=["mk2_tablet"], xp=40,
      mirror="0650996C7818ADB5", section="Energy", desc=[
        "&eWhat:&r burns fuel or sits by lava and turns heat into FE.",
        "&eChemistry:&r a heat engine needs a hot side and a cold side; the bigger the difference, the more work it can do.",
        "&eHow:&r iron, wood, copper and a furnace (check JEI)."]),
    Q("mk2_bio_gen", 0, 0, [item(GEN + "bio_generator")], "Bio-Generator", subtitle="Burn bio fuel", deps=["mk2_tablet"], xp=40,
      mirror="6CD1720B76F47806", section="Energy", desc=[
        "&eWhat:&r burns bio fuel (crushed plants) for FE.",
        "&eChemistry:&r plants store sunlight as sugars: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Burning them gives that energy back.",
        "&eHow:&r redstone, bio fuel and an Energy Tablet (check JEI)."]),
    Q("mk2_wind", 0, 0, [item(GEN + "wind_generator")], "Wind Generator", subtitle="Higher is windier", deps=["mk2_tablet"], xp=50,
      mirror="7778937DF377C1B4", section="Energy", desc=[
        "&eWhat:&r a turbine that makes more FE the higher you build it.",
        "&eChemistry:&r a turbine's power grows with the cube of wind speed, so a little more wind gives a lot more power.",
        "&eHow:&r an Energy Tablet, osmium and circuits (check JEI). Put it on a tall tower."]),
    Q("mk2_cubes", 0, 0, [anyof([MEK + t + "_energy_cube" for t in ("basic", "advanced", "elite", "ultimate")])], "Energy Cube",
      subtitle="Store the surplus", deps=["mk2_tablet"], xp=50, mirror="0AA9EF3981E9BA37", section="Energy", desc=[
        "&eWhat:&r a block battery that stores FE and keeps it when broken. Any tier counts.",
        "&eHow:&r redstone, iron, Energy Tablets and a steel casing (check JEI).",
        "&eTip:&r set its sides in the GUI: one input, the rest output."]),
    # Gadgets
    Q("mk2_jetpack", 0, 0, [item(MEK + "jetpack")], "Jetpack", subtitle="Hydrogen-powered hops", deps=["mk2_chargepad"], xp=60,
      mirror="37D4E5ACB35D8BF1", section="Gadgets", desc=[
        "&eWhat:&r a chest-slot jetpack that burns hydrogen.",
        "&eChemistry:&r hydrogen burns with oxygen into water: 2H₂ + O₂ → 2H₂O, with a lot of energy per gram.",
        "&eHow:&r steel, a basic chemical tank and circuits (check JEI). Fill it with H₂ from a separator.",
        "&eTip:&r hover mode is the safe one for building."]),
    Q("mk2_gauge_dropper", 0, 0, [item(MEK + "gauge_dropper")], "Gauge Dropper", subtitle="Sample or empty a tank", deps=["mk2_chargepad"], xp=20,
      mirror="424B3E3B299D3999", section="Gadgets", desc=[
        "&eWhat:&r sucks a little fluid or gas out of a tank, or dumps a tank you don't want.",
        "&eHow:&r osmium over glass panes (check JEI).",
        "&eTip:&r sneak + right-click empties the dropper itself."]),
    Q("mk2_free_runners", 0, 0, [item(MEK + "free_runners")], "Free Runners", subtitle="No fall damage, taller steps", deps=["mk2_chargepad"], xp=50,
      mirror="227E9783382527CA", section="Gadgets", desc=[
        "&eWhat:&r powered boots that stop fall damage and let you walk up full blocks.",
        "&eHow:&r string, Infused Alloy and an Energy Tablet (check JEI). Charge them on the Chargepad."]),
    Q("mk2_scuba", 0, 0, [item(MEK + "scuba_tank"), item(MEK + "scuba_mask")], "Scuba Gear", subtitle="Breathe from a tank", deps=["mk2_chargepad"], xp=50,
      mirror="47E79DFD123BF617", section="Gadgets", desc=[
        "&eWhat:&r a tank of oxygen on your back and a mask on your face: breathe underwater for a long time.",
        "&eChemistry:&r we need O₂ for respiration; a scuba tank just carries it with you.",
        "&eHow:&r tank: a basic chemical tank and alloy; mask: glass and alloy (check JEI). Fill the tank with O₂ from a separator."]),
    # Ore line: 2x, 3x, 4x, 5x (each machine counts as its factory too)
    Q("mk2_ore2", 0, 0, [fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "2x: Enrich and Smelt",
      subtitle="Two ingots per ore", deps=["mk2_steel_casing"], xp=60, mirror="119BED334E331C25", section="Ore Line: 2x", desc=[
        "&eWhat:&r the first ore line: ore into the Enrichment Chamber (2 dusts), dusts into the smelter.",
        "&eHow:&r an Enrichment Chamber and an Energized Smelter, or any factory of either. Join them with a transporter.",
        "&eTip:&r this is the pack's cap before acids. Every step up needs a gas."]),
    Q("mk2_ore3", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), fac("purification_chamber", "purifying")], "3x: Oxygen",
      subtitle="Water, split, feeds the purifier", deps=["mk2_steel_casing", "t4_ore3"], xp=80, mirror="445CC9AAA6F8AAB6", section="Ore Line: 3x", desc=[
        "&eWhat:&r the 3x line starts with oxygen: pump water, split it, and feed the O₂ into a Purification Chamber.",
        "&eChemistry:&r 2H₂O → 2H₂ + O₂. Keep the hydrogen: it's fuel and a reagent later.",
        "&eHow:&r an Electric Pump, an Electrolytic Separator and a Purification Chamber or Purifying Factory."]),
    Q("mk2_ore3b", 0, 0, [fac("crusher", "crushing"), fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "3x: The Rest of the Line",
      subtitle="Clumps to dust to ingots", deps=["mk2_ore3"], xp=80, mirror="67E7A9A65B14C933", section="Ore Line: 3x", desc=[
        "&eWhat:&r clumps go through the Crusher into dirty dust, the Enrichment Chamber cleans it, and the smelter finishes the ingots.",
        "&eHow:&r a Crusher, an Enrichment Chamber and an Energized Smelter (or their factories), all on one transporter line.",
        "&eTip:&r dirty dust can go to the MI Centrifuge instead for byproducts."]),
    Q("mk2_ore4", 0, 0, [item(MEK + "electric_pump"), item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"),
                         item(MEK + "thermal_evaporation_valve", 2), item(MEK + "electrolytic_separator")], "4x: Brine and Chlorine",
      subtitle="Sea salt becomes a reagent", deps=["mk2_steel_casing", "t4_ore4"], xp=120, mirror="7485BCBE366501DF", section="Ore Line: 4x", desc=[
        "&eWhat:&r the 4x line needs chlorine: an evaporation plant makes brine, and a separator splits it.",
        "&eChemistry:&r electrolysis of brine (the chlor-alkali process): 2NaCl + 2H₂O → Cl₂ + H₂ + 2NaOH. Mekanism gives you Cl₂ and sodium.",
        "&eHow:&r a pump into the evaporation plant, its brine into a separator. Keep the chlorine."]),
    Q("mk2_ore4b", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), item(MEK + "chemical_infuser"), item(MEK + "chemical_injection_chamber")],
      "4x: Hydrogen Chloride", subtitle="H₂ + Cl₂ → 2HCl", deps=["mk2_ore4"], xp=120, mirror="0E175356D43E6A10", section="Ore Line: 4x", desc=[
        "&eWhat:&r hydrogen from a water separator and chlorine from the brine separator meet in the Chemical Infuser to make HCl for the Injection Chamber.",
        "&eChemistry:&r H₂ + Cl₂ → 2HCl. In daylight the mix can react explosively; Mekanism keeps it tame.",
        "&eHow:&r a second pump and separator for H₂, a Chemical Infuser, and the Injection Chamber."]),
    Q("mk2_ore4c", 0, 0, [fac("purification_chamber", "purifying"), fac("crusher", "crushing"), fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")],
      "4x: Shards to Ingots", subtitle="Finish with the 3x line", deps=["mk2_ore4b"], xp=120, mirror="0095422BC87AA135", section="Ore Line: 4x", desc=[
        "&eWhat:&r shards go into the Purification Chamber and then down the 3x line: crush, enrich, smelt.",
        "&eHow:&r one of each machine (or its factory) on a transporter line.",
        "&eTip:&r one factory of each type keeps up with a basic injection chamber."]),
    Q("mk2_ore5", 0, 0, [item(MEK + "dust_sulfur"), item(MEK + "chemical_oxidizer"), item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"),
                         item(MEK + "chemical_infuser"), item(MEK + "rotary_condensentrator")], "5x: Sulfuric Acid",
      subtitle="The contact process", deps=["mk2_steel_casing", "t4_ore5"], xp=150, mirror="75E4751F7A802A44", section="Ore Line: 5x", desc=[
        "&eWhat:&r the 5x line runs on sulfuric acid: burn sulfur, oxidise it again, then add water vapour.",
        "&eChemistry:&r S + O₂ → SO₂; 2SO₂ + O₂ → 2SO₃; SO₃ + H₂O → H₂SO₄.",
        "&eHow:&r Oxidizer (sulfur → SO₂), separator (O₂), Chemical Infuser (SO₃, then acid) and a Rotary Condensentrator for water vapour."]),
    Q("mk2_ore5b", 0, 0, [item(MEK + "chemical_infuser"), item(MEK + "chemical_dissolution_chamber"), item(MEK + "chemical_washer"), item(MEK + "chemical_crystallizer")],
      "5x: Dissolve, Wash, Crystallise", subtitle="Ore into slurry and back", deps=["mk2_ore5"], xp=150, mirror="77FB313845779AED", section="Ore Line: 5x", desc=[
        "&eWhat:&r the acid dissolves ore into dirty slurry, the washer cleans it, and the crystallizer turns it into crystals.",
        "&eChemistry:&r leach, purify, crystallise: the same three steps real hydrometallurgy uses for copper, zinc and uranium.",
        "&eHow:&r one of each machine, joined by pressurized tubes. The washer needs water."]),
    Q("mk2_ore5c", 0, 0, [item(MEK + "electric_pump", 2), item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"),
                          item(MEK + "thermal_evaporation_valve", 2), item(MEK + "electrolytic_separator", 2), item(MEK + "chemical_infuser"),
                          item(MEK + "chemical_injection_chamber")], "5x: The HCl Stage", subtitle="Crystals into shards",
      deps=["mk2_ore5b"], xp=150, mirror="6DC1E08D019FD543", section="Ore Line: 5x", desc=[
        "&eWhat:&r crystals go into the Injection Chamber, so the 5x line needs the whole HCl setup from the 4x line as well.",
        "&eHow:&r two pumps, the evaporation plant, two separators, a Chemical Infuser and an Injection Chamber.",
        "&eTip:&r if you built the 4x line, reuse it: just send the crystals in front of it."]),
    Q("mk2_ore5d", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), fac("purification_chamber", "purifying"), fac("crusher", "crushing"),
                          fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "5x: The Full Line",
      subtitle="Five ingots per ore", deps=["mk2_ore5c"], xp=200, mirror="7934873E784C4B3C", section="Ore Line: 5x", desc=[
        "&6Five from one. You remember when the world gave freely; now you make it give.&r",
        "&eWhat:&r the last stage is the 3x line again: oxygen, purifier, crusher, enrichment, smelter.",
        "&eHow:&r a pump and separator for O₂, then one of each machine (or factory).",
        "&eTip:&r dirty dust can also go to the MI Centrifuge for byproducts."]),
'''
