package com.grandpawarbucks.warbuckscore;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;

/**
 * Converts the chunks around it to the target biome, nearest first (rings outwards from its own
 * chunk), one chunk every ticksPerChunk ticks while it has charge. Works like vanilla /fillbiome on
 * whole chunk columns: biome colours, weather and mob spawning change; existing blocks stay.
 */
public class TerraformerBlockEntity extends BlockEntity {
    public static final TagKey<Item> FUEL = TagKey.create(Registries.ITEM, WarbucksCore.id("terraformer_fuel"));

    private ResourceLocation target;
    private int charge;   // chunks it may still convert
    private int progress; // index into offsets() for the current target
    private int timer;

    public TerraformerBlockEntity(BlockPos pos, BlockState state) {
        super(WarbucksCore.TERRAFORMER_BE.get(), pos, state);
    }

    /** Chunk offsets within the configured radius, nearest first. */
    private static List<int[]> offsets() {
        int r = Config.TERRAFORMER_RADIUS.get();
        List<int[]> list = new ArrayList<>();
        for (int dx = -r; dx <= r; dx++) {
            for (int dz = -r; dz <= r; dz++) {
                list.add(new int[]{dx, dz});
            }
        }
        list.sort(Comparator.comparingInt((int[] o) -> Math.max(Math.abs(o[0]), Math.abs(o[1])))
                .thenComparingInt(o -> o[0] * o[0] + o[1] * o[1]));
        return list;
    }

    void insert(ItemStack stack, Player player) {
        if (stack.is(WarbucksCore.BIOME_CAPSULE.get())) {
            ResourceLocation biome = stack.get(WarbucksCore.STORED_BIOME.get());
            if (biome == null) {
                player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.empty_capsule")
                        .withStyle(ChatFormatting.RED), true);
                return;
            }
            if (!biome.equals(target)) {
                target = biome;
                progress = 0;
            }
            if (!player.getAbilities().instabuild) stack.shrink(1);
            player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.target",
                    BiomeCapsuleItem.biomeName(biome).copy().withStyle(ChatFormatting.GREEN)), true);
        } else if (stack.is(FUEL)) {
            int n = player.isShiftKeyDown() ? stack.getCount() : 1;
            charge += n * Config.TERRAFORMER_CHUNKS_PER_FUEL.get();
            if (!player.getAbilities().instabuild) stack.shrink(n);
            player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.charged", charge)
                    .withStyle(ChatFormatting.AQUA), true);
        }
        level.playSound(null, worldPosition, SoundEvents.BEACON_POWER_SELECT, SoundSource.BLOCKS, 0.8f, 1.2f);
        setChanged();
    }

    void showStatus(Player player) {
        int total = offsets().size();
        Component biome = target == null
                ? Component.translatable("message.warbuckscore.terraformer.no_target")
                : BiomeCapsuleItem.biomeName(target).copy().withStyle(ChatFormatting.GREEN);
        player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.status",
                biome, Math.min(progress, total), total, charge), false);
        if (target != null && progress >= total) {
            player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.done")
                    .withStyle(ChatFormatting.GOLD), false);
        } else if (target != null && charge <= 0) {
            player.displayClientMessage(Component.translatable("message.warbuckscore.terraformer.needs_fuel")
                    .withStyle(ChatFormatting.YELLOW), false);
        }
    }

    public static void serverTick(Level level, BlockPos pos, BlockState state, TerraformerBlockEntity be) {
        if (be.target == null || be.charge <= 0 || !(level instanceof ServerLevel server)) return;
        if (++be.timer < Config.TERRAFORMER_TICKS_PER_CHUNK.get()) return;
        be.timer = 0;
        List<int[]> offsets = offsets();
        if (be.progress >= offsets.size()) return;
        Optional<Holder.Reference<Biome>> biome = server.registryAccess().registryOrThrow(Registries.BIOME)
                .getHolder(ResourceKey.create(Registries.BIOME, be.target));
        if (biome.isEmpty()) return; // biome no longer exists (mod removed): wait for a new capsule
        int[] o = offsets.get(be.progress);
        LevelChunk chunk = server.getChunk((pos.getX() >> 4) + o[0], (pos.getZ() >> 4) + o[1]);
        Holder<Biome> holder = biome.get();
        chunk.fillBiomesFromNoise((x, y, z, sampler) -> holder, server.getChunkSource().randomState().sampler());
        chunk.setUnsaved(true);
        server.getChunkSource().chunkMap.resendBiomesForChunks(List.of(chunk));
        be.progress++;
        be.charge--;
        be.setChanged();
        server.sendParticles(ParticleTypes.HAPPY_VILLAGER, pos.getX() + 0.5, pos.getY() + 1.2, pos.getZ() + 0.5,
                12, 0.4, 0.3, 0.4, 0.0);
        server.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.BLOCKS, 0.6f, 0.8f);
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        if (target != null) tag.putString("Target", target.toString());
        tag.putInt("Charge", charge);
        tag.putInt("Progress", progress);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        target = tag.contains("Target") ? ResourceLocation.tryParse(tag.getString("Target")) : null;
        charge = tag.getInt("Charge");
        progress = tag.getInt("Progress");
    }
}
