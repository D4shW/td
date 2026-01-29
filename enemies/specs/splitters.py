# enemies/specs/splitters.py
from settings import *

DATA = {
    # Le tout petit (la fin de la chaine)
    "Mini Splitter": {
        "hp": 10, "speed": 3.5, "color": (255, 150, 150), "scale": 0.4, 
        "reward": 2,   # <--- Très peu, c'est du menu fretin
        "damage": 1, 
        "split_into": None
    },
    
    # Le Normal
    "Splitter": {
        "hp": 20, "speed": 3.0, "color": (255, 100, 100), "scale": 0.7, 
        "reward": 5,   # <--- Comme un soldat
        "damage": 1, 
        "split_into": "Mini Splitter"
    },
    
    # Le Super
    "Super Splitter": {
        "hp": 100, "speed": 2.5, "color": (200, 50, 50), "scale": 1.0, 
        "reward": 20, 
        "damage": 2, 
        "split_into": "Splitter"
    },
    
    # Le Mega
    "Mega Splitter": {
        "hp": 200, "speed": 1.8, "color": (150, 0, 0), "scale": 1.4, 
        "reward": 100, # <--- Commence à devenir intéressant
        "damage": 5, 
        "split_into": "Super Splitter"
    },
    
    # LE BOSS 
    "Giga Splitter": {
        "hp": 1000, "speed": 0.8, "color": (80, 0, 0), "scale": 1.8, 
        "reward": 1000, # <--- JACKPOT ! Permet d'acheter une usine de robots ou maxer des tours
        "damage": 20, 
        "split_into": "Mega Splitter"
    },
}