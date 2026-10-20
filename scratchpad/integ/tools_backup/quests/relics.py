"""Quest chapter: relics. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's "relics" chapter quest for quest (structure and item list only; every word here is ours):
a hub, three "where it drops" hubs (Overworld, Nether, End) and one quest per relic hanging off the hub of the
dimension whose loot tables carry it. Our older Reliquary and Artifacts quests stay as side quests (Artifacts has
its own page now, tools/quests/artifacts.py).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

RELICS = ["relics:chorus_staff", "relics:experience_disperser", "relics:ghostly_mantle", "relics:glitchy_mantle", "relics:hunting_belt", "relics:jellyfish_necklace", "relics:kinetic_belt", "relics:leafy_mantle", "relics:midnight_mantle", "relics:pet_bone", "relics:piglin_mask", "relics:reflective_necklace", "relics:rider_flute", "relics:ring_of_the_seven_deadly_sins", "relics:roller_skate", "relics:shield_of_retaliation", "relics:sphere_of_self_sacrifice", "relics:springy_boot", "relics:chef_hat", "relics:clot_of_time", "relics:cut_glass_boot"]
ARTIFACTS = ["artifacts:" + n for n in """anglers_hat antidote_vessel aqua_dashers bunny_hoppers charm_of_shrinking charm_of_sinking chorus_totem cloud_in_a_bottle cowboy_hat cross_necklace crystal_heart digging_claws eternal_steak everlasting_beef feral_claws fire_gauntlet flame_pendant flippers golden_hook helium_flamingo kitty_slippers lucky_scarf night_vision_goggles novelty_drinking_hat obsidian_skull onion_ring panic_necklace pickaxe_heater plastic_drinking_hat pocket_piston power_glove rooted_boots running_shoes scarf_of_invisibility shock_pendant snorkel snowshoes steadfast_spikes strider_shoes superstitious_hat thorn_pendant umbrella universal_attractor vampiric_glove villager_hat warp_drive whoopee_cushion withered_bracelet""".split()]

OW, NE, EN = "Overworld Finds", "Nether Finds", "End Finds"


def relic(key, id_, title, subtitle, what, how, tip, section, mirror, deps, xp=50):
    """One relic quest: found, never crafted. Every relic levels its abilities with use."""
    return Q(key, 0, 0, [item(id_)], title, deps=deps, xp=xp, subtitle=subtitle, section=section, mirror=mirror, desc=[
        "&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip])


CHAPTER = Chapter("relics", "Relics", "relics:kinetic_belt",
        ["Found treasures that grow with you: Relics, plus the old Reliquary curios."], SIDE, [
    # --- Hub and the three loot hubs (ATM10: hub, Overworld / Nether / End) -----------------------------------
    Q("rl_intro", 0, 0, [tick()], "Things Mortals Didn't Make", deps=[], xp=10, optional=True, tokens=0, mirror="3E99F4CD379DE9D7",
      subtitle="How relics work", icon="relics:kinetic_belt", desc=[
        "&eWhat:&r Relics are curios you find, never craft. Each has abilities that level up as you use them, and a research screen to spend those levels.",
        "&eHow:&r open a relic's tooltip for its abilities and the key that opens its upgrade screen. Click the checkmark when you have read it.",
        "&eTip:&r relics never drop from the sky: they sit in structure chests, split by dimension as the three hubs below show."]),
    Q("rl_relics", 0, 0, [anyof(RELICS)], "A True Relic", deps=["gs_iron"], xp=100, size=2.0, mirror="64141B720662B652",
      subtitle="Find any item from the Relics mod", desc=[
        "&6You remember owning things no mortal smith made. A few of them seem to have survived.&r",
        "&eWhat:&r Relics are found, never crafted: mantles, belts, necklaces, boots, a chef's hat, a ring of the seven deadly sins. Each has abilities that grow with use.",
        "&eHow:&r loot chests in dungeons, mineshafts, temples, villages and modded structures. Any one relic completes this quest.",
        "&eTip:&r read the tooltip: each relic says what it does and how it gains experience."]),
    Q("rl_overworld", 0, 0, [dim("minecraft:overworld")], "Overworld Chests", deps=["rl_relics"], xp=25, section=OW,
      mirror="730130CCF1CF5119", icon="minecraft:grass_block", subtitle="Villages, mineshafts, temples and ruins", desc=[
        "&eWhat:&r the relics below come from Overworld loot: village chests, mineshafts, jungle and desert temples, shipwrecks and the odd ruin.",
        "&eHow:&r you are already here. Loot every chest you pass; relics are rare rolls, so volume matters.",
        "&eTip:&r an Explorer's Compass points to the nearest structure of the kind you pick; JourneyMap marks the ones you've found."]),
    Q("rl_nether", 0, 0, [dim("minecraft:the_nether")], "Nether Chests", deps=["rl_relics"], xp=25, section=NE,
      mirror="2B08B19B35EEBCBA", icon="minecraft:netherrack", subtitle="Bastions, fortresses and ruined portals", desc=[
        "&eWhat:&r bastion remnants, nether fortresses and ruined portals hold the Nether's relics.",
        "&eHow:&r light a Nether portal (Chapter II) and raid a bastion. Its treasure room has the best chests and the angriest piglins.",
        "&eTip:&r gold armour keeps piglins calm until you open a chest; after that they come anyway."]),
    Q("rl_end", 0, 0, [dim("minecraft:the_end")], "End Chests", deps=["rl_relics"], xp=25, section=EN,
      mirror="5D82340E9BED9C79", icon="minecraft:end_stone", subtitle="End cities and End ships", desc=[
        "&eWhat:&r End city towers and the ships moored to them carry the rarest relics.",
        "&eHow:&r beat the dragon, take the gateway, find a city. Shulkers guard every chest; bring blocks for levitation falls.",
        "&eTip:&r the ship's chest sits behind the elytra frame. Take both."]),

    # --- Overworld relics (ATM10 cluster above the hub) ------------------------------------------------------
    relic("rl_roller_skate", "relics:roller_skate", "Roller Skates", "Faster the longer you run",
          "skates that build up movement speed while you keep running, at the cost of grip: the faster you go, the more you slide.",
          "Overworld chests. Equip them in the feet curio slot and keep sprinting.",
          "stop before corners. Levelled skates reach their top speed sooner.", OW, "6B40AF49F505A551", ["rl_overworld"]),
    relic("rl_jellyfish", "relics:jellyfish_necklace", "Jellyfish Necklace", "Stronger wet, and it stings",
          "a necklace that raises your health and regeneration while you are in water or rain, and stores electric arcs that shock whatever you touch.",
          "Overworld chests, often in shipwrecks and ocean ruins.",
          "pair it with Flippers or Aqua Dashers for ocean monuments.", OW, "12449D23295CF9ED", ["rl_overworld"]),
    relic("rl_hunting_belt", "relics:hunting_belt", "Hunting Belt", "More charms, stronger pets",
          "a belt that adds charm slots and makes your tamed animals hit harder while they fight beside you.",
          "Overworld chests. Wear it in the belt curio slot.",
          "a belt full of charms turns a pack of wolves into a real escort.", OW, "3BD73FEAE853D350", ["rl_overworld"]),
    relic("rl_cut_glass_boot", "relics:cut_glass_boot", "Cut-Glass Boot", "A boot that holds liquids",
          "held in hand, this boot works as a bucket that stores several liquids at once; its tooltip shows which one is selected.",
          "Overworld chests.",
          "it fills the gap between buckets and tanks when you're moving lava or water for the chemistry lines.", OW, "7F2D696AC9F4C4E4", ["rl_overworld"]),
    relic("rl_chef_hat", "relics:chef_hat", "Chef's Hat", "Every kill might be dinner",
          "a hat whose kills have a chance to drop a meatball, which eats like raw beef and cooks into something better.",
          "Overworld chests, mostly in villages.",
          "its abilities level with your cooking and eating, so wear it while you farm.", OW, "3E8BA5E075ABD136", ["rl_overworld"]),
    relic("rl_leafy_mantle", "relics:leafy_mantle", "Leafy Mantle", "At home in the canopy",
          "a cloak that lets you move freely through leaves, land on them without damage and heal while you stand in foliage; it can even absorb leaves to save you from a killing blow.",
          "Overworld chests in forests and jungles.",
          "a jungle treetop is the safest bed in the pack while you wear it.", OW, "677A701E06422CF3", ["rl_overworld"]),
    relic("rl_springy_boot", "relics:springy_boot", "Springy Boot", "Crouch, jump, bounce",
          "a boot that launches you backwards off a crouch-jump and keeps bouncing on every landing until you come to a stop.",
          "Overworld chests.",
          "level the Bounce ability before trying anything near lava.", OW, "748A01B5607C475B", ["rl_overworld"]),
    relic("rl_rider_flute", "relics:rider_flute", "Rider's Flute", "A stable in your pocket",
          "a flute that stores a tamed mount and releases it where you stand, so your horse comes with you through portals and across oceans.",
          "Overworld chests. Right-click a tamed mount to store it, right-click again to release it.",
          "the stored animal is safe in the flute; a horse left outside is not.", OW, "21BEE9867796933A", ["rl_overworld"]),

    # --- Nether relics ---------------------------------------------------------------------------------------
    relic("rl_sphere", "relics:sphere_of_self_sacrifice", "Sphere of Self-Sacrifice", "Spend health now, get it back twice",
          "an orb that burns a third of your maximum health on use and restores twice as much over ten seconds; each active restoration also reduces incoming damage, and crouching fires them off as homing blood bolts.",
          "bastion and fortress chests.",
          "it rewards being hit: resisted damage levels the relic.", NE, "54822638CC243004", ["rl_nether"]),
    relic("rl_piglin_mask", "relics:piglin_mask", "Piglin Mask", "One of the herd",
          "a mask that stops piglins attacking you first and turns nearby piglins on anyone who attacks you; its looting ability drops golden teeth.",
          "bastion chests. The piglins guarding them don't see the irony.",
          "the golden teeth are the quest below.", NE, "5EB87CE5F6DEFAAA", ["rl_nether"]),
    relic("rl_reflective", "relics:reflective_necklace", "Reflective Necklace", "Damage, stored and returned",
          "a necklace with a chance to turn damage you take into orbs that hold part of it, and release every orb at the next thing you hit.",
          "fortress chests.",
          "take a few hits on purpose, then swing at a wither skeleton.", NE, "395668FBCB6537AF", ["rl_nether"]),
    relic("rl_seven_sins", "relics:ring_of_the_seven_deadly_sins", "Ring of the Seven Deadly Sins", "A bonus for every vice",
          "a ring whose abilities are named for the sins: Pride adds damage for height above a target, Envy for a target with more health than you, Wrath for a quick follow-up strike, and so on.",
          "bastion chests.",
          "each sin levels on its own, so the ring rewards the way you already fight.", NE, "40AB457E37919ABE", ["rl_nether"]),
    relic("rl_ghostly_mantle", "relics:ghostly_mantle", "Ghostly Mantle", "Leave a mist behind you",
          "a cloak that trails a mist which drains the air of anything standing in it, and takes less damage from targets that keep staring at you.",
          "fortress and bastion chests.",
          "run circles around a brute and let the mist do the work.", NE, "6A715F4AE22D2439", ["rl_nether"]),
    relic("rl_shield_retaliation", "relics:shield_of_retaliation", "Shield of Retaliation", "Parry, then answer",
          "a shield with a short parry window: hold it and damage from in front is blocked, stored, and returned.",
          "bastion chests.",
          "it blocks a blaze volley cleanly if you raise it as the first fireball leaves.", NE, "073D0D41BA5F219B", ["rl_nether"]),
    relic("rl_teeth", "relics:golden_tooth", "Gold Teeth", "The Piglin Mask's loot",
          "with the Piglin Mask's looting ability, kills drop golden teeth: bigger mobs, more teeth. They also feed the mask's rank.",
          "find a Piglin Mask, level its looting ability and fight. Teeth craft into gold ingots, or trade them to piglins.",
          "it's mob-drop gold, like a zombified piglin farm: handy, but not ore.", NE, "4BADD8A0FD85DB33", ["rl_piglin_mask"]),

    # --- End relics -------------------------------------------------------------------------------------------
    relic("rl_chorus_staff", "relics:chorus_staff", "Chorus Staff", "Blink forward",
          "a staff that teleports you a few blocks forward from a small buffer of charges that refills on its own.",
          "End city chests.",
          "it crosses the gaps between End islands that an ender pearl would miss.", EN, "1E2A9446594638E2", ["rl_end"]),
    relic("rl_clot_of_time", "relics:clot_of_time", "Clot of Time", "Rewind your last few seconds",
          "hold it and you slide back along the path you just walked, several seconds into the past, then it needs a rest.",
          "End city and ship chests.",
          "a shulker bullet lifted you off the edge? Rewind.", EN, "60CECAAE2D43EC6E", ["rl_end"]),
    relic("rl_kinetic_belt", "relics:kinetic_belt", "Kinetic Belt", "Glide on momentum",
          "a belt that adds charm slots and, while you hold jump, lowers your gravity and air resistance so your momentum carries you; falls while gliding hurt less.",
          "End city chests.",
          "with Roller Skates for the run-up it is nearly an elytra.", EN, "18DB8C875F2331B2", ["rl_end"]),
    relic("rl_midnight_mantle", "relics:midnight_mantle", "Midnight Mantle", "Stronger by the moon",
          "a cloak that boosts damage near a full moon, health and regeneration near a new moon, and hides you in deep darkness.",
          "End city chests.",
          "check the moon phase before a boss fight; the mantle does.", EN, "7C3F65B5DAC7E57B", ["rl_end"]),
    relic("rl_glitchy_mantle", "relics:glitchy_mantle", "Glitchy Mantle", "Attacks that miss, copies that don't",
          "a cloak that gives attacks against you a chance to miss and leaves glitchy copies of you behind that detonate on contact.",
          "End ship chests.",
          "wear it into the dragon fight: endermen hit the copies instead.", EN, "11A6D020D6F411A8", ["rl_end"]),

    # --- From the hub ----------------------------------------------------------------------------------------
    relic("rl_disperser", "relics:experience_disperser", "Experience Disperser", "Share relic experience around",
          "when any of your relics gains experience, every other equipped relic receives a share of it.",
          "chests in any dimension; it has no favourite.",
          "it makes a full curio bar level together instead of one relic at a time.", "Relics", "75DA0A46E41E6690", ["rl_relics"]),

    # --- Side quests: Reliquary and the old combined page (kept; keys never change) ---------------------------
    Q("m_reliquary", 0, 6.5, [item("reliquary:mob_charm_fragment")], "Reliquary", deps=["gs_iron"], xp=50, section="Reliquary",
      subtitle="Curios built from mob parts", desc=[
        "&6You remember a treasury. Most of it is scattered now, in chests and in the hands of monsters.&r",
        "&eWhat:&r Reliquary items are crafted from mob parts: hearts, glands, pearls and charm fragments.",
        "&eHow:&r mob charm fragments drop from mobs. JEI shows the charm they build.",
        "&eTip:&r a Mob Charm stops that mob type attacking you."]),
    Q("m_alkahest", 2, 6.5, [item("reliquary:alkahestry_tome")], "Alkahestry Tome", deps=["m_reliquary"], xp=75, section="Reliquary",
      subtitle="The alchemists' dream, in book form", desc=[
        "&eWhat:&r charged with redstone, the tome duplicates common items in a crafting grid.",
        "&eChemistry:&r alchemists searched for alkahest, a universal solvent. None exists (what would you keep it in?), but aqua regia, HCl + HNO₃, dissolves even gold.",
        "&eHow:&r check JEI for the tome and its recipes. Recharge it with redstone."]),
    Q("m_relic_hunt", 1, 8, [tick()], "Relic Hunter", deps=["m_reliquary"], xp=50, section="Reliquary",
      optional=True, tokens=1, subtitle="Optional: find a relic or an artifact", desc=[
        "&eWhat:&r find any Relics or Artifacts item: a cloud in a bottle, running shoes, a leafy mantle, a mimic's treasure.",
        "&eHow:&r loot chests in dungeons, mineshafts and towers, and beware chests that bite. Click the checkmark when you have one.",
        "&eTip:&r Relics items level up as you use them; check their tooltips."]),
    Q("m_fortune", 3, 8, [item("reliquary:fortune_coin")], "Fortune Coin", deps=["m_alkahest"], xp=50, section="Reliquary",
      optional=True, tokens=1, subtitle="Optional: a magnet in your pocket", desc=[
        "&eWhat:&r pulls nearby items and XP toward you while active.",
        "&eHow:&r check JEI. Right-click to toggle it.",
        "&eTip:&r turn it off near your sorting system or it'll grab the items."]),
    Q("rl_relic_level", 2, 5, [tick()], "Relic Growth", deps=["rl_relics"], xp=50, optional=True, tokens=1, section="Relics",
      subtitle="Optional: level up a relic", desc=[
        "&eWhat:&r relics earn experience when you use their abilities, and their levels make those abilities stronger.",
        "&eHow:&r keep the relic equipped and use it. Open its ability screen (the tooltip names the key) to spend levels. Click the checkmark after your first upgrade.",
        "&eTip:&r one well-levelled relic beats a drawer full of new ones."]),
    Q("rl_artifacts", 4, 5, [anyof(ARTIFACTS)], "An Artifact", deps=["gs_iron"], xp=75, optional=True, tokens=1, section="Reliquary",
      subtitle="Optional: Artifacts has its own page now", desc=[
        "&eWhat:&r Artifacts are simple, always-on curios: Running Shoes, Cloud in a Bottle, Digging Claws, a Lucky Scarf and many more.",
        "&eHow:&r found in chests underground and in structures, and dropped by Mimics. Any one artifact completes this quest.",
        "&eTip:&r the full list, one quest per artifact, is the Artifacts page under Tools and Gear."]),
    Q("rl_mimic", 6, 5, [kill("artifacts:mimic")], "That Chest Has Teeth", deps=["rl_artifacts"], xp=100, loot="hunt", section="Reliquary",
      subtitle="Kill a Mimic", optional=True, tokens=1, desc=[
        "&eWhat:&r a Mimic looks exactly like a chest until you open it. It always drops an artifact.",
        "&eHow:&r they hide in mineshafts, dungeons and caves. If a chest stands somewhere odd, hit it before opening it.",
        "&eTip:&r Mimics are tough for their size; fight one with real armor, not a wooden sword."]),
    Q("rl_whoopee", 8, 5, [item("artifacts:whoopee_cushion")], "Divine Comedy", deps=["rl_artifacts"], xp=50, section="Reliquary",
      secret=True, loot="secret", subtitle="Secret: the least dignified artifact", desc=[
        "&6You remember the other gods laughing at something like this. You never admitted it was you.&r",
        "&eWhat:&r the Whoopee Cushion. Equip it and crouch.",
        "&eTip:&r it does exactly what you think."]),
    Q("rl_heart", 4, 6.5, [item("reliquary:zombie_heart", 2)], "Mob Ingredients", deps=["m_reliquary"], xp=40, section="Reliquary",
      subtitle="Hearts, ribs, glands and pearls", desc=[
        "&eWhat:&r Reliquary items are built from rare mob parts: zombie hearts, rib bones, catalyzing glands, slime pearls, molten cores and more.",
        "&eHow:&r they drop from their mobs (zombies drop zombie hearts). In this pack they can also be crafted: a zombie heart is rotten flesh in a ring of iron ingots.",
        "&eTip:&r a Looting sword makes the drops much more common than the iron recipe."]),
    Q("rl_belt", 6, 6.5, [item("reliquary:mob_charm_belt")], "Mob Charm Belt", deps=["rl_heart"], xp=75, section="Reliquary",
      subtitle="Wear all your charms at once", optional=True, tokens=1, desc=[
        "&eWhat:&r the belt holds Mob Charms, so you can be ignored by several mob types at once.",
        "&eHow:&r three leather and five mob charm fragments (check JEI). Each fragment is made from that mob's drops.",
        "&eTip:&r creeper and enderman charms are the most valuable around a base."]),
    Q("rl_void", 5, 8, [item("reliquary:void_tear")], "Void Tear", deps=["rl_heart", "t2_ghast"], xp=75, section="Reliquary",
      subtitle="A pocket that holds one item type", optional=True, desc=[
        "&eWhat:&r a Void Tear stores a huge stack of one item, and pulls more of it from your inventory.",
        "&eHow:&r a ghast tear, a nebulous heart, a slime pearl and lapis (shapeless).",
        "&eTip:&r it's also an ingredient for the Infernal Tear, Emperor's Chalice and Midas Touchstone."]),
    Q("rl_lantern", 7, 8, [item("reliquary:lantern_of_paranoia")], "Lantern of Paranoia", deps=["rl_heart"], xp=60, section="Reliquary",
      optional=True, tokens=1, subtitle="Optional: it places torches for you", desc=[
        "&eWhat:&r the lantern places torches from your inventory wherever it's dark enough for mobs to spawn.",
        "&eHow:&r iron ingots, glass, a slime pearl and a molten core (check JEI).",
        "&eTip:&r carry a stack of torches when caving and let it do the lighting."]),
    Q("rl_handgun", 8, 6.5, [item("reliquary:handgun")], "The Handgun", deps=["rl_heart"], xp=100, section="Reliquary",
      optional=True, tokens=2, subtitle="Optional: Reliquary's magic pistol", desc=[
        "&eWhat:&r a pistol that fires magazines of special bullets: neutral, exorcism, blaze, ender, storm, seeker and more.",
        "&eHow:&r barrel, grip and hammer assemblies plus iron and a slime pearl. Bullets and magazines have their own recipes (check JEI).",
        "&eTip:&r Seeker bullets home in on targets; good against flying mobs."]),
    Q("rl_phoenix", 9, 8, [item("reliquary:phoenix_down")], "Phoenix Down", deps=["rl_heart", "t2_nether"], xp=150, section="Reliquary",
      optional=True, tokens=2, subtitle="Optional: cheat death several times", desc=[
        "&eWhat:&r saves you from death, heals you, and gives you a few seconds of protection. It has several charges.",
        "&eHow:&r three Angelheart Vials and an Angelic Feather. Vials need milk, glass, fertile essence and an infernal claw (check JEI).",
        "&eTip:&r keep it in your inventory before boss fights and Nether trips."]),
], links=[("gs_iron", -2, 5)], mirror="relics")
