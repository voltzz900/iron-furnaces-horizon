fn block_entity_tick(
    game: &mut crate::game::Game<'_>,
    pos: [i32; 3],
    entity: &mut horizon_client::containers::ModBlockEntity,
) {
    use horizon_client::furnace::FurnaceCooking;
    use horizon_world::nbt::Tag;

    // Config's default ticks for a 200 tick recipe.
    let ticks = match entity.id.as_str() {
        "ironfurnaces:copper_furnace" => 180,
        "ironfurnaces:iron_furnace" => 160,
        "ironfurnaces:gold_furnace" => 120,
        "ironfurnaces:diamond_furnace" => 80,
        "ironfurnaces:emerald_furnace" | "ironfurnaces:crystal_furnace" => 40,
        "ironfurnaces:obsidian_furnace" => 20,
        "ironfurnaces:netherite_furnace" => 5,
        _ => return,
    };
    fn int(entity: &horizon_client::containers::ModBlockEntity, key: &str) -> i32 {
        match entity.nbt.get(&horizon_world::nbt::JavaString::from(key)) {
            Some(Tag::Int(value)) => *value,
            _ => 0,
        }
    }
    let [input, fuel, result] = [0, 1, 2].map(|slot| entity.items.get(slot).cloned().flatten());
    let mut furnace = horizon_client::containers::Furnace {
        kind: horizon_client::containers::FurnaceKind::Furnace,
        items: [input, fuel, result],
        lit_remaining: int(entity, "lit_time_remaining"),
        lit_total: int(entity, "lit_total_time"),
        cooking_timer: int(entity, "cooking_time_spent"),
        cooking_total: int(entity, "cooking_total_time"),
        speed: 1.0,
        recipes_used: Default::default(),
    };
    let before = furnace.clone();
    // BlockIronFurnaceTileBase.getSpeed: the tier's time, scaled by the recipe's against 200 ticks.
    let total = |furnace: &horizon_client::containers::Furnace, recipes: &horizon_client::crafting::Recipes| {
        furnace.items[0]
            .as_ref()
            .and_then(|input| recipes.cook(furnace.kind.recipe_type(), input))
            .map(|recipe| ((ticks as f64 * recipe.time as f64 / 200.0) as i32).max(1))
    };
    let mut drops = Vec::new();
    let lit = furnace.tick(
        world_recipes!(game),
        world_items!(game),
        game.res.providers(),
        &mut drops,
    );
    if let Some(total) = total(&furnace, world_recipes!(game)) {
        furnace.cooking_total = total;
    }
    let data = vec![
        furnace.lit_remaining,
        furnace.lit_total,
        furnace.cooking_timer,
        furnace.cooking_total,
    ];
    if entity.data != data {
        entity.data = data;
    }
    if furnace.items != before.items {
        entity.items = furnace.items.to_vec();
    }
    for (key, value) in [
        ("lit_time_remaining", furnace.lit_remaining),
        ("lit_total_time", furnace.lit_total),
        ("cooking_time_spent", furnace.cooking_timer),
        ("cooking_total_time", furnace.cooking_total),
    ] {
        if int(entity, key) != value {
            entity.nbt.insert(key.into(), Tag::Int(value));
        }
    }
    if let Some(lit) = lit {
        game.native_set_block_property(pos, "lit", if lit { "true" } else { "false" });
    }
}
