// Phase 3: compatibility pass
// Unify overlapping systems so each job has one backbone (see docs/PROGRESSION.md §1, pillar 6):
//   - Ore processing: before acids (Mekanism, T3+), no route gives more than 2x per ore block.
//   - Petrochemistry: Modern Industrialization is the refinery; other mods consume its products.
// Ore *generation* duplicates are handled in config/Mekanism/world.toml and
// kubejs/data/powah/neoforge/biome_modifier/*.json. Item duplicates are handled by
// Almost Unified (config/almostunified), with MI as the top-priority mod.

// Run fn on every recipe matching filter: remove it and re-add an edited copy under kubejs:phase3/.
// fn gets the recipe JSON as a plain object and returns the edited object (or null to keep as-is).
function editRecipes(event, filter, fn) {
  let edited = 0
  let sample = null
  event.findRecipes(filter).forEach(r => {
    const id = String(r.getId())
    const json = fn(JSON.parse(String(r.json)), id)
    if (json == null) return
    event.remove({ id: id })
    event.custom(json).id('kubejs:phase3/' + id.replace(':', '/'))
    if (sample == null) sample = id + ' => ' + JSON.stringify(json)
    edited++
  })
  console.info(`[phase3] ${filter.type} ${filter.id} -> edited ${edited} recipes; e.g. ${sample}`)
}

ServerEvents.recipes(event => {
  // --- Ore processing caps (pre-acid tiers max 2x per ore block) ---------------------------

  // MI Macerator: 1 ore -> 3 raw ore. Capped to 2 raw. (Raw ore -> dust stays 1 + 50%.)
  editRecipes(event, { type: 'modern_industrialization:macerator', id: /macerator\/ore_to_raw$/ }, j => {
    j.item_outputs.forEach(o => { if (o.amount > 2) o.amount = 2 })
    return j
  })

  // MI Forge Hammer (steam age, with hammer tool): 1 ore -> 3 raw / 4 dust. Capped to 2.
  editRecipes(event, { type: 'modern_industrialization:forge_hammer', id: /forge_hammer\/ore_to_(raw_metal|dust)_with_tool$/ }, j => {
    if (j.result.count > 2) j.result.count = 2
    return j
  })

  // Integrated Dynamics squeezers: 1 ore -> 2 raw + 75% (manual) or 3 raw + 2x50% (mechanical).
  // Capped to exactly 2 raw: keep the first output, set its count to 2, drop the bonus chances.
  ;['integrateddynamics:squeezer', 'integrateddynamics:mechanical_squeezer'].forEach(type => {
    editRecipes(event, { type: type, id: /squeezer\/ore\// }, j => {
      // The squeezer/ore folder also has sand, gravel, redstone etc.; only cap real ore inputs
      // whose output is a tag (raw metal or gem).
      const input = j.input_item && j.input_item.tag
      const first = j.output_items[0]
      if (!input || !String(input).startsWith('c:ores/') || !first || !first.tag) return null
      // ID stores the count either on the entry or inside the tag object.
      if (first.count != null) first.count = Math.min(first.count, 2)
      else first.tag.count = Math.min(first.tag.count || 1, 2)
      j.output_items = [first]
      return j
    })
  })

  // --- Petrochemistry: MI is the refinery --------------------------------------------------

  // Ad Astra's Fuel Refinery turns any oil (including MI crude oil via #c:crude_oil) straight
  // into rocket fuel, skipping MI's distillation tower. Removed: rockets run on MI diesel,
  // which Ad Astra's #ad_astra:fuel tag already accepts through #c:diesel.
  event.remove({ id: 'ad_astra:refining/fuel_from_refining_oil' })
})

ServerEvents.tags('fluid', event => {
  // Mekanism's HDPE (plastic) recipe takes #c:ethene; MI names the same chemical "ethylene".
  // Tagging MI ethylene as ethene lets MI's distillation tower feed Mekanism plastics.
  event.add('c:ethene', 'modern_industrialization:ethylene')
})
