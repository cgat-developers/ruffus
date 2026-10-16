"""Run each legacy test module in a fresh process to isolate pipeline state."""

import os
from pathlib import Path
import subprocess
import sys


def main():
    test_dir = Path(__file__).resolve().parent
    env = os.environ.copy()
    # Keep subprocesses on the same checkout and interpreter as this runner.
    env["PYTHONPATH"] = os.pathsep.join(
        filter(None, (str(test_dir.parent.parent), env.get("PYTHONPATH")))
    )
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), env["PATH"]))
    failed = []
    for pattern, args in (("test_*.py", ["-m", "pytest", *sys.argv[1:]]),
                          ("check_*.py", [])):
        for path in sorted(test_dir.glob(pattern)):
            print("Running {}".format(path.name), flush=True)
            result = subprocess.run(
                [sys.executable, *args, path.name], cwd=test_dir, env=env
            )
            if result.returncode:
                failed.append(path.name)
    if failed:
        print("Failed modules: " + ", ".join(failed), file=sys.stderr)
    return bool(failed)


if __name__ == "__main__":
    sys.exit(main())
