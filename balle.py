class Balle:
    """Gère la balle : position, vitesse, collisions simples."""

    def __init__(self, canvas, scale):
        self.canvas = canvas
        self.scale = scale
        self.start_speed = 2.0
        self.max_speed = 6.0
        self.vx = self.start_speed * self.scale
        self.vy = -self.start_speed * self.scale
        self.item = None

    def creer(self):
        diam = int(25 * self.scale)
        x1 = self.canvas.winfo_width() // 2 - diam // 2
        y1 = self.canvas.winfo_height() // 2
        self.item = self.canvas.create_oval(
            x1, y1, x1 + diam, y1 + diam,
            fill="white", tags=("balle", "scene")
        )
        return self.item

    def move(self):
        self.canvas.move(self.item, self.vx, self.vy)

    def rebond_murs(self, largeur, hauteur, rotation_active):
        bx1, by1, bx2, by2 = self.canvas.coords(self.item)
        if bx1 <= 0:
            self.vx = abs(self.vx)
        if bx2 >= largeur:
            self.vx = -abs(self.vx)
        if not rotation_active:
            if by1 <= 0:
                self.vy = abs(self.vy)
        else:
            if by2 >= hauteur:
                self.vy = -abs(self.vy)
