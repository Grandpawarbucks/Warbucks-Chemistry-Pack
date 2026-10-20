"""Quest chapter: worlds (The End). See tools/quests/STYLE.md.
Build: python3 tools/build_quests.py

The Twilight Forest moved to twilight.py and Ad Astra to space.py and the Undergarden quests (w_undergarden, w_regalium, wd_catacombs,
w_forgotten, wd_vestige, wd_undergarden_biomes) to undergarden.py, the Deep Dark / Otherside quests (w_ancient, wd_warden, w_otherside,
w_echo, wd_temple, wd_otherside_biomes, w_soul_elytra, w_warden_armor) to deeperdarker.py; the YUNG's / Towns and Towers structure quests
(w_dungeon, w_mineshaft) moved to explore.py (w_town was later merged into ex_village). Keys are unchanged. New quests use the wd_ prefix.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("worlds", "Other Worlds", "minecraft:ender_eye",
        ["The End: the dragon, its cities and its ships."], SIDE, [
    # --- The End (y=0, extras y=-2) ------------------------------------------------------------
    Q("w_end", 0, 0, [dim("minecraft:the_end")], "The End", deps=["t2_nether"], xp=200,
      subtitle="Eyes of ender, a stronghold, a portal", desc=[
        "&6You remember the edge of the world. It's closer than it used to be.&r",
        "&eWhat:&r the End holds the dragon, End Cities, shulkers and azure silver ore. End Crystals power Just Dire Things' flight upgrade.",
        "&eHow:&r throw eyes of ender to find a stronghold, fill the portal frame and jump in.",
        "&eTip:&r bring blocks, a bow and slow-falling potions. YUNG's Better Strongholds make the hunt more interesting."]),
    Q("wd_dragon", 2, 0, [kill("minecraft:ender_dragon")], "Slay the Dragon", deps=["w_end"], xp=300,
      loot="boss", subtitle="The End's guardian falls", desc=[
        "&eWhat:&r the Ender Dragon guards the End's central island. Beating it opens the gateways to the outer islands.",
        "&eHow:&r shoot or climb to the End Crystals on the obsidian pillars and destroy them first (the caged ones need a climb), then fight the dragon when it perches on the portal.",
        "&eTip:&r stay out of its purple breath and never look an enderman in the eye mid-fight. A bow and a stack of arrows do most of the work."]),
    Q("w_dragon", 2, -2, [item("minecraft:dragon_breath", 4)], "The Dragon's Breath", deps=["wd_dragon"], xp=200,
      subtitle="Bottle what the dragon breathes", desc=[
        "&eWhat:&r the dragon's purple breath can be bottled and makes lingering potions.",
        "&eChemistry:&r the Dissolver splits one bottle into 8 xenon and 8 radon, two heavy noble gases. It gives no oganesson in this pack: element 118 has never been found in nature, so here it only comes from the Fusion Chamber.",
        "&eHow:&r catch the purple breath cloud in glass bottles during the fight, or respawn the dragon for another go.",
        "&eTip:&r crystals respawn the dragon when placed on the exit portal, if you need it again."]),
    Q("wd_end_city", 4, 0, [structure("minecraft:end_city")], "An End City", deps=["wd_dragon"], xp=150,
      subtitle="Purple towers on the outer islands", desc=[
        "&eWhat:&r End Cities are tall purpur towers on the outer islands, guarded by shulkers. Some have an End Ship moored alongside.",
        "&eHow:&r throw an ender pearl into an End Gateway near the main island, then search the outer islands. The Explorer's Compass can find one.",
        "&eTip:&r shulker bullets make you float; carry milk or slow falling."]),
    Q("w_elytra", 6, 0, [item("minecraft:elytra"), item("minecraft:shulker_shell", 4)], "End City Loot", deps=["w_dragon", "wd_end_city"], xp=250,
      subtitle="Wings and shulker shells", desc=[
        "&eWhat:&r End Cities hold elytra (on the end ships) and shulkers whose shells make shulker boxes.",
        "&eHow:&r take an End Gateway from the main island, then search the outer islands for purple towers.",
        "&eTip:&r the Angel Ring needs an elytra; shulker shells feed Silent Gear's tyrian steel."]),
    Q("wd_fireworks", 6, -2, [item("minecraft:firework_rocket", 32)], "Rocket Boost", deps=["w_elytra"], xp=100,
      optional=True, tokens=1, subtitle="Optional: chemistry that pushes", desc=[
        "&eWhat:&r firework rockets boost elytra flight. Thirty-two is a good start for a long trip.",
        "&eChemistry:&r gunpowder is black powder: about 75% potassium nitrate (KNO₃, the oxidiser), 15% charcoal and 10% sulfur. The nitrate supplies its own oxygen, so it burns fast even in a sealed tube.",
        "&eHow:&r paper + gunpowder (1–3 for longer flight) in the crafting grid. Creepers and the hunting page give gunpowder.",
        "&eTip:&r rockets with a firework star explode and hurt you; use plain ones for flying."]),
    Q("wd_dragon_egg", 0, -2, [item("minecraft:dragon_egg")], "The Egg", deps=["wd_dragon"], xp=100,
      secret=True, loot="secret", subtitle="Secret: the only one in the world", desc=[
        "&6One egg, one dragon, one world. You remember having a whole shelf of these.&r",
        "&eWhat:&r the dragon leaves a single egg on top of the exit portal the first time it dies.",
        "&eTip:&r it teleports when you hit it. Push it off with a piston, or let it fall onto a torch to pick it up."]),
], links=[("t2_nether", -2, 0)])
