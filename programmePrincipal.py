"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter (version responsive, contrôle arcade)
"""

import tkinter as tk
import random


class InterfaceAccueil:
    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.ref_width = 1600
        self.ref_height = 900

        self.scale_x = self.screen_width / self.ref_width
        self.scale_y = self.screen_height / self.ref_height
        self.scale = min(self.scale_x, self.scale_y)

        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#001a33")

        self.label_titre = tk.Label(
            root,
            text="Bienvenue dans le Casse-Brique",
            font=("Arial", int(28 * self.scale), "bold"),
            fg="white",
            bg="#001a33",
        )
        self.label_titre.pack(pady=int(100 * self.scale))

        self.bouton_jouer = tk.Button(
            root,
            text="Jouer",
            font=("Arial", int(20 * self.scale)),
            command=self.lancer_jeu,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_jouer.pack(pady=int(20 * self.scale))

        # ---- Bouton Quitter (menu) ----
        self.bouton_quitter = tk.Button(
            root,
            text="Quitter",
            font=("Arial", int(20 * self.scale)),
            command=root.destroy,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_quitter.pack(pady=int(10 * self.scale))

    def lancer_jeu(self):
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.bouton_quitter.destroy()  # détruire aussi le bouton Quitter du menu
        self.interface_jeu = InterfaceJeu(self.root, self.scale)


class InterfaceJeu:
    def __init__(self, root, scale):
        self.root = root
        self.scale = scale
        self.root.configure(bg="#001a33")

        self.canvas_width = int(1600 * scale)
        self.canvas_height = int(900 * scale)
        self.raquette_hauteur = int(25 * scale)
        self.balle_diametre = int(25 * scale)
        # Raquette proche du bas
        self.raquette_y = self.canvas_height - int(15 * scale)

        self.raquette_largeurs = [int(260 * scale), int(200 * scale), int(140 * scale)]
        self.hitbox_pad_x = int(10 * self.scale)  # marge horizontale
        self.hitbox_pad_y = int(6 * self.scale)   # marge verticale
        self.raquette_etape = 0

        self.vitesse_x = int(6 * scale)
        self.vitesse_y = -int(6 * scale)
        self.vitesse_max = int(9 * scale)
        self.vitesse_increment = 0.15 * scale

        # Pas de la raquette (réutilisé comme vitesse de déplacement continu)
        self.raquette_pas = int(80 * scale)
        self.vitesse_raquette_coef = 0.15  # gardé tel quel

        self.score = 0
        self.partie_terminee = False
        self.en_cours = False

        # Timers
        self.animation_id = None
        a = None
        self.raquette_move_id = None
        self.rotation_active = False
        self.rotation_timer_id = None
        self.boost_actif = False
        self.boost_timer_id = None
        self.malus_vert_timer_id = None
        self.message_timer_id = None

        # Contrôles
        self.controles_inverses = False
        self.direction_raquette = 0  # -1 gauche, 1 droite, 0 arrêt

        # Piles / files
        self.pile_vitesses = []
        self.file_messages = []

        # UI top
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

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#001a33",
            highlightthickness=0,
        )
        self.canvas.pack(pady=int(10 * scale))

        # --- Zone boutons fin de partie (dans le canvas)
        self.button_frame = tk.Frame(self.canvas, bg="#001a33")

        self.bouton_action = tk.Button(
            self.button_frame,
            text="Rejouer",
            font=("Arial", int(18 * scale)),
            command=self.jouer,
            bg="#003366",
            fg="white",
            width=int(12 * self.scale),
        )
        self.bouton_action.pack(side=tk.LEFT, padx=int(10 * self.scale), pady=int(5 * self.scale))

        # ---- Bouton Quitter (fin de partie) ----
        self.bouton_quitter_ingame = tk.Button(
            self.button_frame,
            text="Quitter",
            font=("Arial", int(18 * scale)),
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
        self.canvas.itemconfigure(self.button_window, state="hidden")  # caché pendant la partie

        # Objets
        self.briques = []
        self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))
        self.balle = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("scene",))

        # Bind: on change juste la direction (contrôle arcade)
        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        # >>> Démarrage immédiat de la partie <<<
        self.jouer()

    # ---------- Briques ----------

    def creer_briques(self):
        self.canvas.delete("brique")
        self.briques = []
        brique_largeur = int(150 * self.scale)
        brique_hauteur = int(30 * self.scale)
        espacement_x = int(15 * self.scale)
        espacement_y = int(12 * self.scale)
        colonnes = 9
        lignes = 1
        marge_haute = 0

        largeur_total = colonnes * brique_largeur + (colonnes - 1) * espacement_x
        marge_gauche = (self.canvas_width - largeur_total) // 2

        for ligne in range(lignes):
            for col in range(colonnes):
                x1 = marge_gauche + col * (brique_largeur + espacement_x)
                y1 = marge_haute + ligne * (brique_hauteur + espacement_y)
                x2 = x1 + brique_largeur
                y2 = y1 + brique_hauteur
                brique = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="#a3d5ff", outline="black", tags=("brique", "scene")
                )
                self.briques.append(brique)

        self.briques_totales = len(self.briques)
        # Bornes de la "zone briques" pour fermer les couloirs latéraux
        self.zone_brique_x1 = marge_gauche
        self.zone_brique_x2 = marge_gauche + largeur_total
        self.zone_brique_y2 = marge_haute + lignes * brique_hauteur + (lignes - 1) * espacement_y

        self.ajouter_briques_speciales()

    def ajouter_briques_speciales(self):
        total_briques = len(self.briques)
        if total_briques < 8:  # cohérent avec sample(8)
            return
        briques_choisies = random.sample(self.briques, 8)
        rouges = briques_choisies[:3]
        violettes = briques_choisies[3:5]
        vertes = briques_choisies[5:8]
        for brique in rouges:
            self.canvas.itemconfig(brique, fill="#ff8c8c", tags=("brique", "brique_rouge", "scene"))
        for brique in violettes:
            self.canvas.itemconfig(brique, fill="#d5a6ff", tags=("brique", "brique_violette", "scene"))
        for brique in vertes:
            self.canvas.itemconfig(brique, fill="#b3ffcc", tags=("brique", "brique_verte", "scene"))

    # ---------- Cycle de jeu ----------

    def jouer(self):
        self.desactiver_rotation(force=True)
        self.reset_partie()
        self.creer_briques()
        self.masquer_bouton_action()  # cacher les boutons pendant la partie
        self.partie_terminee = False
        self.en_cours = True
        self.canvas.focus_set()

        # Départ arcade : mouvement continu (droite par défaut)
        self.direction_raquette = 1
        self.mouvement_raquette()

        self.deplacer_balle()

    def reset_partie(self):
        # Annule timers
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        if self.raquette_move_id is not None:
            self.root.after_cancel(self.raquette_move_id)
            self.raquette_move_id = None
        if self.boost_timer_id is not None:
            self.root.after_cancel(self.boost_timer_id)
            self.boost_timer_id = None
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        if self.rotation_timer_id is not None:
            self.root.after_cancel(self.rotation_timer_id)
            self.rotation_timer_id = None
        if self.message_timer_id is not None:
            self.root.after_cancel(self.message_timer_id)
            self.message_timer_id = None

        self.canvas.delete("popup")
        self.canvas.delete("message")

        # États
        self.file_messages = []
        self.pile_vitesses = []
        self.boost_actif = False
        self.raquette_pas = int(80 * self.scale)
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.raquette_etape = 0
        self.controles_inverses = False
        self.direction_raquette = 0

        self.label_score.config(text=f"Score : {self.score}")

        if self.raquette is None:
            self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))

        self.mettre_a_jour_raquette(recentrer=True)
        self.positionner_balle_centre()

        # Démarrage plus doux
        self.vitesse_x = int(6 * self.scale)
        self.vitesse_y = -int(6 * self.scale)

    def terminer_partie(self, message):
        self.partie_terminee = True
        self.en_cours = False

        # Annule timers
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        if self.raquette_move_id is not None:
            self.root.after_cancel(self.raquette_move_id)
            self.raquette_move_id = None
        self.desactiver_rotation(force=True)
        if self.boost_timer_id is not None:
            self.root.after_cancel(self.boost_timer_id)
            self.boost_timer_id = None
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        if self.message_timer_id is not None:
            self.root.after_cancel(self.message_timer_id)
            self.message_timer_id = None

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

    # ---------- UI ----------

    def afficher_bouton_action(self, texte, commande):
        self.bouton_action.config(text=texte, command=commande, state=tk.NORMAL)
        self.canvas.itemconfigure(self.button_window, state="normal")

    def masquer_bouton_action(self):
        self.canvas.itemconfigure(self.button_window, state="hidden")

    # ---------- Mouvements ----------

    def deplacer_balle(self):
        if self.partie_terminee or not self.en_cours:
            return

        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        # Bords gauche/droite — ferme le couloir à côté des briques
        pad = self.balle_diametre // 3  # petit tampon
        if pos[1] <= getattr(self, "zone_brique_y2", 0) + pad:
            if not self.rotation_active:
                left_wall = max(0, getattr(self, "zone_brique_x1", 0) - pad)
                right_wall = min(self.canvas_width, getattr(self, "zone_brique_x2", self.canvas_width) + pad)
            else:
                # miroir horizontal quand la rotation est active
                left_wall = max(0, self.canvas_width - getattr(self, "zone_brique_x2", self.canvas_width) - pad)
                right_wall = min(self.canvas_width, self.canvas_width - getattr(self, "zone_brique_x1", 0) + pad)
        else:
            left_wall, right_wall = 0, self.canvas_width

        # Rebond + clamp sur les murs internes pour ne pas "passer derrière"
        if pos[0] <= left_wall:
            self.vitesse_x = abs(self.vitesse_x)
            self.canvas.move(self.balle, left_wall - pos[0], 0)
            pos = self.canvas.coords(self.balle)
        elif pos[2] >= right_wall:
            self.vitesse_x = -abs(self.vitesse_x)
            self.canvas.move(self.balle, right_wall - pos[2], 0)
            pos = self.canvas.coords(self.balle)

        # Haut/bas en fonction de la rotation
        if not self.rotation_active:
            if pos[1] <= 0:
                self.vitesse_y = -self.vitesse_y
        else:
            if pos[3] >= self.canvas_height:
                self.vitesse_y = -self.vitesse_y

        # Collision raquette (avec hitbox élargie et repositionnement propre)
        if self.raquette is not None:
            raquette_pos = self.canvas.coords(self.raquette)
            if raquette_pos:
                rx1, ry1, rx2, ry2 = raquette_pos

                # Hitbox élargie (non visible)
                hx1 = rx1 - self.hitbox_pad_x
                hy1 = ry1 - self.hitbox_pad_y
                hx2 = rx2 + self.hitbox_pad_x
                hy2 = ry2 + self.hitbox_pad_y

                if not self.rotation_active:
                    collision = (
                        self.vitesse_y > 0 and
                        pos[2] >= hx1 and pos[0] <= hx2 and
                        pos[3] >= hy1 and pos[1] <= ry1
                    )
                else:
                    collision = (
                        self.vitesse_y < 0 and
                        pos[2] >= hx1 and pos[0] <= hx2 and
                        pos[1] <= hy2 and pos[3] >= ry2
                    )

                if collision:
                    self.vitesse_y = -self.vitesse_y

                    # Repositionner la balle au bord de la raquette visible
                    cx = (pos[0] + pos[2]) / 2
                    r = self.balle_diametre / 2

                    if not self.rotation_active:
                        y2 = ry1 - 1
                        y1 = y2 - 2 * r
                    else:
                        y1 = ry2 + 1
                        y2 = y1 + 2 * r

                    self.canvas.coords(self.balle, int(cx - r), int(y1), int(cx + r), int(y2))
                    pos = self.canvas.coords(self.balle)

        # Collision briques
        for brique in self.briques[:]:
            brique_pos = self.canvas.coords(brique)
            if brique_pos:
                if (
                    pos[2] >= brique_pos[0] and pos[0] <= brique_pos[2]
                    and pos[3] >= brique_pos[1] and pos[1] <= brique_pos[3]
                ):
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

        # Perte "vie" → recentre + rétrécit raquette
        if not self.rotation_active:
            if pos[3] >= self.canvas_height:
                self.positionner_balle_centre()
                self.vitesse_y = -abs(self.vitesse_y)
                self.reduire_raquette()
        else:
            if pos[1] <= 0:
                self.positionner_balle_centre()
                self.vitesse_y = abs(self.vitesse_y)
                self.reduire_raquette()

        self.animation_id = self.root.after(20, self.deplacer_balle)

    def mouvement_raquette(self):
        """Déplacement continu façon arcade. Bords = rebond automatique."""
        if self.partie_terminee or not self.en_cours or self.raquette is None:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.raquette)

        # Vitesse basée sur raquette_pas (pour que le malus vert continue d'agir)
        vitesse = max(1, int(self.raquette_pas * self.vitesse_raquette_coef))

        d = vitesse * (-1 if self.controles_inverses else 1) * self.direction_raquette

        if self.direction_raquette != 0:
            # Gestion des bords + rebond auto
            if x1 + d < 0:
                d = -x1
                self.direction_raquette = 1 if not self.controles_inverses else -1
            elif x2 + d > self.canvas_width:
                d = self.canvas_width - x2
                self.direction_raquette = -1 if not self.controles_inverses else 1

            self.canvas.move(self.raquette, d, 0)

        self.raquette_move_id = self.root.after(20, self.mouvement_raquette)

    # ---------- Effets spéciaux / états ----------

    def activer_boost_rouge(self):
        if self.boost_actif:
            return
        self.boost_actif = True
        self.pile_vitesses.append((abs(self.vitesse_x), abs(self.vitesse_y)))
        self.vitesse_x = self.vitesse_max if self.vitesse_x > 0 else -self.vitesse_max
        self.vitesse_y = self.vitesse_max if self.vitesse_y > 0 else -self.vitesse_max
        self.boost_timer_id = self.root.after(2000, self.fin_boost_rouge)

    def fin_boost_rouge(self):
        self.boost_actif = False
        self.boost_timer_id = None
        if self.pile_vitesses:
            self.pile_vitesses.pop()
        self.ajuster_vitesse()

    def activer_malus_vert(self):
        self.raquette_pas = int(40 * self.scale)
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
        self.malus_vert_timer_id = self.root.after(1500, self.fin_malus_vert)

    def fin_malus_vert(self):
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        self.raquette_pas = int(80 * self.scale)

    def activer_rotation(self):
        if self.rotation_active:
            self.desactiver_rotation()
            return
        self.rotation_active = True
        self.controles_inverses = True
        cx = self.canvas_width / 2
        cy = self.canvas_height / 2
        self.canvas.scale("scene", cx, cy, -1, -1)
        if self.rotation_timer_id is not None:
            self.root.after_cancel(self.rotation_timer_id)
        self.rotation_timer_id = self.root.after(10000, self.desactiver_rotation)

    def desactiver_rotation(self, force=False):
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

    def ajuster_vitesse(self):
        nb_briques_restantes = len(self.briques)
        if nb_briques_restantes <= 15:
            vitesse_cible = self.vitesse_max
        else:
            progression = 1 - (nb_briques_restantes / self.briques_totales)
            vitesse_cible = int(8 * self.scale + progression * (self.vitesse_max - int(8 * self.scale)))
        self.vitesse_x = vitesse_cible if self.vitesse_x >= 0 else -vitesse_cible
        self.vitesse_y = vitesse_cible if self.vitesse_y >= 0 else -vitesse_cible

    # ---------- Entrées clavier (changement de direction uniquement) ----------

    def deplacer_gauche(self, event):
        self.direction_raquette = -1  # direction brute

    def deplacer_droite(self, event):
        self.direction_raquette = 1   # direction brute

    # ---------- Positionnements / raquette ----------

    def positionner_balle_centre(self):
        rayon = self.balle_diametre / 2
        centre_x = self.canvas_width / 2
        if self.rotation_active and self.raquette is not None:
            rp = self.canvas.coords(self.raquette)
            if rp:
                centre_y = min(self.canvas_height - rayon, rp[3] + int(60 * self.scale))
            else:
                centre_y = rayon + int(60 * self.scale)
        else:
            centre_y = max(rayon, self.raquette_y - int(60 * self.scale))
        self.canvas.coords(self.balle, centre_x - rayon, centre_y - rayon, centre_x + rayon, centre_y + rayon)

    def mettre_a_jour_raquette(self, recentrer=False):
        etape = self.raquette_etape
        if etape < 0:
            etape = 0
        if etape >= len(self.raquette_largeurs):
            etape = len(self.raquette_largeurs) - 1

        x_centre = self.canvas_width / 2
        y1 = self.raquette_y
        y2 = self.raquette_y + self.raquette_hauteur

        largeur = self.raquette_largeurs[etape]
        demi_largeur = largeur / 2
        x1 = x_centre - demi_largeur
        x2 = x_centre + demi_largeur

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
        self.raquette_etape += 1
        if self.raquette_etape >= len(self.raquette_largeurs):
            if self.raquette is not None:
                self.canvas.delete(self.raquette)
                self.raquette = None
            self.terminer_partie("Perdu ")
        else:
            self.mettre_a_jour_raquette()

    # ---------- Placeholders (inchangés) ----------

    def traiter_file_messages(self):
        return

    def fin_affichage_message(self):
        return



def main():
    root = tk.Tk()
    root.title("Casse-Brique")
    root.state("zoomed")  # Plein écran adaptatif
    root.configure(bg="#001a33")

    app = InterfaceAccueil(root)
    root.mainloop()


if __name__ == "__main__":
    main()

