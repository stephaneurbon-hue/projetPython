"""
accueil.py
-----------
Interface d'accueil du jeu Casse-Brique.
Affiche le titre et le bouton "Jouer".
"""

import tkinter as tk
from jeu import InterfaceJeu


class InterfaceAccueil:
    """Classe représentant l'écran d'accueil du jeu Casse-Brique."""

    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")

        # Récupération des dimensions d'écran
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Taille de référence pour le calcul du facteur d'échelle
        self.ref_width = 1600
        self.ref_height = 900

        # Calcul du facteur d'adaptation selon la résolution
        self.scale_x = self.screen_width / self.ref_width
        self.scale_y = self.screen_height / self.ref_height
        self.scale = min(self.scale_x, self.scale_y)

        # Configuration générale de la fenêtre
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#001a33")

        # Titre principal
        self.label_titre = tk.Label(
            root,
            text="Bienvenue dans le Casse-Brique",
            font=("Arial", int(28 * self.scale), "bold"),
            fg="white",
            bg="#001a33",
        )
        self.label_titre.pack(pady=int(100 * self.scale))

        # Bouton pour démarrer le jeu
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
        """Lance l'interface du jeu et détruit l'écran d'accueil."""
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.interface_jeu = InterfaceJeu(self.root, self.scale)
