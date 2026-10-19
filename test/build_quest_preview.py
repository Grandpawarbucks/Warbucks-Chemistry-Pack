#!/usr/bin/env python3
"""Build test/preview/index.html: a browsable mock of the in-game quest book (chapter tabs,
banners, quest nodes with item icons, dependency lines, quest text on click).

Icons come from the mod jars in test/server/mods, so the output stays in git-ignored test/
(mod textures must not be published in the public repo).
Positions and text are the real build's: automatic layout (tools/layout.py), then the quest editor's
overrides (tools/quest_overrides.json). To EDIT the book, use tools/quest_editor.py instead.
Usage: python3 test/build_quest_preview.py          then open http://localhost:8765 (python3 -m http.server)
       python3 test/build_quest_preview.py --json   print the quest data as JSON (icons as item ids; used by the editor)
"""
import base64
import glob
import html
import json
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
    for c in CHAPTERS:
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
                       "raw": {"title": q.title or "", "subtitle": q.subtitle or "", "desc": list(q.desc)}, "gen": gen[q.key]})
        # Quest links (shortcuts to quests in other chapters) as faded nodes in the link column.
        for lk, lx, ly in c.links:
            k = f"link:{c.key}:{lk}"
            qs.append({"key": k, "linkOf": lk, "x": lx, "y": ly, "size": 0.8, "shape": "circle", "link": True,
                       "title": "Link: " + strip_codes(titles.get(lk, lk)), "desc": [html.escape(f"Shortcut to a quest in {home.get(lk, 'another chapter')}.")],
                       "sub": "", "deps": [], "tasks": [], "rewards": [], "icon": None, "gen": gen.get(k, {"x": lx, "y": ly})})
        bx, by = layout.banner(c)
        chapters.append({"key": c.key, "title": c.title, "group": GROUPS[c.group] or "Start here", "sub": [fmt(s) for s in c.subtitle],
                         "iconId": c.icon, "icon": icon_fn(c.icon), "manual": getattr(c, "layout", "auto") == "manual",
                         "bx": bx, "by": by, "quests": qs})
    return chapters, warnings


def main():
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
 const xs=c.quests.map(q=>q.x),ys=c.quests.map(q=>q.y),minx=Math.min(...xs,c.bx-3),miny=Math.min(...ys,c.by-0.5)-(c.key=='welcome'?3:1),maxx=Math.max(...xs,c.bx+3),maxy=Math.max(...ys);
 const W=(maxx-minx+3)*U,H=(maxy-miny+3)*U,cv=document.getElementById('canvas');cv.style.width=W+'px';cv.style.height=H+'px';cv.innerHTML='';
 const P=(x,y)=>[(x-minx+1)*U,(y-miny+1)*U];
 if(c.banner){const im=document.createElement('img');im.className='banner';im.src=c.banner;const[bx,by]=P(c.bx-3,c.by-0.5);
  im.style.left=bx+'px';im.style.top=by+'px';im.style.width=6*U+'px';im.style.height=U+'px';cv.appendChild(im)}
 if(c.key=='welcome'){const im=document.createElement('img');im.className='banner';im.src=document.querySelector('nav img.logo').src;const[bx,by]=P(c.bx-3,c.by-3.285);im.style.left=bx+'px';im.style.top=by+'px';im.style.width=7*U+'px';cv.appendChild(im)}
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('width',W);svg.setAttribute('height',H);cv.appendChild(svg);
 const byKey={};c.quests.forEach(q=>{if(!q.link)byKey[q.key]=q});c.quests.forEach(q=>{if(q.link&&!byKey[q.linkOf])byKey[q.linkOf]=q});
 c.quests.forEach(q=>q.deps.forEach(d=>{const p=byKey[d];if(!p)return;const[a,b]=P(p.x,p.y),[e,f]=P(q.x,q.y);
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

if __name__ == "__main__":
    main()
