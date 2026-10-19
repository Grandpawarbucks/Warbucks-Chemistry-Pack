#!/usr/bin/env python3
"""Build test/preview/index.html: a browsable mock of the in-game quest book (chapter tabs,
banners, quest nodes with item icons, dependency lines, quest text on click).

Icons come from the mod jars in test/server/mods, so the output stays in git-ignored test/
(mod textures must not be published in the public repo).
Positions and text are the real build's: automatic layout (tools/layout.py), then the quest editor's
overrides (tools/quest_overrides.json). To EDIT the book, use tools/quest_editor.py instead.
Usage: python3 test/build_quest_preview.py          then open http://localhost:8765 (python3 -m http.server)
       python3 test/build_quest_preview.py --json   print the quest data as JSON (icons as item ids; used by the editor)
       python3 test/build_quest_preview.py --gallery [--cell 24] [--chapters a,b] [--book <quests folder>]
           renders every chapter of the FINAL generated SNBT (pack/config/ftbquests/quests) as one PNG per chapter
           (test/preview/gallery/<chapter>.png: FTB shapes and sizes, item icons from the jars, dependency lines and
           quest links, banners and section images, optional quests dimmed) plus test/preview/gallery.html
           (thumbnails grouped by tab, click to enlarge, tools/layout_lint.py score and issues under each).
           Icons are cached in test/preview/icons. Open gallery.html directly in a browser (no server needed).
"""
import base64
import glob
import html
import json
import math
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OUT = ROOT / "test/preview/index.html"
_PRISM = {"darwin": "Library/Application Support/PrismLauncher", "win32": "AppData/Roaming/PrismLauncher"}.get(
    sys.platform, ".local/share/PrismLauncher")
VANILLA = pathlib.Path.home() / _PRISM / "libraries/com/mojang/minecraft/1.21.1/minecraft-1.21.1-client.jar"
_jar_list = None
_names = None
_icon_cache = {}


def _jars():
    """The mod jars (and the vanilla client jar if Prism has it), opened once on first use."""
    global _jar_list
    if _jar_list is None:
        _jar_list = [zipfile.ZipFile(j) for j in glob.glob(str(ROOT / "test/server/mods/*.jar"))]
        if VANILLA.exists():
            _jar_list.append(zipfile.ZipFile(VANILLA))
    return _jar_list


def names():
    """Item/entity id -> display name, from test/ids.tsv."""
    global _names
    if _names is None:
        _names = {}
        for line in (ROOT / "test/ids.tsv").read_text(encoding="utf-8").splitlines():
            i, t, n = (line.split("\t") + ["", ""])[:3]
            if n or i not in _names:  # registry rows (build_id_index.py) have no name: keep the lang one
                _names[i] = _names.get(i) or n
    return _names


def icon_bytes(item_id):
    """PNG bytes of an item's texture (item/, then block/ variants), or None."""
    if item_id in _icon_cache:
        return _icon_cache[item_id]
    if ":" not in item_id:
        return None
    ns, path = item_id.split(":", 1)
    if ns == "kubejs":
        src = (ROOT / "pack/kubejs/startup_scripts/chemistry_items.js").read_text(encoding="utf-8")
        m = re.search(rf"create\('{re.escape(path)}'\).*?texture\('minecraft:item/([a-z_]+)'\)", src)
        ns, path = ("minecraft", m.group(1)) if m else (ns, path)
    cands = [f"assets/{ns}/textures/item/{path}.png"] + [
        f"assets/{ns}/textures/block/{path}{suf}.png" for suf in ("", "_front", "_side", "_top", "_overlay", "_0")]
    for c in cands:
        for z in _jars():
            try:
                data = z.read(c)
            except KeyError:
                continue
            _icon_cache[item_id] = data
            return data
    _icon_cache[item_id] = None
    return None


def icon(item_id):
    """Data URI for an item's texture, or None."""
    data = icon_bytes(item_id)
    return "data:image/png;base64," + base64.b64encode(data).decode() if data else None


def strip_codes(t):
    return re.sub(r"&[0-9a-fk-or]", "", t)


def fmt(t):
    """FTB & colour codes -> spans."""
    t = html.escape(t)
    t = re.sub(r"&amp;e(.*?)(&amp;r|$)", r'<b class="k">\1</b>', t)
    t = re.sub(r"&amp;6(.*?)(&amp;r|$)", r'<b class="g">\1</b>', t)
    return re.sub(r"&amp;[0-9a-fk-or]", "", t)


