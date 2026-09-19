"""Render an icon PNG as ASCII art (this box has no image-input model).

Usage:  python tools\\show_icon_ascii.py [png] [width]
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

pygame.init()
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "phone-pwa", "icons", "icon-512.png")
width = int(sys.argv[2]) if len(sys.argv) > 2 else 48
img = pygame.image.load(path)
h = max(1, round(img.get_height() * width / img.get_width()))
small = pygame.transform.smoothscale(img, (width, h))
chars = " .:-=+*#%@"
for y in range(h):
    row = []
    for x in range(width):
        c = small.get_at((x, y))[:3]
        row.append(chars[min(9, sum(c) // 26)])
    print("".join(row))
