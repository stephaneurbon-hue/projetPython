"""
Auteur : Stéphane Urbon et Rayane Zidane
Objectif : Menu d’accueil du jeu Casse-Brique (version séparée du jeu principal).
Ce module gère l’interface d’accueil avec les boutons Jouer et Quitter.
"""

import tkinter as tk
from game import InterfaceJeu  # import de la classe principale du jeu

__all__ = ["InterfaceAccueil"]  # pour que "from menu import InterfaceAccueil" fonctionne


class InterfaceAccueil:
    """
    Classe représentant le menu principal du jeu Casse-Brique.

    Elle crée :
      - une fenêtre d’accueil responsive (qui s’adapte à la taille de l’écran)
      - un titre centré
      - deux boutons : "Jouer" et "Quitter"

    Quand on clique sur "Jouer", le menu se détruit et le jeu démarre immédiatement.
    """

    # ------------------------------------------------------------------
    # Initialisation du menu
    # ------------------------------------------------------------------
    def __init__(self, root):
        """
        Initialise la fenêtre d’accueil et configure son apparence.

        :param root: Fenêtre principale Tkinter (Tk)
        """
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

        # Configuration de la fenêtre
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.configure(bg="#001a33")

        # Titre principal
        self.label_titre = tk.Label(
            root,
            text="Le Casse-Brique Ultime",
            font=("Arial", int(28 * self.scale), "bold"),
            fg="white",
            bg="#001a33",
        )
        self.label_titre.pack(pady=int(100 * self.scale))

        # Bouton "Jouer"
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

        # Bouton "Quitter"
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

    # ------------------------------------------------------------------
    # Lancement du jeu
    # ------------------------------------------------------------------
    def lancer_jeu(self):
        """
        Lance le jeu principal après avoir supprimé le menu d’accueil.
        """
        # Nettoyage du menu
        self.label_titre.destroy()
        self.bouton_jouer.destroy()
        self.bouton_quitter.destroy()

        # Lancer le jeu (InterfaceJeu)
        InterfaceJeu(self.root, self.scale)


