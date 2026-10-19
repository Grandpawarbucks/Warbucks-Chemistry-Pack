// Phase 5 harvest tiers for late ores (docs/research/tools_harvest_plan.md section 5, approved 2026-10-18).
// MI ships its late metals as stone tier and Ad Astra's space metals have no tier at all, so the tier
// ladder stopped meaning anything after iron. A block asks for a tier with a needs_* tag; a tool refuses
// every block in its incorrect_for_* tag. Vanilla's incorrect_for_wooden/stone/iron tags already pull in
// #minecraft:needs_iron_tool and #minecraft:needs_diamond_tool, and NeoForge 21.1.262 adds
// #neoforge:needs_netherite_tool to every incorrect_for_* tag below netherite, so tagging is enough.
//
// Real hardness agrees roughly (Mohs): wolframite ~4.5, ilmenite/rutile 5.5-6.5, sperrylite (PtAs2) 6-7,
// native iridium/osmiridium ~6-7, versus ~2.5-4 for galena, sphalerite and chalcopyrite.
//   iron tier     MI titanium, tungsten, platinum, iridium ores; Ad Astra desh (Moon)
//   diamond tier  Ad Astra ostrum (Mars)
//   netherite     Ad Astra calorite (Venus)
// The Mekanism steel paxel (T1) is already diamond tier, so this mostly blocks bronze-age shortcuts.

ServerEvents.tags('block', event => {
  const ironOres = [
    'modern_industrialization:titanium_ore',
    'modern_industrialization:tungsten_ore',
    'modern_industrialization:deepslate_tungsten_ore',
    'modern_industrialization:platinum_ore',
    'modern_industrialization:iridium_ore',
    'ad_astra:moon_desh_ore',
    'ad_astra:deepslate_desh_ore'
  ]
  const diamondOres = ['ad_astra:mars_ostrum_ore', 'ad_astra:deepslate_ostrum_ore']
  const netheriteOres = ['ad_astra:venus_calorite_ore', 'ad_astra:deepslate_calorite_ore']
  const all = ironOres.concat(diamondOres, netheriteOres)

  // MI lists its ores in needs_stone_tool; take them out so each ore has exactly one tier tag.
  event.remove('minecraft:needs_stone_tool', all)
  event.add('minecraft:needs_iron_tool', ironOres)
  event.add('minecraft:needs_diamond_tool', diamondOres)
  event.add('neoforge:needs_netherite_tool', netheriteOres)
  // Both mods already list these as pickaxe blocks; adding again is harmless and keeps it explicit.
  event.add('minecraft:mineable/pickaxe', all)
})
