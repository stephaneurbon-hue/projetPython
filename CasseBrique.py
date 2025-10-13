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
        self.root.geometry("500x400")
        self.root.configure(bg="black")

        self.label_titre = tk.Label(
            root,
            text="Bienvenue dans le Casse-Brique",
            font=("Arial", 18),
            fg="white",
            bg="black",
        )
        self.label_titre.pack(pady=60)

        self.bouton_jouer = tk.Button(
            root,
            text="Jouer",
            font=("Arial", 14),
            command=self.lancer_jeu,
            bg="gray",
            fg="white",
        )
        self.bouton_jouer.pack(pady=10)

        self.bouton_quitter = tk.Button(
            root,
            text="Quitter",
            font=("Arial", 14),
            command=root.destroy,
            bg="gray",
            fg="white",
        )
        self.bouton_quitter.pack(pady=10)

    def lancer_jeu(self):
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.bouton_quitter.destroy()
        InterfaceJeu(self.root)


class InterfaceJeu:
    def __init__(self, root):
        self.root = root
        self.score = 0
        self.vies = 3
        self.partie_terminee = False
        self.en_cours = False
        self.animation_id = None

        top_frame = tk.Frame(root, bg="black")
        top_frame.pack(fill=tk.X, pady=10)

        self.label_vies = tk.Label(
            top_frame,
            text=f"Vies : {self.vies}",
            font=("Arial", 16),
            fg="red",
            bg="black",
        )
        self.label_vies.pack(side=tk.LEFT, padx=20)

        self.label_score = tk.Label(
            top_frame,
            text=f"Score : {self.score}",
            font=("Arial", 16),
            fg="yellow",
            bg="black",
        )
        self.label_score.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(
            root,
            width=500,
            height=300,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.briques = []

        self.raquette = self.canvas.create_rectangle(
            200, 270, 300, 290, fill="white"
        )
        self.balle = self.canvas.create_oval(
            240, 250, 260, 270, fill="white"
        )

        self.vitesse_x = 3
        self.vitesse_y = -3

        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        self.button_frame = tk.Frame(root, bg="black")
        self.bouton_action = tk.Button(
            self.button_frame,
            text="Jouer",
            font=("Arial", 14),
            command=self.jouer,
            bg="gray",
            fg="white",
        )
        self.bouton_action.pack(padx=10, pady=10)

        self.reset_partie()
        self.afficher_bouton_action("Jouer", self.jouer)

    def creer_briques(self):
        self.canvas.delete("brique")
        self.briques = []

        brique_largeur = 60
        brique_hauteur = 20
        espacement_x = 10
        espacement_y = 10
        colonnes = 7
        lignes = 3

        largeur_total = colonnes * brique_largeur + (colonnes - 1) * espacement_x
        marge_gauche = (500 - largeur_total) // 2

        for ligne in range(lignes):
            for col in range(colonnes):
                x1 = marge_gauche + col * (brique_largeur + espacement_x)
                y1 = ligne * (brique_hauteur + espacement_y)
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
        self.deplacer_balle()

    def reset_partie(self):
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.score = 0
        self.vies = 3
        self.partie_terminee = False
        self.en_cours = False

        self.label_score.config(text=f"Score : {self.score}")
        self.label_vies.config(text=f"Vies : {self.vies}")

        self.creer_briques()
        self.canvas.delete("message")
        self.canvas.coords(self.raquette, 200, 270, 300, 290)
        self.canvas.coords(self.balle, 240, 250, 260, 270)
        self.vitesse_x = 3
        self.vitesse_y = -3

    def terminer_partie(self, message):
        self.partie_terminee = True
        self.en_cours = False
        if self.animation_id is not None:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.canvas.delete("message")
        self.canvas.create_text(
            250,
            150,
            text=message,
            fill="white",
            font=("Arial", 18, "bold"),
            tags="message",
        )

        self.afficher_bouton_action("Jouer", self.jouer)

    def afficher_bouton_action(self, texte, commande):
        self.bouton_action.config(text=texte, command=commande, state=tk.NORMAL)
        if not self.button_frame.winfo_manager():
            self.button_frame.pack(side=tk.BOTTOM, pady=10)

    def masquer_bouton_action(self):
        if self.button_frame.winfo_manager():
            self.button_frame.pack_forget()

    def deplacer_balle(self):
        if self.partie_terminee or not self.en_cours:
            return

        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        if pos[0] <= 0 or pos[2] >= 500:
            self.vitesse_x = -self.vitesse_x
        if pos[1] <= 0:
            self.vitesse_y = -self.vitesse_y

        raquette_pos = self.canvas.coords(self.raquette)
        if (
            pos[3] >= raquette_pos[1]
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

        if pos[3] >= 300:
            self.vies -= 1
            self.label_vies.config(text=f"Vies : {self.vies}")
            self.canvas.coords(self.balle, 240, 250, 260, 270)
            self.vitesse_y = -3
            if self.vies <= 0:
                self.terminer_partie("Plus de vies !")
                return

        self.animation_id = self.root.after(20, self.deplacer_balle)

    def deplacer_gauche(self, event):
        pos = self.canvas.coords(self.raquette)
        if pos[0] > 0:
            self.canvas.move(self.raquette, -20, 0)

    def deplacer_droite(self, event):
        pos = self.canvas.coords(self.raquette)
        if pos[2] < 500:
            self.canvas.move(self.raquette, 20, 0)


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()
