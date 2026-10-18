// Phase 4: integration — tie every tech/magic mod into Modern Industrialization's tier ladder,
// so each tier is gated by a chemistry milestone (docs/PROGRESSION.md §3–4).
//
// MI's own ladder is already chemical:
//   LV  Basic hull            analog circuit, steel casing         (coke → steel)
//   MV  Advanced hull         electronic circuit (aluminum)        (bauxite electrolysis, silicon)
//   HV  Turbo hull            digital circuit (polyethylene)       (petrochemistry, salt → sodium)
//   EV  Highly advanced hull  processing unit (PVC)                (chlorine chemistry)
//   IV  Quantum hull          quantum circuit, plutonium battery   (nuclear)
// The recipes below make other mods' key components require the matching MI part.
// Every replaced recipe is removed by its original id and re-added under kubejs:phase4/...

ServerEvents.recipes(event => {
  // Replace a shaped recipe: remove the original id, add the new one under kubejs:phase4/<path>.
  const reshape = (originalId, result, pattern, key) => {
    event.remove({ id: originalId })
    event.shaped(result, pattern, key).id('kubejs:phase4/' + originalId.replace(':', '/'))
  }

  // --- T1: the periodic table opens (steam age) --------------------------------------------
  // Alchemistry's Dissolver and Combiner are the pack's signature machines. Building them
  // needs steel (which needs coke) and an MI bronze machine casing, so they arrive at the end
  // of the steam age. They still need FE: Iron Furnaces generators, Powah Furnator or
  // Mekanism heat generators can run them before MI's electric age.
  reshape('alchemistry:dissolver', 'alchemistry:dissolver',
    ['IPI', 'MCM', 'IPI'],
    { I: '#c:plates/steel', P: 'minecraft:piston', M: 'minecraft:magma_block',
      C: 'modern_industrialization:bronze_machine_casing' })
  reshape('alchemistry:combiner', 'alchemistry:combiner',
    ['IDI', 'OCO', 'IPI'],
    { I: '#c:plates/steel', D: 'minecraft:diamond', O: 'minecraft:obsidian', P: 'minecraft:piston',
      C: 'modern_industrialization:bronze_machine_casing' })

  // --- Mekanism control circuits follow MI's circuit tiers (LV → EV) -----------------------
  // Mekanism's basic circuit was osmium + redstone in the Metallurgic Infuser, and each higher
  // circuit had an infuser shortcut. Now each Mekanism circuit needs the same-tier MI circuit,
  // so Mekanism machines unlock alongside MI's voltage tiers. Infuser shortcuts are removed.
  event.remove({ id: 'mekanism:control_circuit/basic' })
  event.remove({ id: 'mekanism:control_circuit/infused_advanced' })
  event.remove({ id: 'mekanism:control_circuit/infused_elite' })
  event.remove({ id: 'mekanism:control_circuit/infused_ultimate' })
  // LV: MI analog circuit + osmium.
  event.shapeless('mekanism:basic_control_circuit',
    ['modern_industrialization:analog_circuit', '#c:ingots/osmium'])
    .id('kubejs:phase4/mekanism/control_circuit/basic')
  // MV: MI electronic circuit (aluminum chemistry).
  reshape('mekanism:control_circuit/advanced', 'mekanism:advanced_control_circuit',
    [' E ', 'ACA'], { E: 'modern_industrialization:electronic_circuit', A: '#mekanism:alloys/infused',
      C: '#c:circuits/basic' })
  // HV: MI digital circuit (polyethylene).
  reshape('mekanism:control_circuit/elite', 'mekanism:elite_control_circuit',
    [' D ', 'ACA'], { D: 'modern_industrialization:digital_circuit', A: '#mekanism:alloys/reinforced',
      C: '#c:circuits/advanced' })
  // EV: MI processing unit (PVC / chlorine chemistry).
  reshape('mekanism:control_circuit/ultimate', 'mekanism:ultimate_control_circuit',
    [' P ', 'ACA'], { P: 'modern_industrialization:processing_unit', A: '#mekanism:alloys/atomic',
      C: '#c:circuits/elite' })

  // --- T3: acids -------------------------------------------------------------------------
  // The Undergarden opens with acid chemistry: its portal catalyst needs a bucket of sulfuric acid.
  reshape('undergarden:catalyst', 'undergarden:catalyst',
    ['CAC', 'SES', 'CSC'],
    { C: '#c:ingots/copper', A: 'modern_industrialization:sulfuric_acid_bucket',
      E: '#c:ender_pearls', S: '#c:stones' })

  // Powah's Energizing Orb (entry to all Powah tech) needs an MV electronic circuit.
  reshape('powah:crafting/energizing_orb', 'powah:energizing_orb',
    ['geg', 'gcg', 'rrr'],
    { g: '#c:glass_blocks', e: 'modern_industrialization:electronic_circuit',
      c: 'powah:dielectric_casing', r: 'powah:dielectric_rod_horizontal' })

  // Uraninite is uranium dioxide (UO₂). Powah's ore generation is off (Phase 3); instead it is
  // made the real way: oxidise uranium in MI's Chemical Reactor.
  event.custom({
    type: 'modern_industrialization:chemical_reactor',
    eu: 16,
    duration: 200,
    item_inputs: [{ item: 'modern_industrialization:uranium_dust', amount: 1 }],
    fluid_inputs: [{ fluid: 'modern_industrialization:oxygen', amount: 500 }],
    item_outputs: [{ item: 'powah:uraninite', amount: 1 }]
  }).id('kubejs:phase4/powah/uraninite_from_uranium_oxidation')

  // --- T4: petrochemistry → AE2 --------------------------------------------------------------
  // AE2 sits on top of petrochemistry. The Inscriber (needed for every AE2 processor) is built
  // on an MI Turbo (HV) hull, and the ME Controller needs an MI digital circuit (polyethylene).
  reshape('ae2:network/blocks/inscribers', 'ae2:inscriber',
    ['aba', 'cha', 'aba'],
    { a: '#c:ingots/iron', b: 'minecraft:piston', c: '#c:ingots/copper',
      h: 'modern_industrialization:turbo_machine_hull' })
  reshape('ae2:network/blocks/controller', 'ae2:controller',
    ['ada', 'bcb', 'aba'],
    { a: 'ae2:smooth_sky_stone_block', b: 'ae2:fluix_crystal', c: 'ae2:engineering_processor',
      d: 'modern_industrialization:digital_circuit' })

  // --- T5: materials science (EV) ----------------------------------------------------------
  // Wireless power: the Flux Core needs an MI processing unit instead of an Eye of Ender.
  reshape('fluxnetworks:flux_core', 'fluxnetworks:flux_core',
    ['fof', 'opo', 'fof'],
    { f: 'fluxnetworks:flux_dust', o: 'minecraft:obsidian', p: 'modern_industrialization:processing_unit' })

  // Alchemistry transmutation completes the periodic table at T5. Both chamber controllers need
  // an MI processing unit; fusion also keeps its Nether Star.
  reshape('alchemistry:fission_chamber_controller', 'alchemistry:fission_chamber_controller',
    ['ICI', 'GPR', 'ICI'],
    { I: 'minecraft:iron_ingot', C: 'alchemistry:reactor_casing', G: 'minecraft:glass',
      P: 'modern_industrialization:processing_unit', R: 'minecraft:redstone' })
  reshape('alchemistry:fusion_chamber_controller', 'alchemistry:fusion_chamber_controller',
    ['IPI', 'GSR', 'ICI'],
    { I: 'minecraft:iron_ingot', C: 'alchemistry:reactor_casing', G: 'minecraft:glass',
      S: 'minecraft:nether_star', P: 'modern_industrialization:processing_unit', R: 'minecraft:redstone' })

  // --- T5 → T6: leaving the planet ----------------------------------------------------------
  // Ad Astra's NASA Workbench (builds every rocket) needs an MI Highly Advanced (EV) hull.
  reshape('ad_astra:nasa_workbench', 'ad_astra:nasa_workbench',
    ['|#|', 'THT', '#B#'],
    { '#': '#ad_astra:steel_plates', B: '#ad_astra:steel_blocks', T: 'minecraft:redstone_torch',
      '|': '#ad_astra:iron_rods', H: 'modern_industrialization:highly_advanced_machine_hull' })

  // Not changed on purpose:
  //  - pylons:infusion_pylon already needs Nether materials (quartz, blackstone): flight after the Nether.
  //  - justdirethings:upgrade_flight already needs End Crystals: portable flight after the End.
})
