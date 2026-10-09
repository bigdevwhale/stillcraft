# Stillcraft

Small tools for a quieter mind. Landing page for a family of calm, offline, open-source apps:

- [Anyway](https://github.com/bigdevwhale/anyway): memento mori for Android
- [SwissZen](https://github.com/bigdevwhale/SwissZen): the mindfulness multi-tool for Android
- [FocusShield](https://github.com/bigdevwhale/focus-shield): a strict focus timer for Windows

Live: https://bigdevwhale.github.io/stillcraft/

A single static `index.html` (English and Russian, switchable) with images in `assets/`. No build step; GitHub Pages serves the `main` branch root.

## Adding an app

1. Put its images in `assets/`.
2. Copy one `<article class="app ...">` block in `index.html`, give it its own palette class, and add the strings to the `I18N.ru` dictionary.
3. Update the shelf count, the footer links and the closing download buttons.
