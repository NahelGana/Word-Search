import random
import string

# Liste de thèmes et banques de mots pour vos 224 grilles
THEMES = {
    "Animaux": [
        "CHIEN", "CHAT", "ELEPHANT", "SINGE",
        "LION", "TIGRE", "LAPIN", "OISEAU",
        "CHEVAL", "LOUP", "GAZELLE", "OURS",
        "GIRAFE", "DAUPHIN", "PINGOUIN", "ZEBRE",
        "REQUIN", "AIGLE", "PANDA", "KOALA",
        "PANTHERE", "CORBEAU", "LAMA", "RENARD"
    ],

    "Voyages": [
        "AVION", "VALISE", "PASSEPORT", "PLAGE",
        "NAVIRE", "BAGAGE", "CAMPING", "SAFARI",
        "VOYAGEUR", "GARE", "HOTEL", "ESCALE",
        "BATEAU", "ILE", "CARTE", "GUIDE",
        "SOLEIL", "CROISIERE", "VOLCAN",
        "DESERT", "MONTAGNE"
    ],

    "Histoire": [
        "ROI", "REINE", "CHATEAU", "EMPIRE",
        "GUERRE", "TRAITE", "EPOQUE", "SIECLE",
        "ARMEE", "BLASON", "CHEVALIER",
        "COURONNEMENT", "MUSEE", "ARCHIVE",
        "PYRAMIDE", "PHARAON", "ROMAN",
        "GLADIATEUR", "NAPOLEON", "REVOLUTION"
    ]
}

GRID_SIZE = 10
NUM_PUZZLES = 224
DIRECTIONS = {
    "H":  (0, 1),    # Horizontal
    "V":  (1, 0),    # Vertical
    "DD": (1, 1),    # Diagonale descendante
    "DG": (1, -1),   # Diagonale montante
}

def split_theme(theme_words):
    # Nettoyer et supprimer les doublons
    words = list(dict.fromkeys(
        word.upper().replace(" ", "")
        for word in theme_words
    ))

    # Les mots de plus de 10 lettres ne peuvent pas être placés
    # dans une grille de 10 × 10 avec les orientations actuelles.
    words = [word for word in words if 1 <= len(word) <= GRID_SIZE]

    random.shuffle(words)

    # Répartition en deux groupes distincts
    middle = (len(words) + 1) // 2

    return words[:middle], words[middle:]

def create_grid():
    return [["" for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)]

def place_word(grid, word, max_attempts=200):
    word = word.upper().replace(" ", "")

    if not word or len(word) > GRID_SIZE:
        return None

    directions = list(DIRECTIONS.values())

    for _ in range(max_attempts):
        dr, dc = random.choice(directions)

        row = random.randrange(GRID_SIZE)
        col = random.randrange(GRID_SIZE)

        end_row = row + (len(word) - 1) * dr
        end_col = col + (len(word) - 1) * dc

        # Vérifier que le mot reste dans la grille
        if not (
            0 <= end_row < GRID_SIZE
            and 0 <= end_col < GRID_SIZE
        ):
            continue

        # Vérifier que les cases sont libres ou compatibles
        if all(
            grid[row + i * dr][col + i * dc] in ("", letter)
            for i, letter in enumerate(word)
        ):
            # Placer le mot
            for i, letter in enumerate(word):
                grid[row + i * dr][col + i * dc] = letter

            # Conserver les coordonnées pour la correction
            return {
                "word": word,
                "start": (row, col),
                "direction": (dr, dc),
                "length": len(word),
            }

    return None

def fill_grid(grid, theme):
    words = list(theme)
    random.shuffle(words)

    placed_words = []

    for word in words:
        placement = place_word(grid, word)

        if placement is not None:
            placed_words.append(placement)

    # Remplir les cases restantes avec des lettres aléatoires
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == "":
                grid[row][col] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    return grid, placed_words

# Génération des 224 grilles...
#print(f"Prêt à générer {NUM_PUZZLES} grilles pour KDP !")
#grille = create_grid()
#grille = place_word(create_grid(), "Ordinateur")
#print(grille)
#for i in range(len(grille)) :
#    print(grille[i])

#grille1_words, grille2_words = split_theme(THEMES["Animaux"])

#print("Grille 1 :", grille1_words)
#print("Grille 2 :", grille2_words)

#words = THEMES["Animaux"]
#grid, corrections = fill_grid(create_grid(), words)
#for row in grid:
#    print(" ".join(row))
#print("\nMots placés :")
#for placement in corrections:
#    print(placement["word"], placement["start"])
    
theme_words = THEMES["Animaux"]
words1, words2 = split_theme(theme_words)
grid1, correction1 = fill_grid(create_grid(), words1)
grid2, correction2 = fill_grid(create_grid(), words2)
print("Mots de la grille 1 :",
      [p["word"] for p in correction1])
print("Mots de la grille 2 :",
      [p["word"] for p in correction2])

puzzle = [
    {
        "number": 1,
        "theme": "Animaux",
        "grid": grid1,
        "words": correction1,
    },
    {
        "number": 2,
        "theme": "Animaux",
        "grid": grid2,
        "words": correction2,
    },
    {
        "number": 3,
        "theme": "Voyages",
        "grid": grid3,
        "words": correction3,
    },
]