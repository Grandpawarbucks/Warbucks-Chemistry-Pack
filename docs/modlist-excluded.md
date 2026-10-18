## ATM10 performance and library mods left out

Source: ATM10 8.3 mod list (`config/crash_assistant/modlist.json` in github.com/AllTheMods/ATM-10, committed 2026-10-15). Per CLAUDE.md, ATM10's performance and shared library mods are included unless they conflict or only serve ATM10 content we don't use.

### Performance and utility
| Mod | Reason left out |
|---|---|
| Memory Settings | Shows ATM's RAM-warning screen; needs pack-specific config. Our RAM guidance is in README.md. Revisit in Phase 6. |
| Crash Assistant / Crash Utilities | Crash Assistant needs a pack-specific mod list and config. Revisit in Phase 6, before release. |
| Better Compatibility Checker | Needs a pack version and update URL. Add at release (Phase 6). |
| FlickerFix | Minor visual fix. The Modrinth build is older than ATM's; low value. |
| Observable | Developer profiler that duplicates spark; needs Kotlin for Forge. |
| Euphoria Patches | Shader-pack addon; only matters with Complementary shaders. Players can add it. |
| I'm Fast | Couldn't confirm what it does from its listing; not added rather than guessed. |

### Libraries
These are only dependencies of ATM10 mods we don't include. The "used by" column is a best-effort note, not checked mod by mod; what matters is that no mod in this pack needs them (the smoke test would fail on a missing dependency). Each gets added automatically if a mod we pick needs it.

| Library | Used in ATM10 by (not in this pack) |
|---|---|
| Kotlin for Forge, Fzzy Config | Observable and Kotlin-based mods |
| Iceberg, Prism lib | Legendary Tooltips |
| Framework (MrCrayfish) | MrCrayfish mods |
| YACL, Bridging Mod deps | Bridging Mod and others |
| owo-lib | Various Wisp Forest mods |
| playerAnimator, Iron's Lib, Lionfish, Caelus | Mob and spell mods (Iron's Spells, etc.) |
| PolyLib, Omega Config, Valhelsia Core, MonoLib, CorgiLib, Jupiter, Atlas API | Specific ATM10 content mods |
| EdivadLib | DimStorage |
| ExperienceLib, ObserverLib | Specific ATM10 content mods |
| CTM | Connected-texture mods (XyCraft) |
| Scalable Cat's Force | QuarryPlus |
| BlockUI, Cryonic Config | MineColonies and others |
| McJtyLib, Zero CORE 2, Brandon's Core, CodeChicken Lib, Silent Lib, Cucumber, Athena | RFTools/XNet, Extreme Reactors, Draconic Evolution, Ender Storage, Silent's mods, Mystical Agriculture/Iron Jetpacks, Ad Astra connected textures (optional) |
| KubeJS Tweaks, Open Loader | ATM-specific scripting and datapack loading |
| PonderJS | **Excluded:** ATM gets Ponder bundled inside Create |

### ATM10 content intentionally excluded
- **Create addons not added** (Create itself was re-added 2026-10-18 by user decision): Copycats+, Bells & Whistles, Hypertube, Aquatic Ambitions, Rechiseled: Create, Sophisticated Create integrations, Ars Creo.
- **ATM-specific content:** Allthemodium, AllTheOres, AllTheCompressed, AllTheTweaks, ATM gear, ATM: Compat.
- **Refined Storage and its addons:** AE2 is the only storage network.
- **Redundant tech:** Extreme Reactors, Oritech, Ender IO (beta), Immersive Engineering (stale), Actually Additions, RFTools Power, Generator Galore, XNet, Mekanistic Routers, Industrial Foregoing, PneumaticCraft.

### Building mods considered and left out
| Mod | Reason |
|---|---|
| Chipped | No update in 2 years (2024-10); Rechiseled covers block variants |
| LittleTiles | 1.21.1 build is a pre-release; heavy |
| Decorative Blocks | No NeoForge 1.21.1 build |

### Tool mods
| Mod | Reason |
|---|---|
| Tinkers' Construct | No NeoForge 1.21.1 build (newest is 1.20.1 Forge); Silent Gear is used instead |
| Paxels (standalone) | Last update 2024-10; Mekanism Tools provides paxels |
| Immersive Aircraft | Declined by the user (2026-10-18) |
| "Building Sticks" | ATM10's stick mod is Construction Sticks, which is already in the pack |

### Monifactory review (2026-10-18)
| Mod / feature | Reason |
|---|---|
| GregTech CEu Modern | 1.21.1 only has an alpha from July 2025; MI stays as the backbone |
| MoniLabs, Micro Miners, Extended Crafting: Expanded | Monifactory's own 1.20.1 code |
| Modern AE2 Additions | 1.20.1 only; ExtendedAE covers most of it |
| Ender IO | 1.21.1 build is still beta, and it overlaps MI |
| Bountiful | 1.21.1 build is beta |
| The Lost Cities | Declined by the user |
| William Wythers' Overhauled Overworld | Declined by the user (BOP is enough) |
| GregTech Modern Ore Generation: Standalone (GTMOGS) | KubeJS integration broken (per its README), disables all vanilla ore gen, newest commit "breaks datagen"; last release 2025-10 |

### Create addons without a NeoForge 1.21.1 build
| Mod | Reason |
|---|---|
| Destroy (Create chemistry) | No NeoForge 1.21.1 build |
| Create: Steam 'n' Rails | No NeoForge 1.21.1 build |
