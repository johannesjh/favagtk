#!/usr/bin/env python3
import re
from pathlib import Path

from setuptools import setup


def req(filename, folder=Path(__file__).parent / "requirements"):
    """Helper for loading dependencies from requirements files."""
    path = Path(folder) / filename
    with open(path) as file:
        return [
            line.strip()
            for line in file
            if not re.match("^-[cr]", line) and not re.match("^#", line)
        ]


# See setup.cfg for additional configuration.
setup(
    install_requires=req("req-sys.in") + req("req-main.in"),
    extras_require={"all": req("req-extras.in")},
    tests_require=req("req-dev.in"),
    include_package_data=True,
    package_data={"": ["*.svg", "*.ui"]},
)
