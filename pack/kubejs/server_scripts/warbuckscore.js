// Recipes for the pack's own mod, Warbucks Core (source in mod/). The mod ships no recipes so it
// doesn't depend on MI/KubeJS items; they're set here instead.

ServerEvents.recipes(event => {
  const MI = 'modern_industrialization'

  // Spectrometer (LV): an amethyst prism splits light into a spectrum; each element's ore has its
  // own signature. Needs an MI analog circuit, so it arrives with your first LV machines.
  event.shaped('warbuckscore:spectrometer', [' A ', 'PCP', 'PWP'], {
    A: 'minecraft:amethyst_shard', P: `${MI}:steel_plate`, C: `${MI}:analog_circuit`, W: `${MI}:copper_wire`
  }).id('kubejs:warbuckscore/spectrometer')

  // Biome Capsule: a sealed sample bottle (rubber stopper) with a sapling as the living sample.
  event.shapeless('warbuckscore:biome_capsule', ['minecraft:glass_bottle', `${MI}:rubber_sheet`, '#minecraft:saplings'])
    .id('kubejs:warbuckscore/biome_capsule')

  // Terraformer: planting the Seed of a New World. Consumes the Seed (the finale item), so it opens
  // the Creation chapter. It runs on Charged Energy Cores (#warbuckscore:terraformer_fuel).
  event.shaped('warbuckscore:terraformer', ['PUP', 'ESE', 'PUP'], {
    P: `${MI}:stainless_steel_plate`, U: `${MI}:processing_unit`, E: 'kubejs:energy_core',
    S: 'kubejs:seed_of_a_new_world'
  }).id('kubejs:warbuckscore/terraformer')
})
