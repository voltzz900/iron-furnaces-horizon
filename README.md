# Iron Furnaces for Horizon

A port of [Iron Furnaces](https://github.com/Qelifern/IronFurnacesNeoForge) 4.4.2 by Qelifern (pizzaatime),
XenoMustache and Astryxion to [Horizon](https://playhorizon.dev). Unofficial: not made or endorsed by the Iron Furnaces team.

Two parts, both needed:

- **`ironfurnaces`** (content mod, `content/`): the eight furnaces' blocks, items, crafting recipes, loot, models and
  textures. Generated from the original jar by `tools/build_content.py`.
- **`ironfurnaces_native`** (native mod, `native/`): the furnaces' block entities and cooking, as a horizon-mixins
  bundle pinned to Horizon Nightly 2026-11-08 (`fdc87ae`). The launcher builds it into the game.

## What is ported

Copper, iron, gold, diamond, emerald, obsidian, crystal and netherite furnaces, each with the original default speed
(a 200-tick recipe takes 180, 160, 120, 80, 40, 20, 40 and 5 ticks), the vanilla furnace menu, the lit front, and
hoppers on the sides and bottom.

Not ported yet: augments, upgrade kits, factory and generator modes, side configuration, the silver, rainbow and
Allthemodium tiers, the original screens, and the experience from smelting.

## Building

```sh
python3 tools/build_content.py <path to ironfurnaces-4.4.2.jar, unzipped> content
./release.sh   # packs dist/ironfurnaces-<version>.hmod and dist/ironfurnaces_native-<version>.hnmod
```

## Changes from the original

The Java code was not used: the cooking is reimplemented in Rust on Horizon's furnace (`native/`). Textures, models
and recipes are taken from the original jar; the recipes' `c:` tags are replaced with vanilla items, and the loot
tables are rewritten in Minecraft 26.3's format.

## License

Apache-2.0, as the original: see [LICENSE](LICENSE) and [NOTICE-iron-furnaces.txt](NOTICE-iron-furnaces.txt).
