// T4 aluminium line: the Bayer process and the Hall-Heroult cell (machine and fluid registered in
// startup_scripts/aluminum_line.js). Aluminium gates MV (electronic circuit board, Chemical Reactor,
// Electrolyzer, advanced casing), so this is the LV -> MV chemistry gate. Every machine used here is
// LV and needs no aluminium.
//
//   lye        Combiner NaOH crystals + water -> NaOH solution (bootstrap; later the Chemical Reactor)
//   digestion  Mixer: 4 bauxite + 1000 mB NaOH -> 1000 mB sodium aluminate + red mud (Fe, Ti)
//              Al(OH)3 + NaOH -> NaAl(OH)4; iron and titanium oxides don't dissolve and stay behind
//   precipitate Mixer: aluminate + water -> 4 Al(OH)3, 900 mB NaOH back (the Bayer loop recycles lye)
//   calcine    EBF: 2Al(OH)3 -> Al2O3 + 3H2O
//   cell       Hall-Heroult Cell: Al2O3 + carbon anode -> Al (+ CO2); a little fluorite tops up the flux
// Net: 4 bauxite -> 2 aluminium ingots (MI's electrolyzer gave 1.6). Alumina from the Alchemistry
// Combiner (chemlib:aluminum_oxide) works in the cell too: the alchemical route.

ServerEvents.tags('item', event => {
  event.add('warbucks:sodium_hydroxide', ['chemlib:sodium_hydroxide', 'chemlib:sodium_hydroxide_dust'])
  event.add('warbucks:aluminum_hydroxide', ['chemlib:aluminum_hydroxide', 'chemlib:aluminum_hydroxide_dust'])
  event.add('warbucks:alumina', ['chemlib:aluminum_oxide', 'chemlib:aluminum_oxide_dust'])
})

ServerEvents.recipes(event => {
  const MI = 'modern_industrialization'
  const mi = (type, json, id) => event.custom(Object.assign({ type: `${MI}:${type}` }, json)).id(`kubejs:aluminum/${id}`)

  // MI's shortcuts skip the chemistry: bauxite straight into the EBF or the Electrolyzer.
  ;['materials/blast_furnace/bauxite_to_aluminum_ingot', 'materials/blast_furnace/bauxite_to_aluminum_nugget',
    'materials/electrolyzer/bauxite'].forEach(path => event.remove({ id: `${MI}:${path}` }))

  mi('mixer', {
    eu: 2, duration: 100,
    item_inputs: [{ tag: 'warbucks:sodium_hydroxide', amount: 1 }],
    fluid_inputs: [{ fluid: 'minecraft:water', amount: 250 }],
    fluid_outputs: [{ fluid: `${MI}:sodium_hydroxide`, amount: 250 }]
  }, 'lye')

  mi('mixer', {
    eu: 8, duration: 200,
    item_inputs: [{ tag: 'c:dusts/bauxite', amount: 4 }],
    fluid_inputs: [{ fluid: `${MI}:sodium_hydroxide`, amount: 1000 }],
    item_outputs: [{ item: `${MI}:iron_tiny_dust`, amount: 2 }, { item: `${MI}:titanium_tiny_dust`, amount: 1 }],
    fluid_outputs: [{ fluid: `${MI}:sodium_aluminate_solution`, amount: 1000 }]
  }, 'digestion')

  mi('mixer', {
    eu: 4, duration: 300,
    fluid_inputs: [{ fluid: `${MI}:sodium_aluminate_solution`, amount: 1000 }, { fluid: 'minecraft:water', amount: 1000 }],
    item_outputs: [{ item: 'chemlib:aluminum_hydroxide_dust', amount: 4 }],
    fluid_outputs: [{ fluid: `${MI}:sodium_hydroxide`, amount: 900 }]
  }, 'precipitation')

  mi('blast_furnace', {
    eu: 16, duration: 200,
    item_inputs: [{ tag: 'warbucks:aluminum_hydroxide', amount: 2 }],
    item_outputs: [{ item: 'chemlib:aluminum_oxide_dust', amount: 1 }]
  }, 'calcination')

  mi('hall_heroult_cell', {
    eu: 32, duration: 300,
    item_inputs: [
      { tag: 'warbucks:alumina', amount: 1 },
      { item: `${MI}:coke_dust`, amount: 1, probability: 0.5 },
      { item: 'mekanism:dust_fluorite', amount: 1, probability: 0.05 }
    ],
    item_outputs: [{ item: `${MI}:aluminum_ingot`, amount: 1 }]
  }, 'electrolysis')

  // Controller: steel, coils and LV parts only.
  event.shaped(`${MI}:hall_heroult_cell`, ['PAP', 'KHK', 'PAP'], {
    P: `${MI}:steel_large_plate`,
    A: `${MI}:analog_circuit`,
    K: `${MI}:cupronickel_coil`,
    H: `${MI}:basic_machine_hull`
  }).id('kubejs:aluminum/hall_heroult_cell')
})
