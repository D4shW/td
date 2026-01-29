from settings import *

DATA = {
    "Robot Factory": {
        "cost": 450, 
        "range": 0,           # Pas de portée de tir
        "cooldown": 4000,     # Un robot toutes les 4 secondes
        "damage": 0,          # Pas de tir
        "color": (80, 80, 80), 
        "type": "summon",
        # --- NOUVEAU : Stats du Robot ---
        "robot_stats": {
            "hp": 30,        # Assez tanky
            "speed": 1.5,     # Vitesse moyenne
            "color": (200, 200, 200), # Gris clair
            "scale": 0.9
        }
    }
}