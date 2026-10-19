# The Demigod's Market: shop brief (2026-10-19)

User decisions: "repeatable shop quests in the Market chapter, each unlocked after building that machine yourself, priced
by tier", then "add all sorts of stuff to the pack that we can buy from a market in the quest book ... things that we get
to the tier of".

## The rule
**Whatever you've made or obtained yourself, you can buy more of.** Each shop entry depends on the quest where the player
first makes or obtains that item (prefer the main-path quest; a side-page quest is fine for side content). The entry is
invisible until that quest is done, so the shop never shows or sells anything from a tier the player hasn't reached.
Tokens save repetition; they never skip a tier or a chemistry step.

## How an entry is built (engine support is in tools/questlib.py)
```python
Q("<prefix>_buy_<name>", 0, 0, [item("kubejs:demigod_token", PRICE)], "<Item name>", deps=["<quest that makes it>"],
  items=[("<item id>", COUNT)], tokens=0, xp=0, optional=True, repeat=True, consume=True, locked_hidden=True,
  subtitle="<price> · unlocked by <that quest's title>", desc=[...])
```
- MV and up: pay in `kubejs:greater_demigod_token` (1 Greater = 9 tokens).
- Write a small helper at the top of your file so entries are one line each. Coordinates are automatic.
- Group entries in rows by tier (Steam/T0-T1 → LV → MV → HV → EV), each row starting with a short optional "counter"
  checkmark quest (tokens=0) that depends on that tier's milestone.
- One shop chapter needs an intro quest (tokens=0, optional) stating the rule.

## Prices (token economy: the whole book pays ~3,540 tokens; ~1,620 on the required path; T3-T4 pay ~250)
| Tier | Machines | Materials (per stack-ish bundle) | Gear (tool/armour piece or set) | World goods |
|---|---|---|---|---|
| Steam (T0-T1) | 3-6 | 1-3 for 16-64 | 2-6 | 1-2 for 32-64 |
| LV (T3) | 8-15 | 2-6 for 16 | 6-12 | 1-3 |
| MV (T4) | 2-3 Greater | 1 Greater for 16 | 1-2 Greater | 2-4 |
| HV (T5) | 4-6 Greater | 2 Greater for 16 | 3-4 Greater | 4-8 |
| EV (T6) | 8+ Greater | 3-4 Greater for 8-16 | 5+ Greater | 1 Greater |
Price within a band by the item's real material cost (read the recipes in the jars): a purchase must be cheaper in
effort than making it again, but never trivial. Bulk materials come in sensible bundle sizes (16, 32 or 64).

## Never sold
Multiblock controllers; Alchemistry Dissolver/Combiner/fission/fusion; anything flight-related (pylons, potions of
flying, jetpacks, Angel Ring, Ars flight); oganesson and other "complete the periodic table" elements; Seed of a New
World parts (antimatter/energy cores, the Seed); Nether Stars, Dragon Egg, boss trophies; ProjectE items; creative items;
Demigod Tokens themselves; anything the player can't actually obtain in this pack (check test/ids.tsv and pack/kubejs).
Items that are the core of a chemistry lesson (e.g. sulfuric acid, alumina, silicon) CAN be sold, but only after the
quest where the player made them, at the tier price.

## Who owns what (one file each; never edit another writer's file)
| Writer | File (new chapters are already registered in tools/quest_data.py) | Sells |
|---|---|---|
| Machines (running) | `tools/quests/market.py` | machines, boilers, tanks, hulls, cables |
| Materials | `tools/quests/shop_materials.py` (prefix `sm_`) | ingots, dusts, plates, gears, rods, wires, components, circuits' parts, chemicals (buckets, ChemLib compounds and elements the player has made), fuels |
| Gear | `tools/quests/shop_gear.py` (prefix `sg_`) | tools, armour, weapons, backpacks and upgrades, storage blocks (chests/drawers), QoL items, magic gear and trinkets |
| World | `tools/quests/shop_world.py` (prefix `sw_`) | building blocks, decoration, food and crops, saplings and seeds, mob drops, dimension materials (Nether, End, Twilight, Undergarden, Deeper and Darker, space) |
Validate your file only: PowerShell `$env:QUEST_ONLY='<your chapter key>'; .venv\Scripts\python.exe tools\build_quests.py --check`.
Don't touch pack/, tools/*.py, test/ or git. Reply with entries per tier, the price table you used and what you didn't sell.
