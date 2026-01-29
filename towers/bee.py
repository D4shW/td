import pygame, random, math
from settings import *

class Bee(pygame.sprite.Sprite):
    def __init__(self, parent_tower, stats, role="bee", offset=(0,0)):
        super().__init__()
        self.parent = parent_tower
        self.stats = stats
        self.role = role # "bee" ou "hornet"
        
        # Position de la ruche (Home)
        self.home_pos = pygame.math.Vector2(parent_tower.rect.center) + pygame.math.Vector2(offset)
        
        # Visuel : Ovale Jaune avec rayures Noires
        size = 14 if role == "bee" else 20
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = stats["color"]
        
        # Corps
        pygame.draw.ellipse(self.image, color, (0, 0, size, size))
        # Rayures
        pygame.draw.line(self.image, BLACK, (size//2, 0), (size//2, size), 2)
        pygame.draw.line(self.image, BLACK, (size//4, 2), (size//4, size-2), 2)
        pygame.draw.line(self.image, BLACK, (size*3//4, 2), (size*3//4, size-2), 2)
        
        # Ailes (petits cercles blancs translucides sur le côté)
        pygame.draw.circle(self.image, (255,255,255, 150), (size, size//2), 4)
        pygame.draw.circle(self.image, (255,255,255, 150), (0, size//2), 4)

        self.rect = self.image.get_rect(center=self.home_pos)
        self.pos = pygame.math.Vector2(self.home_pos)
        
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.last_attack = 0
        self.target = None
        
        # Vol erratique (bzzzz)
        self.wobble_timer = 0
        self.state = "IDLE"

    def update(self, dt, enemies):
        if self.hp <= 0:
            self.kill()
            return

        current_time = pygame.time.get_ticks()
        
        # 1. CIBLAGE
        if not self.target or not self.target.alive():
            self.target = self.find_flower(enemies)
            if not self.target:
                self.state = "RETURN"
        else:
            dist = pygame.math.Vector2(self.target.rect.center).distance_to(self.parent.rect.center)
            if dist > self.parent.range * 1.3: # Elles poursuivent un peu plus loin
                self.target = None
                self.state = "RETURN"
            else:
                self.state = "ATTACK"

        # 2. MOUVEMENT
        move_target = self.pos
        
        if self.state == "RETURN":
            move_target = self.home_pos
            if self.pos.distance_to(self.home_pos) < 10:
                self.state = "IDLE"
        
        elif self.state == "ATTACK":
            if self.target:
                move_target = pygame.math.Vector2(self.target.rect.center)
                if self.pos.distance_to(move_target) < self.stats["range"]:
                    self.sting(self.target)
        
        # Déplacement avec vibration (Bzzz)
        if self.pos.distance_to(move_target) > 5:
            direction = (move_target - self.pos).normalize()
            
            # Vibration aléatoire
            self.wobble_timer += dt
            if self.wobble_timer > 50: # Change de direction très vite
                wiggle = random.randint(-40, 40)
                direction.rotate_ip(wiggle)
                self.wobble_timer = 0
            
            self.pos += direction * self.speed
            self.rect.center = self.pos

    def find_flower(self, enemies):
        # Cherche l'ennemi le plus proche de la RUCHE
        best = None
        min_d = self.parent.range
        center = pygame.math.Vector2(self.parent.rect.center)
        for e in enemies:
            d = center.distance_to(e.rect.center)
            if d <= self.parent.range and d < min_d:
                min_d = d
                best = e
        return best

    def sting(self, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.stats["attack_speed"]:
            
            ammo = "sting"
            if self.role == "hornet":
                ammo = "venom"
                
            self.parent.projectile_manager.create_projectile(
                ammo, self.rect.center, target, self.damage
            )
            self.last_attack = current_time