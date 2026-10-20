import zipfile, json, sys
z = zipfile.ZipFile(sys.argv[1])
out = {}
for n in z.namelist():
    if n.startswith("data/ars_nouveau/recipe/glyph_") and n.endswith(".json"):
        d = json.loads(z.read(n))
        ins = []
        for i in d.get("inputs", []):
            if isinstance(i, dict):
                ins.append(i.get("item") or ("#" + i.get("tag", "?")))
            else:
                ins.append(str(i))
        out[n.split("/")[-1][:-5]] = (d.get("exp"), ins, {k: v for k, v in d.items() if k not in ("inputs", "exp", "type", "output")})
for k in sorted(out):
    print(k, out[k])
