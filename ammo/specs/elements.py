from settings import NEON_BLUE, NEON_ORANGE, WHITE
DATA = {
    "ice": {"speed": 10, "color": NEON_BLUE, "radius": 6, "type": "debuff", "effect": {"name": "slow", "duration": 2000}},
    "fire": {"speed": 8, "color": NEON_ORANGE, "radius": 7, "type": "debuff", "effect": {"name": "burn", "duration": 3000}},
    "explosive": {"speed": 9, "color": WHITE, "radius": 8, "type": "aoe", "effect": {"name": "explode", "radius": 100}}
}