def b64file(p):
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def collect(icon_fn=icon):
    """The whole book as preview data: [chapter dicts], warnings. Same positions and text as the real build
    (layout, then tools/quest_overrides.json). icon_fn(item_id) gives each icon (data URI, URL or None)."""
    from quest_data import CHAPTERS, GROUPS, apply_overrides  # imported here so --json always reads fresh files
    import layout
    NAMES = names()
    book_keys = {q.key for c in CHAPTERS for q in c.quests}
    try:  # shapes and sizes by role (tools/quest_style.py), BEFORE the layout, as tools/build_quests.py does
        import quest_style
    except ImportError:
        quest_style = None
    for c in CHAPTERS:
        if quest_style is not None:
            quest_style.apply(c)
        layout.apply(c, book_keys)
    gen = {q.key: {"title": q.title or "", "subtitle": q.subtitle or "", "desc": list(q.desc), "x": q.x, "y": q.y}
           for c in CHAPTERS for q in c.quests}
    gen.update({f"link:{c.key}:{lk}": {"x": lx, "y": ly} for c in CHAPTERS for lk, lx, ly in c.links})
    try:
        warnings = apply_overrides(CHAPTERS)
    except ValueError as e:
        warnings = [f"tools/quest_overrides.json is not valid, overrides NOT applied: {e}"]
    home = {q.key: c.title for c in CHAPTERS for q in c.quests}
    titles = {q.key: (q.title or NAMES.get(q.tasks[0][1], q.tasks[0][1]) if q.tasks[0][0] == "item" else q.title or q.key)
              for c in CHAPTERS for q in c.quests}
    chapters = []
    for c in CHAPTERS:
        qs = []
        for q in c.quests:
            tasks = []
            for t in q.tasks:
                if t[0] == "item":
                    tasks.append({"kind": "item", "id": t[1], "n": t[2], "name": NAMES.get(t[1], t[1]), "icon": icon_fn(t[1])})
                elif t[0] == "dimension":
                    tasks.append({"kind": "dim", "id": t[1], "name": "Visit " + t[1].split(":")[1].replace("_", " ").title()})
                elif t[0] == "kill":
                    tasks.append({"kind": "kill", "id": t[1], "name": f"Kill {t[2]}x " + NAMES.get(t[1], t[1].split(":")[1].replace("_", " ").title())})
                elif t[0] in ("structure", "biome"):
                    tasks.append({"kind": t[0], "id": t[1], "name": f"Find {t[0]}: " + t[1].split(":")[1].split("/")[-1].replace("_", " ").title()})
                elif t[0] == "filter":
                    tasks.append({"kind": "filter", "id": t[1], "name": f"{t[2]}x any of: {t[1]}"})
                else:
                    tasks.append({"kind": "check", "name": "Checkmark"})
            first_icon = next((t["icon"] for t in tasks if t.get("icon")), None)
            tokens = q.tokens if q.tokens is not None else c.tokens * (2 if (q.size or 1) >= 1.5 else 1)
            rewards = ([f"{tokens} Demigod Token" + ("s" if tokens != 1 else "")] if tokens else []) + \
                      ([f"{q.xp} XP"] if q.xp else []) + [f"{n}x {NAMES.get(i, i)}" for i, n in q.items] + \
                      ([f"Loot roll: {q.loot}"] if q.loot else []) + ([f"Choose one: {q.choice}"] if q.choice else [])
            qs.append({"key": q.key, "x": q.x, "y": q.y, "size": q.size or 1.0, "shape": q.shape or ("rsquare" if c.group == "main" else "circle"),
                       "title": strip_codes(titles[q.key]), "desc": [fmt(d) if d != "{@pagebreak}" else "<hr>" for d in q.desc],
                       "sub": fmt(q.subtitle) if q.subtitle else "", "deps": q.deps,
                       "tasks": tasks, "rewards": rewards, "icon": first_icon,
                       "hideLines": bool(getattr(q, "hide_lines", False)), "hideDeps": bool(getattr(q, "hide_dependents", False)),
                       "raw": {"title": q.title or "", "subtitle": q.subtitle or "", "desc": list(q.desc)}, "gen": gen[q.key]})
        # Quest links (shortcuts to quests in other chapters) as faded nodes in the link column.
        byq = {q.key: q for cc in CHAPTERS for q in cc.quests}
        for lk, lx, ly in c.links:
            k = f"link:{c.key}:{lk}"
            lq = byq.get(lk)  # FTB: a link button also draws its quest's own dependency lines (size 1.0 by default)
            qs.append({"key": k, "linkOf": lk, "x": lx, "y": ly, "size": 1.0, "shape": "circle", "link": True,
                       "linkDeps": list(lq.deps) if lq else [], "hideLines": bool(getattr(lq, "hide_lines", False)),
                       "hideDeps": bool(getattr(lq, "hide_dependents", False)),
                       "title": "Link: " + strip_codes(titles.get(lk, lk)), "desc": [html.escape(f"Shortcut to a quest in {home.get(lk, 'another chapter')}.")],
                       "sub": "", "deps": [], "tasks": [], "rewards": [], "icon": None, "gen": gen.get(k, {"x": lx, "y": ly})})
        bx, by = layout.banner(c)
        chapters.append({"key": c.key, "title": c.title, "group": GROUPS[c.group] or "Start here", "sub": [fmt(s) for s in c.subtitle],
                         "iconId": c.icon, "icon": icon_fn(c.icon), "manual": getattr(c, "layout", "auto") == "manual",
                         "bx": bx, "by": by, "quests": qs,
                         "sections": [{k: h[k] for k in ("title", "slug", "x", "y", "w", "h")} for h in getattr(c, "sections", [])]})
    return chapters, warnings


def main():
    if "--gallery" in sys.argv:
        return gallery_main()
    from quest_data import BOOK_TITLE
    if "--json" in sys.argv:
        chapters, warnings = collect(icon_fn=lambda i: None)
        out = json.dumps({"title": BOOK_TITLE, "chapters": chapters, "warnings": warnings}, ensure_ascii=False)
        sys.stdout.buffer.write(out.encode("utf-8"))
        return
    chapters, warnings = collect()
    for w in warnings:
        print("WARNING: " + w)
    for c in chapters:
        banner = ROOT / f"pack/kubejs/assets/warbucks/textures/quests/{c['key']}.png"
        c["banner"] = b64file(banner) if banner.exists() else None
        for h in c["sections"]:
            art = ROOT / f"pack/kubejs/assets/warbucks/textures/quests/sections/{c['key']}_{h['slug']}.png"
            h["img"] = b64file(art) if art.exists() else None
    logo = b64file(ROOT / "pack/config/fancymenu/assets/logo.png")
    bg = b64file(ROOT / "pack/config/fancymenu/assets/background.png")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.replace("__CSS__", CSS).replace("__DATA__", json.dumps(chapters)).replace("__LOGO__", logo)
                   .replace("__BG__", bg).replace("__TITLE__", html.escape(BOOK_TITLE)), encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(chapters)} chapters, {sum(len(c['quests']) for c in chapters)} quests)")


