"""Quest chapter: space (Ad Astra + Ad Astra: Giselle Addon). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Moved here from worlds.py (keys unchanged; t7.py depends on w_mars and w_venus): w_desh, w_mars, w_ostrum, w_suit, w_venus,
w_space_metals, w_glacio, w_cheese, w_oxygen, w_mercury. New quests use the sp_ prefix.
Layout: planets on y=0, oxygen and gear above (y=-2/-4), places and biomes below (y=2/4).
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, MAIN, SIDE  # noqa: F401

AA = "ad_astra:"
GA = "ad_astra_giselle_addon:"

CHAPTER = Chapter("space", "Space", "ad_astra:tier_2_rocket",
        ["The Moon, the planets and the air you bring with you."], SIDE, [
    # --- the planets (y=0) ---------------------------------------------------------------------
    Q("w_desh", 0, 0, [item("ad_astra:raw_desh", 8)], "Desh on the Moon", deps=["t7_rocket"], xp=300,
      subtitle="The Moon's metal builds the next rocket", desc=[
        "&6You remember the Moon from above. Now you're standing on it.&r",
        "&eWhat:&r desh ore is found only on the Moon. Desh blocks, engines and tanks build the Tier 2 rocket.",
        "&eChemistry:&r the Moon has no atmosphere and its days swing from about +120 °C to −170 °C, so bring oxygen.",
        "&eHow:&r mine desh ore on the Moon with an iron pickaxe or better (this pack sets its tier) and process it like any ore."]),
    Q("w_mars", 2, 0, [dim("ad_astra:mars"), item("ad_astra:tier_2_rocket")], "Mars", deps=["w_desh"], xp=500,
      subtitle="The red planet", desc=[
        "&eWhat:&r Mars holds ostrum ore, the metal for the Tier 3 rocket.",
        "&eChemistry:&r Mars is red because its dust is rich in iron(III) oxide, Fe₂O₃: rust. Its thin air is about 95% CO₂.",
        "&eHow:&r build the Tier 2 rocket from desh at the NASA Workbench, fuel it with diesel and launch."]),
    Q("w_ostrum", 4, 0, [item("ad_astra:raw_ostrum", 8)], "Ostrum", deps=["w_mars"], xp=300,
      subtitle="Mars's metal for the Tier 3 rocket", desc=[
        "&eWhat:&r ostrum ore is found only on Mars. It builds the Tier 3 rocket.",
        "&eHow:&r mine ostrum ore on Mars and process it. It needs a diamond pickaxe or better (this pack sets its tier).",
        "&eTip:&r grab some extra for the Tier 3 rocket's engine and tank."]),
    Q("w_suit", 6, 0, [item("ad_astra:netherite_space_suit")], "Heat Shielding", deps=["w_ostrum"], xp=300,
      subtitle="A suit that survives 464 °C", desc=[
        "&eWhat:&r Venus and Mercury are hot enough to kill in a normal space suit. The netherite space suit handles the heat.",
        "&eHow:&r check JEI for the netherite suit pieces. Fill it with oxygen at the Oxygen Loader.",
        "&eTip:&r the jet suit (later, check JEI) also handles the heat, and flies."]),
    Q("w_venus", 8, 0, [dim("ad_astra:venus"), item("ad_astra:tier_3_rocket")], "Venus", deps=["w_suit"], xp=600,
      subtitle="Acid clouds and crushing pressure", desc=[
        "&eWhat:&r Venus holds calorite ore, the metal for the Tier 4 rocket.",
        "&eChemistry:&r its atmosphere is about 96% CO₂ at roughly 92 times Earth's pressure, under clouds of sulfuric acid (H₂SO₄). A runaway greenhouse keeps it near 464 °C.",
        "&eHow:&r Tier 3 rocket from ostrum, plus your netherite space suit."]),
    Q("sp_calorite", 10, 0, [item(AA + "raw_calorite", 8)], "Calorite", deps=["w_venus"], xp=250,
      subtitle="Venus's metal for the Tier 4 rocket", desc=[
        "&eWhat:&r calorite ore is found on Venus. It builds the Tier 4 rocket, the only one that reaches another star.",
        "&eHow:&r mine calorite ore in the Venusian stone and process it like any ore. Only a netherite pickaxe (or better) can mine it in this pack.",
        "&eTip:&r Venus is hot and its rain is acid; keep the netherite suit on the whole time."]),
    Q("w_space_metals", 12, 0, [item("ad_astra:desh_ingot", 8), item("ad_astra:ostrum_ingot", 4), item("ad_astra:calorite_ingot", 4)], "Alien Metals", deps=["sp_calorite"], xp=600,
      subtitle="Desh, ostrum and calorite", desc=[
        "&eWhat:&r one metal from each world: desh (Moon), ostrum (Mars) and calorite (Venus). Each builds the next rocket tier.",
        "&eHow:&r process the raw ores; MI and Mekanism ore lines work on them too (check JEI).",
        "&eTip:&r the Dissolver can tell you what these metals break down into."]),
    Q("w_glacio", 14, 0, [dim("ad_astra:glacio"), item("ad_astra:tier_4_rocket")], "Glacio", deps=["w_space_metals"], xp=800,
      size=1.75, shape="hexagon", subtitle="A frozen world around another star", desc=[
        "&6You remember stars that were yours to name. This one you'll have to visit first.&r",
        "&eWhat:&r Glacio orbits Proxima Centauri, the nearest star to the Sun, about 4.2 light-years away. Unlike the others, it has breathable air.",
        "&eHow:&r build the Tier 4 rocket from calorite and launch."]),

    # --- air and gear (y=-2, y=-4) -------------------------------------------------------------
    Q("sp_gas_tank", -2, -4, [item(AA + "gas_tank")], "A Spare Breath", deps=["t7_suit"], xp=100,
      subtitle="Carry oxygen to top up your suit", desc=[
        "&eWhat:&r a gas tank holds oxygen you can carry, to refill the suit far from your Oxygen Loader.",
        "&eChemistry:&r a resting adult breathes in roughly 550 litres of O₂ a day; your suit's tank is all that stands between you and vacuum.",
        "&eHow:&r iron plates and an iron rod (check JEI). Fill it in the Oxygen Loader like the suit.",
        "&eTip:&r the large gas tank holds much more and is a part in later machines."]),
    Q("sp_oxygen_can", 0, -4, [item(GA + "oxygen_can")], "The Oxygen Can", deps=["sp_gas_tank"], xp=100,
      subtitle="Giselle Addon: oxygen for everything you wear", desc=[
        "&eWhat:&r the Giselle Addon's oxygen can stores oxygen and tops up the oxygen gear you're carrying.",
        "&eHow:&r iron plates around an iron rod (check JEI). Fill it with oxygen like a tank.",
        "&eTip:&r the addon also links Ad Astra to Mekanism and other mods; search its name in JEI to see what else it adds."]),
    Q("w_oxygen", 2, -2, [item("ad_astra:oxygen_distributor")], "Breathable Bases", deps=["w_mars"], xp=150,
      optional=True, tokens=1, subtitle="Optional: fill a sealed room with air", desc=[
        "&eWhat:&r the Oxygen Distributor fills a sealed room with breathable air, so you can work without a helmet.",
        "&eChemistry:&r it makes oxygen from water with FE, the same idea as your Electrolytic Separator: 2H₂O → 2H₂ + O₂.",
        "&eHow:&r check JEI. Seal the room completely; any gap stops it working."]),
    Q("sp_sensor", 2, -4, [item(AA + "oxygen_sensor")], "Is There Air?", deps=["w_oxygen"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a redstone check for oxygen", desc=[
        "&eWhat:&r the Oxygen Sensor gives a redstone signal depending on whether the space around it has oxygen.",
        "&eHow:&r check JEI for the recipe, place it inside your sealed base and wire it to a lamp or alarm.",
        "&eTip:&r a light that goes out when the air does is the cheapest life support alarm there is."]),
    Q("sp_water_pump", -2, -6, [item(AA + "water_pump")], "Water for Oxygen", deps=["sp_gas_tank", "t4_separator"], xp=120,
      optional=True, tokens=1, subtitle="Optional: feed your electrolysis off-world", desc=[
        "&eWhat:&r Ad Astra's powered water pump feeds water into your pipes, so a base on the Moon can make its own oxygen.",
        "&eChemistry:&r electrolysis splits water: 2H₂O → 2H₂ + O₂. Every 2 molecules of water give 1 of oxygen and 2 of hydrogen, which you can burn or store.",
        "&eHow:&r steel and desh plates, a gas tank and a hopper (check JEI). Pipe its water into a Mekanism Electrolytic Separator and the O₂ into an Oxygen Loader.",
        "&eTip:&r Ad Astra's ice shards are frozen water; the Moon and Mars both have ice shard ore."]),
    Q("sp_netherite_can", 4, -2, [item(GA + "netherite_oxygen_can")], "Netherite Oxygen Can", deps=["sp_oxygen_can", "w_ostrum"], xp=150,
      optional=True, tokens=1, subtitle="Optional: a bigger can for the hot worlds", desc=[
        "&eWhat:&r the upgraded oxygen can holds much more oxygen than the iron one.",
        "&eHow:&r an oxygen can, a netherite ingot and ostrum plates in the crafting grid (check JEI). Its oxygen carries over.",
        "&eTip:&r on Venus every trip back to base costs time; carry more air instead."]),
    Q("sp_launch_site", -3.5, -2, [item(GA + "fuel_loader"), item(GA + "rocket_sensor")], "An Automated Launch Site", deps=["t7_rocket"], xp=120,
      optional=True, tokens=1, subtitle="Optional: Giselle Addon fuelling and sensing", desc=[
        "&eWhat:&r the Fuel Loader takes piped fuel and fills any rocket or rover within a few blocks; the Rocket Sensor reports a nearby rocket's state to a comparator.",
        "&eHow:&r both are steel ingots and iron plates around a bucket or an observer (check JEI). Pipe diesel into the loader.",
        "&eTip:&r no more filling rockets by hand from buckets."]),
    Q("sp_gravity", 0, -2, [item(AA + "gravity_normalizer")], "Earth Gravity", deps=["w_desh"], xp=150,
      optional=True, tokens=1, subtitle="Optional: normal gravity indoors", desc=[
        "&eWhat:&r the Gravity Normalizer gives an area Earth-like gravity, so your jumps behave in your Moon base.",
        "&eChemistry:&r the Moon's gravity is about 1/6 of Earth's, Mars about 3/8; you weigh less because they have less mass.",
        "&eHow:&r etrionic capacitors, a diamond block and desh plates (check JEI)."]),
    Q("sp_rover", -1.5, -2, [item(AA + "tier_1_rover")], "The Rover", deps=["w_desh"], xp=150,
      optional=True, tokens=1, subtitle="Optional: drive across the Moon", desc=[
        "&eWhat:&r a fuelled buggy for crossing big, airless plains quickly.",
        "&eHow:&r desh engine, desh blocks and plates, a large gas tank, a radio and wheels (check JEI). Fuel it with diesel.",
        "&eTip:&r low gravity makes it bounce; slow down on hills."]),

    # --- places and biomes (y=2, y=4) ----------------------------------------------------------
    Q("w_cheese", 0, 2, [item("ad_astra:cheese", 4)], "The Moon Is Cheese", deps=["w_desh"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the old joke is true here", desc=[
        "&eWhat:&r Ad Astra hides cheese ore on the Moon.",
        "&eChemistry:&r the real Moon is mostly silicate rock: oxygen, silicon, magnesium, iron, calcium and aluminum.",
        "&eHow:&r mine moon cheese ore. Eat responsibly."]),
    Q("sp_lunarians", -2, 2, [structure(AA + "lunarian_village")], "Lunarians", deps=["t7_rocket"], xp=100,
      optional=True, tokens=1, subtitle="Optional: villagers on the Moon", desc=[
        "&eWhat:&r Lunarians are the Moon's villagers. Their villages stand on the lunar wastelands, with towers nearby.",
        "&eHow:&r explore the Moon until you find one, then walk into it. They trade like villagers.",
        "&eTip:&r the Explorer's Compass works on other planets too."]),
    Q("sp_moon_dungeon", -2, 4, [structure(AA + "moon_dungeon")], "Moon Dungeon", deps=["t7_rocket"], xp=100,
      optional=True, tokens=1, subtitle="Optional: something built under the Moon", desc=[
        "&eWhat:&r a dungeon hidden under the lunar wastelands, with loot and hostile guards.",
        "&eHow:&r the Explorer's Compass can find one. Step inside.",
        "&eTip:&r bring a spare gas tank: dungeons take longer than you think."]),
    Q("sp_mars_temple", 3.5, 2, [structure(AA + "mars_temple"), biome(AA + "martian_canyon_creek")], "Temples of Mars", deps=["w_mars"], xp=150,
      optional=True, tokens=1, subtitle="Optional: ruins in the red canyons", desc=[
        "&eWhat:&r temples stand in the Martian wastelands and canyon creeks.",
        "&eChemistry:&r Mars's canyons were carved by liquid water long ago; today its low pressure makes surface water boil or freeze almost at once.",
        "&eHow:&r visit a canyon creek and find a temple (the Explorer's Compass helps)."]),
    Q("sp_mars_poles", 3.5, 4, [biome(AA + "martian_polar_caps"), item(AA + "ice_shard", 8)], "The Polar Caps", deps=["sp_mars_temple"], xp=120,
      optional=True, tokens=1, subtitle="Optional: ice at the ends of Mars", desc=[
        "&eWhat:&r Mars's polar caps are frozen; ice shard ore gives ice shards.",
        "&eChemistry:&r the real caps are water ice with a seasonal layer of dry ice (solid CO₂), which turns straight to gas in spring (sublimation).",
        "&eHow:&r visit the polar caps biome and mine ice shard ore (it's on the Moon too)."]),
    Q("sp_pygro", 8, 2, [structure(AA + "pygro_village")], "The Pygros", deps=["w_venus"], xp=150,
      optional=True, tokens=1, subtitle="Optional: Venus has inhabitants", desc=[
        "&eWhat:&r Pygros are piglin-like natives of Venus. Their villages and towers stand in the Venus wastelands.",
        "&eHow:&r find a village (the Explorer's Compass helps) and step inside. Wear gold, just in case.",
        "&eTip:&r Pygro brutes guard the towers; they hit hard."]),
    Q("sp_venus_barrens", 10, 2, [biome(AA + "infernal_venus_barrens")], "Infernal Barrens", deps=["w_venus"], xp=100,
      optional=True, tokens=1, subtitle="Optional: Venus at its worst", desc=[
        "&eWhat:&r the harshest of the Venusian biomes.",
        "&eChemistry:&r Venus is hotter than Mercury despite being twice as far from the Sun: its thick CO₂ atmosphere traps heat.",
        "&eHow:&r visit it in the netherite space suit. Fire resistance helps."]),
    Q("w_mercury", 12, 2, [dim("ad_astra:mercury")], "Mercury", deps=["w_venus"], xp=200,
      optional=True, tokens=1, subtitle="Optional: the planet closest to the Sun", desc=[
        "&eWhat:&r a scorched, airless world reachable with the Tier 3 rocket.",
        "&eChemistry:&r with almost no atmosphere, Mercury can't hold heat: about 430 °C by day and −180 °C at night.",
        "&eHow:&r Tier 3 rocket plus the netherite space suit."]),
    Q("sp_mercury_deltas", 12, 4, [biome(AA + "mercury_deltas")], "Mercury Deltas", deps=["w_mercury"], xp=80,
      optional=True, tokens=1, subtitle="Optional: walk the deltas", desc=[
        "&eWhat:&r Mercury's deltas, a dark landscape of scorched stone.",
        "&eChemistry:&r despite the name, the planet has no mercury metal; the element was named after the same god for its quick, flowing liquid.",
        "&eHow:&r land on Mercury and walk into the deltas."]),
    Q("sp_glacio", 14, 2, [biome(AA + "glacio_ice_peaks"), biome(AA + "glacio_snowy_barrens")], "Peaks of Glacio", deps=["w_glacio"], xp=200,
      optional=True, tokens=2, subtitle="Optional: walk another star's world", desc=[
        "&6Air you didn't bring, under a sun that isn't yours. You remember this feeling: arriving.&r",
        "&eWhat:&r Glacio's frozen peaks and snowy barrens, with its own trees and woolly rams.",
        "&eHow:&r visit both biomes. You can take your helmet off here.",
        "&eTip:&r Glacio has ordinary ores too (coal, iron, copper, lapis) in its own stone."]),
    Q("sp_orbits", 2, 2, [dim(AA + "moon_orbit"), dim(AA + "mars_orbit")], "In Orbit", deps=["w_mars"], xp=150,
      optional=True, tokens=1, subtitle="Optional: stop above the Moon and Mars", desc=[
        "&eWhat:&r every planet has an orbit dimension above it, where space stations are built.",
        "&eChemistry:&r in orbit you're falling around the planet all the time, which is why everything floats.",
        "&eHow:&r choose the orbit on the rocket's planet screen instead of the surface."]),
], links=[("t7_rocket", -2, 0), ("t4_separator", 0, -6)])
