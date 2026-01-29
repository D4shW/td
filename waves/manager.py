# waves/manager.py
import pygame
from enemies.base import EnemyBase
from waves.data import WAVE_DATA

class WaveManager:
    def __init__(self, path, sprite_group, enemy_group):
        self.path = path
        self.sprites = sprite_group
        self.enemies = enemy_group
        self.waves = WAVE_DATA
        self.current_wave_index = 0
        self.spawn_queue = []
        self.spawn_timer = 0
        self.active = False
        self.in_cooldown = False
        self.cooldown_timer = 0
        self.cooldown_duration = 3000 # 3 secondes entre les vagues

    def start_next_wave(self):
        if self.current_wave_index < len(self.waves):
            wave_config = self.waves[self.current_wave_index]
            self.spawn_queue = []
            
            for group in wave_config:
                count = group["count"]
                for _ in range(count):
                    spawn_data = group.copy()
                    spawn_data["delay"] = group["interval"]
                    self.spawn_queue.append(spawn_data)
                    
            self.active = True
            self.in_cooldown = False
            self.current_wave_index += 1
            print(f"--- Vague {self.current_wave_index} ---")
        else:
            print("Toutes les vagues sont terminées !")

    def update(self, dt):
        if self.in_cooldown:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0: self.start_next_wave()
            return

        if not self.active: return

        if self.spawn_queue:
            self.spawn_timer += dt
            next_spawn = self.spawn_queue[0]
            
            if self.spawn_timer >= next_spawn["delay"]:
                # Lecture du paramètre "shield" (Vrai ou Faux)
                has_shield = next_spawn.get("shield", False)
                
                # Création de l'ennemi
                e = EnemyBase(next_spawn["enemy"], self.path, shield_active=has_shield)
                
                self.sprites.add(e)
                self.enemies.add(e)
                self.spawn_queue.pop(0)
                self.spawn_timer = 0
                
        elif len(self.enemies) == 0:
            self.active = False
            if self.current_wave_index < len(self.waves):
                self.in_cooldown = True
                self.cooldown_timer = self.cooldown_duration
            else:
                print("Victoire finale !")

    def reset(self):
        self.current_wave_index = 0
        self.spawn_queue = []
        self.spawn_timer = 0
        self.active = False
        self.in_cooldown = False
        self.cooldown_timer = 0