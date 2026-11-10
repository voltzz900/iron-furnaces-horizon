#!/bin/sh
# Packs the content mod (.hmod) and the native mod (.hnmod) the Horizon registry takes, into dist/.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/dist"
version="$(sed -n 's/^version = "\(.*\)"/\1/p' "$here/content/horizon-mod.toml")"
content="$here/dist/ironfurnaces-$version.hmod"
rm -f "$content"
cp "$here/LICENSE" "$here/NOTICE-iron-furnaces.txt" "$here/content/"
(cd "$here/content" && zip -q -X -r -9 "$content" .)
rm "$here/content/LICENSE" "$here/content/NOTICE-iron-furnaces.txt"
python3 -I - "$here" <<'EOF'
import json, sys, zipfile, pathlib, tomllib
root = pathlib.Path(sys.argv[1])
mixin = tomllib.loads((root / "native/horizon-mixin.toml").read_text())
version = mixin["mod"]["version"]
meta = {"game": "26.3", "horizon": mixin["compatibility"]["horizon_revision"], "id": "ironfurnaces_native",
        "mixins": "5a64af938ec86b00d53d16a408aabc0038fb3e57", "schema": 1, "version": version}
out = root / "dist" / f"ironfurnaces_native-{version}.hnmod"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    def add(name, data):
        info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, data)
    add("horizon-native.json", json.dumps(meta, indent=2, sort_keys=True) + "\n")
    for f in sorted((root / "native").glob("*.rs")) + [root / "native/horizon-mixin.toml"]:
        add(f"mixins/ironfurnaces_native/{f.name}", f.read_bytes())
    for name in ("LICENSE", "NOTICE-iron-furnaces.txt"):
        add(f"mixins/ironfurnaces_native/{name}", (root / name).read_bytes())
EOF
for f in "$here"/dist/ironfurnaces-"$version".hmod "$here"/dist/ironfurnaces_native-*.hnmod; do
  echo "$f  $(shasum -a 256 "$f" | cut -d' ' -f1)"
done
