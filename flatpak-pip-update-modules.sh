#!/bin/sh

PIP_GENERATOR="./flatpak-pip-generator --checker-data --runtime=org.gnome.Sdk//42"
$PIP_GENERATOR fava --output=python3-fava