# Shared with tools/quest_editor.py (same look). __BG__ is the background image URL.
CSS = r"""
:root{--bg:#080e1e;--panel:#0d1a2b;--edge:#4fd1c5;--gold:#f2b544;--text:#ecf2f8;--muted:#8fa3b8}
*{box-sizing:border-box}body{margin:0;background:var(--bg) url(__BG__) center/cover fixed;color:var(--text);
font:14px/1.45 "Avenir Next",system-ui,sans-serif;display:flex;height:100vh}
nav{width:250px;flex:none;background:rgba(8,14,30,.88);border-right:1px solid #1d3247;overflow:auto;padding:12px}
nav img.logo{width:100%;margin-bottom:8px}nav h3{color:var(--gold);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin:14px 6px 6px}
nav button{display:flex;gap:8px;align-items:center;width:100%;text-align:left;background:none;border:1px solid transparent;color:var(--text);
padding:6px 8px;border-radius:8px;cursor:pointer;font:inherit}nav button:hover{background:#12263a}nav button.on{border-color:var(--edge);background:#11303a}
nav button img{width:20px;height:20px;image-rendering:pixelated}
main{flex:1;display:flex;flex-direction:column;min-width:0}
header{padding:10px 16px;background:rgba(8,14,30,.75);border-bottom:1px solid #1d3247}header .sub{color:var(--muted)}
#map{flex:1;position:relative;overflow:auto}#canvas{position:relative;margin:24px}
.banner{position:absolute;image-rendering:auto;border-radius:10px}
svg{position:absolute;left:0;top:0;pointer-events:none}
.q{position:absolute;display:flex;align-items:center;justify-content:center;background:#132a3c;border:2px solid #3b6b80;cursor:pointer;transition:transform .1s}
.q:hover{transform:scale(1.08);border-color:var(--edge)}.q.sel{border-color:var(--gold);box-shadow:0 0 14px var(--gold)}
.q img{image-rendering:pixelated;width:62%;height:62%;pointer-events:none}.q span{font-size:11px;color:var(--muted)}
.q.rsquare{border-radius:22%}.q.circle{border-radius:50%}.q.hexagon{clip-path:polygon(25% 3%,75% 3%,100% 50%,75% 97%,25% 97%,0 50%);background:#1a3a4c;border:none}
.q.gear{border-radius:50%;border:3px dashed var(--gold);background:#2a2412}
.lbl{position:absolute;font-size:11px;color:var(--text);text-align:center;transform:translateX(-50%);white-space:nowrap;text-shadow:0 1px 2px #000;pointer-events:none}
aside{width:360px;flex:none;background:rgba(8,14,30,.92);border-left:1px solid #1d3247;overflow:auto;padding:16px}
aside h2{margin:0 0 4px;color:var(--gold);font-size:18px}aside .t{display:flex;gap:8px;align-items:center;margin:4px 0}
aside .t img{width:24px;height:24px;image-rendering:pixelated}aside h4{margin:14px 0 4px;color:var(--edge);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.q.link{opacity:.55;border-style:dashed}
.k{color:#ffe27a}.g{color:var(--gold)}aside p{margin:6px 0}.empty{color:var(--muted)}
@media (max-width:900px){body{flex-direction:column}nav{width:auto;height:30vh}aside{width:auto;height:35vh}}
"""

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Quest Book Preview</title>
<style>__CSS__</style></head><body>
<nav><img class="logo" src="__LOGO__" alt="Warbucks Chemistry"><div id="tabs"></div></nav>
<main><header><b id="ct"></b> <span class="sub" id="cs"></span></header><div id="map"><div id="canvas"></div></div></main>
<aside id="info"><p class="empty">Click a quest to read it.</p></aside>
<script>
const D=__DATA__, U=64;
const tabs=document.getElementById('tabs'); let groups={};
D.forEach((c,i)=>{(groups[c.group]=groups[c.group]||[]).push(i)});
for(const g in groups){const h=document.createElement('h3');h.textContent=g;tabs.appendChild(h);
 groups[g].forEach(i=>{const c=D[i],b=document.createElement('button');b.innerHTML=(c.icon?`<img src="${c.icon}">`:'')+c.title;b.onclick=()=>show(i);b.id='tab'+i;tabs.appendChild(b)})}
function show(i){const c=D[i];document.querySelectorAll('nav button').forEach(b=>b.classList.remove('on'));document.getElementById('tab'+i).classList.add('on');
 document.getElementById('ct').textContent=c.title;document.getElementById('cs').innerHTML=c.sub.join(' ');
 const S=c.sections||[],xs=c.quests.map(q=>q.x).concat(S.map(h=>h.x-h.w/2),S.map(h=>h.x+h.w/2)),ys=c.quests.map(q=>q.y).concat(S.map(h=>h.y-h.h/2)),minx=Math.min(...xs,c.bx-3),miny=Math.min(...ys,c.by-0.5)-(c.key=='welcome'?3:1),maxx=Math.max(...xs,c.bx+3),maxy=Math.max(...ys);
 const W=(maxx-minx+3)*U,H=(maxy-miny+3)*U,cv=document.getElementById('canvas');cv.style.width=W+'px';cv.style.height=H+'px';cv.innerHTML='';
 const P=(x,y)=>[(x-minx+1)*U,(y-miny+1)*U];
 if(c.banner){const im=document.createElement('img');im.className='banner';im.src=c.banner;const[bx,by]=P(c.bx-3,c.by-0.5);
  im.style.left=bx+'px';im.style.top=by+'px';im.style.width=6*U+'px';im.style.height=U+'px';cv.appendChild(im)}
 if(c.key=='welcome'){const im=document.createElement('img');im.className='banner';im.src=document.querySelector('nav img.logo').src;const[bx,by]=P(c.bx-3,c.by-3.285);im.style.left=bx+'px';im.style.top=by+'px';im.style.width=7*U+'px';cv.appendChild(im)}
 S.forEach(h=>{if(!h.img)return;const im=document.createElement('img');im.className='banner';im.src=h.img;im.title=h.title;const[hx,hy]=P(h.x-h.w/2,h.y-h.h/2);
  im.style.left=hx+'px';im.style.top=hy+'px';im.style.width=h.w*U+'px';im.style.height=h.h*U+'px';cv.appendChild(im)});
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('width',W);svg.setAttribute('height',H);cv.appendChild(svg);
 const byKey={};c.quests.forEach(q=>{if(!q.link)byKey[q.key]=q});c.quests.forEach(q=>{if(q.link)byKey[q.linkOf]=q});
 c.quests.forEach(q=>(q.link?(q.linkDeps||[]):q.deps).forEach(d=>{const p=byKey[d];if(!p||q.hideLines||p.hideDeps)return;const[a,b]=P(p.x,p.y),[e,f]=P(q.x,q.y);
  const l=document.createElementNS(svg.namespaceURI,'line');l.setAttribute('x1',a);l.setAttribute('y1',b);l.setAttribute('x2',e);l.setAttribute('y2',f);
  l.setAttribute('stroke','#4fd1c5');l.setAttribute('stroke-opacity','.55');l.setAttribute('stroke-width','3');svg.appendChild(l)}));
 c.quests.forEach(q=>{const s=q.size*U*0.8,[x,y]=P(q.x,q.y),el=document.createElement('div');el.className='q '+q.shape+(q.link?' link':'');
  el.style.width=el.style.height=s+'px';el.style.left=(x-s/2)+'px';el.style.top=(y-s/2)+'px';el.title=q.title;
  el.innerHTML=q.icon?`<img src="${q.icon}">`:'<span>✓</span>';el.onclick=()=>{document.querySelectorAll('.q').forEach(e=>e.classList.remove('sel'));el.classList.add('sel');info(q,c)};cv.appendChild(el);
  const lb=document.createElement('div');lb.className='lbl';lb.textContent=q.title;lb.style.left=x+'px';lb.style.top=(y+s/2+2)+'px';cv.appendChild(lb)})}
