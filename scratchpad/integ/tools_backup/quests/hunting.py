"""Quest chapter: hunting (sidebar title "Bounty Board": monster bounties with kill counts). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Prefix hn_. Kill quests use loot="hunt", bosses loot="boss". Tiers of 100+ kills are optional.
Retitled "Bounty Board" 2026-10-19 (ATM10's shape: one column per mob, tiers going down). The eight core mobs
(zombie, skeleton, creeper, spider, enderman, witch, blaze, wither skeleton) now all have three tiers, and the
Moon and Venus have bounties too. Keys unchanged.
Boss kills that live on other pages (Ender Dragon, Warden, Forgotten Guardian, the Twilight bosses) are shown as links.
Columns: tiers run left to right (x=0/2/4); the Overworld block is x=0..4, raids and oceans x=8..12,
the Nether x=16..20; other dimensions on y=12+; boss links from other pages on y=-3/-5.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

MC = "minecraft:"
TF = "twilightforest:"
UG = "undergarden:"
DD = "deeperdarker:"

CHAPTER = Chapter("hunting", "Bounty Board", "minecraft:zombie_head",
        ["Bounties on every monster. Each one is just chemistry with bad manners."], SIDE, [
    # --- the Overworld: undead (x=0..4) --------------------------------------------------------
    Q("hn_zombie_1", 0, 0, [kill(MC + "zombie", 25)], "Zombie Hunter", section="The Undead", deps=["gs_shield"], xp=50,
      loot="hunt", subtitle="Kill 25 zombies", desc=[
        "&6You remember when the dead stayed down out of respect. Time to remind them.&r",
        "&eWhat:&r the first bounty on the board. Each tier asks for more of the same mob and pays out a Hunter's Bounty.",
        "&eHow:&r zombies spawn in the dark and at night everywhere. A sword and shield are all you need.",
        "&eTip:&r zombies burn in daylight; fight at dawn and let the sun help."]),
    Q("hn_zombie_2", 2, 0, [kill(MC + "zombie", 100)], "Zombie Slayer", section="The Undead", deps=["hn_zombie_1"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 zombies", desc=[
        "&eWhat:&r a hundred zombies. You'll get there just by playing at night.",
        "&eChemistry:&r rotten flesh really is rotten: bacteria break proteins into amines like putrescine and cadaverine, which is where the smell comes from.",
        "&eTip:&r a simple dark room over a spawner (YUNG's dungeons have plenty) speeds this up."]),
    Q("hn_zombie_3", 4, 0, [kill(MC + "zombie", 500)], "Bane of the Dead", section="The Undead", deps=["hn_zombie_2"], xp=300,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 500 zombies", desc=[
        "&eWhat:&r five hundred. This one is for people who build mob farms.",
        "&eHow:&r a zombie spawner trap with a killing floor, or a Smite sword and a lot of nights.",
        "&eTip:&r Smite adds damage against all undead: zombies, skeletons, wither skeletons, phantoms and the Wither."]),
    Q("hn_skeleton_1", 0, 1.5, [kill(MC + "skeleton", 25)], "Bone Collector", section="The Undead", deps=["gs_shield"], xp=50,
      loot="hunt", subtitle="Kill 25 skeletons", desc=[
        "&eWhat:&r skeletons drop bones and arrows, and sometimes their bow.",
        "&eChemistry:&r bone meal is crushed bone: calcium phosphate, a real phosphorus fertiliser for plants.",
        "&eHow:&r raise your shield when they draw, then close in between shots.",
        "&eTip:&r strafing sideways makes skeletons miss most of their arrows."]),
    Q("hn_skeleton_2", 2, 1.5, [kill(MC + "skeleton", 100)], "Skeleton Slayer", section="The Undead", deps=["hn_skeleton_1"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 skeletons", desc=[
        "&eWhat:&r a hundred skeletons, and a full stack of bones for bone meal.",
        "&eHow:&r keep killing them at night, or trap a skeleton spawner.",
        "&eTip:&r a skeleton spawner farm is also an arrow farm."]),
    Q("hn_skeleton_3", 4, 1.5, [kill(MC + "skeleton", 500)], "Ossuary", section="The Undead", deps=["hn_skeleton_2"], xp=300,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 500 skeletons", desc=[
        "&eWhat:&r five hundred skeletons. Build a farm.",
        "&eHow:&r YUNG's skeleton dungeons have several spawners close together; trap them.",
        "&eTip:&r Looting raises bone and arrow drops."]),
    Q("hn_undead_kin", 0, -1.5, [kill(MC + "husk", 15), kill(MC + "stray", 15), kill(MC + "drowned", 15)], "Undead of Every Climate", section="The Undead", deps=["hn_zombie_1"], xp=100,
      loot="hunt", subtitle="Husks, strays and drowned", desc=[
        "&eWhat:&r the undead adapt to their biome: husks in deserts, strays in the snow, drowned in the water.",
        "&eHow:&r husks don't burn in daylight; strays shoot slowness arrows; drowned may carry tridents.",
        "&eTip:&r a drowned holding a trident can drop it. The trident is worth the hunt."]),
    Q("hn_drowned_2", 2, -1.5, [kill(MC + "drowned", 100)], "Tide Breaker", section="The Undead", deps=["hn_undead_kin"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 drowned", desc=[
        "&eWhat:&r a hundred drowned, for copper ingots, nautilus shells and the occasional trident.",
        "&eChemistry:&r fitting loot for the sea: copper resists seawater well, because it grows a protective skin of copper oxides and chlorides.",
        "&eHow:&r rivers and oceans at night. Channeling or Impaling help."]),

    # --- the Overworld: creepers, spiders, endermen (x=0..4) -----------------------------------
    Q("hn_creeper_1", 0, 3, [kill(MC + "creeper", 25)], "Creeper Hunter", section="Creepers and Spiders", deps=["gs_shield"], xp=50,
      loot="hunt", subtitle="Kill 25 creepers", desc=[
        "&eWhat:&r creepers drop gunpowder, the oldest chemical explosive.",
        "&eChemistry:&r gunpowder is potassium nitrate, charcoal and sulfur. The nitrate (KNO₃) supplies the oxygen: 2KNO₃ + S + 3C → K₂S + N₂ + 3CO₂.",
        "&eHow:&r hit and step back; a creeper resets its fuse when you leave its range.",
        "&eTip:&r a bow is the safest creeper tool there is."]),
    Q("hn_creeper_2", 2, 3, [kill(MC + "creeper", 100)], "Demolition Expert", section="Creepers and Spiders", deps=["hn_creeper_1"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 creepers", desc=[
        "&eWhat:&r a hundred creepers and a pile of gunpowder for TNT and rockets.",
        "&eHow:&r keep hunting at night; a Knockback sword keeps them away from you.",
        "&eTip:&r a creeper killed by a skeleton's arrow drops a music disc."]),
    Q("hn_creeper_3", 4, 3, [kill(MC + "creeper", 250)], "Ssssilence", section="Creepers and Spiders", deps=["hn_creeper_2"], xp=250,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 250 creepers", desc=[
        "&eWhat:&r two hundred and fifty creepers. The world is quieter now.",
        "&eHow:&r a mob farm, or many careful nights.",
        "&eTip:&r cats scare creepers away from your base."]),
    Q("hn_spider_1", 0, 4.5, [kill(MC + "spider", 25)], "Spider Hunter", section="Creepers and Spiders", deps=["gs_shield"], xp=50,
      loot="hunt", subtitle="Kill 25 spiders", desc=[
        "&eWhat:&r spiders drop string and spider eyes.",
        "&eChemistry:&r a fermented spider eye (eye + sugar + brown mushroom) turns potions into their opposites; real fermentation is microbes turning sugars into new compounds like ethanol and acids.",
        "&eHow:&r spiders climb walls; build with an overhang to keep them out.",
        "&eTip:&r spiders are neutral in daylight unless you hit them."]),
    Q("hn_spider_2", 2, 4.5, [kill(MC + "spider", 100)], "Arachnophobe", section="Creepers and Spiders", deps=["hn_spider_1"], xp=100,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 spiders", desc=[
        "&eWhat:&r a hundred spiders, and enough string for every bow and wool block you need.",
        "&eHow:&r spiders spawn on the surface at night; Bane of Arthropods helps.",
        "&eTip:&r string from spiders makes wool: four string per block."]),
    Q("hn_cave_spider", 6, 4.5, [kill(MC + "cave_spider", 25)], "Cave Spiders", section="Creepers and Spiders", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 25 cave spiders", desc=[
        "&eWhat:&r small, poisonous spiders that only come from spawners in mineshafts and spider caves.",
        "&eChemistry:&r milk cures poison in Minecraft; in reality there's no general antidote, and venoms are treated with antivenom antibodies.",
        "&eHow:&r find a mineshaft or YUNG's spider cave and fight near the spawner. Carry milk.",
        "&eTip:&r torches on and around the spawner stop it."]),
    Q("hn_enderman_1", 0, 6, [kill(MC + "enderman", 16)], "Pearl Diver", section="Creatures of the Night", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 16 endermen", desc=[
        "&eWhat:&r endermen drop ender pearls: teleportation, eyes of ender and many machines.",
        "&eHow:&r look at one to make it attack, then fight with your back to a 2-block-high gap; it can't follow under a low roof.",
        "&eTip:&r endermen hate water. A rain storm sends them teleporting away."]),
    Q("hn_enderman_2", 2, 6, [kill(MC + "enderman", 64)], "Enderman Slayer", section="Creatures of the Night", deps=["hn_enderman_1"], xp=150,
      loot="hunt", subtitle="Kill 64 endermen", desc=[
        "&eWhat:&r a stack of kills and, with luck, a stack of pearls.",
        "&eHow:&r warped forests in the Nether and the End are full of them.",
        "&eTip:&r a carved pumpkin on your head lets you look at endermen safely."]),
    Q("hn_enderman_3", 4, 6, [kill(MC + "enderman", 256)], "Void Walker", section="Creatures of the Night", deps=["hn_enderman_2"], xp=300,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 256 endermen", desc=[
        "&eWhat:&r four stacks of endermen. You'll need an End farm or a lot of patience.",
        "&eHow:&r an enderman farm on the outer End islands is the classic way.",
        "&eTip:&r endermites make endermen aggressive; that's how most End farms lure them."]),

    # --- the Overworld: odd ones (x=0..6, y=7.5 and 9) -----------------------------------------
    Q("hn_witch", 0, 7.5, [kill(MC + "witch", 10)], "Witch Hunt", section="Creatures of the Night", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 10 witches", desc=[
        "&eWhat:&r witches throw potions and drink their own to heal. They drop redstone, glowstone, sugar and bottles.",
        "&eChemistry:&r glowstone dust in-game is a brewing amplifier; real \"glow\" chemicals (like the zinc sulfide in glow paint) store light and release it slowly.",
        "&eHow:&r rush them; at range they out-potion you. Milk clears their effects.",
        "&eTip:&r swamp huts spawn witches over and over: a classic redstone farm."]),
    Q("hn_witch_2", 2, 7.5, [kill(MC + "witch", 50)], "Coven Breaker", section="Creatures of the Night", deps=["hn_witch"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 50 witches", desc=[
        "&eWhat:&r fifty witches and a pile of redstone and glowstone.",
        "&eHow:&r a swamp hut farm, or raids (witches join them).",
        "&eTip:&r witches are immune to most potion damage; use a sword or bow."]),
    Q("hn_slime", 4, 7.5, [kill(MC + "slime", 25)], "Slime Time", section="Creatures of the Night", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 25 slimes", optional=True, tokens=1, desc=[
        "&eWhat:&r slimes split when killed; the smallest drop slimeballs for sticky pistons and leads.",
        "&eChemistry:&r real slime is a polymer gel: long molecules cross-linked loosely enough to flow, like borax and PVA glue.",
        "&eHow:&r slimes spawn in swamps at night and in slime chunks underground.",
        "&eTip:&r every split counts as a kill. A big slime is many kills."]),
    Q("hn_phantom", 0, 9, [kill(MC + "phantom", 10)], "Night Terrors", section="Creatures of the Night", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 10 phantoms", desc=[
        "&eWhat:&r phantoms dive at players who haven't slept for three nights. Their membranes repair elytra.",
        "&eHow:&r stay up three nights, then fight with a bow on open ground at night.",
        "&eTip:&r once you're done, sleep: it resets the timer and phantoms stop coming."]),
    Q("hn_phantom_2", 2, 9, [kill(MC + "phantom", 50)], "Skyclearer", section="Creatures of the Night", deps=["hn_phantom"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 50 phantoms", desc=[
        "&eWhat:&r fifty phantoms, and enough membranes to keep an elytra flying for a long time.",
        "&eHow:&r a bow with Power, or a trident with Loyalty, and a sleepless week.",
        "&eTip:&r phantoms are undead; Smite works on them."]),
    Q("hn_silverfish", 8, 4.5, [kill(MC + "silverfish", 50)], "Pest Control", section="Creepers and Spiders", deps=["hn_cave_spider"], xp=75,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 50 silverfish", desc=[
        "&eWhat:&r silverfish hide in infested stone in strongholds and mountains, and call their friends when hurt.",
        "&eHow:&r YUNG's strongholds are full of infested blocks; a single blow kills each one.",
        "&eTip:&r don't break blocks near a silverfish fight; you'll wake more."]),
    Q("hn_trials", 6, 9, [kill(MC + "breeze", 10), kill(MC + "bogged", 10)], "The Trials", section="Raiders and the Sea", deps=["gs_shield"], xp=150,
      loot="hunt", subtitle="Kill 10 breezes and 10 bogged", optional=True, tokens=1, desc=[
        "&eWhat:&r two mobs from 1.21: breezes (wind spirits) and bogged (mossy skeletons with poison arrows), both from trial chambers.",
        "&eHow:&r find a trial chamber (see the Exploration page) and fight the trial spawners.",
        "&eTip:&r breeze rods make wind charges and the mace."]),

    # --- raids and oceans (x=8..12) ------------------------------------------------------------
    Q("hn_pillager", 10, 3, [kill(MC + "pillager", 25)], "Pillager Hunter", section="Raiders and the Sea", deps=["gs_shield"], xp=75,
      loot="hunt", subtitle="Kill 25 pillagers", desc=[
        "&eWhat:&r crossbow-armed illagers from outposts and patrols.",
        "&eHow:&r a shield blocks their bolts. Outposts respawn pillagers around the tower.",
        "&eTip:&r a captain (banner on its head) gives Bad Omen when killed: drink the ominous bottle to start a raid."]),
    Q("hn_pillager_2", 12, 3, [kill(MC + "pillager", 100)], "Outpost Breaker", section="Raiders and the Sea", deps=["hn_pillager"], xp=150,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 pillagers", desc=[
        "&eWhat:&r a hundred pillagers.",
        "&eHow:&r camp an outpost or run raids. Raids bring them in waves.",
        "&eTip:&r a raid farm is the best emerald source in the game."]),
    Q("hn_vindicator", 10, 4.5, [kill(MC + "vindicator", 10)], "Axes of Malice", section="Raiders and the Sea", deps=["hn_pillager"], xp=100,
      loot="hunt", subtitle="Kill 10 vindicators", desc=[
        "&eWhat:&r axe-wielding illagers from raids and woodland mansions. They hit very hard.",
        "&eHow:&r keep your shield up; their axes can disable it, so back off after a block.",
        "&eTip:&r a vindicator named \"Johnny\" attacks every mob in sight."]),
    Q("hn_evoker", 12, 4.5, [kill(MC + "evoker", 3)], "Evoker Bane", section="Raiders and the Sea", deps=["hn_vindicator"], xp=150,
      loot="hunt", subtitle="Kill 3 evokers", optional=True, tokens=1, desc=[
        "&eWhat:&r evokers summon fangs and vexes. Each one drops a Totem of Undying.",
        "&eHow:&r they come in later raid waves and live in woodland mansions. Kill the evoker first; its vexes die with it.",
        "&eTip:&r keep a totem in your off-hand when fighting raids."]),
    Q("hn_ravager", 10, 6, [kill(MC + "ravager", 3)], "Beast of the Raid", section="Raiders and the Sea", deps=["hn_vindicator"], xp=150,
      loot="hunt", subtitle="Kill 3 ravagers", optional=True, tokens=1, desc=[
        "&eWhat:&r ravagers are huge raid beasts that trample crops and charge.",
        "&eHow:&r they appear in raids from wave 3 on. Block the charge with a shield, then counterattack while it's stunned.",
        "&eTip:&r ravagers drop saddles."]),
    Q("hn_guardian", 10, 7.5, [kill(MC + "guardian", 25)], "Guardian Hunter", section="Raiders and the Sea", deps=["gs_shield"], xp=100,
      loot="hunt", subtitle="Kill 25 guardians", desc=[
        "&eWhat:&r the spiky fish of ocean monuments. They drop prismarine shards and crystals.",
        "&eChemistry:&r prismarine is in-game sea crystal; real sea creatures build shells and spines from calcium carbonate and silica pulled out of seawater.",
        "&eHow:&r find a monument (see the Exploration page). Break line of sight when their laser charges.",
        "&eTip:&r water breathing and Depth Strider make monuments much easier."]),

    # --- the Nether (x=16..20) -----------------------------------------------------------------
    Q("hn_zpiglin", 16, 0, [kill(MC + "zombified_piglin", 50)], "Gold in the Rot", section="Nether Bounties", deps=["t2_nether"], xp=75,
      loot="hunt", subtitle="Kill 50 zombified piglins", optional=True, tokens=1, desc=[
        "&eWhat:&r zombified piglins drop gold nuggets and rotten flesh.",
        "&eHow:&r they're neutral until you hit one, then the whole crowd comes. Fight in a corridor.",
        "&eTip:&r gold farms over Nether-roof portals are a classic build."]),
    Q("hn_blaze_1", 16, 1.5, [kill(MC + "blaze", 25)], "Blaze Hunter", section="Nether Bounties", deps=["t2_nether"], xp=100,
      loot="hunt", subtitle="Kill 25 blazes", desc=[
        "&eWhat:&r blazes drop blaze rods: brewing stands, blaze powder and eyes of ender.",
        "&eChemistry:&r blazes throw fireballs; real fireballs need fuel plus oxygen, which is why a fire triangle (heat, fuel, O₂) puts them out when you remove any side.",
        "&eHow:&r blaze spawners sit in Nether fortresses. Snowballs hurt them.",
        "&eTip:&r fire resistance makes you immune to their fireballs."]),
    Q("hn_blaze_2", 18, 1.5, [kill(MC + "blaze", 100)], "Blaze Slayer", section="Nether Bounties", deps=["hn_blaze_1"], xp=200,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 blazes", desc=[
        "&eWhat:&r a hundred blazes and a good supply of rods.",
        "&eHow:&r build a blaze farm around a fortress spawner.",
        "&eTip:&r blaze rods are a good furnace fuel: 12 items each."]),
    Q("hn_ghast", 16, 3, [kill(MC + "ghast", 10)], "Ghastbuster", section="Nether Bounties", deps=["t2_nether"], xp=100,
      loot="hunt", subtitle="Kill 10 ghasts", optional=True, tokens=1, desc=[
        "&eWhat:&r ghasts drop ghast tears (regeneration potions, end crystals) and gunpowder.",
        "&eHow:&r hit their fireballs back at them with a sword or an arrow.",
        "&eTip:&r kill them over solid ground, not lava, or the tear is lost."]),
    Q("hn_magma", 18, 3, [kill(MC + "magma_cube", 50)], "Hot Jelly", section="Nether Bounties", deps=["t2_nether"], xp=75,
      loot="hunt", subtitle="Kill 50 magma cubes", optional=True, tokens=1, desc=[
        "&eWhat:&r magma cubes split like slimes and drop magma cream for fire resistance.",
        "&eHow:&r basalt deltas are full of them.",
        "&eTip:&r every split counts as a kill."]),
    Q("hn_wither_skel_1", 16, 4.5, [kill(MC + "wither_skeleton", 25)], "Skull Hunter", section="Skulls and Giants", deps=["t2_nether"], xp=100,
      loot="hunt", subtitle="Kill 25 wither skeletons", desc=[
        "&eWhat:&r tall black skeletons in Nether fortresses. They sometimes drop their skull; three summon the Wither.",
        "&eHow:&r fight in a 2-block-high tunnel; they're three blocks tall and can't follow.",
        "&eTip:&r Looting raises the skull drop chance."]),
    Q("hn_wither_skel_2", 18, 4.5, [kill(MC + "wither_skeleton", 100)], "Bonebreaker", section="Skulls and Giants", deps=["hn_wither_skel_1"], xp=200,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 100 wither skeletons", desc=[
        "&eWhat:&r a hundred wither skeletons, and enough skulls for several Withers.",
        "&eHow:&r a wither skeleton farm on a fortress platform.",
        "&eTip:&r a Smite sword kills them quickly."]),
    Q("hn_bastion", 16, 6, [kill(MC + "piglin_brute", 5), kill(MC + "hoglin", 10)], "Bastion Brawl", section="Nether Bounties", deps=["t2_nether"], xp=150,
      loot="hunt", subtitle="Kill 5 piglin brutes and 10 hoglins", optional=True, tokens=1, desc=[
        "&eWhat:&r the toughest regular Nether fighters: axe-armed piglin brutes in bastions and charging hoglins in crimson forests.",
        "&eChemistry:&r hoglins fear warped fungus; real animals avoid many plant compounds, which evolved as chemical defences.",
        "&eHow:&r brutes ignore gold armour; fight them in doorways. Hoglins drop pork and leather.",
        "&eTip:&r hoglins turn into zoglins in the Overworld, so don't bring one home."]),

    # --- other dimensions (y=12..15) -----------------------------------------------------------
    Q("hn_shulker", 0, 12, [kill(MC + "shulker", 20)], "Shell Game", section="Other Worlds", deps=["w_end"], xp=150,
      loot="hunt", subtitle="Kill 20 shulkers", optional=True, tokens=1, desc=[
        "&eWhat:&r shulkers hide in End Cities and drop shells for shulker boxes.",
        "&eHow:&r hit them when their shell opens. Their bullets make you levitate.",
        "&eTip:&r carry milk or slow falling against levitation."]),
    Q("hn_rotspawn", 2, 12, [kill(UG + "rotling", 20), kill(UG + "rotwalker", 10), kill(UG + "rotbeast", 3)], "The Rotspawn", section="Other Worlds", deps=["t4_undergarden"], xp=150,
      loot="hunt", subtitle="Undergarden's rotting horde", optional=True, tokens=1, desc=[
        "&eWhat:&r the Undergarden's undead-like rotspawn: small rotlings, tall rotwalkers and the huge rotbeast.",
        "&eHow:&r utherium weapons deal extra damage to rotspawn.",
        "&eTip:&r rotbeasts hit hard and have a lot of health; fight them in the open."]),
    Q("hn_undergarden", 4, 12, [kill(UG + "nargoyle", 5), kill(UG + "muncher", 10)], "Things in the Dark", section="Other Worlds", deps=["t4_undergarden"], xp=150,
      loot="hunt", subtitle="Nargoyles and munchers", optional=True, tokens=1, desc=[
        "&eWhat:&r more Undergarden predators: nargoyles and the hungry munchers.",
        "&eHow:&r explore the Undergarden at length; both turn up in its caverns.",
        "&eTip:&r cloggrum armour is the Undergarden's best early protection."]),
    Q("hn_sculk", 6, 12, [kill(DD + "sculk_snapper", 10), kill(DD + "sculk_centipede", 10)], "Sculk Fauna", section="Other Worlds", deps=["w_otherside"], xp=150,
      loot="hunt", subtitle="Snappers and centipedes", desc=[
        "&eWhat:&r creatures of the Otherside, grown from sculk.",
        "&eHow:&r roam the Otherside's biomes. Sneak to approach without alerting the sculk.",
        "&eTip:&r carry food and a way home; the Otherside is a long way from your base."]),
    Q("hn_stalker", 8, 12, [kill(DD + "shattered", 10), kill(DD + "stalker", 3)], "Shattered and Stalkers", section="Other Worlds", deps=["hn_sculk"], xp=200,
      loot="hunt", subtitle="The Otherside's hunters", optional=True, tokens=1, desc=[
        "&eWhat:&r shattered drop sculk bones; stalkers drop soul crystals. Both go into the soul elytra.",
        "&eHow:&r both hunt by sound like the Warden. Fight at range.",
        "&eTip:&r sneak to keep your footsteps quiet."]),
    Q("hn_aliens", 10, 12, [kill("ad_astra:martian_raptor", 10)], "Martian Raptors", section="Other Worlds", deps=["w_mars"], xp=200,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: kill 10 raptors on Mars", desc=[
        "&eWhat:&r fast predators of the Martian surface.",
        "&eChemistry:&r anything living on Mars would need to cope with perchlorates (ClO₄⁻), reactive salts found in real Martian soil.",
        "&eHow:&r land on Mars and hunt in the wastelands. Keep your suit topped up."]),
    Q("hn_tf_forest", 0, 14, [kill(TF + "redcap", 20), kill(TF + "kobold", 20), kill(TF + "swarm_spider", 20)], "Twilight Pests", section="Other Worlds", deps=["t5_twilight"], xp=150,
      loot="hunt", subtitle="Redcaps, kobolds and swarm spiders", optional=True, tokens=1, desc=[
        "&eWhat:&r the common hostile mobs of the Twilight Forest.",
        "&eHow:&r redcaps and kobolds roam the forest; swarm spiders spawn around hollow hills and spider-infested spots.",
        "&eTip:&r redcap sappers carry TNT; kill them before they light it."]),
    Q("hn_tf_swamp", 2, 14, [kill(TF + "minotaur", 10), kill(TF + "maze_slime", 10), kill(TF + "skeleton_druid", 10)], "Maze and Swamp", section="Other Worlds", deps=["w_lich"], xp=150,
      loot="hunt", subtitle="Minotaurs, maze slimes and druids", optional=True, tokens=1, desc=[
        "&eWhat:&r guardians of the labyrinth and the swamp beyond the Lich.",
        "&eHow:&r minotaurs and maze slimes fill the labyrinth; skeleton druids lurk in the forest at night.",
        "&eTip:&r maze slimes split like regular slimes."]),
    Q("hn_tf_knights", 4, 14, [kill(TF + "lower_goblin_knight", 10), kill(TF + "blockchain_goblin", 5), kill(TF + "carminite_ghastguard", 10)], "Goblins and Ghastguards",
      section="Other Worlds", deps=["w_hydra"], xp=200, loot="hunt", subtitle="Stronghold and Dark Tower guards", optional=True, tokens=1, desc=[
        "&eWhat:&r goblin knights and block-and-chain goblins hold the Goblin Stronghold; carminite ghastguards haunt the Dark Tower.",
        "&eHow:&r goblin knights ride in pairs; knock off the upper one, then finish the lower.",
        "&eTip:&r ghastguards' fireballs can be hit back like a ghast's."]),
    Q("hn_tf_snow", 6, 14, [kill(TF + "yeti", 10), kill(TF + "winter_wolf", 10)], "Snow Beasts", section="Skulls and Giants", deps=["w_lich"], xp=150,
      loot="hunt", subtitle="Yetis and winter wolves", optional=True, tokens=1, desc=[
        "&eWhat:&r the snowy forest's hunters. Yetis drop arctic fur for warm armour.",
        "&eHow:&r yetis guard the Alpha Yeti's cave; winter wolves roam the snowy forest and breathe frost.",
        "&eTip:&r winter wolves come in packs; back against a tree."]),
    Q("hn_tf_high", 8, 14, [kill(TF + "troll", 5), kill(TF + "giant_miner", 3)], "Trolls and Giants", section="Skulls and Giants", deps=["tf_highlands"], xp=250,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: the highlands' heavyweights", desc=[
        "&eWhat:&r trolls in the troll caves and giant miners on the highlands.",
        "&eHow:&r trolls throw rocks; giants swing slowly but hard. Fight both from range.",
        "&eTip:&r giant miners drop giant pickaxes."]),

    # --- bosses (Elder Guardians next to the guardian line, the Wither under the Nether block) ---------------------------------
    Q("hn_elder", 12, 7.5, [kill(MC + "elder_guardian", 3)], "Elder Guardians", section="Raiders and the Sea", deps=["hn_guardian"], xp=300,
      loot="boss", subtitle="All three elders of a monument", optional=True, tokens=1, desc=[
        "&eWhat:&r each ocean monument holds three elder guardians. They cast Mining Fatigue until all three are dead.",
        "&eHow:&r the elders sit in the top room and two wing rooms. Water breathing, a good sword and patience.",
        "&eTip:&r elders drop wet sponges and, sometimes, a tide armour trim."]),
    Q("hn_wither", 18, 6.25, [kill(MC + "wither"), item(MC + "nether_star")], "The Wither", section="Skulls and Giants", deps=["hn_wither_skel_1"], xp=500,
      size=1.5, shape="hexagon", loot="boss", subtitle="Summon it, kill it, take its star", desc=[
        "&6You remember making stars. This one you'll have to take.&r",
        "&eWhat:&r the Wither is the Nether's boss, summoned by the player. It drops a Nether Star for beacons and many late recipes.",
        "&eHow:&r four soul sand in a T with three wither skeleton skulls on top. Summon it deep underground or far from base: it destroys blocks.",
        "&eTip:&r below half health it gains armour that stops arrows; switch to a Smite sword."]),

    # --- third tiers for the core columns (2026-10-19), so every core mob has three bounties ---------------------
    Q("hn_spider_3", 0, 0, [kill(MC + "spider", 250)], "Web Breaker", section="Creepers and Spiders", deps=["hn_spider_2"], xp=250,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 250 spiders", desc=[
        "&eWhat:&r two hundred and fifty spiders. Every web in the world is a little emptier.",
        "&eChemistry:&r spider silk is a protein whose chains line up into tiny crystals; weight for weight it is tougher than steel.",
        "&eHow:&r a spider spawner farm, or long nights on the surface with Bane of Arthropods."]),
    Q("hn_witch_3", 0, 0, [kill(MC + "witch", 100)], "Hexbreaker", section="Creatures of the Night", deps=["hn_witch_2"], xp=250,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 100 witches", desc=[
        "&eWhat:&r a hundred witches, and enough redstone and glowstone to light a city.",
        "&eHow:&r a swamp hut farm is the only sane way; raids help too.",
        "&eTip:&r witches drink fire resistance when burning, so lava traps work poorly on them."]),
    Q("hn_blaze_3", 0, 0, [kill(MC + "blaze", 250)], "Flame Tamer", section="Nether Bounties", deps=["hn_blaze_2"], xp=300,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 250 blazes", desc=[
        "&eWhat:&r two hundred and fifty blazes: a lifetime supply of rods for brewing and fuel.",
        "&eChemistry:&r a blaze is fire you can kill. Real fire is just a fast oxidation reaction feeding on its own heat.",
        "&eHow:&r a blaze spawner farm in a fortress, with a killing floor and a collector."]),
    Q("hn_wither_skel_3", 0, 0, [kill(MC + "wither_skeleton", 250)], "Skullcrusher", section="Skulls and Giants", deps=["hn_wither_skel_2"], xp=300,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: kill 250 wither skeletons", desc=[
        "&eWhat:&r two hundred and fifty wither skeletons, and a crate of skulls.",
        "&eHow:&r a wither skeleton farm on a cleared fortress platform; the skeletons spawn on nether bricks.",
        "&eTip:&r coal and stone swords from them are worth smelting or dissolving, not keeping."]),

    # --- off-world bounties (2026-10-19): what spawns on the Moon and on Venus (checked in Ad Astra's biome files) ---
    Q("hn_moon", 0, 0, [kill("ad_astra:corrupted_lunarian", 10), kill("ad_astra:star_crawler", 10)], "Moon Raiders", section="Other Worlds", deps=["w_desh"], xp=200,
      optional=True, tokens=1, loot="hunt", subtitle="Optional: corrupted lunarians and star crawlers", desc=[
        "&eWhat:&r the Moon's wastelands are home to corrupted lunarians and star crawlers. Both attack on sight.",
        "&eChemistry:&r the Moon has no air to carry sound or heat, so a fight there is silent and the sun side of a rock is scorching.",
        "&eHow:&r land on the Moon and roam the lunar wastelands. Keep your suit's oxygen topped up."]),
    Q("hn_venus", 0, 0, [kill("ad_astra:sulfur_creeper", 10), kill("ad_astra:mogler", 5), kill("ad_astra:zombified_pygro", 10)], "Venusian Hunt",
      section="Other Worlds", deps=["w_venus"], xp=250, optional=True, tokens=2, loot="hunt", subtitle="Optional: sulfur creepers, moglers and pygros", desc=[
        "&eWhat:&r Venus's barrens crawl with sulfur creepers, charging moglers and zombified pygros.",
        "&eChemistry:&r real Venus has clouds of sulfuric acid (H₂SO₄) over a 460 °C surface, which is why its creepers come in sulfur.",
        "&eHow:&r land on Venus in a heat-shielded suit and hunt the wastelands. Fight on solid ground away from the lava."]),

    # --- spoils of the hunt: what the drops are made of (optional) ------------------------------
    Q("hn_spoil_flesh", 0, 0, [item(MC + "rotten_flesh", 32)], "Spoils: Rotten Flesh", section="The Undead", deps=["hn_zombie_1"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the least wanted drop, put to use", desc=[
        "&eWhat:&r a stack of rotten flesh. Nobody wants to eat it, but your Dissolver does.",
        "&eChemistry:&r the Dissolver breaks one rotten flesh into 3 protein. Proteins are chains of amino acids joined by peptide bonds (–CO–NH–); rotting is bacteria cutting those chains.",
        "&eHow:&r keep the flesh from your zombie hunts instead of throwing it away.",
        "&eTip:&r dissolve the protein again and it gives ammonia, CO₂, ethylene and sulfur; the sulfur comes from the amino acids cysteine and methionine."]),
    Q("hn_spoil_bone", 0, 0, [item(MC + "bone", 32)], "Spoils: Bones", section="The Undead", deps=["hn_skeleton_1"], xp=50,
      optional=True, tokens=1, subtitle="Optional: calcium phosphate on legs", desc=[
        "&eWhat:&r a stack of bones: bone meal, bone blocks and a mineral the Dissolver can use.",
        "&eChemistry:&r bone is mostly hydroxyapatite, Ca₅(PO₄)₃OH. Half the time the Dissolver gives 3 of it per bone: calcium and phosphorus in one crystal.",
        "&eHow:&r keep the bones from skeletons.",
        "&eTip:&r hydroxyapatite is also what tooth enamel is made of; fluoride toothpaste swaps OH⁻ for F⁻ to make it harder."]),
    Q("hn_spoil_spider", 0, 0, [item(MC + "string", 32), item(MC + "spider_eye", 8)], "Spoils: Silk and Eyes", section="Creepers and Spiders", deps=["hn_spider_1"], xp=75,
      optional=True, tokens=1, subtitle="Optional: string and spider eyes", desc=[
        "&eWhat:&r string for bows, wool and machines, and spider eyes for brewing.",
        "&eChemistry:&r in the Dissolver, string gives keratin and a spider eye gives beta-carotene and chitin. Real spider silk is a different protein, spidroin, and is tougher than steel for its weight.",
        "&eHow:&r keep the drops from your spider hunts. Witches drop spider eyes too.",
        "&eTip:&r beta-carotene is the orange pigment in carrots; your body splits it into vitamin A."]),
    Q("hn_spoil_witch", 0, 0, [item(MC + "glowstone_dust", 8), item(MC + "sugar", 8), item(MC + "glass_bottle", 4)], "Spoils: The Witch's Pantry",
      section="Creatures of the Night", deps=["hn_witch"], xp=75, optional=True, tokens=1, subtitle="Optional: glowstone, sugar and bottles", desc=[
        "&eWhat:&r the ingredients witches carry: glowstone dust, sugar and empty bottles.",
        "&eChemistry:&r the Dissolver breaks glowstone dust into 4 phosphorus and sugar into sucrose, C₁₂H₂₂O₁₁. Glass itself is mostly SiO₂, melted with soda (Na₂CO₃) and lime so it softens at a workable heat.",
        "&eHow:&r keep the drops from witches; swamp huts respawn them.",
        "&eTip:&r sucrose in the Dissolver is one of the easiest early sources of carbon, hydrogen and oxygen."]),
    Q("hn_trident", 0, 0, [item(MC + "trident")], "The Trident", section="The Undead", deps=["hn_undead_kin"], xp=150,
      optional=True, tokens=2, loot="hunt", subtitle="Optional: take it from a drowned", desc=[
        "&eWhat:&r the only trident in the game is the one a drowned carries. It can't be crafted.",
        "&eHow:&r fight drowned in rivers and oceans; only those holding a trident can drop one, and it's rare. Looting helps.",
        "&eTip:&r enchant it with Loyalty to have it fly back, Riptide to launch yourself in rain, or Channeling to call lightning."]),
], links=[("gs_shield", -2, 0), ("t2_nether", 14, 0),
          ("wd_dragon", 0, -3), ("wd_warden", 2, -3), ("wd_catacombs", 4, -3),
          ("tf_courtyard", 0, -5), ("tf_lich_tower", 2, -5), ("tf_labyrinth", 4, -5), ("tf_hydra_lair", 6, -5),
          ("tf_stronghold", 8, -5), ("tf_dark_tower", 10, -5), ("tf_yeti_cave", 12, -5), ("tf_aurora", 14, -5)])
