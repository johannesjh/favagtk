# Todos

- Build against a fixed version of org.gnome.Platform

  - This requires to build webkit as part of the flatpak build, because
    org.gnome.Platform//42 does not come with webkit2gtk 5.0
  - Note: I could include a webkite build similar to
    [the flatpak build of org.gabmus.gfeeds](https://github.com/flathub/org.gabmus.gfeeds/blob/2ac73b377018c2248198f8d6d9bbc35c0dca03c4/webkit.json)

- Add a CI workflow.

  - Consider using GNOME infrastructure instead of github,
    not sure what is easier.

- Publish on flathub

- Licensing

  - License under GPL-2 for compatibility with beancount
  - Consider using https://reuse.software/
    e.g., as a pre-commit hook
    https://git.fsfe.org/reuse/tool#run-as-pre-commit-hook

- Add screenshots to the README and to the appstream file
