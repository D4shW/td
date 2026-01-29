DATA = {
    "Rose": {
        "cost": 250,
        "range": 130,
        "cooldown": 1500,       # Pose un piège toutes les 1.5s
        "damage": 7,           # Dégâts du piège
        "color": (255, 0, 127), # Rose vif
        "type": "shoot"         # On utilise "shoot" mais on modifiera la logique pour poser au sol
    },
    "Orchid": {
        "cost": 650,
        "range": 200,
        "cooldown": 900,
        "damage": 10,           # Dégâts faibles mais cumulatifs
        "color": (218, 112, 214), # Orchidée (Orchid Color)
        "type": "shoot"
    },
    "Shampoo": {
        "cost": 300,
        "range": 140,
        "cooldown": 2000,        # Tire très vite (bulles)
        "damage": 0,            # Aucun dégâts
        "color": (255, 192, 203), # Rose pâle (Bouteille de shampoing)
        "type": "shoot"
    }
}