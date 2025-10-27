"""
Écran d’accueil du Casse-Brique
-------------------------------
Affiche le menu principal avec :
 - "Jouer" → lance la partie
 - "Quitter" → ferme le jeu
"""

import tkinter as tk
from game import GameApp


class MenuApp:
    """Classe du menu principal du jeu Casse-Brique."""

    def __init__(self, root):
        self.root = root
        self.root.title("Casse-Brique")

        # Mise à l’échelle responsive
        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        ref_w, ref_h = 1600, 900
        self.scale = min(screen_w / ref_w, screen_h / ref_h)

        # Fenêtre principale
        self.root.geometry(f"{screen_w}x{screen_h}")
        self.root.configure(bg="#001a33")

        # Titre
        titre = tk.Label(
            root,
            text="🎮 Bienvenue dans le Casse-Brique 🎮",
            font=("Arial", int(36 * self.scale), "bold"),
            fg="white",
            bg="#001a33",
        )
        titre.pack(pady=int(100 * self.scale))

        # Bouton Jouer
        bouton_jouer = tk.Button(
            root,
            text="Jouer",
            font=("Arial", int(24 * self.scale)),
            bg="#004080",
            fg="white",
            width=int(10 * self.scale),
            command=lambda: self.start_game(titre, bouton_jouer, bouton_quitter),
        )
        bouton_jouer.pack(pady=int(30 * self.scale))

        # Bouton Quitter
        bouton_quitter = tk.Button(
            root,
            text="Quitter",
            font=("Arial", int(24 * self.scale)),
            bg="#660000",
            fg="white",
            width=int(10 * self.scale),
            command=root.destroy,
        )
        bouton_quitter.pack(pady=int(10 * self.scale))

    def start_game(self, titre, bouton_jouer, bouton_quitter):
        """Supprime le menu et lance le jeu."""
        titre.destroy()
        bouton_jouer.destroy()
        bouton_quitter.destroy()
        GameApp(self.root, self.scale)
