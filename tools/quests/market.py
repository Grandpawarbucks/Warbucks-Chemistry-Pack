"""Quest chapter: market (the Demigod Token shop). See tools/quests/STYLE.md.
The shop itself is in pack/kubejs/server_scripts/phase4_chemistry.js, section 5 (shapeless recipes).
"""
from questlib import Q, Chapter, item, tick, SIDE  # noqa: F401

T = "kubejs:demigod_token"
G = "kubejs:greater_demigod_token"

CHAPTER = Chapter("market", "The Demigod's Market", T,
        ["Spend your Demigod Tokens: supplies and comforts, never shortcuts."], SIDE, [
    Q("mk_intro", 0, 0, [tick()], "The Market", deps=["wel_tokens"], xp=20, tokens=1,
      subtitle="What Demigod Tokens are for", desc=[
        "&6You remember offerings left at your altar. Now the world pays you in coins instead.&r",
        "&eWhat:&r Demigod Tokens are the reward currency of this book. You trade them for supplies by crafting, with no shopkeeper and no server plugin.",
        "&eHow:&r every shop trade is a shapeless crafting recipe: put tokens in a crafting grid and the item appears.",
        "&eHow:&r the price list is JEI: search &eDemigod Token&r and press &eU&r (uses). Every trade shows as a crafting recipe. Do the same for the Greater Demigod Token.",
        "&eTip:&r tokens buy raw supplies and comforts, never machines, circuits, alloys or anything that skips a tier. Bookmark the trades you use most.",
        "{@pagebreak}",
        "&eWhat tokens never buy:&r the shop skips boring gathering (sand, gravel, string, torches), never learning. If a trade seems missing, it was left out on purpose.",
        "&eChemistry:&r a bag of raw ore is not a refinery. Raw tin still needs your crusher, raw titanium still needs your blast furnace."]),
    Q("mk_earn", 2, 0, [item(T)], "Where Tokens Come From", deps=["mk_intro"], xp=20, tokens=1,
      subtitle="Every quest pays", desc=[
        "&eWhat:&r almost every quest pays tokens, scaled by tier: 1 per quest at the start, 2 in the steam and Nether chapters, 3 at LV and MV, 4 at HV, 5 at EV, 8 in space.",
        "&eHow:&r milestone quests (the big ones) pay double and also roll that tier's reward table. Optional side quests pay 1 or 2.",
        "&eTip:&r on a team, rewards go to each player who claims them, so everyone builds their own purse."]),
    Q("mk_small", 0, 2, [tick()], "The Price Bands", deps=["mk_earn"], xp=60, tokens=1,
      subtitle="Small, medium and large trades", desc=[
        "&eWhat:&r the shop has three price bands. Small (1 to 3 tokens): cheap stacks of things you'd otherwise spend an afternoon gathering. Medium and large are on the next pages.",
        "&eHow:&r 1 token: 32 torches, 16 bread, 8 bottles o' enchanting, 32 bone meal, 64 sand, 64 gravel or 32 clay balls.",
        "&eHow:&r 2 tokens: 16 iron ingots, 16 coke, 16 rubber sheets, 16 fire clay dust, 32 salt dust, 16 string, 16 leather or a sleeping bag.",
        "&eHow:&r 3 tokens: 8 osmium ingots, 2 backpack upgrade bases, 16 gunpowder, 16 slime balls, 32 redstone or 16 lapis.",
        "&eTip:&r sand and gravel are the best early value: concrete, glass and silicon all start there.",
        "{@pagebreak}",
        "&eMedium band (4 to 8 tokens):&r raw ores (you still process them yourself) and drops you would otherwise farm.",
        "&eHow:&r 4 tokens: a Warp Stone, 32 raw copper, 16 raw tin, 16 raw lead, 16 bauxite dust, 32 quartz or 32 glowstone dust.",
        "&eHow:&r 5: 16 raw nickel, 8 ender pearls, 4 phantom membranes, 16 amethyst. 6: 8 blaze rods, 4 ghast tears, 16 certus quartz, 8 source gems.",
        "&eHow:&r 7: 8 raw titanium or 2 name tags. 8: 8 raw tungsten or 32 prismarine shards.",
        "&eTip:&r raw ore bought here is worth up to 5x once your Mekanism line is running. Buy late, process well.",
        "{@pagebreak}",
        "&eLarge band (Greater Tokens):&r the big trades cost Greater Demigod Tokens, not regular ones.",
        "&eHow:&r 1 Greater: 4 golden apples, 4 diamonds, 16 emeralds or a saddle. 2: 2 shulker shells, a heart of the sea or a netherite scrap.",
        "&eHow:&r 3 Greater: a totem of undying or 4 echo shards. 4 Greater: an enchanted golden apple.",
        "&eTip:&r shulker shells mean shulker boxes. Many players find that the best trade in the shop."]),
    Q("mk_exchange", 6, 2, [item(G)], "The Exchange", deps=["mk_small"], xp=50, tokens=1,
      subtitle="Nine tokens make one Greater Token", desc=[
        "&eWhat:&r a Greater Demigod Token is worth 9 Demigod Tokens, and the trade works both ways.",
        "&eHow:&r 9 tokens in a crafting grid make 1 Greater Token. 1 Greater Token alone in the grid gives the 9 back.",
        "&eTip:&r late-tier milestones and boss loot sometimes pay Greater Tokens directly."]),

    # --- Market days (y=4): hold tokens, pick a reward -----------------------------------------
    Q("mk_day_early", 0, 4, [item(T, 10)], "Market Day: Early", deps=["mk_small", "gs_iron"], xp=50, tokens=1,
      choice="pick_early", subtitle="Hold 10 tokens; pick a comfort", desc=[
        "&eWhat:&r a reward for saving. Hold 10 Demigod Tokens at once and choose one comfort: a sleeping bag, a Warp Stone, backpack upgrade bases or a saddle.",
        "&eHow:&r the tokens are only checked, not taken. Spend them afterwards if you like.",
        "&eTip:&r the Warp Stone is the pick if you explore a lot."]),
    Q("mk_day_mid", 2, 4, [item(T, 30)], "Market Day: Industrial", deps=["mk_day_early", "t3_analog"], xp=100, tokens=1,
      choice="pick_mid", subtitle="Hold 30 tokens; pick a feedstock", desc=[
        "&eWhat:&r hold 30 tokens and choose a stack of raw feedstock: tin, lead, nickel, bauxite or salt.",
        "&eHow:&r tokens are checked, not taken.",
        "&eTip:&r bauxite is the slow one to find, and aluminium is the gate to MV."]),
    Q("mk_day_late", 4, 4, [item(T, 64)], "Market Day: Divine", deps=["mk_day_mid", "t6_pu"], xp=200, tokens=2, size=2.0, shape="gear",
      choice="pick_late", subtitle="Hold 64 tokens; pick a treasure", desc=[
        "&6You remember when worshippers brought you treasures. Now you just keep a full stack.&r",
        "&eWhat:&r hold a full stack of 64 tokens and choose a treasure: a totem, shulker shells, a heart of the sea, an enchanted golden apple or 3 Greater Tokens.",
        "&eHow:&r tokens are checked, not taken. Exchange Greater Tokens back if you need 64 loose ones.",
        "&eTip:&r picking the Greater Tokens is the same as taking 27 regular tokens home."]),

    # --- Secret -----------------------------------------------------------------------------------
    Q("mk_sec_hoard", 6, 4, [item(G, 9)], "A Dragon's Hoard", deps=["mk_exchange"], secret=True, optional=True, tokens=1,
      loot="secret", subtitle="81 tokens' worth, unspent", desc=[
        "&eWhat:&r hold nine Greater Demigod Tokens at once. That's 81 tokens you chose not to spend.",
        "&eTip:&r the demigod approves of patience. The demigod also notes that totems exist."]),
], links=[("wel_tokens", -2, 0)])
