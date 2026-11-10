fn block_entity_container(block: &str, container: &mut Option<horizon_client::containers::ModContainer>) {
    if block.starts_with("ironfurnaces:") {
        // AbstractFurnaceBlockEntity's faces: result and fuel below, input above, fuel on the sides.
        *container = Some(horizon_client::containers::ModContainer {
            slots: 3,
            faces: [vec![2, 1], vec![0], vec![1], vec![1], vec![1], vec![1]],
            inputs: vec![0, 1],
            outputs: vec![2, 1],
            menu: Some("minecraft:furnace".to_string()),
        });
    }
}
