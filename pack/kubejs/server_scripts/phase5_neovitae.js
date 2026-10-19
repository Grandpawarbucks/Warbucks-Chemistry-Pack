// Neo Vitae (blood magic, added 2026-10-19): fit it into the chemistry progression.
// Research and the reasoning for each change: docs/research/neo_vitae.md. All recipe ids below were read from
// neovitae-1.21.1-1.1.44.jar (data/neovitae/recipe) or from the recipe ids its material system generates
// (com/breakinblocks/neovitae/common/material/MaterialRegistry). pack/config/neovitae/materials.json pins the
// material list (the mod's 12 defaults minus netherite scrap), so client and server register the same items.
//
//   Ore processing    Athanor 5x per ore / 3x per raw (more with Spiritus) -> 2x per ore, raw ore only via dust (<= 1.5x)
//   Flight            Flight flask fusion + Tenebrae scribe tool (Ritual of the Condor) need hydrogen, like every flight
//   Free resources    Nether Star from a diamond and every meteor catalyst removed
//   Tier              Athanor needs MI analog circuits (LV); Tenebrae rituals need an MI electronic circuit (MV)

ServerEvents.recipes(event => {
  // --- 1. Ore processing: the pack cap is 2x per ore block before acids ---------------------------------------
  // The Athanor (an alchemical furnace) turns an ore block into 5 fragments and raw ore into 3, and a chunk full of
  // Raw Spiritus adds one more ("spiritus_boost"). Each fragment -> 1 gravel -> 1 dust -> 1 ingot, so that is 5-6x per
  // ore. Real hydrometallurgy gets more metal out of ore by dissolving it (acid leaching), which this pack keeps for
  // Mekanism's acid chain. So here: ore -> 2 fragments with no Spiritus bonus (2x), raw ore -> fragments is removed
  // (raw ore still goes straight to 1 dust plus a 25% bonus, at most 1.5x even when better cutting fluid doubles the
  // bonus chance), dust-only materials (coal: 6 dust) get at most 2 dust per ore, and the Tabula Vitae recipe that
  // turns a fragment plus corrupted dust into 2 more gravel goes. The Tabula Vitae's own ore -> 2 dust stays (2x).
  // Demonite/hellforged is Neo Vitae's own magic metal from its Demon Realm, not a chemistry metal: left as designed.
  const own = id => /(demonite|hellforged)/.test(id)
  const reAdd = (r, json, why) => {
    const id = String(r.getId())
    event.remove({ id: id })
    event.custom(json).id('kubejs:phase5/neovitae/' + id.replace(':', '/'))
    console.info(`[phase5] neovitae ${id}: ${why}`)
  }
  event.findRecipes({ type: 'neovitae:athanor' }).forEach(r => {
    const id = String(r.getId())
    if (own(id)) return
    const json = JSON.parse(String(r.json))
    const out = (json.guaranteed_outputs || [])[0]
    if (!out) return
    const fragments = /_fragment$/.test(String(out.id))
    if (fragments && out.count <= 3) {          // raw ore (or an extra raw item) -> 3 fragments
      event.remove({ id: id })
      console.info(`[phase5] neovitae ${id}: removed (raw ore -> 3 fragments)`)
    } else if (fragments && out.count > 2) {    // ore block (or an extra ore item) -> 5 fragments
      out.count = 2
      json.spiritus_boost = false
      reAdd(r, json, 'ore -> 2 fragments, no Spiritus bonus')
    } else if (/cutting_fluids\/dusts_from_/.test(id) && (out.count > 2 || json.spiritus_boost)) {
      out.count = Math.min(out.count, 2)        // dust-only materials: ore -> dust_yield_from_ore (coal 6, others 3)
      json.spiritus_boost = false
      reAdd(r, json, 'ore -> at most 2 dust')
    } else if (/cutting_fluids\/dusts_from_raw_/.test(id) && json.chance_outputs) {
      json.chance_outputs.forEach(c => { c.chance = Math.min(c.chance, 0.25) })
      reAdd(r, json, 'raw -> 1 dust + 25% (<= 1.5x with the best cutting fluid)')
    }
  })
  event.findRecipes({ type: 'neovitae:alchemytable' }).forEach(r => {
    const id = String(r.getId())
    if (/^neovitae:alchemytable\/corrupted_/.test(id) && !own(id)) {
      event.remove({ id: id })                 // fragment + corrupted dust -> 2 gravel (doubles the chain again)
      console.info(`[phase5] neovitae ${id}: removed (fragment doubling)`)
    }
  })

  // --- 2. Flight is a chemistry milestone (phase4_flight.js) ----------------------------------------------------
  // The Flight elixir is made by fusing Suspended + Levitation in an Alchemy Flask with a Combinational Catalyst.
  // Same rule as the Potion of Flying and the Ars Ritual of Flight tablet: lift needs the lightest gas, hydrogen (H2,
  // 2 g/mol against air's ~29 g/mol), which only the Alchemistry Dissolver gives as an item (chemlib:hydrogen).
  event.remove({ id: 'neovitae:flask/suspended_to_flight' })
  event.custom({
    type: 'neovitae:flask_effect_transform',
    input: [{ item: 'neovitae:combinational_catalyst' }, { item: 'chemlib:hydrogen' }, { item: 'chemlib:hydrogen' }],
    inputEffects: ['neovitae:suspended', 'minecraft:levitation'],
    outputEffects: [{ duration: 3600, effect: 'neovitae:flight' }],
    syphon: 1000, ticks: 200, upgradeLevel: 1
  }).id('kubejs:phase5/neovitae/flask/suspended_to_flight')

  // The Ritual of the Condor (area flight) needs Tenebrae runes, and those are inscribed with the Tenebrae scribe
  // tool, which the altar made from a plain coal block. It moves to the Tabula Vitae: the coal block becomes a dark
  // "ink" with 2 hydrogen (flight, as above) and an MI electronic circuit (MV), because Tenebrae is the altar's
  // fourth tier and also opens the Endless Quarry-style rites (Meteo, Torment Nexus, Enchanted Vitae).
  // Chemistry: soot (carbon black) is the oldest pigment in ink; hydrogen is what a coal fire drives off as it cokes.
  event.remove({ id: 'neovitae:ara_vitae/tenebrae_tool' })
  event.custom({
    type: 'neovitae:alchemytable',
    input: [{ tag: 'c:storage_blocks/coal' }, { item: 'chemlib:hydrogen' }, { item: 'chemlib:hydrogen' },
      { item: 'modern_industrialization:electronic_circuit' }],
    output: { count: 1, id: 'neovitae:tenebrae_scribe_tool' },
    syphon: 2000, ticks: 200, upgradeLevel: 3
  }).id('kubejs:phase5/neovitae/tenebrae_scribe_tool')

  // --- 3. No free milestone resources ---------------------------------------------------------------------------
  // Nether Stars gate the Angel Ring and ProjectE lite; a diamond is carbon and can't become one.
  event.remove({ id: 'neovitae:athanor/resonator/nether_star_from_diamond' })
  // The Ritual of Meteo (and its Deus form) drops a sphere of ore from one catalyst: an iron block calls ~radius 14
  // of iron/copper/gold ore, a diamond calls diamond and emerald ore, a Nether Star ancient debris, certus quartz a
  // core of fluix blocks. That bypasses ore deposits and the chemistry lines, so the catalysts are removed (the ritual
  // stays, it just has nothing to call). Ore in this pack comes from the ground and from chemistry.
  ;['ae2', 'diamond', 'iron', 'nether', 'nether_star', 'stone']
    .forEach(m => event.remove({ id: `neovitae:meteor/${m}` }))

  // --- 4. Athanor at LV ---------------------------------------------------------------------------------------
  // The Athanor is Neo Vitae's reaction chamber (ore processing, sulfur from netherrack, the Deus-tier gems). A
  // furnace that "feeds itself" and keeps a steady heat is a thermostat problem: its two iron blocks become MI
  // analog circuits, the first control electronics in the pack (LV).
  event.remove({ id: 'neovitae:athanor_block' })
  event.custom({
    type: 'minecraft:crafting_shaped',
    category: 'misc',
    key: {
      c: { item: 'modern_industrialization:analog_circuit' },
      S: { item: 'neovitae:tabula_animata' },
      f: { item: 'minecraft:furnace' },
      o: { type: 'neovitae:orb_tier', tier: 2 },
      s: { tag: 'neovitae:vitae_stone' }
    },
    pattern: ['sss', 'SoS', 'cfc'],
    result: { count: 1, id: 'neovitae:athanor' }
  }).id('kubejs:phase5/neovitae/athanor')
})
