// Phase 5 chemistry gates (docs/research/chem_tier_audit.md, fixes approved 2026-10-18).
// Each block closes a place where a tier's chemistry could be skipped, or makes a design gate real.
// The aluminium fix lives in phase4_aluminum.js, the Undergarden catalyst in phase4_integration.js and
// the Seed's hydrofluoric acid in phase4_chemistry.js.

ServerEvents.tags('item', event => {
  // --- Silicon: MI's carbothermic silicon is the pack's silicon (see the recipes below) -------------
  // AE2's inscriber (printed silicon) and ExtendedAE read the item tag c:silicon, which AE2 fills
  // with its own ae2:silicon only. MI's ingot joins it so AE2 runs on MI silicon.
  event.add('c:silicon', 'modern_industrialization:silicon_ingot')
})

ServerEvents.recipes(event => {
  // --- Oganesson only from fusion (audit #2) ---------------------------------------------------------
  // Alchemistry dissolved one dragon's breath into 8 xenon + 8 radon + 8 oganesson in the T1
  // Dissolver, so the "complete periodic table" key (ProjectE lite, the Seed) fell out of one dragon
  // fight. Oganesson (element 118) doesn't occur anywhere: every atom ever seen was made in a heavy-ion
  // collider (Ca-48 on Cf-249, 2002) and lived under a millisecond. Keep the noble gases (xenon and
  // radon are at least real, heavy, inert gases), drop the oganesson; it now comes only from the
  // fusion chamber (alchemistry:fusion/*_to_118oganesson, EV).
  event.remove({ id: 'alchemistry:dissolver/dragon_breath' })
  event.custom({
    type: 'alchemistry:dissolver',
    group: 'alchemistry:dissolver',
    input: { ingredient: { item: 'minecraft:dragon_breath' } },
    output: {
      groups: [{ probability: 100.0, results: [
        { count: 8, item: 'chemlib:xenon' },
        { count: 8, item: 'chemlib:radon' }
      ] }],
      rolls: 1,
      weighted: false
    }
  }).id('kubejs:phase5/alchemistry/dissolver/dragon_breath')

  // --- T1 -> LV: the first synthesized compound (audit #4) -------------------------------------------
  // MI's redstone battery is built from battery alloy (Pb-Sb), the real lead-acid grid alloy. A lead-acid
  // cell needs its electrolyte: sulfuric acid, Pb + PbO2 + 2H2SO4 -> 2PbSO4 + 2H2O on discharge.
  // The acid is chemlib:sulfuric_acid from the Alchemistry Combiner (2 H + 1 S + 4 O), all T1 elements:
  // H and O from the Dissolver (sugar -> sucrose -> 22 H + 11 O; ChemLib water -> 2 H + O; sand ->
  // SiO2 -> O), S from gunpowder (8 S). So every LV hull (2 batteries) now needs the Combiner.
  // Crafting: one of the two redstone becomes the acid (the grid is the same 3x3).
  event.remove({ id: 'modern_industrialization:electric_age/battery/lv_battery_asbl' })
  event.shaped('modern_industrialization:redstone_battery', ['cac', 'BrB', 'BHB'], {
    a: '#c:plates/battery_alloy',
    c: 'modern_industrialization:tin_cable',
    B: 'modern_industrialization:battery_alloy_curved_plate',
    r: 'minecraft:redstone',
    H: 'chemlib:sulfuric_acid'
  }).id('kubejs:phase5/modern_industrialization/redstone_battery')
  event.remove({ id: 'modern_industrialization:assembler_generated/electric_age/battery/lv_battery' })
  event.custom({
    type: 'modern_industrialization:assembler',
    eu: 8, duration: 200,
    item_inputs: [
      { tag: 'c:plates/battery_alloy', amount: 1 },
      { item: 'modern_industrialization:tin_cable', amount: 2 },
      { item: 'modern_industrialization:battery_alloy_curved_plate', amount: 4 },
      { item: 'minecraft:redstone', amount: 1 },
      { item: 'chemlib:sulfuric_acid', amount: 1 }
    ],
    item_outputs: [{ item: 'modern_industrialization:redstone_battery', amount: 1 }]
  }).id('kubejs:phase5/modern_industrialization/assembler/redstone_battery')

  // --- Silicon needs carbothermic reduction (audit #7) -----------------------------------------------
  // Silicon metal is made by reducing quartz with carbon in an arc furnace at ~2000 C:
  // SiO2 + 2C -> Si + 2CO. MI does exactly that in the EBF (materials/blast_furnace/silicium_from_quartz).
  // These shortcuts made silicon by crushing sand, by smelting certus dust in a vanilla furnace, or by
  // smelting/enriching ExtendedAE's "quartz blend" (quartz + coal + sand at furnace temperature, which
  // can't reduce SiO2). All removed; AE2 uses MI silicon through c:silicon (tag event above).
  ;['mekanism:compat/ae2/sand_to_silicon', 'mekanism:compat/ae2/certus_quartz_dust_to_silicon',
    'ae2:smelting/silicon_from_certus_quartz_dust', 'ae2:blasting/silicon_from_certus_quartz_dust',
    'extendedae:smelting/quartz_blend', 'extendedae:blasting/quartz_blend', 'extendedae:mek/quartz_blend',
    // the blend has no other use once it can't become silicon
    'extendedae:quartz_blend', 'extendedae:quartz_blend_alt'
  ].forEach(id => event.remove({ id: id }))
  // Two recipes ask for the item ae2:silicon itself (which now has no source of its own): accept any
  // c:silicon instead. Same JSON-edit pattern as phase5_balance.js.
  const toSiliconTag = node => {
    if (Array.isArray(node)) return node.map(toSiliconTag)
    if (node && typeof node === 'object') {
      if (node.item === 'ae2:silicon' && Object.keys(node).length === 1) return { tag: 'c:silicon' }
      Object.keys(node).forEach(k => { node[k] = toSiliconTag(node[k]) })
    }
    return node
  }
  ;['extendedae:silicon_block', 'mysticalagriculture:essence/appliedenergistics2/silicon_press'].forEach(id =>
    event.findRecipes({ id: id }).forEach(r => {
      const json = toSiliconTag(JSON.parse(String(r.json)))
      console.info(`[phase5] ${id}: ${JSON.stringify(json.key)}`)
      event.remove({ id: id })
      event.custom(json).id(`kubejs:phase5/${id.replace(':', '/')}`)
    }))
})
