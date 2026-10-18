// Balance fixes found while writing quest book v8 (2026-10-18).

ServerEvents.recipes(event => {
  // --- Mekanism ore chain at MV --------------------------------------------------------------
  // The design (docs/PROGRESSION.md, quest chapter T4) puts Mekanism's 4x (HCl injection) and 5x
  // (H2SO4 dissolution, washing, crystallizing) ore processing at MV, where you first make those
  // acids. But Mekanism's own recipes need Elite (HV) / Ultimate (EV) control circuits for these
  // machines, and in this pack those circuits need MI digital circuits / processing units
  // (phase4_integration.js). Lower these four machines to Advanced (MV) circuits; the acids are
  // still the real gate.
  const circuitTo = (machine, from) =>
    event.findRecipes({ id: `mekanism:${machine}` }).forEach(r => {
      const json = JSON.parse(String(r.json))
      Object.keys(json.key).forEach(k => {
        if (json.key[k].tag === `c:circuits/${from}`) json.key[k] = { tag: 'c:circuits/advanced' }
      })
      event.remove({ id: `mekanism:${machine}` })
      event.custom(json).id(`kubejs:phase5/mekanism/${machine}`)
      console.info(`[phase5] ${machine}: ${JSON.stringify(json.key)}`)
    })
  circuitTo('chemical_injection_chamber', 'elite')
  circuitTo('chemical_dissolution_chamber', 'ultimate')
  circuitTo('chemical_washer', 'ultimate')
  circuitTo('chemical_crystallizer', 'ultimate')

  // --- Reliquary: no free metals ---------------------------------------------------------------
  // The Alkahestry Tome doubles items for redstone charge. For metals, gems and Nether Stars that
  // skips the chemistry tiers the same way EMC would (see ProjectE lite, custom_emc.json), so those
  // recipes go. Building materials (dirt, sand, gravel, clay, obsidian...) stay.
  ;['iron_ingot', 'gold_ingot', 'copper_ingot', 'tin_ingot', 'silver_ingot', 'steel_ingot',
    'diamond', 'emerald', 'lapis_lazuli', 'nether_star']
    .forEach(n => event.remove({ id: `reliquary:alkahestry/crafting/${n}` }))
})

// --- Starting inventory (2026-10-18, user request) ---------------------------------------------
// New players start with an empty inventory: the join gifts are switched off in pack/config
// (MI guidebook, Ars Worn Notebook, Silent Gear material book + blueprint package, Advanced
// Peripherals manual). All of them are craftable, but the Advanced Peripherals manual's own recipe
// uses the pre-1.21 format and never loads, so it gets a working one: book + wired modem.
ServerEvents.recipes(event => {
  event.custom({
    type: 'minecraft:crafting_shapeless',
    category: 'misc',
    ingredients: [{ item: 'minecraft:book' }, { item: 'computercraft:wired_modem' }],
    result: { id: 'patchouli:guide_book', components: { 'patchouli:book': 'advancedperipherals:manual' } }
  }).id('kubejs:phase5/advancedperipherals_manual')
})
