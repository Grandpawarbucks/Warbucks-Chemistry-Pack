// Monifactory-inspired chemistry (user picks, 2026-10-18): ore byproducts, processing chains,
// energy cores, Demigod Tokens, and the capstone. Custom items live in
// startup_scripts/chemistry_items.js. Fluid ids were checked on the running server:
// ChemLib fluids are "<name>_fluid" (chemlib:nitric_acid_fluid, chemlib:ammonia_fluid).

ServerEvents.recipes(event => {
  const MI = 'modern_industrialization'
  const mi = (type, json, id) => event.custom(Object.assign({ type: `${MI}:${type}` }, json)).id(`kubejs:chem/${id}`)

  // ==========================================================================================
  // 1. ORE BYPRODUCTS
  // Mekanism's ore chain ends in dirty dust, which normally goes into the Enrichment Chamber
  // (1 dirty dust -> 1 dust). Mekanism machines allow only one output, so byproducts come from MI's
  // Centrifuge instead: same main dust, plus a chance at a metal that really occurs alongside it.
  // ==========================================================================================
  const byproduct = (metal, main, bonus, chance, why) =>
    mi('centrifuge', {
      eu: 16, duration: 100,
      item_inputs: [{ item: `mekanism:dirty_dust_${metal}`, amount: 1 }],
      item_outputs: [{ item: main, amount: 1 }, { item: bonus, amount: 1, probability: chance }]
    }, `byproduct/${metal}`)
  byproduct('iron', `${MI}:iron_dust`, `${MI}:nickel_dust`, 0.10)        // iron-nickel ores (pentlandite)
  byproduct('copper', `${MI}:copper_dust`, `${MI}:gold_dust`, 0.05)      // gold is recovered from copper refining
  byproduct('gold', `${MI}:gold_dust`, `${MI}:silver_dust`, 0.10)        // native gold is alloyed with silver (electrum)
  byproduct('lead', `${MI}:lead_dust`, `${MI}:silver_dust`, 0.15)        // galena (PbS) is the main source of silver
  byproduct('tin', `${MI}:tin_dust`, `${MI}:tungsten_dust`, 0.05)        // cassiterite often occurs with wolframite
  byproduct('osmium', 'mekanism:dust_osmium', `${MI}:iridium_dust`, 0.03) // osmiridium: osmium and iridium occur together
  byproduct('uranium', `${MI}:uranium_dust`, `${MI}:lead_dust`, 0.10)    // uranium decays into lead

  // ==========================================================================================
  // 2. PROCESSING CHAINS
  // ==========================================================================================
  // Haber-Bosch: N₂ + 3H₂ → 2NH₃. Ammonia feeds fertiliser, nitric acid and ammonium salts.
  mi('chemical_reactor', {
    eu: 16, duration: 300,
    fluid_inputs: [{ fluid: `${MI}:nitrogen`, amount: 1000 }, { fluid: `${MI}:hydrogen`, amount: 3000 }],
    fluid_outputs: [{ fluid: 'chemlib:ammonia_fluid', amount: 2000 }]
  }, 'haber_bosch')

  // Ostwald process: NH₃ + 2O₂ → HNO₃ + H₂O.
  mi('chemical_reactor', {
    eu: 16, duration: 300,
    fluid_inputs: [{ fluid: 'chemlib:ammonia_fluid', amount: 1000 }, { fluid: `${MI}:oxygen`, amount: 2000 }],
    fluid_outputs: [{ fluid: 'chemlib:nitric_acid_fluid', amount: 1000 }, { fluid: 'minecraft:water', amount: 1000 }]
  }, 'ostwald')

  // NH₃ + HCl → NH₄Cl (ammonium chloride, the platinum precipitant).
  mi('chemical_reactor', {
    eu: 8, duration: 100,
    fluid_inputs: [{ fluid: 'chemlib:ammonia_fluid', amount: 1000 }, { fluid: `${MI}:hydrochloric_acid`, amount: 1000 }],
    item_outputs: [{ item: 'chemlib:ammonium_chloride_dust', amount: 1 }]
  }, 'ammonium_chloride')

  // --- Platinum-group metals (PGM) line --------------------------------------------------
  // Step 1: electrolytic refining of nickel and copper leaves PGM-rich anode sludge.
  ;['nickel', 'copper'].forEach(metal => mi('electrolyzer', {
    eu: 32, duration: 200,
    item_inputs: [{ tag: `c:dusts/${metal}`, amount: 4 }],
    item_outputs: [{ item: `${MI}:${metal}_dust`, amount: 4 }, { item: 'kubejs:pgm_sludge', amount: 1, probability: 0.25 }]
  }, `pgm/sludge_from_${metal}`))

  // Step 2: dissolve in aqua regia (3 HCl : 1 HNO₃). Platinum goes into solution as H₂PtCl₆;
  // iridium, osmium, rhodium and ruthenium don't dissolve and stay behind as residue.
  mi('chemical_reactor', {
    eu: 32, duration: 400,
    item_inputs: [{ item: 'kubejs:pgm_sludge', amount: 4 }],
    fluid_inputs: [{ fluid: `${MI}:hydrochloric_acid`, amount: 3000 }, { fluid: 'chemlib:nitric_acid_fluid', amount: 1000 }],
    item_outputs: [{ item: 'kubejs:chloroplatinic_acid', amount: 2 }, { item: 'kubejs:pgm_residue', amount: 1 }]
  }, 'pgm/aqua_regia')

  // Step 3: ammonium chloride precipitates ammonium hexachloroplatinate, (NH₄)₂PtCl₆.
  mi('chemical_reactor', {
    eu: 32, duration: 200,
    item_inputs: [{ item: 'kubejs:chloroplatinic_acid', amount: 1 }, { item: 'chemlib:ammonium_chloride_dust', amount: 2 }],
    item_outputs: [{ item: 'kubejs:ammonium_hexachloroplatinate', amount: 1 }]
  }, 'pgm/precipitate')

  // Step 4: calcining (heating) it drives off NH₃ and HCl and leaves pure platinum.
  mi('blast_furnace', {
    eu: 64, duration: 400,
    item_inputs: [{ item: 'kubejs:ammonium_hexachloroplatinate', amount: 2 }],
    item_outputs: [{ item: `${MI}:platinum_dust`, amount: 1 }]
  }, 'pgm/calcine')

  // Step 5: separate the insoluble residue into the rare PGMs.
  mi('centrifuge', {
    eu: 32, duration: 400,
    item_inputs: [{ item: 'kubejs:pgm_residue', amount: 1 }],
    item_outputs: [
      { item: `${MI}:iridium_dust`, amount: 1, probability: 0.30 },
      { item: 'mekanism:dust_osmium', amount: 1, probability: 0.30 },
      { item: 'chemlib:rhodium_dust', amount: 1, probability: 0.20 },
      { item: 'chemlib:ruthenium_dust', amount: 1, probability: 0.20 }
    ]
  }, 'pgm/residue')

  // ==========================================================================================
  // 3. ENERGY CORES (endgame, Monifactory's "energy core" idea)
  // A stainless-steel shell is charged with a huge amount of EU in MI's Assembler, then
  // upgraded with antimatter. Antimatter Cores are the heart of the capstone.
  // ==========================================================================================
  event.shaped('kubejs:energy_core_empty', ['SPS', 'PCP', 'SPS'], {
    S: `${MI}:stainless_steel_plate`, P: 'mekanism:pellet_polonium', C: `${MI}:processing_unit`
  }).id('kubejs:chem/energy_core_empty')
  mi('assembler', {
    eu: 512, duration: 6000, // about 3 million EU stored in the core
    item_inputs: [{ item: 'kubejs:energy_core_empty', amount: 1 }],
    item_outputs: [{ item: 'kubejs:energy_core', amount: 1 }]
  }, 'energy_core_charge')
  mi('assembler', {
    eu: 2048, duration: 6000,
    item_inputs: [{ item: 'kubejs:energy_core', amount: 1 }, { item: 'mekanism:pellet_antimatter', amount: 4 },
                  { item: `${MI}:quantum_circuit`, amount: 1 }],
    item_outputs: [{ item: 'kubejs:antimatter_core', amount: 1 }]
  }, 'antimatter_core')

  // ==========================================================================================
  // 4. CAPSTONE: Seed of a New World (9x9, Extended Crafting Ultimate Table)
  // One intermediate from every tier: coke (T1), synthesized water and hydrogen (Alchemistry),
  // sulfuric acid (T3), polyethylene (T4), hydrofluoric acid (fluorite + H2SO4, the uranium-
  // enrichment acid of T5), processing units (T5), oganesson (full periodic
  // table), plutonium and polonium (nuclear), and eight Antimatter Cores (T7).
  // ==========================================================================================
  event.custom({
    type: 'extendedcrafting:shaped_table',
    pattern: [
      'KWSFAFSWK',
      'WHUOEOUHW',
      'SUCPXPCUS',
      'POPNANPOP',
      'AEXAZAXEA',
      'POPNANPOP',
      'SUCPXPCUS',
      'WHUOEOUHW',
      'KWSFAFSWK'
    ],
    key: {
      K: { item: `${MI}:coke` },
      W: { item: 'chemlib:water' },
      H: { item: 'chemlib:hydrogen' },
      S: { tag: 'warbucks:sulfuric_acid_buckets' }, // any H2SO4 bucket (MI, Mekanism, ChemLib)
      P: { item: `${MI}:polyethylene_bucket` },
      F: { item: 'mekanism:hydrofluoric_acid_bucket' },
      U: { item: `${MI}:processing_unit` },
      O: { item: 'chemlib:oganesson' },
      E: { item: 'mekanism:pellet_plutonium' },
      N: { item: 'mekanism:pellet_polonium' },
      C: { item: `${MI}:stainless_steel_plate` },
      X: { item: 'minecraft:nether_star' },
      A: { item: 'kubejs:antimatter_core' },
      Z: { item: 'minecraft:dragon_egg' }
    },
    result: { id: 'kubejs:seed_of_a_new_world' }
  }).id('kubejs:chem/seed_of_a_new_world')

  // ==========================================================================================
  // 5. DEMIGOD TOKEN SHOP (quest rewards; convenience only, never tier-skipping)
  // Rules (Phase 5 token overhaul): the shop sells raw feedstocks and comforts, never machines,
  // circuits or anything that skips a tier. Three price bands:
  //   small  1-3 tokens        everyday supplies
  //   medium 4-8 tokens        raw ores and mob drops you would otherwise farm
  //   large  Greater Tokens    rare comforts (1 Greater Token = 9 Demigod Tokens)
  // Every trade is a shapeless recipe; search "Demigod Token" in JEI to see them all.
  // ==========================================================================================
  const T = 'kubejs:demigod_token', G = 'kubejs:greater_demigod_token'
  const shop = (cost, result, count, name, coin) =>
    event.shapeless(Item.of(result, count), Array(cost).fill(coin || T)).id(`kubejs:shop/${name}`)
  // Change: 9 tokens <-> 1 Greater Token.
  event.shapeless(G, Array(9).fill(T)).id('kubejs:shop/greater_token')
  event.shapeless(Item.of(T, 9), [G]).id('kubejs:shop/greater_token_change')

  // Small band (1-3)
  shop(1, 'minecraft:torch', 32, 'torches')
  shop(1, 'minecraft:bread', 16, 'bread')
  shop(1, 'minecraft:experience_bottle', 8, 'xp')
  shop(1, 'minecraft:bone_meal', 32, 'bone_meal')
  shop(1, 'minecraft:sand', 64, 'sand')
  shop(1, 'minecraft:gravel', 64, 'gravel')
  shop(1, 'minecraft:clay_ball', 32, 'clay')
  shop(2, 'minecraft:iron_ingot', 16, 'iron')
  shop(2, `${MI}:coke`, 16, 'coke')
  shop(2, `${MI}:rubber_sheet`, 16, 'rubber')
  shop(2, `${MI}:fire_clay_dust`, 16, 'fire_clay')
  shop(2, `${MI}:salt_dust`, 32, 'salt')
  shop(2, 'minecraft:string', 16, 'string')
  shop(2, 'minecraft:leather', 16, 'leather')
  shop(2, 'comforts:sleeping_bag_white', 1, 'sleeping_bag')
  shop(3, 'mekanism:ingot_osmium', 8, 'osmium')
  shop(3, 'sophisticatedbackpacks:upgrade_base', 2, 'backpack_upgrade_base')
  shop(3, 'minecraft:gunpowder', 16, 'gunpowder')
  shop(3, 'minecraft:slime_ball', 16, 'slime')
  shop(3, 'minecraft:redstone', 32, 'redstone')
  shop(3, 'minecraft:lapis_lazuli', 16, 'lapis')
  // Medium band (4-8): raw ores (still need your own processing line) and mob drops
  shop(4, 'waystones:warp_stone', 1, 'warp_stone')
  shop(4, 'minecraft:raw_copper', 32, 'raw_copper')
  shop(4, `${MI}:raw_tin`, 16, 'raw_tin')
  shop(4, `${MI}:raw_lead`, 16, 'raw_lead')
  shop(4, `${MI}:bauxite_dust`, 16, 'bauxite')
  shop(4, 'minecraft:quartz', 32, 'quartz')
  shop(4, 'minecraft:glowstone_dust', 32, 'glowstone')
  shop(5, `${MI}:raw_nickel`, 16, 'raw_nickel')
  shop(5, 'minecraft:ender_pearl', 8, 'ender_pearls')
  shop(5, 'minecraft:phantom_membrane', 4, 'phantom_membrane')
  shop(5, 'minecraft:amethyst_shard', 16, 'amethyst')
  shop(6, 'minecraft:blaze_rod', 8, 'blaze_rods')
  shop(6, 'minecraft:ghast_tear', 4, 'ghast_tears')
  shop(6, 'ae2:certus_quartz_crystal', 16, 'certus')
  shop(6, 'ars_nouveau:source_gem', 8, 'source_gems')
  shop(7, `${MI}:raw_titanium`, 8, 'raw_titanium')
  shop(7, 'minecraft:name_tag', 2, 'name_tags')
  shop(8, `${MI}:raw_tungsten`, 8, 'raw_tungsten')
  shop(8, 'minecraft:prismarine_shard', 32, 'prismarine')
  // Large band (Greater Tokens)
  shop(1, 'minecraft:golden_apple', 4, 'golden_apples', G)
  shop(1, 'minecraft:diamond', 4, 'diamonds', G)
  shop(1, 'minecraft:emerald', 16, 'emeralds', G)
  shop(1, 'minecraft:saddle', 1, 'saddle', G)
  shop(2, 'minecraft:shulker_shell', 2, 'shulker_shells', G)
  shop(2, 'minecraft:heart_of_the_sea', 1, 'heart_of_the_sea', G)
  shop(2, 'minecraft:netherite_scrap', 1, 'netherite_scrap', G)
  shop(3, 'minecraft:totem_of_undying', 1, 'totem', G)
  shop(3, 'minecraft:echo_shard', 4, 'echo_shards', G)
  shop(4, 'minecraft:enchanted_golden_apple', 1, 'notch_apple', G)
})
