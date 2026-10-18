// Occultism gating (added 2026-10-18). Occultism's miner spirits pull ores out of the
// "otherworld" in a Dimensional Mineshaft. That's a fine mid-game convenience for common ores,
// but like Mystical Agriculture (phase4_mysticalagriculture.js) it must not hand out the
// resources that are chemistry milestones: fissile/nuclear materials, Mekanism-only minerals,
// and the rare metals that the PGM processing line and EV/IV tiers are built around.
// Recipe ids were listed from Occultism's jar (data/occultism/recipe/miner/...).

ServerEvents.recipes(event => {
  const blocked = [
    // ores/ (basic and master miners)
    'ores/uranium_ore', 'ores/uraninite_ore', 'ores/uraninite_poor_ore', 'ores/uraninite_regular_ore',
    'ores/uraninite_dense_ore', 'ores/osmium_ore', 'ores/fluorite_ore', 'ores/platinum_ore',
    'ores/iridium_ore', 'ores/tungsten_ore',
    // eldritch/ (the strongest miners give raw materials directly)
    'eldritch/raw_uranium', 'eldritch/uraninite', 'eldritch/raw_osmium', 'eldritch/fluorite',
    'eldritch/raw_platinum', 'eldritch/raw_iridium', 'eldritch/raw_tungsten'
  ]
  blocked.forEach(id => event.remove({ id: `occultism:miner/${id}` }))
  console.info(`[phase4] Occultism: removed ${blocked.length} miner recipes for chemistry-milestone resources`)
})
