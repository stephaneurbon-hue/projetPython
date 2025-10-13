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

        self.label_titre = tk.Label(root, text="Bienvenue dans le Casse-Brique", font=("Arial", 18), fg="white", bg="black")
        self.label_titre.pack(pady=60)

        self.bouton_jouer = tk.Button(root, text="Jouer", font=("Arial", 14), command=self.lancer_jeu, bg="gray", fg="white")
        self.bouton_jouer.pack(pady=10)

        self.bouton_quitter = tk.Button(root, text="Quitter", font=("Arial", 14), command=root.destroy, bg="gray", fg="white")
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

        top_frame = tk.Frame(root, bg="black")
        top_frame.pack(fill=tk.X, pady=10)

        self.label_vies = tk.Label(top_frame, text=f"Vies : {self.vies}", font=("Arial", 16), fg="red", bg="black")
        self.label_vies.pack(side=tk.LEFT, padx=20)

        self.label_score = tk.Label(top_frame, text=f"Score : {self.score}", font=("Arial", 16), fg="yellow", bg="black")
        self.label_score.pack(side=tk.RIGHT, padx=20)

        self.canvas = tk.Canvas(root, width=500, height=300, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Création des briques sur le même canvas
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
                brique = self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black")
                self.briques.append(brique)

        # Raquette et balle
        self.raquette = self.canvas.create_rectangle(200, 270, 300, 290, fill="white")
        self.balle = self.canvas.create_oval(240, 250, 260, 270, fill="white")

        self.vitesse_x = 3
        self.vitesse_y = -3

        self.root.bind("<Left>", self.deplacer_gauche)
        self.root.bind("<Right>", self.deplacer_droite)

        bottom_frame = tk.Frame(root, bg="black")
        bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.bouton_action = tk.Button(bottom_frame, text="Jouer", font=("Arial", 14), command=self.jouer, bg="gray", fg="white")
        self.bouton_action.pack(side=tk.LEFT, padx=10)

        self.bouton_quitter = tk.Button(bottom_frame, text="Quitter", font=("Arial", 14), command=root.destroy, bg="gray", fg="white")
        self.bouton_quitter.pack(side=tk.RIGHT, padx=10)

        self.deplacer_balle()

    def jouer(self):
        if self.bouton_action.cget("text") == "Jouer":
            self.bouton_action.config(text="Recommencer", command=self.recommencer)
        if self.vies > 0:
            self.score += 1
            self.vies -= 1
            self.label_score.config(text=f"Score : {self.score}")
            self.label_vies.config(text=f"Vies : {self.vies}")
        else:
            self.bouton_action.config(state=tk.DISABLED)
            self.label_vies.config(text="Plus de vies !")

    def recommencer(self):
        self.score = 0
        self.vies = 3
        self.label_score.config(text=f"Score : {self.score}")
        self.label_vies.config(text=f"Vies : {self.vies}")
        self.bouton_action.config(state=tk.NORMAL, text="Jouer", command=self.jouer)
        self.canvas.coords(self.balle, 240, 250, 260, 270)
        self.vitesse_x = 3
        self.vitesse_y = -3

    def deplacer_balle(self):
        self.canvas.move(self.balle, self.vitesse_x, self.vitesse_y)
        pos = self.canvas.coords(self.balle)

        # Rebond sur les bords
        if pos[0] <= 0 or pos[2] >= 500:
            self.vitesse_x = -self.vitesse_x
        if pos[1] <= 0:
            self.vitesse_y = -self.vitesse_y

        # Collision avec la raquette
        raquette_pos = self.canvas.coords(self.raquette)
        if pos[3] >= raquette_pos[1] and pos[2] >= raquette_pos[0] and pos[0] <= raquette_pos[2]:
            self.vitesse_y = -abs(self.vitesse_y)

        # Collision avec les briques
        for brique in self.briques:
            brique_pos = self.canvas.coords(brique)
            if brique_pos:
                if (pos[2] >= brique_pos[0] and pos[0] <= brique_pos[2] and
                    pos[3] >= brique_pos[1] and pos[1] <= brique_pos[3]):
                    self.canvas.delete(brique)
                    self.briques.remove(brique)
                    self.vitesse_y = -self.vitesse_y
                    self.score += 10
                    self.label_score.config(text=f"Score : {self.score}")
                    break

        # Perte de vie
        if pos[3] >= 300:
            self.vies -= 1
            self.label_vies.config(text=f"Vies : {self.vies}")
            self.canvas.coords(self.balle, 240, 250, 260, 270)
            self.vitesse_y = -3
            if self.vies <= 0:
                self.bouton_action.config(state=tk.DISABLED)
                self.label_vies.config(text="Plus de vies !")
                return

        self.root.after(20, self.deplacer_balle)

    def deplacer_gauche(self, event):
        pos = self.canvas.coords(self.raquette)
        if pos[0] > 0:
            self.canvas.move(self.raquette, -20, 0)

    def deplacer_droite(self, event):
        pos = self.canvas.coords(self.raquette)
        if pos[2] < 500:
            self.canvas.move(self.raquette, 20, 0)

# Lancer l'application
if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()
