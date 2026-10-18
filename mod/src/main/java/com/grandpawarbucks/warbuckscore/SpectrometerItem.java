package com.grandpawarbucks.warbuckscore;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import net.minecraft.world.level.chunk.LevelChunkSection;

/**
 * Right-click: reads the ore "signal" in the loaded chunks around the player and reports, per
 * element, how much ore there is, which direction the signal is strongest in, and at what depth.
 * Elements come from c:ores/&lt;element&gt; block tags, so every mod's ores are recognised.
 * Uses each chunk section's block palette, so a scan is cheap even for 81 chunks.
 */
public class SpectrometerItem extends Item {
    private static final Map<Block, Optional<String>> ELEMENT = new IdentityHashMap<>();

    public SpectrometerItem(Properties props) {
        super(props);
    }

    static void clearCache() {
        synchronized (ELEMENT) {
            ELEMENT.clear();
        }
    }

    /** "iron" for a block tagged c:ores/iron; empty for non-ores. */
    private static Optional<String> element(BlockState state) {
        synchronized (ELEMENT) {
            return ELEMENT.computeIfAbsent(state.getBlock(), b -> state.getTags()
                    .map(TagKey::location)
                    .filter(t -> t.getNamespace().equals("c") && t.getPath().startsWith("ores/"))
                    .map(t -> t.getPath().substring(5))
                    .findFirst());
        }
    }

    private static final class Signal {
        long count;
        double sx, sz, sy; // count-weighted sums of block x, z and section-centre y
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(level instanceof ServerLevel server)) {
            return InteractionResultHolder.success(stack);
        }
        int r = Config.SPECTROMETER_RADIUS.get();
        int pcx = player.chunkPosition().x, pcz = player.chunkPosition().z;
        Map<String, Signal> signals = new HashMap<>();
        int scanned = 0;
        for (int cx = pcx - r; cx <= pcx + r; cx++) {
            for (int cz = pcz - r; cz <= pcz + r; cz++) {
                LevelChunk chunk = server.getChunkSource().getChunkNow(cx, cz);
                if (chunk == null) continue;
                scanned++;
                double bx = (cx << 4) + 8, bz = (cz << 4) + 8;
                LevelChunkSection[] sections = chunk.getSections();
                for (int i = 0; i < sections.length; i++) {
                    LevelChunkSection section = sections[i];
                    if (section.hasOnlyAir() || !section.getStates().maybeHas(s -> element(s).isPresent())) continue;
                    double by = (chunk.getSectionYFromSectionIndex(i) << 4) + 8;
                    section.getStates().count((state, n) -> element(state).ifPresent(el -> {
                        Signal s = signals.computeIfAbsent(el, k -> new Signal());
                        s.count += n;
                        s.sx += bx * n;
                        s.sz += bz * n;
                        s.sy += by * n;
                    }));
                }
            }
        }

        player.displayClientMessage(Component.translatable("message.warbuckscore.spectrometer.header",
                scanned, r * 2 + 1).withStyle(ChatFormatting.AQUA), false);
        List<Map.Entry<String, Signal>> top = new ArrayList<>(signals.entrySet());
        top.sort((a, b) -> Long.compare(b.getValue().count, a.getValue().count));
        if (top.isEmpty()) {
            player.displayClientMessage(Component.translatable("message.warbuckscore.spectrometer.none")
                    .withStyle(ChatFormatting.GRAY), false);
        }
        for (Map.Entry<String, Signal> e : top.subList(0, Math.min(8, top.size()))) {
            Signal s = e.getValue();
            double dx = s.sx / s.count - player.getX(), dz = s.sz / s.count - player.getZ();
            int dist = (int) Math.round(Math.sqrt(dx * dx + dz * dz));
            String dir = dist < 12 ? "here" : compass(dx, dz);
            String strength = s.count >= 400 ? "strong" : s.count >= 80 ? "moderate" : "faint";
            player.displayClientMessage(Component.translatable("message.warbuckscore.spectrometer.line",
                    Component.literal(pretty(e.getKey())).withStyle(ChatFormatting.GOLD),
                    Component.translatable("message.warbuckscore.spectrometer." + strength),
                    s.count,
                    Component.translatable("message.warbuckscore.spectrometer.dir." + dir),
                    dist,
                    (int) Math.round(s.sy / s.count)), false);
        }
        level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0f, 1.4f);
        player.getCooldowns().addCooldown(this, Config.SPECTROMETER_COOLDOWN.get());
        return InteractionResultHolder.consume(stack);
    }

    /** Minecraft: +x = east, +z = south. */
    private static String compass(double dx, double dz) {
        double deg = (Math.toDegrees(Math.atan2(dx, -dz)) + 360) % 360; // 0 = north, clockwise
        String[] names = {"n", "ne", "e", "se", "s", "sw", "w", "nw"};
        return names[(int) Math.round(deg / 45) % 8];
    }

    private static String pretty(String element) {
        String[] parts = element.replace('/', ' ').replace('_', ' ').split(" ");
        StringBuilder sb = new StringBuilder();
        for (String p : parts) {
            if (p.isEmpty()) continue;
            if (sb.length() > 0) sb.append(' ');
            sb.append(Character.toUpperCase(p.charAt(0))).append(p.substring(1));
        }
        return sb.toString();
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext ctx, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.warbuckscore.spectrometer").withStyle(ChatFormatting.GRAY));
    }
}
