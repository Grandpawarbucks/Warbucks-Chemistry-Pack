// Allthemodium (CurseForge 3.2.1, user decision 2026-10-19; research in docs/research/allthemodium.md).
// Three fictional metals in an exploration side line, fitted to the chemistry tiers:
//   allthemodium  design T3 (LV -> MV)   Deep Dark cave ceilings, The Other       netherite pick
//   vibranium     design T4-T5 (HV)     Nether ceilings, The Other               allthemodium pick
//   unobtainium   design T5-T6 (EV)     End highlands                            vibranium pick
// The Mining dimension keeps its dense ores (user decision). Its worldgen is not touched here.
// Every recipe id below was read from allthemodium-3.2.1_mc_1.21.1.jar (data/allthemodium/recipe/...).
//
// What this file does:
//   1. Refining is chemistry: no furnace or blast-furnace smelting. Ingots come from the MI Electric Blast
//      Furnace (one reduction recipe per metal, at rising coil tiers) and the mod's own Mekanism chain
//      (O2 3x, HCl 4x, H2SO4 5x) stays as the ore multiplier, so it obeys the T3 acid tiers.
//   2. The three alloys (no recipe at all without Tinkers' Construct) are made in MI machines.
//   3. The Teleport Pad needs MI steel plates and an LV analog circuit, so the Mining dimension, The Other
//      and The Beyond open at design T3.
//   4. Occultism's eldritch miners don't pull raw allthemodium/vibranium/unobtainium blocks out of thin
//      air (same rule as phase4_occultism.js): these metals are mined by hand. The mod itself destroys
//      the ores when a quarry, miner or other FakePlayer breaks them.
// None of these metals is in ChemLib's periodic table (they're fictional), so the Combiner can't make them
// and they stay out of the dissolver tables.

ServerEvents.tags('item', event => {
  // Feed for each reduction: the raw ore, or the dust from Mekanism's chain or a crusher. Both are treated
  // as concentrate (oxide/fluoride-bearing) that still has to be reduced, the way titanium sponge is.
  ;['allthemodium', 'vibranium', 'unobtainium'].forEach(metal =>
    event.add(`warbucks:${metal}_feed`, [`allthemodium:raw_${metal}`, `allthemodium:${metal}_dust`]))
})

