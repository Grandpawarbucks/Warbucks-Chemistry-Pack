GOO, MAT, COAL, M1, M2, TOOL, ARM, GAD, FLU, TIME, TUP, AUP = (
    '"The Goo"', '"Materials"', '"Coal and Fuel"', '"Simple Machines"', '"Advanced Machines"', '"Tools"', '"Armour"', '"Gadgets"',
    '"Fluids"', '"Time"', '"Tool Upgrades"', '"Armour Upgrades"')
F, B, C, E = "jdt_ferricore", "jdt_blazegold_raw", "jdt_celestigem_gem", "jdt_eclipse_ingot"
REQ = {"optional": "False", "tokens": "None"}


def t(*ids):
    return "[" + ", ".join(f'item(J + "{i}")' for i in ids) + "]"


def e(m, s, deps=None, **kw):
    d = {"mirror": f'"{m}"', "section": s}
    if deps is not None:
        d["deps"] = repr(list(deps))
    d.update(kw)
    return d


EDIT = {
    "jdt_goo": e("05D8C6EF8FCD6250", GOO, ["jdt_start"], size="1.5", shape='"hexagon"'),
    "jdt_ferricore": e("5BD5737703F3F077", MAT, ["jdt_goo"], tasks=t("raw_ferricore", "ferricore_ingot")),
    "jdt_blazegold": e("4C54BD57CAB8A54B", GOO, ["jdt_goo", "t2_nether"], tasks=t("gooblock_tier2"), size="1.5", shape='"hexagon"'),
    "jdt_celestigem": e("5C6709350BEF4050", GOO, ["jdt_blazegold", "w_dragon"], tasks=t("gooblock_tier3"), size="1.5", shape='"hexagon"'),
    "jdt_eclipse": e("25213DBA6E6CEDD2", GOO, ["jdt_celestigem", "w_ancient"], tasks=t("gooblock_tier4")),
    "jdt_coal_t1": e("4B3F20E5C7E3BCFB", COAL, ["jdt_goo"], tasks=t("coal_t1")),
    "jdt_coal_t2": e("079A415488A32076", COAL, ["jdt_blazegold", "jdt_coal_t1"], tasks=t("coal_t2")),
    "jdt_coal_t3": e("446A37C7FCDACF84", COAL, ["jdt_celestigem", "jdt_coal_t2"], tasks=t("coal_t3"), **REQ),
    "jdt_coal_t4": e("09D2137B4F42006E", COAL, ["jdt_eclipse", "jdt_coal_t3"], tasks=t("coal_t4"), **REQ),
    "jdt_generator": e("70AD088336748892", M1, ["jdt_t1_tip", F]),
    "jdt_fluid_gen": e("4A5937F6E5D06BE1", M1, ["jdt_t1_tip", F]),
    "jdt_fuel_canister": e("242F74010488F261", GAD, ["jdt_util_tip", F], **REQ),
    "jdt_polymorphic": e("4458F8829800A950", FLU, ["jdt_fluid_tip"], tasks=t("polymorphic_fluid_bucket")),
    "jdt_fuel_t2": e("3D9964CB0440DD5A", FLU, ["jdt_polymorphic", "jdt_coal_t2"]),
    "jdt_fuel_high": e("70BF85E2D235BAD5", FLU, ["jdt_fuel_t2", "jdt_coal_t3"], tasks=t("refined_t3_fluid_bucket"), title='"Voidflame Fuel"', **REQ),
    "jdt_transmitter": e("6F709652A2B88C78", M2, [B, "jdt_t2_tip"], tasks=t("energytransmitter"), **REQ),
    "jdt_time_crystal": e("6ADE6F9E004055F7", TIME, ["jdt_eclipse"], tasks=t("time_crystal"), **REQ),
    "jdt_time_wand": e("76B1C5AFC5D6B7CF", GAD, ["jdt_util_tip", "jdt_time_crystal", B, F, "jdt_time_fluid"], tasks=t("time_wand"), **REQ),
    "jdt_paradox": e("41E8C93A44559E48", M2, ["jdt_time_crystal", E, "jdt_time_fluid", "jdt_t2_tip"], **REQ),
    "jdt_tools_t1": e("5BBE8B30ED7518B8", TOOL, ["jdt_tools_tip", F], tasks=t("ferricore_pickaxe"), title='"Ferricore Pickaxe"'),
    "jdt_tools_t2": e("199388A311FAC14C", TOOL, ["jdt_tools_tip", B], tasks=t("blazegold_pickaxe"), title='"Blazegold Pickaxe"'),
    "jdt_tools_t3": e("6FD4C60B547F4131", TOOL, ["jdt_tools_tip", C], tasks=t("celestigem_pickaxe"), title='"Celestigem Pickaxe"'),
    "jdt_tools_t4": e("6A4D31194C4CE156", TOOL, ["jdt_tools_tip", E], **REQ),
    "jdt_bows": e("5A9436B100FC1E67", TOOL, ["jdt_tools_tip", F], tasks=t("bow_ferricore"), title='"Ferricore Bow"', **REQ),
    "jdt_bow_set": e("71128E508D810DDF", TOOL, ["jdt_tools_tip", E], tasks=t("bow_eclipsealloy"), title='"Eclipse Alloy Bow"', **REQ),
    "jdt_ferricore_kit": e("2F86FB9E4D49E4B0", TOOL, ["jdt_tools_tip", F], tasks=t("ferricore_sword"), title='"Ferricore Sword"', **REQ),
    "jdt_blazegold_kit": e("46E6B1600AA8A61E", TOOL, ["jdt_tools_tip", B], tasks=t("blazegold_sword"), title='"Blazegold Sword"', **REQ),
    "jdt_celestigem_kit": e("4E03AE15BEF86178", TOOL, ["jdt_tools_tip", C], tasks=t("celestigem_sword"), title='"Celestigem Sword"', **REQ),
    "jdt_eclipse_kit": e("37B903620493A354", TOOL, ["jdt_tools_tip", E], tasks=t("eclipsealloy_sword"), title='"Eclipse Alloy Sword"', **REQ),
    "jdt_armor": e("24BA4B4EED0A9DBD", ARM, ["jdt_armor_tip", F], tasks=t("ferricore_helmet"), title='"Ferricore Helmet"', **REQ),
    "jdt_blazegold_armor": e("03ED9B0DFE8B4574", ARM, ["jdt_armor_tip", B], tasks=t("blazegold_helmet"), title='"Blazegold Helmet"', **REQ),
    "jdt_celestigem_armor": e("71441DFA05FD73E5", ARM, ["jdt_armor_tip", C], tasks=t("celestigem_helmet"), title='"Celestigem Helmet"', **REQ),
    "jdt_eclipse_armor": e("0A02DBE226C3F44E", ARM, ["jdt_armor_tip", E], tasks=t("eclipsealloy_helmet"), title='"Eclipse Alloy Helmet"', **REQ),
    "jdt_blank": e("7305EE0F7D73C231", TUP, ["jdt_tools_tip", "jdt_armor_tip", F], tasks=t("upgrade_blank"), size="1.5", shape='"hexagon"'),
    "jdt_oreminer": e("2A01CE9206DD4F8A", TUP, ["jdt_tool_tag"]),
    "jdt_upgrades": e("6690AEE064DC2A7C", TUP, ["jdt_tool_tag"], tasks=t("upgrade_hammer"), title='"Hammer"', subtitle='"Mine a square, not a block"', **REQ),
    "jdt_sense_abilities": e("17C4F6EC1AFBC3AA", TUP, ["jdt_tool_tag"], tasks=t("upgrade_mobscanner"), title='"Mob Scanner"', **REQ),
    "jdt_combat_abilities": e("2875FACD3BFB0A8E", TUP, ["jdt_tool_tag"], tasks=t("upgrade_cauterizewounds"), title='"Cauterize Wounds"', **REQ),
    "jdt_arrow_abilities": e("05056CAA64E3971B", TUP, ["jdt_tool_tag"], tasks=t("upgrade_potionarrow"), title='"Potion Arrow"', **REQ),
    "jdt_smoker": e("61213012615619C5", TUP, ["jdt_tool_tag"], **REQ),
    "jdt_instabreak": e("45D683D7F1A32B04", TUP, ["jdt_tool_tag"], **REQ),
    "jdt_move_abilities": e("3B3E3D81843BB358", AUP, ["jdt_armor_tag"], tasks=t("upgrade_runspeed"), title='"Run Speed"', **REQ),
    "jdt_elytra": e("3A471716A29F5172", AUP, ["jdt_armor_tag"], tasks=t("upgrade_elytra"), title='"Elytra Upgrade"', **REQ),
    "jdt_flight": e("515C0527226BA50C", AUP, ["jdt_armor_tag", "jdt_eclipse"], tasks=t("upgrade_flight"), size="1.0", shape="None"),
    "jdt_chest_more": e("0C2EC56133D3CC6C", AUP, ["jdt_armor_tag"], tasks=t("upgrade_invulnerability"), title='"Invulnerability"', **REQ),
    "jdt_ferricore_ingot": e("49636B3C6E6D0C2A", AUP, ["jdt_armor_tag", F], tasks=t("template_ferricore"), title='"Ferricore Template"'),
    "jdt_breaker": e("7D1D2A4E07E98709", M1, ["jdt_t1_tip", F], tasks=t("blockbreakert1"), title='"Simple Block Breaker"'),
    "jdt_clicker": e("6737CB17D562B134", M1, ["jdt_t1_tip", F], tasks=t("clickert1"), title='"Simple Clicker"'),
    "jdt_fluid_machines": e("1B173E7533E1171F", M1, ["jdt_t1_tip", F], tasks=t("fluidcollectort1"), title='"Simple Fluid Collector"', **REQ),
    "jdt_swapper": e("0B9BBE2A764631BF", M1, ["jdt_t1_tip", B], **REQ),
    "jdt_item_collector": e("3C8C80345D3F5FE8", M2, [F, "jdt_t2_tip"], tasks=t("itemcollector"), title='"Item Collector"', **REQ),
    "jdt_machines_t2": e("16772C399861783D", M2, ["jdt_t2_tip", C], tasks=t("blockbreakert2"), title='"Advanced Block Breaker"', **REQ),
    "jdt_workshop": e("4C40699E0A9A5BE6", M2, ["jdt_t2_tip", E], tasks=t("blockswappert2"), title='"Advanced Swapper"',
                      subtitle='"Swap blocks at a distance"', **REQ),
    "jdt_player_accessor": e("02B0CCD5607FF3B5", M2, [B, "jdt_t2_tip"], **REQ),
    "jdt_blazejet": e("5D4E51471F3939E0", TOOL, [B, "jdt_tools_tip"], **REQ),
    "jdt_voidshift": e("5B910F1389C0B915", TOOL, [C, "jdt_tools_tip"], **REQ),
    "jdt_eclipsegate": e("5B02719C13B1FFE2", TOOL, [E, "jdt_tools_tip"], **REQ),
    "jdt_catcher": e("53F9E5CE7EE6F852", GAD, ["jdt_util_tip", B], tasks=t("creaturecatcher"), title='"Creature Catcher"', **REQ),
    "jdt_portal_v2": e("4F9932477EDDCB8E", GAD, ["jdt_util_tip", C], tasks=t("portalgun_v2"), title='"Advanced Portal Gun"', **REQ),
    "jdt_canisters": e("200ECDC70E97D254", GAD, ["jdt_util_tip", F], tasks=t("fluid_canister"), title='"Fluid Canister"', **REQ),
}


