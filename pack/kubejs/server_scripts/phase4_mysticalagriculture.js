// Phase 4: Mystical Agriculture gating (user choice "option 1", 2026-10-18)
// Farming resources should be a convenience, not a way around the chemistry progression:
//  1. Crops whose resource IS a chemistry milestone can't be farmed (their seed recipes are removed).
//  2. Tier 3/4/5 seeds need an MI circuit of the matching voltage tier (LV/MV/HV), as a one-time
//     cost per seed type (seeds multiply themselves once planted).
// Seeds are only made on the Infusion Altar in this pack (seedCraftingRecipes = false), but the
// crafting-table variants are removed too in case that config is ever flipped.

// Resources that gate a tier: fissile/nuclear chain, Mekanism-only minerals, refined Mekanism
// products, and the MI materials that define LV-EV (steel, aluminum, silicon, platinum, iridium).
const BLOCKED_CROPS = [
  'uranium', 'uraninite', 'osmium', 'fluorite', 'silicon', 'steel', 'aluminum', 'graphite',
  'platinum', 'iridium', 'refined_obsidian', 'refined_glowstone'
]

// Crop tiers 3-5 from Mystical Agriculture's source (lib/ModCrops.java, branch 1.21).
// Crops for mods that aren't in the pack are listed too; their recipes simply don't load.
const TIER_CIRCUIT = {}
const tier = (circuit, crops) => crops.forEach(c => TIER_CIRCUIT[c] = circuit)
tier('modern_industrialization:analog_circuit', [ // Tier 3 (Tertium) -> LV
  'iron', 'copper', 'nether_quartz', 'glowstone', 'redstone', 'obsidian', 'prismarine', 'sculk',
  'zombie', 'skeleton', 'creeper', 'spider', 'phantom', 'rabbit', 'tin', 'bronze', 'zinc', 'brass',
  'silver', 'lead', 'graphite', 'blizz', 'blitz', 'basalz', 'amethyst_bronze', 'slimesteel',
  'pig_iron', 'copper_alloy', 'redstone_alloy', 'conductive_alloy', 'manasteel', 'steeleaf',
  'ironwood', 'aquamarine', 'sky_stone', 'certus_quartz', 'quartz_enriched_iron'])
tier('modern_industrialization:electronic_circuit', [ // Tier 4 (Imperium) -> MV
  'gold', 'lapis_lazuli', 'end', 'experience', 'breeze', 'blaze', 'ghast', 'enderman', 'steel',
  'nickel', 'constantan', 'electrum', 'invar', 'uranium', 'ruby', 'sapphire', 'peridot', 'soulium',
  'signalum', 'lumium', 'flux_infused_ingot', 'hop_graphite', 'cobalt', 'rose_gold', 'soularium',
  'dark_steel', 'pulsating_alloy', 'energetic_alloy', 'elementium', 'osmium', 'fluorite',
  'refined_glowstone', 'refined_obsidian', 'knightmetal', 'fiery_ingot', 'starmetal',
  'compressed_iron', 'fluix', 'energized_steel', 'blazing_crystal'])
tier('modern_industrialization:digital_circuit', [ // Tier 5 (Supremium) -> HV
  'diamond', 'emerald', 'netherite', 'wither_skeleton', 'platinum', 'iridium', 'enderium',
  'flux_infused_gem', 'manyullyn', 'queens_slime', 'hepatizon', 'vibrant_alloy', 'end_steel',
  'terrasteel', 'rock_crystal', 'draconium', 'yellorium', 'cyanite', 'niotic_crystal',
  'spirited_crystal', 'uraninite'])

ServerEvents.recipes(event => {
  // 1. Blocked crops: no seed recipe at all.
  BLOCKED_CROPS.forEach(crop => {
    event.remove({ id: `mysticalagriculture:seed/infusion/${crop}` })
    event.remove({ id: `mysticalagriculture:seed/crafting/${crop}` })
  })

  // 2. Tier gate: on tier 3-5 seed recipes, the last of the 8 altar ingredients (an essence)
  //    becomes the matching MI circuit. Recipe ids are mysticalagriculture:seed/infusion/<crop>.
  let gated = 0
  event.findRecipes({ type: 'mysticalagriculture:infusion', id: /^mysticalagriculture:seed\/infusion\// }).forEach(r => {
    const id = String(r.getId())
    const crop = id.substring(id.lastIndexOf('/') + 1)
    const circuit = TIER_CIRCUIT[crop]
    if (!circuit || BLOCKED_CROPS.indexOf(crop) >= 0) return
    const json = JSON.parse(String(r.json))
    json.ingredients[json.ingredients.length - 1] = { item: circuit }
    event.remove({ id: id })
    event.custom(json).id('kubejs:phase4/mysticalagriculture/seed/' + crop)
    gated++
  })
  console.info(`[phase4] Mystical Agriculture: ${gated} tier 3-5 seed recipes gated behind MI circuits; ${BLOCKED_CROPS.length} crops blocked`)
})
