import random


class BriquesManager:
    """Gère la création et les propriétés des briques."""

    def __init__(self, canvas, scale):
        self.canvas = canvas
        self.scale = scale
        self.briques = []

    def creer_briques(self):
        """Crée les briques du niveau avec quelques briques spéciales."""
        colonnes, lignes = 9, 3
        brique_largeur = int(150 * self.scale)
        brique_hauteur = int(30 * self.scale)
        esp_x, esp_y = int(15 * self.scale), int(12 * self.scale)
        marge_haute = int(60 * self.scale)

        cw = max(1, self.canvas.winfo_width())
        largeur_total = colonnes * brique_largeur + (colonnes - 1) * esp_x
        marge_gauche = (cw - largeur_total) // 2

        ids = []
        for li in range(lignes):
            for co in range(colonnes):
                x1 = marge_gauche + co * (brique_largeur + esp_x)
                y1 = marge_haute + li * (brique_hauteur + esp_y)
                x2, y2 = x1 + brique_largeur, y1 + brique_hauteur
                bid = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#a3d5ff",
                    outline="black",
                    tags=("brique", "scene"),
                )
                ids.append(bid)

        # Ajout des briques spéciales
        if len(ids) >= 8:
            choix = random.sample(ids, 8)
            rouges, violettes, vertes = choix[:3], choix[3:5], choix[5:8]
            for r in rouges:
                self.canvas.itemconfig(r, fill="#ff8c8c")
                self.canvas.addtag_withtag("brique_rouge", r)
            for v in violettes:
                self.canvas.itemconfig(v, fill="#d5a6ff")
                self.canvas.addtag_withtag("brique_violette", v)
            for g in vertes:
                self.canvas.itemconfig(g, fill="#b3ffcc")
                self.canvas.addtag_withtag("brique_verte", g)

        self.briques = ids
        return ids
