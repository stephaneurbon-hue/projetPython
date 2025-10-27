"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Jeu Casse-Brique (version responsive, contrôle arcade).
Ce module gère la partie principale du jeu :
- affichage des briques, raquette, balle
- gestion des collisions, effets spéciaux et vitesses
- interface responsive pour tous les écrans
"""

import tkinter as tk
import random


class InterfaceJeu:
    """
    Classe principale représentant le jeu Casse-Brique.
    Elle gère :
      - le canvas de jeu
      - la balle, la raquette, les briques
      - les collisions et effets (bonus/malus)
      - la rotation de l’écran
      - l’affichage du score et des messages
    """

    # ----------------------------------------------------------------------
    # Initialisation
    # ----------------------------------------------------------------------
    def __init__(self, root, scale):
        """Initialise l’interface de jeu avec tous les paramètres et objets."""
        self.root = root
        self.scale = scale
        self.root.configure(bg="#001a33")

        # --- Dimensions générales ---
        self.canvas_width = int(1600 * scale)
        self.canvas_height = int(900 * scale)
        self.raquette_hauteur = int(25 * scale)
        self.balle_diametre = int(25 * scale)
        self.raquette_y = self.canvas_height - int(15 * scale)

        # --- Raquette ---
        self.raquette_largeurs = [int(260 * scale), int(200 * scale), int(140 * scale)]
        self.raquette_etape = 0
        self.hitbox_pad_x = int(10 * self.scale)  # marges invisibles autour de la raquette
        self.hitbox_pad_y = int(6 * self.scale)

        # --- Balle ---
        self.vitesse_x = int(6 * scale)
        self.vitesse_y = -int(6 * scale)
        self.vitesse_max = int(9 * scale)
        self.vitesse_increment = 0.15 * scale

        # --- Déplacement raquette ---
        self.raquette_pas = int(80 * scale)
        self.vitesse_raquette_coef = 0.15  # utilisé pour le déplacement continu

        # --- États du jeu ---
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False

        # --- Gestion des timers ---
        self.animation_id = None
        self.raquette_move_id = None
        self.rotation_active = False
        self.rotation_timer_id = None
        self.boost_actif = False
        self.boost_timer_id = None
        self.malus_vert_timer_id = None
        self.message_timer_id = None

        # --- Contrôles ---
        self.controles_inverses = False
        self.direction_raquette = 0  # -1 gauche, 1 droite

        # --- Files et piles pour bonus/affichage ---
        self.pile_vitesses = []  # stocke les vitesses pendant boost
        self.file_messages = []  # stocke les messages à afficher à l’écran

        # ------------------------------------------------------------------
        # Interface graphique
        # ------------------------------------------------------------------
        top_frame = tk.Frame(self.root, bg="#001a33")
        top_frame.pack(fill=tk.X, pady=int(10 * scale))

        self.label_score = tk.Label(
            top_frame,
            text=f"Score : {self.score}",
            font=("Arial", int(20 * self.scale), "bold"),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(side=tk.RIGHT, padx=int(30 * self.scale))

        # Canvas principal
        self.canvas = tk.Canvas(
            self.root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#001a33",
            highlightthickness=0,
        )
        self.canvas.pack(pady=int(10 * scale))

        # Boutons de fin de partie (cachés pendant le jeu)
        self._creer_boutons_fin()

        # Objets de jeu
        self.briques = []
        self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))
        self.balle = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("scene",))

        # Contrôles clavier
        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        # Lancement du jeu
        self.jouer()

    # ----------------------------------------------------------------------
    # Création et réinitialisation
    # ----------------------------------------------------------------------
    def _creer_boutons_fin(self):
        """Crée les boutons Rejouer et Quitter dans le canvas."""
        self.button_frame = tk.Frame(self.canvas, bg="#001a33")

        self.bouton_action = tk.Button(
            self.button_frame,
            text="Rejouer",
            font=("Arial", int(18 * self.scale)),
            command=self.jouer,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_action.pack(side=tk.LEFT, padx=int(10 * self.scale), pady=int(5 * self.scale))

        self.bouton_quitter_ingame = tk.Button(
            self.button_frame,
            text="Quitter",
            font=("Arial", int(18 * self.scale)),
            command=self.root.destroy,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_quitter_ingame.pack(side=tk.LEFT, padx=int(10 * self.scale), pady=int(5 * self.scale))

        self.button_window = self.canvas.create_window(
            self.canvas_width // 2,
            self.canvas_height - int(35 * self.scale),
            window=self.button_frame,
            anchor="s"
        )
        self.canvas.itemconfigure(self.button_window, state="hidden")

    def creer_briques(self):
        """Crée les briques du niveau et leurs couleurs spéciales."""
        self.canvas.delete("brique")
        self.briques = []

        brique_largeur = int(150 * self.scale)
        brique_hauteur = int(30 * self.scale)
        espacement_x = int(15 * self.scale)
        espacement_y = int(12 * self.scale)
        colonnes = 9
        lignes = 4
        marge_haute = 0

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

        self.briques_totales = len(self.briques)

        # Briques spéciales (3 rouges, 2 violettes, 3 vertes)
        if len(self.briques) >= 8:
            choix = random.sample(self.briques, 8)
            rouges, violettes, vertes = choix[:3], choix[3:5], choix[5:8]
            for b in rouges:
                self.canvas.itemconfig(b, fill="#ff8c8c", tags=("brique", "brique_rouge", "scene"))
            for b in violettes:
                self.canvas.itemconfig(b, fill="#d5a6ff", tags=("brique", "brique_violette", "scene"))
            for b in vertes:
                self.canvas.itemconfig(b, fill="#b3ffcc", tags=("brique", "brique_verte", "scene"))

        # Bornes de la zone briques (pour bloquer les couloirs latéraux)
        self.zone_brique_x1 = marge_gauche
        self.zone_brique_x2 = marge_gauche + largeur_total
        self.zone_brique_y2 = marge_haute + lignes * brique_hauteur + (lignes - 1) * espacement_y

    # ----------------------------------------------------------------------
    # Cycle de jeu principal
    # ----------------------------------------------------------------------
    def jouer(self):
        """Lance une nouvelle partie."""
        self.desactiver_rotation(force=True)
        self.reset_partie()
        self.creer_briques()
        self.masquer_bouton_action()
        self.partie_terminee = False
        self.en_cours = True
        self.canvas.focus_set()

        # Raquette bouge en continu (droite par défaut)
        self.direction_raquette = 1
        self.mouvement_raquette()

        self.deplacer_balle()

    def reset_partie(self):
        """Réinitialise les paramètres et les timers avant une partie."""
        # Annule tous les timers actifs
        for attr in ["animation_id", "raquette_move_id", "boost_timer_id",
                     "malus_vert_timer_id", "rotation_timer_id", "message_timer_id"]:
            val = getattr(self, attr)
            if val is not None:
                self.root.after_cancel(val)
                setattr(self, attr, None)

        # Nettoyage UI/messages
        self.canvas.delete("popup")
        self.canvas.delete("message")
        self.file_messages.clear()
        self.pile_vitesses.clear()

        # États et UI
        self.score = 0
        self.label_score.config(text=f"Score : {self.score}")
        self.raquette_pas = int(80 * self.scale)
        self.raquette_etape = 0
        self.controles_inverses = False
        self.direction_raquette = 0
        self.partie_terminee = False
        self.en_cours = False

        # Réinitialisation des objets
        if self.raquette is None:
            self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))
        self.mettre_a_jour_raquette(recentrer=True)
        self.positionner_balle_centre()

        # Vitesse de départ 
        self.vitesse_x = int(6 * self.scale)
        self.vitesse_y = -int(6 * self.scale)

    def terminer_partie(self, message):
        """Arrête la partie et affiche le message + les boutons Rejouer/Quitter."""
        self.partie_terminee = True
        self.en_cours = False

        # Annule timers
        for attr in ["animation_id", "raquette_move_id", "boost_timer_id",
                     "malus_vert_timer_id", "rotation_timer_id", "message_timer_id"]:
            val = getattr(self, attr)
            if val is not None:
                self.root.after_cancel(val)
                setattr(self, attr, None)

        # UI fin
        self.canvas.delete("popup")
        self.raquette_pas = int(80 * self.scale)
        self.canvas.delete("message")
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=message,
            fill="white",
            font=("Arial", int(36 * self.scale), "bold"),
            tags="message",
        )
        self.afficher_bouton_action("Rejouer", self.jouer)

    # ----------------------------------------------------------------------
    # UI boutons fin de partie
    # ----------------------------------------------------------------------
    def afficher_bouton_action(self, texte, commande):
        """Affiche le bouton d’action (Rejouer) et la barre de boutons."""
        self.bouton_action.config(text=texte, command=commande, state=tk.NORMAL)
        self.canvas.itemconfigure(self.button_window, state="normal")

    def masquer_bouton_action(self):
        """Cache la barre de boutons de fin de partie."""
        self.canvas.itemconfigure(self.button_window, state="hidden")

    # ----------------------------------------------------------------------
    # Mouvement de la balle et collisions
    # ----------------------------------------------------------------------
    def deplacer_balle(self):
        """Met à jour la position de la balle, gère les rebonds et collisions."""
        if self.partie_terminee or not self.en_cours:
            return

        # Déplacement
        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        bx1, by1, bx2, by2 = self.canvas.coords(self.balle)

        # Rebonds horizontaux avec “murs” alignés sur la zone briques
        pad = self.balle_diametre // 3
        if by1 <= getattr(self, "zone_brique_y2", 0) + pad:
            left_wall = max(0, getattr(self, "zone_brique_x1", 0) - pad)
            right_wall = min(self.canvas_width, getattr(self, "zone_brique_x2", self.canvas_width) + pad)
        else:
            left_wall, right_wall = 0, self.canvas_width

        if bx1 <= left_wall:
            self.vitesse_x = abs(self.vitesse_x)
            self.canvas.move(self.balle, left_wall - bx1, 0)
            bx1, by1, bx2, by2 = self.canvas.coords(self.balle)
        elif bx2 >= right_wall:
            self.vitesse_x = -abs(self.vitesse_x)
            self.canvas.move(self.balle, right_wall - bx2, 0)
            bx1, by1, bx2, by2 = self.canvas.coords(self.balle)

        # Rebonds haut/bas (selon rotation)
        if not self.rotation_active:
            if by1 <= 0:
                self.vitesse_y = -self.vitesse_y
        else:
            if by2 >= self.canvas_height:
                self.vitesse_y = -self.vitesse_y

        # Collision raquette : hitbox élargie pour eviter le probleme de collision interne expliqué dans le readme 
        if self.raquette is not None:
            rx1, ry1, rx2, ry2 = self.canvas.coords(self.raquette)
            hx1 = rx1 - self.hitbox_pad_x
            hy1 = ry1 - self.hitbox_pad_y
            hx2 = rx2 + self.hitbox_pad_x
            hy2 = ry2 + self.hitbox_pad_y

            if not self.rotation_active:
                collision = (
                    self.vitesse_y > 0 and
                    bx2 >= hx1 and bx1 <= hx2 and
                    by2 >= hy1 and by1 <= ry1
                )
            else:
                collision = (
                    self.vitesse_y < 0 and
                    bx2 >= hx1 and bx1 <= hx2 and
                    by1 <= hy2 and by2 >= ry2
                )

            if collision:
                self.vitesse_y = -self.vitesse_y
                # recoller la balle au bord de la raquette visible
                cx = (bx1 + bx2) / 2
                r = self.balle_diametre / 2
                if not self.rotation_active:
                    y2 = ry1 - 1
                    y1 = y2 - 2 * r
                else:
                    y1 = ry2 + 1
                    y2 = y1 + 2 * r
                self.canvas.coords(self.balle, int(cx - r), int(y1), int(cx + r), int(y2))
                bx1, by1, bx2, by2 = self.canvas.coords(self.balle)

        # Collision briques
        for brique in self.briques[:]:
            x1, y1, x2, y2 = self.canvas.coords(brique)
            if bx2 >= x1 and bx1 <= x2 and by2 >= y1 and by1 <= y2:
                tags = self.canvas.gettags(brique)
                self.canvas.delete(brique)
                self.briques.remove(brique)
                self.vitesse_y = -self.vitesse_y
                self.score += 10
                self.label_score.config(text=f"Score : {self.score}")

                if not self.boost_actif:
                    self.ajuster_vitesse()
                if "brique_violette" in tags:
                    self.activer_rotation()
                if "brique_rouge" in tags:
                    self.activer_boost_rouge()
                if "brique_verte" in tags:
                    self.activer_malus_vert()

                if not self.briques:
                    self.terminer_partie("Bravo ! Vous avez gagné !")
                    return
                break

        # Perte "vie"
        if not self.rotation_active:
            if by2 >= self.canvas_height:
                self.positionner_balle_centre()
                self.vitesse_y = -abs(self.vitesse_y)
                self.reduire_raquette()
        else:
            if by1 <= 0:
                self.positionner_balle_centre()
                self.vitesse_y = abs(self.vitesse_y)
                self.reduire_raquette()

        self.animation_id = self.root.after(15, self.deplacer_balle)

    # ----------------------------------------------------------------------
    # Mouvement de la raquette (continu façon arcade)
    # ----------------------------------------------------------------------
    def mouvement_raquette(self):
        """Fait bouger la raquette en continu, avec rebond automatique sur les bords."""
        if self.partie_terminee or not self.en_cours or self.raquette is None:
            return

        rx1, ry1, rx2, ry2 = self.canvas.coords(self.raquette)
        vitesse = max(1, int(self.raquette_pas * self.vitesse_raquette_coef))
        d = vitesse * (-1 if self.controles_inverses else 1) * self.direction_raquette

        if self.direction_raquette != 0:
            if rx1 + d < 0:
                d = -rx1
                self.direction_raquette = 1 if not self.controles_inverses else -1
            elif rx2 + d > self.canvas_width:
                d = self.canvas_width - rx2
                self.direction_raquette = -1 if not self.controles_inverses else 1
            self.canvas.move(self.raquette, d, 0)

        self.raquette_move_id = self.root.after(20, self.mouvement_raquette)

    # ----------------------------------------------------------------------
    # Gestion des bonus / malus
    # ----------------------------------------------------------------------
    def activer_boost_rouge(self):
        """Active un boost de vitesse temporaire (brique rouge)."""
        if self.boost_actif:
            return
        self.boost_actif = True
        self.push_message("Balle à grande vitesse !")

        # Sauvegarde la vitesse actuelle
        self.pile_vitesses.append((abs(self.vitesse_x), abs(self.vitesse_y)))

        # Applique la vitesse max
        self.vitesse_x = self.vitesse_max if self.vitesse_x > 0 else -self.vitesse_max
        self.vitesse_y = self.vitesse_max if self.vitesse_y > 0 else -self.vitesse_max

        # Fin du boost après 2 secondes
        self.boost_timer_id = self.root.after(2000, self.fin_boost_rouge)

    def fin_boost_rouge(self):
        """Désactive le boost rouge et restaure la vitesse précédente."""
        self.boost_actif = False
        self.boost_timer_id = None
        if self.pile_vitesses:
            self.pile_vitesses.pop()
        self.ajuster_vitesse()

    def activer_malus_vert(self):
        """Ralentit temporairement la raquette (brique verte)."""
        self.push_message("Raquette lourde !")
        self.raquette_pas = int(40 * self.scale)
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
        self.malus_vert_timer_id = self.root.after(1500, self.fin_malus_vert)

    def fin_malus_vert(self):
        """Rétablit la vitesse normale de la raquette après le malus vert."""
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        self.raquette_pas = int(80 * self.scale)

    def activer_rotation(self):
        """Inverse l’écran et les contrôles (brique violette)."""
        if self.rotation_active:
            self.desactiver_rotation()
            return

        self.rotation_active = True
        self.push_message("Plateau inversé !")
        self.controles_inverses = True

        cx = self.canvas_width / 2
        cy = self.canvas_height / 2

        # Inversion horizontale/verticale autour du centre
        self.canvas.scale("scene", cx, cy, -1, -1)

        # Désactivation automatique après 10 secondes
        if self.rotation_timer_id is not None:
            self.root.after_cancel(self.rotation_timer_id)
        self.rotation_timer_id = self.root.after(10000, self.desactiver_rotation)

    def desactiver_rotation(self, force=False):
        """Rétablit l’affichage normal après une rotation."""
        if not self.rotation_active and not force:
            return
        if self.rotation_timer_id is not None:
            self.root.after_cancel(self.rotation_timer_id)
            self.rotation_timer_id = None

        if self.rotation_active:
            cx = self.canvas_width / 2
            cy = self.canvas_height / 2
            self.canvas.scale("scene", cx, cy, -1, -1)

        self.rotation_active = False
        self.controles_inverses = False
        self.mettre_a_jour_raquette(recentrer=True)

    # ----------------------------------------------------------------------
    # Ajustement des vitesses
    # ----------------------------------------------------------------------
    def ajuster_vitesse(self):
        """Ajuste la vitesse de la balle en fonction du nombre de briques restantes."""
        nb_briques_restantes = len(self.briques)
        if nb_briques_restantes <= 15:
            vitesse_cible = self.vitesse_max
        else:
            progression = 1 - (nb_briques_restantes / self.briques_totales)
            base = int(8 * self.scale)
            vitesse_cible = int(base + progression * (self.vitesse_max - base))
        self.vitesse_x = vitesse_cible if self.vitesse_x >= 0 else -vitesse_cible
        self.vitesse_y = vitesse_cible if self.vitesse_y >= 0 else -vitesse_cible

    # ----------------------------------------------------------------------
    # Entrées clavier (changement de direction)
    # ----------------------------------------------------------------------
    def deplacer_gauche(self, _):
        """Change la direction de la raquette vers la gauche."""
        self.direction_raquette = -1

    def deplacer_droite(self, _):
        """Change la direction de la raquette vers la droite."""
        self.direction_raquette = 1

    # ----------------------------------------------------------------------
    # Positionnement des éléments
    # ----------------------------------------------------------------------
    def positionner_balle_centre(self):
        """Replace la balle près de la raquette (ou au centre) selon l’état de rotation."""
        r = self.balle_diametre / 2
        cx = self.canvas_width / 2
        if self.rotation_active and self.raquette is not None:
            rp = self.canvas.coords(self.raquette)
            if rp:
                cy = min(self.canvas_height - r, rp[3] + int(60 * self.scale))
            else:
                cy = r + int(60 * self.scale)
        else:
            cy = max(r, self.raquette_y - int(60 * self.scale))
        self.canvas.coords(self.balle, cx - r, cy - r, cx + r, cy + r)

    def mettre_a_jour_raquette(self, recentrer=False):
        """Met à jour la taille/position de la raquette; recentre si demandé."""
        etape = max(0, min(self.raquette_etape, len(self.raquette_largeurs) - 1))
        x_centre = self.canvas_width / 2
        y1 = self.raquette_y
        y2 = self.raquette_y + self.raquette_hauteur

        largeur = self.raquette_largeurs[etape]
        demi = largeur / 2
        x1, x2 = x_centre - demi, x_centre + demi

        if self.rotation_active and self.raquette is not None and not recentrer:
            coords = self.canvas.coords(self.raquette)
            if coords:
                y1, y2 = coords[1], coords[3]

        if self.raquette is None:
            self.raquette = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=("scene",))
        else:
            try:
                self.canvas.coords(self.raquette, x1, y1, x2, y2)
            except tk.TclError:
                self.raquette = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags=("scene",))

    def reduire_raquette(self):
        """Réduit la taille de la raquette à chaque perte; fin si trop petite."""
        self.raquette_etape += 1
        if self.raquette_etape >= len(self.raquette_largeurs):
            if self.raquette is not None:
                self.canvas.delete(self.raquette)
                self.raquette = None
            self.terminer_partie("Perdu 😢")
        else:
            self.mettre_a_jour_raquette()

    # ----------------------------------------------------------------------
    # Messages centrés (file FIFO)
    # ----------------------------------------------------------------------
    def push_message(self, texte):
        """Ajoute un message dans la file d’affichage."""
        self.file_messages.append(texte)
        if len(self.file_messages) == 1:
            self.afficher_message()

    def afficher_message(self):
        """Affiche le message courant au centre de l’écran."""
        if not self.file_messages:
            return
        texte = self.file_messages[0]
        self.canvas.delete("message")
        self.message_id = self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=texte,
            fill="white",
            font=("Arial", int(32 * self.scale), "bold"),
            tags="message",
        )
        self.message_timer_id = self.root.after(1500, self.retirer_message)

    def retirer_message(self):
        """Retire le message courant puis affiche le suivant (si présent)."""
        if self.message_timer_id is not None:
            self.root.after_cancel(self.message_timer_id)
            self.message_timer_id = None
        self.canvas.delete("message")
        if self.file_messages:
            self.file_messages.pop(0)
        if self.file_messages:
            self.afficher_message()