function info(q,c){const ext=q.deps.map(d=>D.flatMap(x=>x.quests).find(z=>z.key==d)).filter(Boolean).map(z=>z.title);
 document.getElementById('info').innerHTML=`<h2>${q.title}</h2>`+(q.sub?`<p class="empty">${q.sub}</p>`:'')+q.desc.map(d=>d?`<p>${d}</p>`:'<br>').join('')+
 '<h4>Tasks</h4>'+q.tasks.map(t=>`<div class="t">${t.icon?`<img src="${t.icon}">`:''}${t.n>1?t.n+'x ':''}${t.name}</div>`).join('')+
 (q.rewards.length?'<h4>Rewards</h4>'+q.rewards.map(r=>`<div class="t">${r}</div>`).join(''):'')+(ext.length?'<h4>Requires</h4><p>'+ext.join(', ')+'</p>':'')}
show(0);
</script></body></html>"""

# ============================================================================ gallery (--gallery)
# Renders the FINAL book (the generated SNBT), so it shows what FTB shows whatever tools/layout.py does.
GAL_DIR = ROOT / "test/preview/gallery"
GAL_HTML = ROOT / "test/preview/gallery.html"
ICON_DIR = ROOT / "test/preview/icons"
ICON_VERSION = "4"  # bump to rebuild the icon cache
KJS_ASSETS = ROOT / "pack/kubejs/assets"
BG = (22, 22, 28, 255)        # FTB's dark quest-screen background
GRID = (32, 32, 40, 255)
LINE = (175, 175, 185, 210)   # dependency line (not yet completed)
FILL = (54, 54, 62, 255)
EDGE = (160, 160, 172, 255)


class Assets:
    """Resource lookup in the game's order: pack/kubejs/assets (KubeJS's resource pack), then the mod jars,
    then the vanilla client jar (if Prism has it)."""

    def __init__(self):
        self._index = None

    def index(self):
        if self._index is None:
            self._index = {}
            for z in _jars():
                for n in z.namelist():
                    if n.startswith("assets/") and n not in self._index:
                        self._index[n] = z
        return self._index

    def read(self, path):
        p = KJS_ASSETS / path[len("assets/"):]
        if p.exists():
            return p.read_bytes()
        z = self.index().get(path)
        if z is None:
            return None
        try:
            return z.read(path)
        except KeyError:
            return None


def _rl(name, kind):
    ns, p = name.split(":", 1) if ":" in name else ("minecraft", name)
    return f"assets/{ns}/{kind}/{p}"


def _tex(A, name):
    """A texture (resource name like ns:block/x) as a square RGBA image (first frame of animations), or None."""
    from PIL import Image
    import io
    if not name or name.startswith("#"):
        return None
    data = A.read(_rl(name, "textures") + ".png")
    if data is None:
        return None
    try:
        im = Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        return None
    w, h = im.size
    if h > w:
        im = im.crop((0, 0, w, w))
    if any(k in name for k in ("leaves", "grass_block_top", "vine", "lily_pad", "fern")):
        im = _tint(im, (90, 170, 50))
    return im


def _tint(im, rgb):
    from PIL import Image
    r, g, b, a = im.split()
    gray = Image.merge("RGB", (r, g, b)).convert("L")
    out = Image.merge("RGB", [gray.point(lambda v, c=c: v * c // 255) for c in rgb])
    out.putalpha(a)
    return out


def _model_chain(A, name):
    """Walk a model's parents: (textures with child entries first, is_2d_item, through_block, has_elements)."""
    tex, flat, block, elements = {}, False, False, False
    info = {}
    cur = name
    _model_chain.info = info
    for _ in range(16):
        path = cur.split(":", 1)[-1]
        if path in ("item/generated", "item/handheld", "builtin/generated", "item/handheld_rod"):
            flat = True
            break
        if path == "builtin/entity":
            break
        if path.startswith("block/"):
            block = True
        data = A.read(_rl(cur, "models") + ".json")
        if data is None:
            break
        try:
            js = json.loads(data)
        except Exception:
            break
        for k, v in (js.get("textures") or {}).items():
            if isinstance(v, str):
                tex.setdefault(k, v)
        elements = elements or bool(js.get("elements"))
        for k in ("loader", "casing", "default_overlays"):
            if k in js:
                info.setdefault(k, js[k])
        par = js.get("parent")
        if not par:
            break
        cur = par if ":" in par else "minecraft:" + par
    return tex, flat, block, elements


def _iso(top, left, right, S=64):
    """A Minecraft-style isometric cube from three face textures."""
    from PIL import Image, ImageEnhance
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    T, L, R, C = (S / 2, S * 0.03), (S * 0.06, S * 0.265), (S * 0.94, S * 0.265), (S / 2, S * 0.5)
    BL, BR, B = (S * 0.06, S * 0.735), (S * 0.94, S * 0.735), (S / 2, S * 0.97)

    def face(img, p0, p1, p3, shade):
        img = img.resize((16, 16), Image.NEAREST)
        if shade != 1:
            rgb = ImageEnhance.Brightness(img.convert("RGB")).enhance(shade)
            rgb.putalpha(img.getchannel("A"))
            img = rgb
        ax, ay = (p1[0] - p0[0]) / 16, (p1[1] - p0[1]) / 16
        bx, by = (p3[0] - p0[0]) / 16, (p3[1] - p0[1]) / 16
        det = ax * by - bx * ay
        ia, ib, id_, ie = by / det, -bx / det, -ay / det, ax / det
        coeffs = (ia, ib, -(ia * p0[0] + ib * p0[1]), id_, ie, -(id_ * p0[0] + ie * p0[1]))
        layer = img.transform((S, S), Image.AFFINE, coeffs, resample=Image.NEAREST, fillcolor=(0, 0, 0, 0))
        out.alpha_composite(layer)

    face(top, L, T, C, 1.0)
    face(left, L, C, BL, 0.78)
    face(right, C, R, B, 0.6)
    return out


