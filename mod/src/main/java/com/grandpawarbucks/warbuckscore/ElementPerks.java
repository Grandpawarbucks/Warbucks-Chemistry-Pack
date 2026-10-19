package com.grandpawarbucks.warbuckscore;

import com.mojang.serialization.Codec;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.Commands;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.config.ModConfigEvent;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.Set;
import java.util.function.Supplier;

/**
 * Periodic Table perks. The mod remembers every element item a player has held (in their
 * inventory at least once). Collecting a whole group from {@code perks.groups} in the config grants
 * that group's permanent attribute bonus. {@code /warbucks elements} shows progress.
 */
public final class ElementPerks {
    public static final DeferredRegister<AttachmentType<?>> ATTACHMENTS =
            DeferredRegister.create(NeoForgeRegistries.ATTACHMENT_TYPES, WarbucksCore.MODID);

    /** Element item ids this player has held. Kept through death. */
    public static final Supplier<AttachmentType<Set<String>>> SEEN = ATTACHMENTS.register("elements_seen",
            () -> AttachmentType.<Set<String>>builder(() -> new HashSet<>())
                    .serialize(Codec.STRING.listOf().<Set<String>>xmap(HashSet::new, List::copyOf))
                    .copyOnDeath()
                    .build());

    /** One perk group, parsed from "id;Name;element,element,...;attribute;amount;operation;description". */
    record Group(String id, String name, List<String> elements, Holder<Attribute> attribute, double amount,
                 AttributeModifier.Operation operation, String description) {
        ResourceLocation modifierId() {
            return WarbucksCore.id("perk/" + id);
        }
    }

    private static List<Group> groups;
    private static Set<String> tracked;

    private ElementPerks() {}

    public static void register(IEventBus modBus) {
        ATTACHMENTS.register(modBus);
        modBus.addListener((ModConfigEvent.Loading e) -> groups = null);
        modBus.addListener((ModConfigEvent.Reloading e) -> groups = null);
        NeoForge.EVENT_BUS.addListener(ElementPerks::onPlayerTick);
        NeoForge.EVENT_BUS.addListener((PlayerEvent.PlayerLoggedInEvent e) -> apply(e.getEntity()));
        NeoForge.EVENT_BUS.addListener((PlayerEvent.PlayerRespawnEvent e) -> apply(e.getEntity()));
        NeoForge.EVENT_BUS.addListener((PlayerEvent.PlayerChangedDimensionEvent e) -> apply(e.getEntity()));
        NeoForge.EVENT_BUS.addListener(ElementPerks::onRegisterCommands);
    }

    static List<Group> groups() {
        if (groups == null) {
            List<Group> parsed = new ArrayList<>();
            for (String line : Config.PERK_GROUPS.get()) {
                parse(line).ifPresent(parsed::add);
            }
            Set<String> all = new HashSet<>();
            parsed.forEach(g -> all.addAll(g.elements()));
            tracked = all;
            groups = parsed;
        }
        return groups;
    }

    private static Optional<Group> parse(String line) {
        String[] f = line.split(";");
        if (f.length != 7) {
            WarbucksCore.LOGGER.warn("perks.groups: expected 7 fields separated by ';', got {}: {}", f.length, line);
            return Optional.empty();
        }
        try {
            List<String> elements = List.of(f[2].trim().split("\\s*,\\s*"));
            Optional<Holder.Reference<Attribute>> attribute =
                    BuiltInRegistries.ATTRIBUTE.getHolder(ResourceLocation.parse(f[3].trim()));
            if (attribute.isEmpty()) {
                WarbucksCore.LOGGER.warn("perks.groups: unknown attribute {} in: {}", f[3], line);
                return Optional.empty();
            }
            AttributeModifier.Operation op = AttributeModifier.Operation.valueOf(f[5].trim().toUpperCase(Locale.ROOT));
            return Optional.of(new Group(f[0].trim(), f[1].trim(), elements, attribute.get(),
                    Double.parseDouble(f[4].trim()), op, f[6].trim()));
        } catch (RuntimeException e) {
            WarbucksCore.LOGGER.warn("perks.groups: can't read '{}': {}", line, e.getMessage());
            return Optional.empty();
        }
    }

