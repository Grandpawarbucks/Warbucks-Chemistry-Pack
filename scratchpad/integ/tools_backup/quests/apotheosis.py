"""Quest chapter: apotheosis. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors two ATM10 chapters on one page (structure and item list only; every word here is ours):
- "apotheosis_gear" (gems, sigils, salvaging, reforging, world tiers, tiered gateways): those quests carry mirror=.
- "apotheosis_2" (Apothic Spawners: runes, capturing, other mods' spawners): section names only, no mirror=
  (Q(mirror=) only takes ids from this chapter's own stem, apotheosis_gear).
Enchanting now has its own page (tools/quests/apothic_enchanting.py); the older enchanting quests below stay here
as optional side quests (keys never change).
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

GEMS, SIGILS, SALVAGE, REFORGE, TIERS, GATES = "Gems", "Sigils", "Salvaging", "Reforging", "World Tiers", "Apothic Gateways"
SPAWN, RUNES, INFUSED, CAPTURE, OTHER = "Spawners", "Spawner Runes", "Infused Runes", "Choosing the Mob", "Other Spawners"
LOOT, ENCH = "Affix Loot", "Old Enchanting Notes"


def mat(key, id_, title, subtitle, what, how, tip, mirror, optional=True, xp=40):
    """One rarity material, salvaged from affixed gear of that rarity (ATM10: one quest per material)."""
    return Q(key, 0, 0, [item(id_)], title, deps=["m_salvage"], xp=xp, subtitle=subtitle, mirror=mirror,
             optional=optional, tokens=1 if optional else None, desc=[
        "&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip])


def tier(key, title, subtitle, what, how, tip, deps, mirror, optional=False, xp=75, icon="apotheosis:boss_summoner", **kw):
    """A world tier milestone. Unlocked by an Apotheosis advancement; the player ticks it off."""
    return Q(key, 0, 0, [tick()], title, deps=deps, xp=xp, subtitle=subtitle, mirror=mirror, icon=icon,
             optional=optional, tokens=1 if optional else None, desc=[
        "&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip], **kw)


def rune(key, id_, title, subtitle, what, how, tip, deps, xp=50):
    """One spawner rune: right-click a placed spawner with it (ATM10 apotheosis_2, no mirror id)."""
    return Q(key, 0, 0, [item(id_)], title, deps=deps, xp=xp, optional=True, tokens=1, subtitle=subtitle, desc=[
        "&eWhat:&r " + what, "&eHow:&r " + how, "&eTip:&r " + tip])


CHAPTER = Chapter("apotheosis", "Apotheosis", "apotheosis:gem_dust",
        ["Affix loot, gems, sigils, world tiers, spawners and Gateways."], SIDE, [
    # === ATM10 apotheosis_gear ===============================================================================
    # --- Gems ------------------------------------------------------------------------------------------------
    Q("ap_gem", 0, 0, [item("apotheosis:gem")], "A Gem in the Rough", deps=["gs_iron"], xp=50, size=2.0, shape="gear",
      section=GEMS, mirror="3BF5B8DE7A1CC4D7", subtitle="Find any Apotheosis gem", desc=[
        "&6You remember gear that remembered you back. Mortal gear can learn, if you teach it.&r",
        "&eWhat:&r Apotheosis gems drop from monsters and chests. Each one carries a bonus that you can set into a socket on your gear.",
        "&eHow:&r fight, loot and read the tooltip of anything that glitters. Any gem completes this quest.",
        "&eTip:&r gems come in purities, from cracked to perfect. Better purity, bigger bonus."]),
    Q("m_gems", 0, 3, [item("apotheosis:gem_dust", 4)], "Gem Dust", deps=["ap_gem"], xp=30, mirror="45647395169978ED",
      subtitle="The currency of Apotheosis", desc=[
        "&eWhat:&r gem dust builds almost every Apotheosis table, sigil and rune.",
        "&eHow:&r crush spare gems into gem dust (JEI shows how).",
        "&eTip:&r keep good gems for sockets and crush the rest."]),
    Q("ap_smithing", 0, 0, [item("minecraft:smithing_table")], "Setting a Gem", deps=["m_gems"], xp=30,
      mirror="7C90008081DEBECA", subtitle="Sockets are filled at the smithing table", desc=[
        "&eWhat:&r the smithing table is where Apotheosis puts gems into sockets and applies sigils to gear.",
        "&eHow:&r 4 planks and 2 iron ingots. Put the gear in, then the gem or sigil.",
        "&eTip:&r a socketed gem is locked in until a Sigil of Withdrawal pulls it out."]),
    Q("m_gem_cut", 6, 3, [item("apotheosis:gem_cutting_table")], "Gem Cutting", deps=["m_gems"], xp=50, mirror="166CE4243896A0CD",
      subtitle="Combine gems into higher purities", desc=[
        "&eWhat:&r the Gem Cutting Table upgrades gems to higher purity using matching gems and dust.",
        "&eChemistry:&r real gems are cut along cleavage planes, flat directions where the crystal's bonds are weakest.",
        "&eHow:&r smooth stone, shears, planks and gem dust."]),

    # --- Sigils -----------------------------------------------------------------------------------------------
    Q("ap_slate", 0, 0, [item("apotheosis:gem_fused_slate", 8)], "Gem-Fused Slate", deps=["m_gems"], xp=30, section=SIGILS,
      mirror="6667638252DB9C74", optional=True, tokens=1, subtitle="Optional: the base of every sigil", desc=[
        "&eWhat:&r gem-fused slate is the backing for sigils and spawner runes.",
        "&eChemistry:&r deepslate is metamorphic rock: older stone squeezed and heated deep underground until its minerals recrystallised.",
        "&eHow:&r 8 deepslate around 1 gem dust makes 8."]),
    Q("m_socket", 7, 4.5, [item("apotheosis:sigil_of_socketing")], "Sigil of Socketing", deps=["ap_slate"], xp=60,
      mirror="24D11ED5F4EEDC48", optional=True, tokens=1, subtitle="Optional: add a socket to any gear", desc=[
        "&eWhat:&r adds a socket to gear in a smithing table, so you can slot in a gem.",
        "&eHow:&r gem-fused slate, an amethyst shard, gunpowder and gem dust (makes 3).",
        "&eTip:&r a Sigil of Withdrawal pulls gems back out later."]),
    Q("ap_unnaming", 0, 0, [item("apotheosis:sigil_of_unnaming")], "Sigil of Unnaming", deps=["ap_slate"], xp=30,
      mirror="4E9DDDBD8263D0E3", optional=True, tokens=1, subtitle="Optional: wipe an affix name", desc=[
        "&eWhat:&r removes the long generated name from an affixed item, so it goes back to its plain name.",
        "&eHow:&r 6 slate around 3 flint makes 6. Apply it at the smithing table.",
        "&eTip:&r a name tag afterwards lets you call the sword whatever you like."]),
    Q("ap_withdraw", 7, 6, [item("apotheosis:sigil_of_withdrawal")], "Sigil of Withdrawal", deps=["ap_slate"], xp=50,
      mirror="7CB03F92F9ECEFFB", optional=True, tokens=1, subtitle="Optional: get your gems back", desc=[
        "&eWhat:&r pulls every gem out of an item without destroying them, so a good gem can move to new gear.",
        "&eHow:&r gem-fused slate, blaze rods, ender pearls, a lava bucket and gem dust (makes 4).",
        "&eTip:&r withdraw gems before salvaging or reforging old gear."]),
    Q("ap_enhance", 11, 4.5, [item("apotheosis:sigil_of_enhancement")], "Sigil of Enhancement", deps=["ap_slate"], xp=200,
      mirror="2002C7EB13626AE7", optional=True, tokens=2, subtitle="Optional: raise a gem's rarity", desc=[
        "&eWhat:&r upgrades a socketed gem to the next rarity at the Reforging Table.",
        "&eHow:&r gem-fused slate, gem dust and a godforged pearl (makes 4). Godforged pearls come from salvaging mythic gear.",
        "&eTip:&r save these for gems you'll keep: a mythic gem in endgame gear is worth it."]),
    Q("ap_sigils", 0, 0, [item("apotheosis:sigil_of_rebirth")], "Sigil of Rebirth", deps=["ap_slate"], xp=40,
      mirror="38956DC28E317DEF", optional=True, tokens=1, subtitle="Optional: fuel for reforging", desc=[
        "&eWhat:&r the Sigil of Rebirth is spent at the Reforging Table each time you reroll an item.",
        "&eHow:&r 6 slate around 3 gem dust makes 6.",
        "&eTip:&r make them in bulk before a long reforging session."]),
    Q("ap_malice", 0, 0, [item("apotheosis:sigil_of_malice")], "Sigil of Malice", deps=["ap_slate"], xp=75,
      mirror="552BA5E6FA987256", optional=True, tokens=1, loot="hunt", subtitle="Optional: taken from an Apothic Invader", desc=[
        "&eWhat:&r a sigil with no crafting recipe. It feeds the highest gateway and spawner upgrade recipes.",
        "&eHow:&r Apothic Invaders (named bosses from World Tier: Frontier on) sometimes drop one. Check JEI for its uses.",
        "&eTip:&r invaders hit very hard. Fight them where you can retreat."]),

    # --- Salvaging and rarity materials ------------------------------------------------------------------------
    Q("m_salvage", 4, 3, [item("apotheosis:salvaging_table")], "Salvaging", deps=["m_gems", "ap_smithing"], xp=60,
      size=1.5, shape="hexagon", section=SALVAGE, mirror="1CD05CB4A3DB112A", subtitle="Junk gear into rarity materials", desc=[
        "&eWhat:&r the Salvaging Table breaks affixed gear into materials of its rarity.",
        "&eHow:&r a smithing table, an iron pickaxe and axe, copper, a lava bucket and gem dust.",
        "&eTip:&r every affixed sword you don't want is a reforge for one you do."]),
    mat("ap_scrap", "apotheosis:mysterious_scrap_metal", "Mysterious Scrap Metal", "Common: from grey gear",
        "the salvage of common (grey) affix gear, used in common-tier reforging.",
        "salvage any common affixed item.", "common gear drops everywhere, so this piles up first.", "16C74B5F99AD6724"),
    mat("ap_fabric", "apotheosis:timeworn_fabric", "Timeworn Fabric", "Uncommon: from green gear",
        "the salvage of uncommon (green) gear. The Frontiersman's spawner upgrade rune uses it too.",
        "salvage uncommon affixed gear.", "sort loot by colour before salvaging; each rarity has its own material.", "0089A394566B0F3B"),
    Q("ap_rarity", 4, 1.5, [item("apotheosis:luminous_crystal_shard", 4)], "Luminous Crystal", deps=["m_salvage"], xp=60,
      mirror="001C1881E9289566", subtitle="Rare: from blue gear", optional=True, tokens=1, desc=[
        "&eWhat:&r luminous crystal shards are the salvage of rare (blue) gear.",
        "&eHow:&r salvage rare gear in the Salvaging Table until you have 4 shards.",
        "&eTip:&r the Wayfarer's spawner upgrade rune is built on these."]),
    mat("ap_pearl", "apotheosis:godforged_pearl", "Godforged Pearl", "Mythic: from orange gear",
        "the salvage of mythic gear, the rarest material: augmenting, enhancement sigils and the top runes need it.",
        "salvage mythic gear. It drops in high world tiers, from tiered gateways and from the toughest elites.",
        "never salvage a mythic item you would rather wear; check its affixes first.", "099C2A9B9CA138F8", xp=100),
    mat("ap_sands", "apotheosis:arcane_sands", "Arcane Sands", "Epic: from purple gear",
        "the salvage of epic (purple) gear. The full Reforging Table needs it.",
        "salvage epic affixed gear.", "keep a few stacks; reforging epic gear spends them fast.", "6EF206A0BD5BAC0A",
        optional=False, xp=60),

    # --- Reforging ----------------------------------------------------------------------------------------------
    Q("m_simple_reforge", 2, 3, [item("apotheosis:simple_reforging_table")], "Simple Reforging", deps=["m_gems"], xp=40,
      section=REFORGE, mirror="29EA8E178F8F8FDB", subtitle="Reroll an item's affixes", desc=[
        "&eWhat:&r the Simple Reforging Table rerolls affixes on gear of lower rarities.",
        "&eHow:&r an enchanting table, iron, smooth stone and gem dust.",
        "&eTip:&r reforging costs rarity materials; salvage junk gear to get them."]),
    Q("m_apoth", 8, 3, [item("apotheosis:reforging_table")], "Divine Reforging", deps=["ap_sands", "m_simple_reforge", "t2_nether"],
      xp=100, mirror="1403D677CF2815C3", subtitle="Reforge any rarity, up to mythic", desc=[
        "&6You remember weapons that chose their wielders. These at least choose good affixes.&r",
        "&eWhat:&r the full Reforging Table handles every rarity, up to mythic gear.",
        "&eHow:&r the Simple Reforging Table, a netherite ingot, nether bricks and arcane sands."]),
    Q("m_augment", 9, 4.5, [item("apotheosis:augmenting_table")], "Augmenting", deps=["ap_enhance", "ap_pearl"], xp=200,
      mirror="57BB2CC6D9D2AE87", optional=True, tokens=2, subtitle="Optional: upgrade and reroll single affixes", desc=[
        "&eWhat:&r the Augmenting Table improves or rerolls one affix at a time.",
        "&eHow:&r an enchanting table, a Nether Star, 2 godforged pearls and polished blackstone.",
        "&eTip:&r save it for gear you plan to keep for the rest of the game."]),

    # --- World tiers ----------------------------------------------------------------------------------------------
    tier("ap_tiers", "World Tiers", "Harder world, better loot",
         "Apotheosis splits the game into five world tiers: Haven, Frontier, Ascent, Summit and Pinnacle. Higher tiers make monsters stronger and loot better, and raise the cap on enchanting power.",
         "press CTRL+T to open the World Tier screen. Hover a tier to see what unlocks it; activate it once unlocked. Click the checkmark when you've looked.",
         "you can step back down to an easier tier at any time.", ["ap_gem"], "196312DF0D2E2CB6", xp=25,
         size=1.5, shape="hexagon", section=TIERS),
    tier("ap_tier_haven", "Haven", "Pick up your first affix item",
         "Haven is the starting tier. It unlocks when you pick up any affixed item. Enchanting power is capped at 30 Eterna here.",
         "find an affixed item (a coloured name). Click the checkmark when the advancement pops.",
         "Haven is the tier to learn the systems in.", ["ap_tiers"], "377A41499D8218C9", xp=25, icon="minecraft:oak_sapling"),
    tier("ap_tier_frontier", "Frontier", "A full set of affix gear",
         "Frontier unlocks when you wear affixed armour in all four slots and hold an affixed weapon. Apothic Invaders start to appear, and the Eterna cap rises to 45.",
         "equip any affixed helmet, chestplate, leggings, boots and weapon, then activate Frontier (CTRL+T). Click the checkmark.",
         "45 Eterna is what the infused shelves need (Apothic Enchanting page).", ["ap_tier_haven"], "2A032EC573B5316C"),
    tier("ap_tier_ascent", "Ascent", "Uncommon gear and one Invader",
         "Ascent needs a full set of uncommon (green) or better gear and one Apothic Invader killed. The Eterna cap rises to 60.",
         "upgrade every slot to uncommon or better, kill an invader, then activate Ascent. Click the checkmark.",
         "invaders announce themselves; fight them near a bed.", ["ap_tier_frontier"], "1D1FAA2F86695781", xp=100),
    tier("ap_tier_summit", "Summit", "Rare gear and the Wither",
         "Summit needs a full set of rare (blue) or better gear and a dead Wither. The Eterna cap rises to 75.",
         "gear up in rare affixes, summon and kill the Wither, then activate Summit. Click the checkmark.",
         "fight the Wither underground or in a bunker: it breaks most blocks around it.", ["ap_tier_ascent"], "097FDC136BC843A7",
         optional=True, xp=150, loot="boss"),
    tier("ap_tier_pinnacle", "Pinnacle", "Epic gear and a free End",
         "Pinnacle, the top tier, needs a full set of epic (purple) gear and the Ender Dragon killed. Enchanting power is uncapped (100 Eterna).",
         "wear epic or better in every slot, beat the dragon, then activate Pinnacle. Click the checkmark.",
         "this is where mythic gear and godforged pearls start to flow.", ["ap_tier_summit"], "7EF873DCEB3B9D48",
         optional=True, xp=250, size=1.5, shape="hexagon"),

    # --- Apothic gateways -------------------------------------------------------------------------------------------
    Q("ap_gate_tiered", 0, 0, [tick()], "Tiered Gateways", deps=["ap_tier_frontier", "ap_gate"], xp=100, section=GATES,
      mirror="22E57BF23B9BA2C5", icon="gateways:gate_pearl", optional=True, tokens=1, loot="hunt",
      subtitle="Optional: a gate that matches your world tier", desc=[
        "&eWhat:&r Apotheosis adds one gateway per world tier (Frontier, Ascent, Summit, Pinnacle). Each opens only in its own tier and pays out affix gear.",
        "&eHow:&r the Frontier pearl is spider eyes, iron, bones, an ender pearl and rotten flesh. JEI lists the others. Open and close one, then click the checkmark.",
        "&eTip:&r the Pinnacle gate needs Sigils of Malice and a Warden Tendril."]),
    Q("ap_gate_endless", 0, 0, [tick()], "The Endless Gateway", deps=["ap_gate_tiered", "ap_tier_pinnacle"], xp=200,
      mirror="6B5B01C612951BAF", icon="gateways:gate_pearl", optional=True, tokens=2, loot="boss",
      subtitle="Optional: invaders that never stop", desc=[
        "&eWhat:&r the Endless Gateway of Apothic Invaders sends wave after wave of invaders until you fall or walk away.",
        "&eHow:&r its pearl is a reward from the Pinnacle gateway. Open it, survive as long as you can, then click the checkmark.",
        "&eTip:&r the deeper you go, the better the payout. Bring totems."]),
    Q("ap_supremacy", 0, 0, [item("apotheosis:sigil_of_supremacy")], "Sigil of Supremacy", deps=["ap_gate_endless"], xp=300,
      mirror="2E5E129F25707C5D", size=1.5, shape="hexagon", optional=True, tokens=2,
      subtitle="Optional: the Endless Gateway's prize", desc=[
        "&6You remember standing where nothing could follow. It was lonely, and you liked it.&r",
        "&eWhat:&r the rarest sigil, paid out deep in the Endless Gateway. Check JEI for what it unlocks.",
        "&eHow:&r keep the endless gate going until it drops.",
        "&eTip:&r the gateway's reward list in JEI shows which wave it starts at."]),

    # --- Affix loot and Gateways (ours, not in ATM10) -----------------------------------------------------------------
    Q("ap_hunt", 0, 1.5, [kill("minecraft:zombie", 50)], "Elite Hunting", deps=["gs_iron"], xp=75, loot="hunt", section=LOOT,
      subtitle="Kill 50 zombies and watch for affix gear", optional=True, tokens=1, desc=[
        "&eWhat:&r Apotheosis gives some monsters affixed gear and makes rare elites with a coloured name. Their drops can roll affixes and sockets.",
        "&eHow:&r kill 50 zombies. Pick up any named or glowing item they drop and read its tooltip.",
        "&eTip:&r elites hit hard. Gear up before poking one with a stick."]),
    Q("ap_charm", 2, 1.5, [item("apotheosis:potion_charm")], "Potion Charm", deps=["m_gems", "t2_brewing"], xp=60, optional=True, tokens=1,
      subtitle="Optional: a potion that never runs out (almost)", desc=[
        "&eWhat:&r a Potion Charm holds a potion effect and applies it while switched on, using durability.",
        "&eChemistry:&r blaze powder is a reactive powder; here it fixes the potion so it lasts, a bit like a preservative.",
        "&eHow:&r three identical potions in the middle row and six blaze powder around them. Infusing it later makes it permanent (check JEI).",
        "&eTip:&r Night Vision or Haste charms are the most useful early."]),
    Q("ap_gate", 6, 1.5, [item("gateways:gate_pearl")], "Gate Pearl", deps=["t2_nether"], xp=75,
      subtitle="Gateways to Eternity: a wave-based arena", desc=[
        "&eWhat:&r a Gate Pearl opens a Gateway that releases waves of a chosen mob. Beat every wave for rewards.",
        "&eHow:&r the Blaze gate is five blaze rods, an ender pearl and three nether bricks. Apotheosis adds tiered gates (Frontier and up); JEI shows them all.",
        "&eTip:&r a gate is a controlled mob farm: blaze rods, ender pearls and XP on demand."]),
    Q("ap_gate_close", 8, 1.5, [tick()], "Close a Gateway", deps=["ap_gate"], xp=100, loot="hunt",
      subtitle="Survive every wave", optional=True, tokens=1, desc=[
        "&eWhat:&r the gateway closes when every wave is defeated and pays out its reward.",
        "&eHow:&r throw the pearl in an open area, stay close (leaving fails the gate) and kill each wave. Click the checkmark when it closes.",
        "&eTip:&r tiered Apotheosis gates hand out affix gear and rarity materials."]),
    Q("ap_gem_case", 0, 0, [item("apotheosis:gem_case")], "Gem Case", deps=["m_gem_cut"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a display case that upgrades gems", desc=[
        "&eWhat:&r a cabinet that stores gems by type and purity and can combine two of a kind into the next purity.",
        "&eChemistry:&r a ruby is corundum (Al₂O₃) with about 1% chromium. Less chromium and it's a pink sapphire.",
        "&eHow:&r glass on top, basalt around a Gem Cutting Table, and an ender chest below.",
        "&eTip:&r infused at the enchanting table it becomes the Gem Case of House Fabergé, which keeps the gems inside."]),
    Q("ap_rarity_all", 0, 0, [item("apotheosis:mysterious_scrap_metal"), item("apotheosis:timeworn_fabric"), item("apotheosis:arcane_sands"),
                              item("apotheosis:godforged_pearl")], "Every Rarity", deps=["ap_rarity"], xp=150,
      optional=True, tokens=2, subtitle="Optional: scrap, fabric, sands and a pearl", desc=[
        "&eWhat:&r one material of each other rarity: common scrap metal, uncommon timeworn fabric, epic arcane sands and a mythic godforged pearl.",
        "&eHow:&r salvage gear of each colour. The pearl only comes from mythic gear: tiered Gateways and the toughest elites.",
        "&eTip:&r Divine Reforging, upgrade runes and the strongest sigils all spend these."]),

    # === ATM10 apotheosis_2 (Apothic Spawners; no mirror ids) =========================================================
    Q("ap_spawner", 0, 0, [item("minecraft:spawner")], "Bottled Monsters", deps=["gs_iron"], xp=60, optional=True, tokens=1,
      size=1.5, shape="hexagon", section=SPAWN, subtitle="Optional: mine a spawner with Silk Touch", desc=[
        "&6You remember making monsters to order. Today you'll settle for moving one.&r",
        "&eWhat:&r with Apothic Spawners a monster spawner can be picked up with a Silk Touch pickaxe and moved home.",
        "&eHow:&r find one in a dungeon or mineshaft, light it up, then mine it with Silk Touch (it costs the pick 100 durability).",
        "&eTip:&r spawners are mob farms for drops you can't make chemically: bones, string, ender pearls, blaze rods."]),
    Q("ap_chain", 0, 0, [item("apotheosis:spawner_chain"), item("minecraft:tnt")], "Spawner Chains", deps=["ap_spawner"], xp=40,
      optional=True, tokens=1, subtitle="Optional: blow up a spawner", desc=[
        "&eWhat:&r spawner chains are the binding for spawner runes. They only come from a monster spawner destroyed by an explosion.",
        "&eChemistry:&r TNT (C₇H₅N₃O₆) carries its own oxygen in its nitro groups, so it burns in microseconds and makes a shock wave.",
        "&eHow:&r find a spawner you don't want to keep and blow it up with TNT. Pick up the chains, and bring a spare TNT for the quest.",
        "&eTip:&r keep the good spawners: Silk Touch them home instead."]),
    Q("ap_rune", 2, 0, [item("apotheosis:spawner_rune")], "Spawner Runes", deps=["ap_chain"], xp=75, optional=True, tokens=1,
      size=1.5, shape="hexagon", section=RUNES, subtitle="Optional: the blank every rune starts from", desc=[
        "&eWhat:&r a blank Spawner Rune. Crafted with one more ingredient it becomes a rune that rewrites a spawner's rules when you right-click the spawner with it.",
        "&eHow:&r gem dust, gem-fused slate and spawner chains (makes 2).",
        "&eTip:&r hold Shift over a placed spawner's tooltip, or look at it with Jade, to see its current stats."]),
    rune("ap_rune_burning", "apotheosis:burning_spawner_rune", "Rune of Immolation", "Optional: mobs spawn on fire",
         "spawned mobs are set alight, so they drop cooked meat and die faster.",
         "a Spawner Rune with 4 campfires around it.", "useless on Nether mobs, which don't burn.", ["ap_rune"]),
    rune("ap_rune_health", "apotheosis:initial_health_spawner_rune", "Rune of Debilitation", "Optional: mobs spawn weakened",
         "lowers the starting health of spawned mobs, so one hit finishes them.",
         "a Spawner Rune with 4 pointed dripstone around it.", "stack it a few times for a one-punch farm.", ["ap_rune"]),
    rune("ap_rune_youth", "apotheosis:youthful_spawner_rune", "Rune of Youth", "Optional: baby mobs only",
         "spawned mobs are babies wherever the mob has a baby form.",
         "a Spawner Rune with 4 turtle eggs around it.", "baby zombies are fast. You were warned.", ["ap_rune"]),
    rune("ap_rune_range", "apotheosis:spawn_range_spawner_rune", "Rune of Spawning Range", "Optional: a wider spawn area",
         "widens the area a spawner may place mobs in.",
         "a Spawner Rune with 4 pistons around it.", "use quartz in the off hand to shrink it again (see Opposite Day).", ["ap_rune"]),
    rune("ap_rune_light", "apotheosis:ignore_light_spawner_rune", "Rune of Perpetual Twilight", "Optional: spawns in any light",
         "the spawner ignores light levels, so a well-lit farm still runs.",
         "a Spawner Rune with 4 soul lanterns around it.", "light your farm fully: the spawner works, wild mobs don't spawn.", ["ap_rune"]),
    rune("ap_rune_redstone", "apotheosis:redstone_control_spawner_rune", "Rune of Control", "Optional: an off switch",
         "the spawner only runs while it gets a redstone signal.",
         "a Spawner Rune with 4 comparators around it.", "put it on every farm first, so you can switch it off.", ["ap_rune"]),
    Q("ap_quartz", 0, 0, [item("minecraft:quartz")], "Opposite Day", deps=["ap_rune"], xp=25, optional=True, tokens=1,
      subtitle="Optional: undo a spawner change", desc=[
        "&eWhat:&r with nether quartz in your off hand, using a rune or modifier on a spawner reverses its effect (turn Silence off, shrink the range, and so on).",
        "&eChemistry:&r quartz is silicon dioxide, SiO₂: the same compound as most sand and glass.",
        "&eHow:&r hold quartz in the off hand and the modifier in the main hand, then right-click the spawner.",
        "&eTip:&r JEI's spawner page lists every modifier and its inverse."]),
    rune("ap_rune_silent", "apotheosis:silent_spawner_rune", "Rune of Silence", "Optional: a quiet farm",
         "spawned mobs make no sound.", "a Spawner Rune with 4 wool around it.", "your ears will thank you.", ["ap_rune"]),
    Q("ap_rune_upgrade", 0, 0, [item("apotheosis:frontier_spawner_upgrade_rune")], "Frontiersman's Upgrade", deps=["ap_rune"], xp=75,
      optional=True, tokens=1, subtitle="Optional: a slightly better spawner", desc=[
        "&eWhat:&r the first of four upgrade runes: faster spawns and more mobs per spawn. The others are Wayfarer's, Mountaineer's and Thundering.",
        "&eHow:&r a Spawner Rune with timeworn fabric, clocks and flint.",
        "&eTip:&r upgrade runes match the world tiers, so each new tier opens the next rune."]),
    rune("ap_rune_ascent", "apotheosis:ascent_spawner_upgrade_rune", "Wayfarer's Upgrade", "Optional: a better spawner",
         "the second upgrade rune: a bigger step in spawn speed and count.",
         "a Spawner Rune with luminous crystal shards, quartz, a spawn egg and a Sigil of Socketing (check JEI).",
         "spawn eggs come from the Capturing enchantment (Choosing the Mob).", ["ap_rune"], xp=75),
    Q("ap_rune_more", 0, 0, [item("apotheosis:infused_spawner_rune")], "Infused Spawner Rune", deps=["ap_rune"], xp=100,
      optional=True, tokens=1, size=1.5, shape="hexagon", section=INFUSED, subtitle="Optional: a rune with real power", desc=[
        "&eWhat:&r the base of the strongest runes: Stupor, Solitude, Defiance, Echoes and the two top upgrade runes.",
        "&eHow:&r infuse a Spawner Rune at the enchanting table: 70 Eterna, 30 Quanta, 50 Arcana. 70 Eterna needs World Tier: Summit.",
        "&eTip:&r the Apothic Enchanting page walks the shelf build up to those numbers."]),
    rune("ap_rune_summit", "apotheosis:summit_spawner_upgrade_rune", "Mountaineer's Upgrade", "Optional: a much better spawner",
         "the third upgrade rune: a large boost to the spawner.",
         "an Infused Spawner Rune with arcane sands, phantom membranes, a Sigil of Malice and a Warden Tendril.",
         "the tendril drops from the Warden. Plan that fight.", ["ap_rune_more"], xp=100),
    rune("ap_rune_pinnacle", "apotheosis:pinnacle_spawner_upgrade_rune", "Thundering Upgrade", "Optional: a spawner at its limit",
         "the last upgrade rune: the spawner reaches its maximum.",
         "an Infused Spawner Rune with godforged pearls, Infused Breath, a Nether Star and a perfect Endersurge gem.",
         "save Nether Stars: the Seed of a New World needs them too.", ["ap_rune_more"], xp=150),
    rune("ap_rune_noai", "apotheosis:no_ai_spawner_rune", "Rune of Stupor", "Optional: mobs that stand still",
         "spawned mobs have no AI: they don't move, attack or flee.",
         "an Infused Spawner Rune with chorus fruit and a Potion of Fatigue.", "a farm that can't fight back. Mobs without AI also don't despawn on their own.", ["ap_rune_more"]),
    rune("ap_rune_players", "apotheosis:ignore_players_spawner_rune", "Rune of Solitude", "Optional: runs with nobody near",
         "the spawner no longer needs a player nearby (the chunk still has to be loaded).",
         "an Infused Spawner Rune with a Nether Star, phantom membranes and an eye of ender.", "pair it with FTB Chunks chunk loading for an always-on farm.", ["ap_rune_more"]),
    rune("ap_rune_conditions", "apotheosis:ignore_conditions_spawner_rune", "Rune of Defiance", "Optional: ignore every spawn rule",
         "the spawner ignores the mob's spawn conditions entirely (light, block, biome).",
         "an Infused Spawner Rune with a conduit and ender pearls.", "useful for mobs with fussy rules, like slimes or guardians.", ["ap_rune_more"]),
    rune("ap_rune_echo", "apotheosis:echoing_spawner_rune", "Rune of Echoes", "Optional: extra loot per kill",
         "spawned mobs drop extra copies of their loot. It stacks up to three times.",
         "an Infused Spawner Rune ringed with 8 echo shards.", "echo shards come from Ancient City chests, or from infusing one into four.", ["ap_rune_more"]),

    # --- Choosing the mob -------------------------------------------------------------------------------------------------
    Q("ap_capture", 0, 0, [tick()], "Choosing the Mob", deps=["ap_spawner"], xp=25, optional=True, tokens=1, size=1.5, shape="hexagon",
      section=CAPTURE, icon="minecraft:zombie_spawn_egg", subtitle="Optional: change what a spawner spawns", desc=[
        "&eWhat:&r right-click a placed spawner with a spawn egg and it spawns that mob from then on.",
        "&eHow:&r spawn eggs don't drop by themselves. The quests here show three ways to get one. Click the checkmark.",
        "&eTip:&r the egg is used up, so change the mob only when you mean it."]),
    Q("ap_capturing_book", 0, 0, [tick()], "Capturing", deps=["ap_capture"], xp=40, optional=True, tokens=1,
      icon="minecraft:enchanted_book", subtitle="Optional: an enchantment that drops eggs", desc=[
        "&eWhat:&r Capturing is a weapon enchantment from Apothic Spawners: each kill has a small chance per level to drop the mob's spawn egg.",
        "&eHow:&r roll it at an enchanting table or find the book, and put it on a sword. Click the checkmark when you have it.",
        "&eTip:&r the chance is low (half a percent per level), so use it on a farm, not on a hunt."]),
    Q("ap_charm_fragment", 0, 0, [item("reliquary:mob_charm_fragment")], "Eggs from Fragments", deps=["ap_capture"], xp=40,
      optional=True, tokens=1, subtitle="Optional: Reliquary's spawn egg recipe", desc=[
        "&eWhat:&r Reliquary's mob charm fragments can be crafted into that mob's spawn egg.",
        "&eHow:&r fragments drop from the mobs they show. Check JEI (look up the fragment) for the egg recipe.",
        "&eTip:&r the same fragments build Reliquary's Mob Charms (Relics page)."]),
    Q("ap_occult_lead", 0, 0, [item("apothic_enchanting:occult_ender_lead")], "Occult Ender Lead", deps=["ap_capture"], xp=75,
      optional=True, tokens=1, subtitle="Optional: bind a caught mob to a spawner", desc=[
        "&eWhat:&r an Ender Lead infused while holding a witch. It can carry a mob and set it into a spawner, no egg needed.",
        "&eHow:&r catch a witch with an Ender Lead, then infuse that lead at 75 Eterna, 85 Quanta and 60 Arcana (World Tier: Summit).",
        "&eTip:&r the Apothic Enchanting page covers the flimsy and normal leads first."]),

    # --- Other spawners -------------------------------------------------------------------------------------------------
    Q("ap_other_spawners", 0, 0, [tick()], "Other Spawners", deps=["ap_spawner"], xp=25, optional=True, tokens=1,
      section=OTHER, icon="mysticalagriculture:soulium_spawner", subtitle="Optional: spawners from other mods", desc=[
        "&eWhat:&r two other mods in the pack make their own spawners: Ars Additions and Mystical Agriculture.",
        "&eHow:&r read on below. Click the checkmark.",
        "&eTip:&r unlike a monster spawner, both are crafted, so you never have to go looking for one."]),
    Q("ap_source_spawner", 0, 0, [item("ars_additions:source_spawner")], "Source Spawner", deps=["ap_other_spawners"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a spawner that runs on Source", desc=[
        "&eWhat:&r Ars Additions' spawner, which spawns mobs using magical Source instead of waiting on a monster spawner.",
        "&eHow:&r see the Ars Nouveau page for how to build it (check JEI).",
        "&eTip:&r keep it next to a Source jar network."]),
    Q("ap_soulium_spawner", 0, 0, [item("mysticalagriculture:soulium_spawner")], "Soulium Spawner", deps=["ap_other_spawners"], xp=60,
      optional=True, tokens=1, subtitle="Optional: spawn mobs from essence", desc=[
        "&eWhat:&r Mystical Agriculture's spawner, fed with mob essence to spawn that mob.",
        "&eHow:&r see the Mystical Agriculture page for soulium and the spawner recipe (check JEI).",
        "&eTip:&r grow the essence and the spawner never runs dry."]),

    # === Older enchanting quests (kept as optional side quests; the full line is on the Apothic Enchanting page) ===
    Q("m_shelves", 1, 4.5, [item("apothic_enchanting:hellshelf", 4)], "Better Bookshelves", deps=["m_gems", "t2_nether"], xp=40,
      section=ENCH, optional=True, tokens=1, subtitle="Optional: push enchanting past level 30", desc=[
        "&eWhat:&r Apothic Enchanting adds shelves that raise enchanting power, quanta and arcana. Hellshelves are the first step.",
        "&eHow:&r a bookshelf, nether bricks, a blaze rod and a Potion of Regeneration. Create: Enchantment Industry can automate enchanting later.",
        "&eTip:&r the Apothic Enchanting page has the whole shelf ladder."]),
    Q("ap_infused", 2, 7, [item("apothic_enchanting:infused_hellshelf")], "Infusion", deps=["m_shelves"], xp=75,
      subtitle="Enchant a block instead of a tool", optional=True, desc=[
        "&eWhat:&r Apothic Enchanting can 'infuse' items: enchanting a hellshelf at the right power makes an Infused Hellshelf.",
        "&eHow:&r put a hellshelf in the enchanting table at 45 Eterna and 30 Quanta (World Tier: Frontier). JEI's infusion page shows the exact window.",
        "&eTip:&r the table's three stats are shown on the screen: power, randomness and how many extra enchantments you get."]),
    Q("ap_library", 4, 7, [item("apothic_enchanting:library")], "Enchantment Library", deps=["ap_infused"], xp=100,
      subtitle="Store every enchanted book", optional=True, tokens=1, desc=[
        "&eWhat:&r the Library absorbs enchanted books and stores their enchantments as points, then pulls out any level you've collected.",
        "&eHow:&r four ender chests, four infused shelves and an enchanting table.",
        "&eTip:&r it only gives back levels up to the highest single book you fed it, so feed it every spare book."]),
    Q("ap_endshelf", 6, 7, [item("apothic_enchanting:endshelf", 4)], "Endshelves", deps=["ap_infused", "w_end"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the strongest shelf family", desc=[
        "&eWhat:&r endshelves push enchanting power past what hellshelves and seashelves allow.",
        "&eHow:&r end stone bricks, a bookshelf, an ender pearl and Infused Breath (dragon's breath infused at 80 Eterna).",
        "&eTip:&r collect dragon's breath in glass bottles during the Ender Dragon fight."]),
    Q("ap_tome", 2, 8.5, [item("apothic_enchanting:scrap_tome")], "Scrap Tome", deps=["m_shelves"], xp=40,
      optional=True, tokens=1, subtitle="Optional: recycle enchanted gear", desc=[
        "&eWhat:&r a Scrap Tome in an anvil with enchanted gear strips off some of its enchantments into a book (the gear is destroyed).",
        "&eHow:&r eight books around an anvil makes eight tomes.",
        "&eTip:&r the Extraction Tome (infused) keeps the item; check JEI's infusion page."]),
    Q("ap_faberge", 0, 0, [item("apotheosis:ender_gem_case")], "House Fabergé", deps=["ap_gem_case", "ap_infused"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the best gem case", desc=[
        "&eWhat:&r the infused Gem Case. It keeps everything stored in the old one.",
        "&eHow:&r infuse a Gem Case at 100 Eterna, 100 Quanta and 45 to 50 Arcana (World Tier: Pinnacle).",
        "&eTip:&r you'll need endshelves or deepshelves to reach those numbers."]),
    Q("ap_god_pearl", 0, 0, [item("apotheosis:god_fused_pearl")], "God-Fused Pearl", deps=["ap_rarity_all", "ap_infused"], xp=200,
      optional=True, tokens=2, subtitle="Optional: infuse a mythic pearl", desc=[
        "&6You remember something like this sitting in your crown. It was warmer then.&r",
        "&eWhat:&r a godforged pearl infused at a maxed-out enchanting table, used for the Raven's table.",
        "&eHow:&r an enchanting table at 100 Eterna, about 59 Arcana and 10 Quanta (JEI's infusion page has the exact window)."]),
    Q("ap_raven", 0, 0, [item("apothic_enchanting:raven_enchanting_table")], "Enchanting Table of the Raven", deps=["ap_god_pearl"], xp=250,
      optional=True, tokens=2, subtitle="Optional: set the enchanting stats yourself", desc=[
        "&eWhat:&r an enchanting table where you set the core stats by hand instead of building shelves.",
        "&eHow:&r an Apothic enchanting table, 2 god-fused pearls, 3 obsidian and a perfect Royalty gem (check JEI).",
        "&eTip:&r a late luxury: a good shelf room already does most of this."]),
    Q("ap_odd_shelves", 0, 0, [anyof(["apothic_enchanting:stoneshelf", "apothic_enchanting:beeshelf", "apothic_enchanting:melonshelf",
                                      "apothic_enchanting:geode_shelf", "apothic_enchanting:basic_bookshelf"])],
      "Curious Shelves", deps=["m_shelves"], xp=30, optional=True, tokens=1, subtitle="Optional: shelves that bend the rules", desc=[
        "&eWhat:&r the Stoneshelf, Beeshelf, Melonshelf, Geode shelf and Basic Bookshelf each nudge the table's stats in an odd direction.",
        "&eChemistry:&r a geode's calcite rind is CaCO₃, the same compound as chalk and limestone.",
        "&eHow:&r Stoneshelf: polished andesite and books. Geode shelf: calcite around a bookshelf and a budding amethyst. JEI has the rest.",
        "&eTip:&r every shelf's tooltip lists its Eterna, Quanta and Arcana: read them before you build."]),
    Q("ap_hellshelf_up", 0, 0, [anyof(["apothic_enchanting:blazing_hellshelf", "apothic_enchanting:glowing_hellshelf",
                                       "apothic_enchanting:sightshelf", "apothic_enchanting:sightshelf_t2"])],
      "Hellshelf Upgrades", deps=["ap_infused"], xp=60, optional=True, tokens=1, subtitle="Optional: blazing, glowing or all-seeing", desc=[
        "&eWhat:&r the Infused Hellshelf upgrades into Blazing (fire charges), Glowing (glowstone) or the Hellshelf of Sight, which shows more enchantment clues.",
        "&eHow:&r an Infused Hellshelf in the grid with the upgrade items (check JEI). Masterful Sight needs netherite and emerald blocks.",
        "&eTip:&r one Sightshelf shows much more of what the table will roll."]),
    Q("ap_seashelf", 0, 0, [item("apothic_enchanting:seashelf", 4)], "Seashelves", deps=["m_shelves"], xp=40,
      optional=True, tokens=1, subtitle="Optional: the ocean's shelf family", desc=[
        "&eWhat:&r seashelves are the second shelf family, with different stats from hellshelves.",
        "&eChemistry:&r sea water is about 3.5% dissolved salts, mostly NaCl with magnesium and sulfate ions.",
        "&eHow:&r prismarine bricks, a bookshelf, a water bottle and a pufferfish."]),
    Q("ap_seashelf_up", 0, 0, [anyof(["apothic_enchanting:infused_seashelf", "apothic_enchanting:crystal_seashelf",
                                      "apothic_enchanting:heart_seashelf", "apothic_enchanting:filtering_shelf"])],
      "Seashelf Upgrades", deps=["ap_seashelf", "ap_infused"], xp=60, optional=True, tokens=1, subtitle="Optional: infuse a seashelf", desc=[
        "&eWhat:&r an Infused Seashelf, then Crystalline, Heart-Forged or the Seashelf of Aquatic Filtration, which keeps chosen enchantments out of the pool.",
        "&eHow:&r infuse a seashelf at the table, then craft it with prismarine crystals, a heart of the sea, or prismarine bricks and slabs (check JEI).",
        "&eTip:&r the filtering shelf is how you stop a table rolling the enchantment you never want."]),
    Q("ap_deepshelf", 0, 0, [item("apothic_enchanting:dormant_deepshelf"), item("apothic_enchanting:deepshelf")], "Deepshelves", deps=["ap_infused"], xp=75,
      optional=True, tokens=1, subtitle="Optional: shelves from the deep dark", desc=[
        "&eWhat:&r the deepshelf family pushes the stats high. It starts dormant and wakes with infusion.",
        "&eHow:&r Dormant Deepshelf: cracked deepslate tiles and books. Infuse it at 60 Eterna (World Tier: Ascent) to wake it.",
        "&eTip:&r upgrade it with echo shards or soul lanterns; the Deepshelf of Arcane Treasures allows treasure enchantments."]),
    Q("ap_deepshelf_up", 0, 0, [anyof(["apothic_enchanting:echoing_deepshelf", "apothic_enchanting:soul_touched_deepshelf",
                                       "apothic_enchanting:treasure_shelf"])],
      "Deepshelf Upgrades", deps=["ap_deepshelf"], xp=75, optional=True, tokens=1, subtitle="Optional: echoing, soul-touched or treasure", desc=[
        "&eWhat:&r Echoing and Soul-Touched deepshelves raise the stats further; the treasure shelf lets the table roll treasure enchantments.",
        "&eHow:&r a Deepshelf with an echo shard and candles, or a soul lantern and sculk. Treasure: 2 deepshelves, gold blocks, diamonds and an emerald block.",
        "&eTip:&r echo shards come from Ancient City chests."]),
    Q("ap_sculkshelf", 0, 0, [item("apothic_enchanting:warden_tendril"), anyof(["apothic_enchanting:echoing_sculkshelf", "apothic_enchanting:soul_touched_sculkshelf"])],
      "Sculkshelves", deps=["ap_deepshelf_up"], xp=150, optional=True, tokens=2, subtitle="Optional: take a tendril from the Warden", desc=[
        "&eWhat:&r the strongest deepshelves need a Warden Tendril, which drops from a Warden.",
        "&eHow:&r kill a Warden (Ancient City; don't make a sound), then craft the tendril over an upgraded deepshelf with sculk and a sculk catalyst.",
        "&eTip:&r a Warden has 500 health and its sonic boom ignores armor. Plan the fight, or plan the escape."]),
    Q("ap_endshelf_up", 0, 0, [item("apothic_enchanting:infused_breath"), anyof(["apothic_enchanting:pearl_endshelf", "apothic_enchanting:draconic_endshelf"])],
      "Endshelf Upgrades", deps=["ap_endshelf"], xp=150, optional=True, tokens=2, subtitle="Optional: pearlescent or draconic", desc=[
        "&eWhat:&r the top of the shelf ladder. The Pearlescent Endshelf adds end rods; the Draconic one is crowned with a dragon head.",
        "&eHow:&r infuse dragon's breath for Infused Breath (3 per bottle), then craft an Endshelf with end rods and ender pearls, or a dragon head and pearls.",
        "&eTip:&r dragon heads hang on End Ship bows. Bring the elytra home too."]),
    Q("ap_tomes", 0, 0, [anyof(["apothic_enchanting:other_tome", "apothic_enchanting:improved_scrap_tome", "apothic_enchanting:extraction_tome"])],
      "Better Tomes", deps=["ap_tome", "ap_infused"], xp=50, optional=True, tokens=1, subtitle="Optional: books with a single job", desc=[
        "&eWhat:&r the Tome of the Others enchants like a tool no other tome covers; Superior Scrapping and Extraction strip enchantments more gently (Extraction keeps the item).",
        "&eHow:&r Tome of the Others: 6 books and a blaze rod (makes 6). Infuse a Scrap Tome for Superior Scrapping, and that for Extraction.",
        "&eTip:&r Extraction tomes are the cleanest way to move a good enchantment to new gear."]),
    Q("ap_alexandria", 0, 0, [item("apothic_enchanting:ender_library")], "Library of Alexandria", deps=["ap_library"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the library, infused", desc=[
        "&eWhat:&r the infused Enchantment Library stores more and gives back higher levels.",
        "&eHow:&r infuse an Enchantment Library at 100 Eterna, 45 to 50 Quanta and 100 Arcana; it keeps the enchantments already inside.",
        "&eTip:&r the real Library of Alexandria burned; keep this one away from your blaze farm."]),
    Q("ap_leads", 0, 0, [anyof(["apothic_enchanting:flimsy_ender_lead", "apothic_enchanting:ender_lead", "apothic_enchanting:occult_ender_lead"])],
      "Ender Leads", deps=["m_shelves"], xp=40, optional=True, tokens=1, subtitle="Optional: carry a mob in your pocket", desc=[
        "&eWhat:&r the Flimsy Ender Lead captures animals; the infused Ender Lead captures most mobs; the Occult one can bind a mob to a spawner.",
        "&eHow:&r flimsy: an ender pearl, a lead and a gold ingot (shapeless). Infuse it for the Ender Lead; infuse that holding a witch for the Occult lead.",
        "&eTip:&r the easy way to move a villager across the world."]),
    Q("ap_trident", 0, 0, [item("apothic_enchanting:inert_trident")], "Inert Trident", deps=["ap_infused"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a trident without a drowned", desc=[
        "&eWhat:&r an inert trident infuses into a real trident at the enchanting table.",
        "&eHow:&r 3 nautilus shells, a heart of the sea and an iron ingot. Then infuse it (check JEI for the stats).",
        "&eTip:&r a Channeling trident in a thunderstorm calls lightning where it lands."]),
], links=[("gs_iron", -2, 3)], mirror="apotheosis_gear")
