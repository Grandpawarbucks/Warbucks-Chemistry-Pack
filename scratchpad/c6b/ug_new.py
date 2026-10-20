"""Builds the new quests for undergarden.py (written into the file by ug_apply.py)."""
UG_KILLS = [
    # key, entity, mirror, title, subtitle, what, how, tip
    ("ug_k_rotling", "rotling", "24D38DA8E86DD897", "Rotling", "The smallest rotspawn",
     "rotlings are the small, quick rotspawn: the infection's first wave.",
     "they gather in the dark caverns. Light an area and they come to you.",
     "utherium weapons deal extra damage to every rotspawn."),
    ("ug_k_rotwalker", "rotwalker", "380D3212D1CBA593", "Rotwalker", "Tall, slow and rotten",
     "rotwalkers are the tall rotspawn: slower than rotlings, much tougher.",
     "they wander the caverns in the dark. Fight in the open.",
     "a shard torch nearby softens them up."),
    ("ug_k_rotbeast", "rotbeast", "70FD8856BFCD9AEE", "Rotbeast", "The biggest of the rotspawn",
     "the rotbeast is the heaviest rotspawn, with a lot of health and a hard hit. It drops utheric shards.",
     "find one in the deeper caverns and fight it where you have room to back off.",
     "its shards make shard torches, which keep its kin away."),
    ("ug_k_muncher", "muncher", "5D229FA3A5F92954", "Muncher", "Something with teeth",
     "munchers are one of the Undergarden's hostile hunters.",
     "you'll meet them in the caverns soon enough. Check JEI for what they drop.",
     "keep your armour up when exploring new caverns."),
    ("ug_k_stoneborn", "stoneborn", "4D836B9D9E3B898F", "Stoneborn", "People made of rock",
     "stoneborn are the stony folk of the Undergarden. They drop depthrock pebbles, among other things.",
     "find one in the caverns and fight it. Check JEI for its drops.",
     "pebbles are slingshot ammo."),
    ("ug_k_gloomper", "gloomper", "79C652E3FCB88550", "Gloomper", "A hopping toad",
     "gloompers are hopping toads, one of the Undergarden's game animals. They drop legs and leather.",
     "hunt them in the forests and fields.",
     "they hop away fast; a slingshot or bow helps."),
    ("ug_k_nargoyle", "nargoyle", "0A1D6E233C0ECC8E", "Nargoyle", "A stone predator",
     "nargoyles are among the Undergarden's nastier predators.",
     "they turn up as you explore. Fight with your back to a wall.",
     "the Bounty Board has a bigger hunt for nargoyles and munchers."),
    ("ug_k_sploogie", "sploogie", "67A2347534269528", "Sploogie", "A strange little creature",
     "sploogies are one of the odder creatures that live in the Undergarden's caverns.",
     "find one and bring it down. Check JEI for what it drops.",
     "every creature down here is worth one look in JEI's mob drops."),
    ("ug_k_gwibling", "gwibling", "53FDC6C536E50A1A", "Gwibling", "The small fish of the seas",
     "gwiblings are the little fish of the Undergarden's seas, and they cook into a decent meal.",
     "find one in an Undergarden sea or lake and catch it with a weapon or a bucket.",
     "the full-grown gwib in the same waters is not friendly."),
    ("ug_k_gwib", "gwib", "71E1454990DEC451", "Gwib", "The big fish bites back",
     "the gwib is the gwibling all grown up: a hostile fish that hunts swimmers.",
     "fight it from the shore, or from a block above the water.",
     "Respiration and Depth Strider help if you must fight in the water."),
    ("ug_k_mog", "mog", "744DBE831C120B2F", "Mog", "A mossy burrower",
     "mogs are mossy burrowers. They drop mogmoss and depthrock pebbles.",
     "find them digging in the depthrock forests.",
     "mogmoss makes rugs and slop bowls."),
    ("ug_k_smog_mog", "smog_mog", "2E596B5A4EA2ABF4", "Smog Mog", "A mog of the smog spires",
     "smog mogs are the mogs of the smog spires. They drop blue mogmoss.",
     "visit the smog spires and find one.",
     "the smog spires are worth a visit for the biome quest anyway."),
    ("ug_k_dweller", "dweller", "17C2C8F64B4AE6EE", "Dweller", "A big grazer you can ride",
     "dwellers are big rideable grazers. They drop meat and leather.",
     "hunt them in the forests and fields; an underbean on a stick steers a tame one.",
     "keep one alive and saddled for long cavern trips."),
    ("ug_k_greater_dweller", "greater_dweller", "1A23BBF444D17A63", "Greater Dweller", "The dweller's bigger cousin",
     "the greater dweller is a much bigger relative of the dweller.",
     "it lives in the Undergarden's open caverns. Check JEI for what it drops.",
     "bring a bow: it has plenty of health."),
    ("ug_k_mysterious_pot", "mysterious_pot", "57545837046F552B", "A Pot That Moves", "Not every pot is a pot",
     "some of the pots in a forgotten vestige are creatures pretending to be pots.",
     "break pots in a vestige until one fights back, then finish it.",
     "keep your sword out while you loot the ruins."),
]

