# enemies/specs/specials.py
from settings import *

DATA = {
    "Ghost": {
        "hp": 30, "speed": 2.5, "color": (200, 200, 255), "scale": 0.9, 
        "reward": 30,  # <--- Prime de détection
        "damage": 1, 
        "gimmick": "invisible"
    },
    "Shield": {
        "hp": 40, "speed": 1.8, "color": NEON_BLUE, "shield": 50, "scale": 1.1, 
        "reward": 45,  # <--- Prime de destruction de bouclier
        "damage": 2, 
        "gimmick": "shielded"
    },
    "Tesla": {
        "hp": 120, "speed": 1.5, "color": NEON_PURPLE, "scale": 1.1, 
        "reward": 70,  # <--- Menace prioritaire
        "damage": 2, 
        "gimmick": "stun_tower"
    },
}