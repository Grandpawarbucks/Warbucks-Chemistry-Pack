import sys; sys.path.insert(0, 'scratchpad/c6b')
from qedit import F
f = F('tools/quests/twilight.py')
S = f.sub
H = f.header

# --- Naga ---
H("tf_courtyard", '''Q("tf_courtyard", 0, 0, [structure(TF + "naga_courtyard"), kill(TF + "naga")], "The Naga's Courtyard", deps=["tf_arrive"], xp=150,
      optional=True, tokens=1, loot="boss", subtitle="Optional: find the serpent's courtyard and win", desc=[''')
S("tf_courtyard", '''        "&6You remember this twilight. You walked here once, when the forest was young.&r",
''', "")
H("w_naga", '''Q("w_naga", 0, 2, [item(TF + "naga_trophy"), item(TF + "naga_scale", 4)], "The Naga", deps=["tf_arrive"], xp=200,
      mirror="3531B28F14CF72A2", section="The Boss Trail", subtitle="Trophy and scales from the forest's first boss", desc=[''')
S("w_naga", "&eHow:&r the Naga drops scales and its trophy when it dies. Hit it when it stops charging; stay out of its coils.",
  "&eHow:&r its courtyard is a walled stone garden in the plain forest (the Magic Map marks it). The Naga drops its trophy and scales; hit it when it stops charging.")
H("tf_naga_armor", '''Q("tf_naga_armor", 0, -2, [item(TF + "naga_chestplate"), item(TF + "naga_leggings")], "Naga Scale Armour", deps=["w_naga"], xp=150,
      mirror="4D4AB60B3B1CD437", subtitle="Armour from the serpent", desc=[''')
# --- Lich ---
H("tf_lich_tower", '''Q("tf_lich_tower", 4, 0, [structure(TF + "lich_tower"), kill(TF + "lich")], "The Lich Tower", deps=["w_naga"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: climb the tower and break the sorcerer", desc=[''')
H("w_lich", '''Q("w_lich", 4, 2, [item("twilightforest:lich_trophy")], "The Lich", deps=["w_naga"], xp=300, mirror="0107D516E038E0DB",
      subtitle="A sorcerer's trophy and scepters", desc=[''')
H("tf_scepters", '''Q("tf_scepters", 4, -2, [item(TF + "twilight_scepter")], "Scepter of Twilight", deps=["w_lich"], xp=150,
      mirror="212EC1F41227184D", section="Scepters of the Lich", subtitle="Bolts of pure dusk", desc=[''')
S("tf_scepters", "&eWhat:&r the Lich drops one scepter per kill: Twilight (fires bolts), Zombie (raises loyal zombies), Lifedrain (heals you as it hurts) and Fortification (a shield).",
  "&eWhat:&r the Lich drops one of four scepters per kill. This one fires bolts of twilight energy at whatever you aim at.")
S("tf_scepters", "&eHow:&r other Lich Towers have their own Lich. Beat it again to collect the set.",
  "&eHow:&r if your Lich dropped a different scepter, other Lich Towers have their own Lich. Beat one again.")
f.after("tf_scepters", '''    Q("tf_scepter_lifedrain", 0, 0, [item(TF + "lifedrain_scepter")], "Scepter of Lifedrain", deps=["w_lich"], xp=150,
      mirror="6CB1BFBA10DF24E4", subtitle="Hurt them, heal yourself", desc=[
        "&eWhat:&r a scepter that drains a target's health in a steady beam and feeds some of it back to you.",
        "&eHow:&r one of the four scepters the Lich can drop. Fight more Liches until it turns up.",
        "&eTip:&r its charge runs down; recharge it on a crafting grid (check JEI)."]),
    Q("tf_scepter_zombie", 0, 0, [item(TF + "zombie_scepter")], "Scepter of Zombies", deps=["w_lich"], xp=150,
      mirror="3908F7C80154D9CA", subtitle="Raise a few loyal dead", desc=[
        "&eWhat:&r a scepter that summons zombies that fight for you for a while before they crumble.",
        "&eHow:&r one of the four scepters the Lich can drop.",
        "&eTip:&r summon them in a doorway: they hold a corridor while you heal."]),
    Q("tf_scepter_fort", 0, 0, [item(TF + "fortification_scepter")], "Scepter of Fortification", deps=["w_lich"], xp=150,
      mirror="3371570F189DF994", subtitle="Shields that circle you", desc=[
        "&eWhat:&r a scepter that wraps you in orbiting shields, the same trick the Lich used on you.",
        "&eHow:&r one of the four scepters the Lich can drop.",
        "&eTip:&r cast it before a boss's opening attack, not after it."]),''')
