# Ultimate Palette Pro - Quick Start Guide

Welcome to **Ultimate Palette Pro** - the professional color palette tool with real-time Blender integration!

---

## Table of Contents

1. [Installation](#installation)
2. [Web App Basics](#web-app-basics)
3. [Blender Addon](#blender-addon)
4. [Web-Blender Sync](#web-blender-sync)
5. [Color Harmony Modes](#color-harmony-modes)
6. [Image Color Extraction](#image-color-extraction)
7. [Export Options](#export-options)
8. [Keyboard Shortcuts](#keyboard-shortcuts)
9. [Tips & Tricks](#tips--tricks)

---

## Installation

### Web App (Free)

**Option A: Use Online**
- Visit [https://sean4e.github.io/UPP/](https://sean4e.github.io/UPP/)
- Works instantly in any modern browser
- Supports PWA installation for offline use

**Option B: Install as Desktop App (PWA)**
1. Open the web app in Chrome/Edge
2. Click the install icon in the address bar
3. Enjoy offline access!

### Blender Addon ($24)

**Requirements:** Blender 4.0 or later

1. Download `UPP_v1.py` from your purchase
2. Open Blender → Edit → Preferences
3. Go to Add-ons → Install
4. Select the downloaded `UPP_v1.py` file
5. Enable "Ultimate Palette Pro" in the list
6. Press `N` to open the sidebar, find "Palette Pro" tab

---

## Web App Basics

### The Interface

```
┌─────────────────────────────────────────────────┐
│  [Logo]  Ultimate Palette Pro    [⚙️] [Connect] │
├─────────────────────────────────────────────────┤
│                                                 │
│     ┌───────────────────────────────────┐       │
│     │                                   │       │
│     │        Color Palette Grid         │       │
│     │         (4x4 to 16x16)            │       │
│     │                                   │       │
│     └───────────────────────────────────┘       │
│                                                 │
│  Harmony: [Dropdown]  Palette: [Dropdown]       │
│                                                 │
│  [🎲 Random] [🔄 Shuffle] [📤 Export]            │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Core Actions

| Action | How |
|--------|-----|
| Generate random palette | Click "Random" or press `Space` |
| Change harmony mode | Use the Harmony dropdown |
| Change grid size | Use the Grid dropdown (4x4 → 16x16) |
| Select a color | Click on any cell |
| Lock a color | Click the lock icon on hover, or press `L` |
| Copy color code | Click the hex code, or press `Ctrl+C` |
| Undo/Redo | `Ctrl+Z` / `Ctrl+Y` |

---

## Blender Addon

### Panel Location

Open the sidebar (`N` key) → "Palette Pro" tab

### Sections

1. **Color Palette**
   - View and manage your current palette
   - Click any color to select it
   - Use harmony presets to generate new palettes

2. **Apply to Scene**
   - Apply palette colors to selected objects
   - Options: Diffuse, Emission, World Background

3. **Extract from Scene**
   - Extract colors from selected objects
   - Extract from all scene materials

4. **Web Sync**
   - Start/Stop WebSocket server
   - Open web app directly
   - Real-time bidirectional sync

---

## Web-Blender Sync

The magic of Ultimate Palette Pro - edit palettes anywhere, sync everywhere!

### Setup

1. **In Blender:**
   - Open Palette Pro panel
   - Click "Start Server"
   - Server runs on `ws://localhost:8765`

2. **In Web App:**
   - Click "Connect" in the header
   - Green indicator = connected!

### How It Works

```
   Blender                      Web App
      │                            │
      │──── Palette Changes ─────▶│
      │                            │
      │◀──── Palette Changes ─────│
      │                            │
      ▼                            ▼
   Real-time bidirectional sync!
```

- Change a color in Blender → Web app updates instantly
- Generate palette on web → Blender receives it
- Lock colors sync both ways
- Grid size changes sync

---

## Color Harmony Modes

Understanding color theory for stunning palettes:

### Complementary
Two colors opposite on the color wheel. High contrast, vibrant.
```
     🔴 ─────────────── 🟢
        180° opposite
```

### Triadic
Three colors equally spaced (120° apart). Balanced, colorful.
```
          🔴
         ╱   ╲
       🟢 ─── 🔵
```

### Tetradic (Square)
Four colors equally spaced (90° apart). Rich, complex.
```
     🔴 ─── 🟡
      │     │
     🔵 ─── 🟢
```

### Analogous
Adjacent colors on the wheel. Harmonious, calm.
```
  🟠 ─ 🟡 ─ 🟢
  Neighbors
```

### Split-Complementary
Base color + two adjacent to its complement. Vibrant but easier than complementary.
```
         🔴
        ╱   ╲
     🔵 ─ ✖ ─ 🟣
         ↑
    (skip complement)
```

### Monochromatic
One hue, varied lightness/saturation. Elegant, cohesive.
```
  ⬜ ─ 🟦 ─ 🔵 ─ 🔷 ─ ⬛
      Same hue, different values
```

---

## Image Color Extraction

Extract palettes from any image!

### In Web App

1. Click the image icon in the toolbar
2. Upload any image (JPG, PNG, WebP, etc.)
3. K-means clustering extracts dominant colors
4. Palette is generated automatically

### Tips for Best Results

- Use images with distinct color regions
- Higher quality images = better extraction
- The algorithm finds dominant colors, not all colors
- Works great for: photos, artwork, movie stills, nature images

---

## Export Options

### Image Formats
- **PNG** - Lossless, transparent background support
- **JPEG** - Smaller file size
- **WebP** - Modern format, best compression
- **SVG** - Vector, infinitely scalable

### Code Formats
- **JSON** - Full palette data with all properties
- **CSS** - CSS custom properties (variables)
- **SCSS** - SCSS variables
- **Tailwind** - Tailwind config extend colors

### Example Exports

**JSON:**
```json
{
  "name": "Sunset Palette",
  "colors": [
    {"hex": "#ff6b6b", "name": "Coral Red"},
    {"hex": "#feca57", "name": "Mango Yellow"},
    {"hex": "#48dbfb", "name": "Sky Blue"}
  ]
}
```

**CSS:**
```css
:root {
  --color-1: #ff6b6b;
  --color-2: #feca57;
  --color-3: #48dbfb;
}
```

**Tailwind:**
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        palette: {
          1: '#ff6b6b',
          2: '#feca57',
          3: '#48dbfb',
        }
      }
    }
  }
}
```

---

## Keyboard Shortcuts

### Navigation
| Key | Action |
|-----|--------|
| `↑` `↓` `←` `→` | Navigate palette cells |
| `Tab` | Next cell |
| `Shift+Tab` | Previous cell |

### Generation
| Key | Action |
|-----|--------|
| `Space` | Random palette |
| `G` | Generate from seed |
| `S` | Shuffle colors |

### Editing
| Key | Action |
|-----|--------|
| `L` | Lock/unlock selected color |
| `Ctrl+C` | Copy selected color hex |
| `Delete` | Clear selected color |

### General
| Key | Action |
|-----|--------|
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+H` | Toggle history panel |
| `Ctrl+S` | Open export dialog |
| `?` | Show help overlay |

---

## Tips & Tricks

### 1. Lock Colors You Love
Before generating new palettes, lock colors you want to keep. Locked colors persist through randomization.

### 2. Use Harmony + Lock Combo
1. Find a base color you like
2. Lock it
3. Try different harmony modes
4. The locked color becomes the base for each harmony

### 3. Extract + Refine
1. Extract colors from an inspiration image
2. Lock the best ones
3. Generate variations to refine the palette

### 4. Sync Workflow
Keep the web app open on a second monitor while working in Blender. Changes sync instantly!

### 5. Grid Size Strategy
- **4x4 (16 colors)**: Quick concepts, simple themes
- **8x8 (64 colors)**: Standard project palettes
- **16x16 (256 colors)**: Comprehensive color systems

### 6. Keyboard Power User
Learn `Space` for random, `L` for lock, `Ctrl+Z` for undo. You'll work 3x faster!

### 7. Export for Teams
Use JSON export for full fidelity when sharing with team members. They can import and get exact colors.

---

## Troubleshooting

### Web App Won't Connect
- Ensure Blender server is running (check "Start Server")
- Check that localhost:8765 isn't blocked by firewall
- Try refreshing the web page

### Colors Look Different
- Ensure color management settings match
- sRGB is used throughout for consistency
- Monitor calibration affects perception

### Addon Not Appearing
- Ensure Blender 4.0+
- Check that addon is enabled in Preferences
- Press `N` to open sidebar
- Look for "Palette Pro" tab

---

## Support

- **Issues:** [GitHub Issues](https://github.com/sean4e/UPP/issues)
- **Updates:** Follow for new features and fixes
- **Created by:** 4E Virtual Design

---

*Happy color hunting!* 🎨