_chem = None


def _chemlib_icon(A, path):
    """ChemLib items are drawn in code (builtin_entity) from tinted layer textures: rebuild that from its
    elements.json / compounds.json colours."""
    from PIL import Image
    global _chem
    if _chem is None:
        _chem = {}
        for z in _jars():
            for f, key in (("data/chemlib/elements.json", "elements"), ("data/chemlib/compounds.json", "compounds")):
                try:
                    for e in json.loads(z.read(f))[key]:
                        _chem[e["name"]] = (key, e.get("matter_state", "solid"), e.get("color", "FFFFFF"))
                except (KeyError, ValueError):
                    pass
    base, form = path, None
    for suf in ("_dust", "_ingot", "_nugget", "_plate"):
        if path.endswith(suf) and path[: -len(suf)] in _chem:
            base, form = path[: -len(suf)], suf[1:]
    if base not in _chem:
        return None
    kind, state, color = _chem[base]
    rgb = tuple(int(str(color)[i:i + 2], 16) for i in (0, 2, 4)) if len(str(color)) >= 6 else (255, 255, 255)
    if form:
        t = _tex(A, f"chemlib:item/{form}")
        return None if t is None else _tint(t, rgb).resize((32, 32), Image.NEAREST)
    pre = "element" if kind == "elements" else "compound"
    l0, l1 = _tex(A, f"chemlib:item/{pre}_{state}_layer_0"), _tex(A, f"chemlib:item/{pre}_{state}_layer_1")
    if l0 is None:
        return None
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    im.alpha_composite(_tint(l0.resize((16, 16), Image.NEAREST), rgb))
    if l1 is not None:
        im.alpha_composite(l1.resize((16, 16), Image.NEAREST))
    return im.resize((32, 32), Image.NEAREST)


_CASING = {"bronze": (184, 115, 51), "steel": (125, 130, 136), "lv": (150, 150, 160), "mv": (196, 120, 70),
           "hv": (210, 170, 60), "ev": (90, 150, 210), "superconductor": (120, 220, 230), "turbo": (60, 60, 70),
           "highly_advanced": (110, 80, 150), "quantum": (40, 40, 50)}


def _casing(name):
    """MI builds casing textures in code: a flat tier-coloured face with a darker rim stands in for them."""
    from PIL import Image, ImageDraw
    col = next((v for k, v in _CASING.items() if k in str(name)), (140, 140, 148))
    f = Image.new("RGBA", (16, 16), col + (255,))
    ImageDraw.Draw(f).rectangle((0, 0, 15, 15), outline=tuple(int(c * 0.6) for c in col) + (255,))
    return f


def _icon_image(A, item_id):
    """32x32 RGBA icon for an item id, or None."""
    from PIL import Image
    if not item_id or ":" not in item_id:
        return None
    ns, path = item_id.split(":", 1)
    if ns == "chemlib":
        im = _chemlib_icon(A, path)
        if im is not None:
            return im
    for mname in (f"{ns}:item/{path}", f"{ns}:block/{path}"):
        tex, flat, block, elements = _model_chain(A, mname)
        info = _model_chain.info
        if info.get("loader") == "neoforge:fluid_container":
            t = _tex(A, "minecraft:item/water_bucket")
            if t is not None:
                return t.resize((32, 32), Image.NEAREST)
        if info.get("casing") and isinstance(info.get("default_overlays"), dict):  # Modern Industrialization machine
            ov = info["default_overlays"]
            base = _casing(info["casing"])
            faces = []
            for k in ("top", "front", "side"):
                f = base.copy()
                t = _tex(A, ov.get(k)) if ov.get(k) else None
                if t is not None:
                    f.alpha_composite(t.resize((16, 16), Image.NEAREST))
                faces.append(f)
            return _iso(*faces).resize((32, 32), Image.LANCZOS)
        if not tex:
            continue

        def res(k):
            v = tex.get(k)
            for _ in range(6):
                if isinstance(v, str) and v.startswith("#"):
                    v = tex.get(v[1:])
            return v
        if flat or "layer0" in tex:
            im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
            got = False
            for i in range(5):
                t = _tex(A, res(f"layer{i}"))
                if t is not None:
                    im.alpha_composite(t.resize((16, 16), Image.NEAREST))
                    got = True
            if got:
                return im.resize((32, 32), Image.NEAREST)
        if "cross" in tex or "plant" in tex:
            t = _tex(A, res("cross") or res("plant"))
            if t is not None:
                return t.resize((32, 32), Image.NEAREST)

        def pick(*keys):
            for k in keys:
                t = _tex(A, res(k))
                if t is not None:
                    return t
            return None
        top = pick("top", "up", "end", "all", "texture", "side", "particle")
        if top is not None:
            side = pick("side", "north", "front", "all", "texture", "particle") or top
            front = pick("front", "north", "south", "side", "all", "texture", "particle") or side
            return _iso(top, front, side).resize((32, 32), Image.LANCZOS)
        for v in tex.values():  # parts and other special models: show their first real texture flat
            t = _tex(A, res(v[1:]) if v.startswith("#") else v)
            if t is not None:
                return t.resize((32, 32), Image.NEAREST)
    # textures named after the item (kubejs items, models built in code)
    for sub in ("item/", "block/"):
        for suf in ("", "_front", "_side", "_top", "_base", "_0"):
            t = _tex(A, f"{ns}:{sub}{path}{suf}")
            if t is not None:
                return t.resize((32, 32), Image.NEAREST)
    pre = f"assets/{ns}/textures/"
    leaf = path.split("/")[-1]
    cands = sorted((k for k in A.index() if k.startswith(pre) and k.endswith(".png") and "/entity/" not in k
                    and (k.endswith("/" + leaf + ".png") or ("/" + leaf + "_") in k or ("/" + leaf + "/") in k)),
                   key=lambda k: ("/item/" not in k, "overlay" in k, len(k)))
    for k in cands[:3]:
        t = _tex(A, f"{ns}:" + k[len(pre):-4])
        if t is not None:
            return t.resize((32, 32), Image.NEAREST)
    data = icon_bytes(item_id)  # the old filename guesses (item/<id>, block/<id>_front, kubejs textures)
    if data:
        import io
        try:
            t = Image.open(io.BytesIO(data)).convert("RGBA")
            if t.size[1] > t.size[0]:
                t = t.crop((0, 0, t.size[0], t.size[0]))
            return t.resize((32, 32), Image.NEAREST)
        except Exception:
            return None
    return None