def q(key, mirror, section, ids, title, sub, deps, lines, xp=40, extra=""):
    tasks = ids if ids.startswith("[") else t(*ids.split())
    body = ",\n        ".join('"' + l.replace('"', "'") + '"' for l in lines)
    return (f'    Q("{key}", 0, 0, {tasks}, "{title}", subtitle="{sub}", deps={deps!r}, xp={xp}, mirror="{mirror}", section={section}{extra}, desc=[\n'
            f'        {body}]),\n')


NEW = [
    q("jdt_start", "7F0B2D58361FB00E", GOO, "[tick()]", "The Living Goo", "Blocks that change the blocks around them", ["gs_iron"], [
        "&6Matter that rewrites matter. You remember being able to do this with a thought.&r",
        "&eWhat:&r Just Dire Things is built on goo: four tiers of living blocks that slowly convert what touches them into new materials.",
        "&eHow:&r every conversion is in JEI under Goo Spreading. Each tier of goo opens a new metal, a new coal and a new tier of tools.",
        "&eTip:&r click to begin."], xp=10, extra=f', icon=J + "gooblock_tier1"'),
    q("jdt_blazegold_raw", "2D86D4403E0F4EB9", MAT, "raw_blazegold blazegold_ingot", "Blazegold", "Gold, changed by the goo", ["jdt_blazegold"], [
        "&eWhat:&r tier 2 goo turns gold blocks into raw blazegold ore. Smelt it into blazegold ingots.",
        "&eChemistry:&r gold barely reacts with anything; it's the goo, not chemistry, that changes it.",
        "&eHow:&r gold blocks against Blazebloom goo; mine the result."]),
    q("jdt_celestigem_gem", "60A4994078500F63", MAT, "celestigem", "Celestigem", "A gem from tier 3 goo", ["jdt_celestigem"], [
        "&eWhat:&r tier 3 goo grows celestigem: the material for the third tier of tools, armour and machines.",
        "&eHow:&r check JEI's Goo Spreading tab for what tier 3 goo converts."]),
    q("jdt_eclipse_ingot", "1705175C20CE91DD", MAT, "raw_eclipsealloy eclipsealloy_ingot", "Eclipse Alloy", "The top goo metal", ["jdt_eclipse"], [
        "&eWhat:&r tier 4 goo makes raw eclipse alloy; smelt it into ingots for the best tools, armour and flight.",
        "&eHow:&r check JEI's Goo Spreading tab for tier 4 (it needs a netherite block)."]),
    q("jdt_t1_tip", "517F0135926B15EE", M1, "[tick()]", "Simple Machines", "Small automation, ferricore tier", ["jdt_ferricore"], [
        "&eWhat:&r Just Dire Things machines are small blocks that each do one job: break, place, click, sense, drop, collect.",
        "&eHow:&r each Simple machine is ferricore with a few vanilla parts (check JEI). They run on redstone or on their own timers.",
        "&eTip:&r a breaker facing a goo block harvests the conversion for you."], xp=10, extra=f', icon=J + "blockbreakert1"'),
    q("jdt_placer", "70C404E5685E4E91", M1, "blockplacert1", "Simple Block Placer", "Puts a block back", ["jdt_t1_tip", F], [
        "&eWhat:&r places the blocks in its inventory in front of it.",
        "&eHow:&r ferricore and a dispenser (check JEI).", "&eTip:&r pair it with a breaker to feed goo automatically."]),
    q("jdt_sensor", "19E678E6EF9539DC", M1, "sensort1", "Simple Sensor", "Redstone when something is there", ["jdt_t1_tip", F], [
        "&eWhat:&r gives a redstone signal when it sees a chosen block or entity in front of it.",
        "&eHow:&r ferricore and an observer (check JEI).", "&eTip:&r it can tell a breaker when a goo conversion has finished."]),
    q("jdt_dropper", "1ECFA72CF2BA4B45", M1, "droppert1", "Simple Dropper", "Drops items on a timer", ["jdt_t1_tip", F], [
        "&eWhat:&r drops items from its inventory in front of it.", "&eHow:&r ferricore and a dropper (check JEI)."]),
    q("jdt_fluid_placer", "433117EEA55B6A54", M1, "fluidplacert1", "Simple Fluid Placer", "Puts a fluid block down", ["jdt_t1_tip", F], [
        "&eWhat:&r places a source block of the fluid inside it.", "&eHow:&r ferricore and a bucket (check JEI).",
        "&eTip:&r useful for polymorphic fluid crafting."]),
    q("jdt_t2_tip", "5F5120451BA5B2FE", M2, "[tick()]", "Advanced Machines", "Celestigem-tier automation", ["jdt_blazegold"], [
        "&eWhat:&r Advanced machines do the same jobs with more range, filters and settings.",
        "&eHow:&r the Simple machine in the centre, ringed with celestigem and more (check JEI)."], xp=10, extra=f', icon=J + "blockbreakert2"'),
]
for key, aid, iid, title, what in [
    ("jdt_placer_t2", "5D182815CB167405", "blockplacert2", "Advanced Block Placer", "places blocks over a larger area"),
    ("jdt_clicker_t2", "0D32774710EC9900", "clickert2", "Advanced Clicker", "right- or left-clicks with an item, with more settings"),
    ("jdt_sensor_t2", "55E882E7FA36AFC6", "sensort2", "Advanced Sensor", "watches a larger area with filters"),
    ("jdt_dropper_t2", "15AD6698663D4A42", "droppert2", "Advanced Dropper", "drops items with more control"),
    ("jdt_fluid_placer_t2", "6D60602560F35F87", "fluidplacert2", "Advanced Fluid Placer", "places fluid over a larger area"),
    ("jdt_fluid_collector_t2", "4D45C0CFF11191ED", "fluidcollectort2", "Advanced Fluid Collector", "picks up fluid over a larger area"),
]:
    NEW.append(q(key, aid, M2, iid, title, "The tier 2 version", ["jdt_t2_tip", C], [
        f"&eWhat:&r {what}.", "&eHow:&r the Simple version ringed with celestigem (check JEI)."]))
