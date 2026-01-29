DATA = {
    "magic_bolt": {
        "speed": 10,
        "color": (180, 0, 255), # Violet clair
        "radius": 5,
        "type": "bullet"
    },
    "fireball": {
        "speed": 12,            # Un peu plus lent
        "color": (255, 69, 0),  # Rouge Orangé
        "radius": 10,           # Gros projectile
        "type": "bullet"        # L'effet d'explosion est géré dans le code
    },
    "iceball": {
        "speed": 12,
        "color": (0, 255, 255), # Cyan
        "radius": 8,
        "type": "bullet"        # L'effet de zone est géré via aoe_slow
    }
}