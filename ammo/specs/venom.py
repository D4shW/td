from settings import *

DATA = {
    "sting": {
        "speed": 50, # Instantané
        "color": (0, 0, 0),
        "radius": 1,
        "type": "bullet"
    },
    "venom": { # Pour le Frelon
        "speed": 50,
        "color": (138, 43, 226), # Violet poison
        "radius": 2,
        "type": "bullet",
        "effect": {"name": "poison", "duration": 3000} # Nouveau statut poison
    }
}