# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Ultimate Palette Pro - Professional Color Palette Tool for Blender
A comprehensive color palette creation, management, and export toolkit.
"""

bl_info = {
    "name": "Ultimate Palette Pro",
    "author": "4E Virtual Design",
    "version": (1, 3, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Palette Pro",
    "description": "Professional color palette creation, management, and export toolkit",
    "warning": "",
    "doc_url": "https://4evirtualdesign.com/docs/ultimate-palette-pro",
    "tracker_url": "https://4evirtualdesign.com/support",
    "category": "Paint",
}

import bpy
import os
import math
import colorsys
import random
import numpy as np
from bpy.props import (
    StringProperty, IntProperty, FloatProperty, BoolProperty,
    EnumProperty, FloatVectorProperty, CollectionProperty, PointerProperty
)
from bpy.types import PropertyGroup, Operator, Panel, AddonPreferences
from mathutils import Color


# ============================================================================
# CONSTANTS & COLOR DATA
# ============================================================================

COLOR_NAMES = {
    (255, 0, 0): "Red", (255, 127, 0): "Orange", (255, 255, 0): "Yellow",
    (127, 255, 0): "Chartreuse", (0, 255, 0): "Green", (0, 255, 127): "Spring Green",
    (0, 255, 255): "Cyan", (0, 127, 255): "Azure", (0, 0, 255): "Blue",
    (127, 0, 255): "Violet", (255, 0, 255): "Magenta", (255, 0, 127): "Rose",
    (255, 255, 255): "White", (0, 0, 0): "Black", (128, 128, 128): "Gray",
    (165, 42, 42): "Brown", (255, 192, 203): "Pink", (75, 0, 130): "Indigo",
    (64, 224, 208): "Turquoise", (255, 215, 0): "Gold", (192, 192, 192): "Silver",
    (245, 245, 220): "Beige", (128, 0, 0): "Maroon", (128, 128, 0): "Olive",
    (0, 128, 128): "Teal", (0, 0, 128): "Navy", (230, 230, 250): "Lavender",
    (255, 127, 80): "Coral", (250, 128, 114): "Salmon", (240, 128, 128): "Light Coral",
    (255, 99, 71): "Tomato", (255, 69, 0): "Orange Red", (220, 20, 60): "Crimson",
}

PRESET_PALETTES = {
    "Nature": {
        "Forest": [(0.133, 0.286, 0.141), (0.180, 0.392, 0.184), (0.275, 0.510, 0.255), 
                   (0.467, 0.624, 0.329), (0.678, 0.776, 0.498), (0.855, 0.894, 0.733),
                   (0.349, 0.231, 0.133), (0.502, 0.349, 0.200), (0.647, 0.490, 0.286)],
        "Ocean": [(0.004, 0.129, 0.263), (0.012, 0.216, 0.400), (0.039, 0.329, 0.537),
                  (0.118, 0.467, 0.651), (0.259, 0.608, 0.757), (0.471, 0.753, 0.859),
                  (0.663, 0.867, 0.918), (0.827, 0.937, 0.961), (0.945, 0.976, 0.988)],
        "Sunset": [(0.153, 0.078, 0.157), (0.329, 0.094, 0.208), (0.541, 0.133, 0.235),
                   (0.749, 0.200, 0.220), (0.906, 0.337, 0.204), (0.969, 0.514, 0.220),
                   (0.988, 0.686, 0.302), (0.996, 0.839, 0.455), (0.996, 0.945, 0.694)],
        "Desert": [(0.925, 0.871, 0.780), (0.886, 0.773, 0.608), (0.831, 0.667, 0.459),
                   (0.765, 0.557, 0.345), (0.678, 0.447, 0.263), (0.573, 0.349, 0.208),
                   (0.451, 0.263, 0.165), (0.318, 0.188, 0.122), (0.188, 0.114, 0.082)],
        "Spring": [(0.984, 0.941, 0.941), (0.969, 0.867, 0.867), (0.949, 0.757, 0.769),
                   (0.922, 0.624, 0.655), (0.878, 0.478, 0.533), (0.502, 0.749, 0.439),
                   (0.392, 0.655, 0.357), (0.282, 0.545, 0.275), (0.188, 0.412, 0.204)],
    },
    "Mood": {
        "Warm": [(0.996, 0.957, 0.906), (0.996, 0.898, 0.769), (0.992, 0.816, 0.616),
                 (0.988, 0.714, 0.459), (0.976, 0.596, 0.306), (0.937, 0.471, 0.196),
                 (0.859, 0.337, 0.145), (0.741, 0.220, 0.118), (0.580, 0.125, 0.098)],
        "Cool": [(0.941, 0.957, 0.976), (0.851, 0.898, 0.949), (0.741, 0.827, 0.914),
                 (0.612, 0.745, 0.871), (0.475, 0.655, 0.820), (0.341, 0.557, 0.761),
                 (0.235, 0.459, 0.694), (0.157, 0.361, 0.620), (0.098, 0.267, 0.537)],
        "Pastel": [(0.980, 0.878, 0.878), (0.980, 0.902, 0.859), (0.996, 0.949, 0.878),
                   (0.898, 0.961, 0.906), (0.878, 0.941, 0.969), (0.867, 0.890, 0.969),
                   (0.918, 0.875, 0.957), (0.957, 0.875, 0.918), (0.969, 0.906, 0.898)],
        "Vibrant": [(0.996, 0.224, 0.212), (0.996, 0.541, 0.106), (0.996, 0.910, 0.220),
                    (0.447, 0.937, 0.278), (0.125, 0.820, 0.592), (0.141, 0.729, 0.937),
                    (0.275, 0.443, 0.925), (0.592, 0.275, 0.925), (0.914, 0.275, 0.698)],
        "Muted": [(0.565, 0.502, 0.475), (0.612, 0.557, 0.502), (0.659, 0.612, 0.549),
                  (0.706, 0.667, 0.596), (0.753, 0.722, 0.659), (0.682, 0.647, 0.600),
                  (0.600, 0.565, 0.533), (0.518, 0.486, 0.467), (0.439, 0.408, 0.400)],
    },
    "Retro": {
        "80s Neon": [(0.996, 0.043, 0.514), (0.996, 0.200, 0.200), (0.996, 0.600, 0.000),
                     (0.996, 0.996, 0.000), (0.000, 0.996, 0.467), (0.000, 0.933, 0.933),
                     (0.000, 0.467, 0.996), (0.467, 0.000, 0.996), (0.933, 0.000, 0.933)],
        "70s Earth": [(0.702, 0.400, 0.169), (0.859, 0.553, 0.263), (0.925, 0.725, 0.400),
                      (0.565, 0.451, 0.231), (0.388, 0.341, 0.208), (0.349, 0.298, 0.231),
                      (0.255, 0.227, 0.188), (0.624, 0.286, 0.165), (0.459, 0.176, 0.125)],
        "Vaporwave": [(0.098, 0.031, 0.169), (0.200, 0.043, 0.286), (0.353, 0.055, 0.467),
                      (0.565, 0.102, 0.565), (0.773, 0.200, 0.600), (0.953, 0.376, 0.541),
                      (0.059, 0.776, 0.773), (0.129, 0.937, 0.773), (0.392, 1.000, 0.827)],
        "Vintage": [(0.953, 0.941, 0.902), (0.886, 0.835, 0.741), (0.796, 0.706, 0.569),
                    (0.682, 0.557, 0.392), (0.549, 0.392, 0.263), (0.400, 0.271, 0.200),
                    (0.278, 0.208, 0.169), (0.184, 0.145, 0.129), (0.110, 0.094, 0.090)],
    },
    "UI/UX": {
        "Material Blue": [(0.890, 0.949, 0.992), (0.788, 0.898, 0.984), (0.565, 0.792, 0.976),
                          (0.329, 0.675, 0.961), (0.129, 0.588, 0.953), (0.118, 0.533, 0.898),
                          (0.098, 0.463, 0.824), (0.082, 0.396, 0.753), (0.051, 0.278, 0.631)],
        "Success/Error": [(0.220, 0.714, 0.333), (0.318, 0.769, 0.412), (0.431, 0.824, 0.502),
                          (0.996, 0.933, 0.247), (0.996, 0.796, 0.129), (0.996, 0.620, 0.106),
                          (0.957, 0.263, 0.212), (0.898, 0.224, 0.208), (0.827, 0.184, 0.184)],
        "Grayscale": [(0.000, 0.000, 0.000), (0.125, 0.125, 0.125), (0.250, 0.250, 0.250),
                      (0.375, 0.375, 0.375), (0.500, 0.500, 0.500), (0.625, 0.625, 0.625),
                      (0.750, 0.750, 0.750), (0.875, 0.875, 0.875), (1.000, 1.000, 1.000)],
        "Dark Mode": [(0.067, 0.071, 0.078), (0.102, 0.106, 0.118), (0.141, 0.145, 0.161),
                      (0.180, 0.188, 0.212), (0.220, 0.231, 0.263), (0.275, 0.290, 0.325),
                      (0.341, 0.357, 0.400), (0.420, 0.443, 0.494), (0.533, 0.561, 0.620)],
    },
    "Art Styles": {
        "Impressionist": [(0.561, 0.667, 0.773), (0.675, 0.761, 0.839), (0.788, 0.855, 0.898),
                          (0.733, 0.784, 0.584), (0.643, 0.722, 0.494), (0.537, 0.639, 0.396),
                          (0.843, 0.749, 0.608), (0.753, 0.631, 0.467), (0.643, 0.494, 0.341)],
        "Pop Art": [(0.996, 0.867, 0.000), (0.996, 0.000, 0.196), (0.000, 0.420, 0.769),
                    (0.996, 0.996, 0.996), (0.000, 0.000, 0.000), (0.996, 0.565, 0.706),
                    (0.467, 0.867, 0.467), (0.996, 0.545, 0.000), (0.667, 0.000, 0.667)],
        "Watercolor": [(0.957, 0.949, 0.941), (0.902, 0.886, 0.875), (0.839, 0.816, 0.800),
                       (0.820, 0.871, 0.894), (0.729, 0.816, 0.859), (0.627, 0.749, 0.816),
                       (0.867, 0.831, 0.808), (0.808, 0.749, 0.710), (0.741, 0.655, 0.608)],
        "Comic Book": [(0.996, 0.867, 0.467), (0.996, 0.545, 0.365), (0.867, 0.200, 0.267),
                       (0.333, 0.133, 0.200), (0.067, 0.067, 0.133), (0.467, 0.600, 0.867),
                       (0.667, 0.800, 0.933), (0.867, 0.933, 0.996), (0.996, 0.996, 0.867)],
    },
    "Cinematic": {
        "Teal & Orange": [(0.004, 0.216, 0.298), (0.016, 0.318, 0.404), (0.039, 0.431, 0.514),
                          (0.078, 0.557, 0.624), (0.878, 0.439, 0.157), (0.918, 0.529, 0.196),
                          (0.953, 0.624, 0.243), (0.980, 0.725, 0.310), (0.996, 0.831, 0.408)],
        "Noir": [(0.031, 0.031, 0.039), (0.063, 0.063, 0.078), (0.110, 0.106, 0.122),
                 (0.176, 0.169, 0.188), (0.267, 0.255, 0.282), (0.380, 0.365, 0.400),
                 (0.518, 0.502, 0.545), (0.690, 0.675, 0.722), (0.894, 0.886, 0.918)],
        "Sci-Fi": [(0.000, 0.043, 0.086), (0.000, 0.082, 0.165), (0.000, 0.137, 0.271),
                   (0.012, 0.686, 0.855), (0.047, 0.784, 0.925), (0.118, 0.875, 0.976),
                   (0.898, 0.333, 0.102), (0.937, 0.451, 0.176), (0.969, 0.584, 0.278)],
        "Horror": [(0.078, 0.039, 0.039), (0.137, 0.059, 0.055), (0.216, 0.078, 0.067),
                   (0.322, 0.094, 0.075), (0.459, 0.106, 0.078), (0.620, 0.114, 0.078),
                   (0.145, 0.129, 0.106), (0.180, 0.165, 0.133), (0.220, 0.204, 0.165)],
    },
}

HARMONY_TYPES = [
    ('COMPLEMENTARY', 'Complementary', 'Two colors opposite on the color wheel', 'MOD_HUE_SATURATION', 0),
    ('SPLIT_COMPLEMENTARY', 'Split Complementary', 'Base color with two adjacent to its complement', 'MOD_ARRAY', 1),
    ('TRIADIC', 'Triadic', 'Three colors equally spaced on the color wheel', 'PIVOT_MEDIAN', 2),
    ('TETRADIC', 'Tetradic', 'Four colors forming a rectangle on the wheel', 'MESH_PLANE', 3),
    ('ANALOGOUS', 'Analogous', 'Colors adjacent on the color wheel', 'IPO_EASE_IN_OUT', 4),
    ('SQUARE', 'Square', 'Four colors equally spaced on the wheel', 'MESH_GRID', 5),
    ('MONOCHROMATIC', 'Monochromatic', 'Variations of a single hue', 'SEQUENCE', 6),
    ('COMPOUND', 'Compound', 'Mix of complementary and analogous', 'RNA', 7),
]

# Enhanced arrangements with grouped/compound sorting
ARRANGEMENT_TYPES = [
    ('ORIGINAL', 'Original Order', 'Keep original order', 'FORWARD', 0),
    ('LUMINANCE_ASC', 'Light → Dark', 'Sort by brightness, light to dark', 'LIGHT_SUN', 1),
    ('LUMINANCE_DESC', 'Dark → Light', 'Sort by brightness, dark to light', 'SHADING_SOLID', 2),
    ('HUE', 'Hue (Rainbow)', 'Sort by hue in rainbow order', 'COLORSET_13_VEC', 3),
    ('HUE_LUMINANCE', 'Hue + Tone', 'Group by hue, then sort by brightness', 'NODE_COMPOSITING', 4),
    ('HUE_SATURATION', 'Hue + Saturation', 'Group by hue, then sort by saturation', 'BRUSHES_ALL', 5),
    ('SATURATION_ASC', 'Low → High Sat', 'Sort by saturation, low to high', 'MOD_OPACITY', 6),
    ('SATURATION_DESC', 'High → Low Sat', 'Sort by saturation, high to low', 'PROP_ON', 7),
    ('WARM_COOL', 'Warm → Cool', 'Sort from warm to cool colors', 'LIGHT_POINT', 8),
    ('COOL_WARM', 'Cool → Warm', 'Sort from cool to warm colors', 'FREEZE', 9),
    ('GRADIENT', 'Smooth Gradient', 'Optimal perceptual gradient ordering', 'IPO_BEZIER', 10),
    ('RANDOM', 'Random', 'Randomize color order', 'SHADERFX', 11),
    ('SPIRAL', 'Spiral', 'Arrange in spiral pattern from center', 'FORCE_VORTEX', 12),
    ('DIAGONAL', 'Diagonal Bands', 'Arrange in diagonal bands', 'OUTLINER_DATA_LATTICE', 13),
    ('CHECKERBOARD', 'Checkerboard', 'Alternating pattern', 'VIEW_ORTHO', 14),
]

EXTRACTION_ALGORITHMS = [
    ('KMEANS', 'K-Means', 'Fast ML-based clustering', 'OUTLINER_OB_POINTCLOUD', 0),
    ('MEDIAN_CUT', 'Median Cut', 'Balanced color distribution', 'MOD_REMESH', 1),
    ('DOMINANT', 'Dominant', 'Most frequent colors', 'COMMUNITY', 2),
    ('DIVERSE', 'Diverse', 'Maximum color variety', 'PARTICLE_DATA', 3),
]

GRID_SIZES = [
    ('2', '2×2', '4 colors - Minimal'),
    ('3', '3×3', '9 colors - Compact'),
    ('4', '4×4', '16 colors - Standard'),
    ('5', '5×5', '25 colors'),
    ('6', '6×6', '36 colors'),
    ('8', '8×8', '64 colors'),
    ('10', '10×10', '100 colors'),
    ('12', '12×12', '144 colors'),
    ('16', '16×16', '256 colors'),
]

EXPORT_FORMATS = [
    ('PNG', 'PNG', 'Lossless', 'FILE_IMAGE', 0),
    ('JPEG', 'JPEG', 'Lossy compression', 'FILE_IMAGE', 1),
    ('EXR', 'OpenEXR', 'HDR format', 'FILE_IMAGE', 2),
    ('TIFF', 'TIFF', 'High quality', 'FILE_IMAGE', 3),
    ('BMP', 'BMP', 'Bitmap', 'FILE_IMAGE', 4),
    ('TGA', 'TGA', 'Targa', 'FILE_IMAGE', 5),
]

EXPORT_RESOLUTIONS = [
    ('4', '4×4', 'Micro - Perfect for 2×2 grids'),
    ('8', '8×8', 'Minimal - 1 pixel per color'),
    ('16', '16×16', 'Tiny'),
    ('32', '32×32', 'Small'),
    ('64', '64×64', 'Medium'),
    ('128', '128×128', 'Standard'),
    ('256', '256×256', 'Large'),
    ('512', '512×512', 'HD'),
    ('1024', '1024×1024', '1K'),
    ('2048', '2048×2048', '2K'),
    ('4096', '4096×4096', '4K Ultra HD'),
    ('8192', '8192×8192', '8K Ultra HD'),
]

GENERATION_SOURCES = [
    ('PRESET', 'Preset', 'Load from built-in presets', 'PRESET', 0),
    ('COLOR', 'Color', 'Generate from seed color', 'COLOR', 1),
    ('IMAGE', 'Image', 'Extract from image', 'IMAGE_DATA', 2),
    ('RANDOM', 'Random', 'Random harmonious colors', 'SHADERFX', 3),
]

CLIPBOARD_FORMATS = [
    ('HEX', 'HEX', '#RRGGBB format'),
    ('RGB', 'RGB', 'rgb(r, g, b) format'),
    ('RGB_255', 'RGB 255', '(255, 255, 255) format'),
    ('HSL', 'HSL', 'hsl(h, s%, l%) format'),
    ('ARRAY_HEX', 'Array HEX', 'JavaScript array of hex'),
    ('ARRAY_RGB', 'Array RGB', 'JavaScript array of RGB'),
    ('CSS_VARS', 'CSS Variables', 'CSS custom properties'),
    ('SCSS', 'SCSS Variables', 'SCSS variable declarations'),
    ('TAILWIND', 'Tailwind Config', 'Tailwind CSS config'),
    ('PYTHON', 'Python', 'Python list of tuples'),
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clamp(value, min_val=0.0, max_val=1.0):
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV."""
    return colorsys.rgb_to_hsv(r, g, b)


