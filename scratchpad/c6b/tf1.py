import sys; sys.path.insert(0, 'scratchpad/c6b')
from qedit import F
f = F('tools/quests/twilight.py')
S = f.sub
S("tf_magic_saplings", "hollow trees hide them in their leafy caches; the castle and the troll vaults turn them up too. Hold one of each.",
  "hollow trees hide them in the leafy caches up in their branches. Climb more than one tree to find all four, then hold one of each.")
# maps
f.header("tf_focus_parts", '''Q("tf_focus_parts", 0, 0, [item(TF + "raven_feather"), item(TF + "torchberries", 4)], "Feather and Berries", deps=["tf_hunter"], xp=50,
      mirror="57940981E8DE55D4", subtitle="A raven's feather and a glowing berry", desc=[''')
S("tf_map_focus", 'deps=["tf_focus_parts"], xp=75,', 'deps=["tf_focus_parts"], xp=75, mirror="4F66DF6B494BEFF3",')
f.header("tf_map", '''Q("tf_map", -8, -6, [anyof(tf("magic_map", "filled_magic_map"))], "A Map of Dusk", deps=["tf_map_focus"], xp=50,
      optional=True, tokens=1, mirror="0990D6CEE042F44E", subtitle="Optional: the forest draws its own map", desc=[''')
S("tf_map", "&eHow:&r eight paper around the focus makes a blank Magic Map. Use it inside the Twilight Forest to fill it in.",
  "&eHow:&r eight paper around the focus makes a blank Magic Map. A blank or a filled one counts; use it inside the forest to fill it in.")
# hills
f.header("tf_ore_magnet", '''Q("tf_ore_magnet", -8, -4, [item(TF + "ore_magnet")], "Ore Magnet", deps=["tf_arrive"], xp=100,
      mirror="5FE4DAE8F41B1437", section="Forest Treasures", subtitle="Pull the vein to you", desc=[''')
S("tf_big_hill", 'deps=["tf_ore_magnet"]', 'deps=["tf_hollow_hill"]')
f.header("tf_hill_curios", '''Q("tf_hill_curios", -12, -4, [item(TF + "peacock_feather_fan")], "Peacock Feather Fan",
      deps=["tf_arrive"], xp=100, mirror="1464D45C474464DB", section="Forest Treasures", subtitle="A fan that blows a gale", desc=[''')
S("tf_hill_curios", "&eWhat:&r odd treasures from hills and the Lich Tower: the Peacock Feather Fan blows a gust of wind, the Moonworm Queen fires glowing moonworms, and Transformation Powder turns some mobs into their Twilight cousins.",
  "&eWhat:&r a fan of peacock feathers. Swing it and a gust of wind shoves mobs, items and you yourself.")
S("tf_hill_curios", "&eHow:&r loot any one of them from hollow hill or tower chests.", "&eHow:&r loot it from hollow hill chests and the Lich Tower's rooms.")
S("tf_hill_curios", "&eTip:&r the Moonworm Queen is a lighting tool that never runs out for good; its repair recipe is in JEI.",
  "&eTip:&r fan yourself upward mid-jump to clear a gap you couldn't otherwise reach.")
f.after("tf_hill_curios", '''    Q("tf_moonworm", 0, 0, [item(TF + "moonworm_queen")], "Moonworm Queen", deps=["tf_arrive"], xp=100, mirror="60FC2DAEA954A849",
      section="Forest Treasures", subtitle="A light source that fires glowing worms", desc=[
        "&eWhat:&r a staff that shoots moonworms: each one sticks to the block it hits and glows there for good.",
        "&eChemistry:&r a cold light like this is chemiluminescence: a reaction leaves a molecule in an excited state, and it sheds the energy as a photon instead of heat.",
        "&eHow:&r a treasure from hollow hill and tower chests.",
        "&eTip:&r it wears down with use; torchberries repair it (check JEI)."]),
    Q("tf_transform_powder", 0, 0, [item(TF + "transformation_powder")], "Transformation Powder", deps=["tf_arrive"], xp=100,
      mirror="0E9DE6293DF611E1", section="Forest Treasures", subtitle="Turn a mob into its Twilight cousin", desc=[
        "&eWhat:&r a dust that changes some mobs into their Twilight relatives, and back again (JEI lists the pairs).",
        "&eHow:&r found in forest chests (the Lich Tower and hollow hills are good bets). Use it on a mob to see what it turns into.",
        "&eTip:&r it's a cheap way to bring Twilight animals home without a lead and a long walk."]),''')
# steeleaf / ironwood armour
f.header("tf_steeleaf_gear", '''Q("tf_steeleaf_gear", -8, -2, [item(TF + "steeleaf_helmet"), item(TF + "steeleaf_chestplate"), item(TF + "steeleaf_leggings"),
                                    item(TF + "steeleaf_boots")],
      "Steeleaf Armour", deps=["tf_arrive"], xp=150, mirror="2BEBF66D7EA594FA", section="Forest Treasures",
      subtitle="A full suit of metal-hard leaves", desc=[''')
