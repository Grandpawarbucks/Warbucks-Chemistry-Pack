#!/usr/bin/env python3
"""Quest editor: the quest preview, but editable, served on http://localhost:8765 (127.0.0.1 only).

    .venv\\Scripts\\python.exe tools\\quest_editor.py        (Windows)
    python3 tools/quest_editor.py [--port N]                 (anywhere)

- Drag a quest or quest link to move it (0.5 grid); it is saved to tools/quest_overrides.json on drop.
- Click a quest to edit its title, subtitle and description; "Reset to generated" drops its override.
- Check runs tools/build_quests.py --check. Push runs check, build, packwiz refresh, then commits ONLY the quest
  files and pushes (players get it on their next Prism launch, the live server on its next restart).
- The page reloads the data after every save, on Refresh, and by itself when the quest files change on disk
  (other writers' edits show up live). Each data load runs test/build_quest_preview.py --json in a fresh process.

Overrides never change quest keys, deps, tasks or rewards (see apply_overrides in tools/quest_data.py).
Icons come from the mod jars in test/server/mods and are only served to this page, never written to the repo.
"""
import http.server
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "test"))
import build_quest_preview as bqp  # noqa: E402  (icons + shared CSS; it imports quest data only inside collect())

PY = sys.executable
OVERRIDES = ROOT / "tools/quest_overrides.json"
BUILD = ROOT / "tools/build_quests.py"
PUSH_PATHS = ["tools/quest_overrides.json", "pack/config/ftbquests", "docs/QUESTS.md", "pack/index.toml", "pack/pack.toml"]
TRAILER = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765

_lock = threading.Lock()        # overrides file
_data_lock = threading.Lock()   # data loads
_push_lock = threading.Lock()
_cache = {"version": None, "body": None, "gen": {}}
_last_check = {"ok": None, "summary": "not run yet", "time": None}


# --- overrides file ---------------------------------------------------------------------------
def read_overrides():
    if not OVERRIDES.exists():
        return {}
    text = OVERRIDES.read_text(encoding="utf-8").strip()
    data = json.loads(text) if text else {}
    if not isinstance(data, dict):
        raise ValueError("tools/quest_overrides.json: top level must be an object")
    return data


def write_overrides(data):
    """UTF-8, LF, sorted, written via a temp file (retried: OneDrive can briefly lock files)."""
    text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n" if data else "{}\n"
    tmp = OVERRIDES.with_suffix(".json.tmp")
    tmp.write_bytes(text.encode("utf-8"))
    for attempt in range(10):
        try:
            os.replace(tmp, OVERRIDES)
            return
        except PermissionError:
            time.sleep(0.1 * (attempt + 1))
    OVERRIDES.write_bytes(text.encode("utf-8"))
    tmp.unlink(missing_ok=True)


# --- data -------------------------------------------------------------------------------------
def version():
    """Changes whenever a file that feeds the quest data changes (or a chapter file appears/disappears)."""
    files = list((ROOT / "tools").glob("*.py")) + list((ROOT / "tools/quests").glob("*.py")) + \
        [OVERRIDES, ROOT / "test/ids.tsv", ROOT / "test/build_quest_preview.py"]
    stamps = []
    for f in files:
        try:
            stamps.append(f.stat().st_mtime_ns)
        except OSError:
            stamps.append(0)
    return f"{len(files)}-{max(stamps)}-{sum(stamps) % 1000003}"


def icon_url(item_id):
    return "/icon/" + urllib.parse.quote(item_id, safe=":") if item_id and bqp.icon_bytes(item_id) else None


def load_data(force=False):
    """(status, body bytes). Fresh subprocess per change, so edits to any quest file show up."""
    with _data_lock:
        v = version()
        if not force and _cache["version"] == v and _cache["body"]:
            return 200, _cache["body"]
        env = dict(os.environ, PYTHONUTF8="1")
        env.pop("QUEST_ONLY", None)
        p = subprocess.run([PY, str(ROOT / "test/build_quest_preview.py"), "--json"], cwd=ROOT, env=env,
                           capture_output=True)
        if p.returncode != 0:
            err = p.stderr.decode("utf-8", "replace")[-6000:]
            return 500, json.dumps({"ok": False, "error": "Loading the quest data failed (a chapter file may be "
                                    "mid-edit; try Refresh in a moment):\n\n" + err}).encode("utf-8")
        data = json.loads(p.stdout.decode("utf-8"))
        gen = {}
        for c in data["chapters"]:
            c["icon"] = icon_url(c.get("iconId"))
            banner = ROOT / f"pack/kubejs/assets/warbucks/textures/quests/{c['key']}.png"
            c["banner"] = f"/banner/{c['key']}.png" if banner.exists() else None
            for q in c["quests"]:
                gen[q["key"]] = q["gen"]
                for t in q["tasks"]:
                    if t["kind"] == "item":
                        t["icon"] = icon_url(t["id"])
                q["icon"] = next((t["icon"] for t in q["tasks"] if t.get("icon")), None)
        try:
            over = read_overrides()
        except ValueError as e:
            over = {}
            data["warnings"].append(str(e))
        data.update(ok=True, version=v, overrides=sorted(over), check=_last_check)
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        _cache.update(version=v, body=body, gen=gen)
        return 200, body


