# Todos

- Publish on flathub

- Add a CI workflow (consider using GNOME infrastructure instead of github?)

- Licensing

  - License under GPL-2 for compatibility with beancount
  - Consider using https://reuse.software/

- Add screenshots to the README and to the appstream file

- WebKit packaging: org.gnome.Platform//42 does not come with webkit2gtk 5.0
  - I could include a webkite build similar to
    [the flatpak build of org.gabmus.gfeeds](https://github.com/flathub/org.gabmus.gfeeds/blob/2ac73b377018c2248198f8d6d9bbc35c0dca03c4/webkit.json)
  - Or I can use org.gnome.Platform//master which does include webkit2gtk 5.0