def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB."""
    return colorsys.hsv_to_rgb(h, s, v)


def get_luminance(r, g, b):
    """Calculate perceived luminance (ITU-R BT.709)."""
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_color_temperature(r, g, b):
    """Estimate color temperature (warm positive, cool negative)."""
    return (r - b) + (r - g) * 0.5


def get_color_name(r, g, b):
    """Get nearest named color - optimized version."""
    r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
    
    min_dist = float('inf')
    nearest_name = "Color"
    
    for (cr, cg, cb), name in COLOR_NAMES.items():
        # Skip early if any channel diff is too large
        if abs(cr - r_int) > 100 and abs(cg - g_int) > 100:
            continue
        dist = (cr - r_int)**2 + (cg - g_int)**2 + (cb - b_int)**2
        if dist < min_dist:
            min_dist = dist
            nearest_name = name
    
    return nearest_name


def shift_hue(r, g, b, amount):
    """Shift hue by amount (0-1)."""
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + amount) % 1.0
    return hsv_to_rgb(h, s, v)


def adjust_saturation(r, g, b, factor):
    """Adjust saturation by factor."""
    h, s, v = rgb_to_hsv(r, g, b)
    s = clamp(s * factor)
    return hsv_to_rgb(h, s, v)


def adjust_value(r, g, b, factor):
    """Adjust value/brightness by factor."""
    h, s, v = rgb_to_hsv(r, g, b)
    v = clamp(v * factor)
    return hsv_to_rgb(h, s, v)


def color_distance(c1, c2):
    """Calculate perceptual color distance."""
    r1, g1, b1 = c1[:3]
    r2, g2, b2 = c2[:3]
    # Weighted Euclidean distance (red-mean approximation)
    rmean = (r1 + r2) / 2
    dr = r1 - r2
    dg = g1 - g2
    db = b1 - b2
    return ((2 + rmean) * dr * dr + 4 * dg * dg + (3 - rmean) * db * db) ** 0.5


def generate_harmony_colors(base_color, harmony_type, count=9):
    """Generate colors based on color theory harmony - optimized."""
    r, g, b = base_color[:3]
    h, s, v = rgb_to_hsv(r, g, b)
    colors = []
    
    if harmony_type == 'COMPLEMENTARY':
        half = count // 2
        for i in range(half):
            t = i / max(half - 1, 1)
            new_s = s * (0.5 + t * 0.5)
            new_v = v * (0.6 + t * 0.4)
            colors.append(hsv_to_rgb(h, clamp(new_s), clamp(new_v)))
        for i in range(count - half):
            t = i / max(count - half - 1, 1)
            new_s = s * (0.5 + t * 0.5)
            new_v = v * (0.6 + t * 0.4)
            colors.append(hsv_to_rgb((h + 0.5) % 1.0, clamp(new_s), clamp(new_v)))
    
    elif harmony_type == 'SPLIT_COMPLEMENTARY':
        angles = [0, 0.417, 0.583]
        per_angle = count // 3
        for i, angle in enumerate(angles):
            new_h = (h + angle) % 1.0
            num = per_angle + (1 if i < count % 3 else 0)
            for j in range(num):
                t = j / max(num - 1, 1)
                colors.append(hsv_to_rgb(new_h, clamp(s * (0.6 + t * 0.4)), clamp(v * (0.5 + t * 0.5))))
    
    elif harmony_type == 'TRIADIC':
        angles = [0, 0.333, 0.667]
        per_angle = count // 3
        for i, angle in enumerate(angles):
            new_h = (h + angle) % 1.0
            num = per_angle + (1 if i < count % 3 else 0)
            for j in range(num):
                t = j / max(num - 1, 1)
                colors.append(hsv_to_rgb(new_h, clamp(s * (0.6 + t * 0.4)), clamp(v * (0.5 + t * 0.5))))
    
    elif harmony_type == 'TETRADIC':
        angles = [0, 0.167, 0.5, 0.667]
        per_angle = count // 4
        for i, angle in enumerate(angles):
            new_h = (h + angle) % 1.0
            num = per_angle + (1 if i < count % 4 else 0)
            for j in range(num):
                t = j / max(num - 1, 1)
                colors.append(hsv_to_rgb(new_h, clamp(s * (0.6 + t * 0.4)), clamp(v * (0.5 + t * 0.5))))
    
    elif harmony_type == 'ANALOGOUS':
        for i in range(count):
            offset = (i - count // 2) * 0.083
            new_h = (h + offset) % 1.0
            # Deterministic variation instead of random for speed
            sv_offset = (i % 5 - 2) * 0.1
            colors.append(hsv_to_rgb(new_h, clamp(s + sv_offset), clamp(v - sv_offset * 0.5)))
    
    elif harmony_type == 'SQUARE':
        angles = [0, 0.25, 0.5, 0.75]
        per_angle = count // 4
        for i, angle in enumerate(angles):
            new_h = (h + angle) % 1.0
            num = per_angle + (1 if i < count % 4 else 0)
            for j in range(num):
                t = j / max(num - 1, 1)
                colors.append(hsv_to_rgb(new_h, clamp(s * (0.5 + t * 0.5)), clamp(v * (0.5 + t * 0.5))))
    
    elif harmony_type == 'MONOCHROMATIC':
        for i in range(count):
            t = i / max(count - 1, 1)
            colors.append(hsv_to_rgb(h, clamp(s * (0.3 + t * 0.7)), clamp(v * (0.3 + t * 0.7))))
    
    elif harmony_type == 'COMPOUND':
        angles = [0, 0.083, -0.083, 0.5, 0.583, 0.417]
        per_angle = count // 6
        for i, angle in enumerate(angles):
            new_h = (h + angle) % 1.0
            num = per_angle + (1 if i < count % 6 else 0)
            for j in range(num):
                t = j / max(num - 1, 1)
                colors.append(hsv_to_rgb(new_h, clamp(s * (0.6 + t * 0.4)), clamp(v * (0.6 + t * 0.4))))
    
    while len(colors) < count:
        colors.append(colors[-1] if colors else (0.5, 0.5, 0.5))
    
    return colors[:count]


def arrange_colors(colors, arrangement_type, grid_size):
    """Arrange colors according to specified pattern - with new compound arrangements."""
    color_list = list(colors)
    n = grid_size
    
    if arrangement_type == 'ORIGINAL':
        return color_list
    
    elif arrangement_type == 'LUMINANCE_ASC':
        return sorted(color_list, key=lambda c: get_luminance(*c[:3]))
    
    elif arrangement_type == 'LUMINANCE_DESC':
        return sorted(color_list, key=lambda c: -get_luminance(*c[:3]))
    
    elif arrangement_type == 'HUE':
        return sorted(color_list, key=lambda c: rgb_to_hsv(*c[:3])[0])
    
    elif arrangement_type == 'HUE_LUMINANCE':
        # Group by hue (12 segments), then sort by luminance within each group
        def hue_lum_key(c):
            h, s, v = rgb_to_hsv(*c[:3])
            hue_bucket = int(h * 12)  # 12 hue segments
            lum = get_luminance(*c[:3])
            return (hue_bucket, lum)
        return sorted(color_list, key=hue_lum_key)
    
    elif arrangement_type == 'HUE_SATURATION':
        # Group by hue (12 segments), then sort by saturation within each group
        def hue_sat_key(c):
            h, s, v = rgb_to_hsv(*c[:3])
            hue_bucket = int(h * 12)
            return (hue_bucket, s)
        return sorted(color_list, key=hue_sat_key)
    
    elif arrangement_type == 'SATURATION_ASC':
        return sorted(color_list, key=lambda c: rgb_to_hsv(*c[:3])[1])
    
    elif arrangement_type == 'SATURATION_DESC':
        return sorted(color_list, key=lambda c: -rgb_to_hsv(*c[:3])[1])
    
    elif arrangement_type == 'WARM_COOL':
        return sorted(color_list, key=lambda c: -get_color_temperature(*c[:3]))
    
    elif arrangement_type == 'COOL_WARM':
        return sorted(color_list, key=lambda c: get_color_temperature(*c[:3]))
    
    elif arrangement_type == 'GRADIENT':
        # Traveling salesman-style ordering for smooth gradients
        if len(color_list) <= 1:
            return color_list
        
        result = [color_list[0]]
        remaining = list(color_list[1:])
        
        while remaining:
            last = result[-1]
            # Find nearest unvisited color
            nearest_idx = 0
            nearest_dist = float('inf')
            for i, c in enumerate(remaining):
                d = color_distance(last, c)
                if d < nearest_dist:
                    nearest_dist = d
                    nearest_idx = i
            result.append(remaining.pop(nearest_idx))
        
        return result
    
    elif arrangement_type == 'RANDOM':
        shuffled = list(color_list)
        random.shuffle(shuffled)
        return shuffled
    
    elif arrangement_type == 'SPIRAL':
        result = [None] * (n * n)
        x, y = 0, 0
        dx, dy = 1, 0
        
        sorted_colors = sorted(color_list, key=lambda c: get_luminance(*c[:3]))
        
        for i in range(min(len(sorted_colors), n * n)):
            result[y * n + x] = sorted_colors[i]
            
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and result[ny * n + nx] is None:
                x, y = nx, ny
            else:
                dx, dy = -dy, dx
                x, y = x + dx, y + dy
        
        return [c if c else (0.5, 0.5, 0.5) for c in result]
    
    elif arrangement_type == 'DIAGONAL':
        sorted_colors = sorted(color_list, key=lambda c: get_luminance(*c[:3]))
        result = [None] * (n * n)
        
        idx = 0
        for diag in range(2 * n - 1):
            for i in range(max(0, diag - n + 1), min(diag + 1, n)):
                j = diag - i
                if j < n and idx < len(sorted_colors):
                    result[i * n + j] = sorted_colors[idx]
                    idx += 1
        
        return [c if c else (0.5, 0.5, 0.5) for c in result]
    
    elif arrangement_type == 'CHECKERBOARD':
        sorted_light = sorted(color_list, key=lambda c: -get_luminance(*c[:3]))
        sorted_dark = sorted(color_list, key=lambda c: get_luminance(*c[:3]))
        
        result = []
        li, di = 0, 0
        
        for row in range(n):
            for col in range(n):
                if (row + col) % 2 == 0:
                    if li < len(sorted_light):
                        result.append(sorted_light[li])
                        li += 1
                    else:
                        result.append((0.8, 0.8, 0.8))
                else:
                    if di < len(sorted_dark):
                        result.append(sorted_dark[di])
                        di += 1
                    else:
                        result.append((0.2, 0.2, 0.2))
        
        return result
    
    return color_list


def expand_colors_to_grid(colors, target_count):
    """Expand a list of colors to fill the target count intelligently."""
    if len(colors) == 0:
        return [(0.5, 0.5, 0.5)] * target_count
    
    if len(colors) >= target_count:
        return list(colors[:target_count])
    
    result = list(colors)
    original_count = len(colors)
    
    while len(result) < target_count:
        for i in range(original_count):
            if len(result) >= target_count:
                break
            
            r, g, b = colors[i][:3]
            h, s, v = rgb_to_hsv(r, g, b)
            
            variation_index = len(result) // original_count
            if variation_index % 2 == 0:
                new_v = clamp(v * (1.0 + 0.15 * (variation_index // 2 + 1)))
                new_s = clamp(s * 0.9)
            else:
                new_v = clamp(v * (1.0 - 0.15 * (variation_index // 2 + 1)))
                new_s = clamp(s * 1.1)
            
            result.append(hsv_to_rgb(h, new_s, new_v))
    
    return result[:target_count]


# ============================================================================
# OPTIMIZED IMAGE EXTRACTION FUNCTIONS
# ============================================================================

def downsample_pixels(pixels, max_samples=5000):
    """Downsample pixel array for faster processing."""
    if len(pixels) <= max_samples:
        return pixels
    indices = np.random.choice(len(pixels), max_samples, replace=False)
    return pixels[indices]


def extract_colors_kmeans(image_path, num_colors, max_samples=5000, max_iters=10):
    """Extract colors using K-means clustering - optimized."""
    try:
        img = bpy.data.images.load(image_path)
        pixels = np.array(img.pixels[:]).reshape(-1, 4)
        rgb_pixels = pixels[:, :3]
        
        # Filter by alpha
        alpha = pixels[:, 3]
        rgb_pixels = rgb_pixels[alpha > 0.1]
        
        if len(rgb_pixels) == 0:
            bpy.data.images.remove(img)
            return [(0.5, 0.5, 0.5)] * num_colors
        
        # Downsample for speed
        rgb_pixels = downsample_pixels(rgb_pixels, max_samples)
        
        # Initialize centers using k-means++
        centers = [rgb_pixels[np.random.randint(len(rgb_pixels))]]
        for _ in range(num_colors - 1):
            dists = np.min([np.sum((rgb_pixels - c) ** 2, axis=1) for c in centers], axis=0)
            probs = dists / dists.sum()
            centers.append(rgb_pixels[np.random.choice(len(rgb_pixels), p=probs)])
        centers = np.array(centers)
        
        # K-means iterations (reduced)
        for _ in range(max_iters):
            distances = np.sqrt(((rgb_pixels[:, None] - centers) ** 2).sum(axis=2))
            labels = distances.argmin(axis=1)
            
            new_centers = np.array([
                rgb_pixels[labels == k].mean(axis=0) if (labels == k).sum() > 0 else centers[k]
                for k in range(num_colors)
            ])
            
            if np.allclose(centers, new_centers, atol=0.01):
                break
            centers = new_centers
        
        bpy.data.images.remove(img)
        return [tuple(c) for c in centers]
    
    except Exception as e:
        print(f"[UPP] K-means extraction error: {e}")
        return [(0.5, 0.5, 0.5)] * num_colors


def extract_colors_median_cut(image_path, num_colors, max_samples=5000):
    """Extract colors using median cut algorithm - optimized."""
    try:
        img = bpy.data.images.load(image_path)
        pixels = np.array(img.pixels[:]).reshape(-1, 4)
        rgb_pixels = pixels[:, :3]
        
        alpha = pixels[:, 3]
        rgb_pixels = rgb_pixels[alpha > 0.1]
        
        if len(rgb_pixels) == 0:
            bpy.data.images.remove(img)
            return [(0.5, 0.5, 0.5)] * num_colors
        
        rgb_pixels = downsample_pixels(rgb_pixels, max_samples)
        
        def median_cut_recursive(pxls, depth):
            if depth == 0 or len(pxls) == 0:
                return [pxls.mean(axis=0)] if len(pxls) > 0 else [np.array([0.5, 0.5, 0.5])]
            
            ranges = pxls.max(axis=0) - pxls.min(axis=0)
            channel = ranges.argmax()
            
            sorted_pxls = pxls[pxls[:, channel].argsort()]
            mid = len(sorted_pxls) // 2
            
            return (median_cut_recursive(sorted_pxls[:mid], depth - 1) +
                    median_cut_recursive(sorted_pxls[mid:], depth - 1))
        
        depth = int(np.ceil(np.log2(num_colors)))
        colors = median_cut_recursive(rgb_pixels, depth)
        
        bpy.data.images.remove(img)
        return [tuple(c) for c in colors[:num_colors]]
    
    except Exception as e:
        print(f"[UPP] Median cut extraction error: {e}")
        return [(0.5, 0.5, 0.5)] * num_colors


def extract_colors_dominant(image_path, num_colors, max_samples=8000):
    """Extract dominant (most frequent) colors - optimized."""
    try:
        img = bpy.data.images.load(image_path)
        pixels = np.array(img.pixels[:]).reshape(-1, 4)
        rgb_pixels = pixels[:, :3]
        
        rgb_pixels = downsample_pixels(rgb_pixels, max_samples)
        
        # Quantize to reduce unique colors (5-bit per channel = 32K colors max)
        quantized = (rgb_pixels * 31).astype(np.uint8)
        
        # Pack into single int for faster unique counting
        packed = quantized[:, 0].astype(np.uint32) << 16 | quantized[:, 1].astype(np.uint32) << 8 | quantized[:, 2]
        unique, counts = np.unique(packed, return_counts=True)
        
        # Get top colors
        top_indices = counts.argsort()[-num_colors:][::-1]
        top_packed = unique[top_indices]
        
        colors = []
        for p in top_packed:
            r = ((p >> 16) & 0xFF) / 31.0
            g = ((p >> 8) & 0xFF) / 31.0
            b = (p & 0xFF) / 31.0
            colors.append((r, g, b))
        
        bpy.data.images.remove(img)
        return colors
    
    except Exception as e:
        print(f"[UPP] Dominant extraction error: {e}")
        return [(0.5, 0.5, 0.5)] * num_colors


def extract_colors_diverse(image_path, num_colors, max_samples=3000):
    """Extract visually diverse colors - optimized."""
    try:
        img = bpy.data.images.load(image_path)
        pixels = np.array(img.pixels[:]).reshape(-1, 4)
        rgb_pixels = pixels[:, :3]
        
        alpha = pixels[:, 3]
        rgb_pixels = rgb_pixels[alpha > 0.1]
        
        if len(rgb_pixels) == 0:
            bpy.data.images.remove(img)
            return [(0.5, 0.5, 0.5)] * num_colors
        
        rgb_pixels = downsample_pixels(rgb_pixels, max_samples)
        
        # Start with random color
        colors = [rgb_pixels[np.random.randint(len(rgb_pixels))]]
        
        for _ in range(num_colors - 1):
            # Vectorized distance calculation
            min_distances = np.full(len(rgb_pixels), np.inf)
            
            for color in colors:
                distances = np.sum((rgb_pixels - color) ** 2, axis=1)
                min_distances = np.minimum(min_distances, distances)
            
            colors.append(rgb_pixels[min_distances.argmax()])
        
        bpy.data.images.remove(img)
        return [tuple(c) for c in colors]
    
    except Exception as e:
        print(f"[UPP] Diverse extraction error: {e}")
        return [(0.5, 0.5, 0.5)] * num_colors


# ============================================================================
# PREVIEW IMAGE MANAGEMENT
# ============================================================================

class PreviewManager:
    """Manages preview images for the addon (Singleton)."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.preview_images = {}
            self.initialized = True
    
    def create_grid_preview(self, colors, grid_size, name="palette_grid_preview"):
        """Create a preview image of the color grid - optimized."""
        img_name = f"UPP_{name}"
        
        if img_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[img_name])
        
        resolution = 256
        img = bpy.data.images.new(img_name, resolution, resolution, alpha=False)
        
        # Pre-allocate and fill using numpy broadcasting
        pixels = np.zeros((resolution, resolution, 4))
        cell_size = resolution // grid_size
        
        for i, color in enumerate(colors):
            if i >= grid_size * grid_size:
                break
            
            row = i // grid_size
            col = i % grid_size
            
            x1, x2 = col * cell_size, (col + 1) * cell_size
            y1 = (grid_size - 1 - row) * cell_size
            y2 = y1 + cell_size
            
            pixels[y1:y2, x1:x2] = [color[0], color[1], color[2], 1.0]
        
        img.pixels[:] = pixels.ravel().tolist()
        img.update()
        img.preview_ensure()
        
        self.preview_images[name] = img
        return img
    
    def load_source_preview(self, filepath, name="palette_source_preview"):
        """Load source image for preview - optimized."""
        img_name = f"UPP_{name}"
        
        if img_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[img_name])
        
        try:
            img = bpy.data.images.load(filepath)
            img.name = img_name
            
            # Scale down large images
            max_size = 256
            if img.size[0] > max_size or img.size[1] > max_size:
                scale = max_size / max(img.size[0], img.size[1])
                new_w = int(img.size[0] * scale)
                new_h = int(img.size[1] * scale)
                img.scale(new_w, new_h)
            
            img.preview_ensure()
            
            self.preview_images[name] = img
            return img
        except Exception as e:
            print(f"[UPP] Failed to load preview: {e}")
            return None
    
    def get_preview(self, name):
        """Get preview image by name."""
        return self.preview_images.get(name)
    
    def cleanup(self):
        """Remove all preview images."""
        for name, img in list(self.preview_images.items()):
            try:
                if img.name in bpy.data.images:
                    bpy.data.images.remove(img)
            except:
                pass
        self.preview_images.clear()


