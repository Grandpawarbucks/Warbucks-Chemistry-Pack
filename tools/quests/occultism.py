"""Quest chapter: occultism. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's "occultism" chapter quest for quest (its quest list, order, clusters and requirements only; every word
here is ours). ATM10's pentacle quests ask for a ritual's ingredients; ours do the same, and where we already had a
quest for the spirit itself (the unbound afrit and marid fights) that quest stays and follows the ingredient quest.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

# Recipes and pentacle chalk colours checked against occultism 1.224.5 (data/occultism/recipe and modonomicon
# multiblocks). Almost Unified merges common dusts and ingots into MI's, so tasks use tags (anytag) for those.
# Pack gates: phase4_occultism.js removes miner recipes for uranium, uraninite, osmium, fluorite, platinum, iridium,
# tungsten; pack/config/occultism-server.toml caps every crusher spirit at 2 dust per ore (higher tiers are only faster).

MINER_BAN = "uranium, uraninite, osmium, fluorite, platinum, iridium or tungsten"
O = "occultism:"
IMPURE = [O + "chalk_%s_impure" % c for c in ("white", "light_gray", "gray", "black", "brown", "red", "orange", "yellow",
                                              "lime", "green", "cyan", "light_blue", "blue", "purple", "magenta", "pink")]
STABILIZERS = [O + "storage_stabilizer_tier%d%s" % (t, d) for d in ("", "_dark") for t in range(6)]

SIGHT, BASICS, FOLIOT, STORAGE, DJINNI, AFRIT, MARID, COLOURS, MINERS = (
    "The Third Eye", "Ritual Basics", "Foliot Work", "Otherworld Storage", "Djinn Pentacles", "Afrit Pentacles",
    "Marid Pentacles", "Every Colour", "Spirit Miners")

CHAPTER = Chapter("occultism", "Occultism", "occultism:datura",
        ["Spirits, pentacles, otherworld storage and miners that dig where you can't."], SIDE, [
    Q("oc_intro", 0, 0, [tick(), tick()], "Before You Summon", deps=[], xp=10, optional=True, tokens=0,
      mirror="6CCDEEDA2C99DA66", icon="occultism:dictionary_of_spirits", subtitle="How this page works", desc=[
        "&eWhat:&r Occultism is ritual magic: chalk circles, bowls of ingredients and spirits bound by name. Each spirit rank (foliot, djinni, afrit, marid) opens the next.",
        "&eHow:&r the Dictionary of Spirits explains every ritual and shows each pentacle in 3D. Tick both boxes once you have it.",
        "&eTip:&r pack gates: miners can't dig the chemistry-milestone ores, and every crusher spirit gives 2 dust per ore."]),

    # --- The Third Eye ---------------------------------------------------------------------------------------
    Q("oc_seeds", 0, 0, [item("occultism:datura_seeds")], "Demon's Dream Seeds", deps=["gs_iron"], xp=40, size=2.0, shape="gear",
      section=SIGHT, mirror="5316DF321B45D2CA", subtitle="A plant that shows you the other side", desc=[
        "&6You remember seeing everything at once. A strange seed in the grass promises some of it back.&r",
        "&eWhat:&r Demon's Dream is the plant every Occultism path starts from: its fruit opens the Third Eye, its seeds make the Dictionary.",
        "&eHow:&r break grass until a Demon's Dream seed drops. Plant it on farmland.",
        "&eTip:&r replant the first seeds; you'll want a small field."]),
    Q("oc_dictionary", 0, 0, [item("occultism:dictionary_of_spirits")], "Dictionary of Spirits", deps=["oc_seeds"], xp=30,
      mirror="6C1BBA559963B3DF", subtitle="The book that knows every name", desc=[
        "&eWhat:&r the Dictionary of Spirits is Occultism's guide: rituals, pentacles in 3D, spirits and their jobs.",
        "&eHow:&r a book and a Demon's Dream seed, shapeless.",
        "&eTip:&r its pentacle pages can project the circle into the world for you to trace."]),
    Q("m_datura", 0, 0, [item("occultism:datura", 4)], "Demon's Dream", deps=["oc_seeds"], xp=40, mirror="47358ADC1470C82A",
      subtitle="Eat it and see the Otherworld", desc=[
        "&eWhat:&r eating Demon's Dream Fruit gives the Third Eye: you see Otherworld blocks hidden behind normal ones.",
        "&eHow:&r grow the seeds and harvest the fruit. Eat one when you want to look.",
        "&eTip:&r with the Third Eye active, otherworld trees appear among normal oaks."]),
    Q("oc_flint", 0, 0, [item("minecraft:flint_and_steel")], "Strike a Spark", deps=["m_datura", "oc_dictionary"], xp=20,
      mirror="3D41D0092D94636B", subtitle="Light the fruit", desc=[
        "&eWhat:&r spiritfire is lit from Demon's Dream Fruit, and flint and steel is the match.",
        "&eChemistry:&r flint and steel sparks are tiny shavings of iron that oxidise so fast in air they glow: 4Fe + 3O₂ → 2Fe₂O₃.",
        "&eHow:&r an iron ingot and a flint.",
        "&eTip:&r the same lighter starts the unbound afrit ritual much later."]),
    Q("oc_spiritfire", 2, 0, [item("occultism:otherstone", 16), item("occultism:otherworld_sapling_natural"), item("occultism:spirit_attuned_gem")],
      "Spiritfire", deps=["oc_flint"], xp=60, mirror="4C873491F6F0FFAF", subtitle="A fire that changes things instead of burning them", desc=[
        "&eWhat:&r spiritfire doesn't hurt you and doesn't destroy items: things thrown into it come out converted.",
        "&eChemistry:&r andesite, the input for otherstone, is a grey volcanic rock made mostly of plagioclase feldspar.",
        "&eHow:&r throw a Demon's Dream Fruit on the ground and light it. Then throw in andesite (otherstone), an oak sapling (otherworld sapling) and a diamond (spirit-attuned gem).",
        "&eTip:&r books, feathers and black dye also go in: they come out as taboo books, awakened feathers and purified ink."]),
    Q("oc_divination", 2, -3, [item("occultism:divination_rod")], "Divination Rod", deps=["oc_spiritfire"], xp=40,
      optional=True, tokens=1, mirror="78ECC28DD4BA9696", subtitle="Optional: dowse for the Otherworld", desc=[
        "&eWhat:&r the rod points toward otherworld blocks such as otherstone and otherworld trees.",
        "&eHow:&r gold ingots, glass and a spirit-attuned gem. Use it as the Dictionary explains to pick a target.",
        "&eTip:&r handy for finding an otherworld grove before you have saplings."]),
    Q("oc_attuned_gem", 2, -1.5, [item("occultism:spirit_attuned_gem", 4)], "Spirit-Attuned Gems", deps=["oc_spiritfire"], xp=50,
      subtitle="Diamonds that spirits can hold", desc=[
        "&eWhat:&r spirit-attuned gems are in almost every spirit tool: magic lamps, lenses, the infused pickaxe, stabilizers and crystals.",
        "&eChemistry:&r a diamond is pure carbon in a rigid tetrahedral lattice, which is why it survives spiritfire unchanged in substance.",
        "&eHow:&r throw diamonds into spiritfire. Four gems make a Spirit-Attuned Crystal, which the mineshaft and bigger pentacles need.",
        "&eTip:&r keep a few diamonds aside for this from the start."]),
    Q("oc_silver", 0, 1.5, [anytag("c:ingots/silver", 8)], "Silver", deps=["m_datura"], xp=40,
      subtitle="The summoner's metal", desc=[
        "&eWhat:&r silver goes into magic lamps, lens frames, satchels, the infused pickaxe and storage remotes.",
        "&eChemistry:&r silver (Ag) is the best electrical conductor of all metals. It tarnishes black when traces of H₂S turn its surface into Ag₂S.",
        "&eHow:&r mine and smelt silver ore; any silver ingot counts (they're unified).",
        "&eTip:&r MI's ore processing gives silver as a byproduct too."]),
    Q("oc_otherwood", 4, -1.5, [item("occultism:otherworld_log", 8), item("occultism:otherworld_ashes", 3)], "Otherworld Trees",
      deps=["oc_spiritfire"], xp=50, subtitle="Wood from beyond, burned to ash", desc=[
        "&eWhat:&r otherworld trees look like oaks unless you have the Third Eye. Their logs burn in spiritfire to otherworld ashes, half of white chalk.",
        "&eChemistry:&r real wood ash is mostly calcium and potassium carbonates. Potash (K₂CO₃ leached from 'pot ash') gave potassium its name.",
        "&eHow:&r grow the otherworld sapling from spiritfire and cut it while under the Third Eye. Burn logs for ashes.",
        "&eTip:&r a foliot sapling trader later sells stable saplings that don't need the Third Eye."]),
    Q("oc_burnt", 4, 1.5, [item("occultism:burnt_otherstone", 3)], "Burnt Otherstone", deps=["oc_spiritfire"], xp=30,
      subtitle="The other half of chalk", desc=[
        "&eWhat:&r burnt otherstone counts as otherstone dust, the base of every chalk.",
        "&eHow:&r cut or craft otherstone into polished otherstone, then smelt it in a furnace.",
        "&eTip:&r make a stack; every new chalk colour starts from white impure chalk."]),

    # --- Ritual basics ---------------------------------------------------------------------------------------
    Q("oc_rituals_basics", 0, 0, [tick()], "How a Ritual Works", deps=["oc_spiritfire"], xp=20, section=BASICS,
      mirror="5ACE97EE75813006", icon="occultism:golden_sacrificial_bowl", subtitle="Circle, bowls, book, sacrifice", desc=[
        "&eWhat:&r a ritual needs a chalk pentacle, a Golden Sacrificial Bowl in the middle, ingredients in plain bowls around it, and an activation item (usually a bound book).",
        "&eHow:&r put the ingredients in the bowls, then right-click the golden bowl with the activation item. Some rituals also want a sacrifice killed nearby, or an item used. Tick the box when you've read this.",
        "&eTip:&r the Dictionary's ritual pages list all of that per ritual, and JEI shows every ritual recipe."]),
    Q("oc_familiars", 0, 0, [tick()], "Familiars", deps=["oc_rituals_basics"], xp=20, optional=True, tokens=1,
      mirror="7F59941D62E672B0", icon="occultism:familiar_ring", subtitle="Optional: spirits that follow you around", desc=[
        "&eWhat:&r familiars are small spirits that stay with you and help: the greedy familiar picks up items, the bat gives night vision, the blacksmith repairs.",
        "&eHow:&r each has its own summoning ritual (the Dictionary lists them). Tick the box when you've read this.",
        "&eTip:&r a Familiar Ring, later, lets you wear one."]),
    Q("oc_candles", 6, 1.5, [item("occultism:butcher_knife")], "The Butcher Knife", deps=["oc_rituals_basics"], xp=40,
      mirror="4DF0D7B85065ADC9", subtitle="Tallow for candles", desc=[
        "&eWhat:&r animals killed with the Butcher Knife drop tallow, the wax of Occultism's large candles.",
        "&eChemistry:&r tallow is rendered animal fat: triglycerides of stearic, palmitic and oleic acid, the stuff of the first candles.",
        "&eHow:&r iron and sticks. Kill pigs, cows or sheep with it.",
        "&eTip:&r a small animal pen pays for a lot of candles."]),
    Q("oc_crystal", 0, 0, [anytag("minecraft:candles", 4), item("occultism:spirit_attuned_crystal")], "Candles and a Crystal",
      deps=["oc_candles", "oc_attuned_gem"], xp=50, mirror="6581D4AF1A6DE230", subtitle="Steady the circle, anchor the call", desc=[
        "&eWhat:&r candles in a pentacle steady it, so summoned spirits last longer. The Spirit-Attuned Crystal anchors bigger pentacles and goes into the mineshaft and miners.",
        "&eChemistry:&r a real crystal is a lattice that repeats in three dimensions; four small gems pressed together would only be a polycrystal.",
        "&eHow:&r a large candle is string over tallow (any candle counts here). The crystal is four spirit-attuned gems in a 2×2 grid.",
        "&eTip:&r the Dictionary's pentacle pages show where candles and crystals go."]),
    Q("oc_brush", 0, 0, [item("occultism:chalk_white_impure"), item("occultism:chalk_white"), item("occultism:brush")], "White Chalk and a Brush",
      deps=["oc_rituals_basics", "oc_otherwood", "oc_burnt"], xp=50, mirror="1B5177A774FCEF64", subtitle="Draw the circle, clean it up", desc=[
        "&eWhat:&r white chalk draws the basic pentacle glyphs. The brush wipes glyphs away again much faster than breaking them.",
        "&eChemistry:&r real chalk is calcium carbonate, CaCO₃, which fizzes away in acid: CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂.",
        "&eHow:&r burnt otherstone and otherworld ashes make impure white chalk; purify it in spiritfire. Brush: three planks over two wool and a string.",
        "&eTip:&r chalk wears out with use, so make a few."]),
    Q("m_chalk", 6, 0, [item("occultism:golden_sacrificial_bowl"), item("occultism:sacrificial_bowl", 4)], "Sacrificial Bowls",
      deps=["oc_rituals_basics"], xp=60, mirror="7F09F8F98C13F11B", subtitle="One golden bowl, several plain ones", desc=[
        "&eWhat:&r the Golden Sacrificial Bowl is the centre of every ritual; plain Sacrificial Bowls hold the ingredients.",
        "&eHow:&r bowls are otherstone; the golden one adds gold. Dark versions (from otherrock) work the same.",
        "&eTip:&r ingredient bowls can stand anywhere within 8 blocks of the golden bowl."]),
    Q("oc_book_foliot", 0, 0, [item("occultism:purified_ink"), item("occultism:book_of_binding_foliot")], "A Book of Binding",
      deps=["oc_rituals_basics"], xp=40, mirror="0B3EA604C5172D98", subtitle="Ink, feather and a taboo book", desc=[
        "&eWhat:&r a Book of Binding waits for a spirit's name. Bound, it becomes the key that starts that spirit's rituals.",
        "&eHow:&r spiritfire turns black dye into purified ink, a book into a taboo book and a feather into an awakened feather. Add blue dye for the foliot book.",
        "&eTip:&r the colour of dye picks the spirit rank: blue foliot, purple djinni, yellow afrit, green marid."]),
    Q("m_foliot", 8, 0, [item("occultism:book_of_binding_bound_foliot"), item("minecraft:iron_ingot"), anytag("c:ingots/silver"),
                          item("minecraft:gold_ingot"), item("minecraft:copper_ingot")], "Bind a Foliot",
      deps=["oc_crystal", "oc_book_foliot", "m_chalk", "oc_brush"], xp=100, size=2.0, shape="gear", mirror="4F35D04721DFC9FF",
      subtitle="Learn a spirit's true name", desc=[
        "&6You remember names that made things kneel. The smallest of them comes back first.&r",
        "&eWhat:&r a bound Book of Binding holds a spirit's name and starts its rituals. Foliots are the weakest spirits, and their first job is crushing ore.",
        "&eHow:&r bind the foliot book with a name as the Dictionary describes (check JEI). The four ingots are the Foliot Crusher's ritual ingredients.",
        "&eTip:&r Aviar's Circle, the foliot summoning pentacle, uses only white chalk."]),
    Q("oc_ars_jar", 0, 0, [item("ars_nouveau:ritual_containment"), item("ars_nouveau:ritual_brazier"), item("ars_nouveau:mob_jar")],
      "Spirits in a Jar", deps=["m_foliot", "m_brazier"], xp=60, optional=True, tokens=1, mirror="06B9D8973E9C6A2C",
      subtitle="Optional: Ars Nouveau can bottle a worker", desc=[
        "&eWhat:&r Ars Nouveau's Containment Jar holds a living creature, and many keep working inside it. Summoned spirits can be stored the same way.",
        "&eHow:&r place jars near a Ritual Brazier and run the Ritual of Containment; it pulls a nearby creature (within 3 blocks) into a jar.",
        "&eTip:&r a jar is a tidy way to move a worker spirit to a new base."]),
    Q("oc_pentacles", 0, 0, [tick()], "Reading a Pentacle", deps=["m_foliot"], xp=20, mirror="0F412542271B6254",
      icon="occultism:chalk_white", subtitle="Each colour does a job", desc=[
        "&eWhat:&r a pentacle's colours say what it does: white is the base, gold possesses, purple infuses, lime calls djinn, red binds afrits, blue binds marids.",
        "&eHow:&r every new colour is impure white chalk plus a special ingredient, purified in spiritfire. Tick the box when you've read this.",
        "&eTip:&r the Dictionary's Pentacles section is a table: each tier upgrades the pentacle you drew before."]),

    # --- Foliot work -----------------------------------------------------------------------------------------
    Q("oc_crusher", 10, 0, [anytag("c:dusts/gold", 4), anytag("c:dusts/obsidian", 2)], "Foliot Crusher", deps=["m_foliot"], xp=60,
      section=FOLIOT, subtitle="A spirit that grinds ore to dust", desc=[
        "&eWhat:&r a crusher spirit picks up ores and gems and drops dusts. New chalks need gold, silver, iron, emerald, calcite and obsidian dust.",
        "&eHow:&r Summon Foliot Crusher: iron, gold, copper and silver ingots in the bowls, a white-chalk circle. Feed it items; any gold and obsidian dust counts for this quest.",
        "&eTip:&r a foliot gives 2 dusts per ore, the pack's normal cap. Bigger crushers are only faster; use the MI and Mekanism ore lines for real ore yield."]),
    Q("oc_gold_chalk", 10, -1.5, [item("occultism:chalk_gold")], "Golden Chalk", deps=["oc_crusher"], xp=50,
      subtitle="The chalk of possession", desc=[
        "&eWhat:&r golden (yellow) chalk turns a summoning into a possession: the spirit takes over a creature's body.",
        "&eHow:&r impure white chalk with glowstone dust and 2 gold dust, purified in spiritfire.",
        "&eTip:&r Hedyrin's Lure (white + gold) is the foliot possession pentacle."]),
    Q("oc_endermite", 12, -1.5, [kill("occultism:possessed_endermite")], "Possessed Endermite", deps=["oc_gold_chalk"], xp=50,
      subtitle="End stone without the End", desc=[
        "&eWhat:&r a possessed endermite has a high chance to drop end stone, which purple chalk needs.",
        "&eHow:&r foliot possession ritual with 2 dirt and 2 stone (the Dictionary shows the extra step). Kill what appears.",
        "&eTip:&r run it a few times; crushed end stone goes into every purple chalk."]),
    Q("oc_skulls", 12, -3, [item("minecraft:skeleton_skull", 4)], "Possessed Skeleton", deps=["oc_gold_chalk"], xp=50,
      subtitle="Skulls for bigger pentacles", desc=[
        "&eWhat:&r skeleton skulls raise a pentacle's calling power. Every djinni, afrit and marid pentacle places them.",
        "&eHow:&r foliot possession ritual with 4 bones and a chicken as the sacrifice. The possessed skeleton drops skulls.",
        "&eTip:&r check each pentacle in the Dictionary for how many skulls it wants."]),
    Q("oc_chalks", 0, 0, [item("occultism:chalk_yellow_impure"), item("occultism:chalk_purple_impure"), item("occultism:chalk_light_gray_impure")],
      "Three New Colours", deps=["oc_pentacles", "oc_endermite"], xp=75, size=1.5, shape="hexagon", mirror="1DE0F289821F55D1",
      subtitle="Yellow, purple and light gray", desc=[
        "&eWhat:&r the first coloured chalks: yellow (possession), purple (infusion) and light gray (a stronger foundation).",
        "&eChemistry:&r calcite, in light gray chalk, is CaCO₃, exactly the compound real chalk and limestone are made of.",
        "&eHow:&r impure white chalk plus: glowstone and 2 gold dust (yellow); crushed end stone and 2 obsidian dust (purple); silver dust, iron dust and crushed calcite (light gray).",
        "&eTip:&r your foliot crusher makes every one of those dusts."]),
    Q("oc_purple_chalk", 12, 0, [item("occultism:chalk_purple")], "Purple Chalk", deps=["oc_endermite"], xp=60,
      subtitle="The chalk of infusion", desc=[
        "&eWhat:&r purple chalk binds spirits into objects. Every crafting ritual (satchels, storage, miners) needs it.",
        "&eChemistry:&r obsidian is volcanic glass, about 70% SiO₂ that cooled too fast to crystallise.",
        "&eHow:&r impure white chalk with crushed end stone and 2 obsidian dust, purified in spiritfire.",
        "&eTip:&r Eziveus' Spectral Compulsion (white + purple) is the foliot crafting pentacle."]),
    Q("oc_lightgray_chalk", 14, 1.5, [item("occultism:chalk_light_gray")], "Light Gray Chalk", deps=["oc_crusher", "oc_silver"], xp=50,
      subtitle="Real chalk, finally", desc=[
        "&eWhat:&r light gray chalk strengthens a pentacle's foundation; djinni pentacles need it.",
        "&eChemistry:&r calcite is CaCO₃, exactly the compound real chalk and limestone are made of.",
        "&eHow:&r impure white chalk with silver dust, iron dust and crushed calcite, purified in spiritfire.",
        "&eTip:&r calcite lines amethyst geodes, so collect it while you farm source gems."]),
    Q("oc_jobs_foliot", 8, 1.5, [anyof(["occultism:book_of_calling_foliot_lumberjack", "occultism:book_of_calling_foliot_farmer",
                                        "occultism:book_of_calling_foliot_cleaner", "occultism:book_of_calling_foliot_transport_items"])],
      "Foliot Workers", deps=["m_foliot"], xp=50, optional=True, tokens=1, subtitle="Optional: a spirit with a job", desc=[
        "&eWhat:&r summoned foliots can work: Lumberjack cuts trees, Farmer tends crops, Janitor picks up items, Transporter moves items between chests.",
        "&eHow:&r each is a foliot summoning ritual (Lumberjack: an otherworld sapling, 3 saplings and an axe). The Book of Calling it gives lets you set its work area.",
        "&eTip:&r a Transporter feeding a Crusher and a Janitor collecting the dust is a whole processing line."]),
    Q("oc_satchel", 12, 1.5, [item("occultism:satchel")], "Surprisingly Large Bag", deps=["oc_purple_chalk"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a foliot lives in your backpack", desc=[
        "&eWhat:&r a satchel with a bound foliot inside that keeps it bigger on the inside.",
        "&eHow:&r a foliot crafting ritual: a chest, two leather, string and a silver ingot around the golden bowl, on a white and purple pentacle.",
        "&eTip:&r the djinni version, the Ender Satchel, opens your ender chest."]),

    # --- The foliot crafting pentacle and the djinni -----------------------------------------------------------
    Q("oc_eziveus", 0, 0, [item("minecraft:experience_bottle", 2), anytag("c:dusts/emerald")], "The Crafting Circle",
      deps=["oc_chalks", "oc_purple_chalk"], xp=75, size=1.5, shape="hexagon", section=DJINNI, mirror="39647A2473F6F7D7",
      subtitle="Eziveus' Spectral Compulsion", desc=[
        "&eWhat:&r the foliot crafting pentacle (white and purple) binds a foliot into an object. Its first useful product is research fragment dust.",
        "&eChemistry:&r emerald is beryl, Be₃Al₂Si₆O₁₈, coloured green by traces of chromium.",
        "&eHow:&r draw the pentacle from the Dictionary. These are the dust's ingredients: 2 bottles o' enchanting and emerald dust (crush an emerald).",
        "&eTip:&r bottles o' enchanting come from villager clerics, or from a Tome of Peritia's stored XP."]),
    Q("oc_research", 14, -1.5, [item("occultism:research_fragment_dust"), item("occultism:chalk_lime_impure")], "Research Fragment Dust",
      deps=["oc_eziveus"], xp=50, mirror="30C5B597610F4AFB", subtitle="Experience pressed into emerald", desc=[
        "&eWhat:&r research fragment dust is the special ingredient of lime chalk and knowledge tablets.",
        "&eHow:&r the foliot crafting ritual with emerald dust and 2 bottles o' enchanting. Then impure white chalk with the dust, emerald dust and a slime ball makes impure lime chalk.",
        "&eTip:&r lime is the colour that calls djinn; make extra."]),
    Q("oc_lime_chalk", 16, -1.5, [item("occultism:chalk_lime")], "Lime Chalk", deps=["oc_research"], xp=60,
      subtitle="The chalk that calls djinn", desc=[
        "&eWhat:&r lime chalk attracts spirits stronger than foliots. Every djinni pentacle and up uses it.",
        "&eHow:&r purify impure lime chalk in spiritfire.",
        "&eTip:&r make several; afrit and marid pentacles still use lime."]),
    Q("oc_goggles", 12, 3, [item("occultism:otherworld_goggles")], "Otherworld Goggles", deps=["oc_eziveus"], xp=60,
      mirror="2A5004EB99AE4F96", subtitle="The Third Eye without the fruit", desc=[
        "&eWhat:&r the goggles give a permanent Third Eye, and show even more hidden blocks than Demon's Dream does, iesnium ore among them.",
        "&eHow:&r lenses (glass panes and an attuned gem) become infused lenses in a foliot ritual with 2 silver and gold; add a lens frame (otherstone and silver) and leather.",
        "&eTip:&r goggles let you see, not harvest: you still need the infused or iesnium pickaxe."]),
    Q("oc_djinni", 16, 0, [item("occultism:book_of_binding_bound_djinni")], "Bind a Djinni", deps=["oc_lime_chalk", "oc_lightgray_chalk", "oc_skulls"],
      xp=100, size=1.5, subtitle="A stronger spirit for bigger rituals", desc=[
        "&6You remember spirits who bowed when you passed. This one only negotiates.&r",
        "&eWhat:&r djinn are the second rank of spirits. Their rituals make storage, soul gems, the infused pickaxe and better miners.",
        "&eHow:&r a Book of Binding with purple dye, bound with a name like the foliot one. Djinni pentacles add light gray and lime chalk and skeleton skulls.",
        "&eTip:&r the Dictionary's Pentacles section is a table: each tier upgrades the pentacle you drew before."]),
    Q("oc_strigeor", 0, 0, [item("minecraft:phantom_membrane"), item("minecraft:gunpowder"), item("minecraft:gray_dye"), item("minecraft:clay_ball")],
      "The Djinni's Workshop", deps=["oc_research", "oc_djinni"], xp=100, size=1.5, shape="hexagon", mirror="0D18BBB04693885A",
      subtitle="Strigeor's Higher Binding", desc=[
        "&eWhat:&r the djinni crafting pentacle makes most of Occultism's mid-game: the infused pickaxe, soul gems, storage, gray paste.",
        "&eChemistry:&r gunpowder is KNO₃, sulfur and charcoal; clay is mostly kaolinite, Al₂Si₂O₅(OH)₄. Together with a phantom membrane and gray dye they make gray paste.",
        "&eHow:&r draw the pentacle from the Dictionary, then run the gray paste ritual with these four ingredients and your djinni book.",
        "&eTip:&r this one pentacle covers more recipes than any other; build it somewhere permanent."]),
    Q("oc_gray_chalk", 18, -4.5, [item("occultism:gray_paste"), item("occultism:chalk_gray")], "Gray Chalk", deps=["oc_strigeor"], xp=50,
      mirror="6FEED25FFAC4101F", subtitle="A stronger foundation", desc=[
        "&eWhat:&r gray chalk is the foundation colour of afrit pentacles.",
        "&eHow:&r impure white chalk with gray paste, purified in spiritfire.",
        "&eTip:&r gray, light gray and black chalk can stand in for white in most pentacles."]),
    Q("oc_ritual_satchel", 0, 0, [item("occultism:ritual_satchel_t1")], "Apprentice Ritual Satchel", deps=["oc_strigeor"], xp=60,
      optional=True, tokens=1, mirror="5AE80FF518B1BBA6", subtitle="Optional: a foliot draws your pentacles", desc=[
        "&eWhat:&r fill the satchel with chalks, candles, skulls and crystals; preview a pentacle in the Dictionary and the foliot places the pieces for you.",
        "&eHow:&r a foliot crafting ritual: a hopper, a dispenser, 2 wool, 2 leather, string and a silver ingot.",
        "&eTip:&r chalks are used up by durability, so keep spares inside."]),
    Q("oc_chalk_repair", 0, 0, [tick()], "Mending Chalk", deps=["oc_strigeor"], xp=20, optional=True, tokens=1,
      mirror="61999669BDE127F9", icon="occultism:chalk_white", subtitle="Optional: a djinni refills your chalk", desc=[
        "&eWhat:&r worn-out chalk can be fully repaired by infusing it with a djinni instead of crafting a new one.",
        "&eHow:&r on the djinni crafting pentacle: 3 otherworld essence and a spirit-attuned gem, started with the chalk itself. Otherworld essence is Demon's Dream essence burned in spiritfire. Tick the box when you've read this.",
        "&eTip:&r it's worth it for the expensive colours: red, blue and anything rainbow."]),
    Q("oc_soulgem", 16, 3, [item("occultism:soul_gem")], "Soul Gem", deps=["oc_strigeor"], xp=75,
      optional=True, tokens=1, mirror="666EA8B8F13EB292", subtitle="Optional: carry a mob around", desc=[
        "&eWhat:&r a Soul Gem traps a living creature so you can move it and release it elsewhere.",
        "&eHow:&r a djinni ritual: a diamond, copper, silver and gold ingots, a fragile soul gem and 3 soul sand or soil.",
        "&eTip:&r it's the easy way to move villagers or animals to your base."]),
    Q("oc_ring", 16, 4.5, [item("occultism:familiar_ring")], "Familiar Ring", deps=["oc_soulgem"], xp=100,
      optional=True, tokens=1, subtitle="Optional: wear your familiar", desc=[
        "&eWhat:&r familiars are summoned with rituals (greedy, bat, beaver, deer, blacksmith...). The ring stores one so it travels with you.",
        "&eHow:&r a djinni ritual with a soul gem, two gold and two silver ingots. Capture your familiar with it.",
        "&eTip:&r the Greedy Familiar picks up items for you. The Dictionary lists what each familiar does."]),
    Q("oc_manage_machine", 18, 1.5, [item("occultism:book_of_calling_djinni_manage_machine")], "Machine Operator", deps=["oc_djinni"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a djinni that runs a machine", desc=[
        "&eWhat:&r the djinni Machine Operator keeps a linked machine fed from your Storage Actuator and returns the results.",
        "&eHow:&r djinni summoning ritual with a coal block, gold, iron and a furnace. Use its Book of Calling on the storage and the machine.",
        "&eTip:&r it's a light autocrafting option before AE2."]),
    Q("oc_ophyx", 0, 0, [anytag("c:dusts/iron"), anytag("c:dusts/silver"), anytag("c:dusts/gold"), anytag("c:dusts/copper")],
      "A Djinni Crusher", deps=["oc_research", "oc_djinni"], xp=75, optional=True, tokens=1, size=1.5, shape="hexagon",
      mirror="5FE507DAEE770507", subtitle="Optional: Ophyx' Calling, and ice dust", desc=[
        "&eWhat:&r the djinni summoning pentacle calls a djinni crusher. It's faster than a foliot, and it can crush ice, which a foliot can't.",
        "&eHow:&r the djinni crusher ritual takes one each of iron, silver, gold and copper dust. Feed it ice, packed ice and blue ice for light blue chalk.",
        "&eTip:&r like every crusher here, it gives 2 dust per ore; it's only faster."]),

    # --- Otherworld storage ------------------------------------------------------------------------------------
    Q("oc_matrix", 18, 3, [item("occultism:dimensional_matrix")], "Dimensional Matrix", deps=["oc_djinni"], xp=75,
      section=STORAGE, subtitle="The heart of Occultism storage", desc=[
        "&eWhat:&r the Dimensional Matrix binds a djinni to hold items in a pocket dimension.",
        "&eChemistry:&r the quartz it needs is SiO₂, the same crystal that keeps time in a real watch by vibrating at a fixed frequency.",
        "&eHow:&r a djinni crafting ritual with three quartz blocks and an ender pearl."]),
    Q("oc_storage", 20, 3, [item("occultism:dimensional_matrix"), anyof([O + "storage_controller_base", O + "storage_controller_base_dark"]),
                            anyof([O + "storage_controller", O + "storage_controller_dark"])], "Storage Actuator",
      deps=["oc_matrix", "oc_chalks"], xp=150, size=1.5, mirror="6CC5FE34778F0DFA", subtitle="A whole warehouse in one block", desc=[
        "&eWhat:&r the Dimensional Storage Actuator stores thousands of items and shows them in one searchable screen.",
        "&eHow:&r a foliot ritual makes the Storage Actuator Base (otherstone pedestal, 2 copper, gold). Put the matrix on top of the base in a crafting grid.",
        "&eTip:&r it's an alternative to AE2 for early storage. Stabilizers expand it."]),
    Q("oc_stabilizer", 22, 3, [anyof(STABILIZERS)], "Storage Stabilizers", deps=["oc_storage"], xp=150, size=2.0, shape="gear",
      mirror="42F50CE7FE715583", subtitle="More room for the warehouse", desc=[
        "&6You remember a treasury with no walls. This one at least has room to grow.&r",
        "&eWhat:&r stabilizers pointed at the Actuator raise how many items and item types it holds. Any tier completes this quest.",
        "&eHow:&r tier 0 is an otherstone pedestal; tier 1 is a foliot ritual: the tier 0 stabilizer, a copper block, blaze dust and a spirit-attuned gem.",
        "&eTip:&r place them within a few blocks, facing the Actuator."]),
    Q("oc_stabilizer_t2", 24, 3, [item("occultism:storage_stabilizer_tier2")], "Djinni Stabilizer", deps=["oc_stabilizer"], xp=75,
      subtitle="Tier 2 storage", desc=[
        "&eWhat:&r the tier 2 stabilizer holds a djinni and adds much more room than tier 1.",
        "&eHow:&r djinni crafting ritual: a tier 1 stabilizer, a silver block, a ghast tear and 2 spirit-attuned gems.",
        "&eTip:&r upgrade your tier 1 stabilizers one at a time; they keep working in between."]),
    Q("oc_stabilizer_high", 26, 3, [anyof(["occultism:storage_stabilizer_tier3", "occultism:storage_stabilizer_tier4"])], "Greater Stabilizers",
      deps=["oc_stabilizer_t2"], xp=150, optional=True, tokens=2, subtitle="Optional: afrit and marid storage", desc=[
        "&eWhat:&r tier 3 binds an afrit, tier 4 a marid; each is a big jump in capacity.",
        "&eHow:&r tier 3: tier 2 stabilizer, a gold block, a Totem of Undying, a crystal and afrit essence. Tier 4 adds an iesnium block, a beacon and marid essence.",
        "&eTip:&r a few high-tier stabilizers beat many low ones."]),
    Q("oc_wormhole", 22, 4.5, [anyof([O + "stable_wormhole", O + "stable_wormhole_dark"]), item("occultism:storage_remote")], "Wormhole and Remote",
      deps=["oc_storage"], xp=75, optional=True, tokens=1, mirror="5831B3192C0E8C56", subtitle="Optional: more doors into storage", desc=[
        "&eWhat:&r a Stable Wormhole opens your Storage Actuator from another room; the Storage Remote opens it from anywhere.",
        "&eHow:&r wormhole: foliot crafting ritual with an otherstone frame, an ender pearl, 2 quartz and 2 gold. Remote: a djinni ritual with an inert remote, two ender pearls and quartz. Link both by clicking the Actuator.",
        "&eTip:&r put a wormhole beside each crafting area."]),
    Q("oc_remote", 20, 4.5, [item("occultism:storage_remote")], "Storage Remote", deps=["oc_storage"], xp=75,
      optional=True, tokens=1, subtitle="Optional: your storage in your pocket", desc=[
        "&eWhat:&r opens your Storage Actuator from anywhere.",
        "&eHow:&r a djinni ritual with an inert remote (iesnium nuggets, an attuned gem, an otherstone tablet, silver), two ender pearls and quartz. Link it by clicking the Actuator.",
        "&eTip:&r one remote per player saves a lot of walking back to base."]),

    # --- Iesnium and the miners --------------------------------------------------------------------------------
    Q("oc_infused_pick", 18, 0, [item("occultism:infused_pickaxe")], "Infused Pickaxe", deps=["oc_goggles", "oc_strigeor", "oc_attuned_gem"],
      xp=75, section=MINERS, mirror="2A3683BF7E50EF83", subtitle="A pickaxe that can cut otherworld ore", desc=[
        "&eWhat:&r a djinni bound into a pickaxe lets you mine otherworld materials such as iesnium ore.",
        "&eHow:&r a spirit-attuned pickaxe head (3 gems) with 2 sticks and 2 silver ingots, in Strigeor's Higher Binding (the djinni crafting pentacle).",
        "&eTip:&r you only need it until you have iesnium; then make an iesnium pickaxe."]),
    Q("m_iesnium", 20, 0, [anyof([O + "iesnium_ore", O + "raw_iesnium", O + "iesnium_ingot"])], "Iesnium", deps=["oc_infused_pick", "t2_nether"], xp=75,
      mirror="33106E24A3B5DDD8", subtitle="An Otherworld metal from the Nether", desc=[
        "&eWhat:&r iesnium ore hides in the Nether and only shows up with the Third Eye. You need the infused pickaxe to mine it.",
        "&eHow:&r wear the goggles (or eat Demon's Dream) in the Nether, mine the ore with the infused pickaxe and smelt it. Ore, raw or ingot completes this.",
        "&eTip:&r three ingots make an iesnium pickaxe, which every miner spirit needs."]),
    Q("oc_iesnium_pick", 0, 0, [item("occultism:iesnium_pickaxe")], "Iesnium Pickaxe", deps=["m_iesnium"], xp=60,
      mirror="57282D7E31EE61EE", subtitle="The pickaxe every miner needs", desc=[
        "&eWhat:&r the iesnium pickaxe mines otherworld blocks and is an ingredient of every miner spirit.",
        "&eHow:&r 3 iesnium ingots over 2 sticks. An iesnium block (9 ingots) goes into the Dimensional Mineshaft.",
        "&eTip:&r you'll want a spare pickaxe for each miner upgrade."]),
    Q("m_miner", 22, 0, [item("occultism:dimensional_mineshaft"), item("occultism:miner_foliot_unspecialized")], "Spirit Miners", deps=["oc_iesnium_pick"], xp=150,
      size=1.5, mirror="172D2A634E849562", subtitle="A spirit digs in a world you can't see", desc=[
        "&6You remember the earth giving up its treasures when asked. Now a spirit asks for you.&r",
        "&eWhat:&r the Dimensional Mineshaft holds a miner spirit that pulls blocks from the Otherworld over time.",
        "&eHow:&r mineshaft: djinni ritual with 4 otherstone, gold, an iesnium block and a spirit-attuned crystal. Foliot miner: a magic lamp (silver and an attuned gem), an iesnium pickaxe, iron and gravel.",
        "&eTip:&r in this pack miners &ccan't&r produce chemistry-milestone ores: " + MINER_BAN + ". Those still come from real processing."]),
    Q("oc_miner_djinni", 24, 0, [item("occultism:miner_djinni_ores")], "Djinni Miner", deps=["m_miner"], xp=150,
      subtitle="A faster miner that only brings ores", desc=[
        "&eWhat:&r the djinni miner skips the stone and pulls only ores, much faster than a foliot.",
        "&eHow:&r a djinni ritual with the foliot miner, an iesnium pickaxe, gold, lapis and a spirit-attuned crystal.",
        "&eTip:&r the pack's ban list still applies: no " + MINER_BAN + "."]),
    Q("oc_miner_afrit", 26, 0, [item("occultism:miner_afrit_deeps")], "Afrit Deep Miner", deps=["oc_miner_djinni", "oc_red_chalk"], xp=200,
      subtitle="Deepslate ores from the Otherworld", desc=[
        "&eWhat:&r the afrit miner brings deepslate ores as well as normal ones, faster again.",
        "&eHow:&r an afrit crafting ritual: the djinni miner, an iesnium pickaxe, a spirit-attuned crystal, afrit essence, an echo shard and crying obsidian.",
        "&eTip:&r miners wear out. Repair them with otherworld essence and an attuned gem in an afrit pentacle (check the Dictionary)."]),
    Q("oc_miner_marid", 28, 0, [item("occultism:miner_marid_master")], "Marid Master Miner", deps=["oc_miner_afrit", "oc_blue_chalk"], xp=300,
      size=1.5, shape="hexagon", subtitle="The strongest miner a mortal can bind", desc=[
        "&6You remember commanding the deep places. A marid remembers being commanded.&r",
        "&eWhat:&r the marid miner is the fastest and also finds rare otherworld blocks like iesnium ore and ancient debris.",
        "&eHow:&r a marid crafting ritual: the afrit miner, an iesnium pickaxe, a spirit-attuned crystal, a netherite pickaxe, dragon's breath, a Totem of Undying, a Nether Star and marid essence.",
        "&eTip:&r even a marid can't reach the pack's chemistry milestones: no " + MINER_BAN + "."]),

    # --- The afrit ---------------------------------------------------------------------------------------------
    Q("oc_ihagan", 0, 0, [item("minecraft:honey_block"), item("minecraft:honeycomb_block"), item("minecraft:honeycomb"), item("minecraft:honey_bottle")],
      "A Possessed Bee", deps=["oc_research", "oc_djinni"], xp=75, size=1.5, shape="hexagon", section=AFRIT, mirror="0BD6365534BF04D5",
      subtitle="Ihagan's Enthrallment", desc=[
        "&eWhat:&r the djinni possession pentacle (white, light gray, lime and gold) puts a djinni into a bee. The possessed bee drops cursed honey, the special ingredient of orange chalk.",
        "&eChemistry:&r honey is a supersaturated sugar solution, mostly fructose and glucose with under 20% water, which is why it never spoils.",
        "&eHow:&r these four honey items in the bowls, a chicken as the sacrifice, your djinni book to start it.",
        "&eTip:&r a bee farm makes the honey side easy."]),
    Q("oc_orange_chalk", 20, -4.5, [item("occultism:cursed_honey"), item("occultism:chalk_orange")], "Orange Chalk", deps=["oc_ihagan"], xp=60,
      mirror="74130EB1E4B8586D", subtitle="Sweet bait for an afrit", desc=[
        "&eWhat:&r orange chalk lures afrits. It doesn't control them; that takes red chalk.",
        "&eHow:&r impure white chalk with cursed honey, glow berries and blaze dust, purified in spiritfire.",
        "&eTip:&r afrit pentacles use orange, gray and lime together."]),
    Q("oc_afrit", 18, -3, [item("occultism:book_of_binding_bound_afrit")], "Bind an Afrit", deps=["oc_djinni"], xp=150,
      subtitle="A spirit of fire", desc=[
        "&eWhat:&r afrits are the third rank of spirits. They power stronger rituals and the deep-mining miner.",
        "&eHow:&r a Book of Binding with yellow dye, bound with the spirit's name (see the Dictionary).",
        "&eTip:&r afrit rituals need afrit essence, which only an unbound afrit drops."]),
    Q("oc_kandar", 0, 0, [item("occultism:iesnium_ingot"), item("minecraft:gunpowder"), item("minecraft:netherrack"), item("minecraft:flint_and_steel")],
      "Calling a Wild Afrit", deps=["oc_gray_chalk", "oc_orange_chalk", "m_iesnium"], xp=100, size=1.5, shape="hexagon", mirror="38A1295878B68F83",
      subtitle="Kandar's Opened Conjure", desc=[
        "&eWhat:&r the unbound afrit pentacle (white, gray, lime, orange, skulls and a spirit-attuned crystal) calls an afrit that answers to no one.",
        "&eHow:&r netherrack, an iesnium ingot, flint and steel and gunpowder in the bowls, a cow as the sacrifice, your afrit book to start it.",
        "&eTip:&r build it far from anything flammable. Then read the next quest before you light it."]),
    Q("oc_afrit_wild", 20, -3, [kill("occultism:afrit_wild")], "Unbound Afrit", deps=["oc_kandar", "oc_afrit"], xp=300, loot="boss",
      size=1.5, shape="hexagon", subtitle="Summon a wild afrit and defeat it", desc=[
        "&6You remember fire that obeyed. This one remembers being free.&r",
        "&eWhat:&r the unbound afrit is hostile. It drops afrit essence when killed.",
        "&eHow:&r start Kandar's Opened Conjure and fight what comes out.",
        "&eTip:&r fire resistance potions turn this from a disaster into a fair fight."]),
    Q("oc_red_chalk", 22, -3, [item("occultism:afrit_essence"), item("occultism:chalk_red")], "Red Chalk", deps=["oc_afrit_wild"], xp=75,
      mirror="145C8235BCCB9BA8", subtitle="Command an afrit", desc=[
        "&eWhat:&r red chalk is made from afrit essence and lets your pentacles bind afrits instead of just calling them.",
        "&eHow:&r impure white chalk with afrit essence, a torchflower and redstone dust, purified in spiritfire.",
        "&eTip:&r Sevira's Permanent Confinement (the afrit crafting pentacle) uses red, orange, lime, purple, gray and white."]),
    Q("oc_odus", 0, 0, [item("minecraft:gilded_blackstone"), item("minecraft:quartz"), item("minecraft:warped_fungus"), item("minecraft:crimson_fungus")],
      "A Possessed Piglin", deps=["oc_orange_chalk", "oc_gray_chalk", "oc_afrit"], xp=75, optional=True, tokens=1, size=1.5, shape="hexagon",
      mirror="429B5A81DF6C43FE", subtitle="Optional: Odus' Open Convocation", desc=[
        "&eWhat:&r the unbound-afrit possession pentacle puts an afrit into a zombified piglin. It drops demonic meat, the special ingredient of pink chalk.",
        "&eHow:&r gilded blackstone, quartz, a warped and a crimson fungus in the bowls, a pig as the sacrifice, your afrit book to start it.",
        "&eTip:&r gilded blackstone only comes from bastions; mine it with Silk Touch or it drops gold nuggets."]),
    Q("oc_pink_chalk", 0, 0, [item("occultism:demonic_meat", 3), item("occultism:chalk_pink")], "Pink Chalk", deps=["oc_odus"], xp=60,
      optional=True, tokens=1, mirror="2E68E1D96B25336D", subtitle="Optional: one of the wild-calling colours", desc=[
        "&eWhat:&r pink chalk is one of three colours (with green and light blue) in the pentacle that calls wild spirits.",
        "&eHow:&r impure white chalk with 3 demonic meat, purified in spiritfire.",
        "&eTip:&r the piglin drops plenty; save the rest for the ritual."]),
    Q("oc_green_chalk", 0, 0, [item("occultism:nature_paste"), item("occultism:chalk_green")], "Green Chalk", deps=["oc_eziveus"], xp=60,
      optional=True, tokens=1, mirror="11A0593C0E2E6A35", subtitle="Optional: leaves, saplings and seeds", desc=[
        "&eWhat:&r green chalk, the second wild-calling colour, is made from nature paste.",
        "&eChemistry:&r leaves are green because chlorophyll absorbs red and blue light and reflects green; it's a magnesium complex at heart.",
        "&eHow:&r nature paste is a foliot crafting ritual: 3 leaves, 3 saplings and 3 seeds. Then impure white chalk with the paste, purified in spiritfire.",
        "&eTip:&r any leaves, saplings and seeds will do."]),
    Q("oc_sevira", 0, 0, [item("minecraft:wither_rose", 3), anytag("c:dusts/netherite"), item("occultism:crushed_blackstone"),
                          item("minecraft:wither_skeleton_skull")], "The Afrit's Forge", deps=["oc_red_chalk"], xp=150, size=1.5, shape="hexagon",
      mirror="2960FFE0C53DFEB1", subtitle="Sevira's Permanent Confinement", desc=[
        "&eWhat:&r the afrit crafting pentacle binds afrits into things: witherite dust, the second satchel, iesnium bowls and miners.",
        "&eChemistry:&r real witherite is barium carbonate, BaCO₃, named after the 18th-century chemist William Withering. It has nothing to do with the Wither.",
        "&eHow:&r these are witherite dust's ingredients: a wither rose, netherite dust (crush a netherite ingot), crushed blackstone and a wither skeleton skull. Extra roses for later batches.",
        "&eTip:&r save one netherite ingot for the crusher; it's the costly part."]),
    Q("oc_black_chalk", 24, -3, [item("occultism:witherite_dust"), item("occultism:chalk_black")], "Black Chalk", deps=["oc_sevira"], xp=75,
      mirror="367E891A50991436", subtitle="The darkest foundation", desc=[
        "&eWhat:&r black chalk is the strongest foundation chalk; marid pentacles need it.",
        "&eHow:&r the afrit ritual gives 3 witherite dust. Impure white chalk with witherite dust, purified in spiritfire.",
        "&eTip:&r three dust is enough for a few chalks; plan your marid circle first."]),
    Q("oc_ritual_satchel_t2", 0, 0, [item("occultism:ritual_satchel_t2")], "Artisanal Ritual Satchel", deps=["oc_ritual_satchel", "oc_sevira"], xp=100,
      optional=True, tokens=1, mirror="4CE571F942461909", subtitle="Optional: an afrit sets the whole circle at once", desc=[
        "&eWhat:&r the afrit version places a whole pentacle in one click, and can also pick one up again: chalk, candles and all.",
        "&eHow:&r an afrit upgrade ritual: the apprentice satchel, afrit essence and 4 ender pearls (it keeps the contents).",
        "&eTip:&r right-click the golden bowl with it to clear an intact pentacle."]),
    Q("oc_repair", 0, 0, [tick()], "Mending Tools", deps=["oc_sevira"], xp=20, optional=True, tokens=1, mirror="1848F431D0380DA9",
      icon="occultism:iesnium_pickaxe", subtitle="Optional: an afrit fixes your gear", desc=[
        "&eWhat:&r on the afrit crafting pentacle, a tool (or armour, or a worn miner) is fully repaired by infusing it with an afrit.",
        "&eHow:&r 3 otherworld essence and a spirit-attuned gem in the bowls; start the ritual with the item itself. Tick the box when you've read this.",
        "&eTip:&r cheaper than an anvil for heavily enchanted gear: no level cost."]),
    Q("oc_iesnium_bowl", 0, 0, [anyof([O + "iesnium_sacrificial_bowl", O + "dark_iesnium_sacrificial_bowl"])], "Iesnium Ritual Bowl",
      deps=["oc_sevira"], xp=100, optional=True, tokens=1, mirror="6FFFAE334DFAAAAB", subtitle="Optional: rituals in a quarter of the time", desc=[
        "&eWhat:&r a centre bowl that runs any ritual in a quarter of the normal time.",
        "&eHow:&r an afrit crafting ritual: a golden bowl, research fragment dust, a spirit-attuned crystal, an iesnium block and afrit essence.",
        "&eTip:&r swap it in for the golden bowl on your busiest pentacle."]),

    # --- The marid ---------------------------------------------------------------------------------------------
    Q("oc_marid", 24, -4.5, [item("occultism:book_of_binding_bound_marid")], "Bind a Marid", deps=["oc_red_chalk"], xp=150,
      section=MARID, subtitle="The highest spirit you can name", desc=[
        "&eWhat:&r marids are the fourth and strongest rank of spirits.",
        "&eHow:&r a Book of Binding with green dye, bound with a name like the others.",
        "&eTip:&r like the afrit, its essence only comes from an unbound one."]),
    Q("oc_tibira", 0, 0, [item("minecraft:prismarine_crystals"), item("minecraft:prismarine_shard"), item("minecraft:ghast_tear"),
                          item("minecraft:conduit"), item("minecraft:trident")], "Calling a Wild Marid", deps=["oc_black_chalk"], xp=150,
      size=1.5, shape="hexagon", mirror="53DEA3DFEDC4809E", subtitle="Tibira's Attraction", desc=[
        "&eWhat:&r the unbound marid pentacle (black, red, orange, lime and white chalk, wither skulls and a crystal) calls a hostile marid.",
        "&eHow:&r a conduit, prismarine crystals, a prismarine shard and a ghast tear in the bowls; use the trident to start it.",
        "&eTip:&r the conduit and trident come from the ocean: a monument and a drowned with luck."]),
    Q("oc_marid_wild", 26, -3, [kill("occultism:marid_unbound")], "Unbound Marid", deps=["oc_tibira", "oc_marid"], xp=400, loot="boss",
      size=1.5, shape="hexagon", subtitle="Summon a wild marid and survive", desc=[
        "&6You remember the sea answering you. This spirit answers to no one.&r",
        "&eWhat:&r the unbound marid is hostile and very strong. It drops marid essence.",
        "&eHow:&r start Tibira's Attraction and win.",
        "&eTip:&r bring your best armor and healing, and don't do it at home."]),
    Q("oc_blue_chalk", 28, -3, [item("occultism:marid_essence"), item("occultism:chalk_blue")], "Blue Chalk", deps=["oc_marid_wild"], xp=75,
      mirror="03250A0202C25E80", subtitle="Command a marid", desc=[
        "&eWhat:&r blue chalk, made from marid essence, lets pentacles control marids.",
        "&eChemistry:&r tube coral builds its skeleton from calcium carbonate (aragonite), the same CaCO₃ as your chalk.",
        "&eHow:&r impure white chalk with marid essence, lapis dust and tube coral, purified in spiritfire.",
        "&eTip:&r Uphyxes' Inverted Tower, the marid crafting pentacle, makes the master miner and tier 4 stabilizers."]),
    Q("oc_fatma", 0, 0, [item("minecraft:diamond_block"), item("minecraft:emerald_block"), item("occultism:iesnium_block"), item("minecraft:ghast_tear")],
      "A Marid Crusher", deps=["oc_blue_chalk"], xp=150, optional=True, tokens=2, size=1.5, shape="hexagon", mirror="2AD68066C1948C90",
      subtitle="Optional: Fatma's Incentivized Attraction", desc=[
        "&eWhat:&r the marid summoning pentacle calls a marid crusher, the fastest crusher and the only one that grinds echo shards.",
        "&eHow:&r diamond, emerald, iesnium and netherite blocks and a ghast tear in the bowls, your marid book to start it.",
        "&eTip:&r still 2 dust per ore in this pack; you pay for speed and for the rare dusts."]),
    Q("oc_xeovrenth", 0, 0, [item("minecraft:armadillo_scute", 4), item("minecraft:rabbit_foot", 4), item("minecraft:pointed_dripstone", 2),
                             anytag("minecraft:wool", 2)], "A Possessed Goat", deps=["oc_blue_chalk"], xp=150, optional=True, tokens=2,
      size=1.5, shape="hexagon", mirror="56EC79AF11B0869E", subtitle="Optional: Xeovrenth Adjure", desc=[
        "&eWhat:&r the marid possession pentacle puts a marid into a goat. The goat drops cruelty essence, the special ingredient of brown chalk.",
        "&eHow:&r 4 armadillo scutes, 4 rabbit feet, 2 pointed dripstone and 2 wool in the bowls, your marid book to start it. The Dictionary names the sacrifice.",
        "&eTip:&r Looting raises the essence drop."]),
    Q("oc_uphyxes", 0, 0, [item("minecraft:dragon_breath", 3), item("occultism:amethyst_dust", 2), item("occultism:crushed_end_stone"),
                           item("minecraft:end_crystal", 4)], "The Marid's Tower", deps=["oc_blue_chalk"], xp=150, optional=True, tokens=2,
      size=1.5, shape="hexagon", mirror="2CF96A264EB5522C", subtitle="Optional: Uphyxes' Inverted Tower", desc=[
        "&eWhat:&r the marid crafting pentacle makes the master miner, tier 4 stabilizers, the iesnium anvil and dragonyst dust.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured purple by iron impurities changed by natural radiation.",
        "&eHow:&r these are dragonyst dust's ingredients: 3 dragon's breath, 2 amethyst dust, crushed end stone and 4 end crystals.",
        "&eTip:&r catch dragon's breath in bottles during the dragon fight's breath attack."]),
    Q("oc_iesnium_anvil", 0, 0, [item("occultism:iesnium_anvil")], "Iesnium Anvil", deps=["oc_uphyxes"], xp=150,
      optional=True, tokens=2, size=1.5, shape="hexagon", mirror="1BDB369FD243D4C6", subtitle="Optional: an anvil a marid helps you pay for", desc=[
        "&eWhat:&r an unbreakable anvil that can go one level past an enchantment's maximum, and the marid pays half the level cost.",
        "&eHow:&r a marid crafting ritual: an anvil, 3 iesnium blocks and marid essence.",
        "&eTip:&r pair it with the Enchantment Library from Apotheosis for top-level books."]),
    Q("oc_lightblue_chalk", 0, 0, [item("occultism:crushed_ice"), item("occultism:crushed_packed_ice"), item("occultism:crushed_blue_ice"),
                                   item("occultism:chalk_light_blue")], "Light Blue Chalk", deps=["oc_fatma", "oc_ophyx"], any_dep=True, xp=75,
      optional=True, tokens=1, mirror="1EB887F8072439A3", subtitle="Optional: three kinds of ice, crushed", desc=[
        "&eWhat:&r light blue chalk, the third wild-calling colour, is made from crushed ice.",
        "&eChemistry:&r ice is H₂O in a hexagonal lattice that is less dense than liquid water, which is why it floats.",
        "&eHow:&r a djinni (or marid) crusher grinds ice, packed ice and blue ice. Impure white chalk with all three dusts, purified in spiritfire.",
        "&eTip:&r a foliot crusher can't do ice; it needs at least a djinni."]),
    Q("oc_wildhunt", 22, -4.5, [kill("occultism:wild_hunt_wither_skeleton", 5)], "The Wild Hunt",
      deps=["oc_green_chalk", "oc_pink_chalk", "oc_lightblue_chalk", "t2_nether"], xp=150, loot="hunt", optional=True, tokens=1,
      size=1.5, shape="hexagon", mirror="67884BFA27870CCE", subtitle="Optional: kill 5 Wild Hunt wither skeletons", desc=[
        "&eWhat:&r the Wild Hunt ritual calls a pack of wither skeletons with a good chance of dropping wither skeleton skulls.",
        "&eHow:&r Osorin's Unbound Calling (green, light blue and pink chalk; check the Dictionary). Activated with a skeleton skull; copper, silver and gold blocks, a diamond, netherrack and soul sand, plus a sacrifice.",
        "&eTip:&r skulls without trial chambers or fortress farming: enough for the Wither and every marid pentacle."]),

    # --- Every colour --------------------------------------------------------------------------------------------
    Q("oc_magenta_chalk", 0, 0, [item("occultism:dragonyst_dust"), item("occultism:chalk_magenta")], "Magenta Chalk",
      deps=["oc_uphyxes", "oc_fatma"], xp=75, optional=True, tokens=1, section=COLOURS, mirror="3543563DF036D461",
      subtitle="Optional: dragonyst and amethyst", desc=[
        "&eWhat:&r magenta chalk is one of the last colours, made from dragonyst dust.",
        "&eHow:&r impure white chalk with dragonyst dust, amethyst dust and a chorus fruit, purified in spiritfire.",
        "&eTip:&r one dragonyst ritual gives one dust; it's the slow part."]),
    Q("oc_cyan_chalk", 0, 0, [item("occultism:echo_dust"), item("occultism:chalk_cyan")], "Cyan Chalk", deps=["oc_fatma"], xp=75,
      optional=True, tokens=1, mirror="00A6020BC979947F", subtitle="Optional: echo and iesnium", desc=[
        "&eWhat:&r cyan chalk is made from echo dust, which only a marid crusher can grind.",
        "&eHow:&r impure white chalk with iesnium dust, echo dust and a glow ink sac, purified in spiritfire.",
        "&eTip:&r echo shards come from Ancient City chests."]),
    Q("oc_brown_chalk", 0, 0, [item("occultism:cruelty_essence"), item("occultism:chalk_brown")], "Brown Chalk", deps=["oc_xeovrenth"], xp=75,
      optional=True, tokens=1, mirror="7BCD4A425CF6199B", subtitle="Optional: cruelty, cocoa and mushroom", desc=[
        "&eWhat:&r brown chalk is made from the possessed goat's cruelty essence.",
        "&eHow:&r impure white chalk with cruelty essence, cocoa beans and a brown mushroom, purified in spiritfire.",
        "&eTip:&r that's the last of the sixteen colours."]),
    Q("oc_all_chalks", 0, 0, [item(i) for i in IMPURE], "Sixteen Colours", deps=["oc_magenta_chalk", "oc_brown_chalk", "oc_cyan_chalk"],
      xp=300, optional=True, tokens=2, size=2.0, shape="gear", mirror="0A25276925EB0CBA", subtitle="Optional: every impure chalk at once", desc=[
        "&6You remember drawing circles in every colour light can take. Your hand remembers the order.&r",
        "&eWhat:&r one impure chalk of each of the sixteen colours: everything the pentacles of Occultism are drawn with.",
        "&eHow:&r each is impure white chalk plus its special ingredient; this page has a quest for every one.",
        "&eTip:&r the eldritch rituals that follow want the purified chalks, so purify a second set."]),
    Q("oc_rainbow", 0, 0, [item("occultism:chalk_rainbow")], "Rainbow Chalk", deps=["oc_all_chalks"], xp=200,
      optional=True, tokens=2, mirror="690B89D23134B624", subtitle="Optional: one chalk for every glyph", desc=[
        "&eWhat:&r rainbow chalk can stand in for any coloured chalk glyph and takes on its look.",
        "&eChemistry:&r chalk colours come from pigments; the oldest, like red ochre (Fe₂O₃), are iron oxides people have used for 100,000 years.",
        "&eHow:&r Ronaza's Contact (the eldritch pentacle) with 12 coloured chalks, a sheep as the sacrifice and the brush to start it. The Dictionary shows the circle and the full list."]),
    Q("oc_void_chalk", 0, 0, [item("occultism:chalk_void")], "Void Chalk", deps=["oc_all_chalks"], xp=200, optional=True, tokens=2,
      mirror="54378277B8D28B1D", subtitle="Optional: rainbow chalk in black and white", desc=[
        "&eWhat:&r void chalk does what rainbow chalk does, flickering white to black instead of in colour.",
        "&eHow:&r Ronaza's Contact with white, light gray, gray and black chalk, started with the brush. The Dictionary names the sacrifice.",
        "&eTip:&r pick whichever look suits your ritual room."]),
    Q("oc_trinity", 0, 0, [item("occultism:trinity_gem")], "Trinity Gem", deps=["oc_all_chalks", "oc_soulgem"], xp=250, optional=True, tokens=2,
      mirror="2FD22502E6481269", subtitle="Optional: a soul gem that holds bosses", desc=[
        "&eWhat:&r the upgraded soul gem: it can capture bosses, and in a Dimensional Battlefield it farms possessed mobs and triples other loot.",
        "&eHow:&r Ronaza's Contact, started with a soul gem: afrit, marid and cruelty essence, echo, dragonyst and witherite dust, and 3 iesnium dust.",
        "&eTip:&r it takes one of every late essence and dust, so it's a good test of your whole setup."]),
    Q("oc_chalice", 0, 0, [anyof([O + "celestial_chalice", O + "eldritch_chalice"])], "The Chalice", deps=["oc_all_chalks", "oc_iesnium_bowl"],
      xp=250, optional=True, tokens=2, mirror="08697EB269B011FD", subtitle="Optional: rituals in an instant", desc=[
        "&eWhat:&r a centre bowl that performs any ritual instantly. Celestial and Eldritch are the light and dark versions.",
        "&eHow:&r Ronaza's Contact, started with an iesnium bowl, a ravager as the sacrifice and twelve rare blocks (heavy core, reinforced deepslate, sculk catalyst and more; check JEI).",
        "&eTip:&r it ends every wait at every pentacle you build it into."]),
    Q("oc_next", 0, 0, [tick()], "The Spirits Are Yours", deps=["oc_trinity", "oc_rainbow", "oc_chalice", "oc_stabilizer"], xp=100,
      optional=True, tokens=2, size=2.0, shape="gear", mirror="29C83B00AC4AFC23", icon="occultism:chalk_rainbow",
      subtitle="Optional: the end of the Dictionary", desc=[
        "&6You remember standing at the centre of every circle at once. Now the circles stand around you.&r",
        "&eWhat:&r you've bound every rank of spirit and drawn every colour. What's left is putting them to work.",
        "&eHow:&r tick the box. Good next steps: miners for the ores they're allowed, crushers on autopilot, familiars for the road.",
        "&eTip:&r the chemistry-milestone ores still need the real chemistry lines; no spirit fetches those."]),
], links=[("gs_iron", -2, 0), ("t2_nether", 20, -1.5)], mirror="occultism")
