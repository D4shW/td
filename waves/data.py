# waves/data.py

# Liste des vagues. Chaque vague est une liste de groupes d'ennemis.
# "shield": True ajoute un bouclier bleu (Barre bleue) à l'ennemi.

WAVE_DATA = [
    # --- PHASE 1 : DÉCOUVERTE (W1-W10) ---
    # Introduction des mécaniques de base, du Berserker et du Gardien.
    
    # Wave 1 : Le classique
    [{"enemy": "Soldier", "count": 5, "interval": 1500}],
    # Wave 2 : Un peu de vitesse
    [{"enemy": "Soldier", "count": 8, "interval": 1200}, {"enemy": "Flash", "count": 3, "interval": 2000}],
    # Wave 3 : Les diviseurs
    [{"enemy": "Splitter", "count": 3, "interval": 2500}],
    # Wave 4 : Tank
    [{"enemy": "Soldier", "count": 10, "interval": 800}, {"enemy": "Tank", "count": 1, "interval": 100}],
    
    # Wave 5 : INTRO BERSERKER (Attention à la vitesse quand ils sont blessés)
    [{"enemy": "Soldier", "count": 5, "interval": 1000}, {"enemy": "Berserker", "count": 3, "interval": 2000}],
    
    # Wave 6 : Fantômes
    [{"enemy": "Ghost", "count": 5, "interval": 1500}],
    
    # Wave 7 : INTRO GARDIEN (Régénération de bouclier)
    [{"enemy": "Guardian", "count": 3, "interval": 2000}],
    
    # Wave 8 : Mix Défensif
    [{"enemy": "Soldier", "count": 10, "interval": 1000}, {"enemy": "Guardian", "count": 2, "interval": 3000}],
    # Wave 9 : Mix Offensif
    [{"enemy": "Flash", "count": 10, "interval": 800}, {"enemy": "Berserker", "count": 2, "interval": 2000}],
    
    # --- WAVE 10 : BOSS ---
    [{"enemy": "Boss", "count": 1, "interval": 5000}],


    # --- PHASE 2 : COMBINAISONS (W11-W20) ---
    # On commence à mélanger les types pour forcer des choix de tours.

    # Wave 11 : Vitesse Pure
    [{"enemy": "Flash", "count": 15, "interval": 600}, {"enemy": "Berserker", "count": 5, "interval": 1000}],
    # Wave 12 : Blindés
    [{"enemy": "Tank", "count": 3, "interval": 2000}, {"enemy": "Guardian", "count": 3, "interval": 2000}],
    # Wave 13 : Électricité
    [{"enemy": "Tesla", "count": 8, "interval": 1500}],
    # Wave 14 : Invisible et Résistant
    [{"enemy": "Ghost", "count": 10, "interval": 1000, "shield": True}],
    # Wave 15 : La Division
    [{"enemy": "Mega Splitter", "count": 1, "interval": 5000}, {"enemy": "Splitter", "count": 5, "interval": 1000}],
    # Wave 16 : Horde
    [{"enemy": "Soldier", "count": 30, "interval": 350}],
    # Wave 17 : L'Escorte (Gardien protège Berserker)
    [{"enemy": "Guardian", "count": 5, "interval": 1500}, {"enemy": "Berserker", "count": 5, "interval": 1500}],
    # Wave 18 : Boucliers Rapides
    [{"enemy": "Flash", "count": 12, "interval": 500, "shield": True}],
    # Wave 19 : Heavy Mix
    [{"enemy": "Tank", "count": 4, "interval": 1500}, {"enemy": "Tesla", "count": 5, "interval": 1000}],
    
    # --- WAVE 20 : BOSS TESLA ---
    [{"enemy": "MegaTesla", "count": 1, "interval": 5000}],


    # --- PHASE 3 : COMPLEXITÉ (W21-W30) ---
    # Les ennemis gagnent des boucliers naturels (stat 'shield': True).

    # Wave 21 : Berserkers Énervés
    [{"enemy": "Berserker", "count": 10, "interval": 1200, "shield": True}],
    # Wave 22 : Fantômes de masse
    [{"enemy": "Ghost", "count": 20, "interval": 700}],
    # Wave 23 : Mur de Gardiens
    [{"enemy": "Guardian", "count": 10, "interval": 1200}],
    # Wave 24 : Électricité Statique
    [{"enemy": "Tesla", "count": 12, "interval": 900, "shield": True}],
    # Wave 25 : Mini-Boss Rush
    [{"enemy": "Boss", "count": 2, "interval": 6000}, {"enemy": "Berserker", "count": 5, "interval": 2000}],
    # Wave 26 : Flash Mob
    [{"enemy": "Flash", "count": 30, "interval": 250, "shield": True}],
    # Wave 27 : Division lourde
    [{"enemy": "Mega Splitter", "count": 3, "interval": 4000}],
    # Wave 28 : Tank + Regen
    [{"enemy": "Tank", "count": 5, "interval": 1500}, {"enemy": "Guardian", "count": 5, "interval": 1500}],
    # Wave 29 : Armée
    [{"enemy": "Soldier", "count": 60, "interval": 150}],
    
    # --- WAVE 30 : BOSS SPLITTER ---
    [{"enemy": "GigaSplitter", "count": 1, "interval": 5000}],


    # --- PHASE 4 : HARDCORE (W31-W40) ---
    # Synergies mortelles.

    # Wave 31 : Super Division
    [{"enemy": "Super Splitter", "count": 10, "interval": 1500, "shield": True}],
    # Wave 32 : Tesla Storm
    [{"enemy": "Tesla", "count": 20, "interval": 600}],
    # Wave 33 : Stealth Ops (Fantômes + Berserkers)
    [{"enemy": "Ghost", "count": 15, "interval": 800}, {"enemy": "Berserker", "count": 10, "interval": 800, "shield": True}],
    # Wave 34 : Iron Clad (Full Tank/Guardian)
    [{"enemy": "Tank", "count": 8, "interval": 1200, "shield": True}, {"enemy": "Guardian", "count": 8, "interval": 1200, "shield": True}],
    # Wave 35 : Escorte VIP
    [{"enemy": "MegaTesla", "count": 1, "interval": 1000}, {"enemy": "Guardian", "count": 6, "interval": 500}],
    # Wave 36 : Blitzkrieg
    [{"enemy": "Flash", "count": 50, "interval": 200, "shield": True}],
    # Wave 37 : Chaos Divisé
    [{"enemy": "Mega Splitter", "count": 5, "interval": 3000, "shield": True}],
    # Wave 38 : Triple Menace
    [{"enemy": "Boss", "count": 3, "interval": 4000}],
    # Wave 39 : L'Invasion
    [{"enemy": "Soldier", "count": 100, "interval": 80}, {"enemy": "Berserker", "count": 10, "interval": 500}],
    
    # --- WAVE 40 : DUO DE BOSS ---
    [{"enemy": "Boss", "count": 1, "interval": 1000}, {"enemy": "MegaTesla", "count": 1, "interval": 3000}],


    # --- PHASE 5 : L'ENFER (W41-W50) ---
    # Bonne chance.

    # Wave 41 : La Totale
    [{"enemy": "GigaSplitter", "count": 1, "interval": 5000}, {"enemy": "Berserker", "count": 15, "interval": 500}],
    # Wave 42 : Mur Électrique
    [{"enemy": "Tesla", "count": 25, "interval": 400, "shield": True}],
    # Wave 43 : Tanks Immortels (Gardiens + Tanks)
    [{"enemy": "Tank", "count": 15, "interval": 1000, "shield": True}, {"enemy": "Guardian", "count": 10, "interval": 1000}],
    # Wave 44 : Division Rapide
    [{"enemy": "Super Splitter", "count": 20, "interval": 800, "shield": True}, {"enemy": "Flash", "count": 20, "interval": 400}],
    # Wave 45 : Boss Parade
    [{"enemy": "Boss", "count": 5, "interval": 2500, "shield": True}],
    # Wave 46 : Fantômes Berserk
    [{"enemy": "Ghost", "count": 40, "interval": 300, "shield": True}, {"enemy": "Berserker", "count": 10, "interval": 500}],
    # Wave 47 : Double MegaTesla
    [{"enemy": "MegaTesla", "count": 2, "interval": 4000}, {"enemy": "Guardian", "count": 10, "interval": 500}],
    # Wave 48 : Apocalypse de Slime
    [{"enemy": "Mega Splitter", "count": 12, "interval": 1500, "shield": True}],
    # Wave 49 : Le Déluge
    [
        {"enemy": "Soldier", "count": 60, "interval": 100, "shield": True},
        {"enemy": "Flash", "count": 40, "interval": 200},
        {"enemy": "Berserker", "count": 20, "interval": 300}
    ],

    # --- WAVE 50 : L'ULTIME DÉFI ---
    [
        {"enemy": "Boss", "count": 2, "interval": 1000},       # Deux sacs à PV
        {"enemy": "MegaTesla", "count": 2, "interval": 2000},  # Deux stunners
        {"enemy": "GigaSplitter", "count": 1, "interval": 3000}, # Le chaos
        {"enemy": "Guardian", "count": 10, "interval": 500},   # Les soigneurs de bouclier
        {"enemy": "Berserker", "count": 15, "interval": 400}   # Les finisseurs
    ]
]