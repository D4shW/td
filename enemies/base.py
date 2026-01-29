import pygame
from settings import *
from enemies.specs import ENEMY_DATA

class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, name, path, shield_active=False):
        super().__init__()
        self.name = name
        self.stats_data = ENEMY_DATA.get(name, ENEMY_DATA["Soldier"])
        
        size = int(32 * self.stats_data.get("scale", 1.0))
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = self.stats_data["color"]
        radius = size // 2
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        pygame.draw.circle(self.image, WHITE, (radius, radius), 4)

        self.rect = self.image.get_rect()
        self.path = path
        self.path_index = 0
        
        if path: 
            self.rect.center = self.path[0]
            self.pos = pygame.math.Vector2(self.path[0]) 
        
        self.max_hp = self.stats_data["hp"]
        self.hp = self.max_hp
        self.base_speed = self.stats_data["speed"]
        self.current_speed = self.base_speed
        self.reward = self.stats_data["reward"]
        self.player_damage = self.stats_data.get("damage", 1)
        
        self.invisible = (self.stats_data.get("gimmick") == "invisible")
        base_shield = self.stats_data.get("shield", 0)
        self.max_shield = max(base_shield, 50) if shield_active or self.stats_data.get("gimmick") == "regen_shield" else base_shield
        self.shield = self.max_shield
        self.last_damage_time = pygame.time.get_ticks()

        self.status = {
            "frozen": 0, "slow": 0, 
            "burn": 0, "burn_tick": 0,
            "poison": 0, "poison_tick": 0,
            "stun": 0,
            "vulnerable": 0,
            "charm": 0, "confuse": 0, 
            "rage": 0
        }
        
        self.reached_end = False 
        self.processed_death = False
        self.tesla_tick = 0 

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        
        if self.stats_data.get("gimmick") == "regen_shield":
            if current_time - self.last_damage_time > 3000 and self.shield < self.max_shield:
                regen_rate = 0.05 
                self.shield = min(self.max_shield, self.shield + regen_rate * dt)

        self.handle_status(dt)
        self.move(dt)
        
        if self.stats_data.get("gimmick") == "tesla_boss":
            self.tesla_tick += dt

    def handle_status(self, dt):
        is_controlled = False
        speed_mod = 1.0
        
        if self.stats_data.get("gimmick") == "berserk":
            ratio = self.hp / self.max_hp
            multiplier = max(1.0, 2.25 - 1.25 * ratio)
            speed_mod *= multiplier

        # Plus besoin de logique complexe pour Rage, l'ennemi est tué
        if self.status["confuse"] > 0:
            self.status["confuse"] -= dt
            self.current_speed = 0
            is_controlled = True
        
        elif self.status["charm"] > 0:
            self.status["charm"] -= dt
            self.current_speed = self.base_speed * speed_mod * -0.5
            is_controlled = True 
        
        elif self.status["stun"] > 0:
            self.status["stun"] -= dt
            self.current_speed = 0
        elif self.status["frozen"] > 0:
            self.status["frozen"] -= dt
            self.current_speed = 0
        elif self.status["slow"] > 0:
            self.status["slow"] -= dt
            self.current_speed = self.base_speed * speed_mod * 0.5
        else:
            if not is_controlled:
                self.current_speed = self.base_speed * speed_mod

        if self.status["vulnerable"] > 0: self.status["vulnerable"] -= dt
        if self.status["burn"] > 0:
            self.status["burn"] -= dt
            self.status["burn_tick"] += dt
            if self.status["burn_tick"] >= 1000:
                self.take_damage(self.max_hp * 0.05, damage_type="fire")
                self.status["burn_tick"] = 0
        if self.status["poison"] > 0:
            self.status["poison"] -= dt
            self.status["poison_tick"] += dt
            if self.status["poison_tick"] >= 500:
                self.take_damage(5, damage_type="poison")
                self.status["poison_tick"] = 0

    def draw_health_bar(self, surface):
        if self.hp < self.max_hp or self.shield > 0:
            bar_w = 40
            x = self.rect.centerx - 20
            y = self.rect.top - 10
            pygame.draw.rect(surface, RED, (x, y, bar_w, 4))
            ratio = max(0, self.hp / self.max_hp)
            pygame.draw.rect(surface, NEON_GREEN, (x, y, bar_w * ratio, 4))
            if self.shield > 0:
                display_max = self.max_shield if self.max_shield > 0 else 50
                shield_ratio = min(1.0, self.shield / display_max)
                pygame.draw.rect(surface, NEON_BLUE, (x - 2, y - 2, (bar_w + 4) * shield_ratio, 8), 2)
        
        if self.status["poison"] > 0:
            pygame.draw.circle(surface, (0, 255, 0), (self.rect.right, self.rect.top), 4)
        if self.status["charm"] > 0: 
            pygame.draw.circle(surface, (255, 105, 180), (self.rect.centerx, self.rect.top - 15), 5)

    def move(self, dt):
        if self.current_speed == 0 and self.status["charm"] <= 0: return
        if self.status["charm"] > 0:
            target_idx = int(self.path_index)
            if target_idx < 0: target_idx = 0
            target = pygame.math.Vector2(self.path[target_idx])
            direction = target - self.pos
            back_speed = self.base_speed * 0.8
            if direction.length() > 0:
                direction = direction.normalize()
                self.pos += direction * back_speed 
                self.rect.center = self.pos
            if self.pos.distance_to(target) < 10:
                self.path_index = max(0, self.path_index - 1)
        else:
            if self.path_index >= len(self.path) - 1: return
            target = pygame.math.Vector2(self.path[self.path_index + 1])
            direction = target - self.pos 
            if direction.length() > 0:
                direction = direction.normalize()
                self.pos += direction * self.current_speed 
                self.rect.center = self.pos   
            if self.pos.distance_to(target) < 10:
                self.path_index += 1
                if self.path_index >= len(self.path) - 1:
                    self.reached_end = True 

    def take_damage(self, amount, damage_type="normal"):
        self.last_damage_time = pygame.time.get_ticks()
        damage_to_hp = amount
        if self.shield > 0:
            damage_on_shield = amount
            if damage_type == "explosive" or damage_type == "robot": damage_on_shield = amount * 2
            if damage_type == "piercing": damage_on_shield = amount * 3
            self.shield -= damage_on_shield
            if self.shield > 0: return 0
            else:
                damage_to_hp = abs(self.shield)
                self.shield = 0
        if self.status["vulnerable"] > 0: damage_to_hp *= 1.5
        self.hp -= damage_to_hp
        return damage_to_hp

    def spawn_children(self):
        if self.processed_death: return
        self.processed_death = True
        child_name = self.stats_data.get("split_into")
        if child_name:
            for _ in range(2):
                child = EnemyBase(child_name, self.path, shield_active=False)
                child.rect.center = self.rect.center
                child.pos = pygame.math.Vector2(self.rect.center)
                child.path_index = self.path_index
                for group in self.groups(): group.add(child)