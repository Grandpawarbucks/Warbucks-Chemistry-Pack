"""Quest chapter: create. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("create", "The Mechanical Age", "create:cogwheel",
        ["Create: rotation, presses and mixers. An early mechanical age that runs alongside steam and feeds into Modern Industrialization."], SIDE, [
    Q("cr_alloy", 0, 0, [item("create:andesite_alloy", 16)], "Andesite Alloy", deps=["gs_iron"], xp=30, desc=[
        "Andesite plus iron (or zinc) nuggets: the frame of every early Create machine.",
        "How: craft it, or mix it in a Mechanical Mixer later for better yields."]),
    Q("cr_power", 2, 0, [item("create:shaft", 8), item("create:cogwheel", 8), item("create:water_wheel")], "Rotational Power", deps=["cr_alloy"], xp=40, desc=[
        "Create runs on rotation, not electricity. A water wheel on flowing water turns shafts and cogs.",
        "Speed and stress capacity matter: big machines need more stress units (check the Engineer's Goggles)."]),
    Q("cr_press", 4, -1, [item("create:mechanical_press"), item("create:basin")], "Pressing and Mixing", deps=["cr_power"], xp=50, desc=[
        "The press flattens ingots into plates and compacts items in a basin."]),
    Q("cr_mixer", 6, -1, [item("create:mechanical_mixer"), item("create:blaze_burner")], "Heated Mixing", deps=["cr_press", "t2_blaze"], xp=75, desc=[
        "A mixer over a basin heated by a Blaze Burner makes alloys and fluids: Create's chemistry bench."]),
    Q("cr_crush", 4, 1, [item("create:millstone"), item("create:crushing_wheel", 2)], "Crushing", deps=["cr_power"], xp=60, desc=[
        "Crushing wheels turn ore into crushed ore. In this pack they give at most &e2x per ore block&r, like everything before acids."]),
    Q("cr_wash", 6, 1, [item("create:encased_fan"), item("create:crushed_raw_iron", 8)], "Bulk Washing", deps=["cr_crush"], xp=60, desc=[
        "Blow crushed ore through water with a fan: it washes into nuggets plus a byproduct (iron gives redstone, for example)."]),
    Q("cr_brass", 8, 0, [item("create:zinc_ingot", 8), item("create:brass_ingot", 8)], "Brass", deps=["cr_mixer"], xp=100, size=1.5, desc=[
        "Copper plus zinc, mixed hot: &ebrass&r, the key metal of Create's second age.",
        "Zinc ore generates in the world (it's Create's)."]),
    Q("cr_precision", 10, 0, [item("create:precision_mechanism"), item("create:mechanical_crafter", 4)], "Precision", deps=["cr_brass"], xp=150, desc=[
        "Precision mechanisms come from a multi-step sequenced assembly: Create's version of a production line."]),
    Q("cr_alternator", 12, -1, [item("createaddition:alternator")], "Rotation to Electricity", deps=["cr_precision", "t3_analog"], xp=150, desc=[
        "Crafts and Additions' Alternator turns rotation into FE. In this pack it needs an &eMI analog circuit&r (LV)."]),
    Q("cr_motor", 12, 1, [item("createaddition:electric_motor")], "Electricity to Rotation", deps=["cr_alternator"], xp=100, desc=[
        "The reverse: power Create contraptions from your MI or Mekanism grid."]),
    Q("cr_newage", 14, -1, [item("create_new_age:generator_coil"), item("create_new_age:basic_energiser")], "Create: New Age", deps=["cr_alternator"], xp=150, desc=[
        "Magnet-and-coil generators (the coil needs an analog circuit) and Energisers that charge items with electricity."]),
    Q("cr_reactor", 16, -1, [item("create_new_age:thorium", 8), item("create_new_age:reactor_rod")], "Thorium Reactor", deps=["cr_newage", "t6_pu"], xp=400, desc=[
        "New Age's nuclear reactor burns &ethorium&r. Its rods need an &eMI processing unit&r (EV), so it arrives alongside Mekanism fission."]),
    Q("cr_enchant", 14, 1, [item("create_enchantment_industry:blaze_enchanter")], "Automated Enchanting", deps=["cr_precision"], xp=100, desc=[
        "Enchantment Industry turns XP into a fluid and enchants items automatically."]),
])
