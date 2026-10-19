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

### The custom mod (Warbucks Core, `mod/`)
```powershell
cd mod; .\gradlew.bat build; cd ..        # jar in mod\build\libs\
```
To ship a new version: bump `mod_version` in `mod/gradle.properties`, build, then
```powershell
gh release create warbuckscore-v1.0.1 mod\build\libs\warbuckscore-1.0.1.jar --title "Warbucks Core 1.0.1" --notes "..."
cd pack; packwiz url add "Warbucks Core" https://github.com/Grandpawarbucks/Warbucks-Chemistry-Pack/releases/download/warbuckscore-v1.0.1/warbuckscore-1.0.1.jar -y; cd ..
```
Mod textures: `python mod/tools/textures.py` (needs Pillow: `pip install pillow`, ideally in a venv). Same for `tools/build_art.py`.

### Generated files you rebuild
| After you change... | Run |
|---|---|
| quests (`tools/quests/*.py`) | `python tools/build_quests.py` (check first with `--check`) |
| the mod list | add a row to `docs/modlist-meta.tsv`, then `python test/gen_modlist.py` |
| mods that add blocks | `python test/build_id_index.py` (needs a test server's mods folder), then `python tools/build_dissolver.py` |
`test/ids.tsv` (every valid item/entity/biome id) is committed, so quests build on Windows without running a server.

### The live server (VPS)
Warbucks runs on the VPS as `warbucks.service` and pulls the pack from GitHub each time it starts (see `docs/SERVER.md`).
After you push, restart it to update, but check `list` for players first. The SSH key on the Mac is Mac-only:
add your Windows PC's own public key to the VPS (`ssh-keygen -t ed25519`, then append `~/.ssh/id_ed25519.pub` to the
server's `/root/.ssh/authorized_keys` from a machine that already has access). Connection details are deliberately
not in this public repo.

### Moving Claude to this PC
Claude sessions stay on the machine they ran on, so start a NEW session on Windows: open this folder in the Claude
desktop app's Code tab and say "continue from the CLAUDE.md handoff". `CLAUDE.md` (read automatically) holds the rules
and the current state. Copy the private memory notes from the Mac's `handoff/` folder (git-ignored) and ask the new
session to install them as its memory.

### Smoke test on Windows
```powershell
powershell -ExecutionPolicy Bypass -File test\smoke.ps1      # $env:KEEP_WORLD=1 first to reuse the world
```
`test/smoke.ps1` + `test/lib.ps1` are the PowerShell port of `smoke.sh` + `lib.sh` (same steps, same `SEED`,
`KEEP_WORLD`, `POST_DONE_WAIT`, `PACKWIZ_PORT` settings, same `parse_logs.py` summary). The first run downloads
packwiz-installer-bootstrap and installs the NeoForge server into `test\server` (a few minutes plus all mod downloads).
It uses Java 21 from `JAVA_HOME`, never the `java` on PATH (Windows often has an old Java 8 there).
`test/known_issues.txt` (the allowlist of harmless log lines) is committed so both machines use the same list.

### Known limits on Windows
- Line endings: the repo has a `.gitattributes` with `* -text`, so Git never converts line endings. Without it, Git for
  Windows (autocrlf=true) checks out CRLF files, packwiz hashes those, and the pushed `index.toml` no longer matches what
  players download. In an older clone, run `git config core.autocrlf false`, then `git rm --cached -r -q .; git reset --hard`.
- `worldgen.sh`, `emc_check.sh` and `client-sync.sh` are still bash only (macOS `sed -i ''`, named pipes); port them the
  same way as smoke.ps1 when needed.
- If Gradle or Java servers fail with "Unable to establish loopback connection" in a Claude shell, run them in a normal
  terminal (or the Claude app's Terminal panel); they work there.
- CLAUDE.md is the project brief for Claude on either machine. Private details (server connection) are deliberately NOT in this public repo.
