"""Quest chapter: occultism. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

# Layout: the main line runs left to right at y=0 (Third Eye -> spiritfire -> chalks -> foliot -> djinni -> miners).
# The afrit and marid ladder sits above (y<0), storage and djinni utilities below (y>0).
# Recipes and pentacle chalk colours checked against occultism 1.224.5 (data/occultism/recipe and modonomicon
# multiblocks). Almost Unified merges common dusts and ingots into MI's, so tasks use tags (anytag) for those.
# Pack gate: phase4_occultism.js removes miner recipes for uranium, uraninite, osmium, fluorite, platinum, iridium, tungsten.

MINER_BAN = "uranium, uraninite, osmium, fluorite, platinum, iridium or tungsten"

CHAPTER = Chapter("occultism", "Occultism", "occultism:datura",
        ["Spirits, pentacles, otherworld storage and miners that dig where you can't."], SIDE, [
    # --- Main line (y=0) -----------------------------------------------------------------------
    Q("m_datura", 0, 0, [item("occultism:datura", 4)], "Demon's Dream", deps=["gs_iron"], xp=40,
      subtitle="Eat it and see the Otherworld", desc=[
        "&6You remember seeing everything at once. One bite, and some of it comes back.&r",
        "&eWhat:&r eating Demon's Dream Fruit gives the Third Eye: you see Otherworld blocks hidden behind normal ones.",
        "&eHow:&r break grass for Demon's Dream seeds, grow them, and eat a fruit. Seeds plus a book make the Dictionary of Spirits, which explains the rest.",
        "&eTip:&r with the Third Eye active, otherworld trees appear among normal oaks."]),
    Q("oc_spiritfire", 2, 0, [item("occultism:otherstone", 16)], "Spiritfire", deps=["m_datura"], xp=50,
      subtitle="A fire that changes things instead of burning them", desc=[
        "&eWhat:&r spiritfire doesn't hurt you and doesn't destroy items: things thrown into it come out converted.",
        "&eChemistry:&r andesite, the input for otherstone, is a grey volcanic rock made mostly of plagioclase feldspar.",
        "&eHow:&r throw a Demon's Dream Fruit on the ground and light it with flint and steel. Then throw andesite in for otherstone (diorite gives otherrock).",
        "&eTip:&r books, feathers and black dye also go in: they come out as taboo books, awakened feathers and purified ink."]),
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
        "&eHow:&r throw an oak sapling into spiritfire for an unstable otherworld sapling, grow it, and cut it while under the Third Eye. Burn logs for ashes.",
        "&eTip:&r a foliot sapling trader later sells stable saplings that don't need the Third Eye."]),
    Q("oc_burnt", 4, 1.5, [item("occultism:burnt_otherstone", 3)], "Burnt Otherstone", deps=["oc_spiritfire"], xp=30,
      subtitle="The other half of chalk", desc=[
        "&eWhat:&r burnt otherstone counts as otherstone dust, the base of every chalk.",
        "&eHow:&r cut or craft otherstone into polished otherstone, then smelt it in a furnace.",
        "&eTip:&r make a stack; every new chalk colour starts from white impure chalk."]),
    Q("m_chalk", 6, 0, [item("occultism:chalk_white"), item("occultism:golden_sacrificial_bowl"), item("occultism:sacrificial_bowl", 4)], "Your First Pentacle",
      deps=["oc_otherwood", "oc_burnt"], xp=60, subtitle="Chalk, bowls and a circle", desc=[
        "&eWhat:&r rituals happen on chalk pentacles, with a Golden Sacrificial Bowl at the centre and Sacrificial Bowls holding the ingredients.",
        "&eChemistry:&r real chalk is calcium carbonate, CaCO₃: the shells of tiny sea creatures, pressed into rock.",
        "&eHow:&r burnt otherstone and otherworld ashes make impure white chalk; purify it in spiritfire. Bowls are otherstone (the golden one adds gold). The Dictionary shows each pentacle's layout.",
        "&eTip:&r ingredient bowls can stand anywhere within 8 blocks of the golden bowl."]),
    Q("m_foliot", 8, 0, [item("occultism:book_of_binding_bound_foliot")], "Bind a Foliot", deps=["m_chalk"], xp=75,
      subtitle="Learn a spirit's true name", desc=[
        "&eWhat:&r a bound Book of Binding holds a spirit's name and starts its rituals. Foliots are the weakest spirits.",
        "&eHow:&r craft the Book of Binding (taboo book, purified ink, awakened feather, blue dye), then bind it with a name as the Dictionary describes (check JEI).",
        "&eTip:&r Aviar's Circle, the foliot summoning pentacle, uses only white chalk."]),
    Q("oc_crusher", 10, 0, [anytag("c:dusts/gold", 4), anytag("c:dusts/obsidian", 2)], "Foliot Crusher", deps=["m_foliot"], xp=60,
      subtitle="A spirit that grinds ore to dust", desc=[
        "&eWhat:&r a crusher spirit picks up ores and gems and drops dusts. New chalks need gold, silver, iron, emerald, calcite and obsidian dust.",
        "&eHow:&r Summon Foliot Crusher: iron, gold, copper and silver ingots in the bowls, a white-chalk circle. Feed it items; any gold and obsidian dust counts for this quest.",
        "&eTip:&r a foliot gives 2 dusts per ore, the pack's normal cap. Bigger crushers exist; use the MI and Mekanism ore lines for real ore yield."]),
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
    Q("oc_purple_chalk", 12, 0, [item("occultism:chalk_purple")], "Purple Chalk", deps=["oc_endermite"], xp=60,
      subtitle="The chalk of infusion", desc=[
        "&eWhat:&r purple chalk binds spirits into objects. Every crafting ritual (satchels, storage, miners) needs it.",
        "&eChemistry:&r obsidian is volcanic glass, about 70% SiO₂ that cooled too fast to crystallise.",
        "&eHow:&r impure white chalk with crushed end stone and 2 obsidian dust, purified in spiritfire.",
        "&eTip:&r Eziveus' Spectral Compulsion (white + purple) is the foliot crafting pentacle."]),
    Q("oc_research", 14, -1.5, [item("occultism:research_fragment_dust", 2)], "Research Fragment Dust", deps=["oc_purple_chalk"], xp=50,
      subtitle="Experience pressed into emerald", desc=[
        "&eWhat:&r research fragment dust is the special ingredient of lime chalk and knowledge tablets.",
        "&eChemistry:&r emerald is beryl, Be₃Al₂Si₆O₁₈, coloured green by traces of chromium.",
        "&eHow:&r foliot crafting ritual: emerald dust and 2 bottles o' enchanting.",
        "&eTip:&r crush emeralds with your crusher spirit for the dust."]),
    Q("oc_lime_chalk", 16, -1.5, [item("occultism:chalk_lime")], "Lime Chalk", deps=["oc_research"], xp=60,
      subtitle="The chalk that calls djinn", desc=[
        "&eWhat:&r lime chalk attracts spirits stronger than foliots. Every djinni pentacle and up uses it.",
        "&eHow:&r impure white chalk with research fragment dust, emerald dust and a slime ball, purified in spiritfire.",
        "&eTip:&r make several; afrit and marid pentacles still use lime."]),
    Q("oc_lightgray_chalk", 14, 1.5, [item("occultism:chalk_light_gray")], "Light Gray Chalk", deps=["oc_crusher", "oc_silver"], xp=50,
      subtitle="Real chalk, finally", desc=[
        "&eWhat:&r light gray chalk strengthens a pentacle's foundation; djinni pentacles need it.",
        "&eChemistry:&r calcite is CaCO₃, exactly the compound real chalk and limestone are made of.",
        "&eHow:&r impure white chalk with silver dust, iron dust and crushed calcite, purified in spiritfire.",
        "&eTip:&r calcite lines amethyst geodes, so collect it while you farm source gems."]),
    Q("oc_djinni", 16, 0, [item("occultism:book_of_binding_bound_djinni")], "Bind a Djinni", deps=["oc_lime_chalk", "oc_lightgray_chalk", "oc_skulls"],
      xp=100, size=1.5, subtitle="A stronger spirit for bigger rituals", desc=[
        "&6You remember spirits who bowed when you passed. This one only negotiates.&r",
        "&eWhat:&r djinn are the second rank of spirits. Their rituals make storage, soul gems, the infused pickaxe and better miners.",
        "&eHow:&r a Book of Binding with purple dye, bound with a name like the foliot one. Djinni pentacles add light gray and lime chalk and skeleton skulls.",
        "&eTip:&r the Dictionary's Pentacles section is a table: each tier upgrades the pentacle you drew before."]),
    Q("oc_infused_pick", 18, 0, [item("occultism:infused_pickaxe")], "Infused Pickaxe", deps=["oc_djinni", "oc_attuned_gem"], xp=75,
      subtitle="A pickaxe that can cut otherworld ore", desc=[
        "&eWhat:&r a djinni bound into a pickaxe lets you mine otherworld materials such as iesnium ore.",
        "&eHow:&r a spirit-attuned pickaxe head (3 gems) with 2 sticks and 2 silver ingots, in Strigeor's Higher Binding (the djinni crafting pentacle).",
        "&eTip:&r you only need it until you have iesnium; then make an iesnium pickaxe."]),
    Q("m_iesnium", 20, 0, [item("occultism:iesnium_ingot", 2)], "Iesnium", deps=["oc_infused_pick", "t2_nether"], xp=75,
      subtitle="An Otherworld metal from the Nether", desc=[
        "&eWhat:&r iesnium ore hides in the Nether and only shows up with the Third Eye. You need the infused pickaxe to mine it.",
        "&eHow:&r eat Demon's Dream (or wear goggles) in the Nether, mine the ore with the infused pickaxe and smelt it.",
        "&eTip:&r three ingots make an iesnium pickaxe, which every miner spirit needs."]),
    Q("m_miner", 22, 0, [item("occultism:dimensional_mineshaft"), item("occultism:miner_foliot_unspecialized")], "Spirit Miners", deps=["m_iesnium"], xp=150,
      size=1.5, subtitle="A spirit digs in a world you can't see", desc=[
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

    # --- Foliot helpers (y=1.5 .. 3) -----------------------------------------------------------
    Q("oc_candles", 6, 1.5, [item("occultism:butcher_knife"), item("occultism:large_candle", 4)], "Tallow and Candles", deps=["m_chalk"], xp=40,
      optional=True, tokens=1, subtitle="Optional: steady the circle", desc=[
        "&eWhat:&r large candles placed in a pentacle steady it, so summoned spirits last longer before they fade.",
        "&eChemistry:&r tallow is rendered animal fat: triglycerides of stearic, palmitic and oleic acid, the stuff of the first candles.",
        "&eHow:&r kill pigs, cows or sheep with the Butcher Knife (iron and sticks) for tallow, then a string over tallow makes a candle.",
        "&eTip:&r the Dictionary's pentacle pages show where candles go."]),
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
    Q("oc_goggles", 12, 3, [item("occultism:otherworld_goggles")], "Otherworld Goggles", deps=["oc_purple_chalk"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the Third Eye without the fruit", desc=[
        "&eWhat:&r the goggles give a permanent Third Eye, and show even more hidden blocks than Demon's Dream does.",
        "&eHow:&r lenses (glass panes and an attuned gem) become infused lenses in a foliot ritual with 2 silver and gold; add a lens frame (otherstone and silver) and leather.",
        "&eTip:&r goggles let you see, not harvest: you still need the infused or iesnium pickaxe."]),
    Q("oc_divination", 2, -3, [item("occultism:divination_rod")], "Divination Rod", deps=["oc_attuned_gem"], xp=40,
      optional=True, tokens=1, subtitle="Optional: dowse for the Otherworld", desc=[
        "&eWhat:&r the rod points toward otherworld blocks such as otherstone and otherworld trees.",
        "&eHow:&r gold ingots, glass and a spirit-attuned gem. Use it as the Dictionary explains to pick a target.",
        "&eTip:&r handy for finding an otherworld grove before you have saplings."]),

    # --- Djinni utilities and storage (y=1.5 .. 4.5) ------------------------------------------
    Q("oc_manage_machine", 18, 1.5, [item("occultism:book_of_calling_djinni_manage_machine")], "Machine Operator", deps=["oc_djinni"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a djinni that runs a machine", desc=[
        "&eWhat:&r the djinni Machine Operator keeps a linked machine fed from your Storage Actuator and returns the results.",
        "&eHow:&r djinni summoning ritual with a coal block, gold, iron and a furnace. Use its Book of Calling on the storage and the machine.",
        "&eTip:&r it's a light autocrafting option before AE2."]),
    Q("oc_matrix", 18, 3, [item("occultism:dimensional_matrix")], "Dimensional Matrix", deps=["oc_djinni"], xp=75,
      subtitle="The heart of Occultism storage", desc=[
        "&eWhat:&r the Dimensional Matrix binds a djinni to hold items in a pocket dimension.",
        "&eChemistry:&r the quartz it needs is SiO₂, the same crystal that keeps time in a real watch by vibrating at a fixed frequency.",
        "&eHow:&r a djinni crafting ritual with three quartz blocks and an ender pearl."]),
    Q("oc_storage", 20, 3, [item("occultism:storage_controller")], "Storage Actuator", deps=["oc_matrix"], xp=150, size=1.5,
      subtitle="A whole warehouse in one block", desc=[
        "&eWhat:&r the Dimensional Storage Actuator stores thousands of items and shows them in one searchable screen.",
        "&eHow:&r a foliot ritual makes the Storage Actuator Base (otherstone pedestal, 2 copper, gold). Put the matrix on top of the base in a crafting grid.",
        "&eTip:&r it's an alternative to AE2 for early storage. Stabilizers expand it."]),
    Q("oc_stabilizer", 22, 3, [item("occultism:storage_stabilizer_tier1", 2)], "Storage Stabilizers", deps=["oc_storage"], xp=75,
      subtitle="More room for the warehouse", desc=[
        "&eWhat:&r stabilizers pointed at the Actuator raise how many items and item types it holds.",
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
    Q("oc_remote", 20, 4.5, [item("occultism:storage_remote")], "Storage Remote", deps=["oc_storage"], xp=75,
      optional=True, tokens=1, subtitle="Optional: your storage in your pocket", desc=[
        "&eWhat:&r opens your Storage Actuator from anywhere.",
        "&eHow:&r a djinni ritual with an inert remote (iesnium nuggets, an attuned gem, an otherstone tablet, silver), two ender pearls and quartz. Link it by clicking the Actuator.",
        "&eTip:&r one remote per player saves a lot of walking back to base."]),
    Q("oc_wormhole", 22, 4.5, [item("occultism:stable_wormhole")], "Stable Wormhole", deps=["oc_storage"], xp=50, optional=True, tokens=1,
      subtitle="Optional: a second door into storage", desc=[
        "&eWhat:&r a Stable Wormhole links to your Storage Actuator so you can open it from another room.",
        "&eHow:&r foliot crafting ritual: an otherstone frame, an ender pearl, 2 quartz and 2 gold ingots. Link it to the Actuator.",
        "&eTip:&r put one beside each crafting area."]),
    Q("oc_soulgem", 16, 3, [item("occultism:soul_gem")], "Soul Gem", deps=["oc_djinni"], xp=75,
      optional=True, tokens=1, subtitle="Optional: carry a mob around", desc=[
        "&eWhat:&r a Soul Gem traps a living creature so you can move it and release it elsewhere.",
        "&eHow:&r a djinni ritual: a diamond, copper, silver and gold ingots, a fragile soul gem and 3 soul sand or soil.",
        "&eTip:&r it's the easy way to move villagers or animals to your base."]),
    Q("oc_ring", 16, 4.5, [item("occultism:familiar_ring")], "Familiar Ring", deps=["oc_soulgem"], xp=100,
      optional=True, tokens=1, subtitle="Optional: wear your familiar", desc=[
        "&eWhat:&r familiars are summoned with rituals (greedy, bat, beaver, deer, blacksmith...). The ring stores one so it travels with you.",
        "&eHow:&r a djinni ritual with a soul gem, two gold and two silver ingots. Capture your familiar with it.",
        "&eTip:&r the Greedy Familiar picks up items for you. The Dictionary lists what each familiar does."]),

    # --- The afrit (y=-3 .. -4.5) ---------------------------------------------------------------
    Q("oc_afrit", 18, -3, [item("occultism:book_of_binding_bound_afrit")], "Bind an Afrit", deps=["oc_djinni"], xp=150,
      subtitle="A spirit of fire", desc=[
        "&eWhat:&r afrits are the third rank of spirits. They power stronger rituals and the deep-mining miner.",
        "&eHow:&r a Book of Binding with yellow dye, bound with the spirit's name (see the Dictionary).",
        "&eTip:&r afrit rituals need afrit essence, which only an unbound afrit drops."]),
    Q("oc_gray_chalk", 18, -4.5, [item("occultism:chalk_gray")], "Gray Chalk", deps=["oc_djinni"], xp=50,
      subtitle="A stronger foundation", desc=[
        "&eWhat:&r gray chalk is the foundation colour of afrit pentacles.",
        "&eHow:&r impure white chalk with gray paste (a djinni ritual: gunpowder, clay, a phantom membrane and gray dye), purified in spiritfire.",
        "&eTip:&r gray, light gray and black chalk can stand in for white in most pentacles."]),
    Q("oc_orange_chalk", 20, -4.5, [item("occultism:chalk_orange")], "Orange Chalk", deps=["oc_djinni"], xp=60,
      subtitle="Sweet bait for an afrit", desc=[
        "&eWhat:&r orange chalk lures afrits. It doesn't control them; that takes red chalk.",
        "&eHow:&r impure white chalk with cursed honey, glow berries and blaze dust. Cursed honey drops from a possessed bee (djinni possession with honey items and a chicken).",
        "&eTip:&r Ihagan's Enthrallment, the djinni possession pentacle, is white, light gray, lime and gold."]),
    Q("oc_afrit_wild", 20, -3, [kill("occultism:afrit_wild")], "Unbound Afrit", deps=["oc_afrit", "oc_gray_chalk", "oc_orange_chalk"], xp=300, loot="boss",
      size=1.5, shape="hexagon", subtitle="Summon a wild afrit and defeat it", desc=[
        "&6You remember fire that obeyed. This one remembers being free.&r",
        "&eWhat:&r the Summon Unbound Afrit ritual calls a hostile afrit. It drops afrit essence when killed.",
        "&eHow:&r Kandar's Open Conjure (white, gray, lime, orange, skulls and a spirit-attuned crystal). Netherrack, an iesnium ingot, flint and steel and gunpowder, plus a cow as the sacrifice.",
        "&eTip:&r fire resistance potions turn this from a disaster into a fair fight. Build far from anything flammable."]),
    Q("oc_red_chalk", 22, -3, [item("occultism:chalk_red")], "Red Chalk", deps=["oc_afrit_wild"], xp=75,
      subtitle="Command an afrit", desc=[
        "&eWhat:&r red chalk is made from afrit essence and lets your pentacles bind afrits instead of just calling them.",
        "&eHow:&r impure white chalk with afrit essence, a torchflower and redstone dust, purified in spiritfire.",
        "&eTip:&r Sevira's Permanent Confinement (the afrit crafting pentacle) uses red, orange, lime, purple, gray and white."]),
    Q("oc_wildhunt", 22, -4.5, [kill("occultism:wild_hunt_wither_skeleton", 5)], "The Wild Hunt", deps=["oc_afrit_wild", "t2_nether"], xp=150,
      loot="hunt", optional=True, tokens=1, subtitle="Optional: kill 5 Wild Hunt wither skeletons", desc=[
        "&eWhat:&r the Wild Hunt ritual calls a pack of wither skeletons with a good chance of dropping wither skeleton skulls.",
        "&eHow:&r Osorin's Unbound Calling (green, light blue and pink chalk; check the Dictionary). Activated with a skeleton skull; copper, silver and gold blocks, a diamond, netherrack and soul sand, plus a sacrifice.",
        "&eTip:&r the easiest way to collect three skulls for the Wither, and the skulls marid pentacles need."]),

    # --- The marid (y=-3 .. -4.5) ---------------------------------------------------------------
    Q("oc_black_chalk", 24, -3, [item("occultism:chalk_black")], "Black Chalk", deps=["oc_red_chalk"], xp=75,
      subtitle="Witherite and netherite", desc=[
        "&eWhat:&r black chalk is the strongest foundation chalk; marid pentacles need it.",
        "&eChemistry:&r real witherite is barium carbonate, BaCO₃, named after the 18th-century chemist William Withering. It has nothing to do with the Wither.",
        "&eHow:&r impure white chalk with 3 witherite dust. Witherite dust is an afrit ritual: netherite dust, a wither skeleton skull, blackstone dust and a wither rose.",
        "&eTip:&r netherite dust comes from crushing a netherite ingot, so save one."]),
    Q("oc_marid", 24, -4.5, [item("occultism:book_of_binding_bound_marid")], "Bind a Marid", deps=["oc_red_chalk"], xp=150,
      subtitle="The highest spirit you can name", desc=[
        "&eWhat:&r marids are the fourth and strongest rank of spirits.",
        "&eHow:&r a Book of Binding with green dye, bound with a name like the others.",
        "&eTip:&r like the afrit, its essence only comes from an unbound one."]),
    Q("oc_marid_wild", 26, -3, [kill("occultism:marid_unbound")], "Unbound Marid", deps=["oc_black_chalk", "oc_marid"], xp=400, loot="boss",
      size=1.5, shape="hexagon", subtitle="Summon a wild marid and survive", desc=[
        "&6You remember the sea answering you. This spirit answers to no one.&r",
        "&eWhat:&r the unbound marid is hostile and very strong. It drops marid essence.",
        "&eHow:&r Tibira's Attraction (black, red, orange, lime and white chalk, wither skulls and a crystal). A conduit, prismarine crystals, a prismarine shard and a ghast tear; use a trident to start it.",
        "&eTip:&r bring your best armor and healing, and don't do it at home."]),
    Q("oc_blue_chalk", 28, -3, [item("occultism:chalk_blue")], "Blue Chalk", deps=["oc_marid_wild"], xp=75,
      subtitle="Command a marid", desc=[
        "&eWhat:&r blue chalk, made from marid essence, lets pentacles control marids.",
        "&eChemistry:&r tube coral builds its skeleton from calcium carbonate (aragonite), the same CaCO₃ as your chalk.",
        "&eHow:&r impure white chalk with marid essence, lapis dust and tube coral, purified in spiritfire.",
        "&eTip:&r Uphyxes' Inverted Tower, the marid crafting pentacle, makes the master miner and tier 4 stabilizers."]),

    # --- ATM10-aligned additions (2026-10-19): tools of the trade --------------------------------
    Q("oc_brush", 0, 0, [item("occultism:brush")], "Chalk Brush", deps=["m_chalk"], xp=20,
      optional=True, tokens=1, subtitle="Optional: clean up after a ritual", desc=[
        "&eWhat:&r right-click chalk glyphs with the brush to wipe them away much faster than breaking them.",
        "&eChemistry:&r chalk, CaCO₃, fizzes away in acid: CaCO₃ + 2HCl → CaCl₂ + H₂O + CO₂. A brush is gentler.",
        "&eHow:&r three planks over two wool and a string."]),
    Q("oc_crystal", 0, 0, [item("occultism:spirit_attuned_crystal")], "Spirit-Attuned Crystal", deps=["oc_attuned_gem"], xp=40,
      optional=True, tokens=1, subtitle="Optional: four gems, one anchor", desc=[
        "&eWhat:&r the crystal anchors bigger pentacles and goes into the mineshaft, miners and the afrit and marid circles.",
        "&eChemistry:&r a real crystal is a lattice that repeats in three dimensions; four small gems pressed together would only be a polycrystal.",
        "&eHow:&r four spirit-attuned gems in a 2×2 grid.",
        "&eTip:&r make two: the mineshaft and the djinni miner each need one."]),
    Q("oc_iesnium_pick", 0, 0, [item("occultism:iesnium_pickaxe"), item("occultism:iesnium_block")], "Iesnium Tools", deps=["m_iesnium"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the pickaxe every miner needs", desc=[
        "&eWhat:&r the iesnium pickaxe mines otherworld blocks and is an ingredient of every miner spirit. The block goes into the Dimensional Mineshaft.",
        "&eHow:&r pickaxe: 3 iesnium ingots over 2 sticks. Block: 9 ingots.",
        "&eTip:&r you'll want a spare pickaxe for each miner upgrade."]),
    Q("oc_ritual_satchel", 0, 0, [item("occultism:ritual_satchel_t1")], "Apprentice Ritual Satchel", deps=["oc_purple_chalk"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a foliot draws your pentacles", desc=[
        "&eWhat:&r fill the satchel with chalks, candles, skulls and crystals; preview a pentacle in the Dictionary and the foliot places the pieces for you.",
        "&eHow:&r a foliot crafting ritual: a hopper, a dispenser, 2 wool, 2 leather, string and a silver ingot.",
        "&eTip:&r chalks are used up by durability, so keep spares inside."]),
    Q("oc_ritual_satchel_t2", 0, 0, [item("occultism:ritual_satchel_t2")], "Artisanal Ritual Satchel", deps=["oc_ritual_satchel", "oc_red_chalk"], xp=100,
      optional=True, tokens=1, subtitle="Optional: an afrit sets the whole circle at once", desc=[
        "&eWhat:&r the afrit version places a whole pentacle in one click, and can also pick one up again: chalk, candles and all.",
        "&eHow:&r an afrit upgrade ritual: the apprentice satchel, afrit essence and 4 ender pearls (it keeps the contents).",
        "&eTip:&r right-click the golden bowl with it to clear an intact pentacle."]),
    Q("oc_iesnium_anvil", 0, 0, [item("occultism:iesnium_anvil")], "Iesnium Anvil", deps=["oc_blue_chalk"], xp=150,
      optional=True, tokens=2, subtitle="Optional: an anvil a marid helps you pay for", desc=[
        "&eWhat:&r an unbreakable anvil that can go one level past an enchantment's maximum, and the marid pays half the level cost.",
        "&eHow:&r a marid crafting ritual: an anvil, 3 iesnium blocks and marid essence.",
        "&eTip:&r pair it with the Enchantment Library from Apotheosis for top-level books."]),
    Q("oc_rainbow", 0, 0, [item("occultism:chalk_rainbow")], "Rainbow Chalk", deps=["oc_blue_chalk"], xp=200,
      optional=True, tokens=2, subtitle="Optional: one chalk for every glyph", desc=[
        "&6You remember not needing a circle at all. This is the next best thing.&r",
        "&eWhat:&r rainbow chalk can stand in for any coloured chalk glyph and takes on its look.",
        "&eChemistry:&r chalk colours come from pigments; the oldest, like red ochre (Fe₂O₃), are iron oxides people have used for 100,000 years.",
        "&eHow:&r the eldritch pentacle with 12 coloured chalks, a sheep as the sacrifice and the brush to start it. The Dictionary shows the circle and the full list."]),
], links=[("gs_iron", -2, 0), ("t2_nether", 20, -1.5)])
