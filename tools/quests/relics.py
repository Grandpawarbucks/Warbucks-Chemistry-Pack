"""Quest chapter: relics. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

RELICS = ["relics:chorus_staff", "relics:experience_disperser", "relics:ghostly_mantle", "relics:glitchy_mantle", "relics:hunting_belt", "relics:jellyfish_necklace", "relics:kinetic_belt", "relics:leafy_mantle", "relics:midnight_mantle", "relics:pet_bone", "relics:piglin_mask", "relics:reflective_necklace", "relics:rider_flute", "relics:ring_of_the_seven_deadly_sins", "relics:roller_skate", "relics:shield_of_retaliation", "relics:sphere_of_self_sacrifice", "relics:springy_boot", "relics:chef_hat", "relics:clot_of_time", "relics:cut_glass_boot"]
ARTIFACTS = ["artifacts:" + n for n in """anglers_hat antidote_vessel aqua_dashers bunny_hoppers charm_of_shrinking charm_of_sinking chorus_totem cloud_in_a_bottle cowboy_hat cross_necklace crystal_heart digging_claws eternal_steak everlasting_beef feral_claws fire_gauntlet flame_pendant flippers golden_hook helium_flamingo kitty_slippers lucky_scarf night_vision_goggles novelty_drinking_hat obsidian_skull onion_ring panic_necklace pickaxe_heater plastic_drinking_hat pocket_piston power_glove rooted_boots running_shoes scarf_of_invisibility shock_pendant snorkel snowshoes steadfast_spikes strider_shoes superstitious_hat thorn_pendant umbrella universal_attractor vampiric_glove villager_hat warp_drive whoopee_cushion withered_bracelet""".split()]

CHAPTER = Chapter("relics", "Relics and Artifacts", "reliquary:mob_charm_fragment",
        ["Found treasures and crafted curios: Relics, Artifacts and Reliquary."], SIDE, [
    # --- Relics (y=6.5) ------------------------------------------------------------------------
    Q("m_reliquary", 0, 6.5, [item("reliquary:mob_charm_fragment")], "Relics", deps=["gs_iron"], xp=50,
      subtitle="Reliquary, Relics and Artifacts", desc=[
        "&6You remember a treasury. Most of it is scattered now, in chests and in the hands of monsters.&r",
        "&eWhat:&r three mods of found and crafted treasures. Reliquary items are crafted from mob parts; Relics and Artifacts hide in chests and structures.",
        "&eHow:&r mob charm fragments drop from mobs. JEI shows the charm they build.",
        "&eTip:&r a Mob Charm stops that mob type attacking you."]),
    Q("m_alkahest", 2, 6.5, [item("reliquary:alkahestry_tome")], "Alkahestry Tome", deps=["m_reliquary"], xp=75,
      subtitle="The alchemists' dream, in book form", desc=[
        "&eWhat:&r charged with redstone, the tome duplicates common items in a crafting grid.",
        "&eChemistry:&r alchemists searched for alkahest, a universal solvent. None exists (what would you keep it in?), but aqua regia, HCl + HNO₃, dissolves even gold.",
        "&eHow:&r check JEI for the tome and its recipes. Recharge it with redstone."]),
    Q("m_relic_hunt", 1, 8, [tick()], "Relic Hunter", deps=["m_reliquary"], xp=50,
      optional=True, tokens=1, subtitle="Optional: find a relic or an artifact", desc=[
        "&eWhat:&r find any Relics or Artifacts item: a cloud in a bottle, running shoes, a leafy mantle, a mimic's treasure.",
        "&eHow:&r loot chests in dungeons, mineshafts and towers, and beware chests that bite. Click the checkmark when you have one.",
        "&eTip:&r Relics items level up as you use them; check their tooltips."]),
    Q("m_fortune", 3, 8, [item("reliquary:fortune_coin")], "Fortune Coin", deps=["m_alkahest"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a magnet in your pocket", desc=[
        "&eWhat:&r pulls nearby items and XP toward you while active.",
        "&eHow:&r check JEI. Right-click to toggle it.",
        "&eTip:&r turn it off near your sorting system or it'll grab the items."]),

    # --- Relics and Artifacts: found treasure (y=5) --------------------------------------------
    Q("rl_relics", 0, 5, [anyof(RELICS)], "A True Relic", deps=["gs_iron"], xp=75,
      subtitle="Find any item from the Relics mod", desc=[
        "&6You remember owning things no mortal smith made. A few of them seem to have survived.&r",
        "&eWhat:&r Relics are found, never crafted: mantles, belts, necklaces, boots, a chef's hat, a ring of the seven deadly sins. Each has abilities that grow with use.",
        "&eHow:&r loot chests in dungeons, mineshafts, temples, villages and modded structures. Any one relic completes this quest.",
        "&eTip:&r read the tooltip: each relic says what it does and how it gains experience."]),
    Q("rl_relic_level", 2, 5, [tick()], "Relic Growth", deps=["rl_relics"], xp=50, optional=True, tokens=1,
      subtitle="Optional: level up a relic", desc=[
        "&eWhat:&r relics earn experience when you use their abilities, and their levels make those abilities stronger.",
        "&eHow:&r keep the relic equipped and use it. Open its ability screen (the tooltip names the key) to spend levels. Click the checkmark after your first upgrade.",
        "&eTip:&r one well-levelled relic beats a drawer full of new ones."]),
    Q("rl_artifacts", 4, 5, [anyof(ARTIFACTS)], "An Artifact", deps=["gs_iron"], xp=75,
      subtitle="Find any item from the Artifacts mod", desc=[
        "&eWhat:&r Artifacts are simple, always-on curios: Running Shoes, Cloud in a Bottle, Digging Claws, a Lucky Scarf, Night Vision Goggles and many more.",
        "&eHow:&r found in chests underground and in structures, and dropped by Mimics. Any one artifact completes this quest.",
        "&eTip:&r a Cloud in a Bottle (double jump) and Running Shoes make early exploring much easier."]),
    Q("rl_mimic", 6, 5, [kill("artifacts:mimic")], "That Chest Has Teeth", deps=["rl_artifacts"], xp=100, loot="hunt",
      subtitle="Kill a Mimic", optional=True, tokens=1, desc=[
        "&eWhat:&r a Mimic looks exactly like a chest until you open it. It always drops an artifact.",
        "&eHow:&r they hide in mineshafts, dungeons and caves. If a chest stands somewhere odd, hit it before opening it.",
        "&eTip:&r Mimics are tough for their size; fight one with real armor, not a wooden sword."]),
    Q("rl_whoopee", 8, 5, [item("artifacts:whoopee_cushion")], "Divine Comedy", deps=["rl_artifacts"], xp=50,
      secret=True, loot="secret", subtitle="Secret: the least dignified artifact", desc=[
        "&6You remember the other gods laughing at something like this. You never admitted it was you.&r",
        "&eWhat:&r the Whoopee Cushion. Equip it and crouch.",
        "&eTip:&r it does exactly what you think."]),

    # --- Reliquary (y=6.5 / 8) -----------------------------------------------------------------
    Q("rl_heart", 4, 6.5, [item("reliquary:zombie_heart", 2)], "Mob Ingredients", deps=["m_reliquary"], xp=40,
      subtitle="Hearts, ribs, glands and pearls", desc=[
        "&eWhat:&r Reliquary items are built from rare mob parts: zombie hearts, rib bones, catalyzing glands, slime pearls, molten cores and more.",
        "&eHow:&r they drop from their mobs (zombies drop zombie hearts). In this pack they can also be crafted: a zombie heart is rotten flesh in a ring of iron ingots.",
        "&eTip:&r a Looting sword makes the drops much more common than the iron recipe."]),
    Q("rl_belt", 6, 6.5, [item("reliquary:mob_charm_belt")], "Mob Charm Belt", deps=["rl_heart"], xp=75,
      subtitle="Wear all your charms at once", optional=True, tokens=1, desc=[
        "&eWhat:&r the belt holds Mob Charms, so you can be ignored by several mob types at once.",
        "&eHow:&r three leather and five mob charm fragments (check JEI). Each fragment is made from that mob's drops.",
        "&eTip:&r creeper and enderman charms are the most valuable around a base."]),
    Q("rl_void", 5, 8, [item("reliquary:void_tear")], "Void Tear", deps=["rl_heart", "t2_ghast"], xp=75,
      subtitle="A pocket that holds one item type", optional=True, desc=[
        "&eWhat:&r a Void Tear stores a huge stack of one item, and pulls more of it from your inventory.",
        "&eHow:&r a ghast tear, a nebulous heart, a slime pearl and lapis (shapeless).",
        "&eTip:&r it's also an ingredient for the Infernal Tear, Emperor's Chalice and Midas Touchstone."]),
    Q("rl_lantern", 7, 8, [item("reliquary:lantern_of_paranoia")], "Lantern of Paranoia", deps=["rl_heart"], xp=60,
      optional=True, tokens=1, subtitle="Optional: it places torches for you", desc=[
        "&eWhat:&r the lantern places torches from your inventory wherever it's dark enough for mobs to spawn.",
        "&eHow:&r iron ingots, glass, a slime pearl and a molten core (check JEI).",
        "&eTip:&r carry a stack of torches when caving and let it do the lighting."]),
    Q("rl_handgun", 8, 6.5, [item("reliquary:handgun")], "The Handgun", deps=["rl_heart"], xp=100,
      optional=True, tokens=2, subtitle="Optional: Reliquary's magic pistol", desc=[
        "&eWhat:&r a pistol that fires magazines of special bullets: neutral, exorcism, blaze, ender, storm, seeker and more.",
        "&eHow:&r barrel, grip and hammer assemblies plus iron and a slime pearl. Bullets and magazines have their own recipes (check JEI).",
        "&eTip:&r Seeker bullets home in on targets; good against flying mobs."]),
    Q("rl_phoenix", 9, 8, [item("reliquary:phoenix_down")], "Phoenix Down", deps=["rl_heart", "t2_nether"], xp=150,
      optional=True, tokens=2, subtitle="Optional: cheat death several times", desc=[
        "&eWhat:&r saves you from death, heals you, and gives you a few seconds of protection. It has several charges.",
        "&eHow:&r three Angelheart Vials and an Angelic Feather. Vials need milk, glass, fertile essence and an infernal claw (check JEI).",
        "&eTip:&r keep it in your inventory before boss fights and Nether trips."]),

    # --- ATM10-aligned additions (2026-10-19) ----------------------------------------------------
    Q("rl_teeth", 0, 0, [item("relics:golden_tooth", 9)], "Gold Teeth", deps=["rl_relic_level"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the Piglin Mask's loot", desc=[
        "&eWhat:&r with the Piglin Mask's looting ability, kills drop golden teeth: bigger mobs, more teeth. Picking them up can also fire up its frenzy rank.",
        "&eChemistry:&r gold crowns last because gold barely reacts with anything in your mouth: it is the least reactive metal of all.",
        "&eHow:&r find a Piglin Mask, level its looting ability and fight. Three teeth craft into a gold ingot, or trade them to piglins.",
        "&eTip:&r it's mob-drop gold, like a zombified piglin farm: handy, but not ore."]),
], links=[("gs_iron", -2, 5)])