S("tf_steeleaf_gear", "&eWhat:&r steeleaf tools and armour come pre-enchanted. The pickaxe is crafted with Fortune II already on it.",
  "&eWhat:&r steeleaf armour and tools come pre-enchanted; the pickaxe even has Fortune II built in.")
S("tf_steeleaf_gear", "&eHow:&r craft any steeleaf piece (vanilla shapes with steeleaf; check JEI).",
  "&eHow:&r helmet, chestplate, leggings and boots in the usual armour shapes, from steeleaf ingots (check JEI).")
f.header("tf_ironwood_gear", '''Q("tf_ironwood_gear", -8, 0, [item(TF + "ironwood_helmet"), item(TF + "ironwood_chestplate"), item(TF + "ironwood_leggings"),
                                   item(TF + "ironwood_boots")],
      "Ironwood Armour", deps=["tf_arrive"], xp=150, mirror="40258842B0359A2D", section="Forest Treasures",
      subtitle="A full suit that comes enchanted", desc=[''')
S("tf_ironwood_gear", "&eWhat:&r ironwood tools and armour come with enchantments built in (the pickaxe has Efficiency I).",
  "&eWhat:&r ironwood armour comes with enchantments built in, and so do its tools (the pickaxe has Efficiency I).")
S("tf_ironwood_gear", "&eHow:&r craft any ironwood piece in the usual shapes (check JEI).",
  "&eHow:&r helmet, chestplate, leggings and boots in the usual shapes from ironwood ingots (the Ironwood side quest shows how to make them).")
f.header("tf_ironwood", '''Q("tf_ironwood", -6, 0, [item(TF + "liveroot", 2), item(TF + "ironwood_ingot", 4)], "Ironwood", deps=["tf_oak"], xp=100,
      optional=True, tokens=1, subtitle="Optional: living root, iron and gold", desc=[''')
# charms
f.header("tf_charm_life", '''Q("tf_charm_life", -6, 8, [item(TF + "charm_of_life_1")], "Charm of Life", deps=["tf_arrive"], xp=100,
      mirror="6F67079A453DAABE", section="Forest Treasures", subtitle="One death, refused", desc=[''')
f.after("tf_charm_life", '''    Q("tf_charm_life2", 0, 0, [item(TF + "charm_of_life_2")], "Greater Charm of Life", deps=["tf_charm_life"], xp=200, size=1.5,
      mirror="15006CF73F8CAB7C", subtitle="Four charms make a stronger one", desc=[
        "&6One death refused was never enough for you. You remember carrying a better promise.&r",
        "&eWhat:&r the second Charm of Life saves you from a killing blow and leaves you in far better shape than the first one does.",
        "&eHow:&r four Charms of Life I, shapeless, make one Charm of Life II (check JEI). Forest chests fill the stack.",
        "&eTip:&r it's used up like the first one, so carry it into the hardest fights only."]),''')
f.header("tf_charm_keeping", '''Q("tf_charm_keeping", -8, 8, [item(TF + "charm_of_keeping_1")], "Charm of Keeping", deps=["tf_maze_map"], xp=100,
      mirror="610F9E9D0B5131C7", subtitle="Keep your things when you fall", desc=[''')
f.header("tf_charm_upgrade", '''Q("tf_charm_upgrade", -10, 8, [item(TF + "charm_of_keeping_2")], "Charm of Keeping II",
      deps=["tf_charm_keeping"], xp=150, mirror="4665E6FD0AAED164", subtitle="Four charms make one better", desc=[''')
S("tf_charm_upgrade", "&eWhat:&r combine charms into a higher tier: Charm of Life II, or Charm of Keeping II and III.",
  "&eWhat:&r the second Charm of Keeping saves more of your inventory when you die than the first.")
S("tf_charm_upgrade", "&eHow:&r four of a tier, shapeless, make one of the next tier (check JEI).",
  "&eHow:&r four Charms of Keeping I, shapeless, make one Charm of Keeping II (check JEI).")
S("tf_charm_upgrade", "&eTip:&r a Charm of Keeping III keeps your whole inventory, so it's worth saving sixteen of the first tier.",
  "&eTip:&r don't stop here: the third tier is the one worth carrying.")
f.after("tf_charm_upgrade", '''    Q("tf_charm_keeping3", 0, 0, [item(TF + "charm_of_keeping_3")], "Charm of Keeping III", deps=["tf_charm_upgrade"], xp=250, size=1.5,
      mirror="3A3ED88027331A6C", subtitle="Die, and keep everything", desc=[
        "&6Even death used to hand your things back. You remember why.&r",
        "&eWhat:&r the top Charm of Keeping: when it's used up, you keep your whole inventory.",
        "&eHow:&r four Charms of Keeping II make one (check JEI). That's sixteen of the first tier in all.",
        "&eTip:&r one in your pocket turns a lost boss fight into a long walk back."]),''')
# ram
f.header("tf_ram_trophy", '''Q("tf_ram_trophy", 0, 0, [item(TF + "quest_ram_trophy")], "The Ram's Own Trophy", deps=["tf_arrive"], xp=100,
      optional=True, tokens=2, loot="secret", mirror="4DA0725E089D7C91", section="Forest Treasures",
      subtitle="Optional: a bundle with a head in it", desc=[''')
f.save()
