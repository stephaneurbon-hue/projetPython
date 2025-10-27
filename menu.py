"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Menu d'accueil (séparé)
"""

import tkinter as tk
from game import InterfaceJeu

__all__ = ["InterfaceAccueil"]  # pour s'assurer que l'import trouve bien la classe


class InterfaceAccueil:
    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")

        # Échelle responsive (référence 1600x900)
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

        # Bouton Quitter (menu)
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
        # Nettoyage du menu
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.bouton_quitter.destroy()
        # Lancer le jeu (immédiat)
        InterfaceJeu(self.root, self.scale)
