# enemies/specs/bosses.py
from settings import *

DATA = {
    # BOSS 1 : CLASSIQUE (Sac à PV)
    "Boss": {
        "hp": 3000, 
        "speed": 0.5,           # Très lent
        "reward": 300, 
        "color": (50, 50, 50),  # Gris foncé
        "scale": 1.6,           # Très gros
        "damage": 10,           # Fait mal aux vies
        "gimmick": "tank_boss"
    },

    # BOSS 2 : TESLA (Stun)
    "MegaTesla": {
        "hp": 1500,             # Moins de vie que le colosse
        "speed": 1.2, 
        "reward": 400, 
        "color": NEON_BLUE,     # Bleu électrique
        "scale": 1.8, 
        "damage": 5, 
        "gimmick": "tesla_boss" # Tag pour la logique
    }
}