NEW.append(q("jdt_tools_tip", "7AEFF81E7C8CF300", TOOL, "[tick()]", "Dire Tools", "Four metals, every tool", ["jdt_ferricore"], [
    "&eWhat:&r each goo metal makes a full set: sword, pickaxe, axe, shovel, hoe and bow, plus paxels at the top tiers.",
    "&eHow:&r craft the ferricore set, then move each tool up a tier at the smithing table with a template and the next metal.",
    "&eTip:&r Dire tools run on FE or fuel and take ability upgrades."], xp=10, extra=f', icon=J + "ferricore_pickaxe"'))
MAT_OF = {"ferricore": F, "blazegold": B, "celestigem": C, "eclipsealloy": E}
NAME = {"ferricore": "Ferricore", "blazegold": "Blazegold", "celestigem": "Celestigem", "eclipsealloy": "Eclipse Alloy"}
for key, aid, m, piece in [
    ("jdt_fc_axe", "5054977BD5354561", "ferricore", "axe"), ("jdt_fc_shovel", "19E6757F04098A0C", "ferricore", "shovel"),
    ("jdt_fc_hoe", "4773421DC70009AB", "ferricore", "hoe"),
    ("jdt_bg_axe", "21147C8CBF98AEB4", "blazegold", "axe"), ("jdt_bg_shovel", "1DAA5DD81EF96469", "blazegold", "shovel"),
    ("jdt_bg_hoe", "52EC86E03EB50525", "blazegold", "hoe"),
    ("jdt_cg_axe", "2B1BAEC5DAAF9DAC", "celestigem", "axe"), ("jdt_cg_shovel", "0C1D55AA9CC902BD", "celestigem", "shovel"),
    ("jdt_cg_hoe", "237D11FF5B09BA88", "celestigem", "hoe"), ("jdt_cg_paxel", "0272E58516A0C284", "celestigem", "paxel"),
    ("jdt_ec_pickaxe", "0C9DD8E53A1B92C0", "eclipsealloy", "pickaxe"), ("jdt_ec_axe", "78840993C7832E89", "eclipsealloy", "axe"),
    ("jdt_ec_shovel", "703BDCDC88DD813C", "eclipsealloy", "shovel"), ("jdt_ec_hoe", "3138B83ABC2930F9", "eclipsealloy", "hoe"),
]:
    first = m == "ferricore"
    NEW.append(q(key, aid, TOOL, f"{m}_{piece}", f"{NAME[m]} {piece.capitalize()}", f"The {NAME[m].lower()} {piece}", ["jdt_tools_tip", MAT_OF[m]], [
        f"&eWhat:&r the {NAME[m].lower()} {piece}." + (" A paxel is a pickaxe, axe and shovel in one." if piece == "paxel" else ""),
        "&eHow:&r " + ("ferricore ingots in the usual tool shape (check JEI)." if first else
                       f"smith the tier below with a {NAME[m].lower()} template and ingot (check JEI)."),
        "&eTip:&r ability upgrades go on at the smithing table."], xp=30))