def gen_for(key):
    if key not in _cache["gen"]:
        load_data()
    return _cache["gen"].get(key)


# --- edits ------------------------------------------------------------------------------------
def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and abs(v) < 10000


def edit_move(body):
    key, x, y = body.get("key"), body.get("x"), body.get("y")
    g = gen_for(key) if isinstance(key, str) else None
    if g is None:
        return 400, {"ok": False, "error": f"unknown quest key {key!r}"}
    if not (num(x) and num(y)):
        return 400, {"ok": False, "error": "x and y must be numbers"}
    x, y = round(x * 2) / 2, round(y * 2) / 2
    with _lock:
        over = read_overrides()
        o = dict(over.get(key, {}))
        if x == g["x"] and y == g["y"]:  # dropped back on the generated spot
            o.pop("x", None)
            o.pop("y", None)
        else:
            o.update(x=x, y=y)
        _store(over, key, o)
        write_overrides(over)
    return 200, {"ok": True, "x": x, "y": y, "count": len(over)}


def edit_text(body):
    key = body.get("key")
    g = gen_for(key) if isinstance(key, str) else None
    if g is None:
        return 400, {"ok": False, "error": f"unknown quest key {key!r}"}
    if key.startswith("link:"):
        return 400, {"ok": False, "error": "quest links have no text of their own"}
    title, sub, desc = body.get("title", ""), body.get("subtitle", ""), body.get("desc", [])
    if not (isinstance(title, str) and isinstance(sub, str) and isinstance(desc, list) and all(isinstance(s, str) for s in desc)):
        return 400, {"ok": False, "error": "title/subtitle must be strings, desc a list of strings"}
    clean = lambda s: s.replace("\r", "")
    vals = {"title": clean(title), "subtitle": clean(sub), "desc": [clean(s) for s in desc]}
    with _lock:
        over = read_overrides()
        o = dict(over.get(key, {}))
        for f, v in vals.items():
            if v == g[f]:
                o.pop(f, None)
            else:
                o[f] = v
        _store(over, key, o)
        write_overrides(over)
    return 200, {"ok": True, "count": len(over), "fields": sorted(o)}


def edit_reset(body):
    key = body.get("key")
    with _lock:
        over = read_overrides()
        existed = over.pop(key, None) is not None if isinstance(key, str) else False
        write_overrides(over)
    return 200, {"ok": True, "removed": existed, "count": len(over)}


def _store(over, key, o):
    if o:
        over[key] = o
    else:
        over.pop(key, None)


def run_check():
    env = dict(os.environ, PYTHONUTF8="1")
    env.pop("QUEST_ONLY", None)
    env.pop("QUEST_OUT", None)
    p = subprocess.run([PY, str(BUILD), "--check"], cwd=ROOT, env=env, capture_output=True)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    _last_check.update(ok=p.returncode == 0, time=time.strftime("%H:%M:%S"),
                       summary=(lines[-1] if p.returncode == 0 and lines else "FAILED: " + (lines[0] if lines else "no output"))[:200])
    _cache["body"] = None  # so the next /api/data carries the new check result
    return 200, {"ok": p.returncode == 0, "output": out, "check": _last_check}


# --- push -------------------------------------------------------------------------------------
def packwiz():
    exe = pathlib.Path(os.environ.get("USERPROFILE", str(pathlib.Path.home()))) / "go/bin" / ("packwiz.exe" if os.name == "nt" else "packwiz")
    return str(exe) if exe.exists() else shutil.which("packwiz")


def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def edit_count():
    """How many override entries differ from the committed tools/quest_overrides.json."""
    rc, old = git("show", "HEAD:tools/quest_overrides.json")
    try:
        old = json.loads(old) if rc == 0 and old.strip() else {}
    except ValueError:
        old = {}
    new = read_overrides()
    return sum(1 for k in set(old) | set(new) if old.get(k) != new.get(k))