# ============================================================================
# UPDATE CALLBACKS
# ============================================================================

def update_preview(self, context):
    """Update the grid preview when colors change."""
    props = context.scene.ultimate_palette
    if len(props.colors) > 0:
        colors = [tuple(c.color) for c in props.colors]
        grid_size = int(props.grid_size)
        pm = PreviewManager()
        pm.create_grid_preview(colors, grid_size)


def update_grid_size(self, context):
    """Handle grid size changes - resize palette intelligently."""
    props = context.scene.ultimate_palette
    grid_size = int(props.grid_size)
    num_colors = grid_size * grid_size
    
    if len(props.colors) == 0:
        return
    
    existing = [tuple(c.color) for c in props.colors]
    
    if len(existing) < num_colors:
        new_colors = expand_colors_to_grid(existing, num_colors)
    else:
        new_colors = existing[:num_colors]
    
    props.colors.clear()
    for color in new_colors:
        item = props.colors.add()
        item.color = color[:3]
        item.name = get_color_name(*color[:3])
    
    pm = PreviewManager()
    pm.create_grid_preview(new_colors, grid_size)


def update_source_image(self, context):
    """Load image preview when path changes."""
    props = context.scene.ultimate_palette
    
    if not props.source_image_path:
        return
    
    filepath = bpy.path.abspath(props.source_image_path)
    if os.path.exists(filepath):
        pm = PreviewManager()
        pm.load_source_preview(filepath)