for key, aid, m in [("jdt_bow_bg", "567005978482235F", "blazegold"), ("jdt_bow_cg", "35A78E04092767AD", "celestigem")]:
    NEW.append(q(key, aid, TOOL, f"bow_{m}", f"{NAME[m]} Bow", "A Dire bow, one tier up", ["jdt_tools_tip", MAT_OF[m]], [
        "&eWhat:&r a stronger Dire bow that takes arrow abilities.", "&eHow:&r smith the bow below with a template and ingot (check JEI)."], xp=30))
NEW.append(q("jdt_armor_tip", "3971FF7D044D1FE5", ARM, "[tick()]", "Dire Armour", "Four metals, four pieces each", ["jdt_ferricore"], [
    "&eWhat:&r each goo metal makes an armour set; higher tiers hold more abilities.",
    "&eHow:&r craft ferricore armour, then smith it up tier by tier.",
    "&eTip:&r flight only goes on the eclipse alloy chestplate."], xp=10, extra=f', icon=J + "ferricore_helmet"'))
for m in ("ferricore", "blazegold", "celestigem", "eclipsealloy"):
    for piece, aid in {"ferricore": [("chestplate", "7464CA1290B3474B"), ("leggings", "04A1D582003A0D9A"), ("boots", "454CA1F8CC198D9D")],
                       "blazegold": [("chestplate", "1CBA0D7DA0558EBC"), ("leggings", "5A38E9F68570F7F3"), ("boots", "176A1CC43467EF23")],
                       "celestigem": [("chestplate", "4B1E4FC4599DB916"), ("leggings", "3BF32843DE3CF3C2"), ("boots", "1FE7C52491E7499B")],
                       "eclipsealloy": [("chestplate", "5A1AB1AD7DEFDD9A"), ("leggings", "2A919F73CB09CF8B"), ("boots", "1FFA1DA6A5EA4E70")]}[m]:
        short = {"ferricore": "fc", "blazegold": "bg", "celestigem": "cg", "eclipsealloy": "ec"}[m]
        NEW.append(q(f"jdt_{short}_{piece}", aid, ARM, f"{m}_{piece}", f"{NAME[m]} {piece.capitalize()}", f"{NAME[m]} armour", ["jdt_armor_tip", MAT_OF[m]], [
            f"&eWhat:&r the {NAME[m].lower()} {piece}.",
            "&eHow:&r " + ("ferricore ingots in the usual armour shape (check JEI)." if m == "ferricore" else
                           f"smith the piece below with a {NAME[m].lower()} template and ingot (check JEI).")], xp=30))
