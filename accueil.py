import tkinter as tk
from jeu import InterfaceJeu


class Accueil:
    """Écran d'accueil du jeu avec menu Jouer / Quitter."""

    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="#001a33")
        self.frame.pack(fill="both", expand=True)

        self.titre = tk.Label(
            self.frame,
            text="🎮 Casse-Brique 🎮",
            font=("Arial", 40, "bold"),
            fg="white",
            bg="#001a33",
        )
        self.titre.pack(pady=100)

        bouton_jouer = tk.Button(
            self.frame,
            text="Jouer",
            font=("Arial", 24),
            bg="#004080",
            fg="white",
            width=12,
            command=self.lancer_jeu,
        )
        bouton_jouer.pack(pady=20)

        bouton_quitter = tk.Button(
            self.frame,
            text="Quitter",
            font=("Arial", 24),
            bg="#660000",
            fg="white",
            width=12,
            command=root.destroy,
        )
        bouton_quitter.pack(pady=10)

    def lancer_jeu(self):
        self.frame.destroy()
        InterfaceJeu(self.root)