# ============================================================================
# PROPERTY GROUPS
# ============================================================================

class UPP_PaletteColorItem(PropertyGroup):
    """Single color in the palette."""
    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=3,
        min=0.0, max=1.0,
        default=(0.5, 0.5, 0.5),
        update=update_preview
    )
    name: StringProperty(name="Name", default="")
    locked: BoolProperty(name="Locked", default=False)


class UPP_PalettePreset(PropertyGroup):
    """Saved palette preset."""
    name: StringProperty(name="Name", default="Untitled")
    category: StringProperty(name="Category", default="Custom")
    colors: CollectionProperty(type=UPP_PaletteColorItem)
    grid_size: IntProperty(name="Grid Size", default=4)
    favorite: BoolProperty(name="Favorite", default=False)
    tags: StringProperty(name="Tags", default="")


class UPP_Properties(PropertyGroup):
    """Main property group for the addon."""
    
    # Generation source
    generation_source: EnumProperty(
        name="Generate From",
        items=GENERATION_SOURCES,
        default='PRESET',
        description="Choose how to generate the palette"
    )
    
    # Grid settings
    grid_size: EnumProperty(
        name="Grid Size",
        items=GRID_SIZES,
        default='4',
        update=update_grid_size,
        description="Number of colors in the palette"
    )
    
    # Palette colors
    colors: CollectionProperty(type=UPP_PaletteColorItem)
    active_color_index: IntProperty(name="Active Color Index", default=0)
    
    # Color generation settings
    seed_color: FloatVectorProperty(
        name="Seed Color",
        subtype='COLOR',
        size=3,
        min=0.0, max=1.0,
        default=(0.8, 0.2, 0.2),
        description="Base color for palette generation"
    )
    
    harmony_type: EnumProperty(
        name="Harmony",
        items=HARMONY_TYPES,
        default='TRIADIC',
        description="Color theory harmony type"
    )
    
    # Preset browser
    preset_category: EnumProperty(
        name="Category",
        items=[
            ('ALL', 'All', 'Show all presets'),
            ('Nature', 'Nature', 'Nature themes'),
            ('Mood', 'Mood', 'Mood themes'),
            ('Retro', 'Retro', 'Retro themes'),
            ('UI/UX', 'UI/UX', 'UI/UX themes'),
            ('Art Styles', 'Art Styles', 'Art style themes'),
            ('Cinematic', 'Cinematic', 'Cinematic themes'),
        ],
        default='ALL',
        description="Filter presets by category"
    )
    
    selected_preset_category: StringProperty(name="Selected Category", default="")
    selected_preset_name: StringProperty(name="Selected Preset", default="")
    
    # Image extraction settings
    source_image_path: StringProperty(
        name="Source Image",
        subtype='FILE_PATH',
        default="",
        description="Image to extract colors from",
        update=update_source_image
    )
    
    extraction_algorithm: EnumProperty(
        name="Algorithm",
        items=EXTRACTION_ALGORITHMS,
        default='KMEANS',
        description="Color extraction algorithm"
    )
    
    # Arrangement
    arrangement_type: EnumProperty(
        name="Arrangement",
        items=ARRANGEMENT_TYPES,
        default='ORIGINAL',
        description="How to arrange colors in the grid"
    )
    
    # HSV Adjustments
    hue_shift: FloatProperty(
        name="Hue Shift",
        min=-1.0, max=1.0, default=0.0,
        subtype='FACTOR',
        description="Shift all hues"
    )
    saturation_mult: FloatProperty(
        name="Saturation",
        min=0.0, max=2.0, default=1.0,
        subtype='FACTOR',
        description="Multiply saturation"
    )
    value_mult: FloatProperty(
        name="Value",
        min=0.0, max=2.0, default=1.0,
        subtype='FACTOR',
        description="Multiply value/brightness"
    )
    temperature_shift: FloatProperty(
        name="Temperature",
        min=-1.0, max=1.0, default=0.0,
        subtype='FACTOR',
        description="Shift colors warmer or cooler"
    )
    
    # Export settings
    export_format: EnumProperty(
        name="Format",
        items=EXPORT_FORMATS,
        default='PNG',
        description="Image export format"
    )
    export_resolution: EnumProperty(
        name="Resolution",
        items=EXPORT_RESOLUTIONS,
        default='256',
        description="Export image resolution"
    )
    export_path: StringProperty(
        name="Export Path",
        subtype='FILE_PATH',
        default="//palette_export",
        description="Path to save exported palette"
    )
    
    # Clipboard format
    clipboard_format: EnumProperty(
        name="Format",
        items=CLIPBOARD_FORMATS,
        default='HEX',
        description="Format for clipboard copy"
    )
    
    # Colorblind simulation
    colorblind_mode: EnumProperty(
        name="Simulation",
        items=[
            ('NONE', 'None', 'Normal vision'),
            ('DEUTERANOPIA', 'Deuteranopia', 'Green-weak'),
            ('PROTANOPIA', 'Protanopia', 'Red-weak'),
            ('TRITANOPIA', 'Tritanopia', 'Blue-yellow'),
        ],
        default='NONE',
        description="Simulate colorblind vision"
    )
    
    # Saved presets
    saved_presets: CollectionProperty(type=UPP_PalettePreset)
    active_preset_index: IntProperty(name="Active Preset", default=0)

    # Web Sync settings
    websocket_port: IntProperty(
        name="Port",
        min=1024, max=65535, default=8765,
        description="WebSocket server port"
    )
    websocket_running: BoolProperty(
        name="Server Running",
        default=False,
        description="Whether the WebSocket server is running"
    )


