"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter
"""

import tkinter as tk


class InterfaceAccueil:
    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")
        self.root.geometry("1280x900")
        self.root.configure(bg="#001a33")

        self.label_titre = tk.Label(
            root,
            text="Bienvenue dans le Casse-Brique",
            font=("Arial", 18),
            fg="white",
            bg="#001a33",
        )
        self.label_titre.pack(pady=60)

        self.bouton_jouer = tk.Button(
            root,
            text="Jouer",
            font=("Arial", 14),
            command=self.lancer_jeu,
            bg="#003366",
            fg="white",
        )
        self.bouton_jouer.pack(pady=10)

    def lancer_jeu(self):
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.interface_jeu = InterfaceJeu(self.root)


class InterfaceJeu:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#001a33")
        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.animation_id = None
        self.raquette_largeurs = [200, 140, 80]
        self.raquette_etape = 0
        self.canvas_width = 1100
        self.canvas_height = 720
        self.raquette_y = self.canvas_height - 60
        self.raquette_hauteur = 20
        self.balle_diametre = 20

        top_frame = tk.Frame(root, bg="#001a33")
        top_frame.pack(fill=tk.X, pady=20)

        self.label_score = tk.Label(
            top_frame,
            text=f"Score : {self.score}",
            font=("Arial", 16),
            fg="yellow",
            bg="#001a33",
        )
        self.label_score.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#001a33",
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        self.button_frame = tk.Frame(root, bg="#001a33")
        self.bouton_action = tk.Button(
            self.button_frame,
            text="Jouer",
            font=("Arial", 14),
            command=self.jouer,
            bg="#003366",
            fg="white",
        )
        self.bouton_action.pack(padx=10, pady=5)

        self.briques = []

        self.raquette = self.canvas.create_rectangle(0, 0, 0, 0, fill="white")
        self.balle = self.canvas.create_oval(0, 0, 0, 0, fill="white")

        self.vitesse_x = 4
        self.vitesse_y = -4

        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        self.reset_partie()
        self.afficher_bouton_action("Jouer", self.jouer)

    def creer_briques(self):
        self.canvas.delete("brique")
        self.briques = []

        brique_largeur = 80
        brique_hauteur = 20
        espacement_x = 10
        espacement_y = 10
        colonnes = 12
        lignes = 5
        marge_haute = 50

        largeur_total = colonnes * brique_largeur + (colonnes - 1) * espacement_x
        marge_gauche = (self.canvas_width - largeur_total) // 2

        for ligne in range(lignes):
            for col in range(colonnes):
                x1 = marge_gauche + col * (brique_largeur + espacement_x)
                y1 = marge_haute + ligne * (brique_hauteur + espacement_y)
                x2 = x1 + brique_largeur
                y2 = y1 + brique_hauteur
                brique = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="orange",
                    outline="black",
                    tags="brique",
                )
                self.briques.append(brique)

    def jouer(self):
        self.reset_partie()
        self.masquer_bouton_action()
        self.partie_terminee = False
        self.en_cours = True
        self.canvas.focus_set()
        self.deplacer_balle()

    def reset_partie(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.score = 0
        self.partie_terminee = False
        self.en_cours = False
        self.raquette_etape = 0

        self.label_score.config(text=f"Score : {self.score}")

        self.creer_briques()
        self.canvas.delete("message")
        self.mettre_a_jour_raquette(recentrer=True)
        self.positionner_balle_centre()
        self.vitesse_x = 4
        self.vitesse_y = -4

    def terminer_partie(self, message):
        self.partie_terminee = True
        self.en_cours = False
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.canvas.delete("message")
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=message,
            fill="white",
            font=("Arial", 18, "bold"),
            tags="message",
        )

        self.afficher_bouton_action("Jouer", self.jouer)

    def afficher_bouton_action(self, texte, commande):
        self.bouton_action.config(text=texte, command=commande, state=tk.NORMAL)
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=5)

    def masquer_bouton_action(self):
        self.button_frame.pack_forget()

    def deplacer_balle(self):
        if self.partie_terminee or not self.en_cours:
            return

        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.vitesse_x = -self.vitesse_x
        if pos[1] <= 0:
            self.vitesse_y = -self.vitesse_y

        if self.raquette is not None:
            raquette_pos = self.canvas.coords(self.raquette)
            if (
                raquette_pos
                and pos[3] >= raquette_pos[1]
                and pos[2] >= raquette_pos[0]
                and pos[0] <= raquette_pos[2]
                and pos[3] <= raquette_pos[3] + 5
            ):
                self.vitesse_y = -abs(self.vitesse_y)

        for brique in self.briques[:]:
            brique_pos = self.canvas.coords(brique)
            if brique_pos:
                collision_horizontale = pos[2] >= brique_pos[0] and pos[0] <= brique_pos[2]
                collision_verticale = pos[3] >= brique_pos[1] and pos[1] <= brique_pos[3]

                if collision_horizontale and collision_verticale:
                    self.canvas.delete(brique)
                    self.briques.remove(brique)
                    self.vitesse_y = -self.vitesse_y
                    self.score += 10
                    self.label_score.config(text=f"Score : {self.score}")

                    if not self.briques:
                        self.terminer_partie("Bravo ! Vous avez gagné !")
                        return
                    break

        if pos[3] >= self.canvas_height:
            self.positionner_balle_centre()
            self.vitesse_x = 4 if self.vitesse_x >= 0 else -4
            self.vitesse_y = -4
            self.reduire_raquette()
            if self.partie_terminee:
                return

        self.animation_id = self.root.after(20, self.deplacer_balle)

    def deplacer_gauche(self, event):
        if self.raquette is None:
            return
        pos = self.canvas.coords(self.raquette)
        if pos[0] > 0:
            deplacement = -35
            if pos[0] + deplacement < 0:
                deplacement = -pos[0]
            self.canvas.move(self.raquette, deplacement, 0)

    def deplacer_droite(self, event):
        if self.raquette is None:
            return
        pos = self.canvas.coords(self.raquette)
        if pos[2] < self.canvas_width:
            deplacement = 35
            if pos[2] + deplacement > self.canvas_width:
                deplacement = self.canvas_width - pos[2]
            self.canvas.move(self.raquette, deplacement, 0)

    def positionner_balle_centre(self):
        rayon = self.balle_diametre / 2
        centre_x = self.canvas_width / 2
        centre_y = max(rayon, self.raquette_y - 60)
        x1 = int(centre_x - rayon)
        y1 = int(centre_y - rayon)
        x2 = int(centre_x + rayon)
        y2 = int(centre_y + rayon)
        self.canvas.coords(self.balle, x1, y1, x2, y2)

    def mettre_a_jour_raquette(self, recentrer=False):
        x_centre = self.canvas_width / 2
        if self.raquette is not None and not recentrer:
            coords = self.canvas.coords(self.raquette)
            if coords:
                x_centre = (coords[0] + coords[2]) / 2
        largeur = self.raquette_largeurs[self.raquette_etape]
        demi_largeur = largeur / 2
        x_centre = max(demi_largeur, min(self.canvas_width - demi_largeur, x_centre))
        x1 = int(x_centre - demi_largeur)
        x2 = int(x_centre + demi_largeur)
        y1 = self.raquette_y
        y2 = self.raquette_y + self.raquette_hauteur
        if self.raquette is None:
            self.raquette = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        else:
            try:
                self.canvas.coords(self.raquette, x1, y1, x2, y2)
            except tk.TclError:
                self.raquette = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white"
                )

    def reduire_raquette(self):
        self.raquette_etape += 1
        if self.raquette_etape >= len(self.raquette_largeurs):
            if self.raquette is not None:
                self.canvas.delete(self.raquette)
                self.raquette = None
            self.terminer_partie("perdu")
        else:
            self.mettre_a_jour_raquette()
    

   

    


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()
