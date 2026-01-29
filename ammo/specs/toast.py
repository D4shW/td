DATA = {
    "toast": {
        "speed": 15,
        "color": (210, 180, 140), # Couleur pain
        "radius": 6,              # Carré en théorie, mais rond ici
        "type": "bullet",
        "effect": {"name": "stun", "duration": 800} # 0.8s de stun
    },
    "burnt_toast": {
        "speed": 18,
        "color": (50, 20, 0),     # Noir brûlé
        "radius": 7,
        "type": "bullet",
        "effect": {"name": "burn", "duration": 3000} # Feu
    },
    "jam_toast": {
        "speed": 12,
        "color": (200, 0, 0),     # Rouge confiture
        "radius": 8,
        "type": "bullet",
        "effect": None # Géré par 'extras' pour la zone de glue
    }
}