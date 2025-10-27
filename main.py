"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Point d’entrée du jeu Casse-Brique.

Ce script lance la fenêtre principale Tkinter et affiche le menu d’accueil
(InterfaceAccueil), depuis lequel le joueur peut démarrer une partie ou quitter.
"""

import tkinter as tk
from menu import InterfaceAccueil  # import de la classe du menu d'accueil


def main():
    """
    Fonction principale :
    - Crée la fenêtre Tkinter
    - Initialise le menu d’accueil
    - Démarre la boucle principale (mainloop)
    """
    # Création de la fenêtre principale
    root = tk.Tk()

    # Initialisation du menu principal (InterfaceAccueil)
    InterfaceAccueil(root)

    # Boucle principale Tkinter (événements, affichage, etc.)
    root.mainloop()


# Si le script est exécuté directement (et non importé)
if __name__ == "__main__":
    main()

