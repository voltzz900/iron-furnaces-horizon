fn block_entity(block: &str, entity: &mut Option<(String, horizon_world::nbt::Compound)>) {
    if entity.is_none() && block.starts_with("ironfurnaces:") {
        *entity = Some((block.to_string(), Default::default()));
    }
}