# --- Labyrinth / Minoshroom ---
H("tf_maze_map", '''Q("tf_maze_map", 8, -4, [anyof(tf("maze_map", "filled_maze_map")), item(TF + "raw_meef", 3)], "Into the Labyrinth", deps=["w_lich"], xp=150,
      mirror="4B95D48D7525FFAD", section="The Labyrinth", subtitle="A maze map and a few cuts of meef", desc=[''')
S("tf_maze_map", "&eWhat:&r a map that draws the tunnels around you at your own depth.",
  "&eWhat:&r the swamp labyrinth under the Lich's old lands: a Maze Map to find your way and meef from the minotaurs that patrol it.")
S("tf_maze_map", "&eHow:&r eight paper around a Maze Map Focus makes a blank Maze Map. Use it in the labyrinth to fill it in.",
  "&eHow:&r minotaurs drop raw meef and the Maze Map Focus; eight paper around the focus makes a blank Maze Map (blank or filled counts).")
H("tf_maze_focus", '''Q("tf_maze_focus", 8, -2, [item(TF + "maze_map_focus")], "Maze Map Focus", deps=["w_lich"], xp=150,
      optional=True, tokens=1, subtitle="Optional: a minotaur's map lens", desc=[''')
H("tf_labyrinth", '''Q("tf_labyrinth", 8, 0, [structure(TF + "labyrinth"), kill(TF + "minoshroom")], "The Labyrinth", deps=["tf_maze_map"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: the maze under the swamp", desc=[''')
H("tf_mazebreaker", '''Q("tf_mazebreaker", 6, -2, [item(TF + "mazebreaker_pickaxe")], "Mazebreaker", deps=["tf_maze_map"], xp=250,
      mirror="51BC981AB4CFAD95", subtitle="The labyrinth's jackpot", desc=[''')
H("tf_minotaur_axe", '''Q("tf_minotaur_axe", 10, -2, [item(TF + "diamond_minotaur_axe")], "Minotaur Axe", deps=["w_minoshroom"], xp=150,
      mirror="730AF9210F00018E", subtitle="The Minoshroom's weapon", desc=[''')
H("tf_ore_map", '''Q("tf_ore_map", 8, -6, [anyof(tf("ore_map", "filled_ore_map"))], "Ore Map", deps=["tf_maze_map"], xp=200,
      optional=True, tokens=2, mirror="6F957D07AA74F16E", subtitle="Optional: a map that shows ore", desc=[''')
S("tf_ore_map", "Use it to fill it in.", "Blank or filled counts.")
H("w_minoshroom", '''Q("w_minoshroom", 8, 2, [item("twilightforest:minoshroom_trophy"), item(TF + "meef_stroganoff")], "The Minoshroom", deps=["tf_maze_map"], xp=300,
      mirror="04440BB2EFFD6DD9", subtitle="Its trophy and its stroganoff", desc=[''')
S("w_minoshroom", "&eTip:&r don't eat all the stroganoff at once; the next quest needs one.",
  "&eTip:&r keep one bowl of stroganoff in your bag for this quest, and eat another before the fire swamp.")
H("tf_stroganoff", '''Q("tf_stroganoff", 10, 2, [item(TF + "meef_stroganoff")], "Mighty Stroganoff", deps=["w_minoshroom"], xp=150,
      optional=True, tokens=1, subtitle="Optional: eat it to bear the fire swamp", desc=[''')
# --- Hydra ---
H("tf_hydra_lair", '''Q("tf_hydra_lair", 12, 0, [structure(TF + "hydra_lair"), kill(TF + "hydra")], "The Hydra's Lair", deps=["w_minoshroom"], xp=250,
      optional=True, tokens=1, loot="boss", subtitle="Optional: a cave in the fire swamp", desc=[''')