# ============================================================================
# WEBSOCKET SERVER (Embedded for easy deployment)
# ============================================================================

import threading
import json
import socket
import struct
import hashlib
import base64

class SimpleWebSocketServer:
    """Minimal WebSocket server - no external dependencies."""

    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        self.on_message = None
        self.on_connect = None
        self.on_disconnect = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)
        self.running = True
        print(f"[UPP WebSocket] Server started on ws://{self.host}:{self.port}")

        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket, address), daemon=True)
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"[UPP WebSocket] Accept error: {e}")

    def stop(self):
        self.running = False
        for client in self.clients[:]:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        if self.server_socket:
            self.server_socket.close()
        print("[UPP WebSocket] Server stopped")

    def _handle_client(self, client_socket, address):
        try:
            # Perform WebSocket handshake
            request = client_socket.recv(4096).decode('utf-8')
            if 'Upgrade: websocket' not in request:
                client_socket.close()
                return

            # Extract Sec-WebSocket-Key
            key = None
            for line in request.split('\r\n'):
                if line.startswith('Sec-WebSocket-Key:'):
                    key = line.split(': ')[1].strip()
                    break

            if not key:
                client_socket.close()
                return

            # Generate accept key
            accept_key = base64.b64encode(
                hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()
            ).decode()

            # Send handshake response
            response = (
                'HTTP/1.1 101 Switching Protocols\r\n'
                'Upgrade: websocket\r\n'
                'Connection: Upgrade\r\n'
                f'Sec-WebSocket-Accept: {accept_key}\r\n\r\n'
            )
            client_socket.send(response.encode())

            self.clients.append(client_socket)
            print(f"[UPP WebSocket] Client connected from {address}")

            if self.on_connect:
                self.on_connect(client_socket)

            # Message loop
            while self.running:
                try:
                    message = self._recv_frame(client_socket)
                    if message is None:
                        break
                    if self.on_message:
                        self.on_message(client_socket, message)
                except:
                    break

        except Exception as e:
            print(f"[UPP WebSocket] Client error: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            try:
                client_socket.close()
            except:
                pass
            if self.on_disconnect:
                self.on_disconnect(client_socket)
            print(f"[UPP WebSocket] Client disconnected")

    def _recv_frame(self, client_socket):
        """Receive and decode a WebSocket frame."""
        try:
            header = client_socket.recv(2)
            if len(header) < 2:
                return None

            opcode = header[0] & 0x0F
            if opcode == 0x8:  # Close frame
                return None

            masked = header[1] & 0x80
            payload_len = header[1] & 0x7F

            if payload_len == 126:
                payload_len = struct.unpack('>H', client_socket.recv(2))[0]
            elif payload_len == 127:
                payload_len = struct.unpack('>Q', client_socket.recv(8))[0]

            mask = client_socket.recv(4) if masked else None
            payload = client_socket.recv(payload_len)

            if masked and mask:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))

            return payload.decode('utf-8')
        except:
            return None

    def send(self, client_socket, message):
        """Send a message to a specific client."""
        try:
            payload = message.encode('utf-8')
            frame = bytearray()
            frame.append(0x81)  # Text frame

            if len(payload) <= 125:
                frame.append(len(payload))
            elif len(payload) <= 65535:
                frame.append(126)
                frame.extend(struct.pack('>H', len(payload)))
            else:
                frame.append(127)
                frame.extend(struct.pack('>Q', len(payload)))

            frame.extend(payload)
            client_socket.send(bytes(frame))
        except Exception as e:
            print(f"[UPP WebSocket] Send error: {e}")

    def broadcast(self, message, exclude=None):
        """Send a message to all connected clients."""
        for client in self.clients[:]:
            if client != exclude:
                self.send(client, message)


# Global WebSocket server instance
_ws_server = None
_ws_thread = None


def get_palette_as_json(context):
    """Get current palette as JSON for web app."""
    props = context.scene.ultimate_palette
    colors = []
    for item in props.palette_colors:
        r = int(item.color[0] * 255)
        g = int(item.color[1] * 255)
        b = int(item.color[2] * 255)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")

    return json.dumps({
        "type": "palette",
        "colors": colors,
        "gridSize": int(props.grid_size)
    })


def apply_palette_from_json(context, data):
    """Apply palette received from web app."""
    props = context.scene.ultimate_palette
    props.palette_colors.clear()

    for hex_color in data.get("colors", []):
        item = props.palette_colors.add()
        hex_clean = hex_color.lstrip('#')
        r = int(hex_clean[0:2], 16) / 255.0
        g = int(hex_clean[2:4], 16) / 255.0
        b = int(hex_clean[4:6], 16) / 255.0
        item.color = (r, g, b)

    grid_size = data.get("gridSize", 8)
    if str(grid_size) in [item[0] for item in GRID_SIZES]:
        props.grid_size = str(grid_size)

    # Force UI update
    for area in bpy.context.screen.areas:
        area.tag_redraw()


