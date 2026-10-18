// Create as the EARLY MECHANICAL TIER (user decision 2026-10-18; see CLAUDE.md).
// Create runs alongside MI's steam age, but it follows the same rules as every other mod:
//   - Ore processing before acids: <= 2x per ore block, <= 1.5x per raw ore (docs/PROGRESSION.md §6).
//   - Making electricity (FE) from rotation needs an MI LV analog circuit.
//   - New Age's thorium reactor is a nuclear tier, so it needs an MI EV processing unit.
// Same remove-and-re-add pattern as phase3_compat.js (recipes re-added under kubejs:create/...).

ServerEvents.recipes(event => {
  const readd = (r, json, tag) => {
    const id = String(r.getId())
    event.remove({ id: id })
    event.custom(json).id(`kubejs:create/${tag}/` + id.replace(':', '/'))
  }

  // --- 1. Crushing-wheel ore yields --------------------------------------------------------
  // Create's ore-block recipes give 1 crushed ore + 75% (1.75x), but deepslate ores give
  // 2 + 25% (2.25x). Any crushing recipe whose input is an ore and whose expected crushed-ore
  // output is above 2 is trimmed to exactly 2. Raw-ore crushing (1 crushed -> 1 ingot) is unchanged.
  let capped = 0
  event.findRecipes({ type: 'create:crushing' }).forEach(r => {
    const json = JSON.parse(String(r.json))
    const ing = JSON.stringify(json.ingredients || [])
    if (!/_ore"|c:ores\//.test(ing)) return
    const isCrushed = res => String(res.id || '').indexOf('crushed_raw_') >= 0
    const expected = json.results.filter(isCrushed)
      .reduce((sum, res) => sum + (res.count || 1) * (res.chance == null ? 1 : res.chance), 0)
    if (expected <= 2) return
    const crushedId = json.results.find(isCrushed).id
    json.results = [{ id: crushedId, count: 2 }].concat(json.results.filter(res => !isCrushed(res)))
    readd(r, json, 'ore_cap')
    capped++
  })
  console.info(`[phase4] Create: ${capped} ore-crushing recipes capped at 2x`)

  // --- 2. Rotation -> electricity needs LV circuitry ---------------------------------------
  // Crafts & Additions Alternator: its centre iron rod becomes an MI analog circuit.
  event.findRecipes({ id: 'createaddition:mechanical_crafting/alternator' }).forEach(r => {
    const json = JSON.parse(String(r.json))
    json.key.R = { item: 'modern_industrialization:analog_circuit' }
    readd(r, json, 'power')
  })
  // New Age Generator Coil: its andesite-alloy core block becomes an MI analog circuit.
  event.findRecipes({ id: 'create_new_age:shaped/generator_coil' }).forEach(r => {
    const json = JSON.parse(String(r.json))
    json.key.A = { item: 'modern_industrialization:analog_circuit' }
    readd(r, json, 'power')
  })

  // --- 3. New Age's thorium reactor is a nuclear (EV) tier -------------------------------
  // Reactor rods: the gold plates in the middle of the top and bottom rows become MI processing units.
  event.findRecipes({ id: 'create_new_age:mechanical_crafting/reactor_rod' }).forEach(r => {
    const json = JSON.parse(String(r.json))
    json.pattern = ['CPUPC', ' GFG ', ' GFG ', 'CPUPC']
    json.key.U = { item: 'modern_industrialization:processing_unit' }
    readd(r, json, 'nuclear')
  })
})
