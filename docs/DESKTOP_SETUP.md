# Playing and developing on another PC (Windows)

## A. Just play (you or your players)
1. Install **Prism Launcher** (prismlauncher.org).
2. Download [`launcher/Warbucks-Chemistry-Prism.zip`](../launcher/Warbucks-Chemistry-Prism.zip) from the GitHub repo (open the file, then use the download button).
3. In Prism: **Add Instance → Import → Browse** and pick the zip.
4. Launch. Before each start, the instance runs packwiz-installer, which downloads or updates every mod, config, script and quest from GitHub. The first launch takes a few minutes.

Notes:
- Prism picks Java 21 automatically (Settings → Java → Auto-detect, or let Prism download it).
- Memory is set to 4–10 GB with ATM's G1 arguments; change it in Edit Instance → Settings → Java.
- A few CurseForge mods may ask you to download them manually if their authors block third-party downloads; the installer shows a window with the links if so.

## B. Develop on the desktop
The repo is the single source of truth. Work on whichever machine you like, then **commit and push**; the other machine **pulls** before starting.

### One-time setup (Windows)
| Tool | Install |
|---|---|
| Git | `winget install Git.Git` |
| GitHub CLI | `winget install GitHub.cli`, then `gh auth login` |
| Java 21 (Temurin) | `winget install EclipseAdoptium.Temurin.21.JDK` |
| Go (to build packwiz) | `winget install GoLang.Go` |
| packwiz | `go install github.com/packwiz/packwiz@latest` (adds `%USERPROFILE%\go\bin\packwiz.exe`) |
| Python 3 | `winget install Python.Python.3.12` |
| Prism Launcher | `winget install PrismLauncher.PrismLauncher` |

```powershell
gh repo clone Grandpawarbucks/Warbucks-Chemistry-Pack
cd Warbucks-Chemistry-Pack
```

### Day-to-day
```powershell
git pull                      # get changes from the other machine
cd pack; packwiz refresh; cd ..   # after editing anything under pack/
python tools/build_quests.py  # after editing tools/quest_data.py (needs test/ids.tsv, see below)
python test/gen_modlist.py    # after adding a mod (and its row in docs/modlist-meta.tsv)
git add -A; git commit -m "..."; git push
```
Your play instance (section A) picks up pushed changes on its next launch, usually within a few minutes, because GitHub caches raw files briefly.

### Known limits on Windows
- The test loop (`test/smoke.sh`, `worldgen.sh`, `client-sync.sh`) is bash with macOS details (`sed -i ''`, named pipes). It runs on the Mac. On Windows, push your change and run the smoke test from the Mac, or ask Claude on the desktop to add a PowerShell version of the test loop.
- `test/build_id_index.py` reads the vanilla jar from Prism's macOS library path and the test server's mods folder; `test/ids.tsv` isn't in git. To rebuild quests on Windows, copy `test/ids.tsv` from the Mac, or port that path.
- CLAUDE.md is the project brief for Claude on either machine. Private details (server connection) are deliberately NOT in this public repo.
