# Wardaddy Market (wdmarket) in Warbucks Chemistry

Researched 2026-10-20 from the mod's source (`C:\Users\Grandpawarbucks\curseforge\minecraft\wdmarket`, 1.24.7 source;
the pack ships 1.24.6, whose Settings class has the same keys), ATM10's config and its `_tools` scripts.

## How it works
- **Wallet:** SG-Economy API (pinned 1.0.5; 1.1.0 breaks FTB XMod Compat's provider, seen in ATM10). Coins are a
  player capability, shown in the inventory. Team wallets (FTB Teams parties) live in wdmarket's own saved data.
- **Market screen:** Market key (`Y` by default, "Open Wardaddy Market") or `/market` / `/shop`. Buy with a cart, sell
  from inventory, buyback for 5 minutes, Daily Deals and Bounties (category "Today's Deals"), Bank tab services.
- **prices.json is NOT generated from recipes by the mod.** On first start, with no file, it writes a small bundled
  vanilla list (`/wdmarket/default_prices.json`). Packs ship their own. ATM10 builds it with `_tools/build_shop_values.py`
  (ProjectE EMC anchors + cheapest-recipe propagation) and `_tools/build_market_gates.py` (quest gates, loot crates).
  `price_overrides.json` in ATM10 is an input of those tools, not something the mod reads. The mod itself reads
  `server_overrides.json` (in-game `/wdmarket price`, applied on top at every load).
- **prices.json format:** `{"categories": [...], "items": [[id, name, buy, sell, tier, category_index, buyable(0/1),
  gate, gate_title], ...]}`. `id` may carry components (`mod:item[comp=snbt]`). Unknown ids are skipped and logged
  ("N ids not registered"). The name field is cosmetic (clients use the item's own name). Potions, enchanted books
  and Apotheosis gems are added by the mod itself as extra categories.
- **Tiers:** `settings.json` `tier_names` (1 to 31) and `tier_quests` (hex FTB quest ids). Tier 0 is always open;
  tier t opens when the player's team completes `tier_quests[t-1]`. An item's `tier` picks its shelf. Unknown quest
  ids never lock anything. The lock message says "complete <tier name> on the Market Tiers quest page" (hard-coded
  text; we have no such page, so our tier names say which quest opens them).
- **Gates:** per item, `gate` = hex quest id. A gated item needs its tier AND that quest.
- **Quest coins:** FTB Quests' own `currency` reward (`dev.ftb.mods.ftbquests.quest.reward.CurrencyReward`) pays
  through FTB Library's CurrencyHelper; FTB XMod Compat registers an SG-Economy provider (`currency_selector:
  "default"` picks SG Economy when it's installed). SNBT: `{ amount: 300, id: "<16 hex>", type: "currency" }`.
  wdmarket adds a "Claim" button (and `/market claim`) that claims every unclaimed coin reward of finished quests.
- **Creative:** ATM10 has a "Creative" category unlocked by its last tier; Deals skip a category named "Creative".
  We have no Creative category and list no creative-only items.
- **Settings** (`config/wdmarket/settings.json`, missing keys are written back with defaults): XP level price,
  potion prices, buyback, sell-bin rate, enchanted-book pricing and shelves, team wallet, services (extra FTB Chunks
  claims / force-loads via `ftbchunks admin extra_*`, repair per durability point, day, clear weather), admin
  permission, Apotheosis Forge stat step price and `forge_price_scale`, relic XP multiplier, perks (attribute steps,
  effects), flight per hour / permanent, loot booster, deals/bounties, structure chest fill, Salvage Station and Loot
  Crate Printer (`printer_crates`), `disabled_features` (perks, flight, loot_boost, forge_stats, apoth_forge,
  rs_ae2_speed, chest_bonus, enchanted_books), `tier_names` / `tier_quests`.
- **Optional integrations** switch on by mod presence: Apotheosis (gems, Forge), Relics, Sophisticated Backpacks (Ore
  Hammer upgrade), Dank Storage, Refined Storage / AE2 (`rs_ae2_speed`: Molecular Assemblers 4x, import/export buses
  64x per operation), JEI. Its mixins are `required: false`, so absent targets are skipped.
- Other ATM10 config folders (`market_categories`, `market_presets`, `createdeliveryrequired-market-item-prices.toml`)
  belong to other mods, not wdmarket.

## Our setup
- Coin scale: **1 old Demigod Token = 100 coins** (`COINS_PER_TOKEN` in tools/build_quests.py). Quests pay their
  chapter's old token rate x 100 (milestones x2); the old Greater Token item rewards in Creation pay 900 each. The book
  pays 623,500 coins in all.
- `tools/build_market_prices.py` writes `pack/config/wdmarket/prices.json` and the tier fields of `settings.json`.
  Re-run it after quest, recipe or mod changes (it needs test/dump from `test/audit_dump.ps1`). The method is in the
  script's docstring; `--why <item>` prints the recipe chain behind a value.
- Tiers = the Demigod's Path: 0 Getting Started (open), 1 Ch. I (after "Ready for Chemistry"), 2 Ch. II (after
  "Endless Water"), 3 Ch. III (after "The Dissolver"), 4 Ch. IV (after "Steel"), 5 Ch. V (after "Electric Blast
  Furnace"), 6 Ch. VI (after "Sulfuric Acid"), 7 Ch. VII (after "HV: Digital Circuits"), 8 Ch. VIII (after "EV:
  Processing Units"), 9 Seed (after "Leaving the Cradle"), 10 Creation (after "Seed of a New World").
- Services are all on; prices are in settings.json (`_warbucks` explains the scale).
