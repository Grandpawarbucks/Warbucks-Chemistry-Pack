// Recipe + registry dump for tools/quest_audit.py (the "items nobody can obtain" check).
// INACTIVE unless the marker file kubejs/config/dump_recipes.json exists in the game folder. The marker is
// never shipped: test/audit_dump.ps1 creates it in test/server only, runs the server, and deletes it again.
// Output (test server only): kubejs/config/recipe_dump.json (every recipe after all KubeJS changes, as JSON)
// and kubejs/config/registry_dump.json (item / entity / biome / structure / dimension ids).
// Named zz_ so its recipes handler is registered last and sees every other script's changes.

const WB_DUMP_MARKER = 'kubejs/config/dump_recipes.json'
function wbDumpActive() {
  try { return !!JsonIO.read(WB_DUMP_MARKER) } catch (e) { return false }
}

ServerEvents.recipes(event => {
  if (!wbDumpActive()) return
  const out = []
  let n = 0
  event.forEachRecipe({}, r => {
    try {
      out.push({ id: String(r.getId()), json: String(r.json) })
      n++
    } catch (e) {
      console.warn('[recipe_dump] skipped ' + r + ': ' + e)
    }
  })
  // forEachRecipe only walks the datapack recipes; recipes added by scripts (event.custom/shaped/...) live here.
  let wbAdded = event.addedRecipes.iterator()
  while (wbAdded.hasNext()) {
    let r = wbAdded.next()
    try {
      if (r.removed) continue
      if (!r.json || r.json.size() == 0 || r.hasChanged()) r.serialize()
      out.push({ id: String(r.getOrCreateId()), json: String(r.json) })
      n++
    } catch (e) {
      console.warn('[recipe_dump] skipped added ' + r + ': ' + e)
    }
  }
  JsonIO.write('kubejs/config/recipe_dump.json', { recipes: out })
  console.info('[recipe_dump] wrote ' + n + ' recipes to kubejs/config/recipe_dump.json')
})

ServerEvents.loaded(event => {
  if (!wbDumpActive()) return
  const $Registries = Java.loadClass('net.minecraft.core.registries.Registries')
  const access = event.server.registryAccess()
  const res = {}
  const keys = { item: $Registries.ITEM, block: $Registries.BLOCK, entity: $Registries.ENTITY_TYPE, fluid: $Registries.FLUID,
                 biome: $Registries.BIOME, structure: $Registries.STRUCTURE }
  // Plain loops and wb-prefixed names: Rhino shares var scope across scripts ("redeclaration of var ids")
  for (let k in keys) {
    try {
      let wbIds = []
      let wbIt = access.registryOrThrow(keys[k]).keySet().iterator()
      while (wbIt.hasNext()) wbIds.push(String(wbIt.next()))
      res[k] = wbIds
    } catch (e) {
      console.warn('[recipe_dump] registry ' + k + ' failed: ' + e)
    }
  }
  // Item and block tags as the server sees them (after KubeJS tag events): {tag: [ids]}
  let tagKeys = { item_tags: $Registries.ITEM, block_tags: $Registries.BLOCK }
  for (let k in tagKeys) {
    try {
      let wbTags = {}
      let wbTi = access.registryOrThrow(tagKeys[k]).getTags().iterator()
      while (wbTi.hasNext()) {
        let wbPair = wbTi.next()
        let wbArr = []
        let wbHi = wbPair.getSecond().iterator()
        while (wbHi.hasNext()) wbArr.push(String(wbHi.next().unwrapKey().get().location()))
        wbTags[String(wbPair.getFirst().location())] = wbArr
      }
      res[k] = wbTags
    } catch (e) {
      console.warn('[recipe_dump] ' + k + ' failed: ' + e)
    }
  }
  try {
    let wbDims = []
    let wbIt = event.server.levelKeys().iterator()
    while (wbIt.hasNext()) wbDims.push(String(wbIt.next().location()))
    res.dimension = wbDims
  } catch (e) {
    console.warn('[recipe_dump] dimensions failed: ' + e)
  }
  JsonIO.write('kubejs/config/registry_dump.json', res)
  console.info('[recipe_dump] wrote registry ids to kubejs/config/registry_dump.json')
})
