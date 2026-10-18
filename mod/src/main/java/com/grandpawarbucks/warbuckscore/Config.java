package com.grandpawarbucks.warbuckscore;

import net.neoforged.neoforge.common.ModConfigSpec;

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

    public static final ModConfigSpec SPEC = B.build();

    private Config() {}
}