NEW += [
    q("jdt_util_tip", "6AB45CC4CE4570E6", GAD, "[tick()]", "Dire Gadgets", "Wands, guns and odd tools", ["jdt_ferricore"], [
        "&eWhat:&r the rest of Just Dire Things: canisters, a pocket generator, portal guns, a mob catcher and more.",
        "&eHow:&r most are ferricore or blazegold with vanilla parts (check JEI)."], xp=10, extra=f', icon=J + "fluid_canister"'),
    q("jdt_pocket_gen", "40C5C355B6DA1893", GAD, "pocket_generator", "Pocket Generator", "Burn coal, charge your tools", ["jdt_util_tip", F], [
        "&eWhat:&r burns fuel in your inventory to charge your FE items.", "&eHow:&r ferricore and a furnace (check JEI)."]),
    q("jdt_copier", "0B485DB737A036E9", GAD, "machinesettingscopier", "Machine Settings Copier", "Set one up, copy the rest", ["jdt_util_tip", F], [
        "&eWhat:&r copies one machine's settings onto another.", "&eHow:&r Primal Coal, paper and ferricore (check JEI).",
        "&eTip:&r set up one breaker perfectly, then copy it down a whole row."]),
    q("jdt_wrench", "45A25221F54A1DEC", GAD, "ferricore_wrench", "Ferricore Wrench", "Turn and pick up machines", ["jdt_util_tip", F], [
        "&eWhat:&r rotates and picks up Just Dire Things machines.", "&eHow:&r ferricore ingots (check JEI)."]),
    q("jdt_portalgun", "16E02F671FBE9148", GAD, "portalgun", "Portal Gun", "Two holes in the world", ["jdt_util_tip", B], [
        "&eWhat:&r fires two linked portals you can walk through.", "&eHow:&r blazegold, ender pearls and a fluid canister (check JEI)."]),
    q("jdt_totem", "27FD46A8C958D259", GAD, "totem_of_death_recall", "Totem of Death Recall", "Back to where you fell", ["jdt_util_tip", B], [
        "&eWhat:&r helps you get back to where you died. Read its tooltip.", "&eHow:&r blazegold, ender pearls, diamonds and lapis (check JEI)."]),
    q("jdt_fluid_tip", "66F79F0F1E05D163", FLU, "[tick()]", "Dire Fluids", "Polymorphic fluid and refined fuels", ["jdt_blazegold"], [
        "&eWhat:&r Polymorphic Fluid takes on the nature of what you drop in it: refined fuels, portal fluid, time fluid.",
        "&eHow:&r every fluid recipe is in JEI (search the fluid's bucket)."], xp=10, extra=f', icon=J + "polymorphic_fluid_bucket"'),
    q("jdt_fuel_t4", "49EF8A4346AEF582", FLU, "refined_t4_fluid_bucket", "Eclipse Fuel", "The best Dire fuel", ["jdt_fuel_high", "jdt_coal_t4"], [
        "&eWhat:&r the top refined fuel for the Simple Fuel Generator.", "&eHow:&r Eclipse Ember in Polymorphic Fluid (check JEI).",
        "&eChemistry:&r a denser fuel stores more energy per litre, the way diesel beats ethanol."]),
    q("jdt_portal_fluid", "0FAF274ADA65B26A", FLU, "portal_fluid_bucket", "Portal Fluid", "Fuel for the advanced portal gun", ["jdt_polymorphic"], [
        "&eWhat:&r Portal Fluid powers the Advanced Portal Gun.",
        "&eHow:&r a Portal Fluid Catalyst in Polymorphic Fluid makes unstable portal fluid; tier 3 goo stabilises it (check JEI)."]),
    q("jdt_time_fluid", "48E4D75FD3145AD6", TIME, "time_fluid_bucket", "Time Fluid", "Liquid time", ["jdt_time_crystal", "jdt_polymorphic"], [
        "&eWhat:&r Time Fluid powers the Time Wand and the Paradox Machine.", "&eHow:&r drop a time crystal into a Polymorphic Fluid source."]),
    q("jdt_tool_tag", "4E9B35DCA018FD42", TUP, '[anytag("c:tools")]', "A Tool to Upgrade", "Any tool counts", ["jdt_blank"], [
        "&eWhat:&r tool abilities go on Dire tools at the smithing table: tool, upgrade, and nothing else.",
        "&eHow:&r hold any tool to complete this; the Dire tools are the ones that take upgrades."], xp=10),
    q("jdt_armor_tag", "67B87570C340C243", AUP, '[anytag("c:armors")]', "Armour to Upgrade", "Any armour counts", ["jdt_blank"], [
        "&eWhat:&r armour abilities go on Dire armour the same way: piece, upgrade, smithing table.",
        "&eHow:&r hold any armour piece to complete this."], xp=10),
    q("jdt_upg_tip", "73552A4BA0687962", TUP, "[tick()]", "Using Abilities", "Keybinds and costs", ["jdt_tool_tag", "jdt_armor_tag"], [
        "&eWhat:&r passive abilities just work; active ones sit on keybinds (Controls, Just Dire Things).",
        "&eTip:&r most abilities cost FE or fuel per use. Keep a Pocket Generator on you."], xp=10, extra=f', icon=J + "upgrade_blank"'),
]
for key, aid, iid, title, what, tag in [
    ("jdt_lawnmower", "07655CA904354E9E", "upgrade_lawnmower", "Lawnmower", "cuts grass and flowers around you", "jdt_tool_tag"),
    ("jdt_skysweeper", "46EE2F9818F8D1D9", "upgrade_skysweeper", "Skysweeper", "is a clearing ability for tools; read its tooltip for what it sweeps", "jdt_tool_tag"),
    ("jdt_treefeller", "4D98D2123BD5BFB3", "upgrade_treefeller", "Treefeller", "fells a whole tree from one log", "jdt_tool_tag"),
    ("jdt_leafbreaker", "0E3FDD8BB6D17A30", "upgrade_leafbreaker", "Leafbreaker", "breaks the connected leaves of a tree", "jdt_tool_tag"),
    ("jdt_smelter", "171DB70D0D19A942", "upgrade_smelter", "Smelter", "smelts what you mine as it drops", "jdt_tool_tag"),
    ("jdt_dropteleport", "636854555AD75DC3", "upgrade_dropteleport", "Drop Teleport", "sends your drops to a bound inventory", "jdt_tool_tag"),
    ("jdt_orexray", "18032636A60D0B2C", "upgrade_orexray", "Ore X-Ray", "shows nearby ores through stone", "jdt_tool_tag"),
    ("jdt_glowing", "283D7E65F2AD45F2", "upgrade_glowing", "Mob X-Ray", "outlines mobs through walls", "jdt_tool_tag"),
    ("jdt_orescanner", "5EE7D5DE07A83C7D", "upgrade_orescanner", "Ore Scanner", "scans for ore around you", "jdt_tool_tag"),
    ("jdt_splash", "3CFD798362605880", "upgrade_splash", "Splash", "makes potion arrows burst like splash potions", "jdt_tool_tag"),
    ("jdt_lingering", "6720F863B907A5F1", "upgrade_lingering", "Lingering", "makes potion arrows leave a lingering cloud", "jdt_tool_tag"),
    ("jdt_homing", "3F3559EF5D08B706", "upgrade_homing", "Homing", "steers arrows towards their target", "jdt_tool_tag"),
    ("jdt_epicarrow", "1256F280F3669DDA", "upgrade_epicarrow", "Yondu Arrow", "makes arrows pass through several targets", "jdt_tool_tag"),
    ("jdt_walkspeed", "132F4671E121C7B8", "upgrade_walkspeed", "Walk Speed", "makes you walk faster", "jdt_armor_tag"),
    ("jdt_stepheight", "17A9D2CA160561D9", "upgrade_stepheight", "Step Assist", "lets you walk up full blocks", "jdt_armor_tag"),
    ("jdt_jumpboost", "0CBFE2CE53DCACD5", "upgrade_jumpboost", "Jump Boost", "makes you jump higher", "jdt_armor_tag"),
    ("jdt_mindfog", "3CBB78C9B8D3665E", "upgrade_mindfog", "Mind Fog", "makes mobs notice you less", "jdt_armor_tag"),
    ("jdt_swimspeed", "4ACB72F3A23A5A19", "upgrade_swimspeed", "Swim Speed", "makes you swim faster", "jdt_armor_tag"),
    ("jdt_groundstomp", "6889EFC6CC291463", "upgrade_groundstomp", "Ground Stomp", "pushes nearby mobs away", "jdt_armor_tag"),
    ("jdt_extinguish", "3AE1811C32B94A66", "upgrade_extinguish", "Extinguish", "puts you out when you catch fire", "jdt_armor_tag"),
    ("jdt_stupefy", "09485B63483B7A15", "upgrade_stupefy", "Stupefy", "makes a mob forget you", "jdt_armor_tag"),
    ("jdt_negatefall", "02B8F50721F12CFF", "upgrade_negatefalldamage", "Negate Fall Damage", "stops fall damage", "jdt_armor_tag"),
    ("jdt_nightvision", "120DCA89A919C7AF", "upgrade_nightvision", "Night Vision", "lets you see in the dark", "jdt_armor_tag"),
    ("jdt_decoy", "5961C1ED32522BEF", "upgrade_decoy", "Decoy", "makes mobs attack a dummy instead of you", "jdt_armor_tag"),
    ("jdt_earthquake", "1E0C6409B2573CCA", "upgrade_earthquake", "Earthquake", "slows the mobs around you", "jdt_armor_tag"),
    ("jdt_noai", "7B9486981786AC47", "upgrade_noai", "Mental Obliteration", "stops nearby mobs for good", "jdt_armor_tag"),
    ("jdt_lavaimmunity", "6D9CFCD81A23BB3B", "upgrade_lavaimmunity", "Lava Immunity", "lets you swim in lava", "jdt_armor_tag"),
    ("jdt_deathprotection", "79BBCC1BEE90DBBB", "upgrade_deathprotection", "Death Protection", "saves you from death once every few minutes", "jdt_armor_tag"),
    ("jdt_debuffremover", "026C63594F813BCC", "upgrade_debuffremover", "Debuff Remover", "clears bad potion effects", "jdt_armor_tag"),
    ("jdt_time_protection", "4987759CF379C1EB", "upgrade_time_protection", "Time Protection", "shields you from time effects", "jdt_armor_tag"),
    ("jdt_phase", "454662617304E299", "upgrade_phase", "Phase", "lets you walk through walls", "jdt_upg_tip"),
]:
    sec = TUP if tag == "jdt_tool_tag" else AUP
    NEW.append(q(key, aid, sec, iid, title, "An ability upgrade", [tag], [
        f"&eWhat:&r this ability {what}.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."], xp=30))
