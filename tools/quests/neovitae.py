"""Quest chapter: neovitae (Neo Vitae blood magic). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirrors ATM10's "neo_vitae" chapter quest for quest (its quest list, order, clusters and requirements only; every word
here is ours). Our older quests that ATM10 doesn't have (Tabula Vitae, slates, rune types, Tenebrae ink, ...) stay
as side steps on the same page.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

# Recipes checked against neovitae-1.21.1-1.1.44.jar (data/neovitae/recipe, loot tables) and its guide book. Pack gates
# (pack/kubejs/server_scripts/phase5_neovitae.js): the Athanor needs MI analog circuits (LV); the Tenebrae scribe tool
# moves to the Tabula Vitae and needs 2 hydrogen + an MI electronic circuit (MV); the Flight flask fusion needs
# 2 hydrogen; Athanor ore yields are capped at 2x per ore block (raw ore -> fragments removed, fragment doubling with
# corrupted dust removed); meteor catalysts and Nether Star from diamond are gone.
# Generated material items exist only for pack/config/neovitae/materials.json (no netherite scrap material).
# Spine: altar -> orb -> runes -> Discipulus -> Veneficus -> rituals -> Tau -> Athanor (LV) -> blood shard -> Magus ->
# Demon Realm keys -> Hellforged metal -> Dominus -> Divinus.

ALTAR, SPIRITUS, SIGILS, TIERS, RITES, ATHANOR, REALM, AURA, ROUTING = (
    "The Altar", "Spiritus and the Forge", "Arrays and Sigils", "Altar Tiers", "Rites", "The Athanor",
    "The Demon Realm", "Aura and Crystals", "Blood Routing")

CHAPTER = Chapter("neovitae", "Neo Vitae", "neovitae:blood_orb_weak",
        ["Blood magic: an altar that drinks, orbs that remember, and rituals carved in stone."], SIDE, [
    Q("nv_intro", 0, 0, [tick(), tick()], "Before You Bleed", deps=[], xp=10, optional=True, tokens=0,
      mirror="538E28637FF76912", icon="neovitae:ara_vitae", subtitle="How this page works", desc=[
        "&eWhat:&r Neo Vitae spends your life, and later your mobs', as a fuel called Essentia Vitae (EV). Everything on this page follows from the altar.",
        "&eHow:&r the guide book Scriptura Vitae (a book and 4 redstone) shows every altar tier, ritual and array in 3D. Tick both boxes once you've made it.",
        "&eTip:&r the big pack gates are noted on the quests they touch: the Athanor (LV circuits), Tenebrae ink and flight (hydrogen and MV)."]),

    # --- First steps -------------------------------------------------------------------------------------------
    Q("nv_altar", 0, 0, [item("neovitae:ara_vitae")], "Ara Vitae", deps=["gs_iron"], xp=60, size=2.0, shape="gear",
      section=ALTAR, mirror="65BD73DA55BCC624", subtitle="An altar that runs on life", desc=[
        "&6You remember that every power has a price, and that the oldest price was always blood.&r",
        "&eWhat:&r the Ara Vitae is the heart of Neo Vitae. It turns life into Essentia Vitae (EV) and uses it to transmute items placed on top.",
        "&eChemistry:&r blood is about 55% plasma (mostly water, salts and proteins) and 45% cells. Its red comes from haemoglobin, an iron(II) complex that carries O₂.",
        "&eHow:&r a furnace, 3 gold ingots and 4 deepslate (the mod's 'vitae stone') in a crafting table.",
        "&eTip:&r the guide book, Scriptura Vitae, is a book with 4 redstone; it shows every multiblock."]),
    Q("nv_orb", 2, 0, [item("neovitae:blood_orb_weak")], "Novicius Orb", deps=["nv_altar"], xp=40,
      mirror="73391A08D7615C77", subtitle="A diamond that holds your blood", desc=[
        "&eWhat:&r an Orb of Vitae is your personal EV network. Right-click it to bleed into it; machines and sigils draw from it anywhere.",
        "&eChemistry:&r the orb starts as a diamond: pure carbon in a tetrahedral lattice, hard enough to hold whatever the altar pours into it.",
        "&eHow:&r place a diamond on the empty altar and stand close. With no blood of its own, the altar draws from anyone nearby.",
        "&eTip:&r watch your hearts while bleeding. Eat well first; regeneration is your fuel."]),
    Q("nv_rasa", 4, 0, [item("neovitae:tabula_rasa", 8)], "Tabula Rasa", deps=["nv_altar"], xp=30,
      mirror="56F4E4845B8F12BB", subtitle="Blank slates for everything", desc=[
        "&eWhat:&r Tabula Rasa is the blank slate in almost every Neo Vitae recipe: runes, sigils, tables and fuel cells.",
        "&eChemistry:&r deepslate is metamorphosed rock: heat and pressure deep underground recrystallised it into dense, layered stone.",
        "&eHow:&r put deepslate on the altar with blood in it. Cobblestone on the altar also turns into cobbled deepslate for 50 EV.",
        "&eTip:&r make a stack; you will use them faster than you expect."]),
    Q("nv_table", 6, 0, [item("neovitae:tabula_vitae")], "Tabula Vitae", deps=["nv_rasa"], xp=40,
      subtitle="The alchemy table", desc=[
        "&eWhat:&r the Tabula Vitae combines up to six items with EV from the orb inside it: reagents, catalysts, cutting fluids, anointments.",
        "&eChemistry:&r its gunpowder recipe is real: sulfur, saltpetre (KNO₃) and charcoal, about 10:75:15 by mass in classic black powder.",
        "&eHow:&r deepslate, planks, iron and gold ingots and a Tabula Rasa. Put your orb in its orb slot.",
        "&eTip:&r it also grinds an ore block into 2 dust, the pack's normal pre-acid yield."]),

    # --- Spiritus and the Hellfire Forge (ATM10: the cluster above the altar) ----------------------------------
    Q("nv_daggers", 8, 1.5, [item("neovitae:throwing_dagger", 16), item("neovitae:base_spiritus_soul_raw")], "Throwing Daggers",
      deps=["nv_table"], xp=30, section=SPIRITUS, mirror="71E0D06EA65172CF", subtitle="Wounds that leave something behind", desc=[
        "&eWhat:&r creatures killed with throwing daggers drop Spiritus Essence, the residue of a soul. The Hellfire Forge burns it.",
        "&eHow:&r 2 iron ingots and a string in the Tabula Vitae make 16 daggers. Throw them at mobs and pick up what's left.",
        "&eTip:&r a Sentient Sword collects Spiritus much faster once you have one."]),
    Q("nv_forge", 10, 3, [item("neovitae:hellfire_forge"), item("neovitae:spiritus_gem_petty")], "Hellfire Forge",
      deps=["nv_daggers"], xp=50, size=1.5, shape="hexagon", mirror="5C3EA8B4F5949406", subtitle="A forge that burns souls", desc=[
        "&eWhat:&r the Hellfire Forge combines items using Spiritus in its gem slot instead of fuel. Its first job is a gem to hold that Spiritus.",
        "&eHow:&r iron ingots, an iron block, deepslate and a Tabula Rasa. Then forge a Petty Spiritus Gem (redstone, gold, glass, lapis).",
        "&eTip:&r a recipe only starts if the gem holds at least its minimum Spiritus. JEI shows both numbers."]),
    Q("nv_gem", 12, 4.5, [item("neovitae:spiritus_gem_petty")], "Petty Spiritus Gem", deps=["nv_forge"], xp=40,
      subtitle="Somewhere to keep it", desc=[
        "&eWhat:&r Spiritus gems store Spiritus and soak up any you pick up, so it stops cluttering your inventory.",
        "&eChemistry:&r lapis lazuli is mostly lazurite, a sodium aluminium silicate whose blue comes from trapped S₃⁻ radical ions.",
        "&eHow:&r redstone, a gold ingot, glass and lapis in the Hellfire Forge.",
        "&eTip:&r bigger gems come later from the same forge; each holds much more."]),
    Q("nv_sentient", 14, 4.5, [item("neovitae:sentient_sword")], "Sentient Sword", deps=["nv_gem"], xp=50,
      mirror="602884068EC40EDB", subtitle="A blade that takes its share", desc=[
        "&eWhat:&r the Sentient Sword collects Spiritus from every kill and hits harder the more Spiritus you carry.",
        "&eHow:&r an iron sword in the Hellfire Forge with a Petty Spiritus Gem as catalyst (the gem stays).",
        "&eTip:&r the axe, pickaxe, shovel and scythe work the same way."]),
    Q("nv_spikes", 0, 0, [item("neovitae:spike_trap")], "Spike Trap", deps=["nv_forge"], xp=60, optional=True, tokens=1,
      mirror="1BBABB2106D321A4", subtitle="Optional: a trap that tithes to the altar", desc=[
        "&eWhat:&r a redstone-triggered block of blades. Kills it makes within 16 blocks of an Ara Vitae feed the altar directly.",
        "&eHow:&r dungeon stone around a dispenser and spikes (spikes are made on the altar). Dungeon stone comes from the Demon Realm, so this waits until you've been there.",
        "&eTip:&r a mob farm that ends on spike traps is an EV farm."]),
    Q("nv_routing", 0, 0, [item("neovitae:routing_conduit", 4), item("neovitae:input_routing_node"), item("neovitae:output_routing_node")],
      "Routing Conduits", deps=["nv_forge"], xp=50, optional=True, tokens=1, section=ROUTING, mirror="24C0619EB4A13CA3",
      subtitle="Optional: item pipes, the blood-magic way", desc=[
        "&eWhat:&r Neo Vitae has its own item routing: conduits link input nodes (which pull from inventories) to output nodes (which push into them).",
        "&eHow:&r conduits are 2 deepslate, iron and glass in the Hellfire Forge; a conduit and a hopper make an input node. Input and output nodes craft into each other.",
        "&eTip:&r check Scriptura Vitae for how the network is linked and filtered."]),
    Q("nv_router", 0, 0, [item("neovitae:node_router"), tick()], "Node Router", deps=["nv_routing"], xp=40, optional=True, tokens=1,
      mirror="3F2FE793CE5052F0", subtitle="Optional: the tool that links nodes", desc=[
        "&eWhat:&r the Node Router connects routing nodes to each other.",
        "&eHow:&r 2 deepslate, an iron ingot and redstone in the Hellfire Forge. Tick the box once you've linked a node pair.",
        "&eTip:&r link in a line or a star; long chains are easier to fix later than tangles."]),
    Q("nv_master_core", 0, 0, [item("neovitae:master_core"), item("neovitae:master_core_speed")], "Routing Upgrades",
      deps=["nv_routing"], xp=50, optional=True, tokens=1, mirror="7CF9A68167ADAD1A", subtitle="Optional: bigger stacks, faster moves", desc=[
        "&eWhat:&r the Routing Stack Upgrade and Routing Speed Upgrade make a routing network move more items, more often.",
        "&eHow:&r stack: 2 iron, glass and a lapis block in the Hellfire Forge. Speed: 2 gold, glass and a redstone block.",
        "&eTip:&r JEI and Scriptura Vitae show where the upgrades go."]),

    # --- Arrays and sigils -------------------------------------------------------------------------------------
    Q("nv_scribe", 8, -1.5, [item("neovitae:arcane_scribe_tool")], "Arcane Scribe Tool", deps=["nv_table"], xp=30,
      section=SIGILS, mirror="0BA0AA8A6F07D383", subtitle="Draw circles on the ground", desc=[
        "&eWhat:&r the Arcane Scribe Tool draws an Alchemy Array. Drop two items into an array and it crafts a sigil or casts an effect.",
        "&eChemistry:&r it is made of redstone, white dye, gunpowder and coal: a pigment, a binder and a little fire.",
        "&eHow:&r Tabula Vitae, then right-click the ground with the tool.",
        "&eTip:&r JEI lists every array recipe under the Alchemy Array category."]),
    Q("nv_array", 0, 0, [tick()], "Arrays: Base and Catalyst", deps=["nv_scribe"], xp=20, mirror="1F7ACF813D8804A6",
      icon="neovitae:arcane_scribe_tool", subtitle="The order matters", desc=[
        "&eWhat:&r every array recipe has a base item, dropped in first, and a catalyst, dropped in second. Swap them and nothing happens.",
        "&eHow:&r draw an array, drop the base, then the catalyst. Tick the box when you've read this.",
        "&eTip:&r sigils are reagent first, slate second; JEI shows which is which."]),
    Q("nv_divination", 10, -1.5, [item("neovitae:sigil_divination"), item("neovitae:sigil_seer")], "Divination and Seer's Sigils",
      deps=["nv_array", "nv_robur"], xp=40, mirror="6101AB772B0317F1", subtitle="Read your own blood", desc=[
        "&eWhat:&r the Divination Sigil shows the EV in your network and in an altar. The Seer's Sigil adds the altar's tier, rates and a ritual's working area.",
        "&eHow:&r Divination: an array with redstone first, then a Tabula Rasa. Seer's: the Sight Reagent (Tabula Vitae) first, then a Tabula Robur.",
        "&eTip:&r keep one handy while you build up the altar; it tells you when a craft has enough EV."]),
    Q("nv_sigils", 12, -3, [item("neovitae:sigil_water"), item("neovitae:sigil_lava"), item("neovitae:sigil_void"),
                             item("neovitae:sigil_green_grove"), item("neovitae:sigil_fast_miner"), item("neovitae:sigil_magnetism")],
      "Utility Sigils", deps=["nv_array", "nv_robur"], xp=80, optional=True, tokens=1, subtitle="Optional: six everyday sigils", desc=[
        "&eWhat:&r Water and Lava place fluids, Void deletes them, Green Grove speeds crops, Fast Miner gives haste and Magnetism pulls items to you.",
        "&eChemistry:&r lava plus cobblestone in the Tabula Vitae gives sulfur: volcanoes really do deposit sulfur where their gases (H₂S, SO₂) cool at vents.",
        "&eHow:&r each is its reagent (Tabula Vitae) in an array with a slate: Tabula Rasa or Robur for most, Tabula Animata for Magnetism.",
        "&eTip:&r a Sigil of Holding keeps them in one slot."], mirror="19891A8F26FBAB0A"),

    # --- Altar tiers -------------------------------------------------------------------------------------------
    Q("nv_runes", 10, 0, [item("neovitae:rune_blank", 8)], "Blank Runes", deps=["nv_orb", "nv_rasa"], xp=40,
      section=TIERS, mirror="4EBC5B191A7B12D9", subtitle="The altar grows downward", desc=[
        "&eWhat:&r runes around the altar raise its tier. Tier II is a ring of 8 runes one block below the altar.",
        "&eHow:&r deepslate, a Tabula Rasa and your orb in a crafting table (the orb is not used up). Scriptura Vitae shows each tier's layout.",
        "&eTip:&r blank runes count for the structure; upgraded runes add their effect on top."]),
    Q("nv_altar_t2", 0, 0, [item("neovitae:blood_orb_apprentice")], "The First Ring", deps=["nv_runes"], xp=60, size=1.5, shape="hexagon",
      mirror="759B0D6F8C0CC1EF", subtitle="Build the Tier II altar", desc=[
        "&eWhat:&r eight runes in a ring under the altar make it Tier II: a bigger basin and new recipes.",
        "&eHow:&r place the ring as Scriptura Vitae shows; the Divination or Seer's sigil confirms the tier. This completes with the orb the new tier makes.",
        "&eTip:&r the altar only checks its shape; you can rebuild it with better runes later without losing anything."]),
    Q("nv_apprentice", 12, 0, [item("neovitae:blood_orb_apprentice")], "Discipulus Orb", deps=["nv_altar_t2"], xp=75, size=1.5,
      shape="hexagon", mirror="7AFEB7A91DC8F413", subtitle="Tier II: the second orb", desc=[
        "&6You remember the weight of a bigger vessel, and how much more it could hold.&r",
        "&eWhat:&r a bigger orb holds more EV and unlocks tier-2 recipes, including the Sacrifice rune and Tabula Robur.",
        "&eHow:&r a block of redstone on a Tier II altar (8 runes), 5,000 EV.",
        "&eTip:&r keep the old orb; Tabula recipes that need a lower orb accept a higher one."]),
    Q("nv_flask", 0, 0, [item("neovitae:alchemy_flask")], "Alchemy Flask", deps=["nv_apprentice"], xp=40, optional=True, tokens=1,
      mirror="564AD8763F753C74", subtitle="Optional: a potion you refill", desc=[
        "&eWhat:&r the Alchemy Flask holds potion effects you can add to, lengthen and strengthen, and drink several times.",
        "&eChemistry:&r a glass bottle is mostly SiO₂ with soda and lime: about as unreactive a container as you can make cheaply.",
        "&eHow:&r a glass bottle on a Tier I altar or better, 4,000 EV. Rinse it with a water bucket to empty it.",
        "&eTip:&r the Flight effect is fused in a flask too; in this pack it needs 2 hydrogen."]),
    Q("nv_tipped", 0, 0, [item("neovitae:tipped_throwing_dagger")], "Tipped Daggers", deps=["nv_flask"], xp=50, optional=True, tokens=1,
      mirror="4840F41B536529E3", subtitle="Optional: daggers that carry a potion", desc=[
        "&eWhat:&r throwing daggers coated with a lingering flask's effect, so every hit applies it.",
        "&eHow:&r amethyst throwing daggers in the Athanor with a lingering flask as the tool make 8 (check JEI).",
        "&eTip:&r weakness or slowness on a dagger makes the Demon Realm a lot friendlier."]),
    Q("nv_rune_types", 12, 1.5, [item("neovitae:rune_sacrifice"), item("neovitae:rune_speed")], "Sacrifice and Speed",
      deps=["nv_runes"], xp=40, subtitle="Runes that do something", desc=[
        "&eWhat:&r Runes of Sacrifice give more EV per creature killed near the altar; Speed Runes make it craft faster.",
        "&eHow:&r both start from a blank rune. Sacrifice needs a Tabula Robur, gold and an Apprentice orb or better; Speed needs Tabula Rasa and sugar.",
        "&eTip:&r a mob farm next to a ring of Sacrifice runes feeds the altar while you're away."]),
    Q("nv_robur", 14, 1.5, [item("neovitae:tabula_robur", 4), item("neovitae:tabula_animata", 2)], "Stronger Slates",
      deps=["nv_apprentice"], xp=50, subtitle="Robur and Animata", desc=[
        "&eWhat:&r Tabula Robur and Tabula Animata are the next slates: runes, sigils, casings and the Athanor need them.",
        "&eHow:&r a Tabula Rasa on the altar becomes Robur (2,000 EV); Robur on a Tier III altar becomes Animata.",
        "&eTip:&r slates are where most of your EV goes early on. Upgrade the altar before mass-producing them."]),
    Q("nv_holding", 16, 3, [item("neovitae:sigil_holding")], "Sigil of Holding", deps=["nv_robur"], xp=40,
      optional=True, tokens=1, subtitle="Five sigils, one slot", desc=[
        "&eWhat:&r the Sigil of Holding stores other sigils and lets you switch between them.",
        "&eHow:&r Reagent Holding (chest, leather, 2 string) in an array with a Tabula Animata.",
        "&eTip:&r put your Water, Lava and Divination sigils in it to free hotbar slots."]),
    Q("nv_altar_t3", 0, 0, [item("neovitae:blood_orb_magician")], "The Second Ring", deps=["nv_apprentice"], xp=75, size=1.5,
      shape="hexagon", mirror="383F7F715C60252B", subtitle="Build the Tier III altar", desc=[
        "&eWhat:&r Tier III adds a wider ring of runes a level further down, with pillars and caps at the corners.",
        "&eHow:&r Scriptura Vitae shows the layout block by block. This completes with the Veneficus orb that the new tier makes.",
        "&eTip:&r Runes of Capacity and Charging help the altar hold enough EV for the orb."]),
    Q("nv_magician", 16, 0, [item("neovitae:blood_orb_magician")], "Veneficus Orb", deps=["nv_altar_t3", "nv_robur"], xp=100,
      size=1.5, shape="hexagon", mirror="1B6642BBDAEB2BD5", subtitle="Tier III: rituals open", desc=[
        "&eWhat:&r the third orb. With it come ritual stones, the Master Ritual Stone and activation crystals.",
        "&eChemistry:&r gold is the input: it barely reacts with anything, which is why it lasts in the ground as native metal.",
        "&eHow:&r a block of gold on a Tier III altar, 25,000 EV. Scriptura Vitae shows the Tier III layout.",
        "&eTip:&r Runes of Capacity and Charging help the altar hold enough EV for this craft."]),
    Q("nv_tome", 18, 4.5, [item("neovitae:experience_tome")], "Tome of Peritia", deps=["nv_magician"], xp=40,
      optional=True, tokens=1, subtitle="Bottle your experience", desc=[
        "&eWhat:&r the Tome of Peritia stores experience levels so you can spend them later.",
        "&eHow:&r an enchanted book, lapis blocks, gold, string, 2 Tabula Animata and a Veneficus orb.",
        "&eTip:&r the Array of Liquified Experience moves stored XP into a tank as fluid."]),

    # --- Rites -------------------------------------------------------------------------------------------------
    Q("nv_ritual", 18, -1.5, [item("neovitae:master_ritual_stone"), item("neovitae:ritual_stone", 8),
                               item("neovitae:activation_crystal_weak")], "Master Ritual Stone",
      deps=["nv_magician"], xp=100, size=1.5, shape="hexagon", section=RITES, mirror="46122A9389875512", subtitle="Carve the circle", desc=[
        "&eWhat:&r a ritual is a Master Ritual Stone surrounded by inscribed ritual stones in a fixed pattern, started with an activation crystal.",
        "&eHow:&r ritual stones from obsidian, Tabula Robur and a Discipulus orb; the master stone needs the Veneficus orb. The crystal is a Lava Crystal on the altar.",
        "&eTip:&r the Ritual Diviner places a whole ritual's stones for you, already inscribed."]),
    Q("nv_diviner", 20, -1.5, [item("neovitae:ritual_diviner")], "Ritual Diviner", deps=["nv_ritual"], xp=50,
      subtitle="Place a whole ritual at once", desc=[
        "&eWhat:&r the Ritual Diviner builds a chosen ritual around a Master Ritual Stone, stone by stone, from your inventory.",
        "&eHow:&r the four elemental inscription tools (ghast tear, obsidian, magma cream, lapis block on the altar) with diamonds and a stick.",
        "&eTip:&r useful early rites: Green Grove (crops), Harvest, Well of Suffering (EV from mobs) and Magnetism (ores, like a slow quarry)."]),
    Q("nv_armour", 22, 3, [item("neovitae:sentient_helmet"), item("neovitae:sentient_plate"), item("neovitae:sentient_leggings"),
                            item("neovitae:sentient_boots")], "Sentient Armour", deps=["nv_ritual"], xp=100,
      mirror="02B5E57E9E803F78", subtitle="Armour that trains itself", desc=[
        "&eWhat:&r Sentient Armour gains upgrades from what you do while wearing it: running, taking hits, mining, eating.",
        "&eHow:&r an Alchemy Array with Reagent Binding (glowstone, redstone, gunpowder, gold nugget) and an iron armour piece, one array per piece.",
        "&eTip:&r a ritual can push the armour's upgrade capacity further; Scriptura Vitae lists it under rituals."]),
    Q("nv_upgrade_tome", 0, 0, [item("neovitae:upgrade_tome")], "Upgrade Tomes", deps=["nv_armour"], xp=50, optional=True, tokens=1,
      mirror="5AA17C1657E8E5DE", subtitle="Optional: teach the armour directly", desc=[
        "&eWhat:&r an Upgrade Tome adds one upgrade to Sentient Armour without earning it the slow way.",
        "&eHow:&r some are Tabula Vitae recipes around a written book (Curios Sockets: shulker shell, ender pearl, gold); others, like Elytra, only come from Demon Realm loot.",
        "&eTip:&r bad upgrades exist too (Limp Leg, Dulled Blade): read a tome before you use it."]),
    Q("nv_tau", 20, 0, [item("neovitae:weak_tau", 4), item("neovitae:strong_tau")], "Tau Fruit", deps=["nv_ritual"], xp=75,
      mirror="5785D68A5F1ED2D2", subtitle="Something grows on the other side", desc=[
        "&eWhat:&r Tau is a fruit from the Demon Realm. Saturated (Strong) Tau feeds the Athanor's blood shards.",
        "&eHow:&r the ritual Breaching the Edge of Demon Realm builds a small dungeon whose chests and farms hold Tau. Replant it; a creature standing on the plant while it ripens makes Strong Tau.",
        "&eTip:&r bring armour and food; the dungeon is not empty."]),

    # --- The Athanor -------------------------------------------------------------------------------------------
    Q("nv_athanor", 18, 1.5, [item("neovitae:athanor")], "Athanor", deps=["nv_tau", "t3_analog"], xp=150, size=1.5, shape="hexagon",
      section=ATHANOR, mirror="40C32A4F6DE4B782", subtitle="An alchemical furnace with a thermostat", desc=[
        "&eWhat:&r the Athanor is Neo Vitae's reaction chamber: ore processing, sulfur from netherrack, blood shards and the late gems.",
        "&eChemistry:&r a medieval athanor was a furnace that fed itself charcoal to hold one steady heat. Holding a temperature is a control problem, so here it needs analog circuits.",
        "&eHow:&r deepslate, 2 Tabula Animata, a furnace, a Veneficus orb and 2 MI analog circuits (LV). Tools go in its tool slot: cutting fluid, resonator, hydration cell.",
        "&eTip:&r it runs at half speed with no Raw Spiritus in the chunk and up to double speed when the chunk is full."]),
    Q("nv_cutting_fluid", 0, 0, [item("neovitae:basic_cutting_fluid")], "Basic Cutting Fluid", deps=["nv_athanor"], xp=50,
      optional=True, tokens=1, mirror="54AB11938676D4C7", subtitle="Optional: the ore-processing tool", desc=[
        "&eWhat:&r cutting fluid is the Athanor's tool for breaking ore apart.",
        "&eChemistry:&r real cutting fluids are oil emulsions that cool and lubricate a cut; this one is plant oil, sugar, coal dust and water with redstone and gunpowder.",
        "&eHow:&r plant oil, redstone, gunpowder, sugar, coal dust and a water bottle (or Water Sigil) in the Tabula Vitae.",
        "&eTip:&r in this pack an ore block gives 2 fragments here, the normal pre-acid cap."]),
    Q("nv_ore", 20, 3, [anyof(["neovitae:iron_dust", "neovitae:gold_dust", "neovitae:copper_dust"], 8)], "Blood and Ore",
      deps=["nv_cutting_fluid"], xp=50, optional=True, tokens=1, subtitle="Cutting fluid and fragments", desc=[
        "&eWhat:&r with Cutting Fluid as its tool, the Athanor breaks an ore block into 2 fragments, then gravel, then dust.",
        "&eChemistry:&r in this pack the big ore multipliers belong to acids (HCl, H₂SO₄ in Mekanism): dissolving ore frees metal that crushing leaves behind.",
        "&eHow:&r put ore and cutting fluid in the Athanor. Raw ore goes straight to 1 dust with a small bonus chance.",
        "&eTip:&r this is a magic route at the normal 2x cap, not a shortcut past the acid lines."]),
    Q("nv_gravel", 0, 0, [item("neovitae:corrupted_dust"), item("neovitae:iron_gravel")], "Gravel and Corruption", deps=["nv_athanor"],
      xp=50, optional=True, tokens=1, mirror="70D2718D54785867", subtitle="Optional: the in-between steps", desc=[
        "&eWhat:&r Athanor ore processing goes ore, fragment, gravel, dust. Corrupted Dust is a by-product of the later steps.",
        "&eHow:&r follow an iron ore through the Athanor and keep the gravel; four tiny piles of corrupted dust craft into one (JEI lists its sources).",
        "&eTip:&r the mod's 'fragment plus corrupted dust makes more gravel' recipe is removed here: no doubling past 2x."]),
    Q("nv_reverter", 0, 0, [item("minecraft:enchanted_book"), item("neovitae:sanguine_reverter")], "Sanguine Reverter",
      deps=["nv_athanor"], xp=50, optional=True, tokens=1, mirror="58248AF507380501", subtitle="Optional: unmake things", desc=[
        "&eWhat:&r with the Sanguine Reverter as its tool, the Athanor takes things apart again: orbs back to their parts, enchantments off books and gear.",
        "&eHow:&r shears, deepslate, a Tabula Animata and an iron ingot in the Hellfire Forge.",
        "&eTip:&r JEI lists everything it can unmake."]),
    Q("nv_shard", 22, 0, [item("neovitae:weak_blood_shard"), item("neovitae:bloodstone", 4)], "Weak Blood Shard",
      deps=["nv_tau", "nv_athanor"], xp=100, mirror="3CA324BE8531F253", subtitle="Concentrated life", desc=[
        "&eWhat:&r Weak Blood Shards open Tier IV: the Magus orb, stronger anointments and potion catalysts. Tier IV's pillars are capped with bloodstone.",
        "&eHow:&r Strong Tau in the Athanor with a hydration cell as the tool and 3,200 mB of Essentia Vitae. Bloodstone is 8 stone around a bucket of Essentia Vitae.",
        "&eTip:&r the Primitive Hydration Cell is cobblestone, a water bucket, a Tabula Rasa and a Veneficus orb."]),
    Q("nv_master", 24, 0, [item("neovitae:blood_orb_master")], "Magus Orb", deps=["nv_shard"], xp=150, size=1.5, shape="hexagon",
      mirror="11F6669733F1420B", subtitle="Tier IV: the deep end", desc=[
        "&6You remember the altar answering before you asked. Your blood and the stone keep the same time now.&r",
        "&eWhat:&r the fourth orb, for Tier IV recipes and the Awakened Activation Crystal.",
        "&eHow:&r a Weak Blood Shard on a Tier IV altar, 40,000 EV.",
        "&eTip:&r stock up EV first; the altar drains fast on big crafts."]),
    Q("nv_tenebrae", 26, -1.5, [item("neovitae:tenebrae_scribe_tool")], "Tenebrae Ink", deps=["nv_master", "t4_circuit", "t2_hydrogen"],
      xp=150, subtitle="Dark runes, flight and the big rites", desc=[
        "&eWhat:&r the Tenebrae inscription tool carves the dark ritual stones of the big rites: Condor (flight in an area), Torment Nexus, Enchanted Vitae.",
        "&eChemistry:&r soot (carbon black) is the oldest ink there is. Here a coal block is made into ink with 2 hydrogen (chemlib:hydrogen) and an MI electronic circuit (MV).",
        "&eHow:&r Tabula Vitae with a Magus-level setup. The Flight elixir (Suspended + Levitation fused with a Combinational Catalyst) also needs 2 hydrogen.",
        "&eTip:&r flight in this pack is always a chemistry milestone. The Ritual of Meteo has no catalysts here: ore comes from the ground and from chemistry."]),
    Q("nv_tenebrae_diviner", 28, -1.5, [item("neovitae:ritual_diviner_tenebrae")], "Ritual Diviner [Tenebrae]",
      deps=["nv_tenebrae", "nv_diviner"], xp=75, subtitle="Place the dark rites too", desc=[
        "&eWhat:&r the Tenebrae diviner can place every Tier IV ritual, including the Ritual of the Condor.",
        "&eHow:&r your Ritual Diviner, 2 Tenebrae tools and 2 Tabula Spiritus.",
        "&eTip:&r the Ritual Configurator changes a ritual's area and options."]),

    # --- The Demon Realm -----------------------------------------------------------------------------------------
    Q("nv_breach", 0, 0, [dim("neovitae:dungeon")], "The Demon Realm", deps=["nv_master"], xp=100, size=1.5, shape="hexagon",
      section=REALM, mirror="09DEA44456CD5010", subtitle="Walk through the veil", desc=[
        "&eWhat:&r the Demon Realm is Neo Vitae's own dimension of dungeons: farms, crypts, libraries and, deeper down, the mines.",
        "&eHow:&r a dungeon ritual on a Master Ritual Stone opens the way (the Diviner lists the dungeon rites). Step through.",
        "&eTip:&r the realm's chests hold keys; every locked door further in wants one."]),
    Q("nv_keys", 0, 0, [item("neovitae:standard_key", 2), dim("neovitae:dungeon")], "Highway to the Deep", deps=["nv_master"], xp=100,
      size=1.5, shape="hexagon", mirror="671F7551CBDF462F", subtitle="Two keys for the standard dungeon", desc=[
        "&eWhat:&r Standard Dungeon Keys open the locked rooms of the Demon Realm's larger dungeons.",
        "&eHow:&r loot Demon Realm chests until you have two. The Highway to Hell ritual leads into the Endless dungeon beyond.",
        "&eTip:&r keys stack; take every one you see."]),
    Q("nv_mine_entrance", 0, 0, [item("neovitae:mine_entrance_key")], "Mine Entrance Key", deps=["nv_keys"], xp=75,
      mirror="4694863405CFB97B", subtitle="Forge your way into the mines", desc=[
        "&eWhat:&r the mines are the Demon Realm level where demonite ore lies. Their entrance key is forged, not found.",
        "&eHow:&r a Tabula Animata, an echo shard, a diamond and a Simple Key (from the first dungeon) in the Hellfire Forge.",
        "&eTip:&r echo shards come from Ancient City chests in the Deep Dark."]),
    Q("nv_mine_key", 0, 0, [item("neovitae:mine_key")], "Mine Dungeon Key", deps=["nv_mine_entrance"], xp=75,
      mirror="419DB4A2A5A5FC58", subtitle="The mines' own locks", desc=[
        "&eWhat:&r Mine Dungeon Keys open the locked rooms inside the mines.",
        "&eHow:&r found in Demon Realm chests (the standard dungeon has a chest for them, and the mines hold more).",
        "&eTip:&r ore rooms and the smithy are worth a key each."]),
    Q("nv_demonite", 0, 0, [item("neovitae:raw_demonite")], "Raw Demonite", deps=["nv_mine_key"], xp=75,
      mirror="4EE580588CC10C4E", subtitle="Ore that isn't from this world", desc=[
        "&eWhat:&r demonite is Neo Vitae's magic metal ore, found only in the Demon Realm's mines.",
        "&eHow:&r mine demonite ore in the mines; it drops raw demonite.",
        "&eTip:&r demonite isn't a chemistry metal, so its processing isn't capped like real ores are."]),
    Q("nv_hellforged", 26, 1.5, [item("neovitae:ingot_hellforged", 9)], "Hellforged Metal", deps=["nv_demonite"], xp=150,
      mirror="7C7C061FC04B89FB", subtitle="Ore from the Demon Realm", desc=[
        "&eWhat:&r Hellforged metal makes the Dominus orb and the reinforced runes.",
        "&eHow:&r smelt or blast raw demonite into Hellforged Ingots.",
        "&eTip:&r Hellforged Dust, which better cutting fluids need, comes from ingots in the Athanor."]),
    Q("nv_archmage", 28, 0, [item("neovitae:blood_orb_archmage"), item("neovitae:hellforged_block")], "Dominus Orb", deps=["nv_hellforged"],
      xp=200, size=1.5, shape="hexagon", mirror="7731623EA92027D9", subtitle="Tier V", desc=[
        "&eWhat:&r the fifth orb, made from a block of Hellforged metal.",
        "&eHow:&r a Hellforged Block on a Tier V altar, 80,000 EV. Tier V needs upgraded runes and capstones (see Scriptura Vitae).",
        "&eTip:&r Reinforced runes (Hellforged Parts) double a rune's effect."]),
    Q("nv_transcendent", 30, 0, [item("neovitae:blood_orb_transcendent"), item("neovitae:crystal_cluster")], "Divinus Orb",
      deps=["nv_archmage"], xp=300, size=2.0, shape="gear", mirror="702FC3E5D0D6C31F", subtitle="Tier VI: the last altar", desc=[
        "&6You remember the last altar: not a tool any more, but a promise kept in stone.&r",
        "&eWhat:&r the sixth and final orb. It opens the Deus rites and the top of Vitaemancy.",
        "&eHow:&r a Crystal Cluster (sculk, Tabula Aetherea, a Weak Blood Shard and a Nether Star in the Hellfire Forge) on a Tier VI altar, 200,000 EV.",
        "&eTip:&r Nether Stars only come from the Wither here; a diamond can't be turned into one."]),
    Q("nv_deeper_key", 0, 0, [item("neovitae:mine_key")], "Deeper Locks", deps=["nv_breach"], xp=50, optional=True, tokens=1,
      mirror="4AE0C2D2D8D145F6", subtitle="Optional: another key, another room", desc=[
        "&eWhat:&r the mines have more locked rooms than one key opens.",
        "&eHow:&r keep looting Demon Realm chests for Mine Dungeon Keys.",
        "&eTip:&r the smithy room is where Hellforged Parts tend to turn up."]),
    Q("nv_parts", 0, 0, [item("neovitae:hellforged_parts")], "Hellforged Parts", deps=["nv_deeper_key"], xp=75, optional=True, tokens=1,
      mirror="4F77EDCEB49EB67F", subtitle="Optional: the stuff of reinforced runes", desc=[
        "&eWhat:&r Hellforged Parts turn a rune into a reinforced rune with double the effect.",
        "&eHow:&r loot from the mines' chests (the foreman's treasure and the smithy especially).",
        "&eTip:&r reinforce your Sacrifice and Capacity runes first."]),

    # --- Tau oil and the aura (ATM10: the clusters off the Magus orb) -------------------------------------------
    Q("nv_tau_oil", 0, 0, [item("neovitae:tau_oil"), item("neovitae:weak_tau", 4)], "Tau Oil", deps=["nv_master"], xp=50,
      optional=True, tokens=1, mirror="22CB17C102BB6773", subtitle="Optional: press the fruit", desc=[
        "&eWhat:&r Tau Oil makes any anointment last four times longer and goes into better cutting fluids.",
        "&eChemistry:&r pressing fruit for oil is old chemistry: most plant oils are triglycerides, three fatty acids on a glycerol backbone.",
        "&eHow:&r 3 Weak Tau and bone meal in the Tabula Vitae.",
        "&eTip:&r keep a Tau farm running; the oil and the shards both eat fruit."]),
    Q("nv_catalyst", 0, 0, [item("neovitae:raw_spiritus_catalyst")], "Raw Crystal Catalyst", deps=["nv_tau_oil"], xp=60,
      optional=True, tokens=1, mirror="5ACB4565C6B2466C", subtitle="Optional: coax crystals out of Spiritus", desc=[
        "&eWhat:&r the Raw Crystal Catalyst helps Spiritus crystals form.",
        "&eChemistry:&r one ingredient is sulfur dust (S): the same element the Athanor bakes out of netherrack and the pack's acid lines are built on.",
        "&eHow:&r nether wart, Tau Oil, sulfur dust and a potato in the Hellfire Forge.",
        "&eTip:&r MI and the Athanor both make sulfur; you'll have spare by now."]),
    Q("nv_crucible", 0, 0, [item("neovitae:vas_maleficum")], "Spiritus Crucible", deps=["nv_master"], xp=60, optional=True, tokens=1,
      section=AURA, mirror="298458E916F65407", subtitle="Optional: feed Spiritus into the air", desc=[
        "&eWhat:&r every chunk has a Spiritus aura. The Crucible burns Spiritus crystals into it, so the chunk runs thick with one aspect.",
        "&eHow:&r a cauldron, deepslate, lapis and a diamond in the Hellfire Forge.",
        "&eTip:&r a chunk thick with an aspect is how you fill a gem with that aspect."]),
    Q("nv_gauge", 0, 0, [item("neovitae:spiritus_gauge")], "Spiritus Aura Gauge", deps=["nv_crucible"], xp=50, optional=True, tokens=1,
      mirror="56DDCB2865CEB9D3", subtitle="Optional: read the aura", desc=[
        "&eWhat:&r the gauge shows how much Spiritus, and of which aspect, hangs over the chunk you stand in.",
        "&eHow:&r gold, redstone, glass and a demon (aspect) crystal in the Hellfire Forge.",
        "&eTip:&r check it before you start a ritual that draws on the aura."]),
    Q("nv_crystallarium", 0, 0, [item("neovitae:crystallarium_maleficum"), item("neovitae:raw_spiritus_crystal")], "Crystallarium",
      deps=["nv_gauge"], xp=75, optional=True, tokens=1, mirror="2E22A601DC126B7B", subtitle="Optional: grow crystals from nothing", desc=[
        "&eWhat:&r the Crystallarium grows Spiritus crystal clusters from the aura around it.",
        "&eChemistry:&r real crystals grow the same way in principle: from a saturated medium, onto a seed, one layer at a time.",
        "&eHow:&r a Hellfire Forge, deepslate, lapis and glass in the Hellfire Forge. A Raw Crystal Cluster is 4 raw crystal shards, also forged.",
        "&eTip:&r Fortune on the harvest scales with how thick the chunk's aura is."]),
    Q("nv_aspects", 0, 0, [anyof(["neovitae:spiritus_ruina_shard", "neovitae:spiritus_nihilum_shard",
                                   "neovitae:spiritus_vindicta_shard", "neovitae:spiritus_invictus_shard"])],
      "An Aspected Crystal", deps=["nv_crystallarium"], xp=75, optional=True, tokens=1, mirror="4393ADF3E4C8B0D4",
      subtitle="Optional: any one aspect", desc=[
        "&eWhat:&r Spiritus has four aspects: Ruina, Nihilum, Vindicta and Invictus. Each crystal carries one, and each fuels different recipes and rites.",
        "&eHow:&r grow crystals in an aspected aura; JEI shows how each aspect's crystal is made. Any one completes this quest.",
        "&eTip:&r one chunk per aspect keeps the auras from mixing."]),
    Q("nv_fractura", 0, 0, [tick()], "Crystallum Fractura", deps=["nv_crystallarium"], xp=75, optional=True, tokens=1,
      mirror="7B293C32824033F9", icon="neovitae:raw_spiritus_crystal", subtitle="Optional: let a ritual do the harvest", desc=[
        "&eWhat:&r the Crystallum Fractura ritual harvests grown Spiritus crystals (and amethyst) around it and speeds their growth.",
        "&eHow:&r its stones are easiest to place with the Tenebrae Ritual Diviner. Tick the box once it's running.",
        "&eTip:&r attune it to one aspect with the Ritual Configurator for better yields of that aspect."]),
], links=[("gs_iron", -2, 0), ("t3_analog", 0, 0), ("t4_circuit", 0, 0), ("t2_hydrogen", 0, 0)], mirror="neo_vitae")
