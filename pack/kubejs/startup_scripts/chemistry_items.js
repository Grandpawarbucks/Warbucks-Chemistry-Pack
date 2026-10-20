// Custom items for the Monifactory-inspired mechanics (2026-10-18).
// Textures reuse vanilla art so no new assets are needed; names make each item's role clear.

StartupEvents.registry('item', event => {
  // --- Platinum-group metals line (see server_scripts/phase4_chemistry.js) ---
  // Real source: PGMs are a byproduct of nickel and copper refining (e.g. the Sudbury mines).
  event.create('pgm_sludge').displayName('Platinum Group Sludge').texture('minecraft:item/gunpowder')
  // Dissolving the sludge in aqua regia gives chloroplatinic acid, H₂PtCl₆ (orange-red crystals).
  event.create('chloroplatinic_acid').displayName('Chloroplatinic Acid').texture('minecraft:item/glowstone_dust')
  // Iridium, osmium, rhodium and ruthenium don't dissolve in aqua regia: they stay as residue.
  event.create('pgm_residue').displayName('Insoluble PGM Residue').texture('minecraft:item/clay_ball')
  // Ammonium chloride precipitates the platinum as (NH₄)₂PtCl₆, which is calcined to pure platinum.
  event.create('ammonium_hexachloroplatinate').displayName('Ammonium Hexachloroplatinate').texture('minecraft:item/sugar')

  // --- Demigod Tokens: RETIRED 2026-10-20 ("Coins replace tokens": quests pay Wardaddy Market coins). Still
  // registered so old ids resolve (harmless; no recipe, quest or loot table uses them any more).
  event.create('demigod_token').displayName('Demigod Token').rarity('uncommon') // texture: kubejs/assets/kubejs/textures/item/demigod_token.png
  event.create('greater_demigod_token').displayName('Greater Demigod Token').rarity('rare') // texture: greater_demigod_token.png

  // --- Endgame energy cores (the Monifactory "energy core" idea, chemistry flavoured) ---
  event.create('energy_core_empty').displayName('Empty Energy Core').texture('minecraft:item/ender_eye').maxStackSize(16)
  event.create('energy_core').displayName('Charged Energy Core').texture('minecraft:item/ender_eye').rarity('rare').maxStackSize(16)
  event.create('antimatter_core').displayName('Antimatter Core').texture('minecraft:item/nether_star').rarity('epic').maxStackSize(16)

  // --- The capstone: needs an intermediate from every tier ---
  event.create('seed_of_a_new_world').displayName('Seed of a New World').texture('minecraft:item/heart_of_the_sea').rarity('epic').maxStackSize(1)
})
