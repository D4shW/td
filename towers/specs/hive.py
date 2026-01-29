from settings import *

DATA = {
    "Hive": { 
        "range": 150,         # Zone de patrouille
        "cooldown": 2500,     # Éclosion rapide
        "damage": 0, 
        "cost": 500, 
        "color": (255, 215, 0), # Or / Jaune Miel
        "type": "summon",     
        "unit_stats": {       # Stats de l'Abeille
            "hp": 15,         # Très fragile
            "damage": 2,      # Piqure faible mais rapide
            "speed": 4.0,     # Vol rapide
            "attack_speed": 400,
            "range": 10,      # Contact
            "color": (255, 255, 0) # Jaune
        }
    }
}