H("w_hydra", '''Q("w_hydra", 12, 2, [item("twilightforest:hydra_trophy")], "The Hydra", deps=["w_minoshroom"], xp=400,
      mirror="7026E46FD8B3A81D", subtitle="Three heads in the fire swamp", desc=[''')
S("w_hydra", "&eHow:&r fire resistance potions help. Hit the heads when they lunge at you; they regrow, so keep up the pressure.",
  "&eHow:&r eat meef stroganoff first or the fire swamp burns you. Fire resistance helps; hit the heads when they lunge, and keep up the pressure.")
H("tf_fiery", '''Q("tf_fiery", 12, 4, [item(TF + "fiery_ingot", 4)], "Fiery Metal", deps=["w_hydra"], xp=200,
      optional=True, tokens=1, subtitle="Optional: iron quenched in burning blood", desc=[''')
H("tf_fiery_gear", '''Q("tf_fiery_gear", 10, 6, [item(TF + "fiery_sword"), item(TF + "fiery_pickaxe")],
      "Fiery Sword and Pickaxe", deps=["w_hydra"], xp=200, mirror="111F2EE85FB0A455", subtitle="A pickaxe that smelts as it digs", desc=[''')
S("tf_fiery_gear", "&eHow:&r fiery ingots with blaze rods for the tools, or alone for the armour (check JEI).",
  "&eHow:&r fiery ingots with blaze rods (check JEI). The Fiery Metal side quest shows how to make the ingots.")
f.after("tf_fiery_gear", '''    Q("tf_fiery_armor", 0, 0, [item(TF + "fiery_helmet"), item(TF + "fiery_chestplate"), item(TF + "fiery_leggings"), item(TF + "fiery_boots")],
      "Fiery Armour", deps=["w_hydra"], xp=200, mirror="1FF5906DF721D091", subtitle="A suit that burns whoever hits it", desc=[
        "&eWhat:&r armour of fiery metal: tough, and it sets attackers alight when they strike you.",
        "&eChemistry:&r a metal that glows when hot is showing black-body radiation: the hotter it gets, the more its light shifts from dull red to yellow-white.",
        "&eHow:&r fiery ingots in the usual armour shapes (check JEI). Fiery blood from the Hydra or fiery tears from the Ur-Ghast make the ingots.",
        "&eTip:&r it pairs well with the fire swamp, where everything else around you is burning anyway."]),''')
H("tf_armor_shards", '''Q("tf_armor_shards", 14, 4, [item(TF + "armor_shard", 9)], "Armour Shards", deps=["w_hydra"], xp=150,
      optional=True, tokens=1, subtitle="Optional: knock the plates off goblins", desc=[''')
H("tf_knightmetal", '''Q("tf_knightmetal", 14, 6, [item(TF + "armor_shard_cluster"), item(TF + "knightmetal_ingot", 4)], "Knightmetal", deps=["tf_armor_shards"], xp=200,
      optional=True, tokens=1, subtitle="Optional: melt the shards back together", desc=[''')
# --- Knights ---
H("tf_knight_gear", '''Q("tf_knight_gear", 16, 6, [item(TF + "knightmetal_helmet"), item(TF + "knightmetal_chestplate"), item(TF + "knightmetal_leggings"),
                                 item(TF + "knightmetal_boots")],
      "Knightmetal Armour", deps=["w_knight"], xp=200, mirror="25906B43A198B72F", section="The Knight's Armoury",
      subtitle="Plate fit for the phantoms", desc=[''')
S("tf_knight_gear", "&eWhat:&r knightmetal tools and armour, or the phantom helmet and chestplate the Knight Phantoms sometimes drop.",
  "&eWhat:&r a full set of knightmetal armour, the heaviest plate the forest makes.")
S("tf_knight_gear", "&eHow:&r craft any knightmetal piece (check JEI), or take phantom armour from the phantoms' drops.",
  "&eHow:&r knightmetal ingots in the usual armour shapes (check JEI). The Knightmetal side quest shows how to make the ingots.")