def push(write):
    """Each step streams its output through write(); stops at the first failure. Returns True on success."""
    env = dict(os.environ, PYTHONUTF8="1", PYTHONUNBUFFERED="1")
    env.pop("QUEST_ONLY", None)
    env.pop("QUEST_OUT", None)

    def step(title, cmd, cwd=ROOT):
        write(f"\n=== {title}\n$ {' '.join(cmd)}\n")
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout:
            write(line.decode("utf-8", "replace"))
        p.wait()
        if p.returncode != 0:
            write(f"\nFAILED: {title} (exit {p.returncode}). Stopped; nothing after this step ran.\n")
        return p.returncode == 0

    # Guard: pack/index.toml hashes every file under pack/, so other uncommitted pack/ changes would be
    # referenced by the pushed index without being pushed themselves.
    rc, st = git("status", "--porcelain", "--", "pack")
    mine = ("pack/config/ftbquests/", "pack/index.toml", "pack/pack.toml")
    other = [ln for ln in st.splitlines() if ln[3:].strip('"') and not ln[3:].strip('"').startswith(mine)]
    if rc != 0:
        write("FAILED: git status:\n" + st)
        return False
    if other:
        write("FAILED: pack/ has other uncommitted changes, and packwiz would put them in the pushed index:\n  "
              + "\n  ".join(other) + "\nCommit or revert those first (they are not quest files), then push again.\n")
        return False
    if not step("1/6 Check the quest book", [PY, str(BUILD), "--check"]):
        return False
    if not step("2/6 Build the quest book", [PY, str(BUILD)]):
        return False
    pw = packwiz()
    if not pw:
        write("FAILED: packwiz not found (expected %USERPROFILE%\\go\\bin\\packwiz.exe).\n")
        return False
    if not step("3/6 packwiz refresh", [pw, "refresh"], cwd=ROOT / "pack"):
        return False
    n = edit_count()
    if not step("4/6 git add (quest files only)", ["git", "add", "--", *PUSH_PATHS]):
        return False
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *PUSH_PATHS], cwd=ROOT).returncode != 0
    if staged:
        msg = f"Quest editor: {n} layout/text edit{'s' if n != 1 else ''}"
        # "-- paths" = commit ONLY these paths, even if something else happens to be staged.
        if not step("5/6 git commit", ["git", "commit", "-m", msg, "-m", TRAILER, "--", *PUSH_PATHS]):
            return False
    else:
        rc, ahead = git("rev-list", "--count", "@{u}..HEAD")
        if rc == 0 and ahead.strip() not in ("", "0"):
            write(f"\n=== 5/6 git commit\nNothing new to commit; {ahead.strip()} earlier commit(s) not pushed yet, pushing those.\n")
        else:
            write("\nNothing to commit: the quest book and tools/quest_overrides.json already match git. Nothing pushed.\n")
            return True
    if not step("6/6 git pull --rebase --autostash", ["git", "pull", "--rebase", "--autostash"]):
        return False
    if not step("6/6 git push", ["git", "push"]):
        return False
    write("\nPUSHED. Players get it on their next Prism launch; the live server on its next restart.\n")
    return True


