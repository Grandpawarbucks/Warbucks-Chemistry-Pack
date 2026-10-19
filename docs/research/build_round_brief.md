# Build round brief (2026-10-18): recipe fixes, Basics + auto layout + pruning, harvest chapter

The user approved: the recipe fixes from `chem_tier_audit.md`, the Basics group + automatic layout pass + pruning from
`quest_layout_audit.md`, and the harvest chapter from `tools_harvest_plan.md` with ore tier raises (MI titanium, tungsten,
platinum, iridium ores need an iron tool; Ad Astra desh = iron, ostrum = diamond, calorite = netherite).
NOT approved (leave alone): real rocket fuel (LOX/kerosene), sulfuric acid in the MV board, token shop prices, stone trace metals.

Seven writers work at the same time. **Each owns only the files listed for it.** Never edit another writer's files.
Repo: `C:\Users\Grandpawarbucks\OneDrive\Desktop\Chem Modpack Dev\Warbucks-Chemistry-Pack` (Windows). Python: `.venv\Scripts\python.exe`.

| Writer | Owns |
|---|---|
| E engine | `tools/questlib.py`, `tools/build_quests.py`, `tools/quest_data.py`, `tools/quests/STYLE.md`, new `tools/layout.py` |
| R recipes | everything under `pack/kubejs/` |
| H harvest | new `tools/quests/harvest.py` |
| M1 main path, early | `welcome.py start.py t0.py t1.py t2.py t3.py` |
| M2 main path, late | `t4.py t5.py t6.py t7.py seed.py creation.py` |
| B basics | `tools.py qol.py utilitarian.py storage.py power.py powah.py farming.py building.py` |
| S side pages | every other chapter file in `tools/quests/` (mekanism, new mekanism_power, ae2, logic, ars, justdirethings, create, occultism, apotheosis, relics, projecte, periodic, lab_notes, mystical, factory, worlds, undergarden, twilight, deeperdarker, space, explore, hunting, market, completionist) |

## Rules for every quest writer (M1, M2, B, S, H)
1. Follow `tools/quests/STYLE.md`. **Never rename a quest key.**
2. **Deleting** a quest: first search every file in `tools/quests/` for the key. If any other file depends on it or links
   to it, don't delete it: make it optional, or merge its tasks into the quest that replaces it and keep the old key as an
   optional quest. Prefer merge/optional over delete. List every deleted key in your reply.
3. **Coordinates don't matter any more**: writer E is adding an automatic layout pass that places every quest from its
   dependencies at build time. Don't spend time on x/y; keep whatever is there.
4. Prune lists come from `docs/research/quest_layout_audit.md` (duplicates, tick chains, required dead ends that should
   be optional, the seed `sd_*` bundles). Apply the ones that touch your files. Use judgement; explain anything you skip.
5. Quests that duplicate another chapter: keep the one in the more natural home, make the other optional or delete it
   (rule 2). Example: the `tc_*_paxel` quests in tools.py repeat start/t0/t1 quests; the Logistics Networks row in
   storage.py repeats logic.py (logic keeps it).
6. Validate only your own files: PowerShell `$env:QUEST_ONLY='<your keys, comma separated>'; .venv\Scripts\python.exe tools\build_quests.py --check`.
   Writer E's engine changes may land while you work; if `--check` breaks on something that isn't yours, note it and continue.
7. Don't run the full build, don't edit `pack/`, don't touch git, don't edit `test/ids.tsv`.
8. Reply with: what you changed per file, deleted keys, keys made optional, merges, and anything you skipped and why.