ServerEvents.recipes(event => {
  const MI = 'modern_industrialization'
  const ATM = 'allthemodium'
  const mi = (type, json, id) => event.custom(Object.assign({ type: `${MI}:${type}` }, json)).id(`kubejs:allthemodium/${id}`)

  // ==========================================================================================
  // 1. NO DIRECT SMELTING (18 recipes)
  // Refractory, reactive metals don't come out of a furnace. Titanium, zirconium, tantalum and niobium
  // all melt above 1650 C, and their oxides are so stable that carbon at furnace heat can't strip the
  // oxygen. Industry reduces them chemically (Kroll process with Mg, sodium reduction of fluorides) and
  // melts them under argon. These metals get the same treatment.
  // ==========================================================================================
  const smelted = []
  ;['allthemodium', 'vibranium', 'unobtainium'].forEach(metal =>
    ['raw', 'ore', 'dust'].forEach(from =>
      ['smelting', 'blasting'].forEach(how => smelted.push(`${ATM}:${metal}_ingot_from_${from}_${how}`))))
  smelted.forEach(id => event.remove({ id: id }))

  // Occultism eldritch miners would hand out raw-metal blocks (weight 30) with no trip into the dark.
  ;['raw_allthemodium', 'raw_vibranium', 'raw_unobtainium'].forEach(id =>
    event.remove({ id: `occultism:miner/eldritch/${id}` }))
  console.info(`[phase5] Allthemodium: removed ${smelted.length} smelting recipes and 3 Occultism miners`)

  // ==========================================================================================
  // 2. REDUCTION IN THE ELECTRIC BLAST FURNACE (1 feed -> 1 ingot; Mekanism's chain is the multiplier)
  // MI coil tiers: cupronickel runs recipes up to 32 EU/t, kanthal up to 128 EU/t (the top EBF tier).
  // ==========================================================================================
  // Allthemodium, design T3, cupronickel EBF at LV (32 EU/t).
  // Carbothermic reduction, the oldest metallurgy there is: MO + C -> M + CO. Coke is the carbon, as in
  // MI's own silicon recipe (SiO2 + 2C -> Si + 2CO). It runs hotter than a furnace can get.
  mi('blast_furnace', {
    eu: 32, duration: 300,
    item_inputs: [{ tag: 'warbucks:allthemodium_feed', amount: 1 }, { item: `${MI}:coke_dust`, amount: 1 }],
    item_outputs: [{ item: `${ATM}:allthemodium_ingot`, amount: 1 }]
  }, 'ebf/allthemodium_ingot')

  // Vibranium, design T4-T5, kanthal EBF (128 EU/t, needs an MV hatch or better).
  // Modelled on the Kroll process for titanium and zirconium: chlorinate the ore with Cl2 over carbon
  // (MO2 + 2Cl2 + 2C -> MCl4 + 2CO), reduce the chloride with molten magnesium (MCl4 + 2Mg -> M + 2MgCl2),
  // all under argon, because hot titanium-like metals grab oxygen and nitrogen from air. The MgCl2 comes
  // back out (real plants electrolyse it back into Mg and Cl2).
  mi('blast_furnace', {
    eu: 128, duration: 400,
    item_inputs: [
      { tag: 'warbucks:vibranium_feed', amount: 1 },
      { item: `${MI}:coke_dust`, amount: 1 },
      { item: 'chemlib:magnesium_dust', amount: 2 }
    ],
    fluid_inputs: [
      { fluid: `${MI}:chlorine`, amount: 500 },
      { fluid: `${MI}:argon`, amount: 50 }
    ],
    item_outputs: [
      { item: `${ATM}:vibranium_ingot`, amount: 1 },
      { item: 'chemlib:magnesium_chloride_dust', amount: 2 }
    ]
  }, 'ebf/vibranium_ingot')

  // Unobtainium, design T5-T6, kanthal EBF at its 128 EU/t ceiling, gated by hydrofluoric acid (the T5
  // acid: fluorite + H2SO4). Modelled on tantalum: the ore is digested in HF, the metal comes out as a
  // fluoride complex (K2TaF7 in real plants), and molten sodium reduces it,
  // K2TaF7 + 5Na -> Ta + 2KF + 5NaF, under argon. MI has no EBF coil above kanthal, so the EV gate is
  // the acid and the long run, not the coil.
  mi('blast_furnace', {
    eu: 128, duration: 800,
    item_inputs: [
      { tag: 'warbucks:unobtainium_feed', amount: 1 },
      { item: `${MI}:sodium_dust`, amount: 2 }
    ],
    fluid_inputs: [
      { fluid: 'mekanism:hydrofluoric_acid', amount: 250 },
      { fluid: `${MI}:argon`, amount: 100 }
    ],
    item_outputs: [{ item: `${ATM}:unobtainium_ingot`, amount: 1 }]
  }, 'ebf/unobtainium_ingot')

  // ==========================================================================================
  // 3. ALLOYS (the mod only makes them with Tinkers' Construct, which this pack doesn't have)
  // Powder metallurgy: refractory alloys are made by blending metal powders and sintering or arc-melting
  // them, because their melting points are too high for a crucible. The Mixer blends, the EBF consolidates.
  // The Piglich Heart (The Other's ancient pyramid) is the binder: magic, but it is the one thing every
  // version of this mod has asked for to fuse these metals.
  // ==========================================================================================
  const blend = (alloy, a, b) => mi('mixer', {
    eu: 16, duration: 200,
    item_inputs: [
      { item: `${ATM}:${a}_dust`, amount: 1 },
      { item: `${ATM}:${b}_dust`, amount: 1 },
      { item: `${ATM}:piglich_heart`, amount: 1 }
    ],
    item_outputs: [{ item: `${ATM}:${alloy}_dust`, amount: 2 }]
  }, `mixer/${alloy}_dust`)
  blend('vibranium_allthemodium_alloy', 'allthemodium', 'vibranium')
  blend('unobtainium_vibranium_alloy', 'unobtainium', 'vibranium')
  blend('unobtainium_allthemodium_alloy', 'unobtainium', 'allthemodium')

  // Vibranium-allthemodium alloy, design T5: arc-melted under argon like any reactive refractory alloy.
  mi('blast_furnace', {
    eu: 128, duration: 400,
    item_inputs: [{ item: `${ATM}:vibranium_allthemodium_alloy_dust`, amount: 1 }],
    fluid_inputs: [{ fluid: `${MI}:argon`, amount: 100 }],
    item_outputs: [{ item: `${ATM}:vibranium_allthemodium_alloy_ingot`, amount: 1 }]
  }, 'ebf/vibranium_allthemodium_alloy_ingot')

  // The two unobtainium alloys, design T6: no coil gets hot enough, so the heat comes from annihilation.
  // A matter-antimatter pair turns its whole rest mass into energy (E = mc^2): one gram of antimatter
  // releases about 1.8 x 10^14 J, roughly 43 kilotons of TNT. One pellet fuses a batch of eight.
  ;['unobtainium_vibranium_alloy', 'unobtainium_allthemodium_alloy'].forEach(alloy => mi('blast_furnace', {
    eu: 128, duration: 1600,
    item_inputs: [{ item: `${ATM}:${alloy}_dust`, amount: 8 }, { item: 'mekanism:pellet_antimatter', amount: 1 }],
    fluid_inputs: [{ fluid: `${MI}:argon`, amount: 1000 }],
    item_outputs: [{ item: `${ATM}:${alloy}_ingot`, amount: 8 }]
  }, `ebf/${alloy}_ingot`))

  // ==========================================================================================
  // 4. TELEPORT PAD (Mining dimension from the Overworld, The Other from the Nether, The Beyond from
  // the End). The original is 1 ender pearl + 4 allthemodium nuggets; the pad now also needs a steel
  // frame and an LV analog circuit to drive it, so all three realms open at design T3.
  // ==========================================================================================
  event.remove({ id: `${ATM}:teleport_pad` })
  event.shaped(`${ATM}:teleport_pad`, ['PnP', 'nEn', 'PCP'], {
    P: `${MI}:steel_plate`,
    n: '#c:nuggets/allthemodium',
    E: 'minecraft:ender_pearl',
    C: `${MI}:analog_circuit`
  }).id('kubejs:allthemodium/teleport_pad')
})