    private static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player)
                || player.tickCount % Config.PERK_SCAN_TICKS.get() != 0) {
            return;
        }
        List<Group> all = groups();
        Set<String> seen = player.getData(SEEN);
        List<String> found = new ArrayList<>();
        Inventory inv = player.getInventory();
        for (List<ItemStack> part : List.of(inv.items, inv.armor, inv.offhand)) {
            for (ItemStack stack : part) {
                if (stack.isEmpty()) continue;
                String id = BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
                if (tracked.contains(id) && seen.add(id)) found.add(id);
            }
        }
        if (found.isEmpty()) return;
        player.setData(SEEN, seen);

        for (Group g : all) {
            List<String> newHere = g.elements().stream().filter(found::contains).toList();
            if (newHere.isEmpty()) continue;
            long have = g.elements().stream().filter(seen::contains).count();
            if (have == g.elements().size()) {
                player.sendSystemMessage(Component.translatable("message.warbuckscore.perk.complete",
                        g.name(), g.description()).withStyle(ChatFormatting.GOLD));
                player.level().playSound(null, player.blockPosition(), SoundEvents.UI_TOAST_CHALLENGE_COMPLETE,
                        SoundSource.PLAYERS, 0.8f, 1.0f);
            } else {
                for (String id : newHere) {
                    player.displayClientMessage(Component.translatable("message.warbuckscore.perk.element",
                            itemName(id), g.name(), have, g.elements().size()), true);
                }
            }
        }
        apply(player);
    }

    /** Add the modifier of every completed group, remove the others (e.g. after a config change). */
    static void apply(net.minecraft.world.entity.player.Player p) {
        if (!(p instanceof ServerPlayer player)) return;
        Set<String> seen = player.getData(SEEN);
        for (Group g : groups()) {
            AttributeInstance inst = player.getAttribute(g.attribute());
            if (inst == null) continue;
            if (seen.containsAll(g.elements())) {
                inst.addOrUpdateTransientModifier(new AttributeModifier(g.modifierId(), g.amount(), g.operation()));
            } else {
                inst.removeModifier(g.modifierId());
            }
        }
    }

    private static Component itemName(String id) {
        return BuiltInRegistries.ITEM.get(ResourceLocation.parse(id)).getDescription();
    }

    private static void onRegisterCommands(RegisterCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("warbucks").then(Commands.literal("elements").executes(ctx -> {
            ServerPlayer player = ctx.getSource().getPlayerOrException();
            Set<String> seen = player.getData(SEEN);
            ctx.getSource().sendSuccess(() -> Component.translatable("message.warbuckscore.perks.header")
                    .withStyle(ChatFormatting.GOLD), false);
            for (Group g : groups()) {
                List<String> missing = g.elements().stream().filter(e -> !seen.contains(e)).toList();
                MutableComponent status;
                if (missing.isEmpty()) {
                    status = Component.translatable("message.warbuckscore.perks.done", g.description())
                            .withStyle(ChatFormatting.GREEN);
                } else {
                    MutableComponent names = Component.empty();
                    for (int i = 0; i < missing.size(); i++) {
                        if (i > 0) names.append(", ");
                        names.append(itemName(missing.get(i)));
                    }
                    status = Component.translatable("message.warbuckscore.perks.missing", names)
                            .withStyle(ChatFormatting.GRAY);
                }
                int have = g.elements().size() - missing.size();
                ctx.getSource().sendSuccess(() -> Component.translatable("message.warbuckscore.perks.line",
                        g.name(), have, g.elements().size(), status), false);
            }
            return 1;
        })));
    }
}
