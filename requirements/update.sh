#!/bin/bash

# updates the json file with python dependencies for the flatpak build.

echo "Generating json file..."
./flatpak-pip-generator -r requirements.txt --runtime org.gnome.Sdk//master
echo "Done generating json file."