class IconCache:
    """Icons cached as PNGs under test/preview/icons/<ns>/<path>.png (missing ids listed in _missing.txt)."""

    def __init__(self):
        self.A = Assets()
        self.mem = {}
        ver = ICON_DIR / "_version.txt"
        if not ver.exists() or ver.read_text(encoding="utf-8").strip() != ICON_VERSION:
            import shutil
            shutil.rmtree(ICON_DIR, ignore_errors=True)
            ICON_DIR.mkdir(parents=True, exist_ok=True)
            ver.write_text(ICON_VERSION + "\n", encoding="utf-8", newline="\n")
        mf = ICON_DIR / "_missing.txt"
        self.missing = set(mf.read_text(encoding="utf-8").split()) if mf.exists() else set()
        self.new_missing = False

    def get(self, item_id):
        from PIL import Image
        if not item_id or ":" not in item_id or item_id in self.missing:
            return None
        if item_id in self.mem:
            return self.mem[item_id]
        ns, path = item_id.split(":", 1)
        f = ICON_DIR / ns / (path.replace("/", "__") + ".png")
        im = None
        if f.exists():
            im = Image.open(f).convert("RGBA")
        else:
            im = _icon_image(self.A, item_id)
            if im is None:
                self.missing.add(item_id)
                self.new_missing = True
            else:
                f.parent.mkdir(parents=True, exist_ok=True)
                im.save(f)
        self.mem[item_id] = im
        return im

    def save(self):
        if self.new_missing:
            (ICON_DIR / "_missing.txt").write_text("\n".join(sorted(self.missing)) + "\n", encoding="utf-8", newline="\n")


def _shape(d, shape, cx, cy, r, fill, edge, ew):
    """Draw one FTB quest shape (size = 2r) on an ImageDraw."""
    pts = None
    if shape == "none":
        return
    if shape == "circle":
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=edge, width=ew)
        return
    if shape == "square":
        k = r * 0.94
        d.rectangle((cx - k, cy - k, cx + k, cy + k), fill=fill, outline=edge, width=ew)
        return
    if shape == "rsquare":
        k = r * 0.94
        d.rounded_rectangle((cx - k, cy - k, cx + k, cy + k), radius=r * 0.38, fill=fill, outline=edge, width=ew)
        return
    if shape == "diamond":
        pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    elif shape in ("pentagon", "hexagon", "octagon"):
        n, start = {"pentagon": (5, -90), "hexagon": (6, 0), "octagon": (8, 22.5)}[shape]
        pts = [(cx + r * math.cos(math.radians(start + i * 360 / n)), cy + r * math.sin(math.radians(start + i * 360 / n)))
               for i in range(n)]
    elif shape == "gear":
        teeth, pts = 10, []
        for i in range(teeth * 4):
            a = math.radians(i * 360 / (teeth * 4) - 4.5)
            rr = r if i % 4 in (0, 1) else r * 0.8
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    elif shape == "heart":
        pts = []
        for i in range(48):
            t = 2 * math.pi * i / 48
            x = 16 * math.sin(t) ** 3
            y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((cx + x * r / 17, cy + y * r / 17 - r * 0.05))
    if pts is None:  # unknown shape: FTB falls back to a circle
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=edge, width=ew)
        return
    d.polygon(pts, fill=fill, outline=edge, width=ew)


def _font(px):
    from PIL import ImageFont
    try:
        return ImageFont.load_default(size=max(6, int(px)))
    except TypeError:
        return ImageFont.load_default()


