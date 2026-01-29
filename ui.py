import pygame
from settings import *
from towers.specs import TOWER_DATA

GRAY = (100, 100, 100)
GRAY_DARK = (50, 50, 50)
BLUE_PANEL = (20, 30, 50)

# ... (Le dictionnaire TOWER_DESCRIPTIONS reste inchangé) ...
TOWER_DESCRIPTIONS = {
    "Standard": {
        "group": "Classique",
        "gimmick": "Aucune. Tour polyvalente de base.",
        "lvl2": "Augmente Dégâts et Portée.",
        "lvl3_a": "Double Gun : Tire deux balles à la fois.",
        "lvl3_b": "Ghostbuster : Peut voir et toucher les ennemis Invisibles."
    },
    "Sniper": {
        "group": "Militaire",
        "gimmick": "Portée immense et dégâts élevés, mais lent.",
        "lvl2": "Augmente Dégâts et Portée critique.",
        "lvl3_a": "Elite Sniper : Brise les Boucliers (Bleu) en un coup.",
        "lvl3_b": "Semi Auto : Divise le temps de recharge par 2."
    },
    "Gatling": {
        "group": "Militaire",
        "gimmick": "Tire très vite, dégâts faibles par balle.",
        "lvl2": "Augmente la vitesse de tir.",
        "lvl3_a": "Double Uzi : Tire 2 projectiles par coup (Mitraille).",
        "lvl3_b": "Modded Gatling : Vitesse de tir extrême (x3)."
    },
    "Canon": {
        "group": "Militaire",
        "gimmick": "Dégâts de zone (Explosif).",
        "lvl2": "Augmente la zone d'explosion.",
        "lvl3_a": "Missile Launcher : Projectiles plus rapides et plus gros.",
        "lvl3_b": "Slime Cannon : Laisse une zone qui ralentit les ennemis."
    },
    "Cryo": {
        "group": "Machine",
        "gimmick": "Ralentit les ennemis (Glace).",
        "lvl2": "Augmente la durée du ralentissement.",
        "lvl3_a": "Deep Freeze : Congèle (Stun) les ennemis sur place.",
        "lvl3_b": "Blizzard : Ralentit tous les ennemis dans une zone autour."
    },
    "Flamethrower": {
        "group": "Machine",
        "gimmick": "Brûle les ennemis (Dégâts sur la durée).",
        "lvl2": "Augmente la durée de brûlure.",
        "lvl3_a": "Blue Flame : Dégâts de feu doublés.",
        "lvl3_b": "Incinerator : Brûlure permanente tant qu'ils sont visés."
    },
    "Laser": {
        "group": "Machine",
        "gimmick": "Tir instantané (Rayon).",
        "lvl2": "Augmente les dégâts.",
        "lvl3_a": "Laser Beam : Tir continu très rapide (faibles dégâts mais constants).",
        "lvl3_b": "Laser Mk2 : Le rayon rebondit sur 2 ennemis supplémentaires."
    },
    "Fan": {
        "group": "Machine",
        "gimmick": "Repousse les ennemis (Knockback). 0 Dégâts.",
        "lvl2": "Souffle plus fort (meilleur recul).",
        "lvl3_a": "Industrial Fan : Ralentissement lourd permanent.",
        "lvl3_b": "Boosted Fan : Peut repousser les Boss."
    },
    "Hive": {
        "group": "Insecte",
        "gimmick": "Invoque des abeilles qui attaquent librement.",
        "lvl2": "Invoque plus d'abeilles.",
        "lvl3_a": "Killer Swarm : 8 Abeilles très rapides.",
        "lvl3_b": "Giant Hornets : 2 Frelons robustes qui font mal."
    },
    "Robot Factory": {
        "group": "Machine",
        "gimmick": "Pose des robots bloqueurs sur la route.",
        "lvl2": "Robots plus résistants.",
        "lvl3_a": "Swarm Maker : 5 petits robots faibles (masse).",
        "lvl3_b": "Mecha Factory : 1 Robot Tank géant (doré)."
    },
    "Cactus": {
        "group": "Plante",
        "gimmick": "Tire des épines.",
        "lvl2": "Meilleure cadence.",
        "lvl3_a": "Twin Spikes : Tire 2 épines à la fois.",
        "lvl3_b": "Armor Piercer : Ignore l'armure/bouclier des ennemis."
    },
    "Toaster": {
        "group": "Absurde",
        "gimmick": "Lance des toasts ! (Projectiles physiques).",
        "lvl2": "Toasts plus croustillants (Dégâts up).",
        "lvl3_a": "Burnt Toast : Toasts enflammés (Dégâts de feu élevés).",
        "lvl3_b": "Sticky Jam : Toasts à la confiture (Ralentit fort)."
    },
    "Butterfly": {
        "group": "Insecte",
        "gimmick": "Contrôle mental. 0 Dégâts.",
        "lvl2": "Meilleure portée de charme.",
        "lvl3_a": "Hypnotic Powder : Confus (Stop) tous les ennemis en zone.",
        "lvl3_b": "Betrayal : Rage (Les ennemis s'attaquent entre eux)."
    },
    "Boomerang": {
        "group": "Classique",
        "gimmick": "Ricoche sur un 2ème ennemi.",
        "lvl2": "Meilleure portée de rebond.",
        "lvl3_a": "Triple Loop : Ricoche sur 3 ennemis consécutifs.",
        "lvl3_b": "Round Trip : Traverse tout et revient (Aller-Retour)."
    },
    "Spy": {
        "group": "Classique",
        "gimmick": "Balles Anti-Tank : Inflige 15% des PV MAX de l'ennemi par tir.",
        "lvl2": "Rechargement plus rapide.",
        "lvl3_a": "Cyanide : La balle inflige 25% des PV MAX.",
        "lvl3_b": "License to Kill : Tue instantanément les ennemis sous 30% de vie."
    }
}

