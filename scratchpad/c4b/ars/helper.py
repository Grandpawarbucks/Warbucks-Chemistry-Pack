
GLYPH_HUB = {1: "ars_glyph_t1", 2: "ars_glyph_t2", 3: "ars_glyph_t3"}
GLYPH_XP_COST = {1: 27, 2: 55, 3: 160}  # experience points per glyph (the recipes' "exp")


def glyph(tier, name, mirror, title, subtitle, what, cost, tip, chem=None):
    """One glyph quest: hold the scribed glyph. Tier 3 glyphs need the (optional) Archmage book, so they're optional."""
    desc = ["&eWhat:&r " + what]
    if chem:
        desc.append("&eChemistry:&r " + chem)
    desc += [f"&eHow:&r at the Scribe's Table: {cost}, plus {GLYPH_XP_COST[tier]} experience points. Learn it into your book afterwards.",
             "&eTip:&r " + tip]
    opt = tier == 3
    return Q("ars_g_" + name, 0, 0, [item("ars_nouveau:glyph_" + name)], title, deps=[GLYPH_HUB[tier]],
             xp={1: 20, 2: 30, 3: 50}[tier], subtitle=subtitle, mirror=mirror, optional=opt, tokens=1 if opt else None,
             desc=desc)


def glyphs(tier, rows):
    return [glyph(tier, *row) for row in rows]