def render_chapter(c, book, icons, U=24, SS=3):
    """One chapter as an RGBA image, U px per cell."""
    from PIL import Image, ImageDraw
    import io
    import layout_lint as LL
    nodes = c["quests"] + c["links"]
    boxes = [(n["x"] - n["size"] / 2, n["y"] - n["size"] / 2, n["x"] + n["size"] / 2, n["y"] + n["size"] / 2) for n in nodes]
    boxes += [LL.image_box(im) for im in c["images"]]
    if not boxes:
        boxes = [(0, 0, 1, 1)]
    M = 1.0
    x0, y0 = min(b[0] for b in boxes) - M, min(b[1] for b in boxes) - M
    x1, y1 = max(b[2] for b in boxes) + M, max(b[3] for b in boxes) + M
    W, H = max(1, int(round((x1 - x0) * U))), max(1, int(round((y1 - y0) * U)))
    S = U * SS
    img = Image.new("RGBA", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    gx = math.ceil(x0)
    while gx < x1:
        X = (gx - x0) * S
        d.line([(X, 0), (X, H * SS)], fill=GRID, width=max(1, SS // 2))
        gx += 1
    gy = math.ceil(y0)
    while gy < y1:
        Y = (gy - y0) * S
        d.line([(0, Y), (W * SS, Y)], fill=GRID, width=max(1, SS // 2))
        gy += 1

    def P(x, y):
        return ((x - x0) * S, (y - y0) * S)

    # chapter images (banners, section headers), in their draw order
    for im in sorted(c["images"], key=lambda i: i["order"]):
        name = im["image"]
        ns, rest = name.split(":", 1) if ":" in name else ("minecraft", name)
        data = icons.A.read(f"assets/{ns}/{rest}")
        pw, ph = max(1, int(im["w"] * S)), max(1, int(im["h"] * S))
        if data:
            try:
                pic = Image.open(io.BytesIO(data)).convert("RGBA").resize((pw, ph), Image.LANCZOS)
            except Exception:
                pic = None
        else:
            pic = None
        if pic is None:  # missing texture: FTB shows nothing useful, we show a dashed placeholder
            pic = Image.new("RGBA", (pw, ph), (90, 40, 40, 120))
            ImageDraw.Draw(pic).rectangle((0, 0, pw - 1, ph - 1), outline=(220, 90, 90, 255), width=SS)
        a = im.get("alpha", 255)
        if isinstance(a, (int, float)) and a < 255:
            pic.putalpha(pic.getchannel("A").point(lambda v, a=a: v * int(a) // 255))
        if im["rot"]:
            pic = pic.rotate(-im["rot"], expand=True, resample=Image.BICUBIC)
        cx, cy = P(im["x"], im["y"])
        img.alpha_composite(pic, (int(cx - pic.size[0] / 2), int(cy - pic.size[1] / 2)))

    # dependency lines (and lines from quest links), straight, skipping hidden ones
    lines, _ = LL.chapter_lines(c, book)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    lw = max(SS, int(S * 0.085))
    for l in lines:
        if l["hidden"]:
            continue
        col = LINE if not l["b"].get("optional") else (LINE[0], LINE[1], LINE[2], 110)
        ld.line([P(l["a"]["x"], l["a"]["y"]), P(l["b"]["x"], l["b"]["y"])], fill=col, width=lw)
    img.alpha_composite(lay)

    # quest shapes
    ew = max(SS, int(S * 0.07))
    for n in nodes:
        cx, cy = P(n["x"], n["y"])
        r = n["size"] * S / 2 * 0.95
        dim = n.get("optional") or "quest" in n  # optional quests and quest links are drawn dimmer
        if dim:
            q = Image.new("RGBA", img.size, (0, 0, 0, 0))
            _shape(ImageDraw.Draw(q), n["shape"], cx, cy, r, FILL, EDGE, ew)
            q.putalpha(q.getchannel("A").point(lambda v: v * 120 // 255))
            img.alpha_composite(q)
        else:
            _shape(d, n["shape"], cx, cy, r, FILL, EDGE, ew)
    img = img.resize((W, H), Image.LANCZOS)

    # icons (or a short label) at final resolution, so 16px textures stay crisp
    d = ImageDraw.Draw(img)
    for n in nodes:
        cx, cy = (n["x"] - x0) * U, (n["y"] - y0) * U
        dim = n.get("optional") or "quest" in n
        ic = icons.get(n.get("icon"))
        sz = max(6, int(round(n["size"] * U * 0.64)))
        if ic is not None:
            t = ic.resize((sz, sz), Image.LANCZOS if sz < ic.size[0] else Image.NEAREST)
            if dim:
                t.putalpha(t.getchannel("A").point(lambda v: v * 120 // 255))
            img.alpha_composite(t, (int(cx - sz / 2), int(cy - sz / 2)))
        else:
            label = (n.get("label") or "")[:6]
            px = U * 0.34 * min(1.6, n["size"])
            f = _font(px)
            while px > 6 and d.textlength(label, font=f) > n["size"] * U * 0.8:
                px -= 1
                f = _font(px)
            col = (225, 225, 230, 130 if dim else 255)
            d.text((cx, cy), label, font=f, fill=col, anchor="mm")
        if "quest" in n:  # quest-link marker: small arrow in the corner
            k = n["size"] * U * 0.42
            ax, ay = cx + k * 0.55, cy - k * 0.55
            s = max(3, U * 0.16)
            d.polygon([(ax - s, ay - s), (ax + s, ay - s), (ax + s, ay + s)], fill=(120, 200, 255, 230))
    return img


def gallery_main():
    import argparse
    import datetime
    import layout_lint as LL
    ap = argparse.ArgumentParser()
    ap.add_argument("--gallery", action="store_true")
    ap.add_argument("--cell", type=int, default=24, help="pixels per grid cell (default 24)")
    ap.add_argument("--chapters", help="comma-separated chapter file names (default: all)")
    ap.add_argument("--book", default=str(LL.OUR_BOOK), help="config/ftbquests/quests folder (default: ours)")
    ap.add_argument("--target", default="18x14", help="lint page-size target WxH")
    ap.add_argument("--compare", default=str(LL.ATM10), help="book for the medians table (skipped if missing)")
    ap.add_argument("--out", default=str(GAL_HTML), help="gallery html path (PNGs go in a 'gallery' folder beside it)")
    args = ap.parse_args()
    target = tuple(float(v) for v in args.target.lower().split("x"))
    only = set(args.chapters.split(",")) if args.chapters else None
    book, results = LL.lint_book(args.book, target, only)
    out_html = pathlib.Path(args.out)
    gal_dir = out_html.parent / "gallery"
    gal_dir.mkdir(parents=True, exist_ok=True)
    icons = IconCache()
    cards = []
    for c, m in results:
        im = render_chapter(c, book, icons, U=args.cell)
        im.convert("RGB").save(gal_dir / f"{c['file']}.png", optimize=True)
        cards.append((c, m, im.size))
        print(f"  {c['file']:18} {im.size[0]:5}x{im.size[1]:<5} score {m['score']:3}")
    icons.save()
    ours = LL.summary(book, results)
    theirs = {}
    if args.compare and (pathlib.Path(args.compare) / "chapters").exists():
        ob, orr = LL.lint_book(args.compare, target)
        theirs = LL.summary(ob, orr)
    lang = LL._lang(pathlib.Path(args.book))
    title = LL._text(lang.get("file.0000000000000001.title") or "Quest book")
    out_html.write_text(_gallery_html(title, book, cards, ours, theirs, target, gal_dir.name), encoding="utf-8", newline="\n")
    print(f"Wrote {out_html} and {len(cards)} PNGs in {gal_dir} "
          f"({sum(1 for c, m, _ in cards if m['score'] < 70)} chapters below 70)")


def _gallery_html(title, book, cards, ours, theirs, target, sub):
    import datetime
    esc = html.escape
    v = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    gname = {g["id"]: g["title"] for g in book["groups"]}
    groups = {}
    for c, m, size in cards:
        groups.setdefault(gname.get(c["group"], "(no group)") if c["group"] else "(no group)", []).append((c, m, size))
    rows = "".join(f"<tr><td>{esc(k)}</td><td>{esc(str(ours[k]))}</td><td>{esc(str(theirs.get(k, '')))}</td></tr>" for k in ours)
    data = []
    sec = []
    for g, items in groups.items():
        cs = []
        for c, m, size in items:
            i = len(data)
            cls = "good" if m["score"] >= 85 else ("ok" if m["score"] >= 65 else "bad")
            d = m["dirs"]
            stats = (f"{m['quests']} quests · {m['w']:.0f}×{m['h']:.0f} cells · cross {m['crossings']} · through {m['through']} · "
                     f"overlap {m['overlaps']} · long {m['long']} · R/D/L/U {d['R']}/{d['D']}/{d['L']}/{d['U']} · "
                     f"hidden {m['hidden']} · images {m['images']}")
            iss = "".join(f"<li>{esc(t)}</li>" for t in m["issues"][:6]) or "<li class='none'>no issues</li>"
            data.append({"src": f"{sub}/{c['file']}.png?v={v}", "title": c["title"], "file": c["file"], "score": m["score"],
                         "stats": stats, "issues": m["all_issues"][:40]})
            cs.append(f"""<figure class="card" data-i="{i}"><button class="thumb" data-i="{i}" aria-label="Enlarge {esc(c['title'])}">
<img src="{sub}/{esc(c['file'])}.png?v={v}" alt="{esc(c['title'])} layout" loading="lazy" width="{size[0]}" height="{size[1]}"></button>
<figcaption><div class="top"><b>{esc(c['title'])}</b><span class="score {cls}">{m['score']}</span></div>
<div class="file">{esc(c['file'])}</div><div class="stats">{stats}</div><ul>{iss}</ul></figcaption></figure>""")
        sec.append(f"<section><h2>{esc(g)}</h2><div class='grid'>{''.join(cs)}</div></section>")
    return GALLERY_TEMPLATE.replace("__TITLE__", esc(title)).replace("__ROWS__", rows).replace("__SECTIONS__", "".join(sec)) \
        .replace("__DATA__", json.dumps(data)).replace("__TARGET__", f"{target[0]:g}×{target[1]:g}") \
        .replace("__WHEN__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) \
        .replace("__CMP__", "ATM10" if theirs else "")


GALLERY_TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Quest Layout Gallery</title>
<style>
:root{--bg:#0f1014;--panel:#181a21;--line:#2a2d38;--text:#e8e9ee;--muted:#9a9fb0;--good:#4cc38a;--ok:#e2b340;--bad:#e5604f;--accent:#7cc4ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 system-ui,"Segoe UI",sans-serif}
header{padding:20px 16px 8px;max-width:1500px;margin:auto}h1{margin:0 0 4px;font-size:22px}header p{margin:0;color:var(--muted)}
details{margin:12px 0;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
summary{cursor:pointer;color:var(--accent)}table{border-collapse:collapse;margin-top:8px}td,th{padding:3px 14px 3px 0;text-align:left}
td:nth-child(n+2),th:nth-child(n+2){text-align:right;font-variant-numeric:tabular-nums}th{color:var(--muted);font-weight:500}
main{max-width:1500px;margin:auto;padding:0 16px 40px}h2{font-size:15px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:26px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.card{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.thumb{all:unset;cursor:zoom-in;display:flex;align-items:center;justify-content:center;height:200px;background:#16161c;border-bottom:1px solid var(--line)}
.thumb:focus-visible{outline:2px solid var(--accent)}.thumb img{max-width:100%;max-height:200px;width:auto;height:auto;object-fit:contain}
figcaption{padding:10px 12px}.top{display:flex;justify-content:space-between;gap:8px;align-items:center}
.score{font-weight:700;border-radius:6px;padding:1px 8px;font-variant-numeric:tabular-nums;color:#111}.good{background:var(--good)}.ok{background:var(--ok)}.bad{background:var(--bad)}
.file{color:var(--muted);font-size:12px}.stats{color:var(--muted);font-size:12px;margin-top:4px}
ul{margin:6px 0 0;padding-left:18px;font-size:12.5px}li{margin:2px 0;overflow-wrap:anywhere}li.none{color:var(--muted);list-style:none;margin-left:-18px}
#lb{position:fixed;inset:0;background:#0b0c10;display:none;flex-direction:column;z-index:10}#lb.on{display:flex}
#lb .bar{display:flex;gap:12px;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line)}#lb .bar b{flex:1}
#lb button{background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer;font:inherit}
#lb .body{flex:1;display:flex;min-height:0}#lb .view{flex:1;overflow:auto;padding:16px}#lb .view img{image-rendering:auto;display:block;margin:auto}
#lb aside{width:360px;flex:none;overflow:auto;padding:12px 16px;border-left:1px solid var(--line)}
@media (max-width:800px){#lb .body{flex-direction:column}#lb aside{width:auto;max-height:35vh;border-left:0;border-top:1px solid var(--line)}}
</style></head><body>
<header><h1>__TITLE__ · layout gallery</h1>
<p>Rendered from the final SNBT on __WHEN__. One cell = one FTB grid unit. Page target __TARGET__ cells. Scores from tools/layout_lint.py (100 = tidy). Click a chapter to enlarge; ←/→ to step, Esc to close.</p>
<details><summary>Book medians (ours vs __CMP__)</summary><table><tr><th>median</th><th>ours</th><th>__CMP__</th></tr>__ROWS__</table></details>
</header><main>__SECTIONS__</main>
<div id="lb" role="dialog" aria-modal="true"><div class="bar"><b id="lt"></b><span id="ls" class="score"></span>
<button id="zf">Fit</button><button id="pv">←</button><button id="nx">→</button><button id="cl">Close</button></div>
<div class="body"><div class="view" id="lv"><img id="li" alt=""></div><aside><div id="lst" class="stats"></div><ul id="lis"></ul></aside></div></div>
<script>
const D=__DATA__;let cur=-1,fit=false;const $=id=>document.getElementById(id);
function open(i){cur=(i+D.length)%D.length;const d=D[cur];$('li').src=d.src;$('lt').textContent=d.title+'  ('+d.file+')';
 const s=$('ls');s.textContent=d.score;s.className='score '+(d.score>=85?'good':d.score>=65?'ok':'bad');
 $('lst').textContent=d.stats;$('lis').innerHTML=d.issues.length?d.issues.map(t=>'<li>'+t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))+'</li>').join(''):'<li class="none">no issues</li>';
 applyFit();$('lb').classList.add('on')}
function applyFit(){const im=$('li');im.style.maxWidth=fit?'100%':'none';im.style.maxHeight=fit?'100%':'none';$('zf').textContent=fit?'1:1':'Fit'}
document.querySelectorAll('.thumb').forEach(b=>b.onclick=()=>open(+b.dataset.i));
$('cl').onclick=()=>$('lb').classList.remove('on');$('pv').onclick=()=>open(cur-1);$('nx').onclick=()=>open(cur+1);
$('zf').onclick=()=>{fit=!fit;applyFit()};
document.addEventListener('keydown',e=>{if(!$('lb').classList.contains('on'))return;if(e.key==='Escape')$('cl').click();
 if(e.key==='ArrowLeft')open(cur-1);if(e.key==='ArrowRight')open(cur+1)});
</script></body></html>"""


if __name__ == "__main__":
    main()
