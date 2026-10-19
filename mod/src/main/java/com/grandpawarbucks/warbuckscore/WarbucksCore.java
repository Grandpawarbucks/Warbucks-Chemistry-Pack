package com.grandpawarbucks.warbuckscore;

import com.mojang.logging.LogUtils;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.TagsUpdatedEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;
import org.slf4j.Logger;

/**
 * Warbucks Core: custom content for the Warbucks Chemistry pack.
 * <ul>
 *   <li>Spectrometer: reads the ore "signal" in nearby loaded chunks (by c:ores/* block tags).</li>
 *   <li>Biome Capsule: records the biome you stand in.</li>
 *   <li>Terraformer: rewrites the biome around it to the capsule's biome, fuelled by items in
 *       the #warbuckscore:terraformer_fuel tag (the pack puts Charged Energy Cores there).</li>
 *   <li>Periodic Table perks ({@link ElementPerks}): a permanent bonus for each completed element group.</li>
 * </ul>
 * Recipes are added by the pack's KubeJS scripts so they can use MI/ChemLib items without
 * this mod depending on them.
 */
@Mod(WarbucksCore.MODID)
public class WarbucksCore {
    public static final String MODID = "warbuckscore";
    public static final Logger LOGGER = LogUtils.getLogger();

    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MODID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, MODID);
    public static final DeferredRegister.DataComponents COMPONENTS =
            DeferredRegister.createDataComponents(Registries.DATA_COMPONENT_TYPE, MODID);
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    /** Biome stored in a Biome Capsule. */
    public static final DeferredHolder<DataComponentType<?>, DataComponentType<ResourceLocation>> STORED_BIOME =
            COMPONENTS.registerComponentType("biome", b -> b.persistent(ResourceLocation.CODEC).networkSynchronized(
                    ResourceLocation.STREAM_CODEC));

    public static final DeferredBlock<TerraformerBlock> TERRAFORMER = BLOCKS.register("terraformer",
            () -> new TerraformerBlock(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_GREEN)
                    .strength(5.0f, 6.0f).requiresCorrectToolForDrops().sound(SoundType.METAL).lightLevel(s -> 7)));
    public static final DeferredItem<BlockItem> TERRAFORMER_ITEM = ITEMS.register("terraformer",
            () -> new BlockItem(TERRAFORMER.get(), new Item.Properties().rarity(Rarity.EPIC)));
    public static final DeferredItem<SpectrometerItem> SPECTROMETER = ITEMS.register("spectrometer",
            () -> new SpectrometerItem(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON)));
    public static final DeferredItem<BiomeCapsuleItem> BIOME_CAPSULE = ITEMS.register("biome_capsule",
            () -> new BiomeCapsuleItem(new Item.Properties().stacksTo(16)));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<TerraformerBlockEntity>> TERRAFORMER_BE =
            BLOCK_ENTITIES.register("terraformer",
                    () -> BlockEntityType.Builder.of(TerraformerBlockEntity::new, TERRAFORMER.get()).build(null));

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.warbuckscore"))
                    .icon(() -> new ItemStack(SPECTROMETER.get()))
                    .displayItems((params, out) -> {
                        out.accept(SPECTROMETER.get());
                        out.accept(BIOME_CAPSULE.get());
                        out.accept(TERRAFORMER_ITEM.get());
                    }).build());

    public WarbucksCore(IEventBus modBus, ModContainer container) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        BLOCK_ENTITIES.register(modBus);
        COMPONENTS.register(modBus);
        TABS.register(modBus);
        ElementPerks.register(modBus);
        container.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
        // Ore tags can change on /reload: forget the cached block -> element lookups.
        NeoForge.EVENT_BUS.addListener((TagsUpdatedEvent e) -> SpectrometerItem.clearCache());
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