for key, aid, m in [("jdt_tpl_bg", "2409EAD96CE3BDF7", "blazegold"), ("jdt_tpl_cg", "25E915AE1FC53254", "celestigem"),
                    ("jdt_tpl_ec", "1EA02BA24AF02256", "eclipsealloy")]:
    NEW.append(q(key, aid, AUP, f"template_{m}", f"{NAME[m]} Template", "Smith gear up a tier", ["jdt_armor_tag", MAT_OF[m]], [
        f"&eWhat:&r the smithing template that moves Dire gear up to {NAME[m].lower()}.",
        f"&eHow:&r an upgrade blank ringed with {NAME[m].lower()} (check JEI).",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."], xp=30))
NEW.append(q("jdt_center_tip", "441F37A95AB66E6B", GOO, "[tick()]", "Waking the Goo", "When goo stops working", ["jdt_goo"], [
    "&eWhat:&r after a conversion, goo can go dormant (a 10% chance in this pack).",
    "&eHow:&r right-click dormant goo with sugar or rotten flesh to wake it, or keep a spare.",
    "&eTip:&r a Simple Clicker holding sugar keeps a goo farm running."], xp=10, extra=', optional=True, tokens=1, icon=J + "gooblock_tier1"'))

INSERT = "    # --- ATM10 mirror round (2026-10-20): one quest per ATM10 Just Dire Things quest ------------------------------\n" + "".join(NEW)
