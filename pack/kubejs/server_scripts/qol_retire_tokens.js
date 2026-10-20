// Demigod Tokens are retired (2026-10-20, user decision "Coins replace tokens"): quests pay Wardaddy Market coins now.
// On login, remove any tokens a player still carries in their inventory or ender chest, so old stacks don't linger.
// The items stay registered (startup_scripts/chemistry_items.js) so old saves still load.
const RETIRED_TOKENS = ['kubejs:demigod_token', 'kubejs:greater_demigod_token']

function wbClearTokens(container) {
  let removed = 0
  for (let i = 0; i < container.getContainerSize(); i++) {
    const stack = container.getItem(i)
    if (!stack.isEmpty() && RETIRED_TOKENS.includes(String(stack.getId()))) {
      removed += stack.getCount()
      stack.shrink(stack.getCount())
    }
  }
  if (removed > 0) container.setChanged()
  return removed
}

PlayerEvents.loggedIn(event => {
  const player = event.player
  const removed = wbClearTokens(player.getInventory()) + wbClearTokens(player.getEnderChestInventory())
  if (removed > 0) {
    player.tell(`Demigod Tokens are retired: removed ${removed} from your inventory. Quests now pay Market coins (press Y).`)
    console.info(`[warbucks] removed ${removed} retired Demigod Tokens from ${player.username}`)
  }
})
