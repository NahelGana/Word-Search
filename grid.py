import random
import string

# Liste de thèmes et banques de mots pour vos 224 grilles
THEMES = {
    "Animaux": ["CHIEN", "CHAT", "ELEPHANT", "SINGE", "LION", "TIGRE", "LAPIN", "OISEAU", "CHEVAL", "LOUPS", "GAZELLE", "OURS", "GIRAFE", "DAUPHIN", "PENGOUIN", "ZEBRE", "REQUIN", "AIGLE", "PANDA", "KOALA", "PANTHERE", "CORBEAU", "LAMA", "RENARD"],
    "Voyages": ["AVION", "VALISE", "PASSEPORT", "PLAGE", "NAVIRE", "BAGAGES", "CAMPING", "SAFARI", "VOYAGEUR", "GARE", "HOTEL", "ESCALES", "BATEAU", "ILE", "CARTE", "GUIDE", "SOLEIL", "CROISIERE", "EVALUATION", "VOLCAN", "DESERT", "MONTAGNE"],
    "Histoire": ["ROI", "REINE", "CHATEAU", "EMPIRE", "GUERRE", "TRAITE", "EPOQUE", "SIECLE", "ARMEE", "BLASON", "CHEVALIER", "CORONATION", "MUSEE", "ARCHIVES", "PYRAMIDE", "PHARAON", "ROMAN", "GLADIATEUR", "NAPOLEON", "REVOLUTION"],
    "Vocabulaire": ["AMITIE", "BONHEUR", "COURAGE", "DOUCEUR", "ESPOIR", "LUMIERE", "SAGESSE", "HARMONIE", "LIBERTE", "PASSION", "SURISE", "VICTOIRE", "SOURIRE", "JARDIN", "POESIE", "AMOUR", "VERITE", "PATIENCE", "RÊVE", "SERENITE"]
}

GRID_SIZE = 10
NUM_PUZZLES = 224

def create_grid():
    return [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_word(grid, word):
    word = word.upper().replace(" ", "")
    
    # Sécurité globale : si le mot est plus grand que la grille entière
    if len(word) > GRID_SIZE:
        return None
        
    # Définition des 4 orientations autorisées
    orientations = ['H', 'V', 'DG', 'DD'] 
    random.shuffle(orientations)
    
    for ori in orientations:
        # 1. Horizontal (de gauche à droite)
        if ori == 'H':
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - len(word))
            if all(grid[row][col+i] in ('', word[i]) for i in range(len(word))):
                for i in range(len(word)):
                    grid[row][col+i] = word[i]
                return grid

        # 2. Vertical (de haut en bas)
        elif ori == 'V':
            row = random.randint(0, GRID_SIZE - len(word))
            col = random.randint(0, GRID_SIZE - 1)
            if all(grid[row+i][col] in ('', word[i]) for i in range(len(word))):
                for i in range(len(word)):
                    grid[row+i][col] = word[i]
                return grid

        # 3. Diagonale : Haut-gauche vers Bas-droit
        elif ori == 'DD':
            row = random.randint(0, GRID_SIZE - len(word))
            col = random.randint(0, GRID_SIZE - len(word))
            if all(grid[row+i][col+i] in ('', word[i]) for i in range(len(word))):
                for i in range(len(word)):
                    grid[row+i][col+i] = word[i]
                return grid

        # 4. Diagonale : Haut-droit vers Bas-gauche
        elif ori == 'DG':
            row = random.randint(0, GRID_SIZE - len(word))
            # On commence au moins à l'indice (len(word) - 1) pour ne pas sortir à gauche
            col = random.randint(len(word) - 1, GRID_SIZE - 1)
            if all(grid[row+i][col-i] in ('', word[i]) for i in range(len(word))):
                for i in range(len(word)):
                    grid[row+i][col-i] = word[i]
                return grid

    return None

# Génération des 224 grilles...
print(f"Prêt à générer {NUM_PUZZLES} grilles pour KDP !")
grille = create_grid()
grille = place_word(create_grid(), "Ordinateur")
#print(grille)
for i in range(len(grille)) :
    print(grille[i])