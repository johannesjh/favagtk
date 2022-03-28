#!/bin/sh

PIP_GENERATOR="./flatpak-pip-generator --checker-data --runtime=org.gnome.Sdk//42"

# force install setuptools
# note: must be force installed as it is in the GMOME sdk but not the platform
$PIP_GENERATOR --include-system-packages setuptools setuptools-scm --output=python3-setuptools
sed -e 's/--no-build-isolation/--no-build-isolation --ignore-installed/g' -i python3-setuptools.json

$PIP_GENERATOR fava --output=python3-fava

