// Monifactory-inspired chemistry (user picks, 2026-10-18): ore byproducts, processing chains,
// energy cores and the capstone (the Demigod Token shop of §5 is retired). Custom items live in
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
  // 5. (retired 2026-10-20, user: "Coins replace tokens") The Demigod Token shop recipes are gone: quests pay
  // Wardaddy Market coins and the Market (Market key / /market) is the only shop. Prices: tools/build_market_prices.py.
  // The kubejs:demigod_token items stay registered (startup_scripts/chemistry_items.js) but nothing uses them.
  // ==========================================================================================
})