S("tf_knight_gear", "&eTip:&r the phantoms also drop knightmetal weapons, so the fight can pay for itself.",
  "&eTip:&r the phantoms drop knightmetal weapons too, so the fight helps pay for the set.")
f.after("tf_knight_gear", '''    Q("tf_phantom_armor", 0, 0, [item(TF + "phantom_helmet"), item(TF + "phantom_chestplate")], "Phantom Armour", deps=["w_knight"], xp=200,
      mirror="0A207A437AF153AA", subtitle="A ghost knight's helm and plate", desc=[
        "&eWhat:&r the phantom helmet and chestplate, worn by the Knight Phantoms and dropped when they fall. Both come enchanted.",
        "&eHow:&r beat the Knight Phantoms; their armour drops with their loot. Another stronghold has another six phantoms if you're missing a piece.",
        "&eTip:&r phantom armour can't be crafted, so repair it with knightmetal rather than letting it break."]),''')
H("tf_block_chain", '''Q("tf_block_chain", 18, 6, [item(TF + "knightmetal_sword"), item(TF + "knightmetal_pickaxe"), item(TF + "knightmetal_axe"),
                                 item(TF + "block_and_chain"), item(TF + "knightmetal_shield")],
      "Knight's Arms", deps=["w_knight"], xp=250, mirror="607D592CE102C82E", subtitle="Sword, pickaxe, axe, flail and shield", desc=[''')
S("tf_block_chain", "&eWhat:&r the Block and Chain is a thrown flail that smashes blocks and mobs; the Knightmetal Shield blocks like a wall.",
  "&eWhat:&r the full knightmetal arsenal: sword, pickaxe and axe, the Block and Chain (a thrown flail that smashes blocks and mobs) and the Knightmetal Shield.")
S("tf_block_chain", "&eHow:&r both start with a knightmetal ring (four ingots in a ring). Block and Chain: block + 3 ingots + ring. Shield: ingots, ring and towerwood (check JEI).",
  "&eHow:&r the tools use knightmetal ingots in the usual shapes. The flail and shield start with a knightmetal ring; the shield also needs towerwood (check JEI).")
H("tf_stronghold", '''Q("tf_stronghold", 16, 0, [structure(TF + "knight_stronghold"), kill(TF + "knight_phantom", 6)], "The Goblin Stronghold", deps=["w_hydra"], xp=300,
      optional=True, tokens=1, loot="boss", subtitle="Optional: six phantoms under the dark forest", desc=[''')
H("w_knight", '''Q("w_knight", 16, 2, [item("twilightforest:knight_phantom_trophy")], "The Knight Phantoms", deps=["w_hydra"], xp=400,
      mirror="3DCF26B53AE1EBF6", subtitle="Six ghosts in the goblin stronghold", desc=[''')
# --- Ur-Ghast ---
H("tf_dark_tower", '''Q("tf_dark_tower", 20, 0, [structure(TF + "dark_tower"), kill(TF + "ur_ghast")], "The Dark Tower", deps=["w_knight"], xp=350,
      optional=True, tokens=1, loot="boss", subtitle="Optional: climb to the Ur-Ghast", desc=[''')
H("tf_carminite", '''Q("tf_carminite", 20, -2, [item(TF + "carminite", 4)], "Carminite", deps=["tf_dark_tower"], xp=200,
      optional=True, tokens=1, subtitle="Optional: the red gem that runs the tower", desc=[''')
H("tf_tower_devices", '''Q("tf_tower_devices", 20, -4, [item(TF + "carminite_builder"), item(TF + "carminite_reactor")],
      "Tower Machinery", deps=["w_urghast"], xp=200, mirror="7B4A687EB505C2FF", subtitle="A bridge builder and a carminite reactor", desc=[''')
S("tf_tower_devices", "&eWhat:&r the redstone gadgets of the Dark Tower: blocks that vanish and reappear, a builder that lays bridges, and the carminite reactor.",
  "&eWhat:&r two of the Dark Tower's devices: the Carminite Builder, which lays a temporary bridge in the direction you face, and the Carminite Reactor.")
