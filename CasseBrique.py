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

        self.canvas_briques = tk.Canvas(root, width=500, height=80, bg="black", highlightthickness=0)
        self.canvas_briques.pack()

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
                brique = self.canvas_briques.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black")
                self.briques.append(brique)

        spacer = tk.Frame(root, bg="black", height=100)
        spacer.pack()

        bottom_frame = tk.Frame(root, bg="black")
        bottom_frame.pack(side=tk.BOTTOM, pady=20)

        self.canvas = tk.Canvas(bottom_frame, width=500, height=60, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.TOP)

        self.raquette = self.canvas.create_rectangle(200, 30, 300, 50, fill="white")
        self.balle = self.canvas.create_oval(240, 10, 260, 30, fill="white")

        self.bouton_action = tk.Button(bottom_frame, text="Jouer", font=("Arial", 14), command=self.jouer, bg="gray", fg="white")
        self.bouton_action.pack(side=tk.LEFT, padx=10)

        self.bouton_quitter = tk.Button(bottom_frame, text="Quitter", font=("Arial", 14), command=root.destroy, bg="gray", fg="white")
        self.bouton_quitter.pack(side=tk.RIGHT, padx=10)

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

# Lancer l'application
if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()

