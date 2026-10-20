"""Quest chapter: t1. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t1", "II. Steam and Steel", "modern_industrialization:coke",
        ["Destructive distillation turns coal into coke, and coke turns iron into steel.",
         "At the end of this chapter, matter itself opens up to you."], MAIN, [
    # --- the coke oven --------------------------------------------------------------------
    Q("t1_bricks", 0, 0, [item("minecraft:bricks", 16)], "A Kiln's Worth of Bricks", subtitle="The Coke Oven's shell", deps=["t0_pump"], xp=30, desc=[
        "&6Smoke rising from a hill of earth, and what came out of it burning hotter than anything before. That memory is older than any city.&r",
        "&eWhat:&r The Coke Oven is built from ordinary brick blocks: one ring of 8 for the controller, and more for its walls.",
        "&eChemistry:&r Firing clay drives out the water bound in its minerals and fuses the grains, turning soft mud into ceramic.",
        "&eHow:&r Smelt clay balls into bricks, then craft 4 bricks into a brick block.",
        "&eTip:&r Rivers and swamps are full of clay. Ultimine a clay patch."]),
    Q("t1_coke_oven", 2, 0, [item("modern_industrialization:coke_oven")], "The Coke Oven", subtitle="The controller block", deps=["t1_bricks"], xp=50, desc=[
        "&eWhat:&r The controller of a small multiblock that bakes coal into coke.",
        "&eChemistry:&r Coal is carbon mixed with many other compounds. Bake it without air and those volatiles are driven off. This is &edestructive distillation&r.",
        "&eHow:&r 8 brick blocks around a furnace."]),
    Q("t1_hatches", 4, 0, [item("modern_industrialization:bronze_item_input_hatch"), item("modern_industrialization:bronze_item_output_hatch"),
                           item("modern_industrialization:bronze_fluid_input_hatch")],
      "Hatches", subtitle="How things get in and out of a multiblock", deps=["t1_coke_oven"], xp=40, desc=[
        "&eWhat:&r MI multiblocks have no inventory of their own. Hatches built into the walls take items and steam in and push products out.",
        "&eHow:&r An item hatch is a hopper on a bronze machine casing; a fluid hatch is a bronze tank on a casing (check JEI for the output versions).",
        "&eTip:&r While you hold a hatch, MI can highlight the spots where it fits (a client option in MI's config)."]),
    Q("t1_coke_build", 6, 0, [tick()], "Build the Coke Oven", subtitle="A 3x3x3 brick cube with hatches", deps=["t1_hatches"], xp=40, desc=[
        "&eWhat:&r Put the shell together and the controller comes to life.",
        "&eHow:&r Press R on the Coke Oven in JEI or open the MI guidebook to see the 3D layout: a 3x3x3 cube of brick blocks with the controller in one face. Swap wall bricks for hatches: item in, item out, steam in, and a fluid output for creosote.",
        "&eTip:&r Pipe steam from your boiler into the fluid input hatch. Click the checkmark once the controller shows it's formed."]),
    Q("t1_fluid_out", 0, 0, [item("modern_industrialization:bronze_fluid_output_hatch")], "A Way Out for Tar", subtitle="A fluid output hatch for the Coke Oven",
      deps=["t1_hatches"], xp=25, desc=[
        "&eWhat:&r Coking coal also drives out a liquid. Without a fluid output hatch it has nowhere to go.",
        "&eChemistry:&r The volatile part of coal leaves as gas and condenses into tar as it cools. Real coke works collect it, because coal tar is a feedstock, not waste.",
        "&eHow:&r A bronze machine casing on top of a bronze tank. Swap one wall brick of the Coke Oven for it.",
        "&eTip:&r Pipe it straight into a tank or a boiler so it never fills up."]),
    Q("t1_coke", 8, 0, [item("modern_industrialization:coke", 16)], "Coke", subtitle="Nearly pure carbon, burns hotter than coal", deps=["t1_coke_build"], xp=40, desc=[
        "&eWhat:&r Coke is exactly what a blast furnace needs: strong, porous, nearly pure carbon.",
        "&eChemistry:&r With the hydrogen, sulfur and tars baked out, what's left is a carbon skeleton that burns hot and clean.",
        "&eHow:&r Feed coal into the item input hatch. Each coal becomes 1 coke in 30 seconds.",
        "&eTip:&r Coal dust works too and comes out as coke dust, which saves a grinding step later."]),
    Q("t1_creosote", 8, 2, [item("modern_industrialization:creosote_bucket")], "Byproduct: Creosote", subtitle="The tar driven out of coal", deps=["t1_coke_build", "t1_fluid_out"], xp=40, desc=[
        "&eWhat:&r Half the time, coking a coal also yields 500 mB of &ecreosote&r. Nothing is wasted in chemistry: creosote is a boiler fuel.",
        "&eChemistry:&r Coal-tar creosote is a mix of phenols, cresols and ring-shaped hydrocarbons, the same family of compounds that makes tar smell the way it does.",
        "&eHow:&r Pipe it out of the fluid output hatch into a tank, or straight into a boiler."]),
    Q("t1_lubricant", 10, 2, [item("modern_industrialization:lubricant_bucket")], "Lubricant", subtitle="Creosote + redstone", deps=["t1_creosote"], xp=30, desc=[
        "&eWhat:&r The Steam Cutting Machine needs lubricant as cutting fluid. Now you can finally run it.",
        "&eHow:&r In the Steam Mixer, 500 mB of creosote and 1 redstone make 500 mB of lubricant.",
        "&eTip:&r Each cut uses only 1 mB, so one bucket lasts a very long time. The Cutting Machine now makes your steel rods and bolts."]),

    # --- steel ----------------------------------------------------------------------------
    Q("t1_coke_dust", 10, 0, [item("modern_industrialization:coke_dust", 4)], "Coke Dust", subtitle="Carbon, powdered", deps=["t1_coke"], xp=25, desc=[
        "&eWhat:&r Steel is mixed as dust, so the carbon has to be a powder too.",
        "&eChemistry:&r Coke is the reducing agent in a real blast furnace: it pulls oxygen out of iron ore and supplies the carbon that becomes steel.",
        "&eHow:&r Grind coke in the Steam Macerator, or coke coal dust directly in the Coke Oven."]),
    Q("t1_iron_dust", 12, 0, [item("modern_industrialization:iron_dust", 7)], "Iron Dust", subtitle="Seven parts of the recipe", deps=["t1_coke_dust"], xp=25, desc=[
        "&eWhat:&r The other ingredient of steel.",
        "&eHow:&r Grind iron ingots in the Steam Macerator or the Forge Hammer (1 ingot makes 1 dust).",
        "&eTip:&r Macerating iron ore gives 2 raw iron per ore, which smelts into more ingots than mining alone."]),
    Q("t1_uncooked", 14, 0, [item("modern_industrialization:uncooked_steel_dust", 7)], "Uncooked Steel", subtitle="7 iron dust + 2 coke dust", deps=["t1_iron_dust"], xp=30, desc=[
        "&eWhat:&r A blend of iron and carbon, ready for the blast furnace.",
        "&eChemistry:&r Real steel holds far less carbon than this mix suggests, but the idea is right: carbon is the ingredient that turns soft iron into steel.",
        "&eHow:&r Craft 7 iron dust with 2 coke dust to get 7 uncooked steel dust."]),
    Q("t1_sbf_parts", 12, -2, [item("modern_industrialization:fire_clay_bricks", 16), item("minecraft:blast_furnace")], "Blast Furnace Materials",
      subtitle="A stack of firebricks and a blast furnace", deps=["t1_coke"], xp=40, desc=[
        "&eWhat:&r The Steam Blast Furnace is a tower of fire clay bricks, hotter than anything you've built.",
        "&eHow:&r Make fire clay bricks as in Chapter I (the Steam Macerator grinds bricks into brick dust now). A vanilla blast furnace is 5 iron, a furnace and 3 smooth stone.",
        "&eTip:&r Automate it: macerator → crafting → steam furnace. You'll want a lot of these."]),
    Q("t1_blast", 15, -2, [item("modern_industrialization:steam_blast_furnace")], "The Steam Blast Furnace", subtitle="Hot enough to dissolve carbon in iron",
      deps=["t1_sbf_parts"], xp=75, desc=[
        "&eWhat:&r A multiblock that gets hot enough to melt iron and dissolve carbon into it.",
        "&eHow:&r Craft the controller from 8 fire clay brick blocks around a blast furnace. Check the structure in JEI: a 3x3 tower, four blocks tall, with bronze hatches for items and steam.",
        "&eTip:&r Some later recipes in this furnace need a steel hatch. Steel itself only needs bronze ones."]),
    Q("t1_steel", 18, 0, [item("modern_industrialization:steel_ingot", 8)], "Steel", subtitle="Iron and carbon in the right ratio",
      deps=["t1_blast", "t1_uncooked"], xp=100, size=1.5, items=[("modern_industrialization:steel_ingot", 16)], desc=[
        "&6Iron that bends without breaking. You once forged weapons for gods out of something very like this.&r",
        "&eWhat:&r Iron with a small, controlled amount of carbon (about 0.2-2%) is &esteel&r: strong, tough, and the backbone of every machine to come.",
        "&eChemistry:&r Carbon atoms sit in the gaps between iron atoms and stop the layers sliding. Too much carbon and you get brittle cast iron. Chemistry is about the right ratio.",
        "&eHow:&r Put uncooked steel dust in the blast furnace's item input hatch. Each dust becomes 1 steel ingot in 30 seconds."]),
    Q("t1_steel_paxel", 18, 3, [item("mekanismtools:steel_paxel")], "Steel Paxel", subtitle="Diamond-tier mining, without diamonds", deps=["t1_steel"], xp=40, desc=[
        "&eWhat:&r Mekanism's steel tools are &ediamond tier&r: a steel paxel mines obsidian, which the Combiner needs, and lasts far longer than iron.",
        "&eChemistry:&r A little carbon in iron makes it much harder: carbon atoms in the gaps of the iron lattice pin it so the layers can't slip.",
        "&eHow:&r A steel pickaxe, axe and shovel with 2 sticks (check JEI).",
        "&eTip:&r No diamonds needed for obsidian now. Save your diamonds for the Combiner itself."]),
    Q("t1_steel_boiler", 18, -3, [item("modern_industrialization:steel_boiler")], "Steel Boiler", subtitle="More steam per tick", deps=["t1_steel"], optional=True, tokens=1, xp=60, desc=[
        "&eWhat:&r More steam per tick than the bronze boiler.",
        "&eHow:&r Steel plates, a steel tank, a furnace and 3 fire clay brick blocks (check JEI).",
        "&eTip:&r Steel versions of the steam machines (macerator, compressor and others) run faster too."]),
    Q("t1_steel_plate", 20, 0, [item("modern_industrialization:steel_plate", 8)], "Steel Plates", subtitle="For gears, pipes and Alchemistry", deps=["t1_steel"], xp=40, desc=[
        "&eWhat:&r The Dissolver and Combiner are framed in steel plates, and steel gears need them too.",
        "&eHow:&r The Steam Compressor presses 1 steel ingot into 1 plate.",
        "&eTip:&r You need at least 8 for the Dissolver and Combiner, plus more for gears. Keep the compressor busy."]),
    Q("t1_steel_gear", 22, -3, [item("modern_industrialization:steel_gear", 2)], "Steel Gears", subtitle="Plates, bolts and a ring, in steel", deps=["t1_steel_plate", "t1_lubricant"], xp=30, desc=[
        "&eWhat:&r Steel machine casings (the core of every LV machine in Chapter IV) and item pipes need steel gears.",
        "&eHow:&r Same pattern as bronze: 4 steel plates, 4 steel bolts and 1 steel ring (check JEI).",
        "&eTip:&r Steel rods, bolts and rings come from the Forge Hammer, or from the Cutting Machine now that you have lubricant."]),
    Q("t1_item_pipes", 24, -3, [item("modern_industrialization:item_pipe", 16)], "Item Pipes", subtitle="Automate the item flow", deps=["t1_steel_gear"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r MI item pipes move items between machines, so dust, ingots and coke flow on their own.",
        "&eHow:&r 6 bronze curved plates and 2 steel gears make 16 pipes.",
        "&eTip:&r Right-click a pipe end with an empty hand to switch it between insert and extract."]),

    # --- power and the Alchemistry machines -----------------------------------------------
    Q("t1_copper_gen", 20, 3, [item("generatorgalore:copper_generator")], "A Simple Generator", subtitle="Burn fuel, make Forge Energy", deps=["t1_redstone"], xp=30, desc=[
        "&eWhat:&r Generator Galore's Copper Generator burns solid fuel into FE (Forge Energy) and pushes it into machines it touches.",
        "&eChemistry:&r Burning releases the chemical energy stored in carbon bonds as heat; the generator turns that heat into electricity.",
        "&eHow:&r Copper ingots around a furnace, with a block of redstone (check JEI)."]),
    Q("t1_power", 22, 3, [item("generatorgalore:iron_generator")], "Forge Energy", subtitle="Enough FE to run the Dissolver", deps=["t1_copper_gen"], xp=50, desc=[
        "&eWhat:&r Some machines run on &eFE&r instead of steam. You'll need it for the Dissolver.",
        "&eHow:&r Upgrade the Copper Generator: surround it with iron ingots and a block of redstone to make the Iron Generator.",
        "&eTip:&r A Mekanism Heat Generator or Powah Furnator also works. Burn coke for long runs."]),
    Q("t1_dissolver_parts", 22, -1, [item("minecraft:magma_block", 2), item("minecraft:piston", 2)], "Heat and Pressure", subtitle="Magma and pistons for the Dissolver",
      deps=["t1_steel_plate"], xp=30, desc=[
        "&eWhat:&r Besides steel plates and a bronze machine casing, the Dissolver needs 2 magma blocks and 2 pistons.",
        "&eChemistry:&r Magma blocks are rock hot enough to glow, a fitting heat source for a machine that tears compounds apart.",
        "&eHow:&r Magma blocks generate in underwater ravines and caves, or can be crafted from 4 magma cream. Pistons need iron, redstone, cobblestone and planks."]),
    Q("t1_combiner_parts", 22, 1, [item("minecraft:diamond"), item("minecraft:obsidian", 2)], "Pressure and Precision", subtitle="A diamond and obsidian for the Combiner",
      deps=["t1_steel_plate", "t1_steel_paxel"], xp=30, desc=[
        "&eWhat:&r The Combiner needs a diamond, 2 obsidian and a piston, plus steel plates and a casing.",
        "&eChemistry:&r Obsidian is volcanic glass: lava that cooled too fast for crystals to form.",
        "&eHow:&r Pour water onto a lava source to make obsidian. Your &esteel paxel&r is diamond tier, so it mines obsidian; no diamond pickaxe needed. Diamonds are most common near the bottom of the world."]),
    Q("t1_dissolver", 25, -1, [item("alchemistry:dissolver")], "The Dissolver", subtitle="Break anything into its elements",
      deps=["t1_dissolver_parts", "t1_power"], xp=150, size=1.75, shape="hexagon", items=[("minecraft:experience_bottle", 16)], desc=[
        "&6Your first gift returns: look at anything and know what it's made of.&r",
        "&eWhat:&r The Dissolver breaks any item into the &eelements and compounds&r it's made of.",
        "&eHow:&r Steel plates, pistons, magma blocks and a Bronze Machine Casing (check JEI). Power it with FE, insert anything, and collect the elements.",
        "&eTip:&r Some things dissolve into compounds first. Put those back in to break them down further."]),
    Q("t1_combiner", 25, 1, [item("alchemistry:combiner")], "The Combiner", subtitle="Build items back up from elements",
      deps=["t1_combiner_parts", "t1_power"], xp=150, size=1.75, shape="hexagon", desc=[
        "&6And the other half of the gift: what you can take apart, you can put back together.&r",
        "&eWhat:&r The reverse: arrange elements and the Combiner builds them back into items and blocks.",
        "&eHow:&r Steel plates, a diamond, obsidian, a piston and a Bronze Machine Casing (check JEI). It runs on FE too.",
        "&eTip:&r Its first real job comes in Chapter IV: sulfuric acid for the lead-acid redstone battery. Taking the world apart and rebuilding it is what this pack is about."]),
    Q("t1_cellulose", 27, -3, [item("chemlib:cellulose", 4)], "Wood, Undone", subtitle="Logs dissolve into cellulose", deps=["t1_dissolver"], xp=40, desc=[
        "&eWhat:&r Your first compound out of the Dissolver.",
        "&eChemistry:&r Cellulose is a chain of glucose units, (C₆H₁₀O₅)ₙ. It's the most common organic compound on Earth and gives wood its strength.",
        "&eHow:&r Dissolve logs: each log gives 1 cellulose. Dissolve the cellulose again to get 6 carbon, 10 hydrogen and 5 oxygen."]),
    Q("t1_graphite", 27, -1, [item("chemlib:graphite", 4)], "Graphite", subtitle="Coal and charcoal, sorted", deps=["t1_dissolver"], xp=40, desc=[
        "&eWhat:&r Coal and charcoal dissolve into graphite, a pure form of carbon.",
        "&eChemistry:&r In graphite, carbon atoms form flat sheets of hexagons that slide over each other. That's why pencil 'lead' leaves a mark.",
        "&eHow:&r Dissolve coal or charcoal: each gives 2 graphite. Each graphite dissolves into 4 carbon."]),
    Q("t1_elements", 29, 0, [item("chemlib:hydrogen", 16), item("chemlib:carbon", 16), item("chemlib:oxygen", 16), item("chemlib:iron", 16)],
      "First Entries in the Periodic Table", subtitle="H, C, O and Fe", deps=["t1_cellulose", "t1_graphite", "t1_combiner"], xp=200, desc=[
        "&eWhat:&r Dissolve whatever you have lying around and collect your first elements: &eH&r (1), &eC&r (6), &eO&r (8), &eFe&r (26).",
        "&eChemistry:&r The number is the &eatomic number&r: how many protons are in the nucleus. Change it and you have a different element.",
        "&eHow:&r Cellulose gives carbon, hydrogen and oxygen; graphite gives carbon. Each iron ingot gives 16 iron.",
        "&eTip:&r The Periodic Table chapter tracks every element from here on."]),
    Q("t1_compound", 31, 0, [item("chemlib:water", 4)], "Your First Synthesis", subtitle="2 H + 1 O → H₂O", deps=["t1_elements"], xp=200, size=1.5, shape="hexagon", desc=[
        "&6Two hydrogen, one oxygen. You once filled oceans with this; today it's a few drops. It's a start, and it's yours.&r",
        "&eWhat:&r Build water from its elements in the Combiner. It's a trivial compound, but you made it from scratch. That's the point.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O. Hydrogen and oxygen share electrons in covalent bonds, and the bent shape of the molecule makes it polar.",
        "&eHow:&r Pick water as the target in the Combiner's GUI, then supply 2 hydrogen and 1 oxygen per water."]),

    Q("t1_redstone", 0, 0, [item("minecraft:redstone_block")], "Blocks of Redstone", subtitle="One for each generator", deps=["t1_steel"], xp=25, desc=[
        "&eWhat:&r The Copper Generator and its Iron upgrade each have a block of redstone in their recipe, so you'll need two in all.",
        "&eHow:&r 9 redstone dust make 1 block. Redstone ore sits deep, mostly below Y 16, and needs an iron pickaxe.",
        "&eTip:&r Ultimine a redstone vein: one gives plenty, and lubricant needs dust too."]),

    # --- optional side quests -------------------------------------------------------------
    Q("t1_opt_coke_block", 8, -3, [item("modern_industrialization:coke_block", 4)], "Fuel Reserve", subtitle="Four blocks of coke", deps=["t1_coke"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r A stockpile of coke for boilers, generators and future steel.",
        "&eChemistry:&r Coke is porous. Air flows through it, which is why it burns so hot and steadily in a furnace.",
        "&eTip:&r A full Coke Oven running overnight fills these quickly."]),
    Q("t1_opt_steel_machines", 16, 3, [item("modern_industrialization:steel_upgrade"), item("modern_industrialization:steel_macerator")], "Steel Upgrades",
      subtitle="Faster steam machines", deps=["t1_steel"], optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r A Steel Upgrade turns a bronze steam machine into its faster steel version.",
        "&eHow:&r Craft Steel Upgrades from a steel machine casing, bronze parts, fluid pipes and fire clay bricks (check JEI), then combine one with the Bronze Macerator.",
        "&eTip:&r Upgrade the machines that bottleneck you first, usually the macerator."]),
    Q("t1_opt_unalloy", 29, -3, [item("chemlib:copper", 16), item("chemlib:tin", 16)], "Proof of Composition", subtitle="Copper and tin, as elements", deps=["t1_elements"],
      optional=True, tokens=1, xp=30, desc=[
        "&eWhat:&r Dissolve a copper ingot and a tin ingot to see the two elements that make bronze.",
        "&eChemistry:&r Copper is element 29 and tin is element 50. Every bronze ingot you made in Chapter I was these two, mixed.",
        "&eHow:&r Each copper or tin ingot dissolves into 16 of its element."]),
    Q("t1_opt_sugar", 31, -3, [item("chemlib:sucrose")], "Sweet Chemistry", subtitle="Sugar is C₁₂H₂₂O₁₁", deps=["t1_elements"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Dissolve sugar into sucrose, then sucrose into its elements.",
        "&eChemistry:&r Sucrose is glucose and fructose joined together. Dissolved, it gives 12 carbon, 22 hydrogen and 11 oxygen.",
        "&eHow:&r Sugar cane makes sugar; the Dissolver turns 1 sugar into 1 sucrose."]),
    Q("t1_opt_diamond", 29, 3, [item("chemlib:graphite", 128)], "Carbon Is Carbon", subtitle="Dissolve a diamond", deps=["t1_elements"], optional=True, tokens=2, xp=40, desc=[
        "&eWhat:&r A diamond dissolves into 128 graphite. Expensive, but it proves a point.",
        "&eChemistry:&r Diamond and graphite are both pure carbon, called &eallotropes&r. In diamond every atom bonds to four neighbours in 3D; in graphite, to three in flat sheets.",
        "&eTip:&r Don't dissolve your last diamond. You'll need them for machines."]),
    Q("t1_opt_steel_hatches", 0, 0, [item("modern_industrialization:steel_item_input_hatch"), item("modern_industrialization:steel_item_output_hatch"),
                                     item("modern_industrialization:steel_fluid_input_hatch")], "Steel Hatches", subtitle="One steel hatch makes a multiblock steel tier",
      deps=["t1_steel_gear"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r Steel hatches hold more than bronze ones, and a steam multiblock with at least one steel hatch is upgraded to steel tier: twice as fast, as long as the recipe stays within 4 EU/t.",
        "&eHow:&r Each is a steel machine casing (8 steel plates around a steel gear) with a hopper or a steel tank on top (check JEI for the output versions).",
        "&eTip:&r Swap one hatch on your Coke Oven and Steam Blast Furnace and both run at double speed."]),
    Q("t1_opt_packer", 0, 0, [item("modern_industrialization:steel_packer"), item("modern_industrialization:steel_unpacker")], "Packer and Unpacker",
      subtitle="Simple crafts, done by steam", deps=["t1_item_pipes"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r The Packer does small crafts on its own: blocks, double ingots and pipes. The Unpacker takes blocks back apart. Both exist only in steel.",
        "&eHow:&r A steel machine casing with bronze gears, fluid pipes and item pipes (check JEI; the Unpacker also needs bronze rods).",
        "&eTip:&r Pipe ingots into the Packer and store your metal as blocks: nine times fewer slots."]),
    Q("t1_opt_alloy_smelter", 0, 0, [item("extended_industrialization:steel_alloy_smelter")], "Steel Alloy Smelter", subtitle="Alloy ingots straight from nuggets",
      deps=["t1_steel_gear"], optional=True, tokens=1, xp=40, desc=[
        "&eWhat:&r An Extended Industrialization machine that melts metals together and pours alloy ingots directly: bronze, invar, cupronickel, electrum, battery alloy, brass and more.",
        "&eChemistry:&r Alloying in the melt is how bronze was really made: liquid copper and tin mix atom by atom, then freeze together.",
        "&eHow:&r Invar plates, a bronze rotor, fluid pipes and a steel machine casing (check JEI). Invar is iron and nickel; mix the dusts and smelt. Feed the smelter nuggets or tiny dusts.",
        "&eTip:&r 27 copper and 9 tin nuggets make 4 bronze ingots: the same 3:1 ratio as the dust, with no mixing step."]),
    Q("t1_opt_quarry", 0, 0, [item("modern_industrialization:steam_quarry"), item("modern_industrialization:bronze_drill", 4)], "The Steam Quarry",
      subtitle="Ore from below the bottom of the world", deps=["t1_item_pipes"], optional=True, tokens=2, xp=75, desc=[
        "&eWhat:&r A steam multiblock that wears out bronze drills to bring up ore from deeper than bedrock. Slow, but you never have to dig.",
        "&eHow:&r The controller takes steel large plates, steel gears, item pipes, an invar rotary blade and a steel machine casing (check JEI for the shape and its ore table). Drills come 4 at a time from a bronze drill head, iron gears and pipes.",
        "&eTip:&r It eats a lot of steel, so build it once your Steam Blast Furnace runs on its own. Quarry ore still obeys the 2x cap until acids."]),
])