# --- HTTP -------------------------------------------------------------------------------------
class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "QuestEditor/1"

    def log_message(self, fmt, *args):
        if args and str(args[1])[:1] in "45":
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _host_ok(self):
        host = (self.headers.get("Host") or "").lower()
        return host in (f"127.0.0.1:{PORT}", f"localhost:{PORT}")  # blocks DNS-rebinding pages

    def _send(self, status, body, ctype="application/json; charset=utf-8", cache=False):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "max-age=3600" if cache else "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self._host_ok():
            return self._send(403, {"ok": False, "error": "use http://localhost:%d" % PORT})
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            return self._send(200, PAGE, "text/html; charset=utf-8")
        if path == "/api/data":
            status, body = load_data(force="force=1" in (urllib.parse.urlparse(self.path).query or ""))
            return self._send(status, body)
        if path == "/api/version":
            return self._send(200, {"version": version()})
        if path.startswith("/icon/"):
            data = bqp.icon_bytes(urllib.parse.unquote(path[6:]))
            return self._send(200, data, "image/png", cache=True) if data else self._send(404, b"", "text/plain")
        if path.startswith("/banner/") and path.endswith(".png"):
            key = path[8:-4]
            f = ROOT / f"pack/kubejs/assets/warbucks/textures/quests/{key}.png"
            if key.replace("_", "").isalnum() and f.exists():
                return self._send(200, f.read_bytes(), "image/png")
            return self._send(404, b"", "text/plain")
        if path in ("/asset/logo.png", "/asset/bg.png"):
            f = ROOT / "pack/config/fancymenu/assets" / ("logo.png" if "logo" in path else "background.png")
            return self._send(200, f.read_bytes(), "image/png", cache=True)
        return self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        # Custom header + JSON content type: a page on another site can't send these without a CORS
        # preflight, which this server never answers, so only this editor's own page can make edits.
        if not self._host_ok() or self.headers.get("X-Quest-Editor") != "1" or \
                not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._send(403, {"ok": False, "error": "forbidden"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}") if n < 5_000_000 else None
            if not isinstance(body, dict):
                raise ValueError("body must be a JSON object")
        except ValueError as e:
            return self._send(400, {"ok": False, "error": f"bad request: {e}"})
        path = urllib.parse.urlparse(self.path).path
        try:
            if path == "/api/move":
                return self._send(*edit_move(body))
            if path == "/api/text":
                return self._send(*edit_text(body))
            if path == "/api/reset":
                return self._send(*edit_reset(body))
            if path == "/api/check":
                return self._send(*run_check())
            if path == "/api/push":
                return self._push(body)
        except ValueError as e:  # e.g. quest_overrides.json hand-edited into invalid JSON
            return self._send(500, {"ok": False, "error": str(e)})
        return self._send(404, {"ok": False, "error": "not found"})

    def _push(self, body):
        if body.get("confirm") is not True:
            return self._send(400, {"ok": False, "error": "push needs {\"confirm\": true}"})
        if not _push_lock.acquire(blocking=False):
            return self._send(409, {"ok": False, "error": "a push is already running"})
        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True

            def write(s):
                try:
                    self.wfile.write(s.encode("utf-8"))
                    self.wfile.flush()
                except OSError:
                    pass  # page closed: keep going, the steps must still finish cleanly
                sys.stdout.write(s)

            ok = push(write)
            write("\n__PUSH_RESULT__ " + ("OK" if ok else "FAILED") + "\n")
            _cache["body"] = None
        finally:
            _push_lock.release()


PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Quest Book Editor</title>
<style>__CSS__
header{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}header .ttl{flex:1;min-width:200px}
#bar{display:flex;gap:8px;align-items:center;font-size:12px;color:var(--muted)}
#bar b{color:var(--text);font-weight:600}#st.bad{color:#ff7a7a}#st.warn{color:var(--gold)}#st.good{color:#7ee2a8}
.btn{background:#12263a;border:1px solid #2b4a63;color:var(--text);border-radius:7px;padding:4px 10px;cursor:pointer;font:inherit;font-size:12px}
.btn:hover{border-color:var(--edge)}.btn.gold{border-color:var(--gold);color:var(--gold)}.btn:disabled{opacity:.45;cursor:default}
#canvas{background-image:linear-gradient(rgba(79,209,197,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(79,209,197,.06) 1px,transparent 1px)}
.q{touch-action:none;user-select:none}.q.drag{transition:none;transform:scale(1.12);border-color:var(--gold);z-index:5;cursor:grabbing}
.q.ov::after{content:"";position:absolute;right:-3px;top:-3px;width:9px;height:9px;border-radius:50%;background:var(--gold);box-shadow:0 0 4px #000}
aside label{display:block;margin:10px 0 3px;color:var(--edge);font-size:11px;letter-spacing:.08em;text-transform:uppercase}
aside input,aside textarea{width:100%;background:#0a1626;color:var(--text);border:1px solid #2b4a63;border-radius:6px;padding:6px 8px;font:13px/1.45 ui-monospace,Consolas,monospace}
aside textarea{resize:vertical;min-height:160px;white-space:pre;overflow-x:auto}
aside .row{display:flex;gap:8px;margin:12px 0}.meta{font-size:12px;color:var(--muted)}.legend{font-size:11px;color:var(--muted);margin-top:4px}
.legend code{background:#0a1626;padding:0 3px;border-radius:3px}.pv{border-left:2px solid #2b4a63;padding-left:8px;margin-top:6px}
#outbox{display:none;flex:none;max-height:38vh;border-top:1px solid #1d3247;background:rgba(5,9,18,.96)}#outbox.on{display:flex;flex-direction:column}
#outbox .h{display:flex;justify-content:space-between;align-items:center;padding:4px 10px;font-size:12px;color:var(--muted)}
#out{margin:0;padding:6px 12px 10px;overflow:auto;font:12px/1.4 ui-monospace,Consolas,monospace;white-space:pre-wrap;color:#cfe3f1}
dialog{background:var(--panel);color:var(--text);border:1px solid var(--gold);border-radius:12px;max-width:520px}
dialog::backdrop{background:rgba(0,0,0,.6)}dialog h3{margin-top:0;color:var(--gold)}dialog li{margin:4px 0}
</style></head><body>
<nav><img class="logo" src="/asset/logo.png" alt="Warbucks Chemistry"><div id="tabs"></div></nav>
<main><header><div class="ttl"><b id="ct"></b> <span class="sub" id="cs"></span></div>
<div id="bar"><span id="st">Loading...</span> | <span><b id="cnt">0</b> overrides</span> | <span>Check: <b id="chk">not run</b></span>
<button class="btn" id="bRefresh" title="Reload all quest data from the files">Refresh</button>
<button class="btn" id="bCheck" title="tools/build_quests.py --check">Check</button>
<button class="btn gold" id="bPush" title="Build, commit the quest files and push to GitHub">Push...</button></div></header>
<div id="map"><div id="canvas"></div></div>
<div id="outbox"><div class="h"><span id="outt">Output</span><button class="btn" id="bClose">Close</button></div><pre id="out"></pre></div></main>
<aside id="info"><p class="empty">Drag quests to move them (saved on drop). Click a quest to edit its text.</p></aside>
<dialog id="dlg"><h3>Push the quest book?</h3>
<p>This publishes the quest book as it is <b>right now</b> (every chapter file, plus your editor changes):</p>
<ul><li>Every player's Prism instance downloads it on its <b>next launch</b>.</li>
<li>The live server picks it up on its <b>next restart</b>.</li></ul>
<p class="meta">Steps (stops at the first failure): build_quests.py --check, build_quests.py, packwiz refresh, git add of the quest files only
(tools/quest_overrides.json, pack/config/ftbquests, docs/QUESTS.md, pack/index.toml, pack/pack.toml), git commit,
git pull --rebase --autostash, git push.</p>
<div class="row"><button class="btn gold" id="dOk">Push</button><button class="btn" id="dNo">Cancel</button></div></dialog>
<script>
const U=64, M=4, $=id=>document.getElementById(id);
let D=[], OV=new Set(), cur=null, sel=null, dirty=false, dragging=false, loading=false, ver=null, frame=null, nodes={}, edges=[], chap=null;
const snap=v=>Math.round(v*2)/2;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function fmt(t){t=esc(t);t=t.replace(/&amp;e(.*?)(&amp;r|$)/g,'<b class="k">$1</b>').replace(/&amp;6(.*?)(&amp;r|$)/g,'<b class="g">$1</b>');return t.replace(/&amp;[0-9a-fk-or]/g,'')}
function setState(t,cls){const s=$('st');s.textContent=t;s.className=cls||''}
function out(title,text,append){$('outbox').classList.add('on');$('outt').textContent=title;const o=$('out');o.textContent=append?o.textContent+text:text;o.scrollTop=o.scrollHeight}
async function api(path,body){try{const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Quest-Editor':'1'},body:JSON.stringify(body||{})});
 const j=await r.json().catch(()=>({ok:false,error:'HTTP '+r.status}));if(!r.ok)j.ok=false;return j}catch(e){return{ok:false,error:String(e)}}}
function showCheck(c){if(!c||c.ok===null){$('chk').textContent='not run';return}$('chk').textContent=(c.ok?'OK':'FAILED')+' at '+c.time;$('chk').title=c.summary;$('chk').style.color=c.ok?'#7ee2a8':'#ff7a7a'}

async function load(force){
 if(loading)return;loading=true;if(!dirty)setState('Loading...','warn');
 try{const r=await fetch('/api/data'+(force?'?force=1':''));const j=await r.json();
  if(!j.ok){setState('Load failed (see output)','bad');out('Load error',j.error);return}
  D=j.chapters;OV=new Set(j.overrides);ver=j.version;$('cnt').textContent=OV.size;showCheck(j.check);
  if(j.warnings&&j.warnings.length)out('Override warnings',j.warnings.join('\n'));
  tabs();let i=D.findIndex(c=>c.key==cur);show(i<0?0:i,true);
  if(sel&&!dirty){const n=nodes[sel];if(n){n.el.classList.add('sel');info(n.q)}else{sel=null;$('info').innerHTML='<p class="empty">Click a quest to edit it.</p>'}}
  if(!dirty)setState('Saved, up to date','good')}
 catch(e){setState('Load failed: '+e,'bad')}finally{loading=false}}
function tabs(){const t=$('tabs');t.innerHTML='';const g={};D.forEach((c,i)=>{(g[c.group]=g[c.group]||[]).push(i)});
 for(const k in g){const h=document.createElement('h3');h.textContent=k;t.appendChild(h);
  g[k].forEach(i=>{const c=D[i],b=document.createElement('button');b.innerHTML=(c.icon?`<img src="${c.icon}">`:'')+esc(c.title);b.onclick=()=>{if(dirty&&!confirm('Discard unsaved text changes?'))return;dirty=false;sel=null;show(i)};b.id='tab'+i;if(c.key==cur)b.classList.add('on');t.appendChild(b)})}}
function bannerPos(c){let l=1e9,t=1e9;c.quests.forEach(q=>{const s=q.link?1:q.size;l=Math.min(l,q.x-s/2);t=Math.min(t,q.y-s/2)});return[l+3,t-1.5]}
const P=(x,y)=>[(x-frame.minx)*U,(y-frame.miny)*U];
function show(i,keep){const c=D[i],map=$('map');let wx=null,wy=null;
 if(keep&&frame&&chap&&chap.key==c.key){wx=map.scrollLeft/U+frame.minx;wy=map.scrollTop/U+frame.miny}
 chap=c;cur=c.key;document.querySelectorAll('nav button').forEach(b=>b.classList.remove('on'));const tb=$('tab'+i);if(tb)tb.classList.add('on');
 $('ct').textContent=c.title+(c.manual?' (manual layout)':'');$('cs').innerHTML=c.sub.join(' ');
 const[bx,by]=bannerPos(c),xs=c.quests.map(q=>q.x),ys=c.quests.map(q=>q.y);
 frame={minx:Math.floor(Math.min(...xs,bx-3))-M,miny:Math.floor(Math.min(...ys,by-0.5))-M-(c.key=='welcome'?3:0),maxx:Math.ceil(Math.max(...xs,bx+3))+M,maxy:Math.ceil(Math.max(...ys))+M};
 const W=(frame.maxx-frame.minx)*U,H=(frame.maxy-frame.miny)*U,cv=$('canvas');cv.style.width=W+'px';cv.style.height=H+'px';cv.innerHTML='';
 cv.style.backgroundSize=`${U/2}px ${U/2}px`;cv.style.backgroundPosition='0 0';
 if(c.banner){const im=document.createElement('img');im.className='banner';im.id='banner';im.src=c.banner;im.style.width=6*U+'px';im.style.height=U+'px';cv.appendChild(im)}
 if(c.key=='welcome'){const im=document.createElement('img');im.className='banner';im.id='logo';im.src='/asset/logo.png';im.style.width=7*U+'px';cv.appendChild(im)}
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('width',W);svg.setAttribute('height',H);cv.appendChild(svg);
 nodes={};edges=[];const byKey={};c.quests.forEach(q=>{if(!q.link)byKey[q.key]=q});c.quests.forEach(q=>{if(q.link&&!byKey[q.linkOf])byKey[q.linkOf]=q});
 c.quests.forEach(q=>q.deps.forEach(d=>{const p=byKey[d];if(!p)return;const l=document.createElementNS(svg.namespaceURI,'line');
  l.setAttribute('stroke','#4fd1c5');l.setAttribute('stroke-opacity',p.link?'.35':'.55');l.setAttribute('stroke-width','3');if(p.link)l.setAttribute('stroke-dasharray','6 5');
  svg.appendChild(l);edges.push({a:p,b:q,l})}));
 c.quests.forEach(q=>{const el=document.createElement('div');el.className='q '+q.shape+(q.link?' link':'')+(OV.has(q.key)?' ov':'');el.title=q.title+(OV.has(q.key)?' (edited)':'');
  el.innerHTML=q.icon?`<img src="${q.icon}" draggable="false">`:'<span>&#10003;</span>';const lb=document.createElement('div');lb.className='lbl';lb.textContent=q.title;
  cv.appendChild(el);cv.appendChild(lb);nodes[q.key]={q,el,lb};place(q.key);el.addEventListener('pointerdown',e=>drag(e,q))});
 edges.forEach(drawEdge);drawBanner();
 if(wx!==null){map.scrollLeft=(wx-frame.minx)*U;map.scrollTop=(wy-frame.miny)*U}else{map.scrollLeft=0;map.scrollTop=0}}
function place(k){const n=nodes[k],q=n.q,s=q.size*U*0.8,[x,y]=P(q.x,q.y);n.el.style.width=n.el.style.height=s+'px';n.el.style.left=(x-s/2)+'px';n.el.style.top=(y-s/2)+'px';
 n.lb.style.left=x+'px';n.lb.style.top=(y+s/2+2)+'px'}
function drawEdge(e){const[a,b]=P(e.a.x,e.a.y),[c,d]=P(e.b.x,e.b.y);e.l.setAttribute('x1',a);e.l.setAttribute('y1',b);e.l.setAttribute('x2',c);e.l.setAttribute('y2',d)}
function drawBanner(){const[bx,by]=bannerPos(chap),b=$('banner'),lg=$('logo');if(b){const[x,y]=P(bx-3,by-0.5);b.style.left=x+'px';b.style.top=y+'px'}
 if(lg){const[x,y]=P(bx-3,by-3.285);lg.style.left=x+'px';lg.style.top=y+'px'}}
function drag(e,q){if(e.button!==0)return;e.preventDefault();const n=nodes[q.key],sx=e.clientX,sy=e.clientY,ox=q.x,oy=q.y;let moved=false;
 n.el.setPointerCapture(e.pointerId);
 const mv=ev=>{if(!moved&&Math.hypot(ev.clientX-sx,ev.clientY-sy)<5)return;
  if(!moved){moved=true;dragging=true;n.el.classList.add('drag')}
  const nx=snap(ox+(ev.clientX-sx)/U),ny=snap(oy+(ev.clientY-sy)/U);if(nx==q.x&&ny==q.y)return;q.x=nx;q.y=ny;place(q.key);
  edges.forEach(ed=>{if(ed.a===q||ed.b===q)drawEdge(ed)});drawBanner();setState(`Moving ${q.key} to ${nx}, ${ny}`,'warn')};
 const up=async()=>{n.el.removeEventListener('pointermove',mv);n.el.removeEventListener('pointerup',up);n.el.removeEventListener('pointercancel',up);
  n.el.classList.remove('drag');dragging=false;
  if(!moved){pick(q.key);return}
  if(q.x==ox&&q.y==oy){setState('Not moved','good');return}
  setState('Saving position...','warn');const r=await api('/api/move',{key:q.key,x:q.x,y:q.y});
  if(r.ok){setState('Saved','good');await load()}else{q.x=ox;q.y=oy;place(q.key);edges.forEach(drawEdge);drawBanner();setState('Save failed','bad');out('Save failed',r.error||'')}};
 n.el.addEventListener('pointermove',mv);n.el.addEventListener('pointerup',up);n.el.addEventListener('pointercancel',up)}
function pick(k){if(k!==sel&&dirty&&!confirm('Discard unsaved text changes?'))return;if(k!==sel)dirty=false;
 document.querySelectorAll('.q.sel').forEach(e=>e.classList.remove('sel'));sel=k;nodes[k].el.classList.add('sel');info(nodes[k].q)}
function info(q){const box=$('info'),g=q.gen||{},ov=OV.has(q.key),all=D.flatMap(x=>x.quests);
 const reqs=q.deps.map(d=>all.find(z=>z.key==d)).filter(Boolean).map(z=>esc(z.title));
 let h=`<h2>${esc(q.title)}</h2><div class="meta">${esc(q.key)}<br>Position ${q.x}, ${q.y}`+(g.x!==undefined&&(g.x!=q.x||g.y!=q.y)?` (generated ${g.x}, ${g.y})`:'')+
  (ov?' | <b style="color:var(--gold)">edited</b>':'')+(chap.manual?'':'<br>Auto-layout chapter: a moved quest stays where you put it.')+'</div>';
 if(q.link){h+=`<p>${q.desc[0]}</p><p class="meta">Quest link: only its position can change.</p>`}
 else{h+=`<label>Title</label><input id="fT" spellcheck="true"><label>Subtitle</label><input id="fS">
  <label>Description (one line per row)</label><textarea id="fD" rows="12" spellcheck="true"></textarea>
  <div class="legend">Codes stay as text: <code>&amp;e</code> <span class="k">key term</span>, <code>&amp;6</code> <span class="g">story</span>, <code>&amp;r</code> reset,
  <code>&amp;a</code> green, <code>&amp;c</code> red, <code>&amp;b</code> aqua, <code>&amp;l</code> bold, <code>&amp;o</code> italic. Empty row = blank line,
  <code>{@pagebreak}</code> = new page. An empty title shows the item name.</div><div class="pv" id="pv"></div>`}
 h+=`<div class="row">${q.link?'':'<button class="btn gold" id="bSave">Save</button>'}<button class="btn" id="bReset" ${ov?'':'disabled'}>Reset to generated</button></div>`;
 if(q.tasks.length)h+='<h4>Tasks</h4>'+q.tasks.map(t=>`<div class="t">${t.icon?`<img src="${t.icon}">`:''}${t.n>1?t.n+'x ':''}${esc(t.name)}</div>`).join('');
 if(q.rewards.length)h+='<h4>Rewards</h4>'+q.rewards.map(r=>`<div class="t">${esc(r)}</div>`).join('');
 if(reqs.length)h+='<h4>Requires</h4><p>'+reqs.join(', ')+'</p>';
 box.innerHTML=h;
 if(!q.link){$('fT').value=q.raw.title;$('fS').value=q.raw.subtitle;$('fD').value=q.raw.desc.join('\n');preview();
  ['fT','fS','fD'].forEach(id=>$(id).addEventListener('input',()=>{dirty=true;setState('Unsaved text changes','warn');preview()}));$('bSave').onclick=()=>save(q)}
 $('bReset').onclick=()=>reset(q)}
function preview(){const t=$('fT').value,s=$('fS').value,d=$('fD').value.split('\n');
 $('pv').innerHTML=(t?`<p><b>${fmt(t)}</b></p>`:'')+(s?`<p class="empty">${fmt(s)}</p>`:'')+d.map(x=>x=='{@pagebreak}'?'<hr>':x?`<p>${fmt(x)}</p>`:'<br>').join('')}
async function save(q){setState('Saving text...','warn');
 const r=await api('/api/text',{key:q.key,title:$('fT').value,subtitle:$('fS').value,desc:$('fD').value.split('\n')});
 if(r.ok){dirty=false;setState('Saved','good');await load()}else{setState('Save failed','bad');out('Save failed',r.error||'')}}
async function reset(q){if(!confirm('Reset "'+q.title+'" to the generated position and text?'))return;
 const r=await api('/api/reset',{key:q.key});if(r.ok){dirty=false;setState('Reset','good');await load()}else{setState('Reset failed','bad');out('Reset failed',r.error||'')}}
$('bRefresh').onclick=()=>{if(dirty&&!confirm('Discard unsaved text changes?'))return;dirty=false;load(true)};
$('bCheck').onclick=async()=>{const b=$('bCheck');b.disabled=true;setState('Checking...','warn');out('Check','Running tools/build_quests.py --check ...\n');
 const r=await api('/api/check');b.disabled=false;out('Check: '+(r.ok?'OK':'FAILED'),r.output||r.error||'');showCheck(r.check);setState(r.ok?'Check passed':'Check FAILED',r.ok?'good':'bad')};
$('bClose').onclick=()=>$('outbox').classList.remove('on');
$('bPush').onclick=()=>{if(dirty){alert('Save or discard your text changes first.');return}$('dlg').showModal()};
$('dNo').onclick=()=>$('dlg').close();
$('dOk').onclick=async()=>{$('dlg').close();const b=$('bPush');b.disabled=true;$('bCheck').disabled=true;setState('Pushing...','warn');out('Push','');
 try{const r=await fetch('/api/push',{method:'POST',headers:{'Content-Type':'application/json','X-Quest-Editor':'1'},body:JSON.stringify({confirm:true})});
  if(!r.ok){const j=await r.json().catch(()=>({error:'HTTP '+r.status}));out('Push refused',j.error);setState('Push refused','bad');return}
  const rd=r.body.getReader(),dec=new TextDecoder();let all='';
  for(;;){const{done,value}=await rd.read();if(done)break;const s=dec.decode(value,{stream:true});all+=s;out('Push (running)',s.replace(/\n__PUSH_RESULT__.*\n?/,''),true)}
  const ok=/__PUSH_RESULT__ OK/.test(all);out(ok?'Push: done':'Push: FAILED','',true);setState(ok?'Push finished':'Push FAILED',ok?'good':'bad')}
 catch(e){out('Push error',String(e),true);setState('Push error','bad')}finally{b.disabled=false;$('bCheck').disabled=false;load()}};
setInterval(async()=>{if(dragging||loading)return;try{const v=(await (await fetch('/api/version')).json()).version;
 if(v!==ver){if(dirty)setState('Files changed on disk: save, then they load','warn');else load()}}catch(e){setState('Server not reachable','bad')}},4000);
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue=''}});
load();
</script></body></html>""".replace("__CSS__", bqp.CSS.replace("__BG__", "/asset/bg.png"))


def main():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    srv.daemon_threads = True
    print(f"Quest editor on http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
