# Ultimate Palette Pro

A professional color palette generator with harmony modes, image color extraction, and Blender sync.

## Features

- **Color Harmony Modes**: Complementary, Triadic, Tetradic, Analogous, Split-Complementary, Square, Monochromatic
- **Image Color Extraction**: Upload any image to extract a color palette using K-means clustering
- **Multiple Grid Sizes**: 4x4 up to 16x16 (256 colors)
- **Export Options**: PNG, JPEG, WebP, SVG, JSON, CSS, SCSS, Tailwind config
- **Blender Integration**: Real-time sync with Blender addon via WebSocket
- **Keyboard Shortcuts**: Space to randomize, arrow keys to navigate, and more
- **WCAG Accessibility Checker**: Check color contrast for accessibility compliance
- **PWA Support**: Install as a desktop app for offline use

## Quick Start

### Web App
1. Open `index.html` in a browser, or
2. Host on GitHub Pages / Netlify / Vercel

### Blender Addon
1. In Blender, go to Edit > Preferences > Add-ons > Install
2. Select `BlenderAddon/UPP_v1.py`
3. Enable "Ultimate Palette Pro" addon
4. Open the sidebar (N key) and find "Palette Pro" tab

### Web-Blender Sync
1. In Blender: Palette Pro panel > Web Sync > Start Server
2. In web app: Click "Connect" in the header
3. Palettes sync bidirectionally in real-time

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Random palette |
| G | Generate from seed |
| S | Shuffle colors |
| L | Lock/unlock selected |
| Ctrl+C | Copy selected color |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+H | Toggle history |
| Ctrl+S | Export |
| Arrow keys | Navigate palette |
| ? | Show help |

## PWA Installation

1. Open `generate-icons.html` in a browser
2. Download the 192px and 512px icons
3. Place them in the project root as `icon-192.png` and `icon-512.png`
4. Host the app on HTTPS
5. The "Install" prompt will appear in compatible browsers

## Tech Stack

- Vanilla HTML/CSS/JavaScript
- Tailwind CSS (via CDN)
- No build process required

## License

GPL-3.0 (Blender addon)
MIT (Web app)

---

Created by 4E Virtual Design
