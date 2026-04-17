import argparse
import json
from pathlib import Path

from solcx import compile_standard, install_solc, set_solc_version


DEFAULT_VERSION = "0.8.0"


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent.parent
    default_source = root / "WorldTribe.sol"
    default_output = root / "build" / "WorldTribe_compiled.json"

    parser = argparse.ArgumentParser(
        description="Compile a Solidity contract and write ABI/bytecode output."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source,
        help=f"Path to the Solidity source file. Default: {default_source}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help=f"Path to the compiled JSON output. Default: {default_output}",
    )
    parser.add_argument(
        "--solc-version",
        default=DEFAULT_VERSION,
        help=f"Solidity compiler version to install and use. Default: {DEFAULT_VERSION}",
    )
    return parser.parse_args()


def compile_contract(source_path: Path, out_path: Path, solc_version: str) -> Path:
    root = Path(__file__).resolve().parent.parent
    source_path = source_path.resolve()
    out_path = out_path.resolve()

    if not source_path.exists():
        raise SystemExit(f"Source file not found: {source_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    source = source_path.read_text(encoding="utf-8")

    try:
        install_solc(solc_version)
        set_solc_version(solc_version)
        compiled = compile_standard(
            {
                "language": "Solidity",
                "sources": {source_path.name: {"content": source}},
                "settings": {
                    "outputSelection": {
                        "*": {"*": ["abi", "evm.bytecode.object"]}
                    }
                },
            },
            allow_paths=str(root),
        )
    except Exception as exc:
        raise SystemExit(f"Compilation failed: {exc}") from exc

    out_path.write_text(json.dumps(compiled, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    args = parse_args()
    output_path = compile_contract(args.source, args.output, args.solc_version)
    print(f"Compiled output written to {output_path}")


if __name__ == "__main__":
    main()
