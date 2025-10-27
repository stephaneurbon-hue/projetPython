import tkinter as tk
from briques import BriquesManager
from raquette import Raquette
from balle import Balle
from utils import set_timer, cancel_timer
from Accueil import Accueil


class InterfaceJeu:
    """Fenêtre principale du jeu."""

    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#001a33")
        self.ref_width, self.ref_height = 1600, 900
        self.scale = 1.0

        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.rotation_active = False
        self.controles_inverses = False
        self.boost_actif = False

        # Timers
        self.rotation_timer_id = None
        self.boost_timer_id = None
        self.malus_vert_timer_id = None

        # --- FRAME PRINCIPALE ---
        self.main_frame = tk.Frame(self.root, bg="#001a33")
        self.main_frame.pack(fill="both", expand=True)

        # --- HAUT : SCORE + BOUTON QUITTER ---
        top_frame = tk.Frame(self.main_frame, bg="#001a33")
        top_frame.pack(fill="x", pady=10)

        self.label_score = tk.Label(
            top_frame,
            text="Score : 0",
            font=("Arial", 20, "bold"),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(side="right", padx=20)

        self.bouton_quitter = tk.Button(
            top_frame,
            text="Quitter",
            font=("Arial", 16, "bold"),
            bg="#660000",
            fg="white",
            command=self.retour_accueil,
            relief="raised",
            width=10
        )
        self.bouton_quitter.pack(side="left", padx=20)

        # --- CANVAS DU JEU ---
        self.canvas = tk.Canvas(
            self.main_frame,
            bg="#001a33",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Objets du jeu
        self.briques_mgr = BriquesManager(self.canvas, self.scale)
        self.raquette = Raquette(self.canvas, self.scale)
        self.balle = Balle(self.canvas, self.scale)

        # Bind clavier
        self.root.bind("<Left>", lambda _: self.raquette.deplacer(-1, self.controles_inverses))
        self.root.bind("<Right>", lambda _: self.raquette.deplacer(1, self.controles_inverses))
        self.root.bind("<Configure>", self._on_resize)

        # Lancement du jeu
        self.root.after(300, self.jouer)

    # ---------- Cycle de jeu ----------
    def jouer(self):
        self._reset_timers()
        self.partie_terminee = False
        self.en_cours = True
        self.score = 0
        self.label_score.config(text="Score : 0")
        self.canvas.delete("all")

        self.briques_mgr.creer_briques()
        self.raquette.creer()
        self.balle.creer()
        self._loop_balle()

    def _loop_balle(self):
        if not self.en_cours:
            return

        self.balle.move()
        bx1, by1, bx2, by2 = self.canvas.coords(self.balle.item)
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.balle.rebond_murs(cw, ch, self.rotation_active)

        # Perte
        if not self.rotation_active and by2 >= ch:
            return self._fin("Perdu !")
        if self.rotation_active and by1 <= 0:
            return self._fin("Perdu !")

        # Collision raquette
        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raquette.item)
        if bx2 >= rx1 and bx1 <= rx2 and by2 >= ry1 and by1 <= ry2:
            self.balle.vy = -abs(self.balle.vy)

        # Collision briques
        for b in self.briques_mgr.briques[:]:
            if not self.canvas.type(b):
                continue
            x1, y1, x2, y2 = self.canvas.coords(b)
            if bx2 >= x1 and bx1 <= x2 and by2 >= y1 and by1 <= y2:
                tags = self.canvas.gettags(b)
                self.canvas.delete(b)
                self.briques_mgr.briques.remove(b)
                self.balle.vy = -self.balle.vy
                self.score += 10
                self.label_score.config(text=f"Score : {self.score}")
                if "brique_rouge" in tags:
                    self._boost()
                if "brique_verte" in tags:
                    self._malus_vert()
                if "brique_violette" in tags:
                    self._rotation()
                break

        # Gagné ?
        if not self.briques_mgr.briques:
            return self._fin("Bravo ! Vous avez gagné !")

        self.root.after(15, self._loop_balle)

    # ---------- Effets spéciaux ----------
    def _boost(self):
        if self.boost_actif:
            return
        self.boost_actif = True
        self.balle.vx *= 2
        self.balle.vy *= 2
        set_timer(self.root, "boost_timer_id", 2000, self._fin_boost, self)

    def _fin_boost(self):
        self.boost_actif = False
        self.balle.vx /= 2
        self.balle.vy /= 2

    def _malus_vert(self):
        self.raquette.ralentir_temporairement()
        cancel_timer(self.root, "malus_vert_timer_id", self)
        set_timer(self.root, "malus_vert_timer_id", 1500, self.raquette.reset_vitesse, self.raquette)

    def _rotation(self):
        if self.rotation_active:
            cancel_timer(self.root, "rotation_timer_id", self)
            set_timer(self.root, "rotation_timer_id", 10000, self._stop_rotation, self)
            return
        self.rotation_active = True
        self.controles_inverses = True
        self._flip_canvas()
        set_timer(self.root, "rotation_timer_id", 10000, self._stop_rotation, self)

    def _stop_rotation(self):
        self.rotation_active = False
        self.controles_inverses = False
        self._flip_canvas()

    def _flip_canvas(self):
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        try:
            self.canvas.scale("scene", cx, cy, -1, -1)
        except Exception:
            pass

    # ---------- Fin / Retour ----------
    def _fin(self, message):
        """Affiche message de fin + bouton Rejouer."""
        self.en_cours = False
        self._reset_timers()

        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=message,
            fill="white",
            font=("Arial", int(36 * self.scale), "bold"),
            tags=("scene"),
        )

        bouton_rejouer = tk.Button(
            self.canvas,
            text="Rejouer",
            font=("Arial", int(18 * self.scale)),
            bg="#003366",
            fg="white",
            command=self.jouer,
        )
        self.canvas.create_window(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2 + int(70 * self.scale),
            window=bouton_rejouer,
            tags=("scene"),
        )

    def retour_accueil(self):
        """Retourne à l'écran d'accueil."""
        for widget in self.root.winfo_children():
            widget.destroy()
        Accueil(self.root)

    def _reset_timers(self):
        for tid in ["rotation_timer_id", "boost_timer_id", "malus_vert_timer_id"]:
            cancel_timer(self.root, tid, self)

    def _on_resize(self, event):
        if event.width < 200 or event.height < 200:
            return
        self.scale = min(event.width / self.ref_width, event.height / self.ref_height)
        self.canvas.config(width=event.width, height=event.height)