UG_BIOMES = [
    # key, biome, mirror, title, what
    ("ug_bi_gronglegrowth", "gronglegrowth", "647A87E800C703C3", "Gronglegrowth",
     "a forest of grongle trees, hung with glowing gronglets."),
    ("ug_bi_ancient_sea", "ancient_sea", "353AEEC116A5DEEF", "Ancient Sea",
     "a dark sea under the world, home to gwiblings, gwibs and glitterkelp."),
    ("ug_bi_wigglewood", "wigglewood_forest", "050D8480EE9D8E62", "Wigglewood Forest",
     "a forest of twisting wigglewood, the wood your slingshot is made from."),
    ("ug_bi_ink_bog", "ink_mushroom_bog", "278D34BBC13356DF", "Ink Mushroom Bog",
     "a bog of giant ink mushrooms."),
    ("ug_bi_veil_bog", "veil_mushroom_bog", "7E3DA4168D352B42", "Veil Mushroom Bog",
     "a bog of giant veil mushrooms."),
    ("ug_bi_indigo_bog", "indigo_mushroom_bog", "0A0A991BAC99092C", "Indigo Mushroom Bog",
     "a bog of giant indigo mushrooms."),
    ("ug_bi_barren_abyss", "barren_abyss", "36389696767EFB4E", "Barren Abyss",
     "a bare, open chasm with little growing in it."),
    ("ug_bi_dead_sea", "dead_sea", "1BAE1519E44E40CE", "Dead Sea",
     "a still, lifeless body of water."),
    ("ug_bi_dense_forest", "dense_forest", "15A8F04BC10E619E", "Dense Forest",
     "the thickest forest below, packed tight with trees."),
    ("ug_bi_frostfields", "frostfields", "1E13D7CE5A9EFF74", "Frostfields",
     "frozen fields of shiverstone, where froststeel ore forms."),
    ("ug_bi_frosty_smogstem", "frosty_smogstem_forest", "0C98503A2F20484D", "Frosty Smogstem Forest",
     "a smogstem forest gone cold and white."),
    ("ug_bi_icy_sea", "icy_sea", "073BA8470EA37A00", "Icy Sea",
     "a frozen sea in the Undergarden's cold corner."),
    ("ug_bi_smog_spires", "smog_spires", "511144EF336BFAF5", "Smog Spires",
     "tall spires that belch smog, home of the smog mogs."),
    ("ug_bi_smogstem", "smogstem_forest", "43FD4AEBB9548E57", "Smogstem Forest",
     "the Undergarden's everyday forest of smogstem trees."),
    ("ug_bi_rogdorium_grove", "rogdorium_grove", "6F483B77D64F4EE2", "Rogdorium Grove",
     "the richest place in the Depths for rogdorium."),
]

CHEM = {
    "ug_bi_ancient_sea": "&eChemistry:&r with no sunlight, nothing in a sea like this can photosynthesise; real deep-sea vents feed whole ecosystems on chemosynthesis, oxidising H₂S for energy.",
    "ug_bi_smog_spires": "&eChemistry:&r real industrial smog is soot plus sulfur dioxide (SO₂), which forms sulfuric acid droplets in damp air.",
    "ug_bi_frostfields": "&eChemistry:&r water is odd: it expands as it freezes (ice is about 9% less dense), which is why ice floats and frost splits rock.",
    "ug_bi_dead_sea": "&eChemistry:&r the real Dead Sea is about 34% salt, mostly MgCl₂ and NaCl; so dense that people float in it, and too salty for fish.",
}


def kills():
    out = []
    for key, ent, mir, title, sub, what, how, tip in UG_KILLS:
        dep = "wd_vestige" if ent == "mysterious_pot" else "ug_enter"
        out.append(f'''    Q("{key}", 0, 0, [kill(UG + "{ent}")], "{title}", deps=["{dep}"], xp=75, loot="hunt", mirror="{mir}",
      section="Creatures of the Dark", subtitle="{sub}", desc=[
        "&eWhat:&r {what}",
        "&eHow:&r {how}",
        "&eTip:&r {tip}"]),''')
    return "\n".join(out)


def biomes():
    out = []
    for key, b, mir, title, what in UG_BIOMES:
        dep = "ug_depths" if b == "rogdorium_grove" else "ug_enter"
        lines = [f'"&eWhat:&r {what}"']
        if key in CHEM:
            lines.append(f'"{CHEM[key]}"')
        how = ("tunnel down through the dreadrock with a Forgotten pickaxe and find it in the Depths." if b == "rogdorium_grove"
               else "Nature's Compass works in the Undergarden. Walk in.")
        lines.append(f'"&eHow:&r {how}"')
        body = ",\n        ".join(lines)
        out.append(f'''    Q("{key}", 0, 0, [biome(UG + "{b}")], "{title}", deps=["{dep}"], xp=50, mirror="{mir}",
      section="Biomes Below", subtitle="Visit the {title.lower()}", desc=[
        {body}]),''')
    return "\n".join(out)
