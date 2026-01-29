import pygame
import math
import random
from settings import *
from towers.specs import TOWER_DATA

try:
    from towers.robot import FriendlyRobot
except ImportError:
    pass 

class TowerBase(pygame.sprite.Sprite):
    def __init__(self, name, pos, projectile_manager, robot_group=None, path=None):
        super().__init__()
        self.name = name
        self.stats = TOWER_DATA[name]
        
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(self.stats["color"])
        pygame.draw.rect(self.image, WHITE, (0,0,TILE_SIZE,TILE_SIZE), 2)
        
        self.rect = self.image.get_rect(center=pos)
        
        self.range = self.stats["range"]
        self.cooldown = self.stats["cooldown"]
        self.damage = self.stats["damage"]
        
        self.last_shot = pygame.time.get_ticks()
        self.projectile_manager = projectile_manager
        
        self.level = 1
        self.branch = None
        self.robot_group = robot_group
        self.path = path
        self.stun_timer = 0 
        
        self.branches = {
            "Standard": ("Double Gun", "Ghostbuster"),
            "Sniper": ("Elite Sniper", "Semi Auto"),
            "Gatling": ("Double Uzi", "Modded Gatling"),
            "Cryo": ("Deep Freeze", "Blizzard"),
            "Canon": ("Missile Launcher", "Slime Cannon"),
            "Laser": ("Laser Beam", "Laser Mk2"),
            "Robot Factory": ("Swarm Maker", "Mecha Factory"),
            "Flamethrower": ("Blue Flame", "Incinerator"),
            "Fan": ("Industrial Fan", "Boosted Fan"),
            "Hive": ("Killer Swarm", "Giant Hornets"),
            "Cactus": ("Twin Spikes", "Armor Piercer"),
            "Toaster": ("Burnt Toast", "Sticky Jam"),
            "Butterfly": ("Hypnotic Powder", "Betrayal"),
            "Boomerang": ("Triple Loop", "Round Trip"),
            # --- AJOUT SPY ---
            "Spy": ("Cyanide", "License to Kill")
        }
        
        self.my_minions = pygame.sprite.Group()

    def update(self, enemies, dt):
        if self.stun_timer > 0:
            self.stun_timer -= dt
            return 

        current_time = pygame.time.get_ticks()

        # Invocations
        if self.stats["type"] == "summon":
            for m in list(self.my_minions):
                if not m.alive(): self.my_minions.remove(m)
            if current_time - self.last_shot >= self.cooldown:
                if self.name == "Robot Factory": self.spawn_robot()
                elif self.name == "Hive": self.spawn_bee()
                self.last_shot = current_time
            return 

        # Tirs (On autorise les tours à 0 dégâts comme Fan/Toaster/Papillon)
        if self.damage == 0 and self.name not in ["Fan", "Toaster", "Butterfly"]: return 

        if current_time - self.last_shot >= self.cooldown:
            target = self.find_target(enemies)
            if target:
                self.shoot(target)
                self.last_shot = current_time

    def upgrade(self, choice=1):
        if self.level >= 3: return
        if self.level == 1:
            self.level = 2
            if self.name == "Fan": self.cooldown = 1500 
            elif self.name in ["Robot Factory", "Hive"]: pass
            else:
                self.damage = int(self.damage * 1.5)
                self.range = int(self.range * 1.2)
            pygame.draw.rect(self.image, WHITE, (TILE_SIZE//2 - 4, TILE_SIZE//2 - 4, 8, 8))
            return

        if self.level == 2:
            self.level = 3
            self.branch = choice
            branch_list = self.branches.get(self.name, ("A", "B"))
            idx = 0 if choice == 1 else 1
            branch_name = branch_list[idx]
            self.apply_branch_passives(branch_name)
            
            pygame.draw.rect(self.image, NEON_YELLOW, (0,0,TILE_SIZE,TILE_SIZE), 4)
            color_mark = NEON_GREEN if choice == 1 else NEON_BLUE
            pygame.draw.circle(self.image, color_mark, (TILE_SIZE//2, TILE_SIZE//2), 6)

    def apply_branch_passives(self, branch_name):
        if branch_name == "Semi Auto": self.cooldown = int(self.cooldown / 2)
        elif branch_name == "Modded Gatling": self.cooldown = int(self.cooldown / 3)
        elif branch_name == "Missile Launcher": self.cooldown = int(self.cooldown / 2)
        elif branch_name == "Laser Beam": 
            self.cooldown = 50; self.damage = max(1, int(self.damage / 8))
        elif branch_name == "Blue Flame": self.damage = int(self.damage * 2)
        elif branch_name == "Burnt Toast": self.damage = 60

    def spawn_robot(self):
        if self.robot_group is not None and self.path is not None:
            from towers.robot import FriendlyRobot 
            stats = self.stats["robot_stats"].copy()
            count = 1
            if self.level >= 2: count = 2 
            if self.level == 3:
                b_name = self.branches.get(self.name, ("A", "B"))[self.branch-1 if self.branch else 0]
                if b_name == "Swarm Maker": count = 5; stats["scale"] = 0.6
                elif b_name == "Mecha Factory": count = 1; stats["hp"] *= 3; stats["scale"] = 1.3; stats["color"] = (255, 215, 0)
            if len(self.my_minions) < 10:
                for i in range(count):
                    robot = FriendlyRobot(self.path, stats)
                    if i > 0: robot.rect.x -= 12 * i; robot.rect.y -= 12 * i
                    self.robot_group.add(robot); self.my_minions.add(robot)

    def spawn_bee(self):
        from towers.bee import Bee
        if self.robot_group is None: return
        stats = self.stats["unit_stats"].copy()
        max_units = 5; role = "bee"
        if self.level >= 2: stats["damage"] += 1
        if self.level == 3:
            b_name = self.branches.get(self.name, ("A", "B"))[self.branch-1 if self.branch else 0]
            if b_name == "Killer Swarm": max_units = 8; stats["speed"] = 5.5; stats["attack_speed"] = 250
            elif b_name == "Giant Hornets": role = "hornet"; max_units = 2; stats["hp"] = 80; stats["damage"] = 10
        if len(self.my_minions) < max_units:
            angle = random.uniform(0, 6.28); dist = random.uniform(10, 40)
            bee = Bee(self, stats, role, offset=(math.cos(angle)*dist, math.sin(angle)*dist))
            self.my_minions.add(bee); self.robot_group.add(bee)

    def find_target(self, enemies):
        nearest = None; min_dist = self.range
        for enemy in enemies:
            # On ignore les ennemis transformés (car ils ne sont techniquement plus dans le groupe enemies)
            # Mais par sécurité on garde le check Rage si jamais la logique change
            if enemy.status.get("rage", 0) > 0:
                continue

            dist = pygame.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
            if dist <= self.range:
                can_see = True
                if enemy.invisible and self.name != "Sniper":
                    can_see = False
                    if self.level == 3:
                        b_list = self.branches.get(self.name, ("A","B"))
                        if b_list[0 if self.branch==1 else 1] == "Ghostbuster": can_see = True
                if can_see and dist < min_dist: min_dist = dist; nearest = enemy
        return nearest

    def shoot(self, target):
        ammo_map = {
            "Standard": "normal", "Sniper": "strong", "Canon": "explosive",
            "Cryo": "ice", "Flamethrower": "fire", "Gatling": "normal",
            "Laser": "beam", "Fan": "wind", "Hive": "sting",
            "Cactus": "needle", "Toaster": "toast",
            "Butterfly": "pollen",
            "Boomerang": "wooden_boomerang",
            "Spy": "silencer_bullet" # <--- AJOUT MAPPING
        }
        p_type = ammo_map.get(self.name, "normal")
        extras = {}
        shots = 1
        
        if self.name == "Fan": extras["knockback"] = True

        # --- LOGIQUE BOOMERANG ---
        if self.name == "Boomerang":
            extras["chain_boost"] = 1
            if self.level == 3:
                b_name = self.branches.get(self.name, ("A", "B"))[0 if self.branch == 1 else 1]
                if b_name == "Triple Loop":
                    extras["chain_boost"] = 3
                elif b_name == "Round Trip":
                    p_type = "metal_boomerang"
                    extras["chain_boost"] = 0
                    extras["piercing"] = True
                    extras["return"] = True
                    extras["start_pos"] = self.rect.center

        # --- LOGIQUE SPY ---
        if self.name == "Spy":
            extras["percent_dmg"] = 0.15 # 15% par défaut
            
            if self.level == 3:
                b_name = self.branches.get(self.name, ("A", "B"))[0 if self.branch == 1 else 1]
                
                if b_name == "Cyanide":
                    extras["percent_dmg"] = 0.25 # 25% de dégâts
                
                elif b_name == "License to Kill":
                    extras["execute_threshold"] = 0.30 # Tue si < 30%

        if self.level == 3 and self.name not in ["Boomerang", "Spy"]: 
            branch_list = self.branches.get(self.name, ("A", "B"))
            idx = 0 if self.branch == 1 else 1
            b_name = branch_list[idx]
            
            if b_name == "Double Gun": shots = 2
            elif b_name == "Ghostbuster": extras["hit_invisible"] = True
            elif b_name == "Elite Sniper": extras["break_shield"] = True
            elif b_name == "Double Uzi": shots = 2
            elif b_name == "Deep Freeze": extras["deep_freeze"] = True
            elif b_name == "Blizzard": extras["aoe_slow"] = True
            elif b_name == "Incinerator": extras["incinerate"] = True
            elif b_name == "Laser Mk2": extras["chain_boost"] = 2
            elif b_name == "Blue Flame": extras["blue_flame"] = True
            elif b_name == "Industrial Fan": extras["heavy_slow"] = True
            elif b_name == "Boosted Fan": extras["boss_knockback"] = True
            elif b_name == "Twin Spikes": shots = 2 
            elif b_name == "Armor Piercer": extras["armor_piercing"] = True
            elif b_name == "Burnt Toast": p_type = "burnt_toast"
            elif b_name == "Sticky Jam": p_type = "jam_toast"; extras["jam_slow"] = True
            elif b_name == "Hypnotic Powder": p_type = "hypno_powder"; extras["aoe_confuse"] = True
            elif b_name == "Betrayal": p_type = "rage_dust"; extras["rage_effect"] = True

        for i in range(shots):
            pos = self.rect.center
            if shots > 1:
                off = (i * 6) - 3
                pos = (pos[0] + off, pos[1] + off)
            
            self.projectile_manager.create_projectile(p_type, pos, target, self.damage, extras=extras)