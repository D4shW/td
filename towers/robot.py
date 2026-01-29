import pygame
from settings import *

class FriendlyRobot(pygame.sprite.Sprite):
    def __init__(self, path, stats):
        super().__init__()
        
        # Gestion de l'image (Sprite de l'ennemi ou Carré Robot)
        if "image" in stats:
            self.image = stats["image"]
        else:
            size = int(32 * stats.get("scale", 1.0))
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            color = stats["color"]
            pygame.draw.rect(self.image, color, (0, 0, size, size), border_radius=4)
            pygame.draw.rect(self.image, WHITE, (0, 0, size, size), 2, border_radius=4)
            pygame.draw.rect(self.image, NEON_BLUE, (6, 8, 8, 4))
            pygame.draw.rect(self.image, NEON_BLUE, (size-14, 8, 8, 4))
            
        self.rect = self.image.get_rect()
        
        # Le robot suit le chemin inverse (du point actuel vers le début)
        self.path = path[::-1] 
        self.path_index = 0
        self.rect.center = self.path[0]
        
        # --- MODIFICATION ICI : Récupération PV actuels et PV Max ---
        self.hp = stats["hp"]
        # Si 'max_hp' est fourni (cas du Betrayal), on l'utilise. Sinon on prend 'hp'.
        self.max_hp = stats.get("max_hp", self.hp)
        
        self.speed = stats["speed"]

    def update(self, dt, enemies):
        self.move(dt)
        self.check_collision(enemies)

    def move(self, dt):
        if self.path_index >= len(self.path) - 1:
            self.kill()
            return
        target = pygame.math.Vector2(self.path[self.path_index + 1])
        pos = pygame.math.Vector2(self.rect.center)
        direction = target - pos
        if direction.length() > 0:
            direction = direction.normalize()
            pos += direction * self.speed
            self.rect.center = pos
        if pos.distance_to(target) < 5:
            self.path_index += 1

    def check_collision(self, enemies):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hits:
            # Le robot inflige autant de dégâts qu'il lui reste de PV
            damage_to_enemy = self.hp
            damage_to_robot = enemy.hp
            
            enemy.take_damage(damage_to_enemy, damage_type="robot")
            
            self.hp -= damage_to_robot
            if self.hp <= 0:
                self.kill()
                break