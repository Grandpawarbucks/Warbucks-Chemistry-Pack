# Running a Warbucks Chemistry server

The kit lives in `server/`:

| File | What it does |
|---|---|
| `install.sh <folder>` | Creates the server folder: copies the start script, JVM args and `server.properties` (only if missing, so your edits are kept), and downloads packwiz-installer-bootstrap. |
| `start.sh` | Every start: pulls the latest pack from GitHub, installs or upgrades NeoForge if the pack needs a new version, then runs the server. It restarts after a crash; `stop` in the console shuts down for good. |
| `server.properties` | Defaults: whitelist on, `allow-flight=true` (required: flight items would get players kicked otherwise), Normal difficulty, 10 players, view distance 8. |
| `user_jvm_args.txt` | 8–12 GB heap with G1 settings (ATM10-based; see README.md). Lower `-Xmx` on smaller machines, never below 6G. |
| `warbucks.service` | systemd unit (Linux). The console runs in tmux session `warbucks`. |

Requirements: Java 21, `curl`, about 10 GB of free disk space plus room for backups, and `tmux` for the systemd unit.

## Install (Linux)
```bash
git clone https://github.com/Grandpawarbucks/Warbucks-Chemistry-Pack.git
sudo Warbucks-Chemistry-Pack/server/install.sh /opt/warbucks
echo eula=true | sudo tee /opt/warbucks/eula.txt   # you accept the Minecraft EULA: https://aka.ms/MinecraftEULA
sudo chown -R minecraft:minecraft /opt/warbucks
sudo cp Warbucks-Chemistry-Pack/server/warbucks.service /etc/systemd/system/
sudo systemctl enable --now warbucks
```
The first start downloads NeoForge and about 200 mods, which takes a few minutes. Then watch the console:
`sudo -u minecraft tmux attach -t warbucks` (detach with Ctrl+B, then D).

## Day to day
- **Players:** `whitelist add <name>`, `op <name>` in the console.
- **Updates:** push to GitHub, then `sudo systemctl restart warbucks`. Restarting pulls the new pack (mods, configs, KubeJS, quests).
  Players update automatically on their next Prism launch.
- **Backups:** Simple Backups makes a full backup every 24 hours and keeps 7 (`pack/config/simplebackups-common.toml`),
  stored in `/opt/warbucks/simplebackups`.
- **Stop or start:** `sudo systemctl stop warbucks` / `start` (stop waits up to 3 minutes for the world to save).
- **Logs:** `/opt/warbucks/logs/latest.log`.

## Notes
- Client-only mods (shaders, minimap rendering, zoom...) are skipped automatically (`-s server`).
- If GitHub is unreachable, the server starts with the files it already has.
- `/reload` and restarts with players online: warn them first.