S("tf_tower_devices", "&eHow:&r encased towerwood + carminite, with redstone, a dispenser or redstone ore depending on the device (check JEI).",
  "&eHow:&r encased towerwood and carminite, with a dispenser for the builder and redstone ore for the reactor (check JEI).")
S("tf_tower_devices", "&eTip:&r vanishing blocks make secret doors for your base; a redstone pulse opens them.",
  "&eTip:&r treat the reactor with care: read its JEI page before you power one.")
f.after("tf_tower_devices", '''    Q("tf_vanishing", 0, 0, [item(TF + "reappearing_block"), item(TF + "vanishing_block")], "Now You See It", deps=["w_urghast"], xp=150,
      mirror="01748C2CD9C97523", subtitle="Blocks that vanish on a signal", desc=[
        "&eWhat:&r the Dark Tower's trick doors: a vanishing block disappears when powered, a reappearing block vanishes and then comes back by itself.",
        "&eHow:&r encased towerwood with carminite and redstone (check JEI for each recipe).",
        "&eTip:&r a hidden base entrance: a pressure plate and a wall of vanishing blocks."]),''')
H("w_urghast", '''Q("w_urghast", 20, 2, [item("twilightforest:ur_ghast_trophy")], "The Ur-Ghast", deps=["w_knight"], xp=500,
      mirror="688C911ECFB2F134", subtitle="The ghast queen of the Dark Tower", desc=[''')
# --- Yeti / Snow Queen ---
H("tf_yeti_cave", '''Q("tf_yeti_cave", 4, 10, [structure(TF + "yeti_cave"), kill(TF + "alpha_yeti")], "The Yeti Cave", deps=["w_urghast"], xp=200,
      optional=True, tokens=1, loot="boss", subtitle="Optional: a cave in the snowy forest", desc=[''')
H("tf_arctic", '''Q("tf_arctic", 2, 12, [item(TF + "arctic_fur", 4), item(TF + "arctic_helmet"), item(TF + "arctic_chestplate"), item(TF + "arctic_leggings"),
                       item(TF + "arctic_boots")],
      "Arctic Armour", deps=["w_yeti"], xp=200, mirror="2A0B3C91D72E8B75", subtitle="Dyeable armour from yeti fur", desc=[''')
S("tf_arctic", "&eHow:&r kill yetis in the snowy forest. Arctic armour uses the usual shapes (check JEI).",
  "&eHow:&r kill yetis in the snowy forest for fur, then make all four pieces in the usual shapes (check JEI). Keep 4 spare fur.")
H("w_yeti", '''Q("w_yeti", 4, 12, [item("twilightforest:alpha_yeti_trophy")], "The Alpha Yeti", deps=["w_urghast"], xp=300,
      mirror="31BB7EB95CE73C1A", subtitle="The snowy forest's boss", desc=[''')
S("w_yeti", "&eTip:&r carrying alpha yeti fur is what lets you bear the glacier's cold.",
  "&eTip:&r the snowy forest opens after the Lich, so you can fight it early; carrying alpha yeti fur lets you bear the glacier's cold.")
H("tf_yeti_armor", '''Q("tf_yeti_armor", 4, 14, [item(TF + "yeti_helmet"), item(TF + "yeti_chestplate"), item(TF + "yeti_leggings"), item(TF + "yeti_boots")],
      "Yeti Armour", deps=["w_yeti"], xp=250, mirror="3C8724C3A9459507", subtitle="The Alpha Yeti's coat", desc=[''')
H("tf_aurora", '''Q("tf_aurora", 8, 10, [structure(TF + "aurora_palace"), kill(TF + "snow_queen")], "The Aurora Palace", deps=["w_yeti"], xp=300,
      optional=True, tokens=1, loot="boss", subtitle="Optional: an ice palace on the glacier", desc=[''')
H("tf_ice_weapons", '''Q("tf_ice_weapons", 10, 10, [item(TF + "ice_sword")], "Ice Sword", deps=["tf_arrive"], xp=150,
      mirror="78CE2ECEF0B651DA", section="Forest Treasures", subtitle="A blade that slows what it cuts", desc=[''')