# ============================================================================
# OPERATORS
# ============================================================================

class UPP_OT_GeneratePalette(Operator):
    """Generate palette based on current settings"""
    bl_idname = "upp.generate_palette"
    bl_label = "Generate Palette"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        num_colors = grid_size * grid_size
        
        colors = []
        source = props.generation_source
        
        if source == 'PRESET':
            cat = props.selected_preset_category
            name = props.selected_preset_name
            
            if cat in PRESET_PALETTES and name in PRESET_PALETTES[cat]:
                preset_colors = list(PRESET_PALETTES[cat][name])
                colors = expand_colors_to_grid(preset_colors, num_colors)
                self.report({'INFO'}, f"Loaded: {name}")
            else:
                self.report({'WARNING'}, "Select a preset first")
                return {'CANCELLED'}
        
        elif source == 'COLOR':
            colors = generate_harmony_colors(
                props.seed_color,
                props.harmony_type,
                num_colors
            )
            self.report({'INFO'}, f"Generated {props.harmony_type} palette")
        
        elif source == 'IMAGE':
            if not props.source_image_path:
                self.report({'ERROR'}, "No image selected")
                return {'CANCELLED'}
            
            filepath = bpy.path.abspath(props.source_image_path)
            if not os.path.exists(filepath):
                self.report({'ERROR'}, f"Image not found")
                return {'CANCELLED'}
            
            algo = props.extraction_algorithm
            if algo == 'KMEANS':
                colors = extract_colors_kmeans(filepath, num_colors)
            elif algo == 'MEDIAN_CUT':
                colors = extract_colors_median_cut(filepath, num_colors)
            elif algo == 'DOMINANT':
                colors = extract_colors_dominant(filepath, num_colors)
            else:
                colors = extract_colors_diverse(filepath, num_colors)
            
            self.report({'INFO'}, f"Extracted {len(colors)} colors")
        
        elif source == 'RANDOM':
            base_hue = random.random()
            
            for i in range(num_colors):
                h = (base_hue + (i / num_colors) * 0.6 + random.uniform(-0.1, 0.1)) % 1.0
                s = random.uniform(0.4, 1.0)
                v = random.uniform(0.4, 1.0)
                colors.append(hsv_to_rgb(h, s, v))
            
            self.report({'INFO'}, f"Generated random palette")
        
        # Update palette
        props.colors.clear()
        for color in colors:
            item = props.colors.add()
            item.color = color[:3]
            item.name = get_color_name(*color[:3])
        
        # Update preview
        pm = PreviewManager()
        pm.create_grid_preview(colors, grid_size)
        
        return {'FINISHED'}


class UPP_OT_LoadPreset(Operator):
    """Load a preset palette"""
    bl_idname = "upp.load_preset"
    bl_label = "Load Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    category: StringProperty()
    name: StringProperty()
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        props.selected_preset_category = self.category
        props.selected_preset_name = self.name
        props.generation_source = 'PRESET'
        
        bpy.ops.upp.generate_palette()
        
        return {'FINISHED'}


class UPP_OT_ApplyArrangement(Operator):
    """Apply current arrangement to colors"""
    bl_idname = "upp.apply_arrangement"
    bl_label = "Apply"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        arranged = arrange_colors(colors, props.arrangement_type, grid_size)
        
        for i, color in enumerate(arranged):
            if i < len(props.colors):
                props.colors[i].color = color[:3]
                props.colors[i].name = get_color_name(*color[:3])
        
        pm = PreviewManager()
        pm.create_grid_preview(arranged, grid_size)
        
        self.report({'INFO'}, f"Applied {props.arrangement_type}")
        return {'FINISHED'}


class UPP_OT_ApplyAdjustments(Operator):
    """Apply HSV adjustments to all colors"""
    bl_idname = "upp.apply_adjustments"
    bl_label = "Apply"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        colors = []
        for item in props.colors:
            r, g, b = item.color[:3]
            
            if props.hue_shift != 0:
                r, g, b = shift_hue(r, g, b, props.hue_shift)
            
            if props.saturation_mult != 1.0:
                r, g, b = adjust_saturation(r, g, b, props.saturation_mult)
            
            if props.value_mult != 1.0:
                r, g, b = adjust_value(r, g, b, props.value_mult)
            
            if props.temperature_shift != 0:
                temp = props.temperature_shift * 0.1
                r = clamp(r + temp)
                b = clamp(b - temp)
            
            item.color = (r, g, b)
            item.name = get_color_name(r, g, b)
            colors.append((r, g, b))
        
        props.hue_shift = 0.0
        props.saturation_mult = 1.0
        props.value_mult = 1.0
        props.temperature_shift = 0.0
        
        pm = PreviewManager()
        pm.create_grid_preview(colors, int(props.grid_size))
        
        self.report({'INFO'}, "Applied adjustments")
        return {'FINISHED'}


class UPP_OT_FlipHorizontal(Operator):
    """Flip palette horizontally"""
    bl_idname = "upp.flip_horizontal"
    bl_label = "Flip H"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        result = []
        for row in range(grid_size):
            start = row * grid_size
            end = start + grid_size
            result.extend(reversed(colors[start:end]))
        
        for i, color in enumerate(result):
            if i < len(props.colors):
                props.colors[i].color = color
        
        pm = PreviewManager()
        pm.create_grid_preview(result, grid_size)
        
        return {'FINISHED'}


class UPP_OT_FlipVertical(Operator):
    """Flip palette vertically"""
    bl_idname = "upp.flip_vertical"
    bl_label = "Flip V"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        result = []
        for row in range(grid_size - 1, -1, -1):
            start = row * grid_size
            end = start + grid_size
            result.extend(colors[start:end])
        
        for i, color in enumerate(result):
            if i < len(props.colors):
                props.colors[i].color = color
        
        pm = PreviewManager()
        pm.create_grid_preview(result, grid_size)
        
        return {'FINISHED'}


class UPP_OT_RotateLeft(Operator):
    """Rotate palette 90° counter-clockwise"""
    bl_idname = "upp.rotate_left"
    bl_label = "Rotate CCW"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        result = [None] * (grid_size * grid_size)
        for row in range(grid_size):
            for col in range(grid_size):
                old_idx = row * grid_size + col
                new_row = grid_size - 1 - col
                new_col = row
                new_idx = new_row * grid_size + new_col
                result[new_idx] = colors[old_idx]
        
        for i, color in enumerate(result):
            if i < len(props.colors):
                props.colors[i].color = color
        
        pm = PreviewManager()
        pm.create_grid_preview(result, grid_size)
        
        return {'FINISHED'}


class UPP_OT_RotateRight(Operator):
    """Rotate palette 90° clockwise"""
    bl_idname = "upp.rotate_right"
    bl_label = "Rotate CW"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        result = [None] * (grid_size * grid_size)
        for row in range(grid_size):
            for col in range(grid_size):
                old_idx = row * grid_size + col
                new_row = col
                new_col = grid_size - 1 - row
                new_idx = new_row * grid_size + new_col
                result[new_idx] = colors[old_idx]
        
        for i, color in enumerate(result):
            if i < len(props.colors):
                props.colors[i].color = color
        
        pm = PreviewManager()
        pm.create_grid_preview(result, grid_size)
        
        return {'FINISHED'}


class UPP_OT_ExportImage(Operator):
    """Export palette as an image"""
    bl_idname = "upp.export_image"
    bl_label = "Export Image"
    bl_options = {'REGISTER'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    def invoke(self, context, event):
        props = context.scene.ultimate_palette
        
        ext_map = {
            'PNG': '.png', 'JPEG': '.jpg', 'EXR': '.exr',
            'TIFF': '.tiff', 'BMP': '.bmp', 'TGA': '.tga'
        }
        ext = ext_map.get(props.export_format, '.png')
        
        self.filepath = bpy.path.abspath(props.export_path) + ext
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        resolution = int(props.export_resolution)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        img = bpy.data.images.new("UPP_Export_Temp", resolution, resolution, alpha=False)
        
        pixels = np.zeros((resolution, resolution, 4))
        cell_size = resolution // grid_size
        
        for i, color in enumerate(colors):
            if i >= grid_size * grid_size:
                break
            
            row = i // grid_size
            col = i % grid_size
            
            x1, x2 = col * cell_size, (col + 1) * cell_size
            y1 = (grid_size - 1 - row) * cell_size
            y2 = y1 + cell_size
            
            pixels[y1:y2, x1:x2] = [color[0], color[1], color[2], 1.0]
        
        img.pixels[:] = pixels.ravel().tolist()
        
        img.filepath_raw = self.filepath
        
        format_settings = {
            'PNG': 'PNG', 'JPEG': 'JPEG', 'EXR': 'OPEN_EXR',
            'TIFF': 'TIFF', 'BMP': 'BMP', 'TGA': 'TARGA'
        }
        img.file_format = format_settings.get(props.export_format, 'PNG')
        
        img.save_render(self.filepath)
        bpy.data.images.remove(img)
        
        self.report({'INFO'}, f"Exported to {self.filepath}")
        return {'FINISHED'}


class UPP_OT_CreateMaterial(Operator):
    """Create a material with palette as texture"""
    bl_idname = "upp.create_material"
    bl_label = "Create Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        while len(colors) < grid_size * grid_size:
            colors.append((0.5, 0.5, 0.5))
        
        img_name = "UPP_Palette_Texture"
        if img_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[img_name])
        
        resolution = 256
        img = bpy.data.images.new(img_name, resolution, resolution, alpha=False)
        
        pixels = np.zeros((resolution, resolution, 4))
        cell_size = resolution // grid_size
        
        for i, color in enumerate(colors):
            if i >= grid_size * grid_size:
                break
            
            row = i // grid_size
            col = i % grid_size
            
            x1, x2 = col * cell_size, (col + 1) * cell_size
            y1 = (grid_size - 1 - row) * cell_size
            y2 = y1 + cell_size
            
            pixels[y1:y2, x1:x2] = [color[0], color[1], color[2], 1.0]
        
        img.pixels[:] = pixels.ravel().tolist()
        img.update()
        
        mat_name = "UPP_Palette_Material"
        if mat_name in bpy.data.materials:
            mat = bpy.data.materials[mat_name]
        else:
            mat = bpy.data.materials.new(mat_name)
        
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        tex = nodes.new('ShaderNodeTexImage')
        tex.location = (-300, 0)
        tex.image = img
        tex.interpolation = 'Closest'
        
        links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
        
        self.report({'INFO'}, "Created palette material")
        return {'FINISHED'}