class Button:
    def __init__(self, text, x, y, w, h, color, text_color=BLACK, callback=None, outline=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.callback = callback
        self.outline = outline 
        self.selected = False
        self.hover = False
        self.tower_name = ""
        self.icon_color = WHITE
        self.font_size = 20

    def draw(self, surface):
        col = self.color
        if self.selected:
            col = NEON_YELLOW 
        elif self.hover:
            pass
            
        pygame.draw.rect(surface, col, self.rect)
        if self.outline:
            pygame.draw.rect(surface, WHITE, self.rect, 2)
            
        font = pygame.font.SysFont("Arial", self.font_size, bold=True)
        txt = font.render(self.text, True, self.text_color)
        rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback(self)

class MainMenu:
    def __init__(self, on_play, on_deck):
        self.on_play = on_play
        self.on_deck = on_deck
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.btn_play = Button("JOUER", cx - 100, cy - 60, 200, 50, NEON_GREEN, BLACK, self.go_play)
        self.btn_deck = Button("DECK", cx - 100, cy + 10, 200, 50, NEON_BLUE, BLACK, self.go_deck)
        self.btn_full = Button("PLEIN ÉCRAN", cx - 100, cy + 80, 200, 50, NEON_PURPLE, BLACK, None)
        self.buttons = [self.btn_play, self.btn_deck, self.btn_full]

    def go_play(self, btn): self.on_play()
    def go_deck(self, btn): self.on_deck()

    def update(self, event):
        for b in self.buttons: b.handle_event(event)

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont("Arial", 60, bold=True)
        title = font.render("TOWER DEFENSE ULTIMATE", True, NEON_YELLOW)
        rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        surface.blit(title, rect)
        for b in self.buttons: b.draw(surface)

class DeckBuilder:
    def __init__(self, on_finish):
        self.on_finish = on_finish
        self.available_towers = list(TOWER_DATA.keys())
        self.selected_towers = []
        
        self.cards_data = [] 
        
        card_w, card_h = 140, 180 
        gap_x, gap_y = 40, 40     
        items_per_row = 5         
        
        total_row_width = (items_per_row * card_w) + ((items_per_row - 1) * gap_x)
        start_x = (SCREEN_WIDTH - total_row_width) // 2
        
        start_y = 200 
        x, y = start_x, start_y
        
        for i, t_name in enumerate(self.available_towers):
            btn_sel = Button("CHOISIR", x + 10, y + 140, 80, 30, GRAY, WHITE, self.toggle_select)
            btn_sel.tower_name = t_name
            btn_sel.font_size = 14
            
            btn_inf = Button("?", x + 100, y + 140, 30, 30, NEON_BLUE, WHITE, self.show_info)
            btn_inf.tower_name = t_name
            
            self.cards_data.append({
                'name': t_name,
                'base_x': x,
                'base_y': y,
                'width': card_w,
                'height': card_h,
                'btn_select': btn_sel,
                'btn_info': btn_inf
            })
            
            x += card_w + gap_x
            if (i + 1) % items_per_row == 0:
                x = start_x
                y += card_h + gap_y

        rows = (len(self.available_towers) + items_per_row - 1) // items_per_row
        self.content_height = (rows * (card_h + gap_y)) 
        
        self.scroll_y = 0
        self.scroll_speed = 30
        self.view_rect = pygame.Rect(0, 180, SCREEN_WIDTH, 450) 
        self.max_scroll = max(0, self.content_height - self.view_rect.height + 50)

        self.btn_validate = Button("VALIDER", SCREEN_WIDTH//2 - 100, 660, 200, 50, NEON_GREEN, BLACK, self.finish)
        
        self.inspected_tower = None
        self.close_info_btn = Button("X", SCREEN_WIDTH//2 + 250, 150, 40, 40, RED, WHITE, self.close_info)

    def toggle_select(self, btn):
        name = btn.tower_name
        if name in self.selected_towers:
            self.selected_towers.remove(name)
        elif len(self.selected_towers) < 6:
            self.selected_towers.append(name)
        self.update_buttons_state()

    def show_info(self, btn):
        self.inspected_tower = btn.tower_name

    def close_info(self, btn):
        self.inspected_tower = None

    def update_buttons_state(self):
        for card in self.cards_data:
            b = card['btn_select']
            if card['name'] in self.selected_towers:
                b.text = "RETIRER"
                b.color = NEON_GREEN
                b.text_color = BLACK
            else:
                b.text = "CHOISIR"
                b.color = GRAY
                b.text_color = WHITE

    def finish(self, btn):
        if len(self.selected_towers) > 0:
            self.on_finish(self.selected_towers)

    def update(self, event):
        if self.inspected_tower:
            self.close_info_btn.handle_event(event)
            return

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * self.scroll_speed
            if self.scroll_y < 0: self.scroll_y = 0
            if self.scroll_y > self.max_scroll: self.scroll_y = self.max_scroll

        for card in self.cards_data:
            curr_y = card['base_y'] - self.scroll_y
            
            card['btn_select'].rect.y = curr_y + 140
            card['btn_info'].rect.y = curr_y + 140
            
            card_rect = pygame.Rect(card['base_x'], curr_y, card['width'], card['height'])
            if self.view_rect.colliderect(card_rect):
                card['btn_select'].handle_event(event)
                card['btn_info'].handle_event(event)

        self.btn_validate.handle_event(event)

    def draw(self, surface):
        surface.fill(BLACK)
        
        font = pygame.font.SysFont("Arial", 50)
        title = font.render(f"CONSTRUIRE LE DECK ({len(self.selected_towers)}/6)", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        surface.set_clip(self.view_rect)
        
        for card in self.cards_data:
            curr_y = card['base_y'] - self.scroll_y
            rect = pygame.Rect(card['base_x'], curr_y, card['width'], card['height'])
            
            if self.view_rect.colliderect(rect):
                color_bg = (30, 30, 40)
                if card['name'] in self.selected_towers:
                    color_bg = (50, 60, 50)
                    pygame.draw.rect(surface, NEON_GREEN, rect, 2)
                else:
                    pygame.draw.rect(surface, GRAY, rect, 1)
                
                pygame.draw.rect(surface, color_bg, (rect.x+1, rect.y+1, rect.w-2, rect.h-2))

                font_nm = pygame.font.SysFont("Arial", 18, bold=True)
                nm = font_nm.render(card['name'], True, NEON_YELLOW)
                nm_r = nm.get_rect(centerx=rect.centerx, top=rect.y + 10)
                surface.blit(nm, nm_r)

                data = TOWER_DATA[card['name']]
                pygame.draw.rect(surface, data["color"], (rect.centerx - 20, rect.y + 40, 40, 40))
                
                font_pr = pygame.font.SysFont("Arial", 20, bold=True)
                pr = font_pr.render(f"{data['cost']}$", True, WHITE)
                pr_r = pr.get_rect(centerx=rect.centerx, top=rect.y + 90)
                surface.blit(pr, pr_r)

                card['btn_select'].draw(surface)
                card['btn_info'].draw(surface)

        surface.set_clip(None)

        self.btn_validate.draw(surface)

        if self.inspected_tower:
            self.draw_info_overlay(surface)

    def draw_info_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0,0))

        w, h = 600, 400
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        rect = pygame.Rect(cx - w//2, cy - h//2, w, h)
        pygame.draw.rect(surface, BLUE_PANEL, rect)
        pygame.draw.rect(surface, WHITE, rect, 3)

        name = self.inspected_tower
        desc = TOWER_DESCRIPTIONS.get(name, {})
        data = TOWER_DATA[name]
        
        group = desc.get("group", "Inconnu")
        title_text = f"{name.upper()} ({group.upper()})"
        
        font_title = pygame.font.SysFont("Arial", 32, bold=True)
        t = font_title.render(title_text, True, NEON_YELLOW)
        surface.blit(t, (rect.x + 30, rect.y + 30))

        font_txt = pygame.font.SysFont("Arial", 20)
        stats = f"Coût: {data['cost']}$  |  Portée: {data['range']}  |  Dégâts: {data['damage']}"
        s_surf = font_txt.render(stats, True, WHITE)
        surface.blit(s_surf, (rect.x + 30, rect.y + 80))

        gimmick = desc.get("gimmick", "Aucune.")
        g_surf = font_txt.render(f"Spécial : {gimmick}", True, NEON_BLUE)
        surface.blit(g_surf, (rect.x + 30, rect.y + 120))

        pygame.draw.line(surface, GRAY, (rect.x+20, rect.y+160), (rect.right-20, rect.y+160), 1)

        font_sub = pygame.font.SysFont("Arial", 22, bold=True)
        surface.blit(font_sub.render("AMÉLIORATIONS", True, WHITE), (rect.x + 30, rect.y + 170))

        lvl2_txt = desc.get("lvl2", "Amélioration standard.")
        l2 = font_txt.render(f"Niveau 2 : {lvl2_txt}", True, NEON_GREEN)
        surface.blit(l2, (rect.x + 30, rect.y + 210))

        l3a_txt = desc.get("lvl3_a", "Option A")
        l3b_txt = desc.get("lvl3_b", "Option B")
        
        l3a = font_txt.render(f"Niveau 3 (A) : {l3a_txt}", True, NEON_PURPLE)
        l3b = font_txt.render(f"Niveau 3 (B) : {l3b_txt}", True, NEON_PURPLE)
        
        surface.blit(l3a, (rect.x + 30, rect.y + 250))
        surface.blit(l3b, (rect.x + 30, rect.y + 290))

        self.close_info_btn.rect.topleft = (rect.right - 50, rect.y + 10)
        self.close_info_btn.draw(surface)

class GameUI:
    def __init__(self, deck, money, lives):
        self.deck = deck
        self.buttons = []
        
        btn_size = 50 
        gap = 10
        total_w = len(deck) * (btn_size + gap)
        start_x = (SCREEN_WIDTH - total_w) // 2
        y = 45 
        
        self.btn_pause = Button("PAUSE", SCREEN_WIDTH - 100, 10, 80, 30, NEON_BLUE, BLACK, None)
        
        x = start_x
        for t_name in deck:
            data = TOWER_DATA[t_name]
            cost = str(data["cost"]) + "$"
            b = Button(cost, x, y, btn_size, btn_size, GRAY_DARK, WHITE, None)
            b.tower_name = t_name
            b.icon_color = data["color"]
            self.buttons.append(b)
            x += btn_size + gap

    def draw(self, surface, money, lives, wave_display, selected_tower_idx, tower_count, is_paused):
        pygame.draw.rect(surface, (20, 20, 30), (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.line(surface, WHITE, (0, 100), (SCREEN_WIDTH, 100), 2)
        font = pygame.font.SysFont("Arial", 24, bold=True)
        
        txt_money = font.render(f"Argent: {money}$", True, NEON_GREEN)
        surface.blit(txt_money, (40, 10))
        
        txt_lives = font.render(f"Vies: {lives}", True, RED)
        surface.blit(txt_lives, (250, 10))
        
        txt_wave = font.render(f"Vague: {wave_display}", True, WHITE)
        surface.blit(txt_wave, (SCREEN_WIDTH // 2 - 50, 10))
        
        color_towers = NEON_BLUE if tower_count < 20 else RED
        txt_towers = font.render(f"Tours: {tower_count}/20", True, color_towers)
        surface.blit(txt_towers, (SCREEN_WIDTH - 250, 10)) 

        if is_paused:
            self.btn_pause.text = "PLAY"
            self.btn_pause.color = NEON_GREEN
        else:
            self.btn_pause.text = "PAUSE"
            self.btn_pause.color = NEON_BLUE
        
        # --- CORRECTION ICI : On utilise juste .draw() ---
        self.btn_pause.draw(surface)
        
        # J'ai supprimé les lignes manuelles ci-dessous qui créaient le doublon :
        # font_p = pygame.font.SysFont("Arial", 16, bold=True)
        # txt_p = font_p.render(self.btn_pause.text, True, BLACK)
        # rect_p = txt_p.get_rect(center=self.btn_pause.rect.center)
        # surface.blit(txt_p, rect_p)

        for i, btn in enumerate(self.buttons):
            if selected_tower_idx == i:
                pygame.draw.rect(surface, WHITE, (btn.rect.x-3, btn.rect.y-3, btn.rect.w+6, btn.rect.h+6), 3)
            pygame.draw.rect(surface, GRAY_DARK, btn.rect)
            pygame.draw.rect(surface, btn.icon_color, (btn.rect.x+10, btn.rect.y+8, 30, 30))
            font_price = pygame.font.SysFont("Arial", 12, bold=True)
            p_txt = font_price.render(btn.text, True, WHITE)
            p_rect = p_txt.get_rect(centerx=btn.rect.centerx, bottom=btn.rect.bottom - 2)
            surface.blit(p_txt, p_rect)

    def draw_upgrade_panel(self, surface, tower):
        panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT - 120, 400, 100)
        pygame.draw.rect(surface, BLUE_PANEL, panel_rect)
        pygame.draw.rect(surface, WHITE, panel_rect, 2)
        
        font = pygame.font.SysFont("Arial", 20, bold=True)
        font_small = pygame.font.SysFont("Arial", 14, bold=True)
        
        name = font.render(f"{tower.name} (Lvl {tower.level})", True, NEON_YELLOW)
        surface.blit(name, (panel_rect.x + 20, panel_rect.y + 10))
        
        close_rect = pygame.Rect(panel_rect.right - 30, panel_rect.y, 30, 30)
        pygame.draw.rect(surface, RED, close_rect)
        x_txt = font.render("X", True, WHITE)
        surface.blit(x_txt, (close_rect.x + 8, close_rect.y + 4))
        
        if tower.level == 1:
            upgrade_cost = int(tower.stats["cost"] * 1.5)
            btn_txt = f"UPGRADE LVL 2 ({upgrade_cost}$)"
            up_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 55, 360, 30)
            pygame.draw.rect(surface, NEON_GREEN, up_rect)
            up_surf = font.render(btn_txt, True, BLACK)
            text_rect = up_surf.get_rect(center=up_rect.center)
            surface.blit(up_surf, text_rect)
            
        elif tower.level == 2:
            upgrade_cost = tower.stats["cost"] + 700 
            branches = tower.branches.get(tower.name, ("Option 1", "Option 2"))
            
            # Gauche
            btn1_rect = pygame.Rect(panel_rect.x + 20, panel_rect.y + 50, 170, 40)
            pygame.draw.rect(surface, NEON_GREEN, btn1_rect)
            txt1 = font_small.render(branches[0], True, BLACK)
            txt1_p = font_small.render(f"{upgrade_cost}$", True, BLACK)
            surface.blit(txt1, (btn1_rect.x + 5, btn1_rect.y + 2))
            surface.blit(txt1_p, (btn1_rect.x + 5, btn1_rect.y + 22))

            # Droite
            btn2_rect = pygame.Rect(panel_rect.x + 210, panel_rect.y + 50, 170, 40)
            pygame.draw.rect(surface, NEON_BLUE, btn2_rect)
            txt2 = font_small.render(branches[1], True, BLACK)
            txt2_p = font_small.render(f"{upgrade_cost}$", True, BLACK)
            surface.blit(txt2, (btn2_rect.x + 5, btn2_rect.y + 2))
            surface.blit(txt2_p, (btn2_rect.x + 5, btn2_rect.y + 22))

        else:
            b_name = tower.branches.get(tower.name, ("",""))[tower.branch-1]
            max_txt = font.render(f"SPÉCIALITÉ : {b_name}", True, NEON_YELLOW)
            surface.blit(max_txt, (panel_rect.x + 20, panel_rect.y + 50))

class EndGameMenu:
    def __init__(self, on_menu):
        self.on_menu = on_menu
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.btn_menu = Button("MENU PRINCIPAL", cx - 125, cy + 50, 250, 60, NEON_BLUE, BLACK, self.go_menu)
        self.title_text = ""
        self.title_color = WHITE

    def set_mode(self, mode):
        if mode == "win":
            self.title_text = "VICTOIRE !"
            self.title_color = NEON_GREEN
        else:
            self.title_text = "GAME OVER"
            self.title_color = RED

    def go_menu(self, btn):
        self.on_menu()

    def update(self, event):
        self.btn_menu.handle_event(event)

    def draw(self, surface):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(200) 
        s.fill(BLACK)
        surface.blit(s, (0,0))
        font = pygame.font.SysFont("Arial", 80, bold=True)
        txt = font.render(self.title_text, True, self.title_color)
        rect = txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        surface.blit(txt, rect)
        self.btn_menu.draw(surface)
        font_btn = pygame.font.SysFont("Arial", 24, bold=True)
        t_btn = font_btn.render("MENU PRINCIPAL", True, BLACK)
        r_btn = t_btn.get_rect(center=self.btn_menu.rect.center)
        surface.blit(t_btn, r_btn)