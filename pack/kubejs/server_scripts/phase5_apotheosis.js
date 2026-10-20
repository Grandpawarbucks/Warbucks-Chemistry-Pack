// Apotheosis tuning modelled on ATM10's (data files from tools/build_apoth_tuning.py in pack/kubejs/data).
// Miner's Fervor is retired like ATM10 does, but without deleting it: Apothic Enchanting lists it in
// #minecraft:non_treasure, and a missing entry makes that tag (and in_enchanting_table, tradeable, on_random_loot,
// on_mob_spawn_equipment, on_traded_equipment and Create's Blaze Enchanter tags built on it) fail to load.
// Taking it out of the tag removes it from enchanting tables, trades and loot while every tag still loads.
ServerEvents.tags('enchantment', event => {
  event.remove('minecraft:non_treasure', 'apothic_enchanting:miners_fervor')
  event.remove('minecraft:in_enchanting_table', 'apothic_enchanting:miners_fervor')
  event.remove('minecraft:tradeable', 'apothic_enchanting:miners_fervor')
  event.remove('minecraft:on_random_loot', 'apothic_enchanting:miners_fervor')
})