class UPP_OT_SetupTexturePaint(Operator):
    """Setup texture paint mode with palette"""
    bl_idname = "upp.setup_texture_paint"
    bl_label = "Setup Texture Paint"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        palette_name = "UPP_Palette"
        if palette_name in bpy.data.palettes:
            palette = bpy.data.palettes[palette_name]
            palette.colors.clear()
        else:
            palette = bpy.data.palettes.new(palette_name)
        
        for item in props.colors:
            color = palette.colors.new()
            color.color = item.color[:3]
        
        ts = context.tool_settings
        ts.image_paint.palette = palette
        
        self.report({'INFO'}, "Texture paint palette ready")
        return {'FINISHED'}


class UPP_OT_CopyToClipboard(Operator):
    """Copy palette to clipboard"""
    bl_idname = "upp.copy_to_clipboard"
    bl_label = "Copy"
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        fmt = props.clipboard_format
        
        colors = [(c.color[0], c.color[1], c.color[2]) for c in props.colors]
        
        if fmt == 'HEX':
            text = '\n'.join([
                f"#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}"
                for c in colors
            ])
        elif fmt == 'RGB':
            text = '\n'.join([
                f"rgb({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})"
                for c in colors
            ])
        elif fmt == 'RGB_255':
            text = '\n'.join([
                f"({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)})"
                for c in colors
            ])
        elif fmt == 'HSL':
            lines = []
            for c in colors:
                h, l, s = colorsys.rgb_to_hls(c[0], c[1], c[2])
                lines.append(f"hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)")
            text = '\n'.join(lines)
        elif fmt == 'ARRAY_HEX':
            hex_colors = [
                f"'#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}'"
                for c in colors
            ]
            text = f"[{', '.join(hex_colors)}]"
        elif fmt == 'ARRAY_RGB':
            rgb_arrays = [f"[{int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}]" for c in colors]
            text = f"[{', '.join(rgb_arrays)}]"
        elif fmt == 'CSS_VARS':
            text = ':root {\n'
            for i, c in enumerate(colors):
                text += f"  --color-{i+1}: #{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x};\n"
            text += '}'
        elif fmt == 'SCSS':
            lines = []
            for i, c in enumerate(colors):
                lines.append(f"$color-{i+1}: #{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x};")
            text = '\n'.join(lines)
        elif fmt == 'TAILWIND':
            text = "colors: {\n"
            for i, c in enumerate(colors):
                text += f"  'palette-{i+1}': '#{int(c[0]*255):02x}{int(c[1]*255):02x}{int(c[2]*255):02x}',\n"
            text += "}"
        elif fmt == 'PYTHON':
            text = '[\n'
            for c in colors:
                text += f"    ({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f}),\n"
            text += ']'
        else:
            text = str(colors)
        
        context.window_manager.clipboard = text
        self.report({'INFO'}, f"Copied {len(colors)} colors")
        return {'FINISHED'}


class UPP_OT_SavePreset(Operator):
    """Save current palette as preset"""
    bl_idname = "upp.save_preset"
    bl_label = "Save Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    preset_name: StringProperty(name="Name", default="My Palette")
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        preset = props.saved_presets.add()
        preset.name = self.preset_name
        preset.grid_size = int(props.grid_size)
        
        for item in props.colors:
            color = preset.colors.add()
            color.color = item.color
            color.name = item.name
        
        self.report({'INFO'}, f"Saved: {self.preset_name}")
        return {'FINISHED'}


class UPP_OT_LoadSavedPreset(Operator):
    """Load a saved preset"""
    bl_idname = "upp.load_saved_preset"
    bl_label = "Load"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: IntProperty()
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        if self.index < len(props.saved_presets):
            preset = props.saved_presets[self.index]
            
            props.grid_size = str(preset.grid_size)
            
            props.colors.clear()
            for c in preset.colors:
                item = props.colors.add()
                item.color = c.color
                item.name = c.name
            
            colors = [tuple(c.color) for c in props.colors]
            pm = PreviewManager()
            pm.create_grid_preview(colors, preset.grid_size)
            
            self.report({'INFO'}, f"Loaded: {preset.name}")
        
        return {'FINISHED'}


class UPP_OT_DeleteSavedPreset(Operator):
    """Delete a saved preset"""
    bl_idname = "upp.delete_saved_preset"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}
    
    index: IntProperty()
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        
        if self.index < len(props.saved_presets):
            name = props.saved_presets[self.index].name
            props.saved_presets.remove(self.index)
            self.report({'INFO'}, f"Deleted: {name}")
        
        return {'FINISHED'}


class UPP_OT_UpdatePreview(Operator):
    """Update the grid preview image"""
    bl_idname = "upp.update_preview"
    bl_label = "Refresh"
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        colors = [tuple(c.color) for c in props.colors]
        
        if len(colors) == 0:
            for i in range(grid_size * grid_size):
                h = i / (grid_size * grid_size)
                colors.append(hsv_to_rgb(h, 0.7, 0.8))
        
        pm = PreviewManager()
        pm.create_grid_preview(colors, grid_size)
        
        return {'FINISHED'}


class UPP_OT_InitializePalette(Operator):
    """Initialize palette with default colors"""
    bl_idname = "upp.initialize_palette"
    bl_label = "Initialize Palette"
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        num_colors = grid_size * grid_size
        
        if len(props.colors) == 0:
            for i in range(num_colors):
                item = props.colors.add()
                h = i / num_colors
                item.color = hsv_to_rgb(h, 0.7, 0.8)
                item.name = get_color_name(*item.color)
        
        colors = [tuple(c.color) for c in props.colors]
        pm = PreviewManager()
        pm.create_grid_preview(colors, grid_size)
        
        return {'FINISHED'}


class UPP_OT_BatchCreateMaterials(Operator):
    """Create material for each color"""
    bl_idname = "upp.batch_create_materials"
    bl_label = "Material Per Color"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.ultimate_palette
        count = 0
        
        for i, item in enumerate(props.colors):
            mat_name = f"UPP_{i+1:02d}_{item.name}"
            
            if mat_name in bpy.data.materials:
                mat = bpy.data.materials[mat_name]
            else:
                mat = bpy.data.materials.new(mat_name)
            
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            
            bsdf = None
            for node in nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf = node
                    break
            
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (*item.color, 1.0)
            
            count += 1
        
        self.report({'INFO'}, f"Created {count} materials")
        return {'FINISHED'}


class UPP_OT_StartWebSocket(Operator):
    """Start WebSocket server for web app sync"""
    bl_idname = "upp.start_websocket"
    bl_label = "Start Web Sync"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global _ws_server, _ws_thread

        props = context.scene.ultimate_palette

        if props.websocket_running:
            self.report({'WARNING'}, "Server already running")
            return {'CANCELLED'}

        def on_message(client, message):
            try:
                data = json.loads(message)
                if data.get("type") == "palette":
                    # Use timer to run in main thread
                    def apply_in_main():
                        apply_palette_from_json(bpy.context, data)
                        return None
                    bpy.app.timers.register(apply_in_main, first_interval=0.1)
            except Exception as e:
                print(f"[UPP WebSocket] Message error: {e}")

        def on_connect(client):
            # Send current palette to new client
            try:
                _ws_server.send(client, get_palette_as_json(bpy.context))
            except:
                pass

        _ws_server = SimpleWebSocketServer('localhost', props.websocket_port)
        _ws_server.on_message = on_message
        _ws_server.on_connect = on_connect

        _ws_thread = threading.Thread(target=_ws_server.start, daemon=True)
        _ws_thread.start()

        props.websocket_running = True
        self.report({'INFO'}, f"WebSocket server started on port {props.websocket_port}")
        return {'FINISHED'}


class UPP_OT_StopWebSocket(Operator):
    """Stop WebSocket server"""
    bl_idname = "upp.stop_websocket"
    bl_label = "Stop Web Sync"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global _ws_server, _ws_thread

        props = context.scene.ultimate_palette

        if not props.websocket_running:
            self.report({'WARNING'}, "Server not running")
            return {'CANCELLED'}

        if _ws_server:
            _ws_server.stop()
            _ws_server = None

        props.websocket_running = False
        self.report({'INFO'}, "WebSocket server stopped")
        return {'FINISHED'}


class UPP_OT_SendToWeb(Operator):
    """Send current palette to connected web clients"""
    bl_idname = "upp.send_to_web"
    bl_label = "Send to Web"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global _ws_server

        props = context.scene.ultimate_palette

        if not props.websocket_running or not _ws_server:
            self.report({'WARNING'}, "Server not running")
            return {'CANCELLED'}

        message = get_palette_as_json(context)
        _ws_server.broadcast(message)

        num_clients = len(_ws_server.clients) if _ws_server else 0
        self.report({'INFO'}, f"Sent palette to {num_clients} client(s)")
        return {'FINISHED'}


# ============================================================================
# PANELS
# ============================================================================

class UPP_PT_MainPanel(Panel):
    """Main panel for Ultimate Palette Pro"""
    bl_label = "Ultimate Palette Pro"
    bl_idname = "UPP_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    
    def draw_header(self, context):
        self.layout.label(text="", icon='COLORSET_13_VEC')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        if len(props.colors) == 0:
            box = layout.box()
            box.scale_y = 1.5
            box.operator("upp.initialize_palette", text="Initialize Palette", icon='ADD')


