"""Quest chapter: worlds (The End, the Deep Dark / Otherside, the Undergarden). See tools/quests/STYLE.md.
Build: python3 tools/build_quests.py

The Twilight Forest moved to twilight.py and Ad Astra to space.py; the YUNG's / Towns and Towers structure quests
(w_dungeon, w_mineshaft, w_town) moved to explore.py. Keys are unchanged. New quests use the wd_ prefix.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("worlds", "Other Worlds", "deeperdarker:heart_of_the_deep",
        ["The End, the Otherside and the Undergarden."], SIDE, [
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

    # --- The Deep Dark and the Otherside (y=3.5, extras y=5.5) -------------------------------------
    Q("w_ancient", 0, 3.5, [tick()], "An Ancient City", deps=["t2_nether"], xp=100,
      subtitle="Find the city beneath the deep dark", desc=[
        "&eWhat:&r Ancient Cities sit deep below the Overworld in the deep dark. Each one's centre holds the frame of a portal to the Otherside.",
        "&eHow:&r the Explorer's Compass can find one. Sneak everywhere: shriekers summon the Warden. Click the checkmark once you're inside.",
        "&eTip:&r sneaking never triggers sculk sensors, and walking on wool doesn't either."]),
    Q("wd_warden", 2, 3.5, [kill("minecraft:warden")], "The Warden", deps=["w_ancient"], xp=300,
      loot="boss", subtitle="Kill the blind guardian of the deep", desc=[
        "&eWhat:&r the Warden is the strongest regular mob in the game, and the key to the Otherside: with Deeper and Darker it drops the Heart of the Deep.",
        "&eHow:&r trigger shriekers three times to summon one (or let it find you). Fight from range; it's blind and tracks you by sound and smell.",
        "&eTip:&r its sonic boom goes through shields and armour. Break line of sight when it starts charging."]),
    Q("w_otherside", 4, 3.5, [item("deeperdarker:heart_of_the_deep"), dim("deeperdarker:otherside")], "The Otherside", deps=["wd_warden"], xp=300,
      subtitle="Take the Warden's heart and step through", desc=[
        "&6You remember a silence older than the world. You can hear it again.&r",
        "&eWhat:&r beyond the Ancient City lies the Otherside, a dark dimension of sculk and echo trees.",
        "&eHow:&r defeat a Warden for its Heart of the Deep, then use it to light the portal frame in the city's centre.",
        "&eTip:&r the Warden is blind but hears everything. Fight from range and keep moving."]),
    Q("w_echo", 6, 3.5, [item("deeperdarker:reinforced_echo_shard", 4)], "Echoes of the Deep", deps=["w_otherside"], xp=200,
      subtitle="The Otherside's strongest material", desc=[
        "&eWhat:&r reinforced echo shards make Warden gear that rivals netherite.",
        "&eHow:&r check JEI for the recipe; echo shards come from Ancient City chests and Otherside loot.",
        "&eTip:&r Warden armour is a netherite smithing upgrade, so keep your netherite gear."]),
    Q("wd_temple", 4, 5.5, [structure("deeperdarker:ancient_temple")], "The Ancient Temple", deps=["w_otherside"], xp=200,
      subtitle="A temple deep in the Otherside", desc=[
        "&eWhat:&r the Otherside's great structure: a sculk-choked temple with traps and the best loot in the dimension.",
        "&eHow:&r the Explorer's Compass points the way. Step inside.",
        "&eTip:&r the temple is full of sculk; sneak, as you did in the Ancient City."]),
    Q("wd_otherside_biomes", 6, 5.5, [biome("deeperdarker:echoing_forest"), biome("deeperdarker:overcast_columns"), biome("deeperdarker:blooming_caverns")],
      "Biomes of the Otherside", deps=["w_otherside"], xp=150, optional=True, tokens=1, subtitle="Optional: forests, columns and caverns", desc=[
        "&eWhat:&r the Otherside has its own biomes: echo-tree forests, towering columns and caverns lit by blooming plants.",
        "&eChemistry:&r there's no sunlight down here; real cave and deep-sea ecosystems run on chemosynthesis, where microbes get energy by oxidising H₂S or CH₄ instead of from light.",
        "&eHow:&r Nature's Compass works in the Otherside. Visit all three."]),
    Q("w_soul_elytra", 8, 1.5, [item("deeperdarker:soul_elytra")], "Soul Elytra", deps=["w_otherside", "w_elytra"], xp=150,
      optional=True, tokens=1, subtitle="Optional: an elytra with its own boost", desc=[
        "&eWhat:&r an upgraded elytra that boosts itself, no rockets needed.",
        "&eHow:&r an elytra, sculk bones (from Shattered), a soul crystal (from Stalkers) and soul dust (check JEI).",
        "&eTip:&r Stalkers and Shattered roam the Otherside; fight them at range."]),
    Q("w_warden_armor", 8, 3.5, [item("deeperdarker:warden_chestplate")], "Warden Armour", deps=["w_echo"], xp=200,
      optional=True, tokens=2, subtitle="Optional: beyond netherite", desc=[
        "&eWhat:&r Warden armour is tougher than netherite.",
        "&eHow:&r netherite chestplate + reinforced echo shard + Warden upgrade template in a smithing table.",
        "&eTip:&r check JEI for where the Warden upgrade template comes from."]),

    # --- The Undergarden (y=8, extras y=10) ----------------------------------------------------
    Q("w_undergarden", 0, 8, [item("undergarden:cloggrum_ingot", 8), item("undergarden:froststeel_ingot", 4), item("undergarden:utherium_crystal", 4)], "Undergarden Metals",
      deps=["t4_undergarden"], xp=200, subtitle="Cloggrum, froststeel and utherium", desc=[
        "&eWhat:&r new ores beneath the world: cloggrum (tough), froststeel (slows what it hits) and utherium (hurts rotspawn).",
        "&eHow:&r mine them in depthrock and shiverstone, then smelt.",
        "&eTip:&r run them through the Alchemistry Dissolver: what are these strange metals made of?"]),
    Q("w_regalium", 2, 8, [item("undergarden:regalium_crystal", 4)], "Regalium", deps=["w_undergarden"], xp=150,
      subtitle="The Undergarden's precious crystal", desc=[
        "&eWhat:&r regalium is the Undergarden's treasure: a rare crystal in depthrock and shiverstone.",
        "&eHow:&r smelt regalium ore. It also turns up in catacomb chests.",
        "&eTip:&r catacombs are also where the Forgotten Guardian waits."]),
    Q("wd_catacombs", 4, 8, [structure("undergarden:catacombs"), kill("undergarden:forgotten_guardian")], "The Catacombs", deps=["w_regalium"], xp=250,
      loot="boss", subtitle="Find the catacombs and beat their guardian", desc=[
        "&eWhat:&r the catacombs are a buried tomb of the Undergarden's old builders. The Forgotten Guardian, a hulking armoured giant, still stands watch.",
        "&eHow:&r the Explorer's Compass can find one. Clear the halls, then fight the guardian.",
        "&eTip:&r it's slow; hit it, step back out of its swing, and repeat."]),
    Q("w_forgotten", 6, 8, [item("undergarden:forgotten_ingot")], "The Forgotten Ingot", deps=["wd_catacombs"], xp=300,
      size=1.5, subtitle="Forge the guardian's metal", desc=[
        "&6You remember the old guardians and the oaths they swore. This one has forgotten its own.&r",
        "&eWhat:&r the Forgotten Guardian drops forgotten nuggets; nine make a Forgotten Ingot for the strongest Undergarden tools.",
        "&eHow:&r find a catacomb, beat the guardian, and craft the nuggets into an ingot. The smithing template is in catacomb chests.",
        "&eTip:&r it hits hard; armour up and keep your distance between swings."]),
    Q("wd_vestige", 2, 10, [structure("undergarden:forgotten_vestige"), structure("undergarden:denizen_camp")], "Ruins and Camps", deps=["w_undergarden"], xp=120,
      optional=True, tokens=1, subtitle="Optional: who else lives down here?", desc=[
        "&eWhat:&r forgotten vestiges are ruins left by the Undergarden's builders; denizen camps belong to the hostile Denizens who live there now.",
        "&eHow:&r explore until you find one of each (the Explorer's Compass helps) and step inside.",
        "&eTip:&r Denizens fight in groups; draw them out one at a time."]),
    Q("wd_undergarden_biomes", 4, 10, [biome("undergarden:forgotten_field"), biome("undergarden:frostfields"), biome("undergarden:smog_spires")],
      "Biomes Below", deps=["w_undergarden"], xp=120, optional=True, tokens=1, subtitle="Optional: three corners of the Undergarden", desc=[
        "&eWhat:&r the Undergarden's biomes range from frozen fields to spires that belch smog.",
        "&eChemistry:&r a smog is a mix of smoke and fog; real industrial smog is soot plus sulfur dioxide (SO₂), which forms sulfuric acid droplets in damp air.",
        "&eHow:&r Nature's Compass works here too. Visit all three."]),
], links=[("t2_nether", -2, 0), ("t4_undergarden", -2, 8)])
