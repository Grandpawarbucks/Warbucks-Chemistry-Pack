// Flight gating (user choice "Option 2", 2026-10-18): every way to fly is a chemistry milestone.
//
//   Infusion Pylon + Potion of Flying  end of Ch. II   needs hydrogen from the Alchemistry Dissolver
//   Iron Jetpacks                      LV -> EV        coils need MI analog/electronic/digital/processing circuits
//   Angel Ring                         HV+             needs an MI digital circuit (plus its Elytra and Nether Stars)
//
// Also gated elsewhere: Just Dire Things flight upgrade (End Crystals, unchanged) and the Ars Nouveau
// Ritual of Flight (Source, area-limited).

ServerEvents.recipes(event => {
  const reshape = (originalId, result, pattern, key) => {
    event.remove({ id: originalId })
    event.shaped(result, pattern, key).id('kubejs:phase4/' + originalId.replace(':', '/'))
  }

  // --- Infusion Pylon: lighter than air -----------------------------------------------------
  // Hydrogen, the lightest element, carried the first manned balloons. It can only be extracted
  // as an item by the Alchemistry Dissolver (chemlib:hydrogen), so flight needs both the Nether
  // (quartz, blackstone) and your first Alchemistry machine.
  reshape('pylons:infusion_pylon', 'pylons:infusion_pylon',
    ['qhq', 'idi', 'bbb'],
    { q: 'minecraft:quartz_slab', h: 'chemlib:hydrogen', i: 'minecraft:iron_bars',
      d: 'minecraft:emerald_block', b: 'minecraft:polished_blackstone' })

  // --- Potion of Flying without the End ----------------------------------------------------
  // Apothic Attributes brews Flying from Levitation + popped chorus fruit, which only grows in
  // the End. The design puts flight right after the Nether, so add a chemistry route: a Potion of
  // Levitation (phantom membrane, then fermented spider eye; no End needed) plus hydrogen, the
  // lightest gas, crafts a Potion of Flying. Longer versions still come from brewing as normal.
  // Potion ids were checked on the running server (apothic_attributes:levitation / :flying).
  event.custom({
    type: 'minecraft:crafting_shapeless',
    category: 'misc',
    ingredients: [
      { type: 'neoforge:components', items: 'minecraft:potion',
        components: { 'minecraft:potion_contents': { potion: 'apothic_attributes:levitation' } } },
      { item: 'chemlib:hydrogen' },
      { item: 'chemlib:hydrogen' }
    ],
    result: { id: 'minecraft:potion', components: { 'minecraft:potion_contents': { potion: 'apothic_attributes:flying' } } }
  }).id('kubejs:phase4/flight/potion_of_flying_from_hydrogen')

  // --- Iron Jetpacks -----------------------------------------------------------------------
  // Every jetpack tier's cells and thrusters use one of four coils (Iron Jetpacks picks the coil
  // from the jetpack's tier; even the wooden jetpack needs a basic coil). Each coil's wooden rod
  // becomes the matching MI circuit, so jetpacks unlock tier by tier with MI's voltage ladder.
  const coil = (name, circuit, metal) =>
    reshape(`ironjetpacks:${name}_coil`, `ironjetpacks:${name}_coil`,
      [' DR', 'DSD', 'RD '], { R: '#c:dusts/redstone', D: metal, S: circuit })
  coil('basic', 'modern_industrialization:analog_circuit', '#c:ingots/iron')        // LV
  coil('advanced', 'modern_industrialization:electronic_circuit', '#c:ingots/gold') // MV
  coil('elite', 'modern_industrialization:digital_circuit', '#c:gems/diamond')      // HV
  coil('ultimate', 'modern_industrialization:processing_unit', '#c:gems/emerald')   // EV

  // --- Angel Ring --------------------------------------------------------------------------
  // Already late (Elytra, ghast tears, diamond blocks, Nether Stars). Its blaze rod becomes an
  // MI digital circuit, so portable free flight also needs polyethylene chemistry (HV).
  reshape('angelring:angel_ring', 'angelring:angel_ring',
    ['FXF', 'GEG', 'NGN'],
    { F: 'minecraft:feather', X: 'modern_industrialization:digital_circuit', G: 'minecraft:gold_block',
      E: 'angelring:diamond_ring', N: 'minecraft:nether_star' })
})
