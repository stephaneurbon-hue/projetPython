class Raquette:
    """Contrôle la raquette du joueur."""

    def __init__(self, canvas, scale):
        self.canvas = canvas
        self.scale = scale
        self.speed_base = 25.0
        self.speed = self.speed_base * self.scale
        self.item = None

    def creer(self):
        largeur, hauteur = int(200 * self.scale), int(25 * self.scale)
        x1 = (self.canvas.winfo_width() - largeur) // 2
        y1 = self.canvas.winfo_height() - int(80 * self.scale)
        self.item = self.canvas.create_rectangle(
            x1, y1, x1 + largeur, y1 + hauteur,
            fill="white", tags=("raquette", "scene")
        )
        return self.item

    def deplacer(self, direction, inverses=False):
        """Déplace la raquette à gauche/droite."""
        sens = direction * (-1 if inverses else 1)
        dx = sens * self.speed
        rx1, _, rx2, _ = self.canvas.coords(self.item)
        cw = self.canvas.winfo_width()
        if rx1 + dx < 0:
            dx = -rx1
        if rx2 + dx > cw:
            dx = cw - rx2
        self.canvas.move(self.item, dx, 0)

    def ralentir_temporairement(self):
        """Ralentit la raquette pour le malus vert."""
        self.speed = max(8.0 * self.scale, (self.speed_base * 0.5) * self.scale)

    def reset_vitesse(self):
        """Rétablit la vitesse normale."""
        self.speed = self.speed_base * self.scale
