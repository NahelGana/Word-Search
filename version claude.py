from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black

from grid import generate_all_puzzles, GRID_SIZE

PAGE_W, PAGE_H = letter  # 8.5 x 11 pouces (adapte au format KDP choisi)


# ---------------------------------------------------------------
# Dessin d'une grille (avec ou sans correction)
# ---------------------------------------------------------------
def draw_grid(c, puzzle, x, y, cell, show_solution=False, font_size=None):
    """
    (x, y) = coin HAUT-GAUCHE de la grille.
    show_solution=True -> chaque mot trouvé est surligné par une capsule.
    """
    font_size = font_size or cell * 0.55
    size = GRID_SIZE * cell

    # 1) Surbrillance : dessinée AVANT les lettres pour rester derrière
    if show_solution:
        c.saveState()
        c.setLineCap(1)                       # bouts arrondis = effet capsule
        c.setStrokeColor(Color(0.55, 0.55, 0.55, alpha=0.45))  # gris (impression N&B)
        # Pour de la couleur : Color(1, 0.85, 0, alpha=0.5)  (jaune surligneur)
        c.setLineWidth(cell * 0.75)
        for p in puzzle["words"]:
            r, col = p["start"]
            dr, dc = p["direction"]
            n = p["length"] - 1
            # centres de la première et de la dernière lettre
            x1 = x + (col + 0.5) * cell
            y1 = y - (r + 0.5) * cell
            x2 = x + (col + dc * n + 0.5) * cell
            y2 = y - (r + dr * n + 0.5) * cell
            c.line(x1, y1, x2, y2)
        c.restoreState()

    # 2) Cadre de la grille
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.rect(x, y - size, size, size)

    # 3) Lettres
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", font_size)
    for r in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            letter_ = puzzle["grid"][r][col]
            cx = x + (col + 0.5) * cell
            cy = y - (r + 0.5) * cell - font_size * 0.35
            c.drawCentredString(cx, cy, letter_)


# ---------------------------------------------------------------
# Pages de grilles (début du livre) : 1 grille par page
# ---------------------------------------------------------------
def puzzle_page(c, puzzle):
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 1 * inch,
                        f"Grille n°{puzzle['number']} - {puzzle['theme']}")

    cell = 0.55 * inch
    gx = (PAGE_W - GRID_SIZE * cell) / 2
    draw_grid(c, puzzle, gx, PAGE_H - 1.6 * inch, cell)

    # Liste des mots à trouver, sur 3 colonnes
    words = sorted(p["word"] for p in puzzle["words"])
    c.setFont("Helvetica", 12)
    top = PAGE_H - 1.6 * inch - GRID_SIZE * cell - 0.5 * inch
    for i, w in enumerate(words):
        col, row = i % 3, i // 3
        c.drawString(1.5 * inch + col * 2 * inch, top - row * 0.28 * inch, w)

    c.showPage()


# ---------------------------------------------------------------
# Pages de corrections (fin du livre) : 6 grilles par page (2 x 3)
# ---------------------------------------------------------------
def solution_pages(c, puzzles, per_row=2, per_col=3):
    per_page = per_row * per_col
    cell = 0.27 * inch
    grid_w = GRID_SIZE * cell
    margin_x = (PAGE_W - per_row * grid_w) / (per_row + 1)
    row_h = (PAGE_H - 1.5 * inch) / per_col

    for start in range(0, len(puzzles), per_page):
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(PAGE_W / 2, PAGE_H - 0.8 * inch, "Corrections")

        for k, puzzle in enumerate(puzzles[start:start + per_page]):
            r, col = divmod(k, per_row)
            x = margin_x + col * (grid_w + margin_x)
            y = PAGE_H - 1.5 * inch - r * row_h

            c.setFont("Helvetica-Bold", 10)
            c.drawString(x, y + 6, f"Grille {puzzle['number']} - {puzzle['theme']}")
            draw_grid(c, puzzle, x, y - 4, cell, show_solution=True)

        c.showPage()


def build_pdf(filename="livre_mots_meles.pdf"):
    puzzles = generate_all_puzzles()
    c = canvas.Canvas(filename, pagesize=letter)

    for puzzle in puzzles:        # début du livre : les grilles
        puzzle_page(c, puzzle)

    solution_pages(c, puzzles)    # fin du livre : les corrections

    c.save()
    print(f"{filename} créé : {len(puzzles)} grilles + corrections")


if __name__ == "__main__":
    build_pdf()
