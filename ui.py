import pygame
from settings import *
from towers.specs import TOWER_DATA

# Couleurs
GRAY = (100, 100, 100)
GRAY_DARK = (50, 50, 50)
BLUE_PANEL = (20, 30, 50)

# --- DESCRIPTIONS COMPLÈTES ---
TOWER_DESCRIPTIONS = {
    "Standard": {
        "group": "Classique",
        "gimmick": "Tour polyvalente de base.",
        "lvl2": "Augmente Dégâts et Portée.",
        "lvl3_a": "Double Gun : Tire deux balles à la fois.",
        "lvl3_b": "Ghostbuster : Voit les ennemis Invisibles."
    },
    "Sniper": {
        "group": "Militaire",
        "gimmick": "Portée immense, dégâts élevés, lent.",
        "lvl2": "Augmente Dégâts critiques.",
        "lvl3_a": "Elite Sniper : Brise les Boucliers (Bleu).",
        "lvl3_b": "Semi Auto : Tire 2x plus vite."
    },
    "Gatling": {
        "group": "Militaire",
        "gimmick": "Tire très vite, dégâts faibles.",
        "lvl2": "Encore plus rapide.",
        "lvl3_a": "Double Uzi : Tire 2 projectiles (Mitraille).",
        "lvl3_b": "Modded Gatling : Vitesse extrême (x3)."
    },
    "Canon": {
        "group": "Explosif",
        "gimmick": "Dégâts de zone (Explosion).",
        "lvl2": "Zone d'explosion plus grande.",
        "lvl3_a": "Missile Launcher : Projectiles rapides.",
        "lvl3_b": "Slime Cannon : Laisse une zone de ralentissement."
    },
    "Cryo": {
        "group": "Contrôle",
        "gimmick": "Ralentit les ennemis (Glace).",
        "lvl2": "Ralentissement plus fort.",
        "lvl3_a": "Deep Freeze : Congèle (Stun) périodiquement.",
        "lvl3_b": "Blizzard : Aura de ralentissement permanent."
    },
    "Flamethrower": {
        "group": "Zone",
        "gimmick": "Brûle les ennemis (Dégâts sur la durée).",
        "lvl2": "Brûlure plus intense.",
        "lvl3_a": "Blue Flame : Dégâts doublés.",
        "lvl3_b": "Incinerator : Brûlure permanente."
    },
    "Laser": {
        "group": "Tech",
        "gimmick": "Rayon instantané, traverse l'armure.",
        "lvl2": "Augmente la puissance.",
        "lvl3_a": "Laser Beam : Tir continu rapide.",
        "lvl3_b": "Laser Mk2 : Rebondit sur 2 ennemis (Chain)."
    },
    "Fan": {
        "group": "Absurde",
        "gimmick": "Repousse les ennemis. 0 Dégâts.",
        "lvl2": "Souffle plus fort.",
        "lvl3_a": "Industrial Fan : Ralentissement lourd.",
        "lvl3_b": "Boosted Fan : Repousse les Boss."
    },
    "Hive": {
        "group": "Nature",
        "gimmick": "Invoque des abeilles autonomes.",
        "lvl2": "Plus d'abeilles.",
        "lvl3_a": "Killer Swarm : 8 Abeilles rapides.",
        "lvl3_b": "Giant Hornets : 2 Frelons robustes."
    },
    "Robot Factory": {
        "group": "Invocation",
        "gimmick": "Pose des robots bloqueurs sur la route.",
        "lvl2": "Robots plus résistants.",
        "lvl3_a": "Swarm Maker : 5 petits robots (masse).",
        "lvl3_b": "Mecha Factory : 1 Robot Tank géant."
    },
    "Cactus": {
        "group": "Plante",
        "gimmick": "Tire des épines. Renvoie les dégâts.",
        "lvl2": "Plus d'épines.",
        "lvl3_a": "Twin Spikes : Tire 2 épines.",
        "lvl3_b": "Armor Piercer : Ignore l'armure."
    },
    "Toaster": {
        "group": "Absurde",
        "gimmick": "Lance des toasts physiques.",
        "lvl2": "Dégâts augmentés.",
        "lvl3_a": "Burnt Toast : Dégâts de feu élevés.",
        "lvl3_b": "Sticky Jam : Toasts qui ralentissent."
    },
    "Butterfly": {
        "group": "Insecte",
        "gimmick": "Charme les ennemis (ils reculent).",
        "lvl2": "Charme plus long.",
        "lvl3_a": "Hypnotic Powder : Confusion de zone.",
        "lvl3_b": "Betrayal : Transforme un ennemi en allié."
    },
    "Boomerang": {
        "group": "Habileté",
        "gimmick": "Ricoche sur un 2ème ennemi.",
        "lvl2": "Meilleure portée.",
        "lvl3_a": "Triple Loop : Ricoche sur 3 ennemis.",
        "lvl3_b": "Round Trip : Traverse tout et revient."
    },
    "Spy": {
        "group": "Tactique",
        "gimmick": "Inflige 15% des PV MAX de la cible.",
        "lvl2": "Rechargement rapide.",
        "lvl3_a": "Cyanide : Inflige 25% des PV MAX.",
        "lvl3_b": "License to Kill : Exécute si < 30% PV."
    },
    "Mage": {
        "group": "Magique",
        "gimmick": "Tir magique (10 dégâts).",
        "lvl2": "Augmente portée.",
        "lvl3_a": "Pyromancer : Boule de feu explosive (Dégâts x4).",
        "lvl3_b": "Cryomancer : Boule de glace (Zone Slow)."
    },
    "Crab": {
        "group": "Nature",
        "gimmick": "Applique 'Fragile' (+1 dégât subi).",
        "lvl2": "Pince plus rapide.",
        "lvl3_a": "King Crab : Frappe en zone (Fragile de masse).",
        "lvl3_b": "Mantis Shrimp : Vitesse extrême + Stun."
    },
    "Rose": {
        "group": "Plante",
        "gimmick": "Pose des ronces (7 dégâts) sur le chemin.",
        "lvl2": "Pose plus souvent.",
        "lvl3_a": "Jardin Carnivore : Les ronces explosent.",
        "lvl3_b": "Racines Profondes : Immobilise (Root) 1.5s."
    },
    "Orchid": {
        "group": "Magique",
        "gimmick": "Charge. 4ème tir = Burst de dégâts.",
        "lvl2": "Recharge plus vite.",
        "lvl3_a": "Prisme : Ricoche sur 2 cibles.",
        "lvl3_b": "Harmonie Parfaite : Invoque 3 cristaux orbitaux qui tirent."
    },
    "Shampoo": {
        "group": "Absurde",
        "gimmick": "Bulles qui repoussent (Knockback).",
        "lvl2": "Plus de bulles.",
        "lvl3_a": "Après-shampoing : Flaque glissante (Slow).",
        "lvl3_b": "Ça pique les yeux : Rend Confus."
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
        self.buttons = [self.btn_play, self.btn_deck]

    def go_play(self, btn): self.on_play()
    def go_deck(self, btn): self.on_deck()

    def update(self, event):
        for b in self.buttons: b.handle_event(event)

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont("Arial", 60, bold=True)
        title = font.render("TOWER DEFENSE", True, NEON_YELLOW)
        rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        surface.blit(title, rect)
        for b in self.buttons: b.draw(surface)

class DeckBuilder:
    def __init__(self, on_finish):
        self.on_finish = on_finish
        self.available_towers = list(TOWER_DATA.keys())
        self.selected_towers = []
        self.cards_data = [] 
        self.font_desc = pygame.font.SysFont("Arial", 18) # Police pour la description
        
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
                'name': t_name, 'base_x': x, 'base_y': y,
                'width': card_w, 'height': card_h,
                'btn_select': btn_sel, 'btn_info': btn_inf
            })
            
            x += card_w + gap_x
            if (i + 1) % items_per_row == 0:
                x = start_x
                y += card_h + gap_y

        rows = (len(self.available_towers) + items_per_row - 1) // items_per_row
        self.content_height = (rows * (card_h + gap_y)) 
        
        self.scroll_y = 0
        self.view_rect = pygame.Rect(0, 180, SCREEN_WIDTH, 450) 
        self.max_scroll = max(0, self.content_height - self.view_rect.height + 50)
        self.btn_validate = Button("VALIDER", SCREEN_WIDTH//2 - 100, 660, 200, 50, NEON_GREEN, BLACK, self.finish)
        self.inspected_tower = None
        self.close_info_btn = Button("X", SCREEN_WIDTH//2 + 250, 150, 40, 40, RED, WHITE, self.close_info)

    def draw_text_wrapped(self, surface, text, pos, max_width, color, font):
        words = text.split(' ')
        space = font.size(' ')[0]
        x, y = pos
        line_height = font.get_linesize()
        for word in words:
            word_surface = font.render(word, True, color)
            word_w, word_h = word_surface.get_size()
            if x + word_w >= pos[0] + max_width:
                x = pos[0]; y += line_height
            surface.blit(word_surface, (x, y))
            x += word_w + space
        return y + line_height

    def toggle_select(self, btn):
        if btn.tower_name in self.selected_towers:
            self.selected_towers.remove(btn.tower_name)
        elif len(self.selected_towers) < 8:
            self.selected_towers.append(btn.tower_name)
        self.update_buttons_state()

    def show_info(self, btn): self.inspected_tower = btn.tower_name
    def close_info(self, btn): self.inspected_tower = None

    def update_buttons_state(self):
        for card in self.cards_data:
            b = card['btn_select']
            if card['name'] in self.selected_towers:
                b.text = "RETIRER"; b.color = NEON_GREEN; b.text_color = BLACK
            else:
                b.text = "CHOISIR"; b.color = GRAY; b.text_color = WHITE

    def finish(self, btn):
        if len(self.selected_towers) > 0: self.on_finish(self.selected_towers)

    def update(self, event):
        if self.inspected_tower:
            self.close_info_btn.handle_event(event)
            return
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - event.y * 30))
        for card in self.cards_data:
            curr_y = card['base_y'] - self.scroll_y
            card['btn_select'].rect.y = curr_y + 140
            card['btn_info'].rect.y = curr_y + 140
            if self.view_rect.colliderect(pygame.Rect(card['base_x'], curr_y, card['width'], card['height'])):
                card['btn_select'].handle_event(event)
                card['btn_info'].handle_event(event)
        self.btn_validate.handle_event(event)

    def draw(self, surface):
        surface.fill(BLACK)
        font = pygame.font.SysFont("Arial", 50)
        title = font.render(f"DECK ({len(self.selected_towers)}/8)", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        surface.set_clip(self.view_rect)
        
        for card in self.cards_data:
            curr_y = card['base_y'] - self.scroll_y
            rect = pygame.Rect(card['base_x'], curr_y, card['width'], card['height'])
            if self.view_rect.colliderect(rect):
                col = (50, 60, 50) if card['name'] in self.selected_towers else (30, 30, 40)
                pygame.draw.rect(surface, NEON_GREEN if card['name'] in self.selected_towers else GRAY, rect, 2)
                pygame.draw.rect(surface, col, (rect.x+1, rect.y+1, rect.w-2, rect.h-2))
                
                nm = pygame.font.SysFont("Arial", 18, bold=True).render(card['name'], True, NEON_YELLOW)
                surface.blit(nm, nm.get_rect(centerx=rect.centerx, top=rect.y + 10))
                
                data = TOWER_DATA[card['name']]
                pygame.draw.rect(surface, data["color"], (rect.centerx - 20, rect.y + 40, 40, 40))
                pr = pygame.font.SysFont("Arial", 20, bold=True).render(f"{data['cost']}$", True, WHITE)
                surface.blit(pr, pr.get_rect(centerx=rect.centerx, top=rect.y + 90))
                
                card['btn_select'].draw(surface); card['btn_info'].draw(surface)
        surface.set_clip(None)
        self.btn_validate.draw(surface)
        if self.inspected_tower: self.draw_info_overlay(surface)

    def draw_info_overlay(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(180); overlay.fill(BLACK)
        surface.blit(overlay, (0,0))
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        rect = pygame.Rect(cx - 300, cy - 200, 600, 400)
        pygame.draw.rect(surface, BLUE_PANEL, rect); pygame.draw.rect(surface, WHITE, rect, 3)
        
        name = self.inspected_tower
        desc = TOWER_DESCRIPTIONS.get(name, {})
        font_t = pygame.font.SysFont("Arial", 32, bold=True)
        surface.blit(font_t.render(f"{name.upper()}", True, NEON_YELLOW), (rect.x + 30, rect.y + 30))
        
        # --- AFFICHAGE DESCRIPTIONS ---
        y_off = rect.y + 80
        x_off = rect.x + 30
        w_txt = 540 # Largeur texte
        
        if "group" in desc:
             y_off = self.draw_text_wrapped(surface, f"Type: {desc['group']}", (x_off, y_off), w_txt, NEON_BLUE, self.font_desc)
             y_off += 10
        if "gimmick" in desc:
             y_off = self.draw_text_wrapped(surface, desc["gimmick"], (x_off, y_off), w_txt, WHITE, self.font_desc)
             y_off += 20
        if "lvl2" in desc:
             y_off = self.draw_text_wrapped(surface, f"Niv 2: {desc['lvl2']}", (x_off, y_off), w_txt, (200, 200, 200), self.font_desc)
             y_off += 10
        if "lvl3_a" in desc:
             y_off = self.draw_text_wrapped(surface, f"Lvl 3 A: {desc['lvl3_a']}", (x_off, y_off), w_txt, NEON_GREEN, self.font_desc)
             y_off += 5
        if "lvl3_b" in desc:
             y_off = self.draw_text_wrapped(surface, f"Lvl 3 B: {desc['lvl3_b']}", (x_off, y_off), w_txt, NEON_BLUE, self.font_desc)

        self.close_info_btn.rect.topleft = (rect.right - 50, rect.y + 10)
        self.close_info_btn.draw(surface)

class GameUI:
    def __init__(self, deck, money, lives):
        self.deck = deck
        self.buttons = []
        btn_size = 50; gap = 10
        total_w = len(deck) * (btn_size + gap)
        start_x = (SCREEN_WIDTH - total_w) // 2
        y = 45 
        self.btn_pause = Button("PAUSE", SCREEN_WIDTH - 100, 10, 80, 30, NEON_BLUE, BLACK, None)
        
        x = start_x
        for t_name in deck:
            data = TOWER_DATA[t_name]
            b = Button(f"{data['cost']}$", x, y, btn_size, btn_size, GRAY_DARK, WHITE, None)
            b.tower_name = t_name; b.icon_color = data["color"]
            self.buttons.append(b); x += btn_size + gap

        # Police pour le texte wrappé
        self.font_desc = pygame.font.SysFont("Arial", 16)

    def draw_text_wrapped(self, surface, text, pos, max_width, color, font):
        words = text.split(' ')
        space = font.size(' ')[0]
        x, y = pos
        line_height = font.get_linesize()
        for word in words:
            word_surface = font.render(word, True, color)
            word_w, word_h = word_surface.get_size()
            if x + word_w >= pos[0] + max_width:
                x = pos[0]; y += line_height
            surface.blit(word_surface, (x, y))
            x += word_w + space
        return y + line_height

    def draw(self, surface, money, lives, wave_display, selected_tower_idx, tower_count, is_paused):
        pygame.draw.rect(surface, (20, 20, 30), (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.line(surface, WHITE, (0, 100), (SCREEN_WIDTH, 100), 2)
        font = pygame.font.SysFont("Arial", 24, bold=True)
        
        surface.blit(font.render(f"Argent: {money}$", True, NEON_GREEN), (40, 10))
        surface.blit(font.render(f"Vies: {lives}", True, RED), (250, 10))
        surface.blit(font.render(f"Vague: {wave_display}", True, WHITE), (SCREEN_WIDTH // 2 - 50, 10))
        surface.blit(font.render(f"Tours: {tower_count}/20", True, NEON_BLUE if tower_count < 20 else RED), (SCREEN_WIDTH - 250, 10)) 

        self.btn_pause.text = "PLAY" if is_paused else "PAUSE"
        self.btn_pause.color = NEON_GREEN if is_paused else NEON_BLUE
        self.btn_pause.draw(surface)

        for i, btn in enumerate(self.buttons):
            if selected_tower_idx == i:
                pygame.draw.rect(surface, WHITE, (btn.rect.x-3, btn.rect.y-3, btn.rect.w+6, btn.rect.h+6), 3)
            pygame.draw.rect(surface, GRAY_DARK, btn.rect)
            pygame.draw.rect(surface, btn.icon_color, (btn.rect.x+10, btn.rect.y+8, 30, 30))
            p_txt = pygame.font.SysFont("Arial", 12, bold=True).render(btn.text, True, WHITE)
            surface.blit(p_txt, p_txt.get_rect(centerx=btn.rect.centerx, bottom=btn.rect.bottom - 2))

    def draw_upgrade_panel(self, surface, tower):
        # --- PANNEAU LATÉRAL DROIT ---
        panel_w = 370 # Largeur augmentée
        panel_rect = pygame.Rect(SCREEN_WIDTH - panel_w, 100, panel_w, SCREEN_HEIGHT - 100)
        pygame.draw.rect(surface, (30, 30, 40), panel_rect)
        pygame.draw.line(surface, WHITE, (panel_rect.x, 100), (panel_rect.x, SCREEN_HEIGHT), 2)
        
        font_title = pygame.font.SysFont("Arial", 22, bold=True)
        
        y_off = 120
        x_off = panel_rect.x + 20
        name_txt = font_title.render(f"{tower.name}", True, tower.stats["color"])
        surface.blit(name_txt, (x_off, y_off))
        y_off += 30
        
        lvl_txt = font_title.render(f"Niveau {tower.level}", True, WHITE)
        surface.blit(lvl_txt, (x_off, y_off))
        y_off += 40
        
        stats = f"Dmg: {tower.damage} | Rg: {tower.range}"
        surface.blit(self.font_desc.render(stats, True, (200, 200, 200)), (x_off, y_off))
        y_off += 30
        
        close_btn = pygame.Rect(panel_rect.right - 40, 110, 30, 30)
        pygame.draw.rect(surface, RED, close_btn)
        surface.blit(font_title.render("X", True, WHITE), (close_btn.x+7, close_btn.y+2))

        desc_data = TOWER_DESCRIPTIONS.get(tower.name, {})
        text_width = panel_w - 40 # 330
        
        if "gimmick" in desc_data:
            y_off = self.draw_text_wrapped(surface, desc_data["gimmick"], (x_off, y_off), text_width, (200, 255, 200), self.font_desc)
            y_off += 20

        if tower.level == 1:
            cost = int(tower.stats["cost"] * 1.5)
            up_rect = pygame.Rect(x_off, y_off, text_width, 40)
            pygame.draw.rect(surface, NEON_GREEN, up_rect, border_radius=5)
            up_txt = font_title.render(f"Améliorer ({cost}$)", True, BLACK)
            surface.blit(up_txt, up_txt.get_rect(center=up_rect.center))
            y_off += 50
            
            if "lvl2" in desc_data:
                y_off = self.draw_text_wrapped(surface, f"Niv 2: {desc_data['lvl2']}", (x_off, y_off), text_width, (180, 180, 180), self.font_desc)

        elif tower.level == 2:
            cost = tower.stats["cost"] + 700
            
            btn1 = pygame.Rect(x_off, y_off, text_width, 50)
            pygame.draw.rect(surface, NEON_GREEN, btn1, border_radius=5)
            branches = tower.branches.get(tower.name, ("A", "B"))
            t1 = font_title.render(branches[0], True, BLACK)
            t1p = self.font_desc.render(f"{cost}$", True, BLACK)
            surface.blit(t1, (btn1.x+10, btn1.y+5)); surface.blit(t1p, (btn1.right-50, btn1.y+15))
            y_off += 60
            
            desc_a = desc_data.get("lvl3_a", "???")
            y_off = self.draw_text_wrapped(surface, desc_a, (x_off, y_off), text_width, (150, 255, 150), self.font_desc)
            y_off += 20

            btn2 = pygame.Rect(x_off, y_off, text_width, 50)
            pygame.draw.rect(surface, NEON_BLUE, btn2, border_radius=5)
            t2 = font_title.render(branches[1], True, BLACK)
            surface.blit(t2, (btn2.x+10, btn2.y+5)); surface.blit(t1p, (btn2.right-50, btn2.y+15))
            y_off += 60
            
            desc_b = desc_data.get("lvl3_b", "???")
            y_off = self.draw_text_wrapped(surface, desc_b, (x_off, y_off), text_width, (150, 150, 255), self.font_desc)

        else:
            surf_max = font_title.render("NIVEAU MAX", True, NEON_YELLOW)
            surface.blit(surf_max, (x_off, y_off))
            y_off += 40
            
            b_name = tower.branches.get(tower.name, ("A", "B"))[0 if tower.branch == 1 else 1]
            col = NEON_GREEN if tower.branch == 1 else NEON_BLUE
            desc_key = "lvl3_a" if tower.branch == 1 else "lvl3_b"
            bonus_desc = desc_data.get(desc_key, b_name)
            
            y_off = self.draw_text_wrapped(surface, f"Bonus Actif: {bonus_desc}", (x_off, y_off), text_width, col, self.font_desc)

class EndGameMenu:
    def __init__(self, on_menu):
        self.on_menu = on_menu
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.btn_menu = Button("MENU PRINCIPAL", cx - 125, cy + 50, 250, 60, NEON_BLUE, BLACK, self.go_menu)
        self.title_text = ""; self.title_color = WHITE

    def set_mode(self, mode):
        if mode == "win": self.title_text = "VICTOIRE !"; self.title_color = NEON_GREEN
        else: self.title_text = "GAME OVER"; self.title_color = RED

    def go_menu(self, btn): self.on_menu()
    def update(self, event): self.btn_menu.handle_event(event)

    def draw(self, surface):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(200); s.fill(BLACK)
        surface.blit(s, (0,0))
        font = pygame.font.SysFont("Arial", 80, bold=True)
        txt = font.render(self.title_text, True, self.title_color)
        surface.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
        self.btn_menu.draw(surface)