package com.grandpawarbucks.warbuckscore;

import net.neoforged.neoforge.common.ModConfigSpec;

import java.util.List;

/** config/warbuckscore-common.toml */
public final class Config {
    private static final ModConfigSpec.Builder B = new ModConfigSpec.Builder();

    public static final ModConfigSpec.IntValue SPECTROMETER_RADIUS = B
            .comment("Spectrometer scan radius in chunks (4 = a 9x9 chunk area). Only loaded chunks are read.")
            .defineInRange("spectrometer.radiusChunks", 4, 1, 8);
    public static final ModConfigSpec.IntValue SPECTROMETER_COOLDOWN = B
            .comment("Ticks between Spectrometer scans (20 ticks = 1 second).")
            .defineInRange("spectrometer.cooldownTicks", 100, 0, 1200);

    public static final ModConfigSpec.IntValue TERRAFORMER_RADIUS = B
            .comment("Terraformer radius in chunks around its own chunk (4 = a 9x9 chunk area, 144x144 blocks).")
            .defineInRange("terraformer.radiusChunks", 4, 0, 8);
    public static final ModConfigSpec.IntValue TERRAFORMER_TICKS_PER_CHUNK = B
            .comment("Ticks between converting two chunks.")
            .defineInRange("terraformer.ticksPerChunk", 40, 1, 1200);
    public static final ModConfigSpec.IntValue TERRAFORMER_CHUNKS_PER_FUEL = B
            .comment("Chunks converted per fuel item (#warbuckscore:terraformer_fuel).")
            .defineInRange("terraformer.chunksPerFuel", 9, 1, 81);

    public static final ModConfigSpec.ConfigValue<List<? extends String>> PERK_GROUPS = B
            .comment("Periodic Table perks: hold every element of a group (at least once) for a permanent bonus.",
                    "One entry per group: id;Name;element,element,...;attribute;amount;operation;description",
                    "operation is add_value, add_multiplied_base or add_multiplied_total. Changing the list",
                    "updates players' bonuses on their next login. Elements are item ids (ChemLib: chemlib:<name>).")
            .defineListAllowEmpty("perks.groups", List.of(
                    "post_transition;Post-Transition Metals;chemlib:aluminum,chemlib:tin,chemlib:lead,chemlib:indium;"
                            + "minecraft:generic.armor_toughness;2;add_value;+2 armor toughness"),
                    () -> "", o -> o instanceof String);
    public static final ModConfigSpec.IntValue PERK_SCAN_TICKS = B
            .comment("Ticks between inventory checks for new elements.")
            .defineInRange("perks.scanTicks", 40, 1, 1200);

    public static final ModConfigSpec SPEC = B.build();

    private Config() {}
}
