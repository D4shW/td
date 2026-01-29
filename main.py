import pygame
import sys
from settings import *
from ui import MainMenu, DeckBuilder, GameUI, EndGameMenu
from towers.base import TowerBase
from towers.specs import TOWER_DATA
from ammo.manager import ProjectileManager
from waves.manager import WaveManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense Ultimate")
        self.clock = pygame.time.Clock()
        self.state = 0 
        self.paused = False
        
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.proj_manager = ProjectileManager(self.projectiles, self.enemies, self.robots)
        
        self.path_points = [
            (0, 150), (200, 150), (200, 600), (500, 600), 
            (500, 150), (800, 150), (800, 600), (1100, 600), 
            (1100, 350), (1280, 350)
        ]
        self.path_thickness = 60
        self.path_rects = self.generate_path_rects()
        
        self.waves = WaveManager(self.path_points, self.sprites, self.enemies)
        self.wave_was_active = False 
        
        self.menu_ui = MainMenu(self.goto_game, self.goto_deck)
        self.deck_ui = DeckBuilder(self.on_deck_validated)
        self.end_ui = EndGameMenu(self.goto_menu) 
        self.game_ui = None
        
        self.deck = []
        self.money = 600
        self.lives = 20
        self.selected_tower_idx = None
        self.inspected_tower = None

    def generate_path_rects(self):
        rects = []
        half = self.path_thickness // 2
        for i in range(len(self.path_points) - 1):
            p1, p2 = self.path_points[i], self.path_points[i+1]
            x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            if y1 == y2:
                r = pygame.Rect(x1 - half, y1 - half, (x2 - x1) + self.path_thickness, self.path_thickness)
            else:
                r = pygame.Rect(x1 - half, y1 - half, self.path_thickness, (y2 - y1) + self.path_thickness)
            rects.append(r)
        return rects

    def goto_deck(self): self.state = 1
    def on_deck_validated(self, deck): self.deck = deck; self.state = 0
    
    def goto_game(self):
        self.reset_game_stats()
        # --- DECK PAR DÉFAUT AVEC LE SPY ---
        if not self.deck: self.deck = ["Standard", "Spy", "Toaster", "Butterfly", "Canon", "Gatling"]
        self.game_ui = GameUI(self.deck, self.money, self.lives)
        self.state = 2; self.paused = False
        self.selected_tower_idx = None; self.inspected_tower = None

    def goto_menu(self): self.state = 0 

    def reset_game_stats(self):
        self.money = 600; self.lives = 20
        self.enemies.empty(); self.sprites.empty(); self.towers.empty()
        self.robots.empty(); self.projectiles.empty()
        self.waves.reset(); self.wave_was_active = False

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if self.state == 0: self.menu_ui.update(event)
            elif self.state == 1: self.deck_ui.update(event)
            elif self.state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: self.handle_game_click(event.pos)
                    elif event.button == 3: self.handle_right_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p: self.paused = not self.paused
            elif self.state == 3 or self.state == 4: self.end_ui.update(event)

    def handle_right_click(self, pos):
        if self.selected_tower_idx is not None: self.selected_tower_idx = None; return 
        for t in self.towers:
            if t.rect.collidepoint(pos):
                self.money += t.stats["cost"] // 2
                if self.inspected_tower == t: self.inspected_tower = None
                t.kill(); return 

    def handle_game_click(self, pos):
        mx, my = pos
        if self.game_ui:
            if self.game_ui.btn_pause.rect.collidepoint(mx, my): self.paused = not self.paused; return
            for i, btn in enumerate(self.game_ui.buttons):
                if btn.rect.collidepoint(mx, my):
                    self.selected_tower_idx = i; self.inspected_tower = None; return
        
        if self.inspected_tower:
             panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 120, 400, 100)
             close_rect = pygame.Rect(panel_rect.right - 30, panel_rect.y, 30, 30)
             if close_rect.collidepoint(mx, my): self.inspected_tower = None; return

             if self.inspected_tower.level == 1:
                 upgrade_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 55, 360, 30)
                 if upgrade_rect.collidepoint(mx, my):
                     cost = int(self.inspected_tower.stats["cost"] * 1.5)
                     if self.money >= cost: self.money -= cost; self.inspected_tower.upgrade()
                     return
             elif self.inspected_tower.level == 2:
                 cost = self.inspected_tower.stats["cost"] + 700
                 btn1_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 50, 170, 40)
                 if btn1_rect.collidepoint(mx, my):
                     if self.money >= cost: self.money -= cost; self.inspected_tower.upgrade(1)
                     return
                 btn2_rect = pygame.Rect(panel_rect.x + 210, panel_rect.y + 50, 170, 40)
                 if btn2_rect.collidepoint(mx, my):
                     if self.money >= cost: self.money -= cost; self.inspected_tower.upgrade(2)
                     return

        for t in self.towers:
            if t.rect.collidepoint(mx, my): self.inspected_tower = t; self.selected_tower_idx = None; return
        
        if self.selected_tower_idx is not None and not self.inspected_tower: self.place_tower(pos)

    def check_valid_placement(self, rect):
        if rect.collidelist(self.path_rects) != -1: return False
        for t in self.towers:
            if t.rect.colliderect(rect): return False
        return True

    def place_tower(self, pos):
        if pos[1] < 80 or len(self.towers) >= 20: return
        test_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE); test_rect.center = pos
        if not self.check_valid_placement(test_rect): return
        
        t_name = self.deck[self.selected_tower_idx]
        cost = TOWER_DATA[t_name]["cost"]
        if self.money >= cost:
            self.money -= cost
            t = TowerBase(t_name, pos, self.proj_manager, self.robots, self.path_points)
            self.towers.add(t)
            self.selected_tower_idx = None
            if self.waves.current_wave_index == 0 and not self.waves.active: self.waves.start_next_wave()

    def update(self, dt):
        if self.state == 2: 
            if self.paused: return
            self.waves.update(dt)
            self.proj_manager.update(dt)
            self.projectiles.update(dt)
            
            for enemy in list(self.enemies):
                if enemy.stats_data.get("gimmick") == "tesla_boss":
                    if enemy.tesla_tick >= 3000:
                        enemy.tesla_tick = 0
                        for t in self.towers:
                            if pygame.math.Vector2(enemy.rect.center).distance_to(t.rect.center) <= 250: t.stun_timer = 1000 

                if enemy.hp <= 0:
                    self.money += enemy.reward
                    if enemy.stats_data.get("gimmick") == "tesla_boss":
                        for t in self.towers: t.stun_timer = 5000 
                    elif enemy.stats_data.get("gimmick") == "stun_tower":
                        for t in self.towers:
                            if pygame.math.Vector2(enemy.rect.center).distance_to(t.rect.center) <= 200: t.stun_timer = 3000
                    enemy.spawn_children(); enemy.kill()
                
                elif enemy.reached_end:
                    self.lives -= enemy.player_damage; enemy.kill()
            
            if self.wave_was_active and not self.waves.active: self.money += 100 + (self.waves.current_wave_index * 20)
            self.wave_was_active = self.waves.active
            
            for t in self.towers: t.update(self.enemies, dt)
            self.robots.update(dt, self.enemies)
            
            self.sprites.update(dt) 

            if self.lives <= 0: self.state = 4; self.end_ui.set_mode("lose")
            if (self.waves.current_wave_index >= len(self.waves.waves) 
                and not self.waves.active and len(self.enemies) == 0 and not self.waves.in_cooldown):
                self.state = 3; self.end_ui.set_mode("win")

    def draw(self):
        if self.state == 0: self.menu_ui.draw(self.screen)
        elif self.state == 1: self.deck_ui.draw(self.screen)
        elif self.state == 2: self.draw_game()
        elif self.state == 3 or self.state == 4: self.draw_game(); self.end_ui.draw(self.screen)
        pygame.display.flip()

    def draw_game(self):
        self.screen.fill(BLACK)
        pygame.draw.lines(self.screen, GRAY_PATH, False, self.path_points, self.path_thickness)
        
        if self.inspected_tower: self.draw_range_circle(self.inspected_tower.rect.center, self.inspected_tower.range)
        self.towers.draw(self.screen)
        
        font_stun = pygame.font.SysFont("Arial", 24, bold=True)
        for t in self.towers:
            if t.stun_timer > 0:
                txt = font_stun.render("ZZZ", True, NEON_YELLOW)
                self.screen.blit(txt, (t.rect.centerx - 15, t.rect.top - 25))

        self.robots.draw(self.screen)
        for r in self.robots:
            pygame.draw.rect(self.screen, (0, 0, 100), (r.rect.x, r.rect.top-6, r.rect.width, 4))
            ratio = r.hp / r.max_hp
            pygame.draw.rect(self.screen, NEON_BLUE, (r.rect.x, r.rect.top-6, r.rect.width * ratio, 4))
        
        self.sprites.draw(self.screen); self.projectiles.draw(self.screen)
        for e in self.enemies: e.draw_health_bar(self.screen)
        
        if self.paused:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(100); s.fill((0,0,0)); self.screen.blit(s, (0,0))
            txt = pygame.font.SysFont("Arial", 80, bold=True).render("PAUSE", True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        if self.game_ui:
            wd = self.waves.current_wave_index
            if wd == 0: wd = "Prêt"
            if self.waves.in_cooldown: wd = f"{int(self.waves.cooldown_timer/1000)+1}s"
            if wd == len(self.waves.waves) and not self.waves.active: wd = "FIN"
            self.game_ui.draw(self.screen, self.money, self.lives, wd, self.selected_tower_idx, len(self.towers), self.paused)
        
        mx, my = pygame.mouse.get_pos()
        if not self.inspected_tower and self.state == 2:
            for t in self.towers:
                if t.rect.collidepoint(mx, my):
                    self.draw_range_circle(t.rect.center, t.range)
                    pygame.draw.rect(self.screen, WHITE, t.rect, 3)
        
        if my > 80 and not self.inspected_tower and self.selected_tower_idx is not None and self.state == 2:
            self.draw_preview(mx, my)
        
        if self.inspected_tower and self.state == 2: self.game_ui.draw_upgrade_panel(self.screen, self.inspected_tower)

    def draw_range_circle(self, center, radius, color=(255, 255, 255, 50)):
        if radius <= 0: return
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (radius, radius), radius)
        pygame.draw.circle(s, (color[0], color[1], color[2], 255), (radius, radius), radius, 2)
        self.screen.blit(s, (center[0]-radius, center[1]-radius))

    def draw_preview(self, mx, my):
        if self.selected_tower_idx is None: return
        t_name = self.deck[self.selected_tower_idx]
        data = TOWER_DATA[t_name]
        rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE); rect.center = (mx, my)
        valid = self.check_valid_placement(rect)
        col = data["color"] if valid else RED
        rc = (255, 255, 255, 30) if valid else (255, 0, 0, 30)
        self.draw_range_circle((mx, my), data["range"], rc)
        s = pygame.Surface((TILE_SIZE, TILE_SIZE)); s.set_alpha(150); s.fill(col); self.screen.blit(s, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)

if __name__ == "__main__": Game().run()