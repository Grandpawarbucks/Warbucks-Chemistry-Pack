# Build round brief (2026-10-19): ATM10-aligned quests + the story through-line

The user asked to "pull the quests from ATM10, the raw quests that align" and to make sure the story part is covered.
ATM10's quest book is **All Rights Reserved** and our repo is **public**: never copy its files, titles, descriptions,
rewards or layouts. We use ATM10 only as a **checklist of items worth a quest**. For every item ATM10 quests on that
exists in our pack and **aligns** with our progression, we write our own quest, in our style and story.

Helper (requirements only): `.venv\Scripts\python.exe tools\quest_compare.py "<ATM10 folder>" --chapter <their chapter>`
or `--mod <namespace>`. ATM10 folder: `C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10\config\ftbquests\quests`.
At the start, 1,124 items were missing. Repo: `C:\Users\Grandpawarbucks\OneDrive\Desktop\Chem Modpack Dev\Warbucks-Chemistry-Pack`.

## Who owns what (never edit another writer's files; never add a quest for another writer's items)
| Writer | Owns chapter files (`tools/quests/`) | ATM10 chapters / item namespaces to cover |
|---|---|---|
| M1 early path + story | welcome, start, t0, t1, t2, t3 | chapters `mainquestline_part_1`, `mi_steam` (incl. their minecraft items) |
| M2 late path + story | t4, t5, t6, t7, seed, creation | chapters `mi_electric`, `mi_digital`, `mi_endgame` |
| B basics | tools, harvest, storage, power, powah, farming, qol, building | `minecraft` items NOT in M1's chapters; powah, sophisticatedbackpacks, sophisticatedstorage, ironfurnaces, functionalstorage, silentgear, mekanismtools, generatorgalore, toms storage, utilitarian, comforts and other QoL/storage/power mods; chapters basic_*, storage, food_and_farming, building_tips, generators, powah, silent_gear |
| T tech | mekanism, mekanism_power, ae2, logic, factory, create, justdirethings | mekanism, mekanismgenerators, ae2, advanced_ae, extendedae, megacells, create (+ addons), justdirethings, integrateddynamics, hostilenetworks, extendedcrafting, packagedauto, logistics/automation mods |
| G magic | ars, occultism, apotheosis, relics, projecte, mystical | ars_nouveau, ars_elemental, ars_additions, occultism, apothic_enchanting, apotheosis, apothic_*, relics, artifacts, reliquary, projecte, mysticalagriculture |
| W worlds | worlds, explore, undergarden, twilight, deeperdarker, space, hunting, periodic, lab_notes, market, completionist | twilightforest, undergarden, deeperdarker, ad_astra, chemlib/alchemistry, mob drops; chapters twilight_forest, undergarden, deeper_and_darker, bounty_board, artifacts-as-loot |
An item in a namespace nobody owns: the writer whose chapter is the most natural home takes it; say so in your reply.

## What "aligns" means
Add a quest only when the item fits our pack:
- It exists in `test/ids.tsv` and is obtainable here (check the pack's KubeJS in `pack/kubejs/` for removed or changed recipes).
- It respects our gates (`tools/quests/STYLE.md` "Pack facts", `CLAUDE.md`): flight only via chemistry (Infusion Pylon,
  Iron Jetpacks, Angel Ring, Ars Ritual of Flight with hydrogen); ProjectE lite (no condensers/collectors/relays); Mystical
  Agriculture and Occultism blocked resources; ore yields capped before acids; no creative items.
- It's worth a player's time: group colour/wood/tier variants into one `anyof(...)` or `anytag(...)` quest; skip pure
  decoration unless it's a building chapter; skip ATM10-specific items (ATM Star, allthemodium, etc. aren't in our pack anyway).
- Most new quests are `optional=True` with `tokens=1`. Only make a quest required when it's a real progression step.
For every skipped item group, give the reason in your reply (one line per group, not per item).

## Rules (same as the last round)
1. Follow `tools/quests/STYLE.md`. **Never rename a quest key.** New keys use your chapter's prefix.
2. Coordinates are automatic (`tools/layout.py`): don't place x/y. Wire `deps` so lines read left to right.
3. Our own text: subtitle + structured desc, real chemistry where it fits. Use only ids that exist; read recipes in the
   jars (`test/server/mods`) or say "check JEI".
4. Validate only your files: PowerShell `$env:QUEST_ONLY='<your chapter keys>'; .venv\Scripts\python.exe tools\build_quests.py --check`.
5. Don't run the full build, don't edit `pack/`, `tools/*.py`, `test/`, or git.
6. Reply: quests added per chapter, items covered vs skipped (with reasons), and anything for the integrator.

## Story (M1 and M2; everyone keeps it in mind)
The player is a demigod who woke without their power and regains it by mastering chemistry (docs/PROGRESSION.md §1).
Every main chapter needs: a gold `&6` memory line on its first quest, a gold payoff line at its milestone(s), and the beat
from PROGRESSION.md §3 for that tier (T0 awakening, T1 the periodic table opens, T2 flight returns, ... T6 the Seed and
Creation). M1 and M2: first read every `&6` line on the main path (welcome → creation) and fix gaps, contradictions and
repetition so the arc reads as one story from first join to the end. Add short story-only checkmark quests ONLY where a
beat is missing (e.g. a chapter end that hands over to the next). Tone: wonder and quiet confidence, a little wry; 1–2
lines; no new characters. Every other writer: give each chapter you touch an opening `&6` line if it lacks one.
