import pygame
import math
from ammo.specs import AMMO_DATA
from towers.robot import FriendlyRobot

class Projectile(pygame.sprite.Sprite):
    def __init__(self, p_type, start_pos, target, damage, extras=None):
        super().__init__()
        self.stats = AMMO_DATA.get(p_type, AMMO_DATA.get("normal", AMMO_DATA.get("basic")))
        radius = self.stats.get("radius", 5)
        color = self.stats.get("color", (255, 255, 0))
        
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        
        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(start_pos)
        self.start_pos = pygame.math.Vector2(start_pos) 
        self.target = target
        self.damage = damage
        self.speed = self.stats.get("speed", 10)
        self.extras = extras if extras else {}
        self.p_type = p_type
        self.life_time = self.extras.get("life_time", 3000)
        
        self.hit_list = []      
        self.returning = False  
        self.return_vec = None  

    def update(self, dt):
        self.life_time -= dt
        if self.life_time <= 0:
            self.kill(); return

        if self.extras.get("is_trap"):
            return 

        if self.returning:
            dist = self.pos.distance_to(self.start_pos)
            if dist < 10: 
                self.kill()
                return
            direction = (self.start_pos - self.pos).normalize()
            self.pos += direction * self.speed
            self.rect.center = self.pos
            return 

        if self.target and self.target.alive():
            target_pos = pygame.math.Vector2(self.target.rect.center)
            dist = self.pos.distance_to(target_pos)
            
            if dist <= self.speed and not self.extras.get("piercing") and not self.extras.get("return"):
                self.pos = target_pos; self.rect.center = self.pos
            else:
                direction = (target_pos - self.pos).normalize()
                self.pos += direction * self.speed
                self.rect.center = self.pos
        
        elif (self.extras.get("piercing") or self.extras.get("return")) and self.return_vec:
             self.pos += self.return_vec * self.speed
             self.rect.center = self.pos
        else:
            self.kill()

