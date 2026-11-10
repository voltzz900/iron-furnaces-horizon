#!/usr/bin/env python3
"""Generate the content mod (blocks, items, recipes, loot, models, textures) from the Iron Furnaces jar."""
import json, shutil, sys
from pathlib import Path

jar, out = Path(sys.argv[1]), Path(sys.argv[2])
TIERS = ["copper", "iron", "gold", "diamond", "emerald", "obsidian", "crystal", "netherite"]
NS = "ironfurnaces"
TAGS = {
    "#c:ingots/iron": "minecraft:iron_ingot", "#c:ingots/copper": "minecraft:copper_ingot",
    "#c:ingots/gold": "minecraft:gold_ingot", "#c:ingots/netherite": "minecraft:netherite_ingot",
    "#c:gems/diamond": "minecraft:diamond", "#c:gems/emerald": "minecraft:emerald",
    "#c:obsidians": "minecraft:obsidian", "#c:glass_blocks/colorless": "minecraft:glass",
    "#c:glass_blocks": "minecraft:glass", "#c:cobblestones": "minecraft:cobblestone",
    "#c:storage_blocks/gold": "minecraft:gold_block", "#c:rods/blaze": "minecraft:blaze_rod",
}
for tier in TIERS:
    TAGS[f"#c:furnaces/{tier}"] = f"{NS}:{tier}_furnace"

if out.exists():
    shutil.rmtree(out)

def write(rel, value):
    path = out / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")

(out).mkdir(parents=True)
(out / "horizon-mod.toml").write_text(
    'id = "ironfurnaces"\nname = "Iron Furnaces (Horizon port)"\nversion = "0.1.0"\n'
    'description = "Faster furnace tiers, ported from Iron Furnaces 4.4.2 (Apache-2.0)."\n'
    'authors = ["voltzz900 (Horizon port)", "Qelifern (pizzaatime)", "XenoMustache", "Astryxion"]\n'
    'api = "0.2"\nside = "both"\ncapabilities = ["registries"]\n'
)
lang = json.loads((jar / f"assets/{NS}/lang/en_us.json").read_text())
names, skipped, textures = {}, [], set()
for tier in TIERS:
    block = f"{tier}_furnace"
    write(f"data/{NS}/horizon/block/{block}.json", {"template": "minecraft:furnace", "item": True})
    write(f"data/{NS}/loot_table/blocks/{block}.json", {
        "type": "minecraft:block",
        "pools": [{"condition": {"type": "minecraft:survives_explosion"},
                   "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}], "rolls": 1}],
    })
    variants = {}
    for facing, y in (("north", 0), ("south", 180), ("west", 270), ("east", 90)):
        for lit, model in (("false", block), ("true", f"{block}_on")):
            variant = {"model": f"{NS}:block/{model}"}
            if y:
                variant["y"] = y
            variants[f"facing={facing},lit={lit}"] = variant
    write(f"assets/{NS}/blockstates/{block}.json", {"variants": variants})
    write(f"assets/{NS}/items/{block}.json",
          {"model": {"type": "minecraft:model", "model": f"{NS}:block/{block}"}})
    for model in (block, f"{block}_on"):
        src = json.loads((jar / f"assets/{NS}/models/block/{model}.json").read_text())
        write(f"assets/{NS}/models/block/{model}.json", src)
        textures.update(t.split("block/", 1)[1] for t in src["textures"].values() if t.startswith(f"{NS}:block/"))
    names[f"block.{NS}.{block}"] = lang[f"block.{NS}.{block}"]
    for recipe in sorted((jar / f"data/{NS}/recipe/furnaces").glob(f"{block}*.json")):
        data = json.loads(recipe.read_text())
        key = {k: TAGS.get(v, v) for k, v in data["key"].items()}
        if any(v.startswith("#c:") for v in key.values()):
            skipped.append(f"{recipe.name}: {sorted(v for v in key.values() if v.startswith('#c:'))}")
            continue
        data["key"] = key
        write(f"data/{NS}/recipe/{recipe.name}", data)
for name in sorted(textures):
    for suffix in (".png", ".png.mcmeta"):
        src = jar / f"assets/{NS}/textures/block/{name}{suffix}"
        if src.exists():
            dst = out / f"assets/{NS}/textures/block/{name}{suffix}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
write(f"assets/{NS}/lang/en_us.json", names)
blocks = [f"{NS}:{t}_furnace" for t in TIERS]
write("data/minecraft/tags/block/mineable/pickaxe.json", {"values": blocks})
print(f"{len(TIERS)} blocks, {len(textures)} textures, skipped recipes: {skipped}")
