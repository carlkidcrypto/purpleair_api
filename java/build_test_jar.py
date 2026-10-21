#!/usr/bin/env python3
"""
Helper script to compile Java test classes and build purpleair-api-tests.jar.
Used by java/meson.build.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


def resolve_executable(name: str) -> str:
    """Find and validate trusted system executable."""
    found = shutil.which(name)
    if not found:
        raise FileNotFoundError(f"Required tool not found in PATH: {name}")
    return os.path.abspath(found)


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: build_test_jar.py <api_jar> <test_src> <out_jar>",
            file=sys.stderr,
        )
        sys.exit(1)

    api_jar = str(pathlib.Path(sys.argv[1]).resolve())
    test_src = str(pathlib.Path(sys.argv[2]).resolve())
    out_jar = str(pathlib.Path(sys.argv[3]).resolve())

    javac_bin = resolve_executable("javac")
    jar_bin = resolve_executable("jar")

    tmp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(
            [javac_bin, "-cp", api_jar, "-d", tmp_dir, test_src],
            check=True,
        )
        subprocess.run(
            [jar_bin, "cf", out_jar, "-C", tmp_dir, "."],
            check=True,
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
