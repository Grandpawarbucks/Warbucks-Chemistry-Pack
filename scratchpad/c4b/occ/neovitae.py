"""Quest chapter: neovitae (Neo Vitae blood magic). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

# Recipes checked against neovitae-1.21.1-1.1.44.jar (data/neovitae/recipe) and its guide book. Pack gates
# (pack/kubejs/server_scripts/phase5_neovitae.js): the Athanor needs MI analog circuits (LV); the Tenebrae scribe tool
# moves to the Tabula Vitae and needs 2 hydrogen + an MI electronic circuit (MV); the Flight flask fusion needs
# 2 hydrogen; Athanor ore yields are capped at 2x per ore block; meteor catalysts and Nether Star from diamond are gone.
# Generated material items exist only for pack/config/neovitae/materials.json (no netherite scrap material).
# Spine: altar -> orb -> Tabula Vitae -> runes -> Apprentice -> Magician -> Athanor (LV) -> blood shard -> Magus ->
# Tenebrae (MV) -> Demon Realm metal -> Dominus -> Divinus.

CHAPTER = Chapter("neovitae", "Neo Vitae", "neovitae:blood_orb_weak",
        ["Blood magic: an altar that drinks, orbs that remember, and rituals carved in stone."], SIDE, [
    # --- First steps -------------------------------------------------------------------------------------------
    Q("nv_altar", 0, 0, [item("neovitae:ara_vitae")], "Ara Vitae", deps=["gs_iron"], xp=40,
      subtitle="An altar that runs on life", desc=[
        "&6You remember that every power has a price, and that the oldest price was always blood.&r",
        "&eWhat:&r the Ara Vitae is the heart of Neo Vitae. It turns life into Essentia Vitae (EV) and uses it to transmute items placed on top.",
        "&eChemistry:&r blood is about 55% plasma (mostly water, salts and proteins) and 45% cells. Its red comes from haemoglobin, an iron(II) complex that carries O₂.",
        "&eHow:&r a furnace, 3 gold ingots and 4 deepslate (the mod's 'vitae stone') in a crafting table.",
        "&eTip:&r the guide book, Scriptura Vitae, is a book with 4 redstone; it shows every multiblock."]),
    Q("nv_orb", 2, 0, [item("neovitae:blood_orb_weak")], "Novicius Orb", deps=["nv_altar"], xp=40,
      subtitle="A diamond that holds your blood", desc=[
        "&eWhat:&r an Orb of Vitae is your personal EV network. Right-click it to bleed into it; machines and sigils draw from it anywhere.",
        "&eChemistry:&r the orb starts as a diamond: pure carbon in a tetrahedral lattice, hard enough to hold whatever the altar pours into it.",
        "&eHow:&r place a diamond on the empty altar and stand close. With no blood of its own, the altar draws from anyone nearby.",
        "&eTip:&r watch your hearts while bleeding. Eat well first; regeneration is your fuel."]),
    Q("nv_rasa", 4, 0, [item("neovitae:tabula_rasa", 8)], "Tabula Rasa", deps=["nv_orb"], xp=30,
      subtitle="Blank slates for everything", desc=[
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
    Q("nv_daggers", 8, 1.5, [item("neovitae:throwing_dagger", 16)], "Throwing Daggers", deps=["nv_table"], xp=30,
      subtitle="Wounds that leave something behind", desc=[
        "&eWhat:&r creatures killed with throwing daggers drop Spiritus, the residue of a soul. The Hellfire Forge burns it.",
        "&eHow:&r 2 iron ingots and a string in the Tabula Vitae make 16 daggers.",
        "&eTip:&r a Sentient Sword collects Spiritus much faster once you have one."]),
    Q("nv_scribe", 8, -1.5, [item("neovitae:arcane_scribe_tool")], "Arcane Scribe Tool", deps=["nv_table"], xp=30,
      subtitle="Draw circles on the ground", desc=[
        "&eWhat:&r the Arcane Scribe Tool draws an Alchemy Array. Drop two items into an array and it crafts a sigil or casts an effect.",
        "&eChemistry:&r it is made of redstone, white dye, gunpowder and coal: a pigment, a binder and a little fire.",
        "&eHow:&r Tabula Vitae, then right-click the ground with the tool.",
        "&eTip:&r JEI lists every array recipe under the Alchemy Array category."]),
    Q("nv_divination", 10, -1.5, [item("neovitae:sigil_divination")], "Divination Sigil", deps=["nv_scribe"], xp=30,
      subtitle="Read your own blood", desc=[
        "&eWhat:&r the Divination Sigil shows how much EV is in your network and in an altar you look at.",
        "&eHow:&r an Alchemy Array with redstone first, then a Tabula Rasa.",
        "&eTip:&r keep it handy while you build up the altar; it tells you when a craft has enough EV."]),
    Q("nv_sigils", 12, -3, [item("neovitae:sigil_water"), item("neovitae:sigil_lava")], "Water and Lava Sigils",
      deps=["nv_divination"], xp=40, optional=True, tokens=1, subtitle="Carry a spring and a volcano", desc=[
        "&eWhat:&r the Water Sigil places water and the Lava Sigil places lava, each for a little EV.",
        "&eChemistry:&r lava plus cobblestone in the Tabula Vitae gives sulfur: volcanoes really do deposit sulfur where their gases (H₂S, SO₂) cool at vents.",
        "&eHow:&r make Reagent Water and Reagent Lava in the Tabula Vitae, then put each in an array with a Tabula Rasa.",
        "&eTip:&r the Water Sigil also replaces water bottles in some Tabula recipes."]),
    # --- Altar tiers -------------------------------------------------------------------------------------------
    Q("nv_runes", 10, 0, [item("neovitae:rune_blank", 8)], "Blank Runes", deps=["nv_table"], xp=40,
      subtitle="The altar grows downward", desc=[
        "&eWhat:&r runes around the altar raise its tier. Tier II is a ring of 8 runes one block below the altar.",
        "&eHow:&r deepslate, a Tabula Rasa and your orb in a crafting table (the orb is not used up). Scriptura Vitae shows each tier's layout.",
        "&eTip:&r blank runes count for the structure; upgraded runes add their effect on top."]),
    Q("nv_rune_types", 12, 1.5, [item("neovitae:rune_sacrifice"), item("neovitae:rune_speed")], "Sacrifice and Speed",
      deps=["nv_runes"], xp=40, subtitle="Runes that do something", desc=[
        "&eWhat:&r Runes of Sacrifice give more EV per creature killed near the altar; Speed Runes make it craft faster.",
        "&eHow:&r both start from a blank rune. Sacrifice needs a Tabula Robur, gold and an Apprentice orb or better; Speed needs Tabula Rasa and sugar.",
        "&eTip:&r a mob farm next to a ring of Sacrifice runes feeds the altar while you're away."]),
    Q("nv_apprentice", 12, 0, [item("neovitae:blood_orb_apprentice")], "Discipulus Orb", deps=["nv_runes"], xp=75, size=1.5,
      subtitle="Tier II: the second orb", desc=[
        "&6You remember the weight of a bigger vessel, and how much more it could hold.&r",
        "&eWhat:&r a bigger orb holds more EV and unlocks tier-2 recipes, including the Sacrifice rune and Tabula Robur.",
        "&eHow:&r a block of redstone on a Tier II altar (8 runes), 5,000 EV.",
        "&eTip:&r keep the old orb; Tabula recipes that need a lower orb accept a higher one."]),
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
    # --- Spiritus ----------------------------------------------------------------------------------------------
    Q("nv_forge", 10, 3, [item("neovitae:hellfire_forge")], "Hellfire Forge", deps=["nv_daggers"], xp=40,
      subtitle="A forge that burns souls", desc=[
        "&eWhat:&r the Hellfire Forge combines items using Spiritus in its gem slot instead of fuel.",
        "&eHow:&r iron ingots, an iron block, deepslate and a Tabula Rasa. Kill mobs with throwing daggers and pick up the Spiritus they drop.",
        "&eTip:&r a recipe only starts if the gem holds at least its minimum Spiritus. JEI shows both numbers."]),
    Q("nv_gem", 12, 4.5, [item("neovitae:spiritus_gem_petty")], "Petty Spiritus Gem", deps=["nv_forge"], xp=40,
      subtitle="Somewhere to keep it", desc=[
        "&eWhat:&r Spiritus gems store Spiritus and soak up any you pick up, so it stops cluttering your inventory.",
        "&eChemistry:&r lapis lazuli is mostly lazurite, a sodium aluminium silicate whose blue comes from trapped S₃⁻ radical ions.",
        "&eHow:&r redstone, a gold ingot, glass and lapis in the Hellfire Forge.",
        "&eTip:&r bigger gems come later from the same forge; each holds much more."]),
    Q("nv_sentient", 14, 4.5, [item("neovitae:sentient_sword")], "Sentient Sword", deps=["nv_gem"], xp=50,
      subtitle="A blade that takes its share", desc=[
        "&eWhat:&r the Sentient Sword collects Spiritus from every kill and hits harder the more Spiritus you carry.",
        "&eHow:&r an iron sword in the Hellfire Forge with a Petty Spiritus Gem as catalyst (the gem stays).",
        "&eTip:&r the axe, pickaxe, shovel and scythe work the same way."]),
    # --- Rituals and the Athanor -------------------------------------------------------------------------------
    Q("nv_magician", 16, 0, [item("neovitae:blood_orb_magician")], "Veneficus Orb", deps=["nv_apprentice", "nv_robur"], xp=100,
      size=1.5, subtitle="Tier III: rituals open", desc=[
        "&eWhat:&r the third orb. With it come ritual stones, the Master Ritual Stone and activation crystals.",
        "&eChemistry:&r gold is the input: it barely reacts with anything, which is why it lasts in the ground as native metal.",
        "&eHow:&r a block of gold on a Tier III altar, 25,000 EV. Scriptura Vitae shows the Tier III layout.",
        "&eTip:&r Runes of Capacity and Charging help the altar hold enough EV for this craft."]),
    Q("nv_ritual", 18, -1.5, [item("neovitae:master_ritual_stone"), item("neovitae:ritual_stone", 8),
                               item("neovitae:activation_crystal_weak")], "Master Ritual Stone",
      deps=["nv_magician"], xp=75, subtitle="Carve the circle", desc=[
        "&eWhat:&r a ritual is a Master Ritual Stone surrounded by inscribed ritual stones in a fixed pattern, started with an activation crystal.",
        "&eHow:&r ritual stones from obsidian, Tabula Robur and a Discipulus orb; the master stone needs the Veneficus orb. The crystal is a Lava Crystal on the altar.",
        "&eTip:&r the Ritual Diviner places a whole ritual's stones for you, already inscribed."]),
    Q("nv_diviner", 20, -1.5, [item("neovitae:ritual_diviner")], "Ritual Diviner", deps=["nv_ritual"], xp=50,
      subtitle="Place a whole ritual at once", desc=[
        "&eWhat:&r the Ritual Diviner builds a chosen ritual around a Master Ritual Stone, stone by stone, from your inventory.",
        "&eHow:&r the four elemental inscription tools (ghast tear, obsidian, magma cream, lapis block on the altar) with diamonds and a stick.",
        "&eTip:&r useful early rites: Green Grove (crops), Harvest, Well of Suffering (EV from mobs) and Magnetism (ores, like a slow quarry)."]),
    Q("nv_athanor", 18, 1.5, [item("neovitae:athanor")], "Athanor", deps=["nv_magician", "t3_analog"], xp=100,
      subtitle="An alchemical furnace with a thermostat", desc=[
        "&eWhat:&r the Athanor is Neo Vitae's reaction chamber: ore processing, sulfur from netherrack, blood shards and the late gems.",
        "&eChemistry:&r a medieval athanor was a furnace that fed itself charcoal to hold one steady heat. Holding a temperature is a control problem, so here it needs analog circuits.",
        "&eHow:&r deepslate, 2 Tabula Animata, a furnace, a Veneficus orb and 2 MI analog circuits (LV). Tools go in its tool slot: cutting fluid, resonator, hydration cell.",
        "&eTip:&r it runs at half speed with no Raw Spiritus in the chunk and up to double speed when the chunk is full."]),
    Q("nv_ore", 20, 3, [anyof(["neovitae:iron_dust", "neovitae:gold_dust", "neovitae:copper_dust"], 8)], "Blood and Ore",
      deps=["nv_athanor"], xp=50, optional=True, tokens=1, subtitle="Cutting fluid and fragments", desc=[
        "&eWhat:&r with Cutting Fluid as its tool, the Athanor breaks an ore block into 2 fragments, then gravel, then dust.",
        "&eChemistry:&r in this pack the big ore multipliers belong to acids (HCl, H₂SO₄ in Mekanism): dissolving ore frees metal that crushing leaves behind.",
        "&eHow:&r Basic Cutting Fluid is plant oil, redstone, gunpowder, sugar, coal dust and water in the Tabula Vitae. Raw ore goes straight to 1 dust with a small bonus chance.",
        "&eTip:&r this is a magic route at the normal 2x cap, not a shortcut past the acid lines."]),
    # --- Demon Realm and the higher orbs -----------------------------------------------------------------------
    Q("nv_tau", 20, 0, [item("neovitae:weak_tau", 4)], "Tau Fruit", deps=["nv_ritual"], xp=75,
      subtitle="Something grows on the other side", desc=[
        "&eWhat:&r the ritual Breaching the Edge of Demon Realm builds a small dungeon that leads into the Demon Realm, where Tau fruit grows wild.",
        "&eHow:&r start the ritual on a Master Ritual Stone (the Diviner lists it); it needs a large EV pool. Bring armour and food.",
        "&eTip:&r replant Tau. A creature standing on the plant while it ripens turns it into Saturated Tau."]),
    Q("nv_shard", 22, 0, [item("neovitae:weak_blood_shard")], "Weak Blood Shard", deps=["nv_tau", "nv_athanor"], xp=100,
      subtitle="Concentrated life", desc=[
        "&eWhat:&r Weak Blood Shards open Tier IV: the Magus orb, stronger anointments and potion catalysts.",
        "&eHow:&r Saturated Tau (strong_tau) in the Athanor with a hydration cell as the tool and 3,200 mB of Essentia Vitae.",
        "&eTip:&r the Primitive Hydration Cell is cobblestone, a water bucket, a Tabula Rasa and a Veneficus orb."]),
    Q("nv_master", 24, 0, [item("neovitae:blood_orb_master")], "Magus Orb", deps=["nv_shard"], xp=150, size=1.5,
      subtitle="Tier IV: the deep end", desc=[
        "&6You remember the altar answering before you asked. Your blood and the stone keep the same time now.&r",
        "&eWhat:&r the fourth orb, for Tier IV recipes and the Awakened Activation Crystal.",
        "&eHow:&r a Weak Blood Shard on a Tier IV altar, 40,000 EV.",
        "&eTip:&r stock up EV first; the altar drains fast on big crafts."]),
    Q("nv_armour", 22, 3, [item("neovitae:sentient_plate")], "Sentient Armour", deps=["nv_magician"], xp=75,
      subtitle="Armour that trains itself", desc=[
        "&eWhat:&r Sentient Armour gains upgrades from what you do while wearing it: running, taking hits, mining, eating.",
        "&eHow:&r an Alchemy Array with Reagent Binding (glowstone, redstone, gunpowder, gold nugget) and an iron chestplate.",
        "&eTip:&r the Elytra upgrade only comes as a tome from Demon Realm loot; it glides like a normal elytra."]),
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
    Q("nv_hellforged", 26, 1.5, [item("neovitae:ingot_hellforged", 9)], "Hellforged Metal", deps=["nv_master"], xp=150,
      subtitle="Ore from the Demon Realm", desc=[
        "&eWhat:&r demonite ore lies deep in the Demon Realm's Endless dungeon. Its metal makes the Dominus orb and the reinforced runes.",
        "&eHow:&r the Highway to Hell ritual opens the Endless dungeon. Smelt or blast raw demonite into Hellforged Ingots.",
        "&eTip:&r Hellforged Dust, which better cutting fluids need, comes from ingots in the Athanor."]),
    Q("nv_archmage", 28, 0, [item("neovitae:blood_orb_archmage")], "Dominus Orb", deps=["nv_hellforged"], xp=200, size=1.5,
      subtitle="Tier V", desc=[
        "&eWhat:&r the fifth orb, made from a block of Hellforged metal.",
        "&eHow:&r a Hellforged Block on a Tier V altar, 80,000 EV. Tier V needs upgraded runes and capstones (see Scriptura Vitae).",
        "&eTip:&r Reinforced runes (netherite scrap + Hellforged Parts) double a rune's effect."]),
    Q("nv_transcendent", 30, 0, [item("neovitae:blood_orb_transcendent")], "Divinus Orb", deps=["nv_archmage"], xp=300,
      size=2.0, shape="gear", subtitle="Tier VI: the last altar", desc=[
        "&6You remember the last altar: not a tool any more, but a promise kept in stone.&r",
        "&eWhat:&r the sixth and final orb. It opens the Deus rites and the top of Vitaemancy.",
        "&eHow:&r a Crystal Cluster (sculk, Tabula Aetherea, a Weak Blood Shard and a Nether Star in the Hellfire Forge) on a Tier VI altar, 200,000 EV.",
        "&eTip:&r Nether Stars only come from the Wither here; a diamond can't be turned into one."]),
    Q("nv_tome", 18, 4.5, [item("neovitae:experience_tome")], "Tome of Peritia", deps=["nv_magician"], xp=40,
      optional=True, tokens=1, subtitle="Bottle your experience", desc=[
        "&eWhat:&r the Tome of Peritia stores experience levels so you can spend them later.",
        "&eHow:&r an enchanted book, lapis blocks, gold, string, 2 Tabula Animata and a Veneficus orb.",
        "&eTip:&r the Array of Liquified Experience moves stored XP into a tank as fluid."]),
], links=[("gs_iron", -2, 0), ("t3_analog", 0, 0), ("t4_circuit", 0, 0), ("t2_hydrogen", 0, 0)])
