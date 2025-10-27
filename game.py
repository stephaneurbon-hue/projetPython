"""
Casse-Brique – Logique principale du jeu
Auteur : Stéphane Urbon & Rayane Zidane
"""

import tkinter as tk
import random
from utils import set_timer, cancel_timer


class GameApp:
    def __init__(self, root, scale=1.0):
        self.root = root
        self.scale = scale
        self.root.configure(bg="#001a33")

        # Canvas principal
        self.canvas = tk.Canvas(
            root, bg="#001a33", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Score
        self.score = 0
        self.label_score = tk.Label(
            root,
            text="Score : 0",
            font=("Arial", int(20 * self.scale), "bold"),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(anchor="ne", padx=20, pady=10)

        # Objets du jeu
        self.balle = None
        self.raquette = None
        self.briques = []

        # Paramètres du jeu
        self.start_speed = 2.5 * self.scale
        self.max_speed = 6.0 * self.scale
        self.vx = self.start_speed
        self.vy = -self.start_speed

        self.raquette_speed = 25 * self.scale
        self.en_cours = True
        self.rotation_active = False
        self.controles_inverses = False

        # Timers
        self.rotation_timer_id = None
        self.boost_timer_id = None
        self.malus_timer_id = None

        # Bind des touches
        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)
        self.root.bind("<Configure>", self.redimensionner)

        # Démarre la partie
        self.root.after(200, self.start)

    # --- Initialisation ---
    def start(self):
        self.canvas.delete("all")
        self.score = 0
        self.label_score.config(text="Score : 0")
        self.creer_briques()
        self.creer_raquette()
        self.creer_balle()
        self.deplacer_balle()

    # --- Responsive ---
    def redimensionner(self, event):
        if event.width < 200 or event.height < 200:
            return
        self.canvas.config(width=event.width, height=event.height)
        self.scale = min(event.width / 1600, event.height / 900)

    # --- Création des objets ---
    def creer_briques(self):
        self.briques.clear()
        cols, rows = 9, 3
        bw, bh = int(150 * self.scale), int(30 * self.scale)
        esp_x, esp_y = int(15 * self.scale), int(12 * self.scale)
        marge_haute = int(60 * self.scale)
        cw = max(1, self.canvas.winfo_width())
        total_w = cols * bw + (cols - 1) * esp_x
        marge_gauche = (cw - total_w) // 2

        for r in range(rows):
            for c in range(cols):
                x1 = marge_gauche + c * (bw + esp_x)
                y1 = marge_haute + r * (bh + esp_y)
                x2, y2 = x1 + bw, y1 + bh
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#a3d5ff", outline="black", tags="brique"
                )
                self.briques.append(rect)

        # Briques spéciales
        if len(self.briques) >= 8:
            choix = random.sample(self.briques, 8)
            rouges, violettes, vertes = choix[:3], choix[3:5], choix[5:8]
            for r in rouges:
                self.canvas.itemconfig(r, fill="#ff8c8c", tags=("brique", "rouge"))
            for v in violettes:
                self.canvas.itemconfig(v, fill="#d5a6ff", tags=("brique", "violette"))
            for g in vertes:
                self.canvas.itemconfig(g, fill="#b3ffcc", tags=("brique", "verte"))

    def creer_raquette(self):
        largeur = int(200 * self.scale)
        hauteur = int(25 * self.scale)
        y = self.canvas.winfo_height() - int(80 * self.scale)
        self.raquette = self.canvas.create_rectangle(
            (self.canvas.winfo_width() - largeur) // 2,
            y,
            (self.canvas.winfo_width() + largeur) // 2,
            y + hauteur,
            fill="white",
        )

    def creer_balle(self):
        d = int(25 * self.scale)
        x = self.canvas.winfo_width() // 2 - d // 2
        y = self.canvas.winfo_height() // 2
        self.balle = self.canvas.create_oval(x, y, x + d, y + d, fill="white")

    # --- Déplacements ---
    def deplacer_balle(self):
        if not self.en_cours:
            return

        self.canvas.move(self.balle, self.vx, self.vy)
        bx1, by1, bx2, by2 = self.canvas.coords(self.balle)
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()

        # rebonds
        if bx1 <= 0:
            self.vx = abs(self.vx)
        if bx2 >= cw:
            self.vx = -abs(self.vx)
        if by1 <= 0:
            self.vy = abs(self.vy)
        if by2 >= ch:
            self.fin_partie("Perdu !")
            return

        # raquette
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raquette)
        if bx2 >= rx1 and bx1 <= rx2 and by2 >= ry1 and by1 <= ry2:
            self.vy = -abs(self.vy)
            delta = ((bx1 + bx2) / 2 - (rx1 + rx2) / 2) / (rx2 - rx1)
            self.vx += 0.6 * delta

        # collisions briques
        for b in self.briques[:]:
            if not self.canvas.type(b):
                continue
            x1, y1, x2, y2 = self.canvas.coords(b)
            if bx2 >= x1 and bx1 <= x2 and by2 >= y1 and by1 <= y2:
                tags = self.canvas.gettags(b)
                self.canvas.delete(b)
                self.briques.remove(b)
                self.vy = -self.vy
                self.score += 10
                self.label_score.config(text=f"Score : {self.score}")
                if "rouge" in tags:
                    self.boost_rouge()
                elif "violette" in tags:
                    self.rotation()
                elif "verte" in tags:
                    self.malus_vert()
                break

        if not self.briques:
            self.fin_partie("Bravo ! Vous avez gagné !")
            return

        self.root.after(15, self.deplacer_balle)

    # --- Déplacement raquette ---
    def deplacer_gauche(self, _):
        sens = -1 if not self.controles_inverses else 1
        self.move_pad(sens)

    def deplacer_droite(self, _):
        sens = 1 if not self.controles_inverses else -1
        self.move_pad(sens)

    def move_pad(self, direction):
        dx = direction * self.raquette_speed
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raquette)
        cw = self.canvas.winfo_width()
        if rx1 + dx < 0:
            dx = -rx1
        if rx2 + dx > cw:
            dx = cw - rx2
        self.canvas.move(self.raquette, dx, 0)

    # --- Effets spéciaux ---
    def boost_rouge(self):
        self.vx *= 1.8
        self.vy *= 1.8
        cancel_timer(self.root, "boost_timer_id", self)
        set_timer(self.root, "boost_timer_id", 2000, self.fin_boost, self)

    def fin_boost(self):
        self.vx = max(min(self.vx, self.max_speed), -self.max_speed)
        self.vy = max(min(self.vy, self.max_speed), -self.max_speed)

    def malus_vert(self):
        self.raquette_speed = max(10 * self.scale, self.raquette_speed / 2)
        cancel_timer(self.root, "malus_timer_id", self)
        set_timer(self.root, "malus_timer_id", 1500, self.fin_malus, self)

    def fin_malus(self):
        self.raquette_speed = 25 * self.scale

    def rotation(self):
        if self.rotation_active:
            cancel_timer(self.root, "rotation_timer_id", self)
            set_timer(self.root, "rotation_timer_id", 10000, self.fin_rotation, self)
            return
        self.rotation_active = True
        self.controles_inverses = True
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.canvas.scale("all", cx, cy, -1, -1)
        set_timer(self.root, "rotation_timer_id", 10000, self.fin_rotation, self)

    def fin_rotation(self):
        self.rotation_active = False
        self.controles_inverses = False
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.canvas.scale("all", cx, cy, -1, -1)

    # --- Fin de partie ---
    def fin_partie(self, message):
        self.en_cours = False
        cancel_timer(self.root, "boost_timer_id", self)
        cancel_timer(self.root, "malus_timer_id", self)
        cancel_timer(self.root, "rotation_timer_id", self)
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=message,
            fill="white",
            font=("Arial", int(36 * self.scale), "bold"),
        )
        bouton = tk.Button(
            self.canvas,
            text="Rejouer",
            font=("Arial", int(20 * self.scale)),
            bg="#004080",
            fg="white",
            command=self.start,
        )
        quitter = tk.Button(
            self.canvas,
            text="Quitter",
            font=("Arial", int(20 * self.scale)),
            bg="#660000",
            fg="white",
            command=self.root.destroy,
        )
        self.canvas.create_window(
            self.canvas.winfo_width() // 2 - 100,
            self.canvas.winfo_height() // 2 + 60,
            window=bouton,
        )
        self.canvas.create_window(
            self.canvas.winfo_width() // 2 + 100,
            self.canvas.winfo_height() // 2 + 60,
            window=quitter,
        )
