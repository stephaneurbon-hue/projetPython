"""
jeu.py
-------
Classe principale contenant la logique du jeu Casse-Brique.
"""

import tkinter as tk
import random


class InterfaceJeu:
    """Gère l'affichage et la logique du jeu Casse-Brique."""

    def __init__(self, root, scale):
        self.root = root
        self.scale = scale
        self.root.configure(bg="#001a33")

        # Paramètres du canvas
        self.canvas_width = int(1600 * scale)
        self.canvas_height = int(700 * scale)

        # Dimensions des éléments du jeu
        self.raquette_hauteur = int(25 * scale)
        self.balle_diametre = int(25 * scale)
        self.raquette_y = self.canvas_height - int(50 * scale)
        self.raquette_largeurs = [int(160 * scale), int(120 * scale), int(80 * scale)]

        # Indicateurs et variables de jeu
        self.raquette_etape = 0
        self.vitesse_x = int(8 * scale)
        self.vitesse_y = -int(8 * scale)
        self.vitesse_max = int(16 * scale)
        self.vitesse_increment = 0.3 * scale
        self.raquette_pas = int(80 * scale)
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False

        # États bonus/malus
        self.rotation_active = False
        self.controles_inverses = False
        self.boost_actif = False

        # Initialisation des timers
        self.animation_id = None
        self.rotation_timer_id = None
        self.boost_timer_id = None
        self.malus_vert_timer_id = None

        # Interface supérieure (score)
        top_frame = tk.Frame(root, bg="#001a33")
        top_frame.pack(fill=tk.X, pady=int(10 * scale))
        self.label_score = tk.Label(
            top_frame,
            text=f"Score : {self.score}",
            font=("Arial", int(20 * self.scale), "bold"),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(side=tk.RIGHT, padx=int(30 * scale))

        # Zone de jeu
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#001a33",
            highlightthickness=0,
        )
        self.canvas.pack(pady=int(10 * scale))

        # Bouton pour lancer la partie
        self.button_frame = tk.Frame(root, bg="#001a33")
        self.bouton_action = tk.Button(
            self.button_frame,
            text="Jouer",
            font=("Arial", int(18 * scale)),
            command=self.jouer,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_action.pack(padx=int(10 * scale), pady=int(5 * scale))

        # Création des objets du jeu
        self.briques = []
        self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))
        self.balle = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("scene",))

        # Contrôles clavier
        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        self.afficher_bouton_action("Jouer", self.jouer)

    # --------------------------------------------------------------
    # Fonctions principales du jeu
    # --------------------------------------------------------------

    def jouer(self):
        """Initialise et démarre une nouvelle partie."""
        self.reset_partie()
        self.creer_briques()
        self.masquer_bouton_action()
        self.en_cours = True
        self.deplacer_balle()

    def reset_partie(self):
        """Réinitialise les paramètres pour une nouvelle partie."""
        for timer in [self.animation_id, self.boost_timer_id, self.malus_vert_timer_id]:
            if timer:
                self.root.after_cancel(timer)

        self.canvas.delete("popup", "message")
        self.score = 0
        self.partie_terminee = False
        self.label_score.config(text=f"Score : {self.score}")
        self.mettre_a_jour_raquette(recentrer=True)
        self.positionner_balle_centre()

    def terminer_partie(self, message):
        """Met fin à la partie et affiche le message de fin."""
        self.partie_terminee = True
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=message,
            fill="white",
            font=("Arial", int(36 * self.scale), "bold"),
            tags="message",
        )
        self.afficher_bouton_action("Rejouer", self.jouer)

    # --------------------------------------------------------------
    # Gestion des briques
    # --------------------------------------------------------------

    def creer_briques(self):
        """Crée la grille de briques (avec bonus et malus)."""
        self.canvas.delete("brique")
        self.briques = []

        brique_largeur = int(150 * self.scale)
        brique_hauteur = int(30 * self.scale)
        espacement_x = int(15 * self.scale)
        espacement_y = int(10 * self.scale)
        colonnes, lignes = 9, 5

        marge_haute = int(20 * self.scale)
        largeur_total = colonnes * brique_largeur + (colonnes - 1) * espacement_x
        marge_gauche = (self.canvas_width - largeur_total) // 2

        for ligne in range(lignes):
            for col in range(colonnes):
                x1 = marge_gauche + col * (brique_largeur + espacement_x)
                y1 = marge_haute + ligne * (brique_hauteur + espacement_y)
                x2, y2 = x1 + brique_largeur, y1 + brique_hauteur
                brique = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#a3d5ff", outline="black", tags=("brique", "scene")
                )
                self.briques.append(brique)

        self.ajouter_briques_speciales()

    def ajouter_briques_speciales(self):
        """Ajoute des briques spéciales (bonus/malus)."""
        if len(self.briques) < 12:
            return
        briques_choisies = random.sample(self.briques, 12)
        for i, brique in enumerate(briques_choisies):
            if i < 5:
                self.canvas.itemconfig(brique, fill="#ff8c8c", tags=("brique", "brique_rouge", "scene"))
            elif i < 7:
                self.canvas.itemconfig(brique, fill="#d5a6ff", tags=("brique", "brique_violette", "scene"))
            else:
                self.canvas.itemconfig(brique, fill="#b3ffcc", tags=("brique", "brique_verte", "scene"))

    # --------------------------------------------------------------
    # Gestion de la balle
    # --------------------------------------------------------------

    def deplacer_balle(self):
        """Anime la balle, gère les collisions et la logique du jeu."""
        if self.partie_terminee or not self.en_cours:
            return

        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        # Rebonds sur les bords
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.vitesse_x = -self.vitesse_x
        if pos[1] <= 0:
            self.vitesse_y = -self.vitesse_y

        # Collision avec la raquette
        raquette_pos = self.canvas.coords(self.raquette)
        if raquette_pos and pos[3] >= raquette_pos[1] and pos[2] >= raquette_pos[0] and pos[0] <= raquette_pos[2]:
            self.vitesse_y = -self.vitesse_y

        # Collision avec les briques
        for brique in self.briques[:]:
            brique_pos = self.canvas.coords(brique)
            if brique_pos and pos[2] >= brique_pos[0] and pos[0] <= brique_pos[2] and pos[3] >= brique_pos[1] and pos[1] <= brique_pos[3]:
                tags = self.canvas.gettags(brique)
                self.canvas.delete(brique)
                self.briques.remove(brique)
                self.vitesse_y = -self.vitesse_y
                self.score += 10
                self.label_score.config(text=f"Score : {self.score}")

                # Effets spéciaux
                if "brique_violette" in tags:
                    self.activer_rotation()
                if "brique_rouge" in tags:
                    self.activer_boost_rouge()
                if "brique_verte" in tags:
                    self.activer_malus_vert()

                if not self.briques:
                    self.terminer_partie("Bravo ! Vous avez gagné !")
                break

        # Perte de balle
        if pos[3] >= self.canvas_height:
            self.reduire_raquette()
            self.positionner_balle_centre()

        self.animation_id = self.root.after(20, self.deplacer_balle)

    # --------------------------------------------------------------
    # Autres méthodes utilitaires (boost, rotation, raquette)
    # --------------------------------------------------------------
    def activer_boost_rouge(self):
        """Active un boost temporaire de vitesse."""
        if self.boost_actif:
            return
        self.boost_actif = True
        self.vitesse_x *= 2
        self.vitesse_y *= 2
        self.boost_timer_id = self.root.after(2000, self.fin_boost_rouge)

    def fin_boost_rouge(self):
        self.boost_actif = False
        self.vitesse_x //= 2
        self.vitesse_y //= 2

    def activer_malus_vert(self):
        """Réduit la vitesse de la raquette temporairement."""
        self.raquette_pas = int(40 * self.scale)
        if self.malus_vert_timer_id:
            self.root.after_cancel(self.malus_vert_timer_id)
        self.malus_vert_timer_id = self.root.after(3000, self.fin_malus_vert)

    def fin_malus_vert(self):
        self.raquette_pas = int(80 * self.scale)

    def activer_rotation(self):
        """Inverse l’écran temporairement."""
        if self.rotation_active:
            return
        self.rotation_active = True
        cx, cy = self.canvas_width / 2, self.canvas_height / 2
        self.canvas.scale("scene", cx, cy, -1, -1)
        self.rotation_timer_id = self.root.after(10000, self.desactiver_rotation)

    def desactiver_rotation(self):
        """Rétablit la vue normale."""
        if not self.rotation_active:
            return
        cx, cy = self.canvas_width / 2, self.canvas_height / 2
        self.canvas.scale("scene", cx, cy, -1, -1)
        self.rotation_active = False

    def positionner_balle_centre(self):
        """Replace la balle au centre de l’écran."""
        rayon = self.balle_diametre / 2
        self.canvas.coords(
            self.balle,
            self.canvas_width / 2 - rayon,
            self.raquette_y - 60,
            self.canvas_width / 2 + rayon,
            self.raquette_y - 60 + self.balle_diametre,
        )

    def afficher_bouton_action(self, texte, commande):
        """Affiche le bouton d’action (Jouer / Rejouer)."""
        self.bouton_action.config(text=texte, command=commande)
        self.button_frame.pack(pady=int(15 * self.scale))

    def masquer_bouton_action(self):
        """Cache le bouton d’action."""
        self.button_frame.pack_forget()

    def mettre_a_jour_raquette(self, recentrer=False):
        """Met à jour la position et la taille de la raquette."""
        largeur = self.raquette_largeurs[self.raquette_etape]
        x_centre = self.canvas_width / 2
        x1, x2 = x_centre - largeur / 2, x_centre + largeur / 2
        y1, y2 = self.raquette_y, self.raquette_y + self.raquette_hauteur
        self.canvas.coords(self.raquette, x1, y1, x2, y2)

    def reduire_raquette(self):
        """Réduit la taille de la raquette après une erreur."""
        self.raquette_etape += 1
        if self.raquette_etape >= len(self.raquette_largeurs):
            self.terminer_partie("Perdu !")
