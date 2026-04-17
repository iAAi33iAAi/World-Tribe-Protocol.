import json
from pathlib import Path
from solcx import install_solc, set_solc_version, compile_standard

# Install and set Solidity compiler
version = '0.8.0'
install_solc(version)
set_solc_version(version)

# Determine paths
root = Path(__file__).resolve().parent.parent
source_path = root / 'WorldTribe.sol'
build_dir = root / 'build'
build_dir.mkdir(exist_ok=True)
out_path = build_dir / 'WorldTribe_compiled.json'

if not source_path.exists():
    raise SystemExit(f"Source file not found: {source_path}")

with open(source_path, 'r') as f:
    source = f.read()

# Compile
compiled = compile_standard({
    "language": "Solidity",
    "sources": {str(source_path.name): {"content": source}},
    "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}}
}, allow_paths=str(root))

# Write output
with open(out_path, 'w') as f:
    json.dump(compiled, f)

print('Compiled output written to', out_path)
