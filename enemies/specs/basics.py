# enemies/specs/basics.py
from settings import *

DATA = {
    "Soldier": {
        "hp": 20, "speed": 2.0, "color": RED, "scale": 1.0, 
        "reward": 5,   # <--- Récompense standard
        "damage": 1, 
        "gimmick": None
    },
    "Flash": {
        "hp": 10, "speed": 4.5, "color": NEON_YELLOW, "scale": 0.8, 
        "reward": 10,  # <--- Un peu plus car difficile à attraper
        "damage": 1, 
        "gimmick": "fast"
    },
    "Tank": {
        "hp": 100, "speed": 1.0, "color": (30, 100, 30), "scale": 1.2, 
        "reward": 80,  # <--- Gros gain pour payer des améliorations
        "damage": 3, 
        "gimmick": "armor"
    },
}