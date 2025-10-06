"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter

"""

#interface graphique
import tkinter as tk

class InterfaceJeu:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Jeu")
        self.root.geometry("500x400")
        self.root.configure(bg="black")  

        self.score = 0
        self.vies = 3

        # Cadre supérieur pour vies et score
        top_frame = tk.Frame(root, bg="black")
        top_frame.pack(fill=tk.X, pady=10)

        self.label_vies = tk.Label(top_frame, text=f"Vies : {self.vies}", font=("Arial", 16), fg="red", bg="black")
        self.label_vies.pack(side=tk.LEFT, padx=20)

        self.label_score = tk.Label(top_frame, text=f"Score : {self.score}", font=("Arial", 16), fg="yellow", bg="black")
        self.label_score.pack(side=tk.RIGHT, padx=20)

        # Espace vide pour centrer les éléments
        spacer = tk.Frame(root, bg="black", height=150)
        spacer.pack()

        # Cadre inférieur pour raquette et boutons
        bottom_frame = tk.Frame(root, bg="black")
        bottom_frame.pack(side=tk.BOTTOM, pady=20)

        # Canvas pour la raquette (placé au-dessus des boutons)
        self.canvas = tk.Canvas(bottom_frame, width=500, height=40, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.TOP)

        # Dessiner la raquette
        self.raquette = self.canvas.create_rectangle(200, 10, 300, 30, fill="white")

        # Bouton jouer
        self.bouton_action = tk.Button(bottom_frame, text="Jouer", font=("Arial", 14), command=self.jouer, bg="gray", fg="white")
        self.bouton_action.pack(side=tk.LEFT, padx=10)

        # Bouton quitter
        self.bouton_quitter = tk.Button(bottom_frame, text="Quitter", font=("Arial", 14), command=root.destroy, bg="gray", fg="white")
        self.bouton_quitter.pack(side=tk.RIGHT, padx=10)

    def jouer(self):
        if self.vies > 0:
            self.score += 1
            self.vies -= 1
            self.label_score.config(text=f"Score : {self.score}")
            self.label_vies.config(text=f"Vies : {self.vies}")
        else:
            self.bouton_action.config(state=tk.DISABLED)
            self.label_vies.config(text="Plus de vies !")

# Lancer l'application
if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceJeu(fenetre)
    fenetre.mainloop()


