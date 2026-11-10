fn block_entity_ticks(block: &str, ticks: &mut bool) {
    if block.starts_with("ironfurnaces:") {
        *ticks = true;
    }
}
