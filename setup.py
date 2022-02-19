#!/usr/bin/env python3
import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join("requirements", "main.in")) as req:
    INSTALL_REQUIRES = list(req)

with open(os.path.join("requirements", "dev.in")) as req:
    TEST_REQUIRES = list(req)


# See setup.cfg for additional configuration.
setup(
    name="fava-gtk",
    version="0.1.5-dev",
    license="GPL-2.0",
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    package_data={"": ["*.svg", "*.ui"]},
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    entry_points={
        "console_scripts": [
            "fava-gtk = fava_gtk.main:main",
        ],
    },
    description="Use Fava and Beancount as a Desktop Application.",
    url="https://github.com/johannesjh/fava-gtk/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
        "Environment :: X11 Applications :: Gnome",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
)
