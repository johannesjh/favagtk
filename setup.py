#!/usr/bin/env python3
import os

from setuptools import setup

with open(os.path.join("requirements", "main.in")) as req:
    INSTALL_REQUIRES = list(req)

with open(os.path.join("requirements", "dev.in")) as req:
    TEST_REQUIRES = list(req)


# See setup.cfg for additional configuration.
setup(
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    include_package_data=True,
    package_data={"": ["*.svg", "*.ui"]},
)
