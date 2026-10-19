// T4 aluminium line (user decision 2026-10-18: GT-style chemistry lines on MI, docs/PROGRESSION.md).
// Real route: Bayer process (bauxite + NaOH -> sodium aluminate -> Al(OH)3 -> Al2O3) and then the
// Hall-Heroult cell (molten alumina electrolysed against carbon anodes: 2Al2O3 + 3C -> 4Al + 3CO2).
// Recipes: server_scripts/phase4_aluminum.js. API: MI docs ADDING_MACHINES.md / ADDING_FLUIDS.md.

let HALL_HEROULT

MIMachineEvents.registerRecipeTypes(event => {
  HALL_HEROULT = event.register('hall_heroult_cell').withItemInputs().withItemOutputs()
})

MIRegistrationEvents.registerFluids(event => {
  // Pale, slightly cloudy liquor (the real "pregnant liquor" is a clear to straw-coloured solution).
  event.register('Sodium Aluminate Solution', 'sodium_aluminate_solution', 0xd8c99a, 'water', false, 'medium')
})

MIMachineEvents.registerMachines(event => {
  // A 3x3 steel pot, 3 high: cupronickel coils ring the molten bath (the empty centre), with steel
  // casing below and above (the anode beam). Hatches go in the casings. Built without aluminium,
  // because the cell is what makes the first aluminium.
  const casing = event.memberOfBlock('modern_industrialization:steel_machine_casing')
  const coil = event.memberOfBlock('modern_industrialization:cupronickel_coil')
  const hatches = event.hatchOf('item_input', 'item_output', 'energy_input')
  // Rows from back to front; each row lists its layers from bottom to top. '#' is the controller.
  const shape = event.layeredShape('steel', [
    ['SSS', 'CCC', 'SSS'],
    ['SSS', 'C C', 'SSS'],
    ['SSS', 'C#C', 'SSS'],
  ])
    .key('S', casing, hatches)
    .key('C', coil, event.noHatch())
    .build()

  event.simpleElectricCraftingMultiBlock(
    'Hall-Héroult Cell', 'hall_heroult_cell', HALL_HEROULT, shape,
    event.progressBar(84, 35, 'arrow'),
    itemInputs => itemInputs.addSlots(26, 35, 3, 1), itemOutputs => itemOutputs.addSlot(116, 35),
    fluidInputs => {}, fluidOutputs => {},
    'steel', 'hall_heroult_cell', true, false, false,
  )
})
