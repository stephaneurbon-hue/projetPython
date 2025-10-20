"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter (version responsive)
"""

import tkinter as tk
import random


class InterfaceAccueil:
    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")

        # --- Détection automatique de la taille de l'écran ---
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Taille de référence (pour échelle)
        self.ref_width = 1600
        self.ref_height = 900

        # Facteur d’échelle
        self.scale_x = self.screen_width / self.ref_width
        self.scale_y = self.screen_height / self.ref_height
        self.scale = min(self.scale_x, self.scale_y)

        # Configuration de la fenêtre
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#001a33")

        # --- Éléments d'accueil ---
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

    def lancer_jeu(self):
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.interface_jeu = InterfaceJeu(self.root, self.scale)


class InterfaceJeu:
    def __init__(self, root, scale):
        self.root = root
        self.scale = scale
        self.root.configure(bg="#001a33")

        # --- Paramètres du jeu (mis à l'échelle) ---
        self.canvas_width = int(1600 * scale)
        self.canvas_height = int(700 * scale)
        self.raquette_hauteur = int(25 * scale)
        self.balle_diametre = int(25 * scale)
        self.raquette_y = self.canvas_height - int(50 * scale)
        self.raquette_largeurs = [int(200 * scale), int(150 * scale), int(100 * scale)]
        self.raquette_etape = 0
        self.vitesse_x = int(8 * scale)
        self.vitesse_y = -int(8 * scale)
        self.vitesse_max = int(16 * scale)
        self.vitesse_increment = 0.3 * scale
        self.raquette_pas = int(60 * scale)

        # États
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.animation_id = None
        self.rotation_active = False
        self.rotation_timer_id = None
        self.controles_inverses = False
        self.boost_actif = False
        self.boost_timer_id = None
        self.malus_vert_timer_id = None

        # --- Interface ---
        top_frame = tk.Frame(root, bg="#001a33")
        top_frame.pack(fill=tk.X, pady=int(10 * scale))

        self.label_score = tk.Label(
            top_frame,
            text=f"Score : {self.score}",
            font=("Arial", int(20 * scale), "bold"),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(side=tk.RIGHT, padx=int(30 * scale))

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#001a33",
            highlightthickness=0,
        )
        self.canvas.pack(pady=int(10 * scale))

        self.button_frame = tk.Frame(root, bg="#001a33")
        self.bouton_action = tk.Button(
            self.button_frame,
            text="Jouer",
            font=("Arial", int(18 * scale)),
            command=self.jouer,
            bg="#003366",
            fg="white",
            width=int(12 * scale),
        )
        self.bouton_action.pack(padx=int(10 * scale), pady=int(5 * scale))

        self.briques = []
        self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", tags=("scene",))
        self.balle = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("scene",))

        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        self.afficher_bouton_action("Jouer", self.jouer)

    # ======================
    # === MÉCANIQUES DU JEU ===
    # ======================

    def creer_briques(self):
        self.canvas.delete("brique")
        self.briques = []
        brique_largeur = int(150 * self.scale)
        brique_hauteur = int(30 * self.scale)
        espacement_x = int(15 * self.scale)
        espacement_y = int(15 * self.scale)
        colonnes = 9
        lignes = 5
        marge_haute = int(40 * self.scale)
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
        self.ajouter_briques_speciales()

    def ajouter_briques_speciales(self):
        total_briques = len(self.briques)
        if total_briques < 12:
            return
        briques_choisies = random.sample(self.briques, 12)
        rouges = briques_choisies[:5]
        violettes = briques_choisies[5:7]
        vertes = briques_choisies[7:12]
        for brique in rouges:
            self.canvas.itemconfig(brique, fill="#ff8c8c", tags=("brique", "brique_rouge", "scene"))
        for brique in violettes:
            self.canvas.itemconfig(brique, fill="#d5a6ff", tags=("brique", "brique_violette", "scene"))
        for brique in vertes:
            self.canvas.itemconfig(brique, fill="#b3ffcc", tags=("brique", "brique_verte", "scene"))

    def jouer(self):
        self.desactiver_rotation(force=True)
        self.reset_partie()
        self.creer_briques()
        self.masquer_bouton_action()
        self.partie_terminee = False
        self.en_cours = True
        self.canvas.focus_set()
        self.deplacer_balle()

    def reset_partie(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        if self.boost_timer_id is not None:
            self.root.after_cancel(self.boost_timer_id)
            self.boost_timer_id = None
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        self.boost_actif = False
        self.raquette_pas = int(60 * self.scale)
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.raquette_etape = 0
        self.label_score.config(text=f"Score : {self.score}")
        self.canvas.delete("message")
        self.mettre_a_jour_raquette(recentrer=True)
        self.positionner_balle_centre()
        self.vitesse_x = int(8 * self.scale)
        self.vitesse_y = -int(8 * self.scale)

    def terminer_partie(self, message):
        self.partie_terminee = True
        self.en_cours = False
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        self.desactiver_rotation(force=True)
        if self.boost_timer_id is not None:
            self.root.after_cancel(self.boost_timer_id)
            self.boost_timer_id = None
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        self.raquette_pas = int(60 * self.scale)
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

    def afficher_bouton_action(self, texte, commande):
        self.bouton_action.config(text=texte, command=commande, state=tk.NORMAL)
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=int(15 * self.scale))

    def masquer_bouton_action(self):
        self.button_frame.pack_forget()

    # === Mouvements et collisions ===

    def deplacer_balle(self):
        if self.partie_terminee or not self.en_cours:
            return

        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.vitesse_x = -self.vitesse_x

        if not self.rotation_active:
            if pos[1] <= 0:
                self.vitesse_y = -self.vitesse_y
        else:
            if pos[3] >= self.canvas_height:
                self.vitesse_y = -self.vitesse_y

        if self.raquette is not None:
            raquette_pos = self.canvas.coords(self.raquette)
            if not self.rotation_active:
                collision = (
                    raquette_pos
                    and pos[3] >= raquette_pos[1]
                    and pos[2] >= raquette_pos[0]
                    and pos[0] <= raquette_pos[2]
                    and pos[3] <= raquette_pos[3] + 5
                )
            else:
                collision = (
                    raquette_pos
                    and pos[1] <= raquette_pos[3]
                    and pos[2] >= raquette_pos[0]
                    and pos[0] <= raquette_pos[2]
                    and pos[1] >= raquette_pos[1] - 5
                )
            if collision:
                self.vitesse_y = -self.vitesse_y

        for brique in self.briques[:]:
            brique_pos = self.canvas.coords(brique)
            if brique_pos:
                if pos[2] >= brique_pos[0] and pos[0] <= brique_pos[2] and pos[3] >= brique_pos[1] and pos[1] <= brique_pos[3]:
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

        # Conditions de défaite
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

    # === Effets spéciaux ===

    def activer_boost_rouge(self):
        if self.boost_actif:
            return
        self.boost_actif = True
        self.vitesse_x = self.vitesse_max if self.vitesse_x > 0 else -self.vitesse_max
        self.vitesse_y = self.vitesse_max if self.vitesse_y > 0 else -self.vitesse_max
        self.boost_timer_id = self.root.after(2000, self.fin_boost_rouge)

    def fin_boost_rouge(self):
        self.boost_actif = False
        self.boost_timer_id = None
        self.ajuster_vitesse()

    def activer_malus_vert(self):
        self.raquette_pas = int(20 * self.scale)
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
        self.malus_vert_timer_id = self.root.after(3000, self.fin_malus_vert)

    def fin_malus_vert(self):
        if self.malus_vert_timer_id is not None:
            self.root.after_cancel(self.malus_vert_timer_id)
            self.malus_vert_timer_id = None
        self.raquette_pas = int(60 * self.scale)

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

    # === Autres ===

    def ajuster_vitesse(self):
        nb_briques_restantes = len(self.briques)
        if nb_briques_restantes <= 15:
            vitesse_cible = self.vitesse_max
        else:
            progression = 1 - (nb_briques_restantes / self.briques_totales)
            vitesse_cible = int(8 * self.scale + progression * (self.vitesse_max - int(8 * self.scale)))
        self.vitesse_x = vitesse_cible if self.vitesse_x >= 0 else -vitesse_cible
        self.vitesse_y = vitesse_cible if self.vitesse_y >= 0 else -vitesse_cible

    def deplacer_gauche(self, event):
        if self.raquette is None:
            return
        pos = self.canvas.coords(self.raquette)
        pas = self.raquette_pas
        deplacement = -pas if not self.controles_inverses else pas
        if pos[0] + deplacement < 0:
            deplacement = -pos[0]
        self.canvas.move(self.raquette, deplacement, 0)

    def deplacer_droite(self, event):
        if self.raquette is None:
            return
        pos = self.canvas.coords(self.raquette)
        pas = self.raquette_pas
        deplacement = pas if not self.controles_inverses else -pas
        if pos[2] + deplacement > self.canvas_width:
            deplacement = self.canvas_width - pos[2]
        self.canvas.move(self.raquette, deplacement, 0)

    def positionner_balle_centre(self):
        rayon = self.balle_diametre / 2
        centre_x = self.canvas_width / 2
        centre_y = self.raquette_y - 60
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

        self.canvas.coords(self.raquette, x1, y1, x2, y2)

    def reduire_raquette(self):
        self.raquette_etape += 1
        if self.raquette_etape >= len(self.raquette_largeurs):
            self.canvas.delete(self.raquette)
            self.terminer_partie("Perdu 😢")
        else:
            self.mettre_a_jour_raquette()


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()