class UPP_PT_GeneratePanel(Panel):
    """Generate panel"""
    bl_label = "Generate"
    bl_idname = "UPP_PT_generate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    
    def draw_header(self, context):
        self.layout.label(text="", icon='PLAY')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        # Source selector (tabs style)
        row = layout.row(align=True)
        row.prop(props, "generation_source", expand=True)
        
        box = layout.box()
        
        # Source-specific options
        if props.generation_source == 'PRESET':
            box.prop(props, "preset_category", text="", icon='COLLECTION_COLOR_04')
            
            col = box.column(align=True)
            for category, presets in PRESET_PALETTES.items():
                if props.preset_category != 'ALL' and props.preset_category != category:
                    continue
                
                col.label(text=category, icon='FILE_FOLDER')
                
                for name in presets.keys():
                    row = col.row(align=True)
                    is_selected = (props.selected_preset_category == category and 
                                   props.selected_preset_name == name)
                    
                    op = row.operator("upp.load_preset", 
                                      text=name, 
                                      icon='RADIOBUT_ON' if is_selected else 'RADIOBUT_OFF',
                                      depress=is_selected)
                    op.category = category
                    op.name = name
        
        elif props.generation_source == 'COLOR':
            row = box.row(align=True)
            row.label(text="", icon='COLOR')
            row.prop(props, "seed_color", text="")
            
            box.prop(props, "harmony_type", text="", icon='MOD_HUE_SATURATION')
        
        elif props.generation_source == 'IMAGE':
            box.prop(props, "source_image_path", text="", icon='FILE_IMAGE')
            
            # Show image thumbnail immediately
            img_name = "UPP_palette_source_preview"
            if img_name in bpy.data.images:
                img = bpy.data.images[img_name]
                if img.preview is None:
                    img.preview_ensure()
                if img.preview and img.preview.icon_id:
                    thumb_box = box.box()
                    thumb_box.template_icon(icon_value=img.preview.icon_id, scale=5.0)
            
            box.prop(props, "extraction_algorithm", text="", icon='OUTLINER_OB_POINTCLOUD')
        
        elif props.generation_source == 'RANDOM':
            box.label(text="Random harmonious colors", icon='SHADERFX')
        
        layout.separator()
        
        # Generate button
        row = layout.row(align=True)
        row.scale_y = 1.4
        row.operator("upp.generate_palette", text="Generate", icon='PLAY')


class UPP_PT_GridPanel(Panel):
    """Palette Grid panel"""
    bl_label = "Palette Grid"
    bl_idname = "UPP_PT_grid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    
    def draw_header(self, context):
        self.layout.label(text="", icon='MESH_GRID')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        grid_size = int(props.grid_size)
        
        # Grid size and transforms at TOP
        row = layout.row(align=True)
        row.prop(props, "grid_size", text="")
        row.separator()
        row.operator("upp.flip_horizontal", text="", icon='ARROW_LEFTRIGHT')
        row.operator("upp.flip_vertical", text="", icon='EMPTY_SINGLE_ARROW')
        row.operator("upp.rotate_left", text="", icon='LOOP_BACK')
        row.operator("upp.rotate_right", text="", icon='LOOP_FORWARDS')
        row.separator()
        row.operator("upp.update_preview", text="", icon='FILE_REFRESH')
        
        # Preview image
        img_name = "UPP_palette_grid_preview"
        if img_name in bpy.data.images:
            img = bpy.data.images[img_name]
            if img.preview is None:
                img.preview_ensure()
            if img.preview and img.preview.icon_id:
                box = layout.box()
                box.template_icon(icon_value=img.preview.icon_id, scale=11.0)
        else:
            box = layout.box()
            box.label(text="No preview", icon='IMAGE_DATA')
        
        # Color grid - allow up to 16 columns
        grid_box = layout.box()
        grid_flow = grid_box.grid_flow(
            row_major=True, 
            columns=grid_size,  # Use actual grid size, not capped at 8
            even_columns=True, 
            even_rows=True,
            align=True
        )
        
        for i, item in enumerate(props.colors):
            if i >= grid_size * grid_size:
                break
            col = grid_flow.column(align=True)
            col.prop(item, "color", text="")


class UPP_PT_ArrangementPanel(Panel):
    """Arrangement panel"""
    bl_label = "Arrange"
    bl_idname = "UPP_PT_arrangement"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='SORTSIZE')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        row = layout.row(align=True)
        row.prop(props, "arrangement_type", text="")
        row.operator("upp.apply_arrangement", text="", icon='CHECKMARK')


class UPP_PT_AdjustmentsPanel(Panel):
    """Adjustments panel"""
    bl_label = "Adjust"
    bl_idname = "UPP_PT_adjustments"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='MODIFIER')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        col = layout.column(align=True)
        col.prop(props, "hue_shift", text="Hue", slider=True, icon='COLORSET_13_VEC')
        col.prop(props, "saturation_mult", text="Saturation", slider=True, icon='PROP_CON')
        col.prop(props, "value_mult", text="Value", slider=True, icon='LIGHT_SUN')
        col.prop(props, "temperature_shift", text="Temp", slider=True, icon='LIGHT_POINT')
        
        layout.operator("upp.apply_adjustments", text="Apply", icon='CHECKMARK')


class UPP_PT_ExportPanel(Panel):
    """Export panel"""
    bl_label = "Export"
    bl_idname = "UPP_PT_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='EXPORT')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        row = layout.row(align=True)
        row.prop(props, "export_format", text="")
        row.prop(props, "export_resolution", text="")
        
        layout.separator()
        
        layout.operator("upp.export_image", text="Export Image", icon='FILE_IMAGE')


class UPP_PT_IntegrationPanel(Panel):
    """Blender Integration panel"""
    bl_label = "Blender"
    bl_idname = "UPP_PT_integration"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='BLENDER')
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("upp.setup_texture_paint", text="Texture Paint", icon='BRUSH_DATA')
        col.operator("upp.create_material", text="Palette Material", icon='MATERIAL')
        col.operator("upp.batch_create_materials", text="Per-Color Materials", icon='NODE_MATERIAL')


class UPP_PT_ClipboardPanel(Panel):
    """Clipboard panel"""
    bl_label = "Clipboard"
    bl_idname = "UPP_PT_clipboard"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='COPYDOWN')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        row = layout.row(align=True)
        row.prop(props, "clipboard_format", text="")
        row.operator("upp.copy_to_clipboard", text="", icon='COPYDOWN')


class UPP_PT_SavedPanel(Panel):
    """Saved Presets panel"""
    bl_label = "Saved"
    bl_idname = "UPP_PT_saved"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='BOOKMARKS')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette
        
        if len(props.saved_presets) > 0:
            for i, preset in enumerate(props.saved_presets):
                row = layout.row(align=True)
                op = row.operator("upp.load_saved_preset", text=preset.name, icon='PRESET')
                op.index = i
                op = row.operator("upp.delete_saved_preset", text="", icon='X')
                op.index = i
        else:
            layout.label(text="No saved palettes", icon='INFO')
        
        layout.separator()
        layout.operator("upp.save_preset", text="Save Current", icon='ADD')


class UPP_PT_WebSyncPanel(Panel):
    """Web Sync panel for connecting to the web app"""
    bl_label = "Web Sync"
    bl_idname = "UPP_PT_websync"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Palette Pro'
    bl_parent_id = "UPP_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon='URL')

    def draw(self, context):
        layout = self.layout
        props = context.scene.ultimate_palette

        # Connection status
        if props.websocket_running:
            row = layout.row()
            row.alert = False
            row.label(text="Server Running", icon='CHECKMARK')

            num_clients = len(_ws_server.clients) if _ws_server else 0
            layout.label(text=f"Clients: {num_clients}", icon='USER')

            layout.operator("upp.stop_websocket", text="Stop Server", icon='CANCEL')
            layout.separator()
            layout.operator("upp.send_to_web", text="Send to Web App", icon='EXPORT')
        else:
            row = layout.row()
            row.label(text="Server Stopped", icon='X')

            layout.prop(props, "websocket_port", text="Port")
            layout.operator("upp.start_websocket", text="Start Server", icon='PLAY')

        # Instructions
        layout.separator()
        box = layout.box()
        box.scale_y = 0.8
        box.label(text="Open web app and click", icon='INFO')
        box.label(text="'Connect' to sync palettes")


# ============================================================================
# REGISTRATION
# ============================================================================

classes = [
    UPP_PaletteColorItem,
    UPP_PalettePreset,
    UPP_Properties,

    UPP_OT_GeneratePalette,
    UPP_OT_LoadPreset,
    UPP_OT_ApplyArrangement,
    UPP_OT_ApplyAdjustments,
    UPP_OT_FlipHorizontal,
    UPP_OT_FlipVertical,
    UPP_OT_RotateLeft,
    UPP_OT_RotateRight,
    UPP_OT_ExportImage,
    UPP_OT_CreateMaterial,
    UPP_OT_SetupTexturePaint,
    UPP_OT_CopyToClipboard,
    UPP_OT_SavePreset,
    UPP_OT_LoadSavedPreset,
    UPP_OT_DeleteSavedPreset,
    UPP_OT_UpdatePreview,
    UPP_OT_InitializePalette,
    UPP_OT_BatchCreateMaterials,
    UPP_OT_StartWebSocket,
    UPP_OT_StopWebSocket,
    UPP_OT_SendToWeb,

    UPP_PT_MainPanel,
    UPP_PT_GeneratePanel,
    UPP_PT_GridPanel,
    UPP_PT_ArrangementPanel,
    UPP_PT_AdjustmentsPanel,
    UPP_PT_ExportPanel,
    UPP_PT_IntegrationPanel,
    UPP_PT_ClipboardPanel,
    UPP_PT_SavedPanel,
    UPP_PT_WebSyncPanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.ultimate_palette = PointerProperty(type=UPP_Properties)
    
    print("[Ultimate Palette Pro] v1.3.0 loaded")


def unregister():
    global _ws_server

    # Stop WebSocket server if running
    if _ws_server:
        _ws_server.stop()
        _ws_server = None

    pm = PreviewManager()
    pm.cleanup()

    del bpy.types.Scene.ultimate_palette

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print("[Ultimate Palette Pro] Unloaded")


if __name__ == "__main__":
    register()