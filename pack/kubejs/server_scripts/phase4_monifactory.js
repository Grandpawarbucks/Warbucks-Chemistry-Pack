// Monifactory-inspired mods, hooked into MI's chemistry tiers (added 2026-10-18).
// Same pattern as phase4_integration.js: remove the original recipe id, re-add it under
// kubejs:phase4/... with one ingredient swapped for the matching MI circuit.

ServerEvents.recipes(event => {
  const reshape = (originalId, result, pattern, key) => {
    event.remove({ id: originalId })
    event.shaped(result, pattern, key).id('kubejs:phase4/' + originalId.replace(':', '/'))
  }

  // --- Hostile Neural Networks ---------------------------------------------------------------
  // Collecting mob data (Deep Learner, data models) stays cheap so players can start early.
  // Simulating drops is powerful, so both machines that do it need an MV electronic circuit
  // (aluminum chemistry) in place of the comparator.
  reshape('hostilenetworks:sim_chamber', 'hostilenetworks:sim_chamber',
    [' G ', 'EOE', 'MCM'],
    { G: '#c:glass_panes', E: 'minecraft:ender_pearl', O: '#c:obsidians', M: '#c:gems/lapis',
      C: 'modern_industrialization:electronic_circuit' })
  reshape('hostilenetworks:loot_fabricator', 'hostilenetworks:loot_fabricator',
    [' I ', 'GOG', 'NCN'],
    { I: '#c:ingots/netherite', G: '#c:gems/diamond', O: '#c:obsidians', N: '#c:ingots/gold',
      C: 'modern_industrialization:electronic_circuit' })

  // --- Extended Crafting ---------------------------------------------------------------------
  // The basic 3x3 table stays as-is. Each bigger table swaps its black iron slate for the next
  // MI circuit, so 5x5 / 7x7 / 9x9 crafting unlocks at MV / HV / EV.
  reshape('extendedcrafting:advanced_table', 'extendedcrafting:advanced_table',
    ['BAB', 'CIC', 'BSB'],
    { I: '#c:storage_blocks/gold', C: ['extendedcrafting:basic_table', 'extendedcrafting:basic_auto_table'],
      B: 'extendedcrafting:advanced_component', A: 'extendedcrafting:advanced_catalyst',
      S: 'modern_industrialization:electronic_circuit' })
  reshape('extendedcrafting:elite_table', 'extendedcrafting:elite_table',
    ['BAB', 'CIC', 'BSB'],
    { I: '#c:storage_blocks/diamond', C: ['extendedcrafting:advanced_table', 'extendedcrafting:advanced_auto_table'],
      B: 'extendedcrafting:elite_component', A: 'extendedcrafting:elite_catalyst',
      S: 'modern_industrialization:digital_circuit' })
  reshape('extendedcrafting:ultimate_table', 'extendedcrafting:ultimate_table',
    ['BAB', 'CIC', 'BSB'],
    { I: '#c:storage_blocks/emerald', C: ['extendedcrafting:elite_table', 'extendedcrafting:elite_auto_table'],
      B: 'extendedcrafting:ultimate_component', A: 'extendedcrafting:ultimate_catalyst',
      S: 'modern_industrialization:processing_unit' })

  // Not changed on purpose: Packaged Auto (needs AE2, which is already HV-gated), Compact
  // Machines, Cable Facades and TelePastries (convenience, no progression skip).
})
