"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Point d’entrée du jeu Casse-Brique.

Ce script lance la fenêtre principale Tkinter et affiche le menu d’accueil
(InterfaceAccueil), depuis lequel le joueur peut démarrer une partie ou quitter.


!!ATTENTION!! :Pour les ordinateurs portables il faut mettre la fenetre Tkinter en plein écran exclusif pour eviter des problemes de scaling.Une partie du code est concacré a scale la resolution (1600x900) sur l'ecran de l'utilisateur mais ca ne marche pas tout le temps en fonction de l'OS.

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


# Si le script est exécuté directement 
if __name__ == "__main__":
    main()


