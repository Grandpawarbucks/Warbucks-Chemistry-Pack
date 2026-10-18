package com.grandpawarbucks.warbuckscore;

import java.util.List;

import net.minecraft.ChatFormatting;
import net.minecraft.Util;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/** Sneak + right-click: record the biome at your feet. Put it in a Terraformer to spread that biome. */
public class BiomeCapsuleItem extends Item {
    public BiomeCapsuleItem(Properties props) {
        super(props);
    }

    public static Component biomeName(ResourceLocation biome) {
        return Component.translatable(Util.makeDescriptionId("biome", biome));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!player.isShiftKeyDown()) {
            return InteractionResultHolder.pass(stack);
        }
        if (!level.isClientSide) {
            ResourceLocation biome = level.getBiome(player.blockPosition()).unwrapKey()
                    .map(k -> k.location()).orElse(null);
            if (biome == null) {
                return InteractionResultHolder.fail(stack);
            }
            // Record into one capsule; split it off a stack so the rest stay empty.
            ItemStack filled = stack.split(1);
            filled.set(WarbucksCore.STORED_BIOME.get(), biome);
            if (stack.isEmpty()) {
                player.setItemInHand(hand, filled);
            } else if (!player.getInventory().add(filled)) {
                player.drop(filled, false);
            }
            player.displayClientMessage(Component.translatable("message.warbuckscore.capsule.recorded",
                    biomeName(biome).copy().withStyle(ChatFormatting.GREEN)), true);
            level.playSound(null, player.blockPosition(), SoundEvents.BOTTLE_FILL, SoundSource.PLAYERS, 1.0f, 1.0f);
        }
        return InteractionResultHolder.sidedSuccess(player.getItemInHand(hand), level.isClientSide);
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return stack.has(WarbucksCore.STORED_BIOME.get());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext ctx, List<Component> tooltip, TooltipFlag flag) {
        ResourceLocation biome = stack.get(WarbucksCore.STORED_BIOME.get());
        if (biome != null) {
            tooltip.add(Component.translatable("tooltip.warbuckscore.capsule.biome",
                    biomeName(biome).copy().withStyle(ChatFormatting.GREEN)).withStyle(ChatFormatting.GRAY));
        } else {
            tooltip.add(Component.translatable("tooltip.warbuckscore.capsule.empty").withStyle(ChatFormatting.GRAY));
        }
    }
}
