# Stillcraft

Small tools for a quieter mind. Landing page for a family of calm, offline, open-source apps:

- [Anyway](https://github.com/bigdevwhale/anyway): memento mori for Android
- [SwissZen](https://github.com/bigdevwhale/SwissZen): the mindfulness multi-tool for Android
- [FocusShield](https://github.com/bigdevwhale/focus-shield): a strict focus timer for Windows

Live: https://bigdevwhale.github.io/stillcraft/

Static site, no build step; GitHub Pages serves the `main` branch root.

- `index.html`: the landing page
- `apps/index.html`: the app catalog (`/apps/`)
- `assets/site.css`, `assets/site.js`: shared styles, language switch (EN/RU) and the breathing orb
- `assets/`: screenshots and icons

## Adding an app

1. Put its images in `assets/`.
2. Landing: copy one `<article class="app ...">` block in `index.html` and give it its own palette class.
3. Catalog: copy one `<a class="card">` in `apps/index.html` (version, status and platform badges).
4. Add the Russian strings to the `I18N.ru` dictionary in `assets/site.js`.
5. Update the app counts, the footer links on both pages and the closing download buttons.
