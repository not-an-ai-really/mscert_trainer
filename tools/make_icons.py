r"""Draw the MS-Cert Trainer PWA icons (512 + 192 PNG) with pygame.

Usage:  python tools\make_icons.py

Original art, generated in code (no downloaded assets). Design: deep-navy
rounded tile, big white "MS" monogram, teal medical cross accent. The
artwork stays inside the central ~80% (maskable safe zone).
"""

import os

import pygame

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "phone-pwa", "icons")

NAVY = (11, 16, 38)
NAVY_EDGE = (28, 38, 84)
TEAL = (45, 212, 191)
WHITE = (240, 244, 255)


def draw(size):
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    r = int(size * 0.19)
    pygame.draw.rect(s, NAVY, (0, 0, size, size),
                     border_radius=r)
    pad = int(size * 0.045)
    pygame.draw.rect(s, NAVY_EDGE, (pad, pad, size - 2 * pad,
                                    size - 2 * pad),
                     width=max(2, size // 64),
                     border_radius=r - pad)
    # white "MS" monogram, centered slightly left
    font = pygame.font.SysFont("segoeui,arial", int(size * 0.30), bold=True)
    mono = font.render("MS", True, WHITE)
    # teal cross accent, upper right of the monogram block
    cx = int(size * 0.665)
    cy = int(size * 0.345)
    arm = int(size * 0.105)
    bar = int(size * 0.042)
    pygame.draw.rect(s, TEAL, (cx - arm, cy - bar, 2 * arm, 2 * bar),
                     border_radius=bar // 2)
    pygame.draw.rect(s, TEAL, (cx - bar, cy - arm, 2 * bar, 2 * arm),
                     border_radius=bar // 2)
    rect = mono.get_rect(center=(int(size * 0.46), int(size * 0.585)))
    s.blit(mono, rect)
    # thin teal baseline under the monogram
    pygame.draw.rect(s, TEAL,
                     (int(size * 0.24), int(size * 0.735),
                      int(size * 0.52), max(2, size // 128)),
                     border_radius=size // 256)
    return s


def main():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    os.makedirs(OUT_DIR, exist_ok=True)
    big = draw(512)
    pygame.image.save(big, os.path.join(OUT_DIR, "icon-512.png"))
    small = pygame.transform.smoothscale(big, (192, 192))
    pygame.image.save(small, os.path.join(OUT_DIR, "icon-192.png"))
    print("icons written to", OUT_DIR)
    pygame.quit()


if __name__ == "__main__":
    main()