S("tf_ice_weapons", "&eWhat:&r the Aurora Palace's chests hold the Ice Sword and Ice Bow, which slow what they hit, and the Ender Bow, which swaps you with your target.",
  "&eWhat:&r a sword of enchanted ice that slows whatever it hits.")
S("tf_ice_weapons", "&eHow:&r loot the palace's rooms and caches on your way up.", "&eHow:&r a treasure from the Aurora Palace's chests (and other forest caches); check every room on the way up.")
S("tf_ice_weapons", "&eTip:&r the Ender Bow is a fine escape tool: shoot a mob far away and trade places.", "&eTip:&r slowed enemies can't chase; use it to kite anything fast.")
f.after("tf_ice_weapons", '''    Q("tf_ice_bow", 0, 0, [item(TF + "ice_bow")], "Ice Bow", deps=["tf_arrive"], xp=150, mirror="49EE6D2A3684A510",
      section="Forest Treasures", subtitle="Arrows that chill", desc=[
        "&eWhat:&r a bow whose arrows slow whatever they hit.",
        "&eChemistry:&r cold slows everything down, chemistry included: a common rule of thumb is that many reaction rates roughly halve for every 10 °C drop.",
        "&eHow:&r a treasure from the Aurora Palace and other forest chests.",
        "&eTip:&r slow the Snow Queen's guardians before they reach you."]),
    Q("tf_ender_bow", 0, 0, [item(TF + "ender_bow")], "Ender Bow", deps=["tf_arrive"], xp=150, mirror="3D29EF7F150F5334",
      section="Forest Treasures", subtitle="Swap places with what you shoot", desc=[
        "&eWhat:&r a bow whose arrows swap you with the mob they hit.",
        "&eHow:&r a treasure from forest chests (the Aurora Palace and hollow hills among them).",
        "&eTip:&r an escape tool: shoot a mob far away and trade places with it."]),''')
H("tf_glass_sword", '''Q("tf_glass_sword", 0, 0, [item(TF + "glass_sword")], "One Hit Wonder", deps=["tf_arrive"], xp=150,
      mirror="38ADDF7FF4E4892D", section="Forest Treasures", subtitle="A blade that shatters on first use", desc=[''')
H("w_snow_queen", '''Q("w_snow_queen", 8, 12, [item("twilightforest:snow_queen_trophy")], "The Snow Queen", deps=["w_yeti"], xp=400,
      mirror="6FD41DF7704466A4", subtitle="The glacier's ice palace", desc=[''')
H("tf_queen_bows", '''Q("tf_queen_bows", 8, 14, [item(TF + "triple_bow")], "Tri-Bow", deps=["w_snow_queen"], xp=200,
      mirror="53A79338994088FD", subtitle="Three arrows at once", desc=[''')
S("tf_queen_bows", "&eWhat:&r the Snow Queen drops one of two bows: the Tri-Bow fires three arrows at once, the Seeker Bow's arrows home in on targets.",
  "&eWhat:&r the Tri-Bow fires three arrows in a spread with every shot.")
S("tf_queen_bows", "&eHow:&r beat the Snow Queen; one bow drops with her trophy.", "&eHow:&r the Snow Queen drops one of her two bows with her trophy; beat another Queen if you got the Seeker Bow.")
S("tf_queen_bows", "&eTip:&r the Seeker Bow is perfect against the flying Ur-Ghast's ghastlings.", "&eTip:&r a spread shot is made for crowds: point it at a swarm and loose.")
f.after("tf_queen_bows", '''    Q("tf_seeker_bow", 0, 0, [item(TF + "seeker_bow")], "Seeker Bow", deps=["w_snow_queen"], xp=200, mirror="7509E4093010EA4C",
      subtitle="Arrows that find their mark", desc=[
        "&eWhat:&r the Seeker Bow's arrows curve towards the nearest target.",
        "&eHow:&r the Snow Queen drops one of her two bows; fight another Queen if you got the Tri-Bow.",
        "&eTip:&r perfect against fliers like ghastlings that never hold still."]),''')
# --- Highlands and the end ---
H("tf_highlands", '''Q("tf_highlands", 24, 8, [biome(TF + "highlands"), biome(TF + "thornlands")], "The Highlands", deps=["w_urghast", "w_snow_queen"], xp=300,
      optional=True, tokens=2, subtitle="Optional: the plateau beyond every barrier", desc=[''')
