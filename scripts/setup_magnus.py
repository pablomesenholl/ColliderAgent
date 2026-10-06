"""Apply this repository's collider blueprints to the active Magnus station."""
import argparse
from pathlib import Path
import subprocess
import sys

from magnus import get_blueprint, save_blueprint
from magnus.client import parse_blueprint_yaml, strip_imports


BLUEPRINTS = (
    "madgraph-compile",
    "madgraph-compile-no-update",
    "madgraph-launch",
    "madanalysis-process",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-local", action="store_true",
                        help="Start local Magnus before applying repository blueprints")
    parser.add_argument("--check", action="store_true",
                        help="Verify registrations without changing them")
    args = parser.parse_args()
    if args.start_local and args.check:
        parser.error("--start-local and --check cannot be combined")
    root = Path(__file__).resolve().parents[1]
    definitions = []
    for name in BLUEPRINTS:
        meta = parse_blueprint_yaml(root / "src" / "blueprints" / f"{name}.yaml")
        code = strip_imports(meta["code"])
        compile(code, f"{name}.yaml", "exec")
        definitions.append((name, meta, code))
    if args.start_local:
        subprocess.run([str(Path(sys.executable).parent / "magnus"), "local", "start"],
                       check=True)
    for name, meta, code in definitions:
        if not args.check:
            save_blueprint(name, meta["title"], meta.get("description", ""), code)
        registered = get_blueprint(name)
        if registered["code"] != code:
            raise RuntimeError(f"{name}: registered code differs from repository definition")
        print(f"Verified {name}", flush=True)


if __name__ == "__main__":
    main()
