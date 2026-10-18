// ProjectE "lite" (user decision 2026-10-18; reverses the earlier "No ProjectE").
// ProjectE is the demigod's endgame toy for building and terraforming, not a way around chemistry:
//   1. The Philosopher's Stone needs oganesson (element 118), so ProjectE opens only after the
//      player has completed the periodic table (Alchemistry fusion, T5+).
//   2. Condensers, Collectors and Relays are removed: they turn EMC into unlimited items or
//      power, which would bypass every tier gate.
//   3. Metals and chemistry materials have no EMC (config/ProjectE/custom_emc.json, EMC 0;
//      custom-conversion files can't hold 0, only positive values), so transmutation can't make ingots, dusts, plates, ores or gems.

ServerEvents.recipes(event => {
  // 1. Philosopher's Stone: the diamond in the centre becomes oganesson. The alternative layout
  //    is removed so there's one recipe.
  event.remove({ id: 'projecte:philosophers_stone_alt' })
  event.remove({ id: 'projecte:philosophers_stone' })
  event.shaped('projecte:philosophers_stone', ['RGR', 'GOG', 'RGR'], {
    R: '#c:dusts/redstone', G: '#c:dusts/glowstone', O: 'chemlib:oganesson'
  }).id('kubejs:phase4/projecte/philosophers_stone')

  // 2. No EMC-to-matter or EMC-to-power machines.
  ;['condenser_mk1', 'condenser_mk2', 'collector_mk1', 'collector_mk2', 'collector_mk3',
    'relay_mk1', 'relay_mk2', 'relay_mk3'].forEach(r => event.remove({ id: `projecte:${r}` }))
})