H("tf_magic_beans", '''Q("tf_magic_beans", 27, 10.5, [item(TF + "magic_beans"), item(TF + "uberous_soil")], "Magic Beans", deps=["w_snow_queen"], xp=200,
      mirror="58BD1063A19777DC", section="Beyond the Thorns", subtitle="Beans, and soil rich enough to grow them", desc=[''')
S("tf_magic_beans", "&eHow:&r kill trolls or loot their gardens (the gardens also hold uberous soil). Plant a bean on the glowing soil under the clouds.",
  "&eHow:&r troll caves in the highlands: kill trolls for beans and loot their gardens for uberous soil. Plant a bean on the soil under the clouds.")
H("tf_giants", '''Q("tf_giants", 30, 10.5, [item(TF + "giant_pickaxe")], "Giant's Pickaxe", deps=["tf_magic_beans"], xp=250,
      mirror="20436AFCC7E6855D", subtitle="A pickaxe the size of a house", desc=[''')
S("tf_giants", "&eWhat:&r giant miners drop the Giant's Pickaxe, which breaks the oversized blocks of the cloud world; armoured giants drop the Giant's Sword.",
  "&eWhat:&r the Giant's Pickaxe breaks the oversized blocks of the cloud world in one go.")
S("tf_giants", "&eHow:&r climb the beanstalk to the clouds and beat a giant. Both can also be crafted from giant cobblestone and giant logs (check JEI).",
  "&eHow:&r climb the beanstalk to the clouds and beat a giant miner, or craft one from giant cobblestone and giant logs (check JEI).")
H("tf_troll_cave", '''Q("tf_troll_cave", 27, 8, [item(TF + "lamp_of_cinders")], "The Lamp of Cinders", deps=["tf_giants"], xp=250,
      mirror="5CBA8C89FE717B9C", subtitle="A lamp that burns away the thorns", desc=[''')
S("tf_troll_cave", "&eWhat:&r caves under the highlands, full of trolls guarding vaults. The Lamp of Cinders hides in one.",
  "&eWhat:&r the Lamp of Cinders, the key to the forest's last region. It sits in a troll cave vault under the highlands.")
H("tf_thorn_rose", '''Q("tf_thorn_rose", 0, 0, [item(TF + "thorn_rose", 12)], "Thorn Roses", deps=["tf_troll_cave"], xp=150,
      mirror="2951B1D7080C5EF9", subtitle="A dozen flowers from among the thorns", desc=[''')
S("tf_thorn_rose", "&eHow:&r pick them carefully at the thornlands' edge; living thorns hurt to touch.",
  "&eHow:&r pick twelve at the thornlands' edge; living thorns hurt to touch.")
f.after("tf_thorn_rose", '''    Q("tf_castle_doors", 0, 0, [item(TF + "pink_castle_door", 12), item(TF + "yellow_castle_door", 12), item(TF + "blue_castle_door", 12),
                                item(TF + "violet_castle_door", 12)],
      "Rune Doors", deps=["tf_thorn_rose"], xp=300, mirror="420158B1736A1354", subtitle="Twelve of each of the castle's coloured doors", desc=[
        "&eWhat:&r the Final Castle's rune doors come in four colours, one for each wing of the castle.",
        "&eHow:&r burn through the thorns with the Lamp of Cinders, climb onto the final plateau and mine the doors out of the castle walls. Twelve of each colour.",
        "&eTip:&r the doors vanish when activated; mine them while they're solid."]),''')
H("tf_final_plateau", '''Q("tf_final_plateau", 30, 8, [biome(TF + "final_plateau")], "The Final Plateau", deps=["tf_troll_cave"], xp=300,
      optional=True, tokens=1, subtitle="Optional: burn through the thorns", desc=[''')
H("tf_final_castle", '''Q("tf_final_castle", 33, 8, [structure(TF + "final_castle")], "The Unfinished Castle", deps=["tf_final_plateau"], xp=300,
      optional=True, tokens=2, loot="boss", subtitle="Optional: the castle at the top of the world", desc=[''')
f.save()
