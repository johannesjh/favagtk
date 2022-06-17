# Build Options

Available options are declared in `meson_options.txt`.

## Debug versus Release Builds

The "profile" option allows to toggle between a debug and release build.

The option (as well as other options) can be set in the following ways:

- In GNOME Builder's build options,
  by entering `-Dprofile=release` under "configure options".
  This modifies the flatpak `.json` manifest file.

- In the flatpak manifest `.json` file, the build can be configured
  as follows:

  ```json
  {
    "name": "favagtk",
    "config-opts": ["-Dprofile=release"]
  }
  ```

- If building from the commandline, the build option can be set as follows:
  `meson configure -Dprofile=release`.
  See the [meson documentation about build options](https://mesonbuild.com/Build-options.html)
  for further explanation.
