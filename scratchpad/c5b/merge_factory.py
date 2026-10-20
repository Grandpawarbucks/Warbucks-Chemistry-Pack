"""Merge the hostile_neural_networks mirror into tools/quests/factory.py."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "tools/quests/factory.py"
s = p.read_text(encoding="utf-8")
new = (ROOT / "scratchpad/c5b/factory_new.txt").read_text(encoding="utf-8")

HELPER = '''
# ATM10 mirror (2026-10-20, user decision): the Hostile Neural Networks part follows ATM10's "hostile_neural_networks"
# chapter quest for quest (its item list, order and shape only; all text is ours). ATM10 asks for a prediction of each
# mob; our engine can't ask for an item with a data component, so each of those quests asks for the drop the Loot
# Fabricator makes from that mob's predictions. Extended Crafting and Compact Machines stay as our own sections.
HNN = "Mob Simulation"


def sim(key, mob, drop, title, mirror, ids=None, note=None, optional=True, size=None, xp=40):
    """One simulated mob: fabricate its drop from predictions (hunting it also works)."""
    task = anyof(ids) if ids else item(drop)
    return Q(key, 0, 0, [task], "Simulated " + title, deps=["mf_fab"], xp=xp, optional=optional, size=size, section=HNN,
             mirror=mirror, subtitle=("Optional: " if optional else "") + f"{mob} predictions into loot", desc=[
                 f"&eWhat:&r run a {mob} data model in the Simulation Chamber, then turn its predictions into drops in the Loot Fabricator.",
                 "&eHow:&r train the model to Basic or better, simulate it, and pick this drop in the Fabricator's menu (check JEI for the full list).",
                 "&eTip:&r " + (note or "hunting the mob also counts; the point is never having to again.")])

'''
imp = 'from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401\n'
if "def sim(" not in s:
    assert s.count(imp) == 1
    s = s.replace(imp, imp + HELPER)


def patch(key, old, new_):
    global s
    m = re.search(r'    Q\("' + key + r'".*?\]\),\n', s, re.S)
    assert m, key
    b = m.group(0)
    assert old in b, (key, old)
    s = s.replace(b, b.replace(old, new_, 1))


patch("mf_learner", '[item("hostilenetworks:deep_learner"), item("hostilenetworks:blank_data_model")], "Deep Learning", deps=["gs_iron"], xp=40,',
      '[item("hostilenetworks:deep_learner")], "Deep Learning", deps=["mf_hnn_hub"], xp=40, section=HNN, mirror="3E3CBDCEAB0FF28F",')
patch("mf_learner", '"&eHow:&r craft the Deep Learner and a Blank Data Model (check JEI).', '"&eHow:&r craft the Deep Learner (check JEI).')
patch("mf_model", 'deps=["mf_learner"], xp=40,', 'deps=["mf_learner", "mf_blank_model"], xp=40, section=HNN, mirror="34CD54347E9821B5",')
patch("mf_sim", 'item("hostilenetworks:prediction_matrix", 4)], "Simulation", deps=["mf_model", "t4_mv"], xp=150,',
      'item("hostilenetworks:prediction_matrix")], "Simulation", deps=["mf_learner", "mf_blank_model", "t4_mv"], xp=150, section=HNN, mirror="104EBBC08B4733F5",')
patch("mf_fab", 'deps=["mf_sim"], xp=150,', 'deps=["mf_sim"], xp=150, section=HNN, mirror="14B3542ECB59869C",')
patch("mf_twilight_pred", '[item("hostilenetworks:twilight_prediction", 4)]', '[item("hostilenetworks:twilight_prediction")]')
patch("mf_twilight_pred", 'xp=100,', 'xp=100, section=HNN, mirror="14F7F256DA863280",')
patch("mf_predictions", '[item("hostilenetworks:overworld_prediction", 4), item("hostilenetworks:nether_prediction", 4), item("hostilenetworks:end_prediction", 4)], "Three Worlds of Data", deps=["mf_sim", "w_end"], xp=100,\n      optional=True, tokens=1, subtitle="Optional: predictions from every dimension"',
      '[item("hostilenetworks:overworld_prediction")], "Overworld Predictions", deps=["mf_sim"], xp=40, section=HNN, mirror="2559201BCF5D497C",\n      subtitle="Data from an Overworld mob"')
patch("mf_predictions", '"&eHow:&r run simulations of one mob from each dimension, such as a zombie, a blaze and an enderman."',
      '"&eHow:&r simulate any Overworld mob, such as a zombie or a cow. The Nether and End ones are their own quests."')
patch("mf_data_center", '[item("hostilenetworks:data_center"), item("hostilenetworks:data_center_io_port")], "The Data Center", deps=["mf_fab"], xp=300,\n      optional=True, tokens=2, subtitle="Optional: 25 simulations at once"',
      '[item("hostilenetworks:data_center"), anytag("c:obsidians"), item("minecraft:black_stained_glass"), item("hostilenetworks:data_center_io_port")],\n      "The Data Center", deps=["mf_fab"], xp=300, size=2.0, shape="gear", section=HNN, mirror="3F3F3174BD9D03BD", loot="t5",\n      subtitle="25 simulations at once"')

if 'Q("mf_hnn_hub"' not in s:
    i = s.rindex("], links=[")
    s = s[:i] + new + s[i:]
s = s.replace("from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE",
              "from questlib import Q, Chapter, item, dim, tick, kill, anytag, anyof, MAIN, SIDE")
if 'mirror="hostile_neural_networks"' not in s:
    s = s.replace('("t5_ae2", -2, 4)])', '("t5_ae2", -2, 4)], mirror="hostile_neural_networks")')
assert 'mirror="hostile_neural_networks"' in s
p.write_text(s, encoding="utf-8", newline="\n")
print("done")
