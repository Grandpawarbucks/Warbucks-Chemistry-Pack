// priority: -100
// Furnace QoL (user request 2026-10-18, from the user's Wardaddy ATM10 server tweak zz_custom/furnace_speed.js):
// 4x faster cooking for furnace, blast furnace and smoker recipes, including every mod's smelting recipes.
// Only vanilla cooking types: machine recipes (MI, Mekanism, Create) keep their own times.

const WB_FURNACE_SPEED = 4

const WB_COOKING_DEFAULTS = {
  'minecraft:smelting': 200,
  'minecraft:blasting': 100,
  'minecraft:smoking': 100
}

ServerEvents.recipes(event => {
  Object.keys(WB_COOKING_DEFAULTS).forEach(type => {
    let changed = 0
    event.forEachRecipe({ type: type }, recipe => {
      let json = JSON.parse(recipe.json)
      let time = json.cookingtime != null ? json.cookingtime : WB_COOKING_DEFAULTS[type]
      recipe.set('cookingtime', Math.max(1, Math.floor(time / WB_FURNACE_SPEED)))
      changed++
    })
    console.info(`[qol] ${type}: sped up ${changed} recipes ${WB_FURNACE_SPEED}x`)
  })
})
