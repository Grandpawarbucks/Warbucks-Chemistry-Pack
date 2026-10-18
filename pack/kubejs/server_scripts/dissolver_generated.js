// Alchemistry Dissolver recipes for modded and missing blocks (the "dissolve ANY block" goal).
// GENERATED data: kubejs/config/dissolver_recipes.json, written by tools/build_dissolver.py, which copies each
// block's output from an analogous block Alchemistry already handles (see docs/dissolver-coverage.md).
// Don't edit the table by hand; rerun the generator after mod-list changes.

ServerEvents.recipes(event => {
  const table = JsonIO.read('kubejs/config/dissolver_recipes.json')
  if (!table) {
    console.error('[dissolver] kubejs/config/dissolver_recipes.json is missing: run tools/build_dissolver.py')
    return
  }
  let added = 0, missing = 0
  table.recipes.forEach(row => {
    const item = String(row[0])
    if (!Item.exists(item)) { missing++; return }
    event.custom({
      type: 'alchemistry:dissolver',
      group: 'alchemistry:dissolver',
      input: { ingredient: { item: item } },
      output: table.outputs[row[1]]
    }).id('kubejs:dissolver/' + item.replace(':', '/'))
    added++
  })
  console.info('[dissolver] added ' + added + ' generated dissolver recipes (' + missing + ' items not present)')
})