class ProjectileManager:
    def __init__(self, projectile_group, enemy_group, robot_group):
        self.projectile_group = projectile_group
        self.enemy_group = enemy_group
        self.robot_group = robot_group

    def create_projectile(self, p_type, start_pos, target, damage, extras=None):
        proj = Projectile(p_type, start_pos, target, damage, extras)
        if target and target.alive():
             d = (pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(start_pos))
             if d.length() > 0: proj.return_vec = d.normalize()
        self.projectile_group.add(proj)

    def update(self, dt):
        for proj in list(self.projectile_group):
            
            if proj.extras.get("is_trap"):
                hits = pygame.sprite.spritecollide(proj, self.enemy_group, False)
                for enemy in hits:
                    if enemy.alive():
                        self.hit_target(proj, enemy)
                        proj.kill() 
                        break 
                continue 

            if proj.extras.get("piercing") or proj.extras.get("return"):
                hits = pygame.sprite.spritecollide(proj, self.enemy_group, False)
                for enemy in hits:
                    if enemy not in proj.hit_list:
                        self.hit_target(proj, enemy)
                        proj.hit_list.append(enemy) 
                
                if proj.extras.get("return") and not proj.returning:
                    dist_from_start = proj.pos.distance_to(proj.start_pos)
                    if dist_from_start > 300: 
                        proj.returning = True
                        proj.hit_list = [] 

            else:
                if proj.target and proj.target.alive():
                    dist = proj.pos.distance_to(proj.target.pos)
                    hit_threshold = 25 + proj.stats.get("radius", 5)
                    
                    if dist < hit_threshold:
                        self.hit_target(proj, proj.target)
                        
                        if proj.extras.get("chain_boost", 0) > 0:
                            proj.extras["chain_boost"] -= 1
                            best_dist = 300
                            new_target = None
                            for e in self.enemy_group:
                                if e != proj.target and e.alive():
                                    d = proj.pos.distance_to(e.pos)
                                    if d < best_dist: best_dist = d; new_target = e
                            
                            if new_target: 
                                proj.target = new_target
                            else: 
                                proj.kill() 
                        else:
                            proj.kill() 
                else:
                    proj.kill() 

    def hit_target(self, projectile, target):
        if not target.alive(): return

        dmg = projectile.damage
        if projectile.extras.get("blue_flame"): dmg *= 2
        if projectile.extras.get("hit_invisible") and target.invisible: dmg *= 1.5

        if target.status.get("shatter", 0) > 0:
            dmg += 1

        pct = projectile.extras.get("percent_dmg")
        if pct:
            percent_damage = target.max_hp * pct
            final_percent_dmg = int(percent_damage)
            dmg = max(dmg, final_percent_dmg)

        exec_thresh = projectile.extras.get("execute_threshold")
        if exec_thresh:
            if target.hp < (target.max_hp * exec_thresh):
                dmg = target.hp + target.shield + 1000 

        # --- ORCHID LOGIC (BURST VIA PROJECTILE) ---
        if projectile.extras.get("orchid_burst"):
            bonus_dmg = 80
            if projectile.extras.get("heal_player"):
                 target.reward += 5 
            target.take_damage(bonus_dmg, "magic")

        explode_r = projectile.extras.get("explode_radius")
        cleave_r = projectile.extras.get("cleave_radius")
        trap_explode = projectile.extras.get("trap_explode")
        
        radius = 0
        if explode_r: radius = explode_r
        elif cleave_r: radius = cleave_r
        elif trap_explode: radius = 100
        
        if radius > 0:
            c = pygame.math.Vector2(target.rect.center)
            for e in self.enemy_group:
                if e != target and e.alive():
                    if c.distance_to(e.rect.center) <= radius:
                        if cleave_r and projectile.extras.get("apply_shatter"):
                            e.status["shatter"] = 3000
                        e.take_damage(dmg, "explosive")

        if projectile.extras.get("apply_shatter"):
            target.status["shatter"] = 3000
            
        if projectile.extras.get("combo_stun"):
            if not hasattr(target, "mantis_hits"): target.mantis_hits = 0
            target.mantis_hits += 1
            if target.mantis_hits >= 10:
                target.mantis_hits = 0
                target.status["stun"] = 500
                target.path_index = max(0, target.path_index - 0.2)

        if projectile.extras.get("trap_root"):
            target.status["stun"] = 1500

        if projectile.extras.get("bubble_slow"):
            target.status["slow"] = 2000
        if projectile.extras.get("bubble_confuse"):
            target.status["confuse"] = 3000

        if projectile.extras.get("bubble_knockback"):
            if "boss" not in target.name.lower():
                target.path_index = max(0, target.path_index - 1.0) 

        d_type = "normal"
        if projectile.p_type == "explosive": d_type = "explosive"
        elif projectile.p_type == "robot": d_type = "robot"
        elif projectile.p_type == "fire" or projectile.p_type == "burnt_toast": d_type = "fire"
        if projectile.extras.get("armor_piercing"): d_type = "piercing"

        target.take_damage(dmg, d_type)

        effect = projectile.stats.get("effect")
        if effect:
            ename = effect["name"]
            dur = effect.get("duration", 0)
            if ename == "slow": target.status["slow"] = dur
            elif ename == "burn": target.status["burn"] = dur
            elif ename == "poison": target.status["poison"] = dur
            elif ename == "stun": target.status["stun"] = dur
            elif ename == "charm": target.status["charm"] = dur
            elif ename == "confuse": target.status["confuse"] = dur
            elif ename == "rage": target.status["rage"] = dur

        if projectile.extras.get("incinerate"): target.status["burn"] = 2000
        if projectile.extras.get("deep_freeze"): target.status["frozen"] = 2000
        if projectile.extras.get("jam_slow"): target.status["slow"] = 2000
        
        if projectile.extras.get("aoe_confuse"):
            c = pygame.math.Vector2(projectile.target.rect.center)
            for e in self.enemy_group:
                if c.distance_to(e.rect.center) <= 120:
                    e.status["confuse"] = 4000
        
        if projectile.extras.get("aoe_slow"):
            c = pygame.math.Vector2(projectile.target.rect.center)
            for e in self.enemy_group:
                if c.distance_to(e.rect.center) <= 100: e.status["slow"] = 1000

        if projectile.extras.get("rage_effect"):
            name_lower = target.name.lower()
            is_boss = "boss" in name_lower or "mega" in name_lower or "giga" in name_lower or "construct" in name_lower
            
            if not is_boss:
                stats = {
                    "hp": target.hp,
                    "max_hp": target.max_hp,
                    "speed": target.base_speed,
                    "color": (0,0,0), 
                    "scale": target.stats_data.get("scale", 1.0),
                    "image": target.image.copy() 
                }
                
                robot = FriendlyRobot(target.path, stats)
                robot.rect.center = target.rect.center
                
                path_len = len(target.path)
                robot.path_index = max(0, path_len - 2 - target.path_index)
                
                self.robot_group.add(robot)
                target.kill()
                return

        if projectile.extras.get("knockback"):
            if "boss" not in target.name.lower() or projectile.extras.get("boss_knockback"):
                target.path_index = max(0, target.path_index - 0.5)