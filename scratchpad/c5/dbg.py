import re,pathlib,sys
sys.argv=["x","basic_armor"]
src=pathlib.Path(__file__).parent.joinpath("parse_atm.py").read_text(encoding="utf-8").replace("\nmain()\n","\n")
exec(src)
text = ATM.joinpath("basic_armor.snbt").read_text(encoding="utf-8", errors="replace")
for b in list_blocks(text, text.index("\n\tquests: [") + len("\n\tquests: ")):
    if '3D72E3E53E7306FA' in b:
        print(base(b)); m = re.search(rf"\n\t{{{base(b)}}}tasks: \[", b); print(m)
        ts=list_blocks(b, m.end()-1); print(len(ts)); t=ts[0]; print(repr(t[:200])); print(base(t), fld(t,4,"type